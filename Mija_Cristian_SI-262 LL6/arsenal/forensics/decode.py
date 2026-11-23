import argparse
import base64
import hashlib
import json
import os
import re
from urllib.parse import unquote


def citibil(b: bytes) -> bool:
    """Verifică dacă toți octeții sunt caractere ASCII imprimabile (32..126)."""
    if not b:
        return False
    return all(32 <= c < 127 for c in b)


def ghici_strat(s: str) -> str:
    """Clasifică șirul după formă: url -> hex -> base64 -> necunoscut."""
    s_curat = s.strip()
    if not s_curat:
        return "necunoscut"

    # 1. URL encoding (%XX)
    if re.search(r"%[0-9a-fA-F]{2}", s_curat):
        return "url"

    # 2. Hex (doar 0-9, a-f/A-F și lungime pară)
    if len(s_curat) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", s_curat):
        return "hex"

    # 3. Base64 (alfabetul standard + padding =, lungime multiplu de 4)
    if len(s_curat) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s_curat):
        return "base64"

    return "necunoscut"


def desfa(s: str) -> tuple[str, bytes]:
    """Desface un singur strat de codare și returnează (tip_strat, octeti_decodati)."""
    s_curat = s.strip()
    strat = ghici_strat(s_curat)

    try:
        if strat == "url":
            return strat, unquote(s_curat).encode("utf-8")
        elif strat == "hex":
            return strat, bytes.fromhex(s_curat)
        elif strat == "base64":
            return strat, base64.b64decode(s_curat)
    except Exception:
        return "necunoscut", s_curat.encode("utf-8")

    return "necunoscut", s_curat.encode("utf-8")


def desfa_straturi(s: str, max_pasi: int = 10) -> tuple[list[str], str]:
    """Decodează iterativ în buclă până când nu mai sunt straturi recunoscute."""
    straturi_gasite = []
    curent = s.strip()

    for _ in range(max_pasi):
        strat, b = desfa(curent)
        if strat == "necunoscut":
            break
        straturi_gasite.append(strat)
        try:
            curent = b.decode("utf-8")
        except UnicodeDecodeError:
            curent = b.hex()
            break

    return straturi_gasite, curent


def sparge_xor(date: bytes) -> tuple[int | None, str | None]:
    """Încearcă toate cele 256 de chei XOR pe un octet și returnează textul citibil."""
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            return k, clar.decode("ascii")
    return None, None


def sparge_hash(tinta: str, cale_wordlist: str = "probe/wordlist.txt") -> tuple[str, str | None]:
    """Identifică algoritmul după lungime și caută parola într-o wordlist."""
    tinta = tinta.strip().lower()
    algoritmi = {32: "md5", 40: "sha1", 64: "sha256"}
    algo = algoritmi.get(len(tinta))
    if not algo:
        return "necunoscut", None

    if not os.path.exists(cale_wordlist):
        return algo, None

    with open(cale_wordlist, "r", encoding="latin1") as f:
        for linie in f:
            cuv = linie.strip()
            if hashlib.new(algo, cuv.encode("utf-8")).hexdigest() == tinta:
                return algo, cuv

    return algo, None


def main():
    p = argparse.ArgumentParser(description="Decoder universal & unealtă forensics (Lab 6)")
    p.add_argument("intrare", help="Șir de decodat sau cale către fișier (cu --fisier)")
    p.add_argument("--fisier", action="store_true", help="Tratează intrarea ca o cale de fișier")
    p.add_argument("--xor", action="store_true", help="Rulează brute-force XOR (1 octet) pe fișier")
    p.add_argument("--hash", action="store_true", help="Sparge hash-urile folosind dicționar")
    p.add_argument("--wordlist", default="probe/wordlist.txt", help="Calea către wordlist")
    args = p.parse_args()

    rezultat_fisa = {}

    if args.xor:
        with open(args.intrare, "rb") as f:
            date = f.read()
        cheie, text_clar = sparge_xor(date)
        print(f"[XOR] Cheie găsită: {cheie} | Mesaj: {text_clar}")
        rezultat_fisa = {"strat": f"xor (cheie={cheie})", "rezultat": text_clar}

    elif args.hash:
        with open(args.intrare, "r", encoding="utf-8") as f:
            linii = [l.strip() for l in f if l.strip()] if args.fisier else [args.intrare.strip()]
        sparte = {}
        for tinta in linii:
            algo, parola = sparge_hash(tinta, args.wordlist)
            print(f"[HASH - {algo.upper()}] {tinta} -> {parola}")
            sparte[tinta] = {"algoritm": algo, "parola": parola}
        rezultat_fisa = {"strat": "hash_dictionary", "rezultat": sparte}

    else:
        if args.fisier:
            with open(args.intrare, "rb") as f:
                continut = f.read().decode("utf-8", errors="ignore").strip()
        else:
            continut = args.intrare

        straturi, text_final = desfa_straturi(continut)
        strat_descriere = " -> ".join(straturi) if straturi else "text_simplu"
        print(f"[DECODE] Straturi: {strat_descriere}")
        print(f"[DECODE] Rezultat: {text_final}")
        rezultat_fisa = {"strat": strat_descriere, "rezultat": text_final}

    os.makedirs("arsenal/forensics", exist_ok=True)
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as out:
        json.dump(rezultat_fisa, out, indent=2, ensure_ascii=False)
    print("[+] Fișa a fost salvată în arsenal/forensics/fisa.json")


if __name__ == "__main__":
    main()