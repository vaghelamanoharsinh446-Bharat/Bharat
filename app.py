from flask import Flask, request, render_template
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

def load_index():
    try:
        with open(os.path.join(BASE_DIR, "index.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    q = request.args.get("q", "").strip().lower()
    data = load_index()
    results = []

    if q:
        for item in data:
            text = (
                str(item.get("title", "")) + " " +
                str(item.get("text", ""))
            ).lower()
            if q in text:
                results.append(item)

    return render_template("results.html", query=q, results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
