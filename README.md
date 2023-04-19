# Markdown Accessibility Helper


This GitHub Action checks if all images in a markdown file have alt text. If any image lacks alt text, it uses the [Microsoft Azure Cognitive Services Computer Vision API (v3.2)](https://westcentralus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-2/operations/56f91f2e778daf14a499f21f) to generate a description of the image in human-readable language with complete sentences. This happens whenever there is a push on the main branch or when a PR is created or updated. The action only runs when there is a commit of a push or PR that changes a markdown file.

## Usage

To use this action, you will need to have the following secrets set up in your repository

#### AZURE_SUBSCRIPTION_KEY: The subscription key for your Azure Cognitive Services resource.

#### AZURE_ENDPOINT: The endpoint for your Azure Cognitive Services resource.

You can also optionally set the following repository variables:

#### ALT_LANGUAGE: The language for the alt text suggested by the API. 

Currently, the API supports the following languages:
- en (English, default)
- es (Spanish)
- ja (Japanese)
- pt (Portuguese)
- zh (Simplified Chinese)

Here is an example workflow that uses this action:
