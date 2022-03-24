import time
import os
import urllib.request
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def startCreating(driver, queryInput, styleNumber):
    styleXpath = "/html/body/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div[2]/div[%s]"%(styleNumber)
    driver.get('https://app.wombo.art')
    searchBox = driver.find_element_by_tag_name("input")
    time.sleep(1)
    searchBox.send_keys(queryInput)
    styleClicker = driver.find_element_by_xpath(styleXpath)
    styleClicker.click()
    time.sleep(1)
    createButton = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div/div[1]/div[2]')
    time.sleep(1)
    createButton.click()
    

def startGenerating(driver, queryInput, styleNumber):
    driver.execute_script("window.open('about:blank', 'tab%s');"%(styleNumber))
    driver.switch_to.window("tab%s"%(styleNumber))
    startCreating(driver, queryInput, styleNumber)
    
    
def openStore(driver, queryInput, styleNumber):
    driver.switch_to.window("tab%s"%(styleNumber))
    success = False
    while success == False:
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div/div/div[1]/div[2]/div/div[2]/div[2]/button/div"))).click()
            success = True
        except TimeoutException:
            print('Timeout exception happened, trying again...')
            startCreating(driver, queryInput, styleNumber)
    time.sleep(1)

def generateFileName(inputPrompt, runner):
    dashedInput = inputPrompt.replace(' ', '-')
    styleDict = ['Pshychedelic', 'Synthwave', 'Ghibli', 'Steampunk', 'Fantasy', 'Vibrant', 'HighDef', 'Psychic', 'DarkFantasy', 'Mystical', 'Baroque', 'Etching', 'Dali', 'Wuhtercuhler', 'Provenance', 'Moonwalker', 'Blacklight', 'NoStyle', 'Ukiyoe']
    styleName = styleDict[runner-1]
    now_ns = str(time.time_ns())
    finalFileName = '%s_%s_%s.jpg'%(dashedInput, styleName, now_ns[-8:-2])
    return finalFileName
    

def getAllStyles(driver, inputString, savePath):
    print('Now generating images with the input: "%s"'%(inputString))
    numberOfStyles = 20 # hardcoded, could be dynamically looked up
    for i in range(1, numberOfStyles):
        startGenerating(driver,inputString, i )

    for j in range(1, numberOfStyles):
        openStore(driver, inputString, j)
    runner = 1
    for k in driver.window_handles:
        driver.switch_to.window(k)
        currentURL = driver.current_url
        if 'shop.wombo.art/products' in currentURL:
            imageObject = driver.find_element_by_xpath('/html/body/main/section/section/div/div[1]/slider-component/ul/li[2]/modal-opener/div/img')
            imageUrl = imageObject.get_attribute("src")
            urlOpener = urllib.request.URLopener()
            fileName = generateFileName(inputString, runner)
            targetFolder = '%s\\'%(savePath) 
            urlOpener.retrieve(imageUrl, targetFolder+fileName)
            runner +=1
    time.sleep(1)
    for k in driver.window_handles:
        driver.switch_to.window(k)
        currentURL = driver.current_url
        if 'wombo' in currentURL:
            driver.close() 
    time.sleep(1)   
    

    
def saveImages(queries):
    savePath = 'generatedImages'
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    for inputString in queries:
        driver = webdriver.Chrome()
        driver.get('about:blank');
        getAllStyles(driver, inputString, savePath)
        driver.quit()
    print('Done with the queries')

queries = ['Sunset cliffs', 'Never ending flower', 'Fire and water']
saveImages(queries)
