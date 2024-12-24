import requests
import os
import re

username = 'Kimmy1209'

# GraphQL query to fetch anime lists
query = '''
query ($username: String) {
  MediaListCollection(userName: $username, type: ANIME) {
    lists {
      name
      entries {
        media {
          title {
            romaji
          }
          coverImage {
            large
          }
        }
      }
    }
  }
}
'''

# Anilist API endpoint
url = 'https://graphql.anilist.co'

# Function to clean the filename
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# Download an image
def download_image(url, file_name):
    response = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(response.content)

response = requests.post(url, json={'query': query, 'variables': {'username': username}})

if response.status_code == 200:
    data = response.json()
    anime_lists = data['data']['MediaListCollection']['lists']

    # Create a folder for storing images
    if not os.path.exists('anime_images'):
        os.makedirs('anime_images')

    # Iterate over lists (watching, completed, planning)
    for anime_list in anime_lists:
        list_name = anime_list['name']
        print(f"Downloading images from list: {list_name}")

        # Create a subfolder for each list
        list_folder = os.path.join('anime_images', list_name)
        if not os.path.exists(list_folder):
            os.makedirs(list_folder)

        # Download images for each anime in the list
        for entry in anime_list['entries']:
            anime_title = sanitize_filename(entry['media']['title']['romaji'])
            image_url = entry['media']['coverImage']['large']
            file_name = os.path.join(list_folder, f"{anime_title}.jpg")
            download_image(image_url, file_name)
            print(f"Downloaded: {anime_title}")
else:
    print("Failed to fetch the anime list.")
