from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import os
import requests
import ffmpeg
from zipfile import ZipFile


x = input("Please enter song title and artist name(if multiple use ','): \n")
listOfSongs = x.split(',')
zipObj = ZipFile('songs.zip', 'w')
for song in listOfSongs:
    dirPath = song

    os.mkdir(dirPath)
    baseLink = 'https://www.youtube.com/results?search_query='
    lst = song.split()
    endpoint = 'https://www.youtube.com/results?search_query='
    for word in lst:
        endpoint = endpoint + word
        endpoint = endpoint + '+'
        print(endpoint)
    endpoint = endpoint + 'Lyric'

    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    driver.get(endpoint)

    try:
        myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ytd-video-renderer")))
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
        myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "no-downloadable")))
        print ("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    downloadLink = driver.find_element_by_class_name('no-downloadable').get_attribute('href')
    print('Dowloading ' + song)
    driver.quit()
    video = requests.get(downloadLink)
    f = open(dirPath + '/song.mp4', 'wb')
    f.write(video.content)
    f.close()
    stream = ffmpeg.input(dirPath + '/song.mp4')
    stream = ffmpeg.output(stream, song +'.mp3')
    ffmpeg.run(stream)
    os.remove(dirPath + '/song.mp4')
    os.rmdir(dirPath)
    zipObj.write(song +'.mp3')
    os.remove(song +'.mp3')

zipObj.close()

