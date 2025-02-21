# Paperless-ngx ChatGPT Python Script

This Python script is designed to help you manage and organize your documents using the [Paperless-ngx](https://github.com/the-paperless-project/paperless-ngx) document management system, with the assistance of the OpenAI ChatGPT model. It can be used to automatically rename documents based on their content and to create cleaned copies of documents in a specific directory. This was a helpful script but I no longer use it; I wanted to add local AI support via Ollama. Maybe one day! I made it easy for anyone to update it.

## Prerequisites

Before using this script, make sure you have the following:

- OpenAI API Token (for ChatGPT)
- Paperless API Token (for Paperless-ngx)
- Python 3.x

## Setup

1. Clone or download this repository.

2. Install the required Python libraries using pip:

   ```
   pip install openai requests
   ```

3. Set up your environment variables:

   - `CHATGPT_TOKEN`: Your OpenAI API Token.
   - `PAPERLESS_TOKEN`: Your Paperless API Token.
   - `PAPERLESS_BASE_URL`: The base URL of your Paperless-ngx instance. For example, `https://paperless.domain.com/api`.

   You can set these environment variables in your system or create a `.env` file in the root directory of the project with the following content:

   ```
   CHATGPT_TOKEN=your_chatgpt_api_token
   PAPERLESS_TOKEN=your_paperless_api_token
   PAPERLESS_BASE_URL=https://paperless.domain.com/api
   ```

4. Modify the `search_params` variable in the script to specify the patterns for filtering documents in Paperless-ngx. By default, it is set to `["*"]`, which matches all documents. You can customize this to match specific document titles.

## Usage

### Main Script (main.py)

The `main.py` script performs the following tasks:

- Retrieves all documents from Paperless-ngx.
- Filters documents based on the specified search parameters.
- Uses ChatGPT to suggest a new title for each document based on its content.
- Renames the documents with the suggested title (with retries in case of failure).
- Logs failed renaming attempts in the `error.log` file.

To run the main script, execute the following command:

```
python main.py
```

### Test Script (test-chatgpt.py)

The `test-chatgpt.py` script is designed to generate new names for documents based on their content using ChatGPT. It reads text files from the `content/` directory, suggests new names, and copies the renamed files to the `cleaned-content/` directory.

To use this script, follow these steps:

1. Place the text files you want to rename in the `content/` directory.

2. Run the test script using the following command:

   ```
   python test-chatgpt.py
   ```

   This will generate new names for the files and save them in the `cleaned-content/` directory.

### Paperless Document Retrieval (test-paperless.py)

The `test-paperless.py` script is used to retrieve documents from Paperless-ngx based on search parameters and save their content as text files in the `content/` directory.

To use this script, run it using the following command:

```
python test-paperless.py
```

The script will retrieve and save documents from Paperless-ngx to the `content/` directory based on the specified search parameters.

## Important Notes

- The main script (`main.py`) and the test script (`test-chatgpt.py`) use the OpenAI ChatGPT API to suggest new names for documents. Make sure you have an active API subscription and the necessary API key.

- The scripts assume that you have set up the Paperless-ngx document management system and provided the correct API token.

- Customization: You can customize the search parameters, retry count, and other settings in the scripts to suit your specific requirements.

Feel free to use and modify these scripts to automate your document management workflow with Paperless-ngx and ChatGPT.