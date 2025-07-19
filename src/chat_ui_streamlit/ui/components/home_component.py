from __future__ import annotations

from datetime import UTC, datetime

import streamlit as st

from chat_ui_streamlit.core.constants import COLORS


def render_hero_section() -> None:
    """Render the hero section."""
    st.markdown(
        f"""
            <div style="
                background: linear-gradient(135deg, {COLORS["PRIMARY"]}, {COLORS["SECONDARY"]});
                color: white;
                padding: 3rem 2rem;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            ">
                <h1 style="font-size: 3rem; margin-bottom: 1rem;">🔬 Deep Research Assistant</h1>
                <h3 style="font-weight: 300; margin-bottom: 2rem;">AI-Powered Comprehensive Research Platform</h3>
                <p style="font-size: 1.2rem; opacity: 0.9;">
                    Conduct in-depth research with advanced AI analysis, multi-source verification,
                    and comprehensive insights generation.
                </p>
            </div>
        """,  # noqa: E501
        unsafe_allow_html=True,
    )


def render_features() -> None:
    """Render feature cards."""
    st.markdown("## 🚀 Key Features")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
                <div style="
                    background: #749d7f;
                    padding: 2rem;
                    border-radius: 10px;
                    border-left: 4px solid {COLORS["PRIMARY"]};
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    height: 250px;
                ">
                    <h3>🔍 Multi-Source Research</h3>
                    <p>Search across multiple engines including Google, Bing, and Google Scholar for comprehensive source discovery.</p>
                    <ul>
                        <li>Web search integration</li>
                        <li>Academic paper discovery</li>
                        <li>Real-time content extraction</li>
                    </ul>
                </div>
            """,  # noqa: E501
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
                <div style="
                    background: #749d7f;
                    padding: 2rem;
                    border-radius: 10px;
                    border-left: 4px solid {COLORS["SUCCESS"]};
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    height: 250px;
                ">
                    <h3>🧠 AI-Powered Analysis</h3>
                    <p>Advanced AI models analyze and synthesize information to provide deep insights and actionable recommendations.</p>
                    <ul>
                        <li>Gemini integration</li>
                        <li>Contextual understanding</li>
                    </ul>
                </div>
            """,  # noqa: E501
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
                <div style="
                    background: #749d7f;
                    padding: 2rem;
                    border-radius: 10px;
                    border-left: 4px solid {COLORS["WARNING"]};
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    height: 250px;
                ">
                    <h3>📊 Research Types</h3>
                    <p>Specialized research modes tailored for different domains and use cases.</p>
                    <ul>
                        <li>Market Analysis</li>
                        <li>Technical Investigation</li>
                        <li>Comprehensive Studies</li>
                    </ul>
                </div>
            """,  # noqa: E501
            unsafe_allow_html=True,
        )


def render_getting_started() -> None:
    """Render the redesigned 'Getting Started' section."""
    st.markdown(
        """
        <h2 style="
            -webkit-background-clip: text;
            font-size: 2.5rem;
            font-weight: bold;
        ">
        🚀 Getting Started
        </h2>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            """
            <div style="
                background-color: rgb(202 211 202);
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            ">
                <h3 style="color: #4f5f71;">📚 How to Use the Deep Research Assistant</h3>
                <ol style="font-size: 1rem; line-height: 1.8; color: #333; padding-left: 1.2rem;">
                    <li><b>Navigate to the Chatbot:</b> Click on "CAT Deep Research" in the sidebar.</li>
                    <li><b>Configure Research Settings:</b> Choose your research type, search engine, and AI model.</li>
                    <li><b>Ask Your Question:</b> Type your research query in natural language.</li>
                    <li><b>Review Results:</b> Analyze the comprehensive research results with sources, insights, and recommendations.</li>
                    <li><b>Ask Follow-ups:</b> Continue the conversation to dive deeper into specific aspects.</li>
                </ol>
                <h4 style="color: #4f5f71; margin-top: 20px;">🔍 Example Queries</h4>
                <ul style="font-size: 1rem; line-height: 1.8; color: #333; padding-left: 1.2rem;">
                    <li>"What are the latest developments in quantum computing?"</li>
                    <li>"Analyze the market trends for electric vehicles in 2024."</li>
                    <li>"Compare different machine learning frameworks for deep learning."</li>
                    <li>"Research the environmental impact of cryptocurrency mining."</li>
                </ul>
            </div>
            """,  # noqa: E501
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #3578E5, #4CAF50);
                color: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    top: -13px;
                    right: -13px;
                    background: linear-gradient(135deg, rgb(203 186 93), #8d7637);
                    border-radius: 50%;
                    width: 32px;
                    height: 32px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
                    border: 2px solid white;
                ">
                    📌
                </div>
                <h4>💡 Tips for Better Results</h4>
                <ul style="font-size: 1rem; line-height: 1.8;">
                    <li>Be specific in your queries.</li>
                    <li>Choose the appropriate research type.</li>
                    <li>Review source relevance.</li>
                    <li>Ask follow-up questions.</li>
                    <li>Export important findings.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_footer() -> None:
    """Render footer."""
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
                <div style="text-align: center;">
                    <h4>🔬 Research Engine</h4>
                    <p>Powered by advanced AI models and real-time web search capabilities</p>
                </div>
            """,  # noqa: E501
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
                <div style="text-align: center;">
                    <h4>🚀 Version</h4>
                    <p>Deep Research Assistant v1.0<br/>Built with Streamlit & Gemini</p>
                </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        current_time = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(
            f"""
                <div style="text-align: center;">
                    <h4>⏰ Current Time</h4>
                    <p>{current_time}<br/>Ready for research</p>
                </div>
            """,
            unsafe_allow_html=True,
        )
