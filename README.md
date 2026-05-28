# Zdravko API – Standalone Python

Bez baze podataka. Svi podaci su u memoriji.

## Pokretanje

```bash
pip install -r requirements.txt
python app.py
```

Server se pokreće na http://localhost:5000

---

## Svi endpointi

### CRUD (POST / GET / PUT / DELETE)

| Entitet    | Base URL            | Filter rute                              |
|------------|---------------------|------------------------------------------|
| Ustanova   | /api/ustanove       | GET /api/ustanove/grad/:grad             |
| Pacijent   | /api/pacijenti      | PATCH /:id/lozinka                       |
| Lijecnik   | /api/lijecnici      | GET /spec/:spec · PATCH /:id/lozinka     |
| Termin     | /api/termini        | GET /pacijent/:id · GET /lijecnik/:id    |
| Nalaz      | /api/nalazi         | GET /pacijent/:id                        |
| Recept     | /api/recepti        | GET /pacijent/:id                        |
| Podsjetnik | /api/podsjetnici    | GET /pacijent/:id · PATCH /:id/poslano   |
| Prituzba   | /api/prituzbe       | GET /pacijent/:id                        |

### Složeni upiti

| URL | Opis |
|-----|------|
| GET /api/query/karton/:pacijent_id | Karton – termini + nalazi + recepti |
| GET /api/query/raspored/:lijecnik_id?datum=YYYY-MM-DD | Raspored liječnika |
| GET /api/query/statistike | Admin dashboard |
| GET /api/query/pretraga?q=tekst | Pretraga pacijenata |
| GET /api/query/video-konzultacije | Budući video termini |
| GET /api/query/podsjetnici-za-slanje | Podsjetnici na čekanju |

---

## Primjeri

```bash
# Svi pacijenti
curl http://localhost:5000/api/pacijenti

# Novi pacijent
curl -X POST http://localhost:5000/api/pacijenti \
  -H "Content-Type: application/json" \
  -d '{"oib":"11111111111","ime":"Petra","prezime":"Babić","datum_rodenja":"1995-03-10","lozinka":"test"}'

# Karton pacijenta 1
curl http://localhost:5000/api/query/karton/1

# Raspored liječnika 1 za 15.6.2025.
curl "http://localhost:5000/api/query/raspored/1?datum=2025-06-15"

# Statistike
curl http://localhost:5000/api/query/statistike
```
