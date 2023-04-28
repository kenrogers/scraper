import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to fetch the webpage and extract the content of the target div
def fetch_directory_search():
    url = "https://www.causeiq.com/directory/amateur-sports-clubs-list/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    directory_search = soup.find("div", class_="directory-search")
    return directory_search.get_text(strip=True)

# Function to query the OpenAI API
def query_openai_api(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=700,
        temperature=0,
    )
    return response.choices[0].text.strip()

# Function to format the extracted information as a Markdown list
def format_info_as_markdown(info):
    # Escape dollar signs to avoid LaTeX formatting
    info = info.replace('$', '\\$')

    lines = info.split('\n')
    markdown_lines = [f"- {line}" for line in lines if line.strip()]
    return '\n'.join(markdown_lines)


# Main app
st.title("Amateur Sports Clubs Information Extractor")

# Fetch the directory search content
directory_search_text = fetch_directory_search()

# Prepare the OpenAI API prompt
prompt = f"Extract the name, revenue, assets, and employees of each club from the following text:\n\n{directory_search_text}"

# Call the OpenAI API
extracted_info = query_openai_api(prompt)

# Format the extracted information as a Markdown list
formatted_info = format_info_as_markdown(extracted_info)

# Display the extracted information
st.write("Extracted information:")
st.write(formatted_info)
