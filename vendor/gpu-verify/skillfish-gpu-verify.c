/* prova-silicio — le 40 CU di questa BC-250 calcolano GIUSTO?
 *
 *   prova-silicio calcolo <secondi> [work-items] [giri-interni]
 *   prova-silicio memoria <MB> [passate]
 *
 * PERCHE' NON BASTA UN BANCO DI PROVA NORMALE. clpeak, un gioco, un benchmark:
 * misurano la VELOCITA'. Una CU guasta non e' lenta, e' SBAGLIATA — restituisce
 * un numero diverso da quello che doveva. Con un banco normale non la vedi:
 * i fotogrammi escono, magari con un pixel storto ogni tanto, e tu dai la colpa
 * al gioco. Qui invece si controlla il risultato, e un solo bit fuori posto e'
 * una bocciatura.
 *
 * COME SI SA QUAL E' IL RISULTATO GIUSTO. Due strade, apposta diverse:
 *
 *   1. La catena a NUMERI INTERI si confronta con la stessa catena calcolata
 *      dalla CPU. Gli interi danno lo stesso identico risultato su qualunque
 *      macchina, quindi il confronto e' onesto bit per bit: se la GPU non e'
 *      d'accordo con la CPU, ha sbagliato lei.
 *
 *   2. La catena in VIRGOLA MOBILE si confronta con la PRIMA passata della GPU
 *      stessa, non con la CPU.
 *      ⚠️ E' una scelta, non una pigrizia: in virgola mobile CPU e GPU danno
 *      risultati leggermente diversi in modo del tutto legittimo (la GPU fonde
 *      moltiplicazione e somma in una istruzione sola e arrotonda una volta
 *      invece di due). Confrontarle darebbe differenze continue che non sono
 *      guasti, e a furia di allarmi falsi non si guarderebbe piu' nessun
 *      allarme. Confrontando la GPU con se' stessa, invece, ogni differenza e'
 *      un guasto vero: lo stesso silicio, lo stesso conto, due risultati.
 *
 * CHE COSA VEDE E CHE COSA NO. Vede l'errore che cambia il risultato: una CU
 * marginale che sbaglia sotto calore o tensione bassa, la memoria che perde un
 * bit. NON vede una CU spenta o pigra — quella si vede dai GFLOPS, ed e' un
 * altro conto.
 */
#define CL_TARGET_OPENCL_VERSION 300
#include <CL/cl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <dirent.h>

/* La stessa catena del kernel, in C. Deve restare IDENTICA a quella dentro
 * KERNEL: se si tocca una, si tocca l'altra, o il confronto perde senso. */
static unsigned int catena_intera(unsigned int gid, unsigned int iters, unsigned int seed)
{
    unsigned int x = gid * 2654435761u ^ seed;
    for (unsigned int i = 0; i < iters; i++) {
        x = x * 1664525u + 1013904223u;
        x ^= (x >> 15);
        x = (x << 7) | (x >> 25);
        x += 0x9E3779B9u;
    }
    return x;
}

static const char *KERNEL =
"__kernel void catena(__global uint *oi, __global float *of,\n"
"                     const uint iters, const uint seed)\n"
"{\n"
"    uint gid = get_global_id(0);\n"
"    uint x = gid * 2654435761u ^ seed;\n"
"    float f = 1.0f + (float)(gid & 1023) * 0.000977f;\n"
"    float g = 2.0f;\n"
"    for (uint i = 0; i < iters; i++) {\n"
"        x = x * 1664525u + 1013904223u;\n"
"        x ^= (x >> 15);\n"
"        x = (x << 7) | (x >> 25);\n"
"        x += 0x9E3779B9u;\n"
"        f = f * 1.0000003f + 0.0000001f;\n"
"        g = fma(g, 0.9999997f, 0.0000002f);\n"
"        f = f + g * 1e-7f;\n"
"    }\n"
"    oi[gid] = x;\n"
"    of[gid] = f + g;\n"
"}\n"
"\n"
"__kernel void scrivi(__global uint *b, const uint seed)\n"
"{\n"
"    uint i = get_global_id(0);\n"
"    uint x = i ^ seed;\n"
"    x = x * 2654435761u;\n"
"    x ^= x >> 16;\n"
"    b[i] = x;\n"
"}\n";

static unsigned int schema_memoria(unsigned int i, unsigned int seed)
{
    unsigned int x = i ^ seed;
    x = x * 2654435761u;
    x ^= x >> 16;
    return x;
}

static double adesso(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec / 1e9;
}

/* temperatura e watt della GPU, presi dal kernel: servono per dire A CHE
 * TEMPERATURA il silicio ha sbagliato, che e' meta' della risposta. */
static int hwmon(const char *file)
{
    DIR *d = opendir("/sys/class/hwmon");
    struct dirent *e;
    char p[256], n[64];
    int v = 0;
    if (!d) return 0;
    while ((e = readdir(d))) {
        if (e->d_name[0] == '.') continue;
        snprintf(p, sizeof p, "/sys/class/hwmon/%s/name", e->d_name);
        FILE *f = fopen(p, "r");
        if (!f) continue;
        if (!fgets(n, sizeof n, f)) { fclose(f); continue; }
        fclose(f);
        if (strncmp(n, "amdgpu", 6)) continue;
        snprintf(p, sizeof p, "/sys/class/hwmon/%s/%s", e->d_name, file);
        f = fopen(p, "r");
        if (!f) continue;
        if (fscanf(f, "%d", &v) != 1) v = 0;
        fclose(f);
        break;
    }
    closedir(d);
    return v;
}
#define TEMPC (hwmon("temp1_input") / 1000)
#define WATT  (hwmon("power1_average") / 1000000)

/* La tensione della GPU non sta in hwmon: sta nel registro di debug del driver,
 * scritta come "\t968 mV (VDDGFX)".
 * ⚠️ Serve per distinguere due spiegazioni che da fuori si somigliano — il
 * governor che abbassa la tensione col tempo, e il silicio che cede quando il
 * calore si accumula. Senza questo numero restano in piedi tutte e due, e la
 * prima volta l'ho letta male (cercavo la cifra a inizio riga, ma davanti c'e'
 * una tabulazione) ritrovandomi una colonna vuota e nessuna risposta. */
static int millivolt(void)
{
    FILE *f = fopen("/sys/kernel/debug/dri/0/amdgpu_pm_info", "r");
    char r[256];
    int v = 0;
    if (!f) return 0;
    while (fgets(r, sizeof r, f))
        if (strstr(r, "(VDDGFX)")) { v = atoi(r + strspn(r, " \t")); break; }
    fclose(f);
    return v;
}

#define CHECK(x, dove) do { \
    cl_int _e = (x); \
    if (_e != CL_SUCCESS) { fprintf(stderr, "%s: errore OpenCL %d\n", dove, _e); return 2; } \
} while (0)

static cl_context ctx;
static cl_command_queue coda;
static cl_program prog;
static cl_device_id dev;

static int apri_gpu(void)
{
    cl_platform_id piatt;
    cl_uint n = 0;
    cl_int err;
    if (clGetPlatformIDs(1, &piatt, &n) != CL_SUCCESS || n == 0) {
        fprintf(stderr, "nessuna piattaforma OpenCL. Serve RUSTICL_ENABLE=radeonsi\n");
        return 1;
    }
    if (clGetDeviceIDs(piatt, CL_DEVICE_TYPE_GPU, 1, &dev, &n) != CL_SUCCESS || n == 0) {
        fprintf(stderr, "nessuna GPU OpenCL. Serve RUSTICL_ENABLE=radeonsi\n");
        return 1;
    }
    char nome[256] = "?";
    cl_uint cu = 0;
    clGetDeviceInfo(dev, CL_DEVICE_NAME, sizeof nome, nome, NULL);
    clGetDeviceInfo(dev, CL_DEVICE_MAX_COMPUTE_UNITS, sizeof cu, &cu, NULL);
    printf("GPU: %s\nunita di calcolo viste da OpenCL: %u\n", nome, cu);

    ctx = clCreateContext(NULL, 1, &dev, NULL, NULL, &err);
    if (!ctx) { fprintf(stderr, "contesto: errore %d\n", err); return 1; }
    coda = clCreateCommandQueueWithProperties(ctx, dev, NULL, &err);
    if (!coda) { fprintf(stderr, "coda: errore %d\n", err); return 1; }
    prog = clCreateProgramWithSource(ctx, 1, &KERNEL, NULL, &err);
    if (clBuildProgram(prog, 1, &dev, "-cl-std=CL1.2", NULL, NULL) != CL_SUCCESS) {
        char log[8192] = "";
        clGetProgramBuildInfo(prog, dev, CL_PROGRAM_BUILD_LOG, sizeof log, log, NULL);
        fprintf(stderr, "compilazione del kernel fallita:\n%s\n", log);
        return 1;
    }
    return 0;
}

static int modo_calcolo(int secondi, size_t N, unsigned int iters)
{
    cl_int err;
    unsigned int seed = 0x5F1547;

    printf("\ncalcolo verificato: %zu work-items, %u giri interni, per %d secondi\n",
           N, iters, secondi);

    unsigned int *oro = malloc(N * sizeof(unsigned int));
    unsigned int *gi  = malloc(N * sizeof(unsigned int));
    float        *gf  = malloc(N * sizeof(float));
    float        *rif = malloc(N * sizeof(float));
    if (!oro || !gi || !gf || !rif) { fprintf(stderr, "memoria host\n"); return 2; }

    printf("calcolo il risultato giusto sulla CPU");
    fflush(stdout);
    double t0 = adesso();
    #pragma omp parallel for schedule(static)
    for (long long i = 0; i < (long long)N; i++)
        oro[i] = catena_intera((unsigned int)i, iters, seed);
    printf(" — %.1f s\n", adesso() - t0);

    cl_mem bi = clCreateBuffer(ctx, CL_MEM_WRITE_ONLY, N * sizeof(unsigned int), NULL, &err);
    cl_mem bf = clCreateBuffer(ctx, CL_MEM_WRITE_ONLY, N * sizeof(float), NULL, &err);
    cl_kernel k = clCreateKernel(prog, "catena", &err);
    CHECK(err, "kernel");
    CHECK(clSetKernelArg(k, 0, sizeof bi, &bi), "arg0");
    CHECK(clSetKernelArg(k, 1, sizeof bf, &bf), "arg1");
    CHECK(clSetKernelArg(k, 2, sizeof iters, &iters), "arg2");
    CHECK(clSetKernelArg(k, 3, sizeof seed, &seed), "arg3");

    long giri = 0, sbagli_int = 0, sbagli_float = 0;
    int tmax = 0, wmax = 0, primo_detto = 0;
    double inizio = adesso(), fine = inizio + secondi;

    while (adesso() < fine) {
        CHECK(clEnqueueNDRangeKernel(coda, k, 1, NULL, &N, NULL, 0, NULL, NULL), "avvio");
        CHECK(clEnqueueReadBuffer(coda, bi, CL_TRUE, 0, N * sizeof(unsigned int), gi, 0, NULL, NULL), "lettura int");
        CHECK(clEnqueueReadBuffer(coda, bf, CL_TRUE, 0, N * sizeof(float), gf, 0, NULL, NULL), "lettura float");
        giri++;

        long si = 0, sf = 0;
        for (size_t i = 0; i < N; i++) {
            if (gi[i] != oro[i]) {
                si++;
                if (!primo_detto) {
                    printf("\n  ⚠️ PRIMO ERRORE, giro %ld, work-item %zu: "
                           "la GPU dice 0x%08x, il conto giusto e' 0x%08x, a %d C\n",
                           giri, i, gi[i], oro[i], TEMPC);
                    primo_detto = 1;
                }
            }
        }
        if (giri == 1) {
            memcpy(rif, gf, N * sizeof(float));   /* la prima passata fa da riferimento */
        } else {
            for (size_t i = 0; i < N; i++)
                if (memcmp(&gf[i], &rif[i], sizeof(float))) sf++;
        }
        sbagli_int += si;
        sbagli_float += sf;

        int t = TEMPC, w = WATT;
        if (t > tmax) tmax = t;
        if (w > wmax) wmax = w;
        printf("%6.0fs  giro %-5ld  %4d mV  %2d C  %3d W  errori interi %ld  errori virgola %ld\n",
               adesso() - inizio, giri, millivolt(), t, w, sbagli_int, sbagli_float);
        fflush(stdout);
    }

    printf("\n\n=== esito del calcolo ===\n");
    printf("  giri completati        %ld  (%zu work-items ognuno)\n", giri, N);
    printf("  massimi               %d C, %d W\n", tmax, wmax);
    printf("  errori a numeri interi %ld\n", sbagli_int);
    printf("  errori in virgola      %ld\n", sbagli_float);
    if (sbagli_int == 0 && sbagli_float == 0)
        printf("  ESITO: nessun bit fuori posto in %.0f miliardi di operazioni.\n",
               (double)giri * N * iters * 7.0 / 1e9);
    else
        printf("  ESITO: SILICIO NON AFFIDABILE in questa configurazione.\n");

    free(oro); free(gi); free(gf); free(rif);
    clReleaseMemObject(bi); clReleaseMemObject(bf); clReleaseKernel(k);
    return (sbagli_int || sbagli_float) ? 1 : 0;
}

static int modo_memoria(int mb, int passate)
{
    cl_int err;
    size_t N = (size_t)mb * 1024 * 1024 / sizeof(unsigned int);
    printf("\nmemoria video: %d MB, %d passate\n", mb, passate);

    unsigned int *host = malloc(N * sizeof(unsigned int));
    if (!host) { fprintf(stderr, "memoria host\n"); return 2; }

    cl_mem b = clCreateBuffer(ctx, CL_MEM_READ_WRITE, N * sizeof(unsigned int), NULL, &err);
    if (!b) { fprintf(stderr, "non riesco ad allocare %d MB sulla GPU (errore %d)\n", mb, err); return 2; }
    cl_kernel k = clCreateKernel(prog, "scrivi", &err);
    CHECK(err, "kernel");
    CHECK(clSetKernelArg(k, 0, sizeof b, &b), "arg0");

    long sbagli = 0;
    for (int p = 0; p < passate; p++) {
        unsigned int seed = 0xA5A5 + p * 7919;
        CHECK(clSetKernelArg(k, 1, sizeof seed, &seed), "arg1");
        CHECK(clEnqueueNDRangeKernel(coda, k, 1, NULL, &N, NULL, 0, NULL, NULL), "avvio");
        CHECK(clEnqueueReadBuffer(coda, b, CL_TRUE, 0, N * sizeof(unsigned int), host, 0, NULL, NULL), "lettura");
        long s = 0;
        for (size_t i = 0; i < N; i++)
            if (host[i] != schema_memoria((unsigned int)i, seed)) {
                if (!s) printf("\n  ⚠️ passata %d, parola %zu: letto 0x%08x invece di 0x%08x\n",
                               p + 1, i, host[i], schema_memoria((unsigned int)i, seed));
                s++;
            }
        sbagli += s;
        printf("\rpassata %d/%d  %2d C  %3d W  errori %ld   ", p + 1, passate, TEMPC, WATT, sbagli);
        fflush(stdout);
    }
    printf("\n\n=== esito della memoria ===\n");
    printf("  parole controllate %.0f milioni\n", (double)N * passate / 1e6);
    printf("  errori             %ld\n", sbagli);
    printf("  ESITO: %s\n", sbagli ? "MEMORIA NON AFFIDABILE" : "nessun bit perso.");
    free(host);
    clReleaseMemObject(b); clReleaseKernel(k);
    return sbagli ? 1 : 0;
}

int main(int argc, char **argv)
{
    if (argc < 3) {
        fprintf(stderr,
            "uso:\n"
            "  %s calcolo <secondi> [work-items] [giri-interni]\n"
            "  %s memoria <MB> [passate]\n", argv[0], argv[0]);
        return 2;
    }
    setvbuf(stdout, NULL, _IOLBF, 0);
    if (apri_gpu()) return 2;

    if (!strcmp(argv[1], "calcolo")) {
        size_t N = argc > 3 ? (size_t)atol(argv[3]) : 4u * 1024 * 1024;
        unsigned int it = argc > 4 ? (unsigned int)atol(argv[4]) : 20000;
        return modo_calcolo(atoi(argv[2]), N, it);
    }
    if (!strcmp(argv[1], "memoria"))
        return modo_memoria(atoi(argv[2]), argc > 3 ? atoi(argv[3]) : 10);

    fprintf(stderr, "modo sconosciuto: %s\n", argv[1]);
    return 2;
}
