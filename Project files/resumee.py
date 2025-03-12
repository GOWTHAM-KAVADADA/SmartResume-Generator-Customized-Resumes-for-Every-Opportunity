import streamlit as st
import google.generativeai as genai

api_key = "AIzaSyDRb_0g6-Ya__xUIhjSq-Us3DNZ8e0RTmE"
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

def generate_resume(context):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    context
                ],
            },
        ]
    )
    response = chat_session.send_message(context)
    text = response.candidates[0].content if isinstance(response.candidates[0].content, str) else response.candidates[0].content.parts[0].text
    return text

def clean_resume_text(text):
    cleaned_text = text.replace("[Add Email Address]", "[Your Email Address]")
    cleaned_text = cleaned_text.replace("[Add Phone Number]", "[Your Phone Number]")
    cleaned_text = cleaned_text.replace("[Add LinkedIn Profile URL (optional)]", "[Your LinkedIn URL (optional)]")
    cleaned_text = cleaned_text.replace("[University Name]", "[Your University Name]")
    cleaned_text = cleaned_text.replace("[Graduation Year]", "[Your Graduation Year]")
    return cleaned_text

# Streamlit UI for taking user inputs
st.title("Resume Generator")

# Textboxes for name and job title input with unique keys
name = st.text_input("Enter your name", key="name_input")
job_title = st.text_input("Enter your job title", key="job_title_input")

# Submit button
if st.button("Generate Resume"):
    if name and job_title:
        context = f'name:{name}\njob_title:{job_title}\nwrite a resume on above data.'
        resume = generate_resume(context)
        cleaned = clean_resume_text(resume)
        st.markdown("### Generated Resume")
        st.markdown(cleaned)
    else:
        st.warning("Please enter both your name and job title.")
