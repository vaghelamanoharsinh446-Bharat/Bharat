import json, os, re, time
from collections import deque
from urllib.parse import urljoin, urlparse
from urllib import request
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup

DATA_FILE=os.path.join(os.path.dirname(__file__),"index.json")
USER_AGENT="BharatSearchBot/0.1 (+contact-your-email@example.com)"
MAX_PAGES=50
TIMEOUT=8

def load_index():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE,"r",encoding="utf-8") as f:
        return json.load(f)

def save_index(items):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(items,f,ensure_ascii=False,indent=2)

def clean_text(text):
    return re.sub(r"\s+"," ",text).strip()

def allowed(url, rp_cache):
    p=urlparse(url)
    if p.scheme not in ("http","https") or not p.netloc:
        return False
    root=f"{p.scheme}://{p.netloc}"
    if root not in rp_cache:
        rp=RobotFileParser()
        rp.set_url(root+"/robots.txt")
        try: rp.read()
        except Exception: rp=None
        rp_cache[root]=rp
    rp=rp_cache[root]
    return True if rp is None else rp.can_fetch(USER_AGENT,url)

def crawl(seeds, max_pages=MAX_PAGES):
    queue=deque(seeds)
    seen=set()
    pages=[]
    rp_cache={}

    while queue and len(pages)<max_pages:
        url=queue.popleft()
        if url in seen: continue
        seen.add(url)
        if not allowed(url,rp_cache): continue

        try:
            req=request.Request(url,headers={"User-Agent":USER_AGENT})
            with request.urlopen(req,timeout=TIMEOUT) as resp:
                ctype=resp.headers.get("Content-Type","")
                if "text/html" not in ctype: continue
                data=resp.read(2_000_000)
                charset=resp.headers.get_content_charset() or "utf-8"
                html=data.decode(charset,errors="ignore")
        except Exception:
            continue

        soup=BeautifulSoup(html,"html.parser")
        for tag in soup(["script","style","noscript"]): tag.decompose()
        title=clean_text(soup.title.get_text(" ",strip=True) if soup.title else url)
        desc=""
        meta=soup.find("meta",attrs={"name":re.compile("^description$",re.I)})
        if meta: desc=clean_text(meta.get("content",""))
        text=clean_text(soup.get_text(" ",strip=True))
        if not desc: desc=text[:300]

        pages.append({"title":title[:200],"description":desc[:500],"url":url,"text":text[:5000]})

        for a in soup.find_all("a",href=True):
            nxt=urljoin(url,a["href"]).split("#")[0]
            if nxt.startswith(("http://","https://")) and nxt not in seen:
                queue.append(nxt)
        time.sleep(0.2)

    save_index(pages)
    return len(pages)

def score(item, terms):
    title=item["title"].lower()
    desc=item["description"].lower()
    body=item.get("text","").lower()
    url=item["url"].lower()
    s=0
    for t in terms:
        s += title.count(t)*8
        s += desc.count(t)*4
        s += body.count(t)
        s += url.count(t)*2
    return s

def search_index(q):
    terms=[x for x in re.findall(r"\w+",q.lower()) if len(x)>1]
    if not terms: return []
    rows=[]
    for item in load_index():
        s=score(item,terms)
        if s: rows.append((s,item))
    rows.sort(key=lambda x:x[0],reverse=True)
    return [x[1] for x in rows[:50]]
