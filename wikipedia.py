# RUN THIS FILE WITH 
# streamlit run wikipedia.py

from wikipediaapi import Wikipedia
import streamlit as st
from nltk import word_tokenize
from nltk.corpus import stopwords

key_words = ["is", "were", "was"]
separators = ['.']
stopwords = stopwords.words('english') # importing nltk's list of "filler" words

wiki = Wikipedia('en')

name = st.text_input("Page name", "Python") # The name variable will take the input from the input box

page = wiki.page(title=name)
info = dict()

def show_info(page):
    st.write(page.fullurl)
    
    info = list()
    append = False
    tokens = word_tokenize(page.summary) # splitting all words into a list (example: "Hello world" becomes ["Hello", "world"])
    for i in range(len(tokens)):
        if tokens[i] in key_words: # if a key_word is met
            info.append(list())
            j = 1 # skipping the key word
            while tokens[i + j] not in separators: # adding the end of the sentence to a list
                info[-1].append(tokens[i + j]) 
                j += 1
            info[-1] = " ".join([word for word in info[-1] if word not in stopwords]) # turning list to a string while removing unnecessary words
    st.write(info)

    choice = st.radio("Content", ["Summary", "Sections", "Text", "Links", "Categories"])
    if choice == "Summary":
        st.write(page.summary)
    elif choice == "Sections":
        st.write(page.sections)
    elif choice == "Text":
        st.write(page.text)
    elif choice == "Categories":
        for index, value in enumerate(page.categories.values()):
            st.write(value.fullurl)
            if index > 10:
                break
    elif choice == "Links":
        for index, value in enumerate(page.links.values()):
            st.write(value.fullurl)
            if index > 10:
                break
    

if page.exists():    
    if ('may refer to:' in page.summary):
        options = list()
        for key, index in page.links.items():
            if name in key and "Talk:" not in key:
                options.append(index)
        name = st.selectbox(f"{name} may refer to:", ["", *[option.title for option in options]])
        if name is not "":
            show_info(wiki.page(title=name))
    else: 
        show_info(page)
else:
    st.write("Page not found")
