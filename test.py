# Import required libraries
import os 
from apikey import apikey 
import streamlit as st 
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# Set page width with custom CSS
st.markdown(
    """
    <style>
        .stApp {
            max-width: 900px;  /* Adjust this value to increase/decrease the width */
            margin: auto;
        }
        .st-df {
            flex-direction: row;
        }
        .st-eb {
            width: 40% !important;
            margin-right: 1% !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title for the app
st.title('👉  Itinerary-GPT🌎 ')
st.subheader('Plan Your Trip in just 20 sec. 😎 ')

# Date input for start date and end date side by side
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now().date())
with col2:
    end_date = st.date_input("End Date", datetime.now().date())

# Show trip duration
if start_date and end_date:
    try:
        duration = (end_date - start_date).days
    except TypeError:
        st.write("Please select valid dates for both the start and end of your trip.")

# LangChain setup
os.environ['GOOGLE_API_KEY'] = apikey
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.9)
prompt = st.text_input('Enter Your City') 

# Prompt templates
Trip_template = PromptTemplate(
    input_variables=['city', 'duration'], 
    template='generate {city} itinerary plan exactly for {duration} days, use google map for adding eating plan for every day, add morning, afternoon, evening plan for every day including food'
)

# Memory 
Trip_memory = ConversationBufferMemory(input_key='city', memory_key='chat_history')

# Llms
Trip_chain = LLMChain(llm=llm, prompt=Trip_template, verbose=True, output_key='city', memory=Trip_memory)

# Display trip plan
if prompt: 
    Plan_Trip = Trip_chain.run({'city': prompt, 'duration': duration})
    st.write(Plan_Trip) 

    with st.expander('Title History'): 
        st.info(Trip_memory.buffer)
