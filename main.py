import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_image(url, folder_name, image_num):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((150, 150), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        img.save(os.path.join(folder_name, f'image_{image_num}.jpg'))
    except Exception as e:
        print(f"Could not download {url}. Error: {e}")

def scrape_google_images(search_term, num_images, folder_name):
    search_url = f"https://www.google.com/search?q={search_term}&source=lnms&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    create_folder(folder_name)

    count = 0
    page = 0

    while count < num_images:
        params = {"start": page * 20}  # Google Images usually shows 20 images per page
        response = requests.get(search_url, headers=headers, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')

        if not images:
            print("No more images found.")
            break

        for img in images:
            if count >= num_images:
                break
            try:
                img_url = img['src']
                if img_url.startswith('http'):
                    download_image(img_url, folder_name, count)
                    count += 1
            except Exception as e:
                print(f"Could not process image. Error: {e}")

        page += 1  # Move to the next page

    print(f"Downloaded {count} images to {folder_name}")

if __name__ == "__main__":
    search_term = "cute puppies"  # Change this to your search term
    num_images = 1000  # Number of images to download
    folder_name = "safe"

    scrape_google_images(search_term, num_images, folder_name)
