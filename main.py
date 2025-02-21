import os
import requests
import re
import fnmatch
from openai import OpenAI

# Load environment variables
CHATGPT_TOKEN = os.getenv("CHATGPT_TOKEN")
PAPERLESS_TOKEN = os.getenv("PAPERLESS_TOKEN")
PAPERLESS_BASE_URL = os.getenv("PAPERLESS_BASE_URL")
client = OpenAI(api_key=CHATGPT_TOKEN)

# Ensure that tokens are available
if not CHATGPT_TOKEN or not PAPERLESS_TOKEN:
    raise ValueError("Environment variables for tokens are not set")

# Set search parameters to get all documents
search_params = ["*"]

# Maximum number of retries for renaming a failed document
MAX_RETRIES = 3


def get_all_documents():
    headers = {"Authorization": f"Token {PAPERLESS_TOKEN}"}
    url = f"{PAPERLESS_BASE_URL}/documents/"
    documents = []
    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        for doc in data.get("results", []):
            documents.append(
                {
                    "id": doc["id"],
                    "title": doc["title"],
                    "content": doc.get("content", ""),
                }
            )
        url = data.get("next")
    return documents


def filter_documents(documents, search_params):
    filtered_docs = []
    for doc in documents:
        for pattern in search_params:
            if fnmatch.fnmatch(doc["title"], pattern):
                filtered_docs.append(doc)
                break
    return filtered_docs


def sanitize_filename(name):
    # Remove invalid characters and replace spaces with underscores
    return re.sub(r'[\\/*?:"<>|]', "", name)


def generate_pdf_name(ocr_content):
    formatted_content = ocr_content.replace("\n", " ")
    try:
        # Prompt for generating a PDF title based on OCR content
        prompt = f"""
        Please suggest a descriptive and unique document title. 
        Spaces are preferred over underscores. 
        First, correct any spelling mistakes in the following content, then suggest the title: {formatted_content}
        """

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {"role": "user", "content": ""},
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        if response and response.choices:
            suggested_name = response.choices[0].message.content.strip()
            if "unable to suggest" not in suggested_name:
                return sanitize_filename(suggested_name)
            else:
                return "Unable_To_Suggest_Title"
        else:
            return "No_Response"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error_Generated_Title"


def rename_pdf(document_id, new_name):
    headers = {"Authorization": f"Token {PAPERLESS_TOKEN}"}
    data = {"title": new_name}
    response = requests.patch(
        f"{PAPERLESS_BASE_URL}/documents/{document_id}/", headers=headers, data=data
    )
    return response.ok


def main():
    documents = get_all_documents()
    filtered_documents = filter_documents(documents, search_params)

    # Create a dictionary to store the number of retries for each document
    retry_counts = {doc["id"]: 0 for doc in filtered_documents}

    for doc in filtered_documents:
        # Retry renaming a failed document up to MAX_RETRIES times
        while retry_counts[doc["id"]] < MAX_RETRIES:
            ocr_content = doc["content"]
            new_name = generate_pdf_name(ocr_content)

            if new_name and rename_pdf(doc["id"], new_name):
                print(f"Renamed document {doc['id']} to {new_name}")
                break  # Rename successful, move to the next document
            else:
                retry_counts[doc["id"]] += 1
                print(f"Retry {retry_counts[doc['id']]} for document {doc['id']}")

        # Log failed documents
        if retry_counts[doc["id"]] == MAX_RETRIES:
            with open("error.log", "a") as error_log:
                error_log.write(
                    f"Failed to rename document {doc['id']} after {MAX_RETRIES} retries\n"
                )


if __name__ == "__main__":
    main()
