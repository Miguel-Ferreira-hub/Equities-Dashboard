import streamlit as st
import time
from utils import hide_sidebar_navigation

hide_sidebar_navigation()

# ---------- Page Config ----------
st.set_page_config(
    page_title="Dashboard Selection",
    page_icon="📈",
    layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 700;
    margin-top: 80px;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #9ca3af;
    margin-bottom: 60px;
}

/* Navigation buttons */
div.stButton > button {
    width: 100%;
    height: 180px;
    border-radius: 15px;
    border: 1px solid #374151;
    background-color: #111827;
    color: white;
    font-size: 24px;
    font-weight: 600;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    border-color: #60a5fa;
    background-color: #1f2937;
    transform: translateY(-3px);
}

</style>
""", unsafe_allow_html=True)

# ---------- Header ----------

# st.markdown(
#     '<div class="main-title">Dashboard Selection</div>',
#     unsafe_allow_html=True
# )

title_text = "Equities Dashboard"
subheader_text = "Select Dashboard To Begin"

title_placeholder = st.empty()
subheader_placeholder = st.empty()

animated_title = ""

for char in title_text:
    animated_title += char
    title_placeholder.markdown(
        f"<h1 style='text-align:center; font-weight:700;'>{animated_title}</h1>",
        unsafe_allow_html=True
    )
    time.sleep(0.045)

time.sleep(0.2)

animated_subheader = ""

for char in subheader_text:
    animated_subheader += char
    subheader_placeholder.markdown(
        f"<h3 style='text-align:center; color:#A0A0A0; font-weight:400;'>{animated_subheader}</h3>",
        unsafe_allow_html=True
    )
    time.sleep(0.035)

# ---------- Sidebar ----------

with st.sidebar:

    st.title("Select Dashboard",text_alignment="center")

    if st.button(
        "🛡️\n\nDefence",
        key="Defence_sidebar",
        use_container_width=True
        ):
            st.switch_page("pages/defence.py")

    if st.button(
        "🏦\n\nBanking",
        key="Banking_sidebar",
        use_container_width=True
    ):
        st.switch_page("pages/banking.py")

    if st.button(
        "💻\n\nTechnology",
        key="Technology_sidebar",
        use_container_width=True
    ):
        st.switch_page("pages/technology.py")

    if st.button(
        "🤖\n\nSemiconductors & AI",
        key="Semiconductors & AI_sidebar",
        use_container_width=True
    ):
        st.switch_page("pages/semiconductors.py")

    if st.button(
        "🏥\n\nHealthcare",
        key="Healthcare_sidebar",
        use_container_width=True
    ):
        st.switch_page("pages/healthcare.py")

    if st.button(
        "🛒\n\nConsumer Staples",
        key="Consumer_Staples_sidebar",
        use_container_width=True
    ):
        st.switch_page("pages/consumer.py")

    if st.button(
        "💊\n\nPharmaceuticals",
        key="Pharmaceuticals_sidebar",
        use_container_width=True
    ):
        st.switch_page("pages/pharmaceuticals.py")

    if st.button(
        "🛢️\n\nEnergy, Oil & Gas",
        key="Energy,_Oil_&_Gas_sidebar",
        use_container_width=True
    ):
        st.switch_page("pages/energy.py")
        
# ---------- Old Navigation ----------
# col1, col2, = st.columns(2, gap="large")

# with col1:

#     if st.button(
#         "🛡️\n\nDefence",
#         key="Defence",
#         use_container_width=True
#     ):
#         st.switch_page("pages/defence.py")

#     if st.button(
#         "🏦\n\nBanking",
#         key="Banking",
#         use_container_width=True
#     ):
#         st.switch_page("pages/banking.py")

#     if st.button(
#         "💻\n\nTechnology",
#         key="Technology",
#         use_container_width=True
#     ):
#         st.switch_page("pages/technology.py")

#     if st.button(
#         "🤖\n\nChips",
#         key="Chips",
#         use_container_width=True
#     ):
#         st.switch_page("pages/chips.py")

# with col2:

#     if st.button(
#         "🏥\n\nHealthcare",
#         key="Healthcare",
#         use_container_width=True
#     ):
#         st.switch_page("pages/healthcare.py")

#     if st.button(
#         "🛒\n\nConsumer Staples",
#         key="Consumer Staples",
#         use_container_width=True
#     ):
#         st.switch_page("pages/consumer.py")

#     if st.button(
#         "💊\n\nPharmaceuticals",
#         key="Pharmaceuticals",
#         use_container_width=True
#     ):
#         st.switch_page("pages/pharmaceuticals.py")

#     if st.button(
#         "🛢️\n\nEnergy, Oil & Gas",
#         key="Energy, Oil & Gas",
#         use_container_width=True
#     ):
#         st.switch_page("pages/energy.py")