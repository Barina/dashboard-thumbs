import os
import json
import yaml
import re

FORMATS = {"webp": ["webp"], "png": ["png"], "gif": ["gif"], "jpg": ["jpg", "jpeg"]}

pattern = re.compile(r"^(.*?)(?:@(\d+))?\.(\w+)$")

index = {}


def scan_format(folder, extensions):

    if not os.path.isdir(folder):
        return

    for f in sorted(os.listdir(folder)):

        m = pattern.match(f)
        if not m:
            continue

        name, size, ext = m.groups()

        if ext.lower() not in extensions:
            continue

        size = int(size) if size else 512

        # normalize format to the folder name
        fmt = folder

        if name not in index:
            index[name] = {"files": {}, "sizes": set(), "formats": set()}

        entry = index[name]

        entry["files"].setdefault(fmt, {})
        entry["files"][fmt][size] = f"{folder}/{f}"

        entry["sizes"].add(size)
        entry["formats"].add(fmt)


def load_metadata():
    meta_dir = "meta"

    if not os.path.isdir(meta_dir):
        return

    for f in sorted(os.listdir(meta_dir)):

        if not (f.endswith(".yml") or f.endswith(".yaml")):
            continue

        path = os.path.join(meta_dir, f)

        with open(path) as fp:
            data = yaml.safe_load(fp)

        name = data.get("name")

        if not name:
            continue

        if name not in index:
            index[name] = {}

        index[name]["meta"] = data


for folder, extensions in FORMATS.items():
    scan_format(folder, extensions)

load_metadata()

# normalize sets
for k in index:

    if "sizes" in index[k]:
        index[k]["sizes"] = sorted(index[k]["sizes"])

    if "formats" in index[k]:
        index[k]["formats"] = sorted(index[k]["formats"])


with open("index.json", "w") as f:
    json.dump(index, f, indent=2)
