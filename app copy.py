import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os 
from dotenv import load_dotenv

load_dotenv()

# Implement Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot with OpenAI"

# Prompt Template 
prompt = ChatPromptTemplate.from_messages([
    {"role": "system", "content": "You are an assistant. Please respond to user queries"},
    {"role": "user", "content": "Question: {question}"}
])

# Function to generate the response
def generate_response(question, api_key, llm, temperature, max_tokens):
    openai.api_key = api_key
    llm_model = ChatOpenAI(model=llm, temperature=temperature, max_tokens=max_tokens)
    output_parser = StrOutputParser()
    chain = prompt | llm_model | output_parser  # Chain the components together correctly
    answer = chain.invoke({'question': question})
    return answer

# Creating Web app
st.title("Enhanced Q&A Chatbot With OpenAI")

# Sidebar for Settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OPEN AI API keys:", type="password")

# Drop Down for various Open AI Model
llm = st.sidebar.selectbox("Select an Open AI Model", ["gpt-4", "gpt-4-turbo", "gpt-4"])

# Slider for Temperature and Tokens
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

# Main interface for user input
st.write("Go ahead and ask any question")
user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input, api_key, llm, temperature, max_tokens)
    st.write(response)
