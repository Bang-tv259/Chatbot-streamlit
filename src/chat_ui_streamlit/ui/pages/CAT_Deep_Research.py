from __future__ import annotations  # noqa: N999

import time
from pathlib import Path
from datetime import UTC, datetime

import streamlit as st
import google.generativeai as genai
from exa_py import Exa

from chat_ui_streamlit.core.config import config
from chat_ui_streamlit.core.constants import MODEL_NAME
from chat_ui_streamlit.ui.components.chat_component import (
    render_input,
    render_message,
    render_welcome,
)
from chat_ui_streamlit.ui.components.header_component import render_header
from chat_ui_streamlit.ui.components.sidebar_component import render_sidebar


st.set_page_config(
    page_title="CAT Research Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==================== CONSTANTS ====================
# Note: Constants are defined separately to ensure compatibility
# with deployment on Streamlit Cloud.
# Streamlit Cloud may restrict certain dynamic behaviors, so
# constants must be pre-defined and static for stable deployment.

MAX_SEARCH_RESULTS = 10
MAX_CONTEXT_LENGTH = 25000
BASE_CHAT_TEMPLATE = """
You are a precise and logical AI assistant. Your primary task is to answer the user's question.

Rules:
1. If the provided context is NOT empty, use ONLY the information in the context to answer. Do not add outside knowledge.
2. If the provided context IS empty, answer the question using your own knowledge base, ensuring the response is accurate and reliable.
3. Always answer in the **same language as the user question**.
4. The answer must be in **Markdown format**, with a clear and well-structured layout (e.g., bullet points, numbered lists, tables, or code blocks where appropriate).
5. Avoid unnecessary words, greetings, or commentary. Return only the essential answer.
6. Ensure the answer is concise, logically structured, and scientifically accurate.

Context:
{context}

Question:
{question}

---
Please provide a detailed, accurate, and concise response that directly answers the question.
If context is provided, rely solely on it. If no context is provided, use your own knowledge.
Format the entire response using proper Markdown syntax with clear structure.
Ensure the response is written in the same language as the original question.
"""  # noqa: E501


RESEARCH_QUESTIONS_TEMPLATE = """
Please generate a list of 5 research questions based on the following input.
Each question should be returned as a single line, and the list should be formatted as:
1. Question 1
2. Question 2
3. Question 3
4. Question 4
5. Question 5
Ensure the questions are written in the same language as the input.
"""


MAX_QUESTIONS = 5
ANSWER_PROMPT_TEMPLATE = """
Based on the following question:
'{question}'
Please provide a detailed and precise answer.
Ensure the answer is written in the same language as the question.
"""


SUMMARY_PROMPT_TEMPLATE = """
Based on the original question: '{original_question}',
and the following question-answer pairs:
{question_answer_pairs},
---
Please provide a detailed, accurate, and concise response that directly answers the original question. Format the entire response using proper Markdown syntax with clear headings, bullet points, and code blocks where applicable. Ensure the response is well-structured, easy to read, and directly relevant to the query without unnecessary information.
Ensure the response is written in the same language as the original question.
"""  # noqa: E501


# ==================== LOAD CSS ====================
def load_css() -> None:
    """Load all CSS files."""
    css_files = ["header.css", "sidebar.css", "chat.css"]
    all_css = """
        <style>
        /* Global Styles */
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@300;400;500;600&display=swap');

        * {
            font-family: 'Google Sans', sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        /* Hide Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    """

    # Load each CSS file
    parent_dir = Path(__file__).parent.parent
    for css_file in css_files:
        css_path = parent_dir / "styles" / css_file
        try:
            all_css += Path(css_path).read_text(encoding="utf-8")
        except FileNotFoundError:
            # Fallback if file doesn't exist
            continue

    all_css += "</style>"
    st.markdown(all_css, unsafe_allow_html=True)


# ==================== SESSION STATE ====================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "deep_research_clicked" not in st.session_state:
    st.session_state["deep_research_clicked"] = False

if "cat_submit" not in st.session_state:
    st.session_state["cat_submit"] = False

if "cat_input" not in st.session_state:
    st.session_state["cat_input"] = ""

if "cat_temp" not in st.session_state:
    st.session_state["cat_temp"] = ""


# ================ INITIALIZE CONNECTION =================
genai.configure(api_key=config.gemini_api_key)
if "chat_client" not in st.session_state:
    st.session_state.chat_client = genai.GenerativeModel(model_name=MODEL_NAME[0])

search_engine = Exa(api_key=config.search_engine_api_key)


# ======================= MAIN APP =======================
def main() -> None:  # noqa: C901, PLR0912, PLR0914, PLR0915
    """Main app."""
    # Load styles
    load_css()

    # Render components
    render_header()
    render_sidebar()

    render_welcome()
    st.markdown('<div class="messages-container">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        render_message(message, is_user=(message["role"] == "user"))

    st.markdown("</div>", unsafe_allow_html=True)

    # Render interactive input
    prompt = render_input()

    if prompt and not st.session_state["deep_research_clicked"]:  # noqa: PLR1702
        # Log user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
            "model": MODEL_NAME[0],
        })

        with st.spinner(
            f"🚀 [Chat] CAT is analyzing your request: '{prompt}'...", show_time=True
        ):
            # Create a container to hold the streaming response
            message_container = st.empty()
            # Perform search engine
            search_results = search_engine.search_and_contents(
                prompt,
                text=True,
                num_results=MAX_SEARCH_RESULTS,
                type="keyword",
            ).results

            if not search_results:
                full_prompt = BASE_CHAT_TEMPLATE.format(
                    context="No relevant context found.",
                    question=prompt,
                )
                reference_links = []
            else:
                search_context = "\n".join([
                    f"Context {idx + 1}: {result.text.strip()}"
                    for idx, result in enumerate(search_results)
                ])
                reference_links = [result.url for result in search_results]
                reference_links_formatted = "<br>".join(
                    f"- {link}" for link in reference_links
                )
                # Prepare the full prompt with context
                full_prompt = BASE_CHAT_TEMPLATE.format(
                    context=search_context[:MAX_CONTEXT_LENGTH],
                    question=prompt,
                )
                message_container.markdown(
                    f"""
                    <div class="message assistant">
                        <div class="message-avatar">😽</div>
                        <div class="message-content">
                            <div class="message-bubble" style="background-color: #2c2222b3; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                                References: <br> {reference_links_formatted}
                            </div>
                        </div>
                    </div>
                    """,  # noqa: E501
                    unsafe_allow_html=True,
                )

            try:
                chat_session = st.session_state.chat_client.start_chat(history=[])
                response = chat_session.send_message(full_prompt, stream=True)

                # Initialize streaming content
                streaming_content = ""

                for chunk in response:
                    # Append each chunk to the streaming content
                    streaming_content += chunk.text.strip()

                    # Update the message container
                    message_container.markdown(
                        f"""
                        <div class="message assistant">
                            <div class="message-avatar">😽</div>
                            <div class="message-content">
                                <div class="message-bubble" style="background-color: #2c2222b3; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                                    Thinking: {streaming_content}
                                </div>
                            </div>
                        </div>
                        """,  # noqa: E501
                        unsafe_allow_html=True,
                    )
                    time.sleep(0.3)

                # Log assistant response
                answer_final = (
                    streaming_content.strip()
                    + "<br><br>"
                    + "Reference Links:<br>"
                    + reference_links_formatted
                )
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer_final,
                    "timestamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
                    "model": MODEL_NAME[0],
                })

            except Exception as e:  # noqa: BLE001
                if "429" in str(e):
                    st.warning(
                        f"[INFO] Model '{MODEL_NAME[0]}' encountered Too Many Requests (429). Switching models..."  # noqa: E501
                    )
                    # Move the model to the end of the list
                    MODEL_NAME.append(MODEL_NAME.pop(0))

                    # Set new chat client with the next model
                    st.session_state.chat_client = genai.GenerativeModel(
                        model_name=MODEL_NAME[0]
                    )
                    st.info(f"[INFO] Switched to model: {MODEL_NAME[0]}")
                else:
                    st.error(f"[ERROR] Please try again later (>5 minutes). Error: {e}")
                    time.sleep(600)

        prompt = ""

        st.rerun()

    elif prompt and st.session_state["deep_research_clicked"]:
        # Log user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
            "model": MODEL_NAME[0],
        })

        with st.spinner(f"🚀 [Deep Research] Thinking: '{prompt}'...", show_time=True):
            try:
                # Step 1: Define template and send prompt
                full_prompt = f"{RESEARCH_QUESTIONS_TEMPLATE}\nInput: {prompt}"

                # Send prompt with template to generate questions
                chat_session = st.session_state.chat_client.start_chat(history=[])
                question_response = chat_session.send_message(full_prompt, stream=True)

                # Create a container for displaying questions
                message_container = st.empty()
                streaming_content = ""

                # Stream generated questions
                for chunk in question_response:
                    streaming_content += chunk.text.strip()
                    message_container.markdown(
                        f"""
                        <div class="message assistant">
                            <div class="message-avatar">😽</div>
                            <div class="message-content">
                                <div class="message-bubble" style="background-color: #2c2222b3; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                                    Questions: {streaming_content}
                                </div>
                            </div>
                        </div>
                        """,  # noqa: E501
                        unsafe_allow_html=True,
                    )
                    time.sleep(0.3)

                # Parse the response into a list of questions
                questions = [
                    line.strip() for line in streaming_content.split("\n") if line.strip()
                ]
                if len(questions) > MAX_QUESTIONS:  # Limit to MAX_QUESTIONS questions
                    questions = questions[:MAX_QUESTIONS]

                # Step 2: Answer each question
                answers = []
                question_answer_pairs = []
                try:
                    for idx, question in enumerate(questions):
                        with st.spinner(
                            f"🚀 [Deep Research] Answering question {idx + 1}/{len(questions)}: '{question}'...",  # noqa: E501
                            show_time=True,
                        ):
                            answer_prompt = ANSWER_PROMPT_TEMPLATE.format(
                                question=question
                            )
                            chat_session = st.session_state.chat_client.start_chat(
                                history=[]
                            )
                            answer_response = chat_session.send_message(
                                answer_prompt, stream=True
                            )

                            # Stream answers
                            message_container.empty()
                            answer_streaming_content = ""
                            for chunk in answer_response:
                                answer_streaming_content += chunk.text.strip()
                                message_container.markdown(
                                    f"""
                                    <div class="message assistant">
                                        <div class="message-avatar">😽</div>
                                        <div class="message-content">
                                            <div class="message-bubble" style="background-color: #2c2222b3; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                                                <b>Question:</b> {question}<br>
                                                <b>Answer:</b><br> {answer_streaming_content}
                                            </div>
                                        </div>
                                    </div>
                                    """,  # noqa: E501
                                    unsafe_allow_html=True,
                                )
                                time.sleep(0.3)

                            answers.append(answer_streaming_content.strip())
                            question_answer_pairs.append(
                                f"---\nQuestion: {question}\n"
                                f"Answer: {answer_streaming_content.strip()}"
                            )
                except:  # noqa: E722, S110
                    pass

                # Step 3: Generate final summary/response
                with st.spinner(
                    "🚀 [Deep Research] Generating final response...",
                    show_time=True,
                ):
                    summary_prompt = SUMMARY_PROMPT_TEMPLATE.format(
                        original_question=prompt,
                        question_answer_pairs="\n".join(question_answer_pairs),
                    )

                    # Send summary prompt to generate final response
                    chat_session = st.session_state.chat_client.start_chat(history=[])
                    final_response = chat_session.send_message(
                        summary_prompt, stream=True
                    )

                    # Stream the final response
                    message_container.empty()
                    final_streaming_content = ""
                    for chunk in final_response:
                        final_streaming_content += chunk.text.strip()
                        message_container.markdown(
                            f"""
                            <div class="message assistant">
                                <div class="message-avatar">😽</div>
                                <div class="message-content">
                                    <div class="message-bubble" style="background-color: #2c2222b3; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                                        <b>Final Response:</b> {final_streaming_content}
                                    </div>
                                </div>
                            </div>
                            """,  # noqa: E501
                            unsafe_allow_html=True,
                        )
                        time.sleep(0.3)

                # Log final response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_streaming_content.strip(),
                    "timestamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
                    "model": MODEL_NAME[0],
                })

                prompt = ""

                st.rerun()

            except Exception as e:  # noqa: BLE001
                st.error(f"[ERROR] Deep Research failed! Error: {e}")


if __name__ == "__main__":
    main()
