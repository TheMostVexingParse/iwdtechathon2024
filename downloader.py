import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service 

from bs4 import BeautifulSoup
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
# chrome_options.binary_location = r"C:\Users\Computer\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"
driver = webdriver.Chrome(service=Service(r'chromedriver.exe'), options=chrome_options)

def download_video(url, headers, filename):
    
    driver.get(url)
    time.sleep(5)  
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    video_tag = soup.find('video')

    # driver.quit()
    
    if video_tag:
        video_url = video_tag['src']
        print(video_url)
        response = requests.get(video_url, headers=headers)
        if response.status_code - 200 < 100:
            with open(filename, 'wb+') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print("Video downloaded successfully.")
        else:
            print("Failed to download video.")
            print(response)
    else:
        print("Video not found on the page.")

if __name__ == "__main__":
    url =  "https://www.instagram.com/reels/C4FMGCRKWyX/"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "identity;q=1, *;q=0",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Range": "bytes=0-",
        "Referer": "https://www.instagram.com/",
        "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "video",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    download_video(url, headers)

