from flask import Flask, render_template, request, redirect, url_for, abort
from . import db

PRIORITES = ["faible", "moyenne", "élevée"]
STATUTS = ["nouveau", "en cours", "résolu"]


def create_app():
    app = Flask(__name__)
    db.init_db()

    # 2. Afficher la liste des incidents
    @app.route("/")
    def index():
        with db.get_connection() as conn:
            incidents = conn.execute(
                "SELECT * FROM incidents ORDER BY id DESC"
            ).fetchall()
        return render_template("index.html", incidents=incidents)

    # 1. Ajouter un incident
    @app.route("/incidents/ajouter", methods=["GET", "POST"])
    def ajouter():
        if request.method == "POST":
            titre = request.form["titre"].strip()
            description = request.form["description"].strip()
            lieu = request.form["lieu"].strip()
            priorite = request.form["priorite"]

            if not titre or not description or not lieu or priorite not in PRIORITES:
                return render_template(
                    "ajouter.html", priorites=PRIORITES, erreur="Champs invalides"
                ), 400

            with db.get_connection() as conn:
                conn.execute(
                    "INSERT INTO incidents (titre, description, lieu, priorite) "
                    "VALUES (?, ?, ?, ?)",
                    (titre, description, lieu, priorite),
                )
            return redirect(url_for("index"))
        return render_template("ajouter.html", priorites=PRIORITES)

    # 3. Consulter les détails d'un incident
    @app.route("/incidents/<int:incident_id>")
    def detail(incident_id):
        with db.get_connection() as conn:
            incident = conn.execute(
                "SELECT * FROM incidents WHERE id = ?", (incident_id,)
            ).fetchone()
        if incident is None:
            abort(404)
        return render_template("detail.html", incident=incident, statuts=STATUTS)

    # 4. Modifier le statut
    @app.route("/incidents/<int:incident_id>/statut", methods=["POST"])
    def modifier_statut(incident_id):
        statut = request.form["statut"]
        if statut not in STATUTS:
            abort(400)
        with db.get_connection() as conn:
            conn.execute(
                "UPDATE incidents SET statut = ? WHERE id = ?", (statut, incident_id)
            )
        return redirect(url_for("detail", incident_id=incident_id))

    # 5. Supprimer un incident
    @app.route("/incidents/<int:incident_id>/supprimer", methods=["POST"])
    def supprimer(incident_id):
        with db.get_connection() as conn:
            conn.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
        return redirect(url_for("index"))

    return app
