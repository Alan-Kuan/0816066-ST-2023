from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(service=Service(driver_path), options=options)

driver.get('https://www.nycu.edu.tw')
driver.maximize_window()

news_link = driver.find_element(By.CSS_SELECTOR, 'a[title="新聞"]')
news_link.click()

first_news_link = driver.find_element(By.CSS_SELECTOR, '.su-post a')
first_news_link.click()

title = driver.find_element(By.TAG_NAME, 'h1').text
print(title)

paragraphs = driver.find_elements(By.TAG_NAME, 'p')
for paragraph in paragraphs:
    print(paragraph.text)

driver.switch_to.new_window('tab')
driver.get('https://www.google.com')

search_input = driver.find_element(By.CSS_SELECTOR, 'input[name="q"]')
search_input.send_keys('0816066')
search_input.submit()

second_res = driver.find_elements(By.CLASS_NAME, 'g')[1]
second_res_title = second_res.find_element(By.TAG_NAME, 'h3').text
print(second_res_title)

driver.quit()
