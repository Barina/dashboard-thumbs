import os
import subprocess
import re

FORMATS = {
    "webp": "webp",
    "png": "png",
    "gif": "gif",
    "jpg": "jpg",
    "jpg": "jpeg"
}

TARGETS = [512, 256, 128]

pattern = re.compile(r"^(.*?)(?:@(\d+))?\.(webp|png|gif|jpg|jpeg)$")

def run(cmd):
    subprocess.run(cmd, check=True)

def generate(base_path, ext, size):
    src = f"{base_path}.{ext}"
    dst = f"{base_path}@{size}.{ext}"

    if os.path.exists(dst):
        return

    if not os.path.exists(src):
        return

    run([
        "magick",
        src,
        "-coalesce",
        "-resize", f"x{size}",
        "-strip",
        "-quality", "85",
        dst
    ])

def process_dir(folder, ext):
    for f in os.listdir(folder):
        m = pattern.match(f)
        if not m:
            continue

        name, size, extension = m.groups()

        if size:
            continue

        base = os.path.join(folder, name)

        for target in TARGETS:
            generate(base, ext, target)

for folder, ext in FORMATS.items():
    if not os.path.isdir(folder):
        continue

    process_dir(folder, ext)