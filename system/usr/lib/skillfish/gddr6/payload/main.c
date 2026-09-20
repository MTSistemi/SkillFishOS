/* GDDR6 per-chip temperature handler for the BC-250 SMU, with bounded waits.
 *
 * Upstream: onlinermm/BC250-Telemetry, memory/payload/main.c (MIT), itself
 * adapted from pan-Rijovich/bc250-memory-temperature. The sequence below is
 * theirs and is unchanged: MR3 DRAM Info read, one UMC at a time.
 *
 * WHAT WE CHANGED, AND WHY.
 *
 * The upstream handler waits for the memory controller with two loops that have
 * no way out:
 *
 *     while (5      != umc_read(..., 0x53a20 | (umc_id << 20), 2)) {};
 *     while (0x1234 == umc_read(..., 0x53a2c | (umc_id << 20), 2)) {};
 *
 * One MR3 read that never completes and the SMU spins inside the message
 * handler for ever. Queue 3 stops answering and nothing short of a reboot
 * brings it back. Measured on a BC-250 on 19 and 20/09/2026: it happened after
 * 31 min, after 55 min, and once after 5 - the spread of something that has a
 * probability per read, not a budget that runs out.
 *
 * Both waits are counted now. A wait that runs out answers SMU_RETURN_FAILED
 * instead of never answering at all: a reading that fails is one missing
 * sample, a handler that never returns is a dead queue.
 *
 * The chip index is checked too. It arrives from the host through the queue
 * head, and an index outside 0..7 turns into a wild SMN address inside
 * umc_write - a write, not a read. The host validates it, but the host reaches
 * this firmware through a PCI config index/data pair that other programs on the
 * machine use as well, so a value the host never sent can still arrive here.
 * Refusing it costs four instructions.
 *
 * Careful with the two constants below: they are not seconds. The loop runs at
 * whatever the SMU core and its SMN reads manage, and the only thing that
 * matters is that the ceiling stays well under the host's own 5 s mailbox
 * timeout, so the host sees a failed reading rather than a silent one.
 */

extern void queue_write_status_qid(int qid, unsigned int status);
extern void queue_store_word_head_for_qid(int qid, unsigned int data);
extern unsigned int queue_read_head_for_qid(int qid);

extern unsigned int umc_read(int zero, unsigned int addr, int size);
extern void umc_write(int zero, unsigned int addr, unsigned int data, int size);

#define SMU_RETURN_OK      0x01
#define SMU_RETURN_FAILED  0xFF

#define UMC_WAIT_MAX  100000
#define UMC_COUNT     8

void umc_read_temp_per_chip(int qid) {

    unsigned int umc_id = queue_read_head_for_qid(qid);
    unsigned int waited;

    if (umc_id >= UMC_COUNT) {
        queue_write_status_qid(qid, SMU_RETURN_FAILED);
        return;
    }

    umc_write(0, (0x53a24 | (umc_id << 20)), 2, 2);
    umc_write(0, (0x53a1c | (umc_id << 20)), 5, 2);

    for (waited = 0; waited < UMC_WAIT_MAX; waited++)
        if ((int)5 == umc_read(0, (0x53a20 | (umc_id << 20)), 2))
            break;
    if (waited == UMC_WAIT_MAX) {
        queue_write_status_qid(qid, SMU_RETURN_FAILED);
        return;
    }

    for (waited = 0; waited < UMC_WAIT_MAX; waited++)
        if ((int)0x1234 != umc_read(0, (0x53a2c | (umc_id << 20)), 2))
            break;
    if (waited == UMC_WAIT_MAX) {
        queue_write_status_qid(qid, SMU_RETURN_FAILED);
        return;
    }

    queue_store_word_head_for_qid(qid, umc_read(0, (0x53a2c | (umc_id << 20)), 2));
    queue_write_status_qid(qid, SMU_RETURN_OK);
}
