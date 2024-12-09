import streamlit as st
from pymongo import MongoClient
import torch
from transformers import BertTokenizer, BertModel
import numpy as np

# Connect to the database
user = st.secrets['user']
password = st.secrets['password']
uri_url = st.secrets['uri']

uri = f'mongodb+srv://{user}:{password}@{uri_url}/?retryWrites=true&w=majority&appName=Cluster1'

client = MongoClient(uri)
db = client['techies-responses']
collection = client['techies-responses']['responses']

# create embeddings by stating model and tokenizer which are from BERT in Hugging Face
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# function to generate embeddings
def generate_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True) # pt is for pytorch tensors
    output = model(**inputs)
    embedding = output.last_hidden_state.mean(dim=1).detach().numpy()
    return embedding


# Write the title of the app
st.title('Matching app for techies')

# Place a divider
st.divider()

# Write a text
st.write('Welcome to my app, fill the form to get started!')

st.divider()

# Add a subheader
st.subheader('Fill the form to get matched with a techie')

name = st.text_input('What is your name?')
programming_languages = st.text_input('What are your programming languages?')
framework = st.text_input('What is your favourite of framework?')
conference_blog = st.text_input('What is your favourite tech conference or blog post?')
open_source = st.text_input('Have you contributed to any open source, name projects?')
company = st.text_input('What is your favourite tech company?')
code_editor = st.text_input('What is your favourite code editor?')

if st.button('Submit'):
    # generate my document to then convert it into embeddings using my function
    responses =  {
        'name': name,
        'programming_languages': programming_languages,
        'framework': framework,
        'conference_blog': conference_blog,
        'open_source': open_source,
        'company': company,
        'code_editor': code_editor,
    }

    concatenated_responses = ' '.join(responses.values())

    # pass on the responses to my embedded model
    embeddings = generate_embeddings(concatenated_responses)
    # st.write(embeddings)

    document = {
        'responses': responses,
        'embeddings': embeddings.tolist(),
    }

    collection.insert_one(document) # insert the document into the collection
    
    all_documents = list(collection.find())
    if all_documents:
        # person who filled the form is the current embedding (vector 1)
        current_embedding = embeddings.flatten()
        # store similar interests of the people from our database
        similarities = []
        
        for doc in all_documents:
            store_embedding = np.array(doc['embeddings']).flatten()
            similarity = np.dot(current_embedding, store_embedding) / (np.linalg.norm(current_embedding) * np.linalg.norm(store_embedding)) # cosine similarity
            similarities.append((doc, similarity))

            similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

            # display the top 3 techies that match the interests
            st.subheader('Here are the top 3 techies that match your interests:')
            st.divider()

            for match, similarity in similarities[:3]:
                st.write(similarity)


    st.success('Your responses have been submitted successfully!')
else:
    st.warning('Opps! Something went wrong!!!')
