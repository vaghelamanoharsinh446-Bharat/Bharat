from crawler import crawl

# Start small and respect each site's robots.txt.
seeds=[
    "https://www.python.org/",
    "https://www.wikipedia.org/",
    "https://developer.mozilla.org/",
    "https://www.india.gov.in/"
]

n=crawl(seeds,max_pages=50)
print(f"Bharat Search indexed {n} pages.")
