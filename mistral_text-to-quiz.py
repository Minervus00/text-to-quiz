from gradio_client import Client
import streamlit as st
import json
import random
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# read pdf file and return text
def get_pdf_text(file):
    # print(file, type(file))
    text = ""
    # Read the PDF file using PdfReader
    pages_reader = PdfReader(file)

    # Loop through each page in the PDF
    for _, page in enumerate(pages_reader.pages):
        page_text = page.extract_text()
        text += page_text

    return text


# split text into chunks
def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400
    )
    chunks = splitter.split_text(text)
    return chunks  # list of strings


# Initialize session state variables
def initialize_state():
    # print("initilizing state")
    st.session_state.submitted = False
    st.session_state.generated = False
    if 'quizz_data' in st.session_state:
        del st.session_state['quizz_data']


# Placeholder function to generate the quiz questions
def generate_quiz(chunks, language, num_questions):
    passages = random.sample(chunks, min(num_questions, len(chunks)))

    quizzes = []
    for i, passage in enumerate(passages):
        gen = False
        while not gen:
            try:
                result = st.session_state.client.predict(
                    json.dumps({"text": passage, "lang": language}),
                    api_name="/predict"
                )
                quizzes.append(json.loads(result["output"]))
            except Exception:
                print(f"Error while generating question {i+1}, retrying...")
            else:
                gen = True

    return quizzes


# Define the Gradio app interface
def quiz_generator_app(uploaded_file, language, num_questions):
    initialize_state()

    if uploaded_file is None:
        st.warning("Please upload a PDF file.")
        return

    # Call the placeholder function to process the uploaded file
    processed_content = get_pdf_text(uploaded_file)

    chunks = []
    file_chunks = get_text_chunks(processed_content)
    chunks.extend(file_chunks)

    with st.spinner("Generation in progress..."):
        # Call the placeholder function to generate the quiz
        quiz = generate_quiz(chunks, language, num_questions)

    st.session_state.quizz_data = quiz
    st.session_state.generated = True


def change():
    st.session_state.submitted = True


def main():
    st.html('<h1 style="text-align: center"><span style="color: #D42034;">Mistral 7b</span> Quiz Generator</h1>')

    # File uploader for quizzes
    uploaded_file = st.file_uploader("Upload a pdf file", type="pdf", accept_multiple_files=False)

    # Language selection
    language = st.selectbox("Select Language", ["English", "French"])

    # Number of questions input
    num_questions = st.number_input(
        "Number of Questions", min_value=3, max_value=15, value=3
    )
    st.button("Generate Quiz", on_click=quiz_generator_app, args=(uploaded_file, language, num_questions), disabled=st.session_state.get("no_api", True))

    # Generate quiz button
    if 'generated' in st.session_state and st.session_state["generated"]:
        # print("displaying quiz")
        quiz_questions = st.session_state.quizz_data

        # Store user answers
        user_answers = {}

        # Render questions
        for i, q in enumerate(quiz_questions):
            with st.container(border=True):
                st.write(f"#### **Question {i + 1}**")
                user_answers[i] = st.radio(f"**{q['question']}**", q['options'], key=f"q{i}", index=None)

                # Check session state for "submitted" to display results
                if st.session_state["submitted"]:
                    correct_option = q['options'][ord(q['answer']) - ord('A')]
                    explanation = q['explanation']
                    if user_answers[i] == correct_option:
                        st.success("Correct!")
                    else:
                        st.error("Incorrect.")
                    st.markdown(f"#### :bulb: Explanation\n{explanation}")

        # Display overall score if "submitted" is True
        if st.session_state["submitted"]:
            score = sum(
                1 for i, q in enumerate(quiz_questions)
                if user_answers[i] == q['options'][ord(q['answer']) - ord('A')]
            )
            st.write(f"## Score: {score}/{len(quiz_questions)}")
        else:
            # Submit answers button
            st.button("Submit Answers", on_click=change)


if __name__ == "__main__":
    if "no_api" not in st.session_state:
        print("launching api")
        url = "https://6329753acc4c323e75.gradio.live/"
        st.session_state.client = Client(url)
        st.session_state.no_api = False
    main()
