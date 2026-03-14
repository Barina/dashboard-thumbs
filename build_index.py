import os
import json
import yaml
import re

FORMATS = ["webp", "png", "gif"]

pattern = re.compile(r"^(.*?)(?:@(\d+))?\.(webp|png|gif)$")

index = {}

def scan_format(fmt):
    folder = fmt

    if not os.path.isdir(folder):
        return

    for f in os.listdir(folder):
        m = pattern.match(f)

        if not m:
            continue

        name, size, ext = m.groups()

        size = int(size) if size else 512

        if name not in index:
            index[name] = {
                "files": {},
                "sizes": set(),
                "formats": set()
            }

        entry = index[name]

        entry["files"].setdefault(ext, {})
        entry["files"][ext][size] = f"{fmt}/{f}"

        entry["sizes"].add(size)
        entry["formats"].add(ext)


def load_metadata():
    meta_dir = "meta"

    if not os.path.isdir(meta_dir):
        return

    for f in os.listdir(meta_dir):
        if not f.endswith(".yml") and not f.endswith(".yaml"):
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


for fmt in FORMATS:
    scan_format(fmt)

load_metadata()

# normalize sets
for k in index:
    if "sizes" in index[k]:
        index[k]["sizes"] = sorted(index[k]["sizes"])

    if "formats" in index[k]:
        index[k]["formats"] = sorted(index[k]["formats"])

with open("index.json", "w") as f:
    json.dump(index, f, indent=2)