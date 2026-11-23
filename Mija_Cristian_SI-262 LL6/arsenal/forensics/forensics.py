import os
import re
import zipfile
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


def tip_real(cale: str) -> str:
    with open(cale, "rb") as f:
        cap = f.read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if cap.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return f"necunoscut ({cap.hex()})"


def extrage_strings(cale: str, lungime_min: int = 6) -> list[str]:
    with open(cale, "rb") as f:
        date = f.read()
    potriviri = re.findall(rb"[ -~]{" + str(lungime_min).encode() + rb",}", date)
    return [m.decode("ascii") for m in potriviri]


def _dms_in_zecimal(dms, ref: str) -> float:
    zecimal = float(dms[0]) + (float(dms[1]) / 60.0) + (float(dms[2]) / 3600.0)
    if ref in ("S", "W"):
        zecimal = -zecimal
    return round(zecimal, 6)


def extrage_exif_gps(cale: str):
    img = Image.open(cale)
    exif_obj = img.getexif()

    print(f"\n--- Metadate EXIF pentru {cale} ---")
    for tag_id, val in exif_obj.items():
        nume_tag = TAGS.get(tag_id, tag_id)
        if nume_tag != "GPSInfo":
            print(f"  {nume_tag}: {val}")

    gps_raw = exif_obj.get_ifd(0x8825)
    gps_info = {GPSTAGS.get(k, k): v for k, v in gps_raw.items()}

    if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
        lat = _dms_in_zecimal(gps_info["GPSLatitude"], gps_info.get("GPSLatitudeRef", "N"))
        lon = _dms_in_zecimal(gps_info["GPSLongitude"], gps_info.get("GPSLongitudeRef", "E"))
        print(f"  [GPS] Latitudine: {lat} | Longitudine: {lon}")
        print(f"  [GPS] Hartă: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon}")
    else:
        print("  [GPS] Nu s-au găsit coordonate GPS.")


def file_carving_zip(cale_imagine: str, cale_iesire: str = "probe/gasit.zip"):
    with open(cale_imagine, "rb") as f:
        date = f.read()

    idx = date.find(b"PK\x03\x04")
    if idx != -1:
        with open(cale_iesire, "wb") as out:
            out.write(date[idx:])
        print(f"\n[CARVING] Arhivă ZIP extrasă de la octetul {idx} în '{cale_iesire}'.")

        os.makedirs("probe/extras_zip", exist_ok=True)
        with zipfile.ZipFile(cale_iesire, "r") as z:
            z.extractall("probe/extras_zip")
            print(f"[CARVING] Conținut dezarhivat: {z.namelist()}")
            for nume in z.namelist():
                cale_f = os.path.join("probe/extras_zip", nume)
                if os.path.isfile(cale_f):
                    print(f"  -> {nume}: {open(cale_f, 'r', errors='ignore').read().strip()}")
    else:
        print("\n[CARVING] Nu s-a găsit nicio arhivă ZIP atașată.")


if __name__ == "__main__":
    print("=== B1. VERIFICARE MAGIC BYTES ===")
    for fisier in ["probe/foto.jpg", "probe/ascuns.png", "probe/xor.bin"]:
        if os.path.exists(fisier):
            print(f"  {fisier} -> {tip_real(fisier)}")

    if os.path.exists("probe/ascuns.png"):
        print("\n=== B2. STRINGS DIN probe/ascuns.png (ultimele 10 șiruri) ===")
        for s in extrage_strings("probe/ascuns.png")[-10:]:
            print(" ", s)

        print("\n=== B4. FILE CARVING ===")
        file_carving_zip("probe/ascuns.png")

    if os.path.exists("probe/foto.jpg"):
        print("\n=== B3. EXIF ȘI GPS ===")
        extrage_exif_gps("probe/foto.jpg")
