from flask import Flask, render_template, request
from cs50 import SQL
from helpers import apology


app = Flask(__name__)

db = SQL("sqlite:///foods.db")

@app.route("/", methods=["GET","POST"])
def index():
    #Redirect to desired food profile (TODO)
    if request.method == "POST":

        searched = request.form.get("food")

        found = db.execute("SELECT id FROM foods WHERE name = ?", searched)
        if not found:
            return apology("Food not found", 404)

        found_row = found[0]
        food_id = found_row['id']

        ketoStatus_index = db.execute("SELECT status FROM KetoStatus WHERE id = (SELECT keto_id FROM foods WHERE id = ?)", food_id)
        whyKeto_index = db.execute("SELECT why FROM Foods WHERE id = ?", food_id)
        NutriInfo = db.execute("SELECT * FROM NutritionalInfo WHERE food_id = ?", food_id)

        #Parameters to send
        food_name = searched.capitalize()
        ketoStatus = ketoStatus_index[0]
        whyKeto = whyKeto_index[0]

        return render_template("food.html", food_name=food_name, ketoStatus=ketoStatus["status"], whyKeto=whyKeto["why"], NutriInfo = NutriInfo)
    else:
        return render_template("index.html")


@app.route("/search", methods=["GET","POST"])
def search():

    food = request.args.get("food")

    if food:
        suggestions = db.execute("SELECT * FROM foods WHERE name LIKE ? LIMIT 8", food + "%")
    else:
        suggestions = []

    return render_template("suggestions.html", suggestions=suggestions)


@app.route("/keto", methods=["GET"])
def keto():
    return render_template("whatisKeto.html")

@app.route("/requestfood", methods=["GET", "POST"])
def foodrequest():
    if request.method == "GET":
        return render_template("requestfood.html")

    else:
        food_requested = request.form.get("food_requested")
        food_description = request.form.get("food_description")
        person_name = request.form.get("person_name")
        person_email = request.form.get("person_email")

        db.execute("INSERT INTO Requests (food_requested, food_description, person_name, person_email) VALUES (?, ?, ?, ?)", food_requested, food_description, person_name, person_email)

        return apology("Success!", 500)

@app.route("/uploadfood", methods=["GET","POST"])
def uploadfood():
    if request.method == "GET":
        return render_template("uploadfood.html")

    else:
        name = request.form.get("name")
        keto_id = int(request.form.get("keto_id"))
        why = request.form.get("why")

        db.execute("INSERT INTO Foods(name, keto_id, why) VALUES(?,?,?)", name, keto_id, why)

        #We need also to get the "food_id"
        found = db.execute("SELECT id FROM Foods WHERE name = ?", name)
        found_row = found[0]
        food_id = found_row['id']

        description = request.form.get("description")
        img_url = request.form.get("img_url")
        calories = float(request.form.get("calories"))
        protein = float(request.form.get("protein"))
        fat = float(request.form.get("fat"))
        carbs = float(request.form.get("carbs"))

        db.execute("INSERT INTO NutritionalInfo(food_id, description, img_url, calories, protein, fat, carbs) VALUES(?,?,?,?,?,?,?)", food_id, description, img_url, calories, protein, fat, carbs)

        return apology("Success!", 500)
