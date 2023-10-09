import requests
import time
import json
import os

# Assuming the midjourney_api is imported or available in your environment
from midjourney_api import TNL

TNL_API_KEY = os.env("NEXT_LEG_AUTH_TOKEN")
tnl = TNL(TNL_API_KEY)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://midjourney.com/",
}

session = requests.Session()


def check_progress_and_get_image_urls(message_id, prompt):
    image_urls = []
    while True:
        progress_response = tnl.get_message_and_progress(message_id, expire_mins=None)
        print("Progress Response:", progress_response)
        progress = progress_response.get("progress", 0)
        print(f"Progress: {progress}%")
        if progress == 100:
            print("Progress hit 100%!")
            if "imageUrls" in progress_response["response"]:
                image_urls = progress_response["response"]["imageUrls"]
                break
        else:
            time.sleep(5)
    return image_urls


def save_to_image_links(data):
    with open("image-links.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    with open("prompts.json", "r") as f:
        prompts_data = json.load(f)

    all_image_links = []

    for entry in prompts_data:
        hex_id = entry["id"]
        prompt_entries = []

        for prompt_text in entry["prompts"]:
            try:
                response = tnl.imagine(prompt_text)
                print("API Response:", response)

                if response.get("success") and "messageId" in response:
                    message_id = response["messageId"]
                    urls = check_progress_and_get_image_urls(message_id, prompt_text)

                    versions = [
                        {"id": idx + 1, "url": url} for idx, url in enumerate(urls)
                    ]
                    prompt_entry = {"prompt": prompt_text, "versions": versions}
                    prompt_entries.append(prompt_entry)

            except requests.exceptions.RequestException as e:
                print(f"Error during request: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        all_image_links.append({"id": hex_id, "prompts": prompt_entries})

    save_to_image_links(all_image_links)
