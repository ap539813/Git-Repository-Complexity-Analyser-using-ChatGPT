# Import necessary modules for data visualization, web app building and data processing
import altair as alt
import streamlit as st
import json
import os

# Import user-defined variables and page configurations
from important_variables import model_name, style_css
from application_pages import main, homepage

# Import the chat model
from langchain.chat_models import ChatOpenAI

# Function to load and apply a CSS file to the Streamlit app
def local_css(file_name):
    with open(file_name) as f:
        # Apply the CSS styles to the app
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Set the page layout of the Streamlit app to be wide
st.set_page_config(layout="wide")

# Set the Altair visualization render options
alt.renderers.set_embed_options(scaleFactor=2)

# Apply the CSS styles
local_css(style_css)

# Load the API key from a JSON file
with open('secrets.json') as f:
    data = json.load(f)

# Set the API key as an environment variable
os.environ["OPENAI_API_KEY"] = data['api_key']

# Set the GPT model in the session state
st.session_state['GPT'] = ChatOpenAI(temperature=0.7, model=model_name)

# Set a default value for the home_page key if it doesn't exist in the session state
if 'home_page' not in st.session_state:
    st.session_state['home_page'] = True

# Entry point of the application
if __name__ == '__main__':
    # If the user is on the home page, display the homepage content
    if st.session_state['home_page']:
        homepage()
    # Otherwise, display the main content
    else:
        main()
