import altair as alt
import streamlit as st
import json
import os
from important_variables import model_name, style_css
from application_pages import main, homepage

from langchain.chat_models import ChatOpenAI

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.set_page_config(layout="wide")

alt.renderers.set_embed_options(scaleFactor=2)

local_css(style_css)

with open('secrets.json') as f:
    data = json.load(f)

os.environ["OPENAI_API_KEY"] = data['api_key']

st.session_state['GPT'] = ChatOpenAI(temperature=0.7, model=model_name, )


if 'home_page' not in st.session_state:
    st.session_state['home_page'] = True

    


if __name__ == '__main__':
    if st.session_state['home_page']:
        homepage()
    else:
        main()

