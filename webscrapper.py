import json
import os
import requests
from bs4 import BeautifulSoup
import cloudscraper
import time
import random
import re
def load_last_chapter(name):
    STATE_FILE= f"data/{name}.jsonl"
    if not os.path.exists(STATE_FILE):
        return 0
    
    with open(STATE_FILE, "r") as f:
        data = list(f)[-1]
        chapter = json.loads(data)['chapter'].split()[1]
        return int(chapter)
        
def get_chapter_list(name):
    scraper = cloudscraper.create_scraper()
    r = scraper.get(f"https://novelbin.me/b/{name}")
    soup = BeautifulSoup(r.text, "html.parser")
    match = re.search(r"novelId\s*=\s*['\"]([^'\"]+)", r.text)
    novel_id = match.group(1)
    ajax = scraper.get(
        f"https://novelbin.me/ajax/chapter-archive?novelId={novel_id}"
    )
    soup = BeautifulSoup(ajax.text, "html.parser")
    chapters = soup.select("span.nchr-text.chapter-title")
    return [
    {
        "title": c.text.strip(),
        "url": c.find_parent("a")["href"]
    }
    for c in chapters
    ]

def scrap_chapters(name):
    links = get_chapter_list(name)
    latest = load_last_chapter(name)
    links = links[latest:]
    scraper = cloudscraper.create_scraper()
    
    for item in links:
        for _ in range(3):
            res = scraper.get(item['url'])
            text = res.text
            if "Just a moment..." not in text:
                soup = BeautifulSoup(text, "html.parser")
                body = soup.find(id="chr-content")
                chcontent = [p.get_text(strip=True) for p in body.find_all("p")] 
                with open(f"data/{name}.jsonl","a",encoding="utf-8") as f:
                    data = {
                        "chapter":item['title'],
                        "data":chcontent
                    }
                    f.write(json.dumps(data, ensure_ascii=False) + "\n")
                    print("saved",item['title'])
                    f.flush()
                    break
            time.sleep(random.uniform(5,10))



name = str(input("enter the novel to scrap, use dashes '-' instead of space, ex - 'shadow-slave' : "))
scrap_chapters(name)
