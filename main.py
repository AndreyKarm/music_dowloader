from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
import requests
import ffmpeg

counter = 0
x = input("Please enter song title: \n")
y = input("Please enter artist name: \n")
dirPath = x + y
os.mkdir(dirPath)
baseLink = 'https://www.youtube.com/results?search_query='
lst = x.split() + y.split()
endpoint = 'https://www.youtube.com/results?search_query='
for word in lst:
    endpoint = endpoint + word
    endpoint = endpoint + '+'
    print(endpoint)

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
"download.default_directory": "D:\Zagruzchik\python",
"download.prompt_for_download": False,
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True
})
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
driver.get(endpoint)
delay = 10

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "ytd-video-renderer")))
    print ("Page is ready!")
except TimeoutException:
    corrected = driver.find_element_by_class_name('yt-search-query-correction')
    corrected.click()
    print("Loading took too much time!")
elem = driver.find_element_by_class_name('ytd-thumbnail')
link = elem.get_attribute('href')
begining = link[:12]
ending = link[link.find("?") + 1 : ]
forSavefromnet = begining + 'ss' + 'youtube.com/watch?' + ending
driver.get(forSavefromnet)
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "no-downloadable")))
    print ("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")
downloadLink = driver.find_element_by_class_name('no-downloadable').get_attribute('href')
print(downloadLink)
driver.quit()
video = requests.get(downloadLink)
f = open(dirPath + '/song.mp4', 'wb')
f.write(video.content)
stream = ffmpeg.input(dirPath + '/song.mp4')
stream = ffmpeg.output(stream, 'output.mp3')
ffmpeg.run(stream)

