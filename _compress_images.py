import os
import shutil
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent
backup = root / "_img_backup"
backup.mkdir(exist_ok=True)


def size_kb(p):
    return os.path.getsize(p) / 1024


for path in sorted(root.iterdir()):
    if not path.is_file():
        continue
    ext = path.suffix.lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        continue

    orig = size_kb(path)
    bak = backup / path.name
    if not bak.exists():
        shutil.copy2(path, bak)

    img = Image.open(path)
    img.load()
    name_lower = path.name.lower()
    is_logo = name_lower in {"logo.png", "favicon.png"}

    if is_logo:
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        img.save(path, "PNG", optimize=True)
    elif ext == ".png":
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
        if max(img.size) > 1600:
            img.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        img.save(path, "PNG", optimize=True, compress_level=9)
    else:
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        if max(img.size) > 1920:
            img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
        img.save(path, "JPEG", quality=82, optimize=True, progressive=True)

    new = size_kb(path)
    print(f"{path.name}: {orig:.0f} KB -> {new:.0f} KB")

print("Backup:", backup)
