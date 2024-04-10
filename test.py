from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import time


print()
welcome = "Welcome to Job analyzer"
print(welcome)
print("=" * len(welcome))
print()

title = input("Enter your desired job title, keywords, or company: ")
city = input("Enter your desired location, city, province, or 'remote': ")


def get_job_url(title, city):
    title = title.replace(" ", "+")
    city = city.replace(" ", "+")
    # url = f"https://ca.indeed.com/jobs?q={title}&l={city}"
    url = f"https://www.indeed.ca/jobs?q={title}&l={city}"
    return url


url = get_job_url(title, city)


def start_drive(url):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)

    time.sleep(20)



start_drive(url)
