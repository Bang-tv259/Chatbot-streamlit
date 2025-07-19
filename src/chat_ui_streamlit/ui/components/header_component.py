from __future__ import annotations

import streamlit as st


def render_header() -> None:
    """Render CAT header."""
    st.markdown(
        """
            <div class="cat-header">
                <div class="header-left">
                    <button class="menu-btn">☰</button>
                </div>
                <div class="header-center">
                    <div class="model-selector">
                        <span>Chat Intelligence Platform Pro ▼</span>
                    </div>
                </div>
                <div class="header-right">
                    <button class="upgrade-btn">🔺 Upgrade</button>
                    <div class="user-avatar">TB</div>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )
