import requests
import json
import os

NEXT_LEG_API_URL = "https://api.thenextleg.io/v2/imagine"
AUTH_TOKEN = os.getenv("NEXT_LEG_AUTH_TOKEN")


def generate_images_from_prompts(prompts):
    results = []

    for prompt in prompts:
        payload = json.dumps(
            {
                "msg": prompt,
                "ref": "",
                "webhookOverride": "",
                "ignorePrefilter": "false",
            }
        )
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json",
        }

        response = requests.post(NEXT_LEG_API_URL, headers=headers, data=payload)
        if response.status_code == 200:
            image_url = response.json().get("data", {}).get("url")
            if image_url:
                save_image_from_url(image_url, prompt)
            results.append(image_url)

    return results


def save_image_from_url(image_url, prompt):
    # Create directory if it doesn't exist
    if not os.path.exists("./images"):
        os.makedirs("./images")

    # Replace special characters in prompt to create a filename
    filename = "".join(e for e in prompt if e.isalnum()) + ".jpg"
    filepath = os.path.join("./images", filename)

    response = requests.get(image_url)
    with open(filepath, "wb") as file:
        file.write(response.content)


if __name__ == "__main__":
    prompts = ["a cute cat driving a pink car, anime style"]
    results = generate_images_from_prompts(prompts)
    print(results)

#     with open("prompts.json", "r") as file:
#         data = json.load(file)
#         prompts = data.get("prompts", [])
#         results = generate_images_from_prompts(prompts)
#         print(results)
