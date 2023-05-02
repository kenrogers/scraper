import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to fetch the webpage and extract the content of the target div
def fetch_website_info():
    url = "https://www.washingtonpremierfc.com/about-us/about-us/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    directory_search = soup.find("div", class_="inner-pagecontent")
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


# Main app
st.title("Washington Premier Football Club Analysis")

# Fetch the directory search content
website_text = fetch_website_info()

# Prepare the OpenAI API prompt
prompt = f"The following text is a description of a sports club. Based on the information given, list out the key competitive achievements of the organization. Only include achievements that are relevant to competitions and a focus on producing high-quality athletes:\n\n{website_text}"

# Call the OpenAI API
extracted_info = query_openai_api(prompt)

# Display the extracted information
st.write("Extracted information:")
st.write(extracted_info)
