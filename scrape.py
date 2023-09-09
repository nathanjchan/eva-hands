import requests
import os
import time
import random
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

def save_image(title, img_url, post_index, img_index, page_num):
    
    folder_path = './eva_images/'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '\n']
    for char in invalid_chars:
        title = title.replace(char, '_')

    img_name = f"{page_num}_{title}_{post_index}_{img_index}.jpg"
    img_path = os.path.join(folder_path, img_name)

    urlretrieve(img_url, img_path)
    print(f"Saved image {img_name}...")

def scrape_og_image(image_url, title, post_index, page_num):
    response = requests.get(image_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    og_image = soup.find("meta", property="og:image")
    if og_image:
        img_url = og_image["content"]
        save_image(title, img_url, post_index, 0, page_num)

def scrape_page(page_num):
    url = f'https://shotsofhandsinevangelion.tumblr.com/page/{page_num}'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    posts = soup.find_all('div', class_='post')
    
    for i, post in enumerate(posts):
        content = post.find('div', class_='content')
        if content.find('div', class_='npf_row') is not None:
            paras = content.find_all('p')
            if len(paras) >= 2:
                full_title = "_".join([para.text.strip() for para in paras])
                
                anchor_tags = content.find_all('a', class_='post_media_photo_anchor')
                
                for j, anchor_tag in enumerate(anchor_tags):  
                    img_url = anchor_tag.get('data-big-photo', None)
                    
                    if img_url:
                        print("Long post", img_url)
                        save_image(full_title, img_url, i, j, page_num)
                        
        else:
            paras = content.find_all('p')
            if len(paras) >= 2:
                full_title = "_".join([para.text.strip() for para in paras])
                
                # Finding the 'a' tag within 'content' (not 'post') to fetch 'href' value
                image_link = content.find('a', href=True)
                if image_link:
                    image_url = image_link['href']
                    if image_url.startswith('https://shotsofhandsinevangelion.tumblr.com/image/'):
                        print("Short post", image_url)
                        scrape_og_image(image_url, full_title, i, page_num)

for page in range(0, 139):
    print(f"Scraping page {page}...")
    scrape_page(page)
    
    time_to_sleep = random.randint(5, 10)
    print(f"Waiting for {time_to_sleep} seconds...")
    time.sleep(time_to_sleep)

# after scraping, you will find 3 images that don't belong ;)
