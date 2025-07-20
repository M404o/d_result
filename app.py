from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results")
def results():
    return render_template("user_result.html")

@app.route("/email")
def email():
    return render_template("results_email.html")

if __name__ == "__main__":
    app.run(debug=True)
