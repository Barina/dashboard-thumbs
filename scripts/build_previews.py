import json
import os

INDEX_FILE = "index.json"
OUT_FILE = "PREVIEWS.md"

FORMAT_PRIORITY = ["gif", "webp", "png", "jpg"]
SIZE_PRIORITY = [256, 128, 512]


def choose_preview(entry):
    files = entry.get("files", {})

    for fmt in FORMAT_PRIORITY:
        if fmt not in files:
            continue

        sizes = files[fmt]

        for s in SIZE_PRIORITY:
            key = str(s)
            if key in sizes:
                return sizes[key]

        # fallback to any available size
        return list(sizes.values())[0]

    return None


def load_index():
    with open(INDEX_FILE) as f:
        return json.load(f)


def build():

    data = load_index()

    thumbs = []

    for name, entry in data.items():

        preview = choose_preview(entry)

        if not preview:
            continue

        meta = entry.get("meta", {})
        service = meta.get("service") or meta.get("name") or name

        thumbs.append((service, preview))

    thumbs.sort(key=lambda x: x[0].lower())

    with open(OUT_FILE, "w") as f:

        f.write("# Thumb Gallery\n\n")
        f.write("Auto-generated preview gallery.\n\n")

        f.write("<p>")
        for name, img in thumbs:
            f.write(
                f"""
  <a href="{img}">
    <img src="{img}" width="180" alt="{name}">
  </a>"""
            )
        f.write("\n</p>\n")


if __name__ == "__main__":
    build()
