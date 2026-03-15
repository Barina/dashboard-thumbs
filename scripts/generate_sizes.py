import os
import subprocess
import re
import shutil

MAGICK = shutil.which("magick") or shutil.which("convert")
IDENTIFY = shutil.which("identify")
FORMATS = {"webp": ["webp"], "png": ["png"], "gif": ["gif"], "jpg": ["jpg", "jpeg"]}
TARGETS = [512, 256, 128]
pattern = re.compile(r"^(.*?)(?:@(\d+))?\.(\w+)$")


def run(cmd):
    subprocess.run(cmd, check=True)


def get_height(path):
    result = subprocess.check_output([IDENTIFY, "-format", "%h", path])
    return int(result.decode().strip())


def generate(base_path, ext, size, source_height):

    if size >= source_height:
        return

    src = f"{base_path}.{ext}"
    dst = f"{base_path}@{size}.{ext}"

    if os.path.exists(dst):
        return

    run(
        [
            MAGICK,
            src,
            "-coalesce",
            "-resize",
            f"x{size}",
            "-strip",
            "-quality",
            "85",
            dst,
        ]
    )


def process_dir(folder, extensions):

    for f in os.listdir(folder):

        if "@" in f:
            continue

        m = pattern.match(f)
        if not m:
            continue

        name, size, ext = m.groups()

        # ensure file extension is allowed for this folder
        if ext.lower() not in extensions:
            continue

        if size:
            continue

        base = os.path.join(folder, name)
        src = f"{base}.{ext}"

        source_height = get_height(src)

        for target in TARGETS:
            generate(base, ext, target, source_height)


for folder, exts in FORMATS.items():
    if not os.path.isdir(folder):
        continue

    process_dir(folder, exts)
