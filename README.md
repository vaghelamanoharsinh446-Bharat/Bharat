# Bharat Search V2

This version adds a small web crawler, robots.txt checking, local indexing and ranked search.

## Run
pip install -r requirements.txt
python build_index.py
python app.py

Then open http://127.0.0.1:5000

## Important
This is a prototype, not a Google-scale crawler. It intentionally indexes only a small seed set and up to 50 pages per run. Respect robots.txt, site terms, server limits, and applicable laws. Before public deployment, replace the example bot contact address with a real monitored contact.

## Next production stages
Distributed crawling, URL frontier, deduplication, persistent search index, language detection, spam/quality ranking, recrawl scheduling, monitoring, rate limits, abuse controls, and scalable hosting.
