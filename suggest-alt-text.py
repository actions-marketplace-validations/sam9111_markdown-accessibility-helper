import os
import re
import requests
import json
import sys

def suggest_alt_text(image_url):
    subscription_key = os.environ['AZURE_SUBSCRIPTION_KEY']
    endpoint = os.environ['AZURE_ENDPOINT']
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'visualFeatures': 'Description'}
    data = {'url': image_url}
    response = requests.post(endpoint, headers=headers, params=params, json=data)
    response_data = json.loads(response.text)
    suggested_alt_text = response_data['description']['captions'][0]['text']
    return suggested_alt_text

def update_markdown_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        matches = re.findall(r'\!\[(.*?)\]\((.*?)\)(?!\(|\w)', content)
        for match in matches:
            alt_text = match[0]
            image_url = match[1]
            if not alt_text:
                suggested_alt_text = suggest_alt_text(image_url)
                content = content.replace(f"![]({image_url})", f"![{suggested_alt_text}]({image_url})")
    with open(file_path, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    clone_url = sys.argv[1]
    branch = sys.argv[2]
    os.system(f"git clone --depth=1 --branch={branch} {clone_url} repo")
    os.chdir('repo')
    for filename in os.listdir('.'):
        if filename.endswith('.md'):
            update_markdown_file(filename)
            os.system(f"git add {filename}")
    os.system('git config --global user.email "<YOUR_GITHUB_EMAIL>"')
    os.system('git config --global user.name "<YOUR_GITHUB_USERNAME>"')
    os.system('git commit -m "Suggest alt text for inline images"')
    os.system(f"git push {clone_url} {branch}")
