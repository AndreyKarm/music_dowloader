from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import os.path
import time

counter = 0
x = input("Please enter song title: \n")
y = input("Please enter artist name: \n")
lst = x.split() + y.split()
endpoint = ''
for word in lst:
    endpoint = endpoint + word
    endpoint = endpoint + ' '
    print(endpoint)

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
"download.default_directory": "D:\Zagruzchik\python",
"download.prompt_for_download": False,
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True
})
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
driver.get("https://ru-music.com/search/" + endpoint)
delay = 5

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "playlist-btn-down")))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")
elem = driver.find_element_by_class_name('playlist-btn-down')
link = elem.get_attribute('href')
elem.click()
window_after = driver.window_handles[1]
driver.switch_to.window(window_after)
btn = driver.find_element_by_id('dbutton')
btn.click()

closure = y + '-' + x + '.mp3'
while not os.path.exists(closure):
    time.sleep(1)
    counter = counter + 1
    if counter > 20:
        driver.quit()
        break
if os.path.isfile(closure):
    driver.quit()

