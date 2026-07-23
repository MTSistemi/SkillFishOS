#!/usr/bin/env python3
# Make eggs honor `produce -K <kernelversion>` for the LIVE medium kernel.
# eggs bugs on Debian: Kernel.vmlinuz(k) ignores its arg (always uname), and
# ovary produce.js calls Utils.vmlinuz() with no arg. We add explicit-kernel
# early returns and pass this.kernel through.
import os, glob, shutil

def _read(path, **kw):
    with open(path, **kw) as f:
        return f.read()

def patch(path, reps, anchor=None):
    s = _read(path, encoding="utf-8")
    if not os.path.exists(path + ".skfbak"):
        shutil.copy(path, path + ".skfbak")
    for a, b in reps:
        if b.split("\n")[0].strip() in s and a not in s:
            print("  already?", path); continue
        if a in s:
            s = s.replace(a, b, 1); print("  OK  :", path, "<-", a[:40])
        else:
            print("  MISS:", path, "<-", a[:40])
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)

# locate files
kjs = [p for p in glob.glob('/usr/lib/penguins-eggs/dist/**/kernel.js', recursive=True)
       if 'vmlinuzFromUname' in _read(p, encoding='utf-8', errors='ignore')]
prods = [p for p in glob.glob('/usr/lib/penguins-eggs/dist/classes/ovary.d/produce.js')]
print("kernel.js:", kjs)
print("produce.js:", prods)

for kj in kjs:
    # Patch A: vmlinuz(kernel) early return
    patch(kj, [(
        "    static vmlinuz(kernel = '') {\n        let kernelFile = '';",
        "    static vmlinuz(kernel = '') {\n        if (kernel !== '' && fs.existsSync(`/boot/vmlinuz-${kernel}`)) {\n            return `/boot/vmlinuz-${kernel}`;\n        }\n        let kernelFile = '';"
    )])
    # Patch B: initramfs(kernel) explicit early return (after targetKernel resolved)
    patch(kj, [(
        "        const kernelVersionShort = targetKernel.split('.').slice(0, 2).join('.');",
        "        if (kernel !== '' && fs.existsSync(`/boot/initrd.img-${kernel}`)) {\n            return `/boot/initrd.img-${kernel}`;\n        }\n        const kernelVersionShort = targetKernel.split('.').slice(0, 2).join('.');"
    )])

for pr in prods:
    # Patch C: pass this.kernel to Utils.vmlinuz
    patch(pr, [(
        "    this.vmlinuz = Utils.vmlinuz();",
        "    this.vmlinuz = Utils.vmlinuz(this.kernel);"
    )])

print("done")
