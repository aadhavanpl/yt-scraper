from selenium import webdriver
import time
from bs4 import BeautifulSoup

PATH = "/usr/bin/chromedriver"

channel_name = input("Enter channel name: ")
channel = "https://youtube.com/c/" + channel_name + "/videos"

def sort_popular():
    return channel + "?view=0&sort=p&flow=grid"

def sort_old():
    return channel + "?view=0&sort=da&flow=grid"

def sort_new():
    return channel + "?view=0&sort=dd&flow=grid"

option = input("\nSort by...\n(1) -> Date added (newest)\n(2) -> Date added (oldest)\n(3) -> Most popular\nOption: ")

if option=='1':
    channel = sort_new()
    option = "newest"
elif option=='2':
    channel = sort_old()
    option = "oldest"
else:
    channel = sort_popular()
    option = "popular"

print(channel)

driver = webdriver.Chrome(PATH)
driver.get(channel)

#scroll to bottom
height = driver.execute_script("return document.documentElement.scrollHeight;")
while True:
    prev_height = driver.execute_script("return document.documentElement.scrollHeight;")
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)
    height = driver.execute_script("return document.documentElement.scrollHeight;")
    if prev_height==height:
        break

content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content, 'lxml')

titles = soup.findAll('a', id='video-title')

#for i, title in enumerate(titles):
#    print(f"{i}: {title.text}")

views_and_times = soup.findAll('span', class_="style-scope ytd-grid-video-renderer")

#for i, view in enumerate(views_and_times):
#    print(f"{i}: {view.text}")

urls = soup.findAll('a', id='video-title')

#for i, url in enumerate(urls):
#    print(f"{i}: {url.get('href')}")

f = open(f"output/{channel_name}_{option}.txt", "x")

i, j = 0, 0

for title in titles:
    f = open(f"output/{channel_name}_{option}.txt", "a")
    f.write(f"{title.text}\n{views_and_times[i].text} {views_and_times[i+1].text}\nhttps://www.youtube.com{urls[j].get('href')}\n\n")
    i+=2
    j+=1
