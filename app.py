from flask import Flask, render_template, request
from crawler import search_index

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    q=request.args.get("q","").strip()
    results=search_index(q) if q else []
    return render_template("results.html", q=q, results=results)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
