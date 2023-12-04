from bs4 import BeautifulSoup,Tag
import requests,random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USER_AGENTS = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
]

def get_random_user_agent():
    return {"User-Agent" : random.choice(USER_AGENTS)}

def search(query : str):
    url = f"https://genius.com/search?q={query}"
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(options=firefox_options)
    driver.get(url)
    link = None
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div[1]/search-result-item/div/mini-song-card/a'))
        )
        element = driver.find_element(By.XPATH,'/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div[1]/search-result-item/div/mini-song-card/a')
        link = element.get_attribute('href')
    finally:
        driver.quit()
    return link

def get_lyrics(query):
    song_url = search(query)
    if song_url:
        response = requests.get(song_url,headers=get_random_user_agent())
        if not response.ok:
            raise Exception
        soup = BeautifulSoup(response.text,"html.parser")
        divs = soup.find_all("div",{"data-lyrics-container" : "true"})
        lyrics = ""
        for div in divs:
            br_tags = div.find_all("br")
            for br in br_tags:
                br.replace_with("\n")
            lyrics += div.text
        return lyrics
    else:
        return None

