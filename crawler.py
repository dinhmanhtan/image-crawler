import requests
import time
import logging
import schedule
import argparse
from os import listdir
from os.path import isfile, join
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By



# Set up for logging
logging.basicConfig(filename="crawl.log",
            format='%(asctime)s %(message)s',
            filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

IMAGE_PATH = "images/"
RUN = True

# Get image urls 
def get_urls(url, max_image):

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver = webdriver.Chrome()
    driver.get(url)
    elements = driver.find_elements(By.CLASS_NAME,"etm-media-1-box")

    url_images = set()
    dowloaded_images = list_downloaded_images(IMAGE_PATH)

    for element in elements:
        if len(url_images) < max_image:
            a_tag = element.find_element(By.TAG_NAME,'a')
        
            url_image = a_tag.get_attribute('data-urlimg')
            filename = url_image.split('/')[-1]
            filename = filename.split('?')[0]

            if filename not in dowloaded_images:
                url_images.add(url_image)
                print(f"Found : {url_image}")

    return url_images


# Download images
def get_images(url_images, delay):

    for u in url_images:
        image = requests.get(u)
        filename = u.split('/')[-1]
        filename = filename.split('?')[0]
        print(f"Dowloading {filename} ............................")

        with open(f"images/{filename}","wb") as f:
            f.write(image.content)
            logger.info(f"Download {filename}")
            f.close()

        time.sleep(delay)


# Get list of dowloaded images
def list_downloaded_images(path_image):
    images = [f for f in listdir(path_image) if isfile(join(path_image, f))]

    return images

def main(num_image):

    url = "https://www.24h.com.vn/thoi-trang-c78.html"
    urls = get_urls(url, num_image)
    get_images(urls,0)

if __name__ == "__main__":
    #
    parser = argparse.ArgumentParser(description='Crawl images from https://www.24h.com.vn/thoi-trang-c78.html ')
    parser.add_argument('--s', type=int, help="Run crawler after every S seconds")
    parser.add_argument('--m',type=int, help="Run crawler after every M minutes")
    parser.add_argument('--h',type=int, help="Run crawler after every H hours")
    parser.add_argument('--e',type=str,metavar="HH:MM:SS" ,help="Run crawler every day at specific HH:MM:SS")
    parser.add_argument('--n',type=int,help="The number of images downloaded in one time, default = 3")
    
    args = parser.parse_args()
    num_image = args.n if args.n != None else 3
 
    if not ( (args.s == None and args.h == None and args.m == None) ^ (args.e == None) ) :
        main(num_image)
        print("\nSchedule for crawling by:")
        print("usage: crawler.py [-h] [--s S] [--m M] [--h H] [--e HH:MM:SS]")
        RUN = False

    elif args.e == None:
        main(num_image)
        seconds =  int(args.s) if args.s != None else 0
        minutes =  int(args.m) if args.m != None else 0
        hours =  int(args.h) if args.h != None else 0
        print(f'Run crawler after everry {hours}h,{minutes}m,{seconds}s')
        seconds += minutes*60 + hours*3600
  
        schedule.every(seconds).seconds.do(main,num_image)
    else:
        arr = args.e.split(':')
        if len(arr) != 3:
            print("usage: crawler.py [-h] [--s S] [--m M] [--h H] [--e HH:MM:SS]")
        else:
            hour = arr[0]
            minute = arr[1]
            second = arr[2]
            try:
                schedule.every().day.at(f"{hour}:{minute}:{second}").do(main,num_image)
                print(f"Run crawler at {hour}:{minute}:{second}")
            except NameError:
                # print(NameError)
                print("usage: crawler.py [-h] [--s S] [--m M] [--h H] [--e HH:MM:SS]")

    while RUN:
        schedule.run_pending()
   





