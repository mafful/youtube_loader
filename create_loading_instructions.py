import os
import csv
import shutil
from dotenv import load_dotenv

from settings import input_dir

load_dotenv()

# - - - - - - - - -
# Copy cookies file from the path in the .env to /cookies
# - - - - - - - - -
def copy_cookies_file():
    cookies_file_path = os.getenv('COOKIES_FILE_PATH')
    destination = input_dir

    if cookies_file_path:
        if os.path.exists(cookies_file_path):
            shutil.copy(cookies_file_path, destination)
            print(f"Cookies file copied to: {destination}")
        else:
            print(f"Cookies file not found at: {cookies_file_path}")
    else:
        print("COOKIES_FILE_PATH is not set in the .env file.")


# - - - - - - - - -
# Create Sample CSV
# - - - - - - - - -
def create_sample_csv(sample_data):
    sample_file = os.path.join(input_dir, 'loading_instructions.csv')

    with open(sample_file, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "url"])
        writer.writeheader()
        writer.writerows(sample_data)


if __name__ == '__main__':
    copy_cookies_file()

    sample_data = [
            {"id": 1, "url": "https://www.youtube.com/watch?v=byMQPKC-Uxg"},
            {"id": 2, "url": "https://www.youtube.com/watch?v=PS9lNOySIpI"},
        ]

    create_sample_csv(sample_data)