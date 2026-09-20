/* GDDR6 per-chip temperature handler for the BC-250 SMU: bounded waits, and
 * four chips per message.
 *
 * Upstream: onlinermm/BC250-Telemetry, memory/payload/main.c (MIT), itself
 * adapted from pan-Rijovich/bc250-memory-temperature. The MR3 sequence is
 * theirs and is unchanged.
 *
 * TWO THINGS WE CHANGED.
 *
 * 1. THE WAITS ARE COUNTED. The upstream handler waits for the memory
 *    controller with two loops that have no way out. One MR3 read that never
 *    completes and the SMU spins inside the message handler for ever - and not
 *    only queue 3 goes: queue 2 times out as well, amdgpu stops getting its
 *    metrics table, the GPU sensors disappear, and the board hard-resets on the
 *    watchdog a couple of minutes later. Measured on a BC-250 after 31 min,
 *    after 55 min, and once after 5.
 *
 * 2. FOUR CHIPS PER MESSAGE. Reading the eight chips used to cost eight
 *    mailbox round trips, each one an opportunity to collide with everything
 *    else that talks to the SMU - our V/F governor several times a second, the
 *    clock sampler, amdgpu itself. A JEDEC temperature code is seven bits, so
 *    four of them fit in the single word the queue gives us back, and eight
 *    round trips become two.
 *
 * THE ARGUMENT SAYS WHICH:
 *
 *     0x00 .. 0x07   one chip, the reading in the low byte, as upstream
 *     0x40           chips 0 1 2 3, one byte each, chip 0 in the low byte
 *     0x41           chips 4 5 6 7, same order
 *     anything else  SMU_RETURN_FAILED, and nothing is touched
 *
 * ⚠️ AN ARGUMENT OF 0x40 SENT TO THE UPSTREAM PAYLOAD HANGS THE SMU: it takes
 * any number it is given, shifts it into an address, and waits for a memory
 * controller that is not there. So the host must only ask for a group when it
 * has verified that this payload is the one installed - which is what
 * patcher.ensure_patch does by comparing the SRAM against the bundled binary,
 * byte for byte, before it returns.
 *
 * ⚠️ NO GLOBALS, AND NOTHING NESTED. The linker puts .data and .bss in the same
 * SRAM window, and nobody initialises them, so an initialised global would hold
 * whatever was there before. And read_one is always_inline on purpose: keeping
 * the call depth exactly what the upstream handler had means the firmware's
 * register windows spill no differently than they already do.
 */

extern void queue_write_status_qid(int qid, unsigned int status);
extern void queue_store_word_head_for_qid(int qid, unsigned int data);
extern unsigned int queue_read_head_for_qid(int qid);

extern unsigned int umc_read(int zero, unsigned int addr, int size);
extern void umc_write(int zero, unsigned int addr, unsigned int data, int size);

#define SMU_RETURN_OK      0x01
#define SMU_RETURN_FAILED  0xFF

/* Not seconds: however fast the SMU core gets through those SMN reads. What
 * matters is that it stays well under the host's 5 s mailbox timeout, so the
 * host sees a failed reading rather than silence. */
#define UMC_WAIT_MAX  100000
#define UMC_COUNT     8
#define GROUP_FIRST   0x40
#define GROUP_SIZE    4

static inline __attribute__((always_inline))
int read_one(unsigned int umc_id, unsigned int *out) {
    unsigned int waited;

    umc_write(0, (0x53a24 | (umc_id << 20)), 2, 2);
    umc_write(0, (0x53a1c | (umc_id << 20)), 5, 2);

    for (waited = 0; waited < UMC_WAIT_MAX; waited++)
        if ((int)5 == umc_read(0, (0x53a20 | (umc_id << 20)), 2))
            break;
    if (waited == UMC_WAIT_MAX)
        return 0;

    for (waited = 0; waited < UMC_WAIT_MAX; waited++)
        if ((int)0x1234 != umc_read(0, (0x53a2c | (umc_id << 20)), 2))
            break;
    if (waited == UMC_WAIT_MAX)
        return 0;

    *out = umc_read(0, (0x53a2c | (umc_id << 20)), 2);
    return 1;
}

void umc_read_temp_per_chip(int qid) {

    unsigned int arg = queue_read_head_for_qid(qid);
    unsigned int value = 0;
    unsigned int packed = 0;
    unsigned int chip;

    if (arg < UMC_COUNT) {
        if (!read_one(arg, &value)) {
            queue_write_status_qid(qid, SMU_RETURN_FAILED);
            return;
        }
        queue_store_word_head_for_qid(qid, value);
        queue_write_status_qid(qid, SMU_RETURN_OK);
        return;
    }

    if (arg == GROUP_FIRST || arg == GROUP_FIRST + 1) {
        unsigned int base = (arg - GROUP_FIRST) * GROUP_SIZE;
        for (chip = 0; chip < GROUP_SIZE; chip++) {
            /* One chip short is the whole group short. The host drops the round
             * either way, and half a group would need a second status to say
             * which half. */
            if (!read_one(base + chip, &value)) {
                queue_write_status_qid(qid, SMU_RETURN_FAILED);
                return;
            }
            packed |= (value & 0xFF) << (chip * 8);
        }
        queue_store_word_head_for_qid(qid, packed);
        queue_write_status_qid(qid, SMU_RETURN_OK);
        return;
    }

    queue_write_status_qid(qid, SMU_RETURN_FAILED);
}
