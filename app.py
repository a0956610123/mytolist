"""Flask 应用入口"""
from flask import Flask, render_template
from todolist.api import todolist_bp
from finance.api import finance_bp

app = Flask(__name__)
app.config.from_pyfile("config.py")

app.register_blueprint(todolist_bp)
app.register_blueprint(finance_bp)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/todolist")
def todolist_page():
    return render_template("todolist.html")


@app.route("/finance")
def finance_page():
    return render_template("finance.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
