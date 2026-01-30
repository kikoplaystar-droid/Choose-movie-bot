import requests

headers = {
    "User-Agent": "Mozilla/5.0"
}


def save_image(url: str) -> str:
    """Downloads an image from a URL and saves it locally."""
    response = requests.get(url, timeout=15, headers=headers)
    with open("file.jpg", "wb") as file:
        file.write(response.content)
    return "file.jpg"
