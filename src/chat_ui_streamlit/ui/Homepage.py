from __future__ import annotations  # noqa: N999

import sys
from pathlib import Path

import streamlit as st

from chat_ui_streamlit.ui.components.home_component import (
    render_footer,
    render_features,
    render_hero_section,
    render_getting_started,
)


sys.path.append(str(Path(__file__).parent.parent))
# Page configuration
st.set_page_config(
    page_title="Deep Research Assistant - Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main() -> None:
    """Main homepage function."""
    render_hero_section()

    st.markdown("---")
    render_features()

    st.markdown("---")
    render_getting_started()
    render_footer()

    # Call-to-action button
    st.markdown("---")
    _, col2, _ = st.columns([1, 1, 1])
    with col2:
        if st.button(
            "🚀 Start Research Session", type="primary", use_container_width=True
        ):
            st.switch_page("./pages/CAT_Deep_Research.py")


if __name__ == "__main__":
    main()
