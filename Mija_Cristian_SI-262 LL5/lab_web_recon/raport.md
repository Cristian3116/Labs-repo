# Raport de Laborator — Analiza și Recon-ul Aplicațiilor Web în Python
**Student:** Mija Cristian  
**Universitatea Tehnică a Moldovei (UTM)** — FCIM, Specialitatea Securitatea Informațională (SI)  
**Ținta analizată:** `https://cybercor.org`

---

## 1. Structura Proiectului
* `lab_web_recon/etapa1_cereri_baza.py` (`EX 1 – EX 8`): Cereri HTTP de bază prin `requests` și `urllib.request`, limitarea ratei cererilor (`time.sleep(1)`), inspecția modulelor și măsurarea timpului de răspuns (`perf_counter`, `elapsed`).
* `lab_web_recon/etapa2_raspuns_http.py` (`EX 9 – EX 20`): Analiza codurilor HTTP, gestionarea erorilor cu `raise_for_status()`, citirea antetelor, extragerea tagului `<title>`, urmărirea redirecționărilor HTTP→HTTPS (`history`), diferența dintre `HEAD` și `GET`, cookie-uri și sesiuni persistente (`requests.Session`).
* `lab_web_recon/etapa3_functii_sec.py` (`EX 21 – EX 34`): Modularizarea codului cu adnotări de tip (*type hints*) și *docstrings*, auditul antetelor de securitate (`HSTS`, `CSP`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`), parsarea `/robots.txt` și tratarea centralizată a erorilor (`safe_call`).
* `lab_web_recon/etapa4_raport_final.py` (`EX 35 – EX 50`): Parsarea URL-urilor (`urlparse`, `urljoin`), clasificarea linkurilor interne/externe, extragerea imaginilor cu `HTMLParser`, amprentarea paginii prin `SHA-256`, rezoluția DNS (`socket`), verificarea expirării certificatului SSL/TLS (`ssl`) și exportul rezultatelor în `headers.json`, `report.csv` și `report.json`.

---

## 2. Concluzie
Prin parcurgerea celor 50 de exerciții structurate pe patru etape, am dezvoltat un instrument complet de colectare și analiză a informațiilor web în Python. Lucrarea a consolidat utilizarea bibliotecilor pentru rețelistică, parsare HTML și criptografie/TLS, demonstrând importanța configurării corecte a antetelor de securitate și a limitării ratei cererilor în procesul de recunoaștere web.