from apikey import apikey 
import os
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
            max-width: 1200px;  /* Adjust this value to increase/decrease the width */
            margin: auto;
        }
        .st-df {
            flex-direction: row;
        }
        .st-eb {
            width: 40% !important;
            # margin-right: 1% !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title for the app
st.title('👉  Travel Planner🌎 ')
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
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.9, google_api_key=apikey)

prompt = st.text_input('Enter Your City/Country') 

# Prompt templates
Trip_template = PromptTemplate(
    input_variables=['city', 'duration'], 
    template='generate {city} itinerary plan exactly for {duration} days, use google map for adding eating plan for every day, add morning, afternoon, evening plan for every day including food, not give link'
)

# Memory 
Trip_memory = ConversationBufferMemory(input_key='city', memory_key='chat_history')

# Llms
Trip_chain = LLMChain(llm=llm, prompt=Trip_template, verbose=True, output_key='city', memory=Trip_memory)

# Display trip plan
output_button = st.button("Generate Trip Plan")
if output_button:
    if prompt: 
        Plan_Trip = Trip_chain.run({'city': prompt, 'duration': duration})
        st.write(Plan_Trip) 

        with st.expander('Title History'): 
            st.info(Trip_memory.buffer)
    else:
        st.write("Please enter a prompt to generate the trip plan.")
