import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="State of LLM Apps", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for dark theme, hover effects, and text colors
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
    /* Subheaders in white */
    h2, h3, h4 {
        color: #FFFFFF !important;  /* White subheaders */
    }
    /* Table Styling */
    .css-1ssif6e.e16nr0p30 {
        background-color: #2B2B2B !important;
        color: #FFFFFF !important;
    }
    /* For progress bars */
    .stProgress {
        color: white !important;
    }
    /* General text color */
    .stText {
        color: #FFFFFF !important;
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

# Key Takeaways
st.header("Key Takeaways")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("OpenAI is dominant")
    st.write("73% use GPT models")
    st.button("Top models")

with col2:
    st.subheader("The future is multi-agent")
    st.write("55% use orchestration")
    st.button("Top orchestration tools")

with col3:
    st.subheader("Most apps bypass vector magic")
    st.write("Only 18% use vector retrieval")
    st.button("Top vector retrieval tools")

with col4:
    st.subheader("Chatbots are on the rise")
    st.write("31% (and growing) are chatbots")
    st.button("Are chatbots the future?")

# App & Developer Growth Section
st.header("App & Developer Growth")
growth_data = {
    "Week Start": pd.date_range(start="2023-04-01", periods=20, freq="W"),
    "Apps Created": [500, 1000, 1200, 1400, 1700, 2000, 2500, 3000, 3200, 3400, 3600, 3700, 3900, 4100, 4200, 4300, 4400, 4500, 4600, 4700],
    "Unique Developers": [200, 400, 600, 700, 800, 1000, 1300, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800]
}

df_growth = pd.DataFrame(growth_data)
fig_growth = px.line(df_growth, x="Week Start", y=["Apps Created", "Unique Developers"], title="App & Developer Growth", template="plotly_dark")
st.plotly_chart(fig_growth, use_container_width=True)

# LLM Adoption Data Section
st.header("LLMs Adoption at a Glance")

adoption_data = {
    "LLM Tool": ["OpenAI", "LangChain", "HuggingFace Hub", "Transformers", "Faiss", "Pinecone", "Llama Index", "ChromaDB", "Cohere", "Anthropic"],
    "Percent Usage in LLM Apps": [72.8, 54.4, 16.3, 14.4, 6.6, 6.4, 4.4, 4.1, 1.2, 1.0],
    "LLM Category": ["LLM models", "LLM orchestration", "LLM models", "LLM models", "Vector retrieval", "Vector retrieval", "LLM orchestration", "Vector retrieval", "LLM models", "LLM models"]
}

df_adoption = pd.DataFrame(adoption_data)

# Show detailed table of apps with dark mode styling
st.dataframe(df_adoption.style.background_gradient(cmap='Blues'))

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Built with ❤️ using Streamlit.</p>", unsafe_allow_html=True)
