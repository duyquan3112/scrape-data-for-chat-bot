import os
from app.feats.scraper import getArticles, saveArticlesMarkdown, slugify
from app.feats.upload_vector import uploadVector, createFilePaths
from app.utils.hash import getHash, loadHashes, saveHashes
from app.utils.save_upload_log import logUpdatedResult

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
    if len(articlesToSave) > 0:
        saveArticlesMarkdown(articlesToSave)
    else:
        print("No new or updated articles to save.")

    # Upload only new/updated markdown files
    filePaths = createFilePaths()
    slugs = []
    for article in articlesToSave:
        rawTitle = f"{article.get('id')} {article.get('name') or article.get('title')}"
        slug = slugify(rawTitle)
        slugs.append(slug)

    # Filter out the markdown files that correspond to these slugs
    deltaFilePaths = []
    for filePath in filePaths:
        fileName = os.path.basename(filePath)
        for slug in slugs:
            if slug in fileName:
                deltaFilePaths.append(filePath)
                break
    if deltaFilePaths:
        uploadVector(deltaFilePaths)
    else:
        print("No new or updated files to upload.")

    # Save new hashes
    saveHashes(newHashes)

    # Log result
    logUpdatedResult(added, updated, skipped)