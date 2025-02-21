import os
import requests
import fnmatch

# Load environment variables
PAPERLESS_TOKEN = os.getenv("PAPERLESS_TOKEN")
PAPERLESS_BASE_URL = os.getenv("PAPERLESS_BASE_URL")

# Ensure that the token is available
if not PAPERLESS_TOKEN:
    raise ValueError("Paperless token is not set")

if not PAPERLESS_BASE_URL:
    raise ValueError("Paperless base URL is not set")

# Set search parameters
search_params = ["Scan*", "PDF*"]


# Function to get all documents from Paperless with pagination
def get_all_documents():
    headers = {"Authorization": f"Token {PAPERLESS_TOKEN}"}
    url = f"{PAPERLESS_BASE_URL}/documents/"

    documents = []
    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        documents.extend(data.get("results", []))
        url = data.get("next")
    return documents


# Function to filter documents based on search parameters
def filter_documents(documents, search_params):
    filtered_docs = []
    for doc in documents:
        for pattern in search_params:
            if fnmatch.fnmatch(doc["title"], pattern):
                filtered_docs.append(doc)
                break
    return filtered_docs


def save_document_content(file_name, content):
    os.makedirs("content", exist_ok=True)  # Ensure the content directory exists
    with open(f"content/{file_name}.txt", "w", encoding="utf-8") as file:
        file.write(content)


def main():
    all_documents = get_all_documents()
    filtered_documents = filter_documents(all_documents, search_params)

    for doc in filtered_documents:
        # Use the 'content' field directly
        doc_content = doc.get("content", "")
        save_document_content(doc["title"], doc_content)
        print(
            f"Saved content for Document ID: {doc['id']} to content/{doc['title']}.txt"
        )


if __name__ == "__main__":
    main()
