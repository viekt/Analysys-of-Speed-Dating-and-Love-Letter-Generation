#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AdamW
import torch
import re
from collections import Counter
import requests
import base64
import random

cloud = open('C:/Users/Hp/Downloads/wordcloud.png', "rb")
contents = cloud.read()
data_url = base64.b64encode(contents).decode("utf-8")
cloud.close()

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создание таблицы names
cursor.execute('''CREATE TABLE IF NOT EXISTS names
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS texts
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, letter TEXT, name_id INTEGER,
                   FOREIGN KEY(name_id) REFERENCES names(id))''')

model = GPT2LMHeadModel.from_pretrained('C:/Users/Hp/Downloads/model2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})


def text_generation(name):
    text = f"Darling {name},\n I miss you so much"
    input_ids = tokenizer.encode(text, return_tensors="pt")

    model.eval()
    with torch.no_grad():
        out = model.generate(input_ids, do_sample=True, temperature=1.2, max_length = 100)
    generated_text = list(map(tokenizer.decode, out))[0]

    return generated_text

def save_name_text(name, generated_text):
    try:
        cursor.execute("INSERT INTO names (name) VALUES (?)", (name,))
        name_id = cursor.lastrowid

        cursor.execute("INSERT INTO texts (letter, name_id) VALUES (?, ?)", (generated_text, name_id))
        
        conn.commit()

        st.success("Name and generated text are successfully saved in database")
    except sqlite3.Error as error:
        st.error(f"Error in saving name and text in database: {error}")


    
def main():
    page_bg_color = 'pink'
    st.markdown(f"""
    <style>
    .reportview-container {{
        background-color: {page_bg_color};
    }}
    </style>
    """, unsafe_allow_html=True)

    st.title("Love letter generation")
    st.markdown(f'<img src="data:image/gif;base64,{data_url}">', unsafe_allow_html=True)

    
    st.subheader("Be in love:")
    
    st.set_option('deprecation.showPyplotGlobalUse', True)
    st.write("")
    
    name = st.text_input("Please enter your lover's name to write a letter")
    
    st.text("Isn't it romantic?")
    st.video("https://youtu.be/cdWHFPDUcSk")
    
    if st.button("Generate"):
        if name:
            generated_text = text_generation(name)

            save_name_text(name, generated_text)

            st.subheader("Love letter:")
            st.write(generated_text.replace('<NAME>', name))
            
            api_key = "live_6u97DRwkeOxkjee3IIdfhoCHc5KtBgdg4pOTWApXmtrYt4MdAbvGYHTFm8xh5x7C"
            url = f"https://api.thecatapi.com/v1/images/search?limit=20&breed_ids=beng&api_key={api_key}"
            n = random.randint(0, 19)
            response = requests.get(url)
            answer = response.json()
            url_gif = answer[n]['url']
            st.image(url_gif)
        else:
            st.warning("Please enter your lover's name:")

if __name__ == "__main__":
    main()

