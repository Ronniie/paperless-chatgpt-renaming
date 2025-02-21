import os
import requests
import shutil
import openai
from openai import OpenAI
import re

client = OpenAI(api_key=os.getenv("CHATGPT_TOKEN"))


def sanitize_filename(name):
    # Remove invalid characters from the file name
    return re.sub(r'[\\/*?:"<>|]', "", name)


def generate_pdf_name(file_content):
    formatted_content = file_content.replace("\n", " ")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Suggest a new name for a document with the following content: "
                    + formatted_content[:500],
                },
                {"role": "user", "content": ""},
                {
                    "role": "assistant",
                    "content": '"Energetic Greetings: An Expressive Salutation"',
                },
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        print("Response Object:", response)
        if response and response.choices:
            suggested_name = response.choices[0].message.content.strip()
            if "unable to suggest" not in suggested_name:
                # Sanitize the suggested file name
                sanitized_name = sanitize_filename(suggested_name)
                return sanitized_name + ".txt"
            else:
                return "Unable_To_Suggest_Name.txt"
        else:
            return "No_Response.txt"
    except Exception as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)


def main():
    content_dir = "content/"
    cleaned_content_dir = "cleaned-content/"

    # Create the cleaned content directory if it doesn't exist
    if not os.path.exists(cleaned_content_dir):
        os.makedirs(cleaned_content_dir)

    # Process each file in the content directory
    for filename in os.listdir(content_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(content_dir, filename)

            # Read the content of the file
            with open(file_path, "r") as file:
                file_content = file.read()

            # Generate a new name for the document
            new_name = generate_pdf_name(file_content)

            # Copy the file to the cleaned-content directory
            new_file_path = os.path.join(cleaned_content_dir, new_name)
            shutil.copy(file_path, new_file_path)

            print(f"Copied and renamed '{filename}' to '{new_name}'")


if __name__ == "__main__":
    main()
