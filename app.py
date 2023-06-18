import altair as alt
import streamlit as st
import json
import os
# importing the local modules
from important_variables import model_name
from application_pages import main, homepage

import openai
# from langchain.llms import OpenAI
# import langchain.llms
from langchain.chat_models import ChatOpenAI

st.set_page_config(layout="wide")

alt.renderers.set_embed_options(scaleFactor=2)

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

