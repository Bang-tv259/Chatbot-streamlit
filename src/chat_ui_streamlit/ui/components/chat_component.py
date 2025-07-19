from __future__ import annotations

import streamlit as st


def render_welcome() -> None:
    """Render welcome screen."""
    st.markdown(
        """
            <div class="welcome-container">
                <h1 class="welcome-text">Hello Cat!</h1>
            </div>
        """,
        unsafe_allow_html=True,
    )


def render_message(message: dict[str, str], *, is_user: bool = False) -> None:
    """Render chat message."""
    if is_user:
        avatar = "TB"
        role_class = "user"
    else:
        avatar = "😽"
        role_class = "assistant"

    st.markdown(
        f"""
            <div class="message {role_class}">
                <div class="message-avatar">{avatar}</div>
                <div class="message-content">
                    <div class="message-bubble">
                        {message["content"]}
                    </div>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )


def process_input() -> None:
    """Process user input."""
    if st.session_state["cat_input"].strip():
        st.session_state["cat_temp"] = st.session_state["cat_input"].strip()
        st.session_state["cat_submit"] = True
        st.session_state["cat_input"] = ""


def render_input() -> str:
    """Render input field and buttons."""
    st.markdown(
        "<hr style='border: none; border-top: 2px solid #4f5f71; margin-left: 280px;'>",
        unsafe_allow_html=True,
    )
    deep_research_btn = st.button(
        "🔍 Deep Research", key="deep_research", use_container_width=False
    )
    if deep_research_btn:
        st.session_state["deep_research_clicked"] = not st.session_state[
            "deep_research_clicked"
        ]
    if st.session_state["deep_research_clicked"]:
        st.markdown(
            "<p style='margin-left: 448px; margin-top: -40px; font-size: -40px;'>✔️</p>",
            unsafe_allow_html=True,
        )

    col1, col2 = st.columns([8, 1])
    with col1:
        _ = st.text_input(
            label="💬 Ask CAT:",
            placeholder="💼 Ask CAT about anything...",
            label_visibility="collapsed",
            key="cat_input",
            on_change=process_input,
        )
    with col2, st.container():
        st.button("➤", use_container_width=True, on_click=process_input)

    if st.session_state["cat_submit"]:
        st.session_state["cat_submit"] = False
        return str(st.session_state["cat_temp"])

    return ""
