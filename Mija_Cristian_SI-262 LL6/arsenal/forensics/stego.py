from PIL import Image


def ascunde_lsb(cale_sursa: str, mesaj: str, cale_destinatie: str = "stego.png"):
    img = Image.open(cale_sursa).convert("RGB")
    px = list(img.getdata())

    date_binare = mesaj.encode("utf-8") + b"\x00"
    biti = "".join(f"{octet:08b}" for octet in date_binare)

    if len(biti) > len(px) * 3:
        raise ValueError("Mesajul este prea lung pentru dimensiunea imaginii!")

    px_nou = []
    idx_bit = 0
    for r, g, b in px:
        canale = [r, g, b]
        for i in range(3):
            if idx_bit < len(biti):
                canale[i] = (canale[i] & ~1) | int(biti[idx_bit])
                idx_bit += 1
        px_nou.append(tuple(canale))

    img_stego = Image.new("RGB", img.size)
    img_stego.putdata(px_nou)
    img_stego.save(cale_destinatie, format="PNG")
    print(f"[STEGO] Mesaj ascuns cu succes în '{cale_destinatie}' ({len(biti)} biți scriși).")


def dezvaluie_lsb(cale_stego: str) -> str:
    img = Image.open(cale_stego).convert("RGB")
    px = list(img.getdata())

    biti = []
    for r, g, b in px:
        biti.extend([str(r & 1), str(g & 1), str(b & 1)])

    octeti = bytearray()
    for i in range(0, len(biti), 8):
        grup = "".join(biti[i : i + 8])
        if len(grup) < 8:
            break
        valoare = int(grup, 2)
        if valoare == 0:
            break
        octeti.append(valoare)

    mesaj_extras = octeti.decode("utf-8", errors="replace")
    print(f"[STEGO] Mesaj dezvăluit din '{cale_stego}': {mesaj_extras}")
    return mesaj_extras


if __name__ == "__main__":
    ascunde_lsb("probe/foto.jpg", "FLAG{ascuns_in_pixeli}", "stego.png")
    dezvaluie_lsb("stego.png")
