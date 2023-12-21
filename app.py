
# Bring in deps
import os 
from apikey import apikey 

import streamlit as st 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

os.environ['GOOGLE_API_KEY'] = apikey
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.9)

# App framework
st.title('👉  itenerary-GPT🌎 ')
st.subheader('Plan Your Trip in just 20 sec. 😎 ')
prompt = st.text_input('Enter Your City') 

# Prompt templates
Trip_template = PromptTemplate(
    input_variables = ['city'], 
    template='generate {city} itenerary plan exact for 5 days, use google map for adding eating plan for every day, add morning, afternoon, evening plan for every day including food'
)


# Memory 
Trip_memory = ConversationBufferMemory(input_key='city', memory_key='chat_history')


# Llms
Trip_chain = LLMChain(llm=llm, prompt=Trip_template, verbose=True, output_key='city', memory=Trip_memory)


# Show stuff to the screen if there's a prompt
if prompt: 
    Plan_Trip = Trip_chain.run(prompt)


    st.write(Plan_Trip) 

    with st.expander('Title History'): 
        st.info(Trip_memory.buffer)

