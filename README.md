# SAL Web

Software per la redazione degli Stati di Avanzamento Lavori (SAL) e il controllo dell'avanzamento economico dei cantieri.

Domanda che deve rispondere in pochi secondi: **"Partendo da questo computo, quanto ho già fatto, quanto mi rimane da fare e quanto lavoro sto facendo fuori capitolato?"**

## Riferimenti
- Briefing funzionale: `../Briefing_Software_SAL_Controllo_Avanzamento_Lavori.docx`
- File di test import (esportazione PriMus): `../Via Umberto PRIMUS.xlsx`

## Stack
| Componente | Scelta |
|---|---|
| Backend/API | Python + FastAPI |
| Database | SQLite (un file, backup banale) |
| Frontend | React + Vite (SPA) |
| PDF | ReportLab (generato server-side) |
| Import Excel | openpyxl (profilo PriMus + mappatura manuale) |
| Infrastruttura | FastAPI+uvicorn nativo (no Docker), SPA React precompilata, SQLite su questo PC sempre acceso; accesso remoto via Tailscale (HTTPS automatico ts.net) |

## Requisiti chiave v1
- Multi-cantiere: più schede/cantieri aperti contemporaneamente, sessioni indipendenti.
- Unico computo vivo: CME contrattuale immutabile + colonne di avanzamento affiancate.
- Due modalità di inserimento quantità (progressiva / incrementale); progressiva sempre memorizzata.
- Fuori capitolato / nuove lavorazioni visivamente distinte, totali separati.
- Storico SAL a snapshot immutabili; solo il SAL corrente è modificabile fino al congelamento.
- Dashboard economica + filtri (categoria, lavorazione, stato, contrattuale/fuori capitolato).
- PDF standardizzato: Copertina → Riepilogo → Dettaglio → Chiusura (firme), impaginazione automatica.

## Stato fasi
- [x] **Fase 0** — Setup locale completo: ambiente su questo PC, Tailscale attivo (nodo `salweb`), backup notturno su C:, repo GitHub `GianpietroR/sal-web`
- [ ] Fase 1 — Fondamenta: modello dati ✓, motore app ✓, login + schede multi-cantiere *(in corso)*
- [ ] Fase 2 — Import CME (profilo PriMus testato su Via Umberto + mappatura manuale)
- [ ] Fase 3 — Tabella computo, SAL, quantità, calcoli automatici
- [ ] Fase 4 — Fuori capitolato + dashboard + filtri
- [ ] Fase 5 — Storico e congelamento SAL
- [ ] Fase 6 — PDF standardizzato
- [ ] Fase 7 — Go-live: deploy, collaudo dai due uffici, routine backup
