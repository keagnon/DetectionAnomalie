import streamlit as st
import plotly.express as px
import pandas as pd

# Page Configuration (must be the first Streamlit command)
st.set_page_config(page_title="State of LLM Apps", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Sidebar Hover Effect and Title Colors
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

# Key Takeaways Section
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

# Developer Growth Section (with line chart)
st.header("App & Developer Growth")
growth_data = {
    "Week Start": pd.date_range(start="2023-04-01", periods=20, freq="W"),
    "Apps Created": [500, 1000, 1200, 1400, 1700, 2000, 2500, 3000, 3200, 3400, 3600, 3700, 3900, 4100, 4200, 4300, 4400, 4500, 4600, 4700],
    "Unique Developers": [200, 400, 600, 700, 800, 1000, 1300, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800]
}

df_growth = pd.DataFrame(growth_data)
fig_growth = px.line(df_growth, x="Week Start", y=["Apps Created", "Unique Developers"], title="App & Developer Growth")
st.plotly_chart(fig_growth, use_container_width=True)

# LLMs Adoption at a Glance Section (with bar chart)
st.header("LLMs Adoption at a Glance")
llm_adoption_data = {
    "LLM Tool": ["OpenAI", "LangChain", "HuggingFace", "Transformers", "Faiss", "Pinecone", "Llama Index", "ChromaDB", "Cohere", "Anthropic"],
    "Usage %": [72.8, 54.4, 16.3, 14.4, 6.6, 6.4, 4.4, 4.1, 1.2, 1.0]
}

df_llm = pd.DataFrame(llm_adoption_data)
fig_llm = px.bar(df_llm, x="LLM Tool", y="Usage %", title="LLM Adoption by Tool")
st.plotly_chart(fig_llm, use_container_width=True)

# Concerns Building with LLMs Section
st.header("Concerns building with LLMs")
st.subheader("What is your biggest concern when building LLM apps?")
st.write("In June 2023, 980 respondents from the Streamlit community answered:")

# Create donut charts for each concern
col1, col2, col3, col4 = st.columns(4)

with col1:
    fig_trust = px.pie(values=[36, 64], names=["Trust", ""], hole=0.6)
    fig_trust.update_traces(textinfo='percent+label', marker=dict(colors=['#00BFFF', '#e8e8e8']))
    fig_trust.update_layout(showlegend=False, title="Trust", annotations=[dict(text='36%', x=0.5, y=0.5, font_size=20, showarrow=False)])
    st.plotly_chart(fig_trust, use_container_width=True)

with col2:
    fig_privacy = px.pie(values=[28, 72], names=["Privacy", ""], hole=0.6)
    fig_privacy.update_traces(textinfo='percent+label', marker=dict(colors=['#00FF00', '#e8e8e8']))
    fig_privacy.update_layout(showlegend=False, title="Privacy", annotations=[dict(text='28%', x=0.5, y=0.5, font_size=20, showarrow=False)])
    st.plotly_chart(fig_privacy, use_container_width=True)

with col3:
    fig_cost = px.pie(values=[19, 81], names=["Cost", ""], hole=0.6)
    fig_cost.update_traces(textinfo='percent+label', marker=dict(colors=['#FFD700', '#e8e8e8']))
    fig_cost.update_layout(showlegend=False, title="Cost", annotations=[dict(text='19%', x=0.5, y=0.5, font_size=20, showarrow=False)])
    st.plotly_chart(fig_cost, use_container_width=True)

with col4:
    fig_skills = px.pie(values=[17, 83], names=["Skills", ""], hole=0.6)
    fig_skills.update_traces(textinfo='percent+label', marker=dict(colors=['#FF6347', '#e8e8e8']))
    fig_skills.update_layout(showlegend=False, title="Skills", annotations=[dict(text='17%', x=0.5, y=0.5, font_size=20, showarrow=False)])
    st.plotly_chart(fig_skills, use_container_width=True)

# Footer or any additional info
st.markdown("---")
st.markdown("<p style='text-align: center;'>Built with ❤️ using Streamlit.</p>", unsafe_allow_html=True)

# Optional: Embedding Social Media Links
st.markdown("""
    <div style='text-align: center;'>
        <a href='https://github.com/' target='_blank'>GitHub</a> |
        <a href='https://www.linkedin.com/' target='_blank'>LinkedIn</a> | 
        <a href='https://twitter.com/' target='_blank'>Twitter</a>
    </div>
""", unsafe_allow_html=True)
