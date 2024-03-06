# api: https://m.comic.naver.com/webtoon/detail?titleId=793275&no=15&week=sat&listSortOrder=ASC&listPage=1
import requests
from bs4 import BeautifulSoup
import os
import sys

# Validate arguments
if len(sys.argv) < 5:
    print("Usage: python image_fetcher.py --api <api_url> --fname <folder_name>")
    sys.exit(1)

api_url = None
folder_name = None

# Extract arguments
for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == "--api":
        api_url = sys.argv[i + 1]
    elif sys.argv[i] == "--fname":
        folder_name = sys.argv[i + 1]

if not api_url or not folder_name:
    print("Missing required arguments: --api or --fname")
    sys.exit(1)

# Get the request
response = requests.get(api_url)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    image_tags = soup.find_all("img", class_="fx2 lazy toon_image", id=lambda x: x and x.startswith("toon_"))

    os.makedirs(folder_name, exist_ok=True)  # Create the folder if it doesn't exist

    for image_tag in image_tags:
        image_url = image_tag["src"]
        image_filename = image_url.split("/")[-1]
        image_filepath = os.path.join(folder_name, image_filename)

        with open(image_filepath, "wb") as f:
            image_response = requests.get(image_url, stream=True)
            for chunk in image_response.iter_content(1024):
                f.write(chunk)

        print(f"Image saved: {image_filepath}")

else:
    print("API request failed with status code:", response.status_code)