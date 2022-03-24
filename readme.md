# Wombo AI Art Downloader
Using Selenium to generated multiple pictures from wombo.art and saves them to local drive.

## Requirements
* Python
* Selenium
* Chrome Webdriver
    * [Download from here and place `chromedriver.exe` in same folder as run.py](https://chromedriver.chromium.org/downloads)

## Instructions
Add your queries (strings) to the `queries` parameter (list).

For example 
```javascript
queries = ['Sunset cliffs', 'Never ending flower', 'Fire and water']
```
Will run the script three times, with `Sunset cliffs`, `Never ending flower` and `Fire and water` as inputs