import json
from selenium import webdriver
import os
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
import time


def download_image_from_url(url, save_path="./", hex_id="", image_number=1):
    # Ensure the save path exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    print(f"Initializing Chrome webdriver for {url}...")

    # Setting up Chrome driver options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--log-level=DEBUG")  # Enable logging

    # Create a Chrome service instance
    service = webdriver.ChromeService(executable_path=binary_path)

    # Initialize the Chrome webdriver with logging
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the URL
    driver.get(url)

    # Save the image
    image_element = driver.find_element(By.TAG_NAME, "img")
    image_url = image_element.get_attribute("src")
    driver.get(image_url)
    filename = f"{hex_id}-{image_number}.png"
    full_save_path = os.path.join(save_path, filename)
    driver.save_screenshot(full_save_path)

    # Close the browser
    driver.quit()

    print(f"Image saved to {full_save_path}.")


def download_images_from_json():
    with open("image-links.json", "r") as f:
        image_links_data = json.load(f)

    for entry in image_links_data:
        hex_id = entry["id"]
        for prompt_entry in entry["prompts"]:
            prompt_text = prompt_entry["prompt"]
            prompt_folder = prompt_text.replace(" ", "-")
            for index, version in enumerate(prompt_entry["versions"], start=1):
                url = version["url"]
                save_path = f"./images/{hex_id}/{prompt_folder}"
                download_image_from_url(
                    url, save_path, hex_id=hex_id, image_number=index
                )
                time.sleep(0.5)


if __name__ == "__main__":
    download_images_from_json()
