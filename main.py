import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from io import BytesIO
from PIL import Image
import re
from audio import *
from text_speech import *
import google.generativeai as genai

# Set page config
st.set_page_config(page_title="PDF Summarizer", page_icon="📄")

deepgram_api = os.getenv("DEEPGRAM_API_KEY")


def get_api_key():
    return os.getenv("GEMINI_API_KEY")

genai.configure(api_key=get_api_key())

def text_model(api_key):
    return ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key, temperature=0.9)

def fine_tuning():
    return """You are an AI summarizer with excellent knowledge in summarizing content. 
    You will be given a large amount of content. Your task is to summarize the content provided to you in the best possible way by identifying 
    important points and highlighting key terms.

    Additionally, include any existing diagrams and graphs present in the content. The summarized content should be 5-7 pages at minimum.
    """

def summarize_image_notes():
    return """You are an AI assistant specialized in summarizing handwritten or typed notes. 
    Analyze the image provided and summarize the key points, main ideas, and important concepts.
    Organize the summary in a clear and concise manner, using bullet points or short paragraphs as appropriate.
    If there are any diagrams or visual elements, describe them briefly as well."""

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def get_pdf_content(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def summarize(pdf_content, api_key):
    prompt = fine_tuning() + "\n\nHere's the content to summarize:\n" + pdf_content
    message = HumanMessage(content=prompt)
    llm = text_model(api_key)
    response = llm.invoke([message])
    return response.content

def process_bold_text(line):
    bold_pattern = re.compile(r'\**__(.*?)__\**')
    processed_line = bold_pattern.sub(r'<b>\1</b>', line)
    return processed_line

def create_enhanced_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.steelblue,
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.steelblue,
        spaceBefore=12,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'Subheading',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.darkgrey,
        spaceBefore=6,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['BodyText'],
        fontSize=12,
        textColor=colors.black,
        spaceBefore=6,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )

    sections = text.split('\n')
    is_first_paragraph = True
    for i, section in enumerate(sections):
        section = section.strip()
        if i == 0:
            title_text = section.lstrip('#').strip()
            story.append(Paragraph(title_text, title_style))
        elif section.startswith('##') or section.startswith('###'):
            if not is_first_paragraph:
                story.append(Spacer(1, 12))
            if section.startswith('## '):
                subheading_text = section.lstrip('#').strip()
                story.append(Paragraph(subheading_text, heading_style))
            elif section.startswith('### '):
                subheading_text = section.lstrip('#').strip()
                story.append(Paragraph(subheading_text, subheading_style))
            is_first_paragraph = True
        elif section:
            processed_line = re.sub(r'\**(.*?)\**', r'<b>\1</b>', section)
            if is_first_paragraph:
                story.append(Paragraph(processed_line, body_style))
                is_first_paragraph = False
            else:
                story.append(Spacer(1, 12))
                story.append(Paragraph(processed_line, body_style))
        else:
            if not is_first_paragraph:
                story.append(Spacer(1, 12))
                is_first_paragraph = True

    doc.build(story)
    buffer.seek(0)
    return buffer

def main():

    api_key = get_api_key()
    if not api_key:
        st.warning("Please set your Google API Key as an environment variable to proceed.")
        return

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'summary' not in st.session_state:
        st.session_state.summary = ""
    if 'summary_stage' not in st.session_state:
        st.session_state.summary_stage = "initial"

    st.title("DocuGenie: AI Document Summarizer")

    # Sidebar with select box and file upload
    option = st.sidebar.selectbox("Choose Summarizer", ["PDF Summarizer", "Note Summarizer"],help="Provide the necessary feature you want to use")


    if option == "PDF Summarizer":
        st.info("📄 **PDF Summarizer**: Upload a PDF document to generate a summary. You can also download and listen to the summary." )
        st.sidebar.header("Upload PDF")
        uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf",help="Helps you providing with summarized PDF Doc")
    
        if uploaded_file is not None:
            if st.button("Summarize") or st.session_state.summary_stage == "modify":
                with st.spinner("📚 Summarizing... Please wait."):
                    pdf_content = get_pdf_content(uploaded_file)
                    if st.session_state.summary_stage == "initial":
                        st.session_state.summary = summarize(pdf_content, api_key)
                    elif st.session_state.summary_stage == "modify":
                        modification_prompt = st.session_state.modification_prompt
                        new_prompt = f"Please modify the following summary according to this instruction: {modification_prompt}\n\nOriginal summary:\n{st.session_state.summary}"
                        st.session_state.summary = summarize(new_prompt, api_key)

                    st.subheader("Summary:")
                    st.write(st.session_state.summary)

                    if st.button("Read Summary Aloud"):
                        text_to_speech(model='deepgram', api_key=deepgram_api, text=st.session_state.summary[0:50], output_file_path="summary_audio.wav")
                        try:
                            play_audio("summary_audio.wav")
                        except Exception as e:
                            st.error(f"Error playing audio: {e}")

                    st.session_state.summary_stage = "feedback"

            if st.session_state.summary_stage == "feedback":
                user_satisfied = st.radio("Are you satisfied with this summary?", ("Yes", "No"))
         
                if user_satisfied == "Yes":
                    pdf_buffer = create_enhanced_pdf(st.session_state.summary)
                    st.download_button(
                        label="Download Summary PDF",
                        data=pdf_buffer,
                        file_name="summary.pdf",
                        mime="application/pdf"
                    )
                    
                    st.session_state.summary_stage = "initial"
                    st.session_state.chat_history = [AIMessage(content=st.session_state.summary)]
        
                elif user_satisfied == "No":
                    st.session_state.modification_prompt = st.text_area("How should the summary be modified?")
                    if st.button("Modify Summary"):
                        st.session_state.summary_stage = "modify"
                        st.rerun()

        if st.session_state.summary:
            st.subheader("Download Latest Summary")
            pdf_buffer = create_enhanced_pdf(st.session_state.summary)
            st.download_button(
                label="Download Latest Summary PDF",
                data=pdf_buffer,
                file_name="latest_summary.pdf",
                mime="application/pdf"
            )

            if st.button("Read Latest Summary Aloud"):
                text_to_speech(model='deepgram', api_key=deepgram_api, text=st.session_state.summary[0:50], output_file_path="latest_summary_audio.wav")
                try:
                    play_audio("latest_summary_audio.wav")
                except Exception as e:
                    st.error(f"Error playing audio: {e}")

        st.header("Chat about the Summary")
        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.write(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.write(message.content)

        user_input = st.chat_input("Type your message here:")
        if user_input:
            with st.spinner("🤔 Thinking..."):
                st.session_state.chat_history.append(HumanMessage(content=user_input))
                llm = text_model(api_key)
                conversation = ConversationChain(
                    llm=llm,
                    memory=ConversationBufferMemory(return_messages=True)
                )
                
                for message in st.session_state.chat_history:
                    if isinstance(message, HumanMessage):
                        conversation.predict(input=message.content)
                    elif isinstance(message, AIMessage):
                        conversation.memory.chat_memory.add_ai_message(message.content)

                response = conversation.predict(input=user_input)

                st.session_state.chat_history.append(AIMessage(content=response))

            st.rerun()

    elif option == "Note Summarizer":
        st.info("📝**Note Summarizer**: Upload a notes img to generate a summary. You can also download and listen to the summary.")
        st.sidebar.header("Upload Notes Image")
        uploaded_image = st.sidebar.file_uploader("Upload an image of your notes", type=["png", "jpg", "jpeg"],help="Provides summary for uploaded images")
        
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Notes", use_column_width=True)
            
            if st.button("Summarize Notes"):
                with st.spinner("📝 Analyzing and summarizing notes... Please wait."):
                    image_data = input_image_setup(uploaded_image)
                    summary = get_gemini_response(summarize_image_notes(), image_data, "")
                    st.subheader("Notes Summary:")
                    st.write(summary)
                    
                    pdf_buffer = create_enhanced_pdf(summary)
                    st.download_button(
                        label="Download Notes Summary PDF",
                        data=pdf_buffer,
                        file_name="notes_summary.pdf",
                        mime="application/pdf"
                    )
                    
                    if st.button("Read Notes Summary Aloud"):
                        text_to_speech(model='deepgram', api_key=deepgram_api, text=summary[0:50], output_file_path="notes_summary_audio.wav")
                        try:
                            play_audio("notes_summary_audio.wav")
                        except Exception as e:
                            st.error(f"Error playing audio: {e}")

if __name__ == "__main__":
    main()
