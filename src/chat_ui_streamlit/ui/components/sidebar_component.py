from __future__ import annotations

import streamlit as st


def render_sidebar() -> None:
    """Render CAT sidebar."""
    st.markdown(
        """
            <div class="cat-sidebar">
                <div class="sidebar-section">
                    <div class="sidebar-item">
                        <span class="sidebar-item-icon">✏️</span>
                        <span class="sidebar-item-text">New conversation</span>
                    </div>
                    <div class="sidebar-item">
                        <span class="sidebar-item-icon">🔍</span>
                        <span class="sidebar-item-text">CAT</span>
                    </div>
                </div>
                <div class="sidebar-section">
                    <div class="sidebar-section-title">Chats</div>
                    <div class="sidebar-item active">
                        <span class="sidebar-item-icon">💼</span>
                        <span class="sidebar-item-text">CAT Research Session</span>
                    </div>
                    <div class="sidebar-item">
                        <span class="sidebar-item-icon">💬</span>
                        <span class="sidebar-item-text">Report Analysis</span>
                    </div>
                    <div class="sidebar-item">
                        <span class="sidebar-item-icon">💬</span>
                        <span class="sidebar-item-text">Market Research</span>
                    </div>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )
