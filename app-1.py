from flask import Flask, request, render_template
import json

# HTML files are in the repository root, not inside a templates folder.
app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="/static")


def load_index():
    try:
        with open("index.json", "r", encoding="utf-8") as f:
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
    app.run(host="0.0.0.0", port=5000, debug=True)
