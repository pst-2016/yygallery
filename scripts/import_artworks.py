"""Import artwork images, create thumbnails, and update data/artworks.json.

Example:
  python scripts/import_artworks.py incoming/artworks
  python scripts/import_artworks.py incoming/artworks --format png
  python scripts/import_artworks.py incoming/artworks --update-manifest

Optional metadata manifest:
  incoming/artworks/artworks.csv

CSV columns:
  filename,id,title,date,medium,description,alt

Supported source formats:
  jpg, png, svg

Supported output formats:
  jpg, png, svg

SVG output is an SVG wrapper around an embedded resized image. It is not vector
tracing.
"""

import argparse
import base64
import csv
import io
import json
import re
import unicodedata
from pathlib import Path

import cairosvg
from PIL import Image, ImageOps


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "data" / "artworks.json"
ARTWORKS_DIR = REPO_ROOT / "assets" / "images" / "artworks"
THUMBS_DIR = ARTWORKS_DIR / "thumbs"
DEFAULT_MANIFEST_NAME = "artworks.csv"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".svg"}
OUTPUT_FORMATS = ("jpg", "png", "svg")
FULL_IMAGE_MAX_SIZE = 1600
THUMB_SIZE = 600
JPEG_QUALITY = 88


def parse_args():
  parser = argparse.ArgumentParser(
    description="Import artwork images and update data/artworks.json."
  )
  parser.add_argument(
    "source_dir",
    type=Path,
    help="Folder containing source artwork images and optional artworks.csv.",
  )
  parser.add_argument(
    "--manifest",
    type=Path,
    help="CSV metadata file. Defaults to <source_dir>/artworks.csv if present.",
  )
  parser.add_argument(
    "--format",
    choices=OUTPUT_FORMATS,
    default="jpg",
    help="Output image format for full images and thumbnails. Defaults to jpg.",
  )
  parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Show what would be imported without writing files.",
  )
  parser.add_argument(
    "--update-manifest",
    action="store_true",
    help="Add missing image rows to the CSV manifest without importing images.",
  )
  return parser.parse_args()


def slugify(value):
  normalized = unicodedata.normalize("NFKD", value)
  ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
  slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value.lower()).strip("-")
  return slug or "artwork"


def title_from_stem(stem):
  words = re.split(r"[-_\s]+", stem.strip())
  return " ".join(word.capitalize() for word in words if word) or "Untitled"


def relative_path(path):
  return path.relative_to(REPO_ROOT).as_posix()


def load_manifest(manifest_path):
  if not manifest_path or not manifest_path.exists():
    return {}

  rows = {}
  with manifest_path.open("r", encoding="utf-8-sig", newline="") as file_obj:
    reader = csv.DictReader(file_obj)
    for row in reader:
      filename = (row.get("filename") or "").strip()
      if not filename:
        raise ValueError("Every manifest row must include a filename.")
      rows[Path(filename).name] = {
        key: (value or "").strip()
        for key, value in row.items()
        if key is not None
      }
  return rows


def default_manifest_path(source_dir):
  return source_dir / DEFAULT_MANIFEST_NAME


def manifest_fieldnames():
  return ["filename", "id", "title", "date", "medium", "description", "alt"]


def load_manifest_rows(manifest_path):
  if not manifest_path.exists():
    return manifest_fieldnames(), []

  with manifest_path.open("r", encoding="utf-8-sig", newline="") as file_obj:
    reader = csv.DictReader(file_obj)
    if not reader.fieldnames:
      return manifest_fieldnames(), []
    return reader.fieldnames, list(reader)


def write_manifest_rows(manifest_path, fieldnames, rows):
  manifest_path.parent.mkdir(parents=True, exist_ok=True)
  with manifest_path.open("w", encoding="utf-8", newline="") as file_obj:
    writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


def build_manifest_row(source_path):
  title = title_from_stem(source_path.stem)
  return {
    "filename": source_path.name,
    "id": slugify(title),
    "title": title,
    "date": "",
    "medium": "",
    "description": "",
    "alt": "",
  }


def update_manifest(source_dir):
  manifest_path = default_manifest_path(source_dir)
  fieldnames, rows = load_manifest_rows(manifest_path)
  required_fields = manifest_fieldnames()
  merged_fieldnames = list(fieldnames)

  for fieldname in required_fields:
    if fieldname not in merged_fieldnames:
      merged_fieldnames.append(fieldname)

  existing_filenames = {
    (row.get("filename") or "").strip()
    for row in rows
    if (row.get("filename") or "").strip()
  }
  added_rows = []

  for source_path in image_files(source_dir):
    if source_path.name in existing_filenames:
      continue
    row = build_manifest_row(source_path)
    rows.append(row)
    added_rows.append(row)

  write_manifest_rows(manifest_path, merged_fieldnames, rows)
  return manifest_path, added_rows


def load_artworks():
  if not DATA_PATH.exists():
    return []

  with DATA_PATH.open("r", encoding="utf-8") as file_obj:
    data = json.load(file_obj)

  if not isinstance(data, list):
    raise ValueError(f"{DATA_PATH} must contain a JSON array.")
  return data


def save_artworks(artworks):
  DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
  with DATA_PATH.open("w", encoding="utf-8") as file_obj:
    json.dump(artworks, file_obj, ensure_ascii=False, indent=2)
    file_obj.write("\n")


def image_files(source_dir):
  return sorted(
    path
    for path in source_dir.iterdir()
    if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
  )


def to_rgb(image):
  if image.mode == "RGB":
    return image

  rgba = image.convert("RGBA")
  background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
  background.alpha_composite(rgba)
  return background.convert("RGB")


def load_source_image(source_path):
  if source_path.suffix.lower() == ".svg":
    png_bytes = cairosvg.svg2png(
      url=str(source_path),
      output_width=FULL_IMAGE_MAX_SIZE,
    )
    with Image.open(io.BytesIO(png_bytes)) as source_image:
      return to_rgb(source_image).copy()

  with Image.open(source_path) as source_image:
    oriented = ImageOps.exif_transpose(source_image)
    return to_rgb(oriented).copy()


def resized_full_image(image):
  resized = image.copy()
  resized.thumbnail((FULL_IMAGE_MAX_SIZE, FULL_IMAGE_MAX_SIZE), Image.Resampling.LANCZOS)
  return resized


def resized_thumbnail(image):
  return ImageOps.fit(
    image,
    (THUMB_SIZE, THUMB_SIZE),
    method=Image.Resampling.LANCZOS,
    centering=(0.5, 0.5),
  )


def save_jpeg(image, output_path):
  output_path.parent.mkdir(parents=True, exist_ok=True)
  image.save(
    output_path,
    "JPEG",
    quality=JPEG_QUALITY,
    optimize=True,
    progressive=True,
  )


def save_png(image, output_path):
  output_path.parent.mkdir(parents=True, exist_ok=True)
  image.save(output_path, "PNG", optimize=True)


def save_svg(image, output_path):
  output_path.parent.mkdir(parents=True, exist_ok=True)
  buffer = io.BytesIO()
  image.save(
    buffer,
    "JPEG",
    quality=JPEG_QUALITY,
    optimize=True,
    progressive=True,
  )
  encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
  width, height = image.size
  svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
    f'  <image width="{width}" height="{height}" '
    f'href="data:image/jpeg;base64,{encoded}" preserveAspectRatio="xMidYMid meet" />\n'
    "</svg>\n"
  )
  output_path.write_text(svg, encoding="utf-8")


def save_output_image(image, output_path, output_format):
  if output_format == "jpg":
    save_jpeg(image, output_path)
  elif output_format == "png":
    save_png(image, output_path)
  elif output_format == "svg":
    save_svg(image, output_path)
  else:
    raise ValueError(f"Unsupported output format: {output_format}")


def build_entry(source_path, metadata, image_path, thumb_path):
  stem = source_path.stem
  title = metadata.get("title") or title_from_stem(stem)
  artwork_id = metadata.get("id") or slugify(title)
  description = metadata.get("description") or ""
  alt = metadata.get("alt") or title

  return {
    "id": slugify(artwork_id),
    "title": title,
    "date": metadata.get("date") or "",
    "medium": metadata.get("medium") or "",
    "image": relative_path(image_path),
    "thumb": relative_path(thumb_path),
    "alt": alt,
    "description": description,
  }


def upsert_artwork(artworks, entry):
  for index, artwork in enumerate(artworks):
    if artwork.get("id") == entry["id"]:
      artworks[index] = entry
      return "updated"

  artworks.append(entry)
  return "added"


def sort_artworks(artworks):
  return sorted(artworks, key=lambda artwork: artwork.get("date") or "", reverse=True)


def import_image(source_path, metadata, output_format, dry_run):
  artwork_id = slugify(metadata.get("id") or metadata.get("title") or source_path.stem)
  image_path = ARTWORKS_DIR / f"{artwork_id}.{output_format}"
  thumb_path = THUMBS_DIR / f"{artwork_id}.{output_format}"
  entry = build_entry(source_path, metadata, image_path, thumb_path)

  if dry_run:
    return entry

  rgb = load_source_image(source_path)
  save_output_image(resized_full_image(rgb), image_path, output_format)
  save_output_image(resized_thumbnail(rgb), thumb_path, output_format)

  return entry


def main():
  args = parse_args()
  source_dir = args.source_dir.resolve()
  manifest_path = args.manifest

  if not source_dir.exists() or not source_dir.is_dir():
    raise SystemExit(f"Source folder does not exist: {source_dir}")

  if args.update_manifest:
    manifest_path, added_rows = update_manifest(source_dir)
    if added_rows:
      for row in added_rows:
        print(f"added manifest row: {row['filename']} -> {row['id']}")
    else:
      print("Manifest already has rows for all images.")
    print(f"Updated {relative_path(manifest_path)}")
    return 0

  if manifest_path is None:
    discovered_manifest = default_manifest_path(source_dir)
    manifest_path = discovered_manifest if discovered_manifest.exists() else None
  else:
    manifest_path = manifest_path.resolve()

  metadata_by_filename = load_manifest(manifest_path)
  sources = image_files(source_dir)
  if not sources:
    raise SystemExit(f"No supported images found in {source_dir}")

  artworks = load_artworks()
  changes = []

  for source_path in sources:
    metadata = metadata_by_filename.get(source_path.name, {})
    entry = import_image(source_path, metadata, args.format, args.dry_run)
    action = upsert_artwork(artworks, entry)
    changes.append((action, source_path.name, entry["id"]))

  artworks = sort_artworks(artworks)
  if not args.dry_run:
    save_artworks(artworks)

  for action, filename, artwork_id in changes:
    print(f"{action}: {filename} -> {artwork_id}")

  if args.dry_run:
    print("Dry run only. No files were changed.")
  else:
    print(f"Updated {relative_path(DATA_PATH)}")


if __name__ == "__main__":
  raise SystemExit(main())
