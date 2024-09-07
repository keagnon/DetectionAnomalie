import streamlit as st
import plotly.express as px
import pandas as pd

# Page Configuration (must be the first Streamlit command)
st.set_page_config(page_title="State of LLM Apps", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Sidebar Hover Effect, Title Colors, and Dark Mode
st.markdown("""
    <style>
    /* Sidebar hover color */
    .css-1d391kg:hover {
        color: #4CAF50 !important;  /* Green color on hover */
    }
    /* Sidebar text styling */
    .css-1d391kg {
        color: #FFFFFF !important;  /* White color for sidebar text */
        font-size: 16px;
    }
    /* Main header in green */
    h1 {
        color: #4CAF50 !important;  /* Green main title */
        font-weight: bold;
    }
    /* Subheaders in black */
    h2, h3, h4 {
        color: #000000 !important;  /* Black subheaders */
    }
    /* Table Styling */
    .css-1ssif6e.e16nr0p30 {
        background-color: #2B2B2B !important;
        color: #FFFFFF !important;
    }
    .css-zt5igj {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Menu
st.sidebar.title("State of LLM Apps 2023")
st.sidebar.markdown("### Key takeaways")
st.sidebar.markdown("### App and developer growth")
st.sidebar.markdown("### LLMs adoption at-a-glance")
st.sidebar.markdown("### Top models")
st.sidebar.markdown("### Top orchestration tools")
st.sidebar.markdown("### Top vector retrieval tools")
st.sidebar.markdown("### Are chatbots the future?")
st.sidebar.markdown("### Gallery of LLM apps")
st.sidebar.markdown("### Concerns building with LLMs")
st.sidebar.markdown("### LLM app architecture")
st.sidebar.markdown("### About Streamlit")
st.sidebar.markdown("### Methodology")

# Header Section
st.markdown("<h1 style='text-align: center;'>State of LLM Apps 2023</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: yellow;'>Explore emerging trends, tools, and use cases in LLM app development from 29,183 apps built by 17,926 developers.</p>", unsafe_allow_html=True)
st.markdown("---")

# Gallery of LLM Apps Section
st.header("Gallery of LLM Apps")
st.write("Explore and search through popular LLM apps from the Streamlit community cloud.")

# Sample app data (replace with actual data)
app_data = {
    "App Name": ["etedward-gptzero-main", "chatgptm", "scooter7-web-hn", "langchain-quickstart", "wvsu-mis-weebsugpt"],
    "App URL": [
        "https://etedward-gptzero-main.streamlit.app",
        "https://chatgptm.streamlit.app",
        "https://scooter7-web-hn.streamlit.app",
        "https://langchain-quickstart.streamlit.app",
        "https://wvsu-mis-weebsugpt.streamlit.app"
    ],
    "Cumulative Views": [102911, 61023, 56650, 51883, 46493],
    "GitHub URL": [
        "https://github.com/etedward/gptzero-main",
        "https://github.com/chatgptm/repo",
        "https://github.com/scooter7/web-hn",
        "https://github.com/langchain/quickstart",
        "https://github.com/wvsu-mis/weebsugpt"
    ],
    "App Type": ["single text input", "single text input", "single text input", "single text input", "single text input"]
}

df_apps = pd.DataFrame(app_data)

# Create progress bars to represent views
st.subheader("Top LLM Apps")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.image("https://via.placeholder.com/150", caption="etedward-gptzero-main")
    st.markdown("[View source](https://etedward-gptzero-main.streamlit.app)")
    st.write(f"Cumulative Views: {app_data['Cumulative Views'][0]}")
    st.progress(int(app_data['Cumulative Views'][0] / 102911 * 100))

with col2:
    st.image("https://via.placeholder.com/150", caption="chatgptm")
    st.markdown("[View source](https://chatgptm.streamlit.app)")
    st.write(f"Cumulative Views: {app_data['Cumulative Views'][1]}")
    st.progress(int(app_data['Cumulative Views'][1] / 102911 * 100))

with col3:
    st.image("https://via.placeholder.com/150", caption="scooter7-web-hn")
    st.markdown("[View source](https://scooter7-web-hn.streamlit.app)")
    st.write(f"Cumulative Views: {app_data['Cumulative Views'][2]}")
    st.progress(int(app_data['Cumulative Views'][2] / 102911 * 100))

with col4:
    st.image("https://via.placeholder.com/150", caption="langchain-quickstart")
    st.markdown("[View source](https://langchain-quickstart.streamlit.app)")
    st.write(f"Cumulative Views: {app_data['Cumulative Views'][3]}")
    st.progress(int(app_data['Cumulative Views'][3] / 102911 * 100))

with col5:
    st.image("https://via.placeholder.com/150", caption="wvsu-mis-weebsugpt")
    st.markdown("[View source](https://wvsu-mis-weebsugpt.streamlit.app)")
    st.write(f"Cumulative Views: {app_data['Cumulative Views'][4]}")
    st.progress(int(app_data['Cumulative Views'][4] / 102911 * 100))

# Show detailed table of apps (with dark mode styling)
st.markdown("### App Details")
st.dataframe(df_apps.style.background_gradient(cmap='Blues'))

# Footer or any additional info
st.markdown("---")

# Results section at the bottom of the dataframe
st.markdown("<p style='text-align:left; color: green;'><b>Results:</b> 20,052 public apps</p>", unsafe_allow_html=True)

# Optional: Embedding Social Media Links
st.markdown("""
    <div style='text-align: center;'>
        <a href='https://github.com/' target='_blank'>GitHub</a> |
        <a href='https://www.linkedin.com/' target='_blank'>LinkedIn</a> | 
        <a href='https://twitter.com/' target='_blank'>Twitter</a>
    </div>
""", unsafe_allow_html=True)
