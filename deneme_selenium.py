import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import random

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem



driver = None
def setup_selenium_driver(user_agent):
    try:
        chrome_options = Options()
        chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Chrome'un kurulu olduğu konumu kontrol edin ve buna göre ayarlayın
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_argument("--no-sandbox")  # Sandbox olmadan çalıştır
        chrome_options.add_argument("--disable-dev-shm-usage")  # Paylaşılan bellek kullanımını kısıtla
        chrome_options.add_argument("--disable-gpu")  # GPU donanım hızlandırmasını devre dışı bırak
        chrome_options.add_argument("--disable-extensions")  # Chrome uzantılarını devre dışı bırak
        # ChromeDriverManager ile driver'ı kur ve options'ı doğru şekilde belirt.
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Driver setup failed: {e}")
        return None

# setup ve test_project_web_site_should_have_correct_title fonksiyonları artık gerekli değil, çünkü onları setup_selenium_driver içinde yönetiyoruz.


user_agent_rotator = UserAgent(software_names=[SoftwareName.CHROME.value],
                               operating_systems=[OperatingSystem.WINDOWS.value], limit=100)
user_agent = user_agent_rotator.get_random_user_agent()
driver = setup_selenium_driver(user_agent)


try:
    # Hedef URL
    url = 'https://letterboxd.com/films/popular/this/week/decade/2020s/'
    driver.get(url)

    # Sayfanın yüklenmesini bekle
    time.sleep(3)  # Sayfanın tamamen yüklenmesi için bekleme süresi

    # Filmleri çek
    films = driver.find_elements(By.CSS_SELECTOR, 'li.listitem.poster-container.film-not-watched')
    for film in films:
        name = film.get_attribute('data-film-name')
        year = film.get_attribute('data-film-release-year')
        print(f"Film Name: {name}, Year: {year}")
finally:
    driver.quit()  # Tarayıcıyı kapat
