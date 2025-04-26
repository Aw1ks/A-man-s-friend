import requests
import os
import shutil


def download_picture(full_path, url):

    img_response = requests.get(url)
    img_response.raise_for_status()

    with open(full_path, "wb") as file:
        file.write(img_response.content)

    
def main():
    url = 'https://random.dog/woof.json'
    name_folder = "dogs"
    if os.path.exists(name_folder):
        shutil.rmtree(name_folder)    
    os.mkdir(name_folder)

    payload = {'filter': 'mp4,webm'}

    for number in range(50):
        response = requests.get(url, params=payload)
        response.raise_for_status()
        picture_link = response.json()["url"]
        link, picture_extension = os.path.splitext(picture_link)
        file_name = f"dogs_{number+1}{picture_extension}"
        full_path = os.path.join(name_folder, file_name)
        download_picture(full_path, picture_link)


if __name__ == "__main__":
    main()
