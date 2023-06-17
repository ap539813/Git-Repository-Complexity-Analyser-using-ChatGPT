import altair as alt
import streamlit as st
import seaborn as sns

# importing the local modules
from application_pages import main, homepage

st.set_page_config(layout="wide")

alt.renderers.set_embed_options(scaleFactor=2)



if 'home_page' not in st.session_state:
    st.session_state['home_page'] = True

    


if __name__ == '__main__':
    if st.session_state['home_page']:
        homepage()
    else:
        main()

