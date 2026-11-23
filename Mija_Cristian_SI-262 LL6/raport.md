# Raport de Laborator 6 — Forensics și Steganografie în Python
**Student:** Mija Cristian (Grupa SI-262)  
**Universitatea Tehnică a Moldovei (UTM)** — FCIM, Securitatea Informațională

---

## 1. Lucrarea A — Decodare, XOR Brute-Force și Spargere Hash-uri (`decode.py`)
* **Decodare multi-strat (`probe/mesaj.txt`):** S-au identificat și desfăcut automat 3 straturi (`base64 -> base64 -> hex`), obținând mesajul clar: `FLAG{straturi_de_encoding}` (salvat în `arsenal/forensics/fisa.json`).
* **Atac Brute-Force XOR (`probe/xor.bin`):** Testând toate cele 256 de chei posibile pe 1 octet, s-a identificat cheia `128` (`0x80`), dezvăluind textul: `Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}`.
* **Dictionary Attack (`probe/hashuri.txt`):** Folosind `probe/wordlist.txt`, s-au spart toate cele 5 hash-uri MD5 (`password`, `dragon`, `qwerty`, `letmein`, `monkey`).
* **Testare automată (`teste/test_decode.py`):** Toate cele 4 teste unitare au trecut cu succes (`4 passed` prin `pytest`).

---

## 2. Lucrarea B — Analiză Binară, EXIF/GPS, File Carving și Steganografie (`forensics.py`, `stego.py`)
* **Magic Bytes & Strings:** S-au verificat semnăturile binare reale (`JPEG`, `PNG`, `ZIP`) și s-au extras șirurile ASCII imprimabile.
* **Metadate EXIF & Coordonate GPS (`probe/foto.jpg`):** Dispozitiv identificat: `Apple iPhone 13` (data `2026:09:14 10:30:00`). Coordonate GPS convertite în grade zecimale: `47.016667 N, 28.8575 E` (Chișinău).
* **File Carving (`probe/ascuns.png`):** S-a detectat semnătura arhivei ZIP (`PK\x03\x04`) concatenată la finalul imaginii PNG, extrăgând fișierul `secret.txt` cu conținutul: `FLAG{ascuns_prin_carving}`.
* **Steganografie LSB (`stego.py` -> `stego.png`):** S-a implementat ascunderea unui mesaj (`FLAG{ascuns_in_pixeli}`) în bitul cel mai puțin semnificativ (LSB) al canalelor RGB și recuperarea ulterioară a acestuia fără alterarea vizibilă a imaginii.
