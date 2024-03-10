import requests
import json
from datetime import datetime

# Constants (Sensitive information like API tokens and IDs should be stored securely and imported from a safe location)
API_TOKEN = 'your_api_token_here'
FILE_ID = 'your_file_id_here'
NODE_ID = 'your_node_id_here'

# Base URL for Figma API
BASE_URL = "https://api.figma.com/v1"

# Headers for API requests
HEADERS = {"X-Figma-Token": API_TOKEN}

def get_figma_node(file_id, node_id):
    """Fetches a specific node from a Figma file."""
    url = f"{BASE_URL}/files/{file_id}/nodes?ids={node_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        exit()

def extract_id_and_name(document):
    """Extracts IDs and names for nodes starting with 'FR_'."""
    extracted_data = []
    if "children" in document:
        for child in document["children"]:
            if child["name"].startswith("FR_"):
                extracted_data.append({"id": child["id"], "name": child["name"]})
    return extracted_data

def fetch_image_urls(file_id, nodes):
    """Fetches image URLs for given nodes."""
    image_urls = []
    for node in nodes:
        node_id = node['id']
        params = {'ids': node_id, 'format': 'png'}
        image_response = requests.get(f"{BASE_URL}/images/{file_id}", headers=HEADERS, params=params)
        
        if image_response.status_code == 200:
            image_data = image_response.json()
            if node_id in image_data['images']:
                image_url = image_data['images'][node_id]
                image_urls.append({
                    "name": node['name'],
                    "id": node_id,
                    "url": image_url,
                    "dateTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
        else:
            print(f"Error fetching image URL for node {node_id}: {image_response.status_code} - {image_response.text}")
    return image_urls

def save_image_urls(image_urls):
    """Saves the list of image URLs to a JSON file."""
    json_file_name = 'image_urls.json'
    with open(json_file_name, 'w', encoding='utf-8') as json_file:
        json.dump(image_urls, json_file, ensure_ascii=False, indent=4)
    print(f"Image URLs saved to {json_file_name}")

# Main script execution
data = get_figma_node(FILE_ID, NODE_ID)
root_document = data["nodes"][NODE_ID]["document"]
extracted_data = extract_id_and_name(root_document)
image_urls = fetch_image_urls(FILE_ID, extracted_data)
save_image_urls(image_urls)
