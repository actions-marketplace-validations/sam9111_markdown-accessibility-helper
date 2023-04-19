import os
import re
import requests
import json

# Post an image to the Azure Cognitive Services Computer Vision API to get a suggested alt text
def suggest_alt_text(image_url,language='en'):
    subscription_key = os.environ['AZURE_SUBSCRIPTION_KEY']
    endpoint = os.environ['AZURE_ENDPOINT']+ 'vision/v3.2/describe'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    data = {'url': image_url}
    params = {'language': language}
    response = requests.post(endpoint, headers=headers, params=params, json=data)
    response_data = json.loads(response.text)
    suggested_alt_text = response_data['description']['captions'][0]['text']
    return suggested_alt_text

# Update the markdown file with the suggested alt text
def update_markdown_file(file_path,language):
    with open(file_path, 'r') as f:
        content = f.read()
        matches = re.findall(r'\!\[(.*?)\]\((.*?)\)(?!\(|\w)', content)
        for match in matches:
            alt_text = match[0]
            image_url = match[1]
            if not alt_text:
                suggested_alt_text = suggest_alt_text(image_url,language)
                content = content.replace(f"![]({image_url})", f"![{suggested_alt_text}]({image_url})")
    with open(file_path, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    repo=os.environ['GITHUB_REPOSITORY']
    repo_name = repo.split('/')[1]
    language = os.environ['ALT_LANGUAGE']
    clone_url = f'https://github.com/{repo}.git'

    if os.environ['CLONE_URL']:
        clone_url = os.environ['CLONE_URL']
    branch = 'main'
    if os.environ['BRANCH']:
        branch = os.environ['BRANCH']

    os.system(f"git clone --depth=1 --branch={branch} {clone_url} repo")
    os.chdir('repo')

    for filename in os.listdir('.'):
        if filename.endswith('.md'):
            update_markdown_file(filename,language)
            os.system(f"git add {filename}")

    # Commit and push changes
    github_username = os.environ['GITHUB_ACTOR']
    os.system(f'git config --global user.email "{github_username}@users.noreply.github.com"')
    os.system(f'git config --global user.name "{github_username}"')
    os.system('git commit -m "Suggest alt text for inline images"')
    token = os.environ['GITHUB_TOKEN']
    os.system(f"git push {clone_url.replace('https://',f'https://{github_username}:{token}@')} {branch}")
