import requests
import os
import shutil
import logging
import hashlib
from urllib.parse import urlparse


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_picture(full_path, url):
    try:
        img_response = requests.get(url, stream=True, timeout=10)  
        img_response.raise_for_status()

        with open(full_path, "wb") as file:
            for chunk in img_response.iter_content(chunk_size=8192):
                file.write(chunk)

        logging.info(f"Изображение успешно загружено: {url} -> {full_path}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при загрузке изображения {url}: {e}")
    except IOError as e:
        logging.error(f"Ошибка при записи файла {full_path}: {e}")

def get_file_extension(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    return os.path.splitext(path)[1]

def main():
    url = 'https://random.dog/woof.json'
    name_folder = "dogs"

    try:
        if os.path.exists(name_folder):
            shutil.rmtree(name_folder)
        os.makedirs(name_folder, exist_ok=True)  

        payload = {'filter': 'mp4,webm'}

        for number in range(50):
            try:
                response = requests.get(url, params=payload, timeout=5)
                response.raise_for_status()
                picture_link = response.json()["url"]

                picture_extension = get_file_extension(picture_link)
                if not picture_extension:
                    logging.warning(f"Не удалось определить расширение файла для {picture_link}")
                    continue

                file_name = f"dogs_{number+1}{picture_extension}"
                full_path = os.path.join(name_folder, file_name)
                download_picture(full_path, picture_link)

            except requests.exceptions.RequestException as e:
                logging.error(f"Ошибка при запросе {url}: {e}")
            except ValueError as e:
                logging.error(f"Ошибка при обработке JSON: {e}")

    except OSError as e:
        logging.error(f"Ошибка при работе с директорией {name_folder}: {e}")

if __name__ == "__main__":
    main()