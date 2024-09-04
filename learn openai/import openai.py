# DO NOT USE ME, I HAVE NO IDEA HOW MANY TOKENS I USE

# import openai
# import json
# import os
# from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the OpenAI API client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def upload_file_and_convert_to_json(file_path):
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Upload the file to OpenAI
    with open(file_path, "rb") as file:
        upload_response = client.files.create(
            file=file,
            purpose='fine-tune'
        )
    file_id = upload_response.id

    # Create a prompt for the GPT model to convert the content to JSON
    prompt = f"""
    Convert the following Markdown content to JSON format suitable for fine-tuning OpenAI models.
    Each section should be a separate JSON object with 'title' and 'content' fields.
    The content should preserve all Markdown formatting.

    Here's the content to convert:

    {content}

    Please provide the result in valid JSON format.
    """

    # Use the GPT model to convert the content to JSON
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that converts Markdown to JSON."},
            {"role": "user", "content": prompt}
        ],
        # max_tokens=12000
    )

    # Extract the JSON from the response
    json_content = response.choices[0].message.content

    # Parse the JSON to ensure it's valid
    try:
        parsed_json = json.loads(json_content)
    except json.JSONDecodeError:
        print("The generated content is not valid JSON. Manual review may be needed.")
        parsed_json = {"error": "Invalid JSON generated"}

    # Save the JSON to a file
    output_file = 'output.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_json, f, ensure_ascii=False, indent=2)

    print(f"Conversion complete. JSON saved to {output_file}")
    print(f"Uploaded file ID: {file_id}")

    return file_id

# Use the function
file_path = 'ta-articles-for-notes.md'
uploaded_file_id = upload_file_and_convert_to_json(file_path)