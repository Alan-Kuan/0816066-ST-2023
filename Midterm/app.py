from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

driver_path = ChromeDriverManager().install()

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
# options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(driver_path), options=options)

# Q1

driver.get('https://docs.python.org/3/tutorial/index.html')

# lang_select_el = driver.find_element(By.CSS_SELECTOR, '.language_switcher_placeholder #language_select')
# lang_select = Select(lang_select_el)
# print(lang_select.first_selected_option.text)
# lang_select.select_by_visible_text('Traditional Chinese')

h1 = driver.find_element(By.TAG_NAME, 'h1')
print(h1.text)

p = driver.find_element(By.CSS_SELECTOR, '#the-python-tutorial p')
print(p.text)

# Q2

WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'inline-search')))

search_input = driver.find_element(By.CSS_SELECTOR, '.inline-search input')
search_input.send_keys('class')
search_input.submit()

WebDriverWait(driver, timeout=100) \
    .until(EC.text_to_be_present_in_element(
        (By.CLASS_NAME, 'search-summary'),
        'Search finished, found 432 page(s) matching the search query.')
    )

res_list = driver.find_element(By.CLASS_NAME, 'search')
items = res_list.find_elements(By.TAG_NAME, 'li')

for item in items[:5]:
    link = item.find_element(By.TAG_NAME, 'a')
    print(link.text)
