import os
import json
import hashlib
from datetime import datetime
from app.feats.scraper import getArticles, saveArticlesMarkdown, slugify
from app.feats.upload_vector import uploadVector, createFilePaths

hashesPath = "data/hashes.json"
logPath = "logs/last_run.log"

def getHash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def loadHashes(path=hashesPath):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def saveHashes(hashes, path=hashesPath):
    with open(path, 'w') as f:
        json.dump(hashes, f)

def logResult(added, updated, skipped, logPath=logPath):
    with open(logPath, "a") as f:
        f.write(f"{datetime.now()} - Added: {added}, Updated: {updated}, Skipped: {skipped}\n")
    print(f"Log saved to {logPath}")

if __name__ == "__main__":
    # Scrape articles
    articlesData = getArticles()
    articles = articlesData.get("articles", [])

    # Load old hashes
    oldHashes = loadHashes()
    newHashes = {}
    added, updated, skipped = 0, 0, 0
    articlesToSave = []

    # Detect delta
    for article in articles:
        rawTitle = f"{article.get('id')} {article.get('name') or article.get('title')}"
        slug = slugify(rawTitle)
        body = article.get("body", "")
        hashedBody = getHash(body)
        newHashes[slug] = hashedBody
        if slug not in oldHashes:
            added += 1
            articlesToSave.append(article)
        elif oldHashes[slug] != hashedBody:
            updated += 1
            articlesToSave.append(article)
        else:
            skipped += 1

    # Save only new/updated articles to markdown
    if articlesToSave:
        saveArticlesMarkdown(articlesToSave)
    else:
        print("No new or updated articles to save.")

    # Upload only new/updated markdown files
    filePaths = createFilePaths()
    slugs = [slugify(f"{article.get('id')} {article.get('name') or article.get('title')}") for article in articlesToSave]
    deltaFilePaths = [filePath for filePath in filePaths if any(slug in os.path.basename(filePath) for slug in slugs)]
    if deltaFilePaths:
        uploadVector(deltaFilePaths)
    else:
        print("No new or updated files to upload.")

    # Save new hashes
    saveHashes(newHashes)

    # Log result
    logResult(added, updated, skipped)