import streamlit as st
from services.transcript_service import get_transcript, extract_video_id, list_available_transcripts
from services.vector_store_service import split_text, setup_vector_store
from chains.query_chain import build_chain

st.set_page_config(page_title="YouTube Q&A", layout="wide")
st.title("AskTube AI")

# Initialize session state
if "chain" not in st.session_state:
    st.session_state.chain = None
if "video_url" not in st.session_state:
    st.session_state.video_url = None
if "video_id" not in st.session_state:
    st.session_state.video_id = None

# ========== LEFT SIDEBAR: YouTube Input & Q&A ========== #
with st.sidebar:
    st.header("Video Input + Q&A")

    # YouTube URL form
    with st.form("video_form"):
        youtube_url = st.text_input("Enter YouTube video URL")
        language_options = {
            "English": "en",
            "Hindi": "hi", 
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Japanese": "ja",
            "Korean": "ko",
            "Chinese": "zh",
            "Arabic": "ar",
            "Russian": "ru"
        }
        selected_language = st.selectbox(
            "Preferred Language (for transcript extraction)",
            list(language_options.keys()),
            help="Select the language you prefer for transcript extraction. If not available, the system will try other languages and translate to English."
        )
        language = language_options[selected_language]
        submitted = st.form_submit_button("Submit Video")
        if submitted:
            if not youtube_url or youtube_url.strip() == "":
                st.error("Please enter a YouTube URL")
            else:
                video_id = extract_video_id(youtube_url)
                print("Video Id: ", video_id)
                if not video_id:
                    st.error("Invalid YouTube URL. Please enter a valid YouTube video URL.")
                    st.info("Supported formats:\n- https://www.youtube.com/watch?v=VIDEO_ID\n- https://youtu.be/VIDEO_ID\n- https://www.youtube.com/embed/VIDEO_ID")
                else:
                    with st.spinner("Fetching and processing transcript..."):
                        try:
                            transcript = get_transcript(video_id, language=language)
                            texts = split_text(transcript)
                            retriever = setup_vector_store(video_id, texts)
                            chain = build_chain(retriever)

                            st.session_state.video_url = youtube_url
                            st.session_state.video_id = video_id
                            st.session_state.chain = chain

                            # Show processing info
                            st.success(f"Video processed! Transcript has {len(texts)} chunks. Ask your questions below.")
                            with st.expander("Processing Details"):
                                st.write(f"**Transcript Length:** {len(transcript)} characters")
                                st.write(f"**Number of Chunks:** {len(texts)}")
                                st.write(f"**Chunk Size:** 1000 characters with 200 overlap")
                                st.write(f"**Search Method:** MMR (Maximum Marginal Relevance)")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                            # Show available transcripts for debugging
                            available_transcripts = list_available_transcripts(video_id)
                            if available_transcripts:
                                st.info(f"Available transcripts: {[t['language_code'] for t in available_transcripts]}")
                            else:
                                st.info("No transcripts found for this video.")

    # Q&A Section (shown only if video is processed)
    if st.session_state.chain and st.session_state.video_url:
        st.markdown("#### Ask a Question About the Video")
        with st.form("question_form"):
            question = st.text_input("Your question")
            asked = st.form_submit_button("Ask")
            if asked and question:
                with st.spinner("Thinking..."):
                    try:
                        answer = st.session_state.chain.invoke(question)
                        st.success(answer)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# ========== RIGHT SIDE: Embedded YouTube Video ========== #
if st.session_state.video_url and st.session_state.video_id:
    st.markdown("#### Video Preview")
    st.components.v1.html(
        f"""
        <iframe width="640" height="360" 
                src="https://www.youtube.com/embed/{st.session_state.video_id}" 
                frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen></iframe>
        """,
        height=370,
    )