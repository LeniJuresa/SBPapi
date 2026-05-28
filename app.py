from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ljuresa:11@ucka.veleri.hr/ljuresa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



# MODELI


class Pacijent(db.Model):
    __tablename__ = "Pacijent"

    pacijent_id = db.Column(db.Integer, primary_key=True)
    oib = db.Column(db.String(11), unique=True, nullable=False)
    ime = db.Column(db.String(32), nullable=False)
    prezime = db.Column(db.String(32), nullable=False)
    datum_rodenja = db.Column(db.Date)
    spol = db.Column(db.String(1))
    adresa = db.Column(db.String(64))
    telefon = db.Column(db.String(16))
    email = db.Column(db.String(64))
    lozinka = db.Column(db.String(255), nullable=False)
    pristupacnost = db.Column(db.String(32))
    e_gradani_token = db.Column(db.String(255))
    datum_kreiranja = db.Column(db.Date)


class Lijecnik(db.Model):
    __tablename__ = "Lijecnik"

    lijecnik_id = db.Column(db.Integer, primary_key=True)
    oib = db.Column(db.String(11))
    ime = db.Column(db.String(32))
    prezime = db.Column(db.String(32))
    specijalizacija = db.Column(db.String(64))
    email = db.Column(db.String(64))
    lozinka = db.Column(db.String(255))
    broj_licence = db.Column(db.String(32))
    ustanova_id = db.Column(db.Integer)


class Ustanova(db.Model):
    __tablename__ = "Ustanova"

    ustanova_id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(64))
    adresa = db.Column(db.String(64))
    postanski_broj = db.Column(db.String(16))
    grad = db.Column(db.String(32))
    kontakt_telefon = db.Column(db.String(16))
    email = db.Column(db.String(64))
    pristupacnost = db.Column(db.String(32))


class Termin(db.Model):
    __tablename__ = "Termin"

    termin_id = db.Column(db.Integer, primary_key=True)
    pacijent_id = db.Column(db.Integer, db.ForeignKey("Pacijent.pacijent_id"))
    lijecnik_id = db.Column(db.Integer, db.ForeignKey("Lijecnik.lijecnik_id"))
    ustanova_id = db.Column(db.Integer)
    datum_vrijeme = db.Column(db.DateTime)
    tip_pregleda = db.Column(db.String(32))
    napomena = db.Column(db.String(32))
    video_konzultacija = db.Column(db.Boolean)


class Nalaz(db.Model):
    __tablename__ = "Nalaz"

    nalaz_id = db.Column(db.Integer, primary_key=True)
    termin_id = db.Column(db.Integer, db.ForeignKey("Termin.termin_id"))
    vrsta_nalaza = db.Column(db.String(32))
    datum = db.Column(db.Date)
    opis = db.Column(db.String(255))
    dokument = db.Column(db.String(255))


class Recept(db.Model):
    __tablename__ = "Recept"

    recept_id = db.Column(db.Integer, primary_key=True)
    termin_id = db.Column(db.Integer, db.ForeignKey("Termin.termin_id"))
    lijek = db.Column(db.String(64))
    doza = db.Column(db.String(32))
    trajanje_dani = db.Column(db.Integer)
    napomena = db.Column(db.String(255))
    datum_izdavanja = db.Column(db.Date)


class Podsjetnik(db.Model):
    __tablename__ = "Podsjetnik"

    podsjetnik_id = db.Column(db.Integer, primary_key=True)
    pacijent_id = db.Column(db.Integer, db.ForeignKey("Pacijent.pacijent_id"))
    sadrzaj = db.Column(db.String(255))
    vrijeme = db.Column(db.DateTime)
    poslano = db.Column(db.Boolean)


class Prituzba(db.Model):
    __tablename__ = "Prituzba"

    prituzba_id = db.Column(db.Integer, primary_key=True)
    sadrzaj = db.Column(db.String(255))
    datum = db.Column(db.Date)



# HOME


@app.route("/")
def home():
    return jsonify({"message": "API radi"})




# PACIJENT CRUD


@app.route("/api/pacijenti", methods=["GET"])
def get_pacijenti():
    return jsonify([
        {
            "pacijent_id": p.pacijent_id,
            "oib": p.oib,
            "ime": p.ime,
            "prezime": p.prezime,
            "email": p.email,
            "datum_rodenja": str(p.datum_rodenja) if p.datum_rodenja else None,
            "spol": p.spol,
            "adresa": p.adresa,
            "telefon": p.telefon
        }
        for p in Pacijent.query.all()
    ])


@app.route("/api/pacijenti", methods=["POST"])
def create_pacijent():
    d = request.json
    p = Pacijent(
        oib=d["oib"],
        ime=d["ime"],
        prezime=d["prezime"],
        lozinka=d["lozinka"]
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"message": "Pacijent kreiran"})


@app.route("/api/pacijenti/<int:id>", methods=["PUT"])
def update_pacijent(id):
    p = Pacijent.query.get_or_404(id)
    d = request.json

    p.ime = d.get("ime", p.ime)
    p.prezime = d.get("prezime", p.prezime)
    p.email = d.get("email", p.email)

    db.session.commit()
    return jsonify({"message": "Pacijent ažuriran"})


@app.route("/api/pacijenti/<int:id>", methods=["DELETE"])
def delete_pacijent(id):
    p = Pacijent.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Pacijent obrisan"})




# LIJEČNIK CRUD


@app.route("/api/lijecnici", methods=["GET"])
def get_lijecnici():
    return jsonify([
        {
            "lijecnik_id": l.lijecnik_id,
            "ime": l.ime,
            "prezime": l.prezime,
            "specijalizacija": l.specijalizacija,
            "email": l.email,
            "ustanova_id": l.ustanova_id,
            "oib": l.oib,
            "broj_licence": l.broj_licence,
        }
        for l in Lijecnik.query.all()
    ])


@app.route("/api/lijecnici", methods=["POST"])
def create_lijecnik():
    d = request.json
    l = Lijecnik(
        oib=d["oib"],
        ime=d["ime"],
        prezime=d["prezime"],
        lozinka=d["lozinka"]
    )
    db.session.add(l)
    db.session.commit()
    return jsonify({"message": "Liječnik kreiran"})


@app.route("/api/lijecnici/<int:id>", methods=["PUT"])
def update_lijecnik(id):
    l = Lijecnik.query.get_or_404(id)
    d = request.json

    l.ime = d.get("ime", l.ime)
    l.prezime = d.get("prezime", l.prezime)

    db.session.commit()
    return jsonify({"message": "Liječnik ažuriran"})


@app.route("/api/lijecnici/<int:id>", methods=["DELETE"])
def delete_lijecnik(id):
    l = Lijecnik.query.get_or_404(id)
    db.session.delete(l)
    db.session.commit()
    return jsonify({"message": "Liječnik obrisan"})



# TERMINI (JOIN + FULL READ)


@app.route("/api/termini", methods=["GET"])
def get_termini():
    data = db.session.query(Termin, Pacijent, Lijecnik)\
        .join(Pacijent, Termin.pacijent_id == Pacijent.pacijent_id)\
        .join(Lijecnik, Termin.lijecnik_id == Lijecnik.lijecnik_id)\
        .all()

    return jsonify([
        {
            "termin_id": t.termin_id,
            "datum_vrijeme": str(t.datum_vrijeme),
            "tip_pregleda": t.tip_pregleda,
            "napomena": t.napomena,
            "video_konzultacija": t.video_konzultacija,
            "pacijent": f"{p.ime} {p.prezime}",
            "lijecnik": f"{l.ime} {l.prezime}",
            "pacijent_id": t.pacijent_id,
            "lijecnik_id": t.lijecnik_id,
            "ustanova_id": t.ustanova_id,
            "oib_pacijenta": p.oib,
            "oib_lijecnika": l.oib,
            "broj_licence_lijecnika": l.broj_licence,
            "specijalizacija_lijecnika": l.specijalizacija
        }
        for t, p, l in data
    ])


@app.route("/api/termini", methods=["POST"])
def create_termin():
    d = request.json
    t = Termin(
        pacijent_id=d["pacijent_id"],
        lijecnik_id=d["lijecnik_id"],
        datum_vrijeme=datetime.fromisoformat(d["datum_vrijeme"]),
        tip_pregleda=d.get("tip_pregleda")
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({"message": "Termin kreiran"})


@app.route("/api/termini/<int:id>", methods=["DELETE"])
def delete_termin(id):
    t = Termin.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"message": "Termin obrisan"})



# OSTALO (FULL READ)


@app.route("/api/recepti", methods=["GET"])
def get_recepti():
    return jsonify([
        {
            "recept_id": r.recept_id,
            "lijek": r.lijek,
            "doza": r.doza,
            "trajanje_dani": r.trajanje_dani,
            "napomena": r.napomena,
            "datum_izdavanja": str(r.datum_izdavanja)
        }
        for r in Recept.query.all()
    ])


@app.route("/api/nalazi", methods=["GET"])
def get_nalazi():
    return jsonify([
        {
            "nalaz_id": n.nalaz_id,
            "vrsta_nalaza": n.vrsta_nalaza,
            "opis": n.opis,
            "datum": str(n.datum),
            "dokument": n.dokument,
            "termin_id": n.termin_id
        }
        for n in Nalaz.query.all()
    ])


@app.route("/api/ustanova", methods=["GET"])
def get_ustanove():
    return jsonify([
        {
            "ustanova_id": u.ustanova_id,
            "naziv": u.naziv,
            "grad": u.grad
        }
        for u in Ustanova.query.all()
    ])


@app.route("/api/podsjetnici", methods=["GET"])
def get_podsjetnici():
    return jsonify([
        {
            "podsjetnik_id": p.podsjetnik_id,
            "sadrzaj": p.sadrzaj
        }
        for p in Podsjetnik.query.all()
    ])


@app.route("/api/prituzbe", methods=["GET"])
def get_prituzbe():
    return jsonify([
        {
            "prituzba_id": p.prituzba_id,
            "sadrzaj": p.sadrzaj
        }
        for p in Prituzba.query.all()
    ])



# RUN


if __name__ == "__main__":
    app.run(debug=True)