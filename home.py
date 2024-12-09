import streamlit as st
from pymongo import MongoClient

user = st.secrets['user']
password = st.secrets['password']
uri_url = st.secrets['uri']

uri = f'mongodb+srv://{user}:{password}@{uri_url}/?retryWrites=true&w=majority&appName=Cluster1'

client = MongoClient(uri)
db = client['techies-responses']
collection = client['responses']

# Write the title of the app
st.title('Matching app for techies')

# Place a divider
st.divider()

# Write a text
st.write('Welcome to my app, fill the form to get started!')

st.divider()

# Add a subheader
st.subheader('Fill the form to get matched with a techie')

st.text_input('What is your name?')
st.text_input('What are your programming language?')
st.text_input('What is your favourite of framework?')
st.text_input('What is your favourite tech conference or blog post?')
st.text_input('Have you contributed to any open source, name projects?')
st.text_input('What is your favourite tech company?')
st.text_input('What is your favourite code editor?')

if st.button('Submit'):
    # generate potential matches for my tech form
    st.success('Yay you have been matched with a techie!')
else:
    st.warning('Opps! Something went wrong!!!')