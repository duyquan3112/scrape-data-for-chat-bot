import html2text
from bs4 import BeautifulSoup
import re

# Clean html: remove nav, ads, etc.
def cleanHtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Remove nav, ads (assume class/id contains nav, ad, ads)
    for tag in soup.find_all(['nav', 'aside']):
        tag.decompose()
    for tag in soup.find_all(True, {'class': re.compile(r'(nav|ad|ads)', re.I)}):
        tag.decompose()
    for tag in soup.find_all(True, {'id': re.compile(r'(nav|ad|ads)', re.I)}):
        tag.decompose()
    return str(soup)

# Convert html to markdown
def convertHtmlToMarkdown(html):
    cleanedHtml = cleanHtml(html)
    converter = html2text.HTML2Text()
    converter.ignore_links = False  # Keep link
    converter.ignore_images = False
    converter.body_width = 0
    converter.protect_links = True
    converter.ignore_emphasis = False
    converter.bypass_tables = False
    converter.ignore_tables = False
    converter.single_line_break = True
    converter.inline_links = False
    converter.use_automatic_links = False
    converter.escape_all = False
    converter.unicode_snob = True
    md = converter.handle(cleanedHtml)
    return md.strip()
