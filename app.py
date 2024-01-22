import streamlit as st
import os
import PyPDF2 as pdf
from langchain.llms import OpenAI
from dotenv import load_dotenv
import json
load_dotenv()



# Prompt template
input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""



input_prompt2 = """
Act like a skilled or very experience ATS(Application Tracking System) \
with a deep understanding of tech field, software engineering, data science, data analyst \
and big data engineer. Your task is to evaluate the resume based on the given job description. \
You must consider the job market is very competitve and you should provide best assistance for improving \ 
the resumes. Below are the queries to evaluate the job description: \

Step 1: First examine the job details. What would be the best qualications for the given job description?
Step 2: Assign the percentage matching based on JD and the missing keywords with higher accuracy.
Step 3: Tell me about the specific details and keywords required to modify in the resume to maximize the selection of resume.

resume:{text}
description:{jd}

In the first line provide the Step 1 details. 
In the second line provide detail in one single string having the structure {{"JD Match": "%", "Missing Keywords : []", "Profile Summary" : " "}}
In the third line provide step 3 details.

Sometimes, it may happen that the job description is in French language, in that case evaluate the resume in French language.

At last always provide the additional information for getting selected.
"""

## Function to load OpenAI model and get responses
def get_openai_response(question):
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct", 
                 temperature=0.5, 
                 openai_api_key=os.getenv('OPENAI_API_KEY'))
    response = llm(question)
    return response



def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text



# streamlit app
## streamlit app
st.title("Smart ATS Resume Expert")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description", key="input", height=200)
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

if uploaded_file is not None:
    st.write('PDF Uploaded Successfully')

submit1 = st.button("Tell me about the Resume")

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_text(uploaded_file)

        response=get_openai_response(input_prompt1)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")


submit2 = st.button("Submit")

if submit2:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_openai_response(input_prompt2)
        st.subheader(response)
    else:
        st.write("Please uplaod the resume")