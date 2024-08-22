import streamlit as st
import json
import os
from markdown_processor import display_markdown, parse_markdown
from translator import translate_markdown

# File to store history
HISTORY_FILE = "translation_history.json"

# Load history from file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# Save history to file
def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file)

# Delete a history entry
def delete_history(index):
    history = load_history()
    if 0 <= index < len(history):
        history.pop(index)
        save_history(history)
        return True
    return False

# Custom CSS for a minimalist, futuristic design
st.markdown("""
    <style>
    /* Base styles for the app */
    .stApp {
        background: linear-gradient(135deg, #232526, #414345);
        color: #F5F5F5;
        font-family: 'Poppins', sans-serif;
        padding: 50px 30px;
    }
    
    /* Title style */
    .stTitle {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #A8E6CF;
        text-align: center;
        animation: fadeInDown 1.2s ease;
        margin-bottom: 20px;
        letter-spacing: 2px;
    }
    
    /* Description style */
    .description {
        text-align: center;
        font-size: 1.25rem;
        font-weight: 300;
        color: #D3D3D3;
        margin-bottom: 50px;
        line-height: 1.6;
    }
    
    /* Upload section */
    .upload-section {
        background-color: #333333;
        border: 1px solid #555555;
        border-radius: 12px;
        padding: 35px;
        margin-bottom: 30px;
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    
    /* Subheader style */
    .stSubheader {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        color: #83a9cb;
        margin-top: 40px;
        margin-bottom: 15px;
        animation: zoomIn 0.6s ease;
        text-align: center;
        border-bottom: 1px solid #555555;
        padding-bottom: 10px;
    }
    
    /* Button styles */
    .stButton>button {
        background: linear-gradient(135deg, #9d966d, #996e6e);
        color: #232526;
        border: none;
        padding: 15px 35px;
        font-size: 16px;
        margin: 15px auto;
        display: block;
        cursor: pointer;
        border-radius: 30px;
        box-shadow: 0 5px 15px rgba(0 0, 0, 50%);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #9d966d, #996e6e);
        transform: translateY(-3px);
        box-shadow: 0 5px 35px 0px rgba(0,0,0,.1);
    }
    
    /* Input and select box styles */
    .stTextInput>div>input, .stSelectbox>div>div>div {
        background-color: #444444;
        border: 2px solid #555555;
        border-radius: 12px;
        color: #F5F5F5;
        font-family: 'Poppins', sans-serif;
        # padding: 10px;
        transition: all 0.3s ease;
    }
    .stTextInput>div>input:focus, .stSelectbox>div>div>div:focus {
        border-color: #FFD700;
        box-shadow: 0 0 8px rgba(255, 215, 0, 0.8);
    }
    
    /* Animation keyframes */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes zoomIn {
        from {
            transform: scale(0.8);
            opacity: 0;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Footer styling */
    footer {
        text-align: center;
        margin-top: 50px;
        color: #A8E6CF;
        font-weight: 400;
    }
    footer a {
        color: #FFD700;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    footer a:hover {
        color: #FFA500;
    }

    /* Hide Streamlit footer and watermark */
    .css-1omk9w8, footer {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'content' not in st.session_state:
    st.session_state.content = None
if 'translated_content' not in st.session_state:
    st.session_state.translated_content = None
if 'target_language' not in st.session_state:
    st.session_state.target_language = "es"
if 'history' not in st.session_state:
    st.session_state.history = load_history()
if 'selected_history' not in st.session_state:
    st.session_state.selected_history = None

# Sidebar for file upload, language selection, and history display
with st.sidebar:
    st.markdown("<h2 class='stTitle'>Upload & Translate</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose Your Markdown or PDF File",
        type=["md", "txt", "pdf"]
    )
    st.session_state.target_language = st.selectbox(
        "Select Language",
        ["es", "fr", "de", "zh", "hi"],
        index=["es", "fr", "de", "zh", "hi"].index(st.session_state.target_language)
    )

    # Display history
    st.markdown("<h2 class='stSubheader'>Translation History</h2>", unsafe_allow_html=True)
    if st.session_state.history:
        for i, entry in enumerate(st.session_state.history):
            if st.button(f"Show Translation: {entry['file_name']} ({entry['language_name']})", key=f"history_{i}"):
                st.session_state.selected_history = i

            if st.button(f"Delete {entry['file_name']} ({entry['language_name']})", key=f"delete_{i}"):
                if delete_history(i):
                    st.session_state.history = load_history()  # Reload the updated history

    else:
        st.markdown("*No history available*")

# Mapping of language codes to language names
language_names = {
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "hi": "Hindi"
}

# Title and description in the main area
st.markdown("<h1 class='stTitle'>Translation Hub</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>Quickly translate Markdown or PDF files with a sleek, modern interface.</p>", unsafe_allow_html=True)

# Text input for prompt translation
st.markdown("<h2 class='stSubheader'>Translate a Prompt</h2>", unsafe_allow_html=True)
user_prompt = st.text_area("Enter text to translate", "")

if user_prompt and st.button("Translate Prompt"):
    try:
        language_name = language_names[st.session_state.target_language]

        with st.spinner(f"Translating prompt into {language_name}..."):
            st.session_state.translated_content = translate_markdown(user_prompt, st.session_state.target_language)

        st.markdown(f"<h2 class='stSubheader'>Translated Prompt ({language_name})</h2>", unsafe_allow_html=True)
        display_markdown(st.session_state.translated_content)

        # Save history
        new_entry = {
            "file_name": "Text Prompt",
            "language_name": language_name,
            "translated_content": st.session_state.translated_content
        }
        st.session_state.history.append(new_entry)
        save_history(st.session_state.history)

    except Exception as e:
        st.error(f"Error during translation: {e}")

# Main content
if uploaded_file is not None:
    try:
        # Parse the content from the uploaded file
        st.session_state.content = parse_markdown(uploaded_file)
        
        # Display the original content
        st.markdown("<h2 class='stSubheader'>Original Content</h2>", unsafe_allow_html=True)
        display_markdown(st.session_state.content)

        # Button to trigger translation
        if st.button("Translate File"):
            try:
                language_name = language_names[st.session_state.target_language]
                
                with st.spinner(f"Translating file into {language_name}..."):
                    st.session_state.translated_content = translate_markdown(st.session_state.content, st.session_state.target_language)

                st.markdown(f"<h2 class='stSubheader'>Translated Content ({language_name})</h2>", unsafe_allow_html=True)
                display_markdown(st.session_state.translated_content)

                # Save history
                new_entry = {
                    "file_name": uploaded_file.name,
                    "language_name": language_name,
                    "translated_content": st.session_state.translated_content
                }
                st.session_state.history.append(new_entry)
                save_history(st.session_state.history)

                # Provide an option to download the translated content
                st.download_button(
                    label="Download Translation",
                    data=st.session_state.translated_content,
                    file_name="translated.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"Error during translation: {e}")

    except Exception as e:
        st.error(f"File processing error: {e}")

# Display the selected history content if any
if st.session_state.selected_history is not None:
    history_entry = st.session_state.history[st.session_state.selected_history]
    st.markdown(f"<h2 class='stSubheader'>Translated Content ({history_entry['language_name']})</h2>", unsafe_allow_html=True)
    display_markdown(history_entry['translated_content'])

# Clear button functionality
if st.button("Clear"):
    st.session_state.content = None
    st.session_state.translated_content = None
    st.session_state.selected_history = None
    # Use a workaround to simulate a rerun
    st.experimental_rerun() if 'experimental_rerun' in dir(st) else None

# Footer with additional information
st.markdown("""
    <footer>
        <p>Powered by <a href="https://www.streamlit.io" target="_blank">Streamlit</a> | Visit our <a href="https://github.com/your-repo" target="_blank">GitHub</a></p>
    </footer>
""", unsafe_allow_html=True)
