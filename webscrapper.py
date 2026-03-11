import json
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cloudscraper

STATE_FILE= "state.json"


def load_last_chapter(name):
    if not os.path.exists(STATE_FILE):
        return 0
    
    with open(STATE_FILE, "r") as f:
        data = json.load(f)
        return data[name]

def save_last_chapter(chapter,name):
    with open(STATE_FILE, "w") as f:
        json.dump({name: chapter}, f)
        
def chapter_list(name):
    driver = webdriver.Chrome()
    driver.get(f"https://novelbin.me/b/{name}")
    driver.implicitly_wait(2)
    chapter_title = driver.find_element(by=By.CLASS_NAME , value = "tab-chapters-title")
    chapter_title.click()
    chapter_list = driver.find_element(by=By.CLASS_NAME, value = "list-chapter")
    print(chapter_list)
    
chapter_list("shadow-slave")