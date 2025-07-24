import requests

from app.api.api_endpoint import GET_ARTICLES_ENDPOINT
from app.config.app_config import BASE_URL
from app.utils.convert_markdown import convertHtmlToMarkdown
import os
import re

# Convert title to slug: "How to use Optisigns" -> "how-to-use-optisigns"
def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\-\_\s]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text.strip('-_')

# Save articles to markdown file in data/markdown folder
# Example: "[id]-[name].md" => "1-how-to-use-optisigns.md"
def saveArticlesMarkdown(articles, out_dir='data/markdown'):
    os.makedirs(out_dir, exist_ok=True)
    for article in articles:
        rawTitle =  f"{article.get('id')} {article.get('name') or article.get('title')}"
        slug = slugify(rawTitle)
        md = convertHtmlToMarkdown(article.get('body', ''))
        filePath = os.path.join(out_dir, f"{slug}.md")
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(md)
    print(f"Saved {len(articles)} articles to {out_dir}")

# Get articles from API
# Example: https://support.optisigns.com/api/v2/help_center/en-us/articles.json?per_page=100&sort_by=position&sort_order=desc
def getArticles():
    params = {"per_page": 100, "sort_by": "position", "sort_order": "desc"}
    try:
        print(f"Getting articles...")
        url = f"{BASE_URL}{GET_ARTICLES_ENDPOINT}"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print(f"Get articles successed")
            print("URL: ", response.url)
            data = response.json()
            return data
        else:
            print(f"Failed: {response.status_code}")
            print(response.text)
            return {}
    except Exception as e:
        print(f"Failed: {e}")
