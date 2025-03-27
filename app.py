import streamlit as st
from utils.chat import Chat
from utils.messages import HumanMessage, AIMessage
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# Set page configuration
st.set_page_config(
    page_title="SAMAR.AI - M&A Analysis Platform",
    page_icon="💼",
    layout="wide"
)

# Initialize Chat instance
@st.cache_resource
def get_chat_instance():
    return Chat()

chat_instance = get_chat_instance()

# App header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🚀 SAMAR.AI")
    st.subheader("Strategic Acquisition & Merger Analysis Resource")
with col2:
    st.image("https://via.placeholder.com/150?text=SAMAR.AI", width=150)

st.markdown("---")

# Sidebar for navigation and options
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to", ["Company Analysis", "M&A Recommendations", "About"])
    
    st.markdown("---")
    
    # Fixed model selection - only one option
    model = "databricks-meta-llama-3-3-70b-instruct"
    st.info(f"Using model: {model}")
    
    # Temperature setting
    temperature = st.slider("Response Creativity", 0.0, 1.0, 0.2, 0.1, 
                           help="Lower values produce more focused, deterministic responses. Higher values produce more creative, varied responses.")
    
    st.markdown("---")
    st.markdown("© 2025 SAMAR.AI")
    st.caption(f"Current user: bibhabasuiitkgp")
    st.caption(f"Last updated: 2025-03-27")

# Main content logic based on selected page
if page == "Company Analysis":
    st.header("Company Analysis Dashboard")
    
    # Company input section
    company_name = st.text_input("Enter company name:", "")
    
    analyze_button = st.button("Analyze Company")
    
    # Display analysis results when button is clicked
    if analyze_button and company_name:
        with st.spinner(f"Analyzing {company_name}..."):
            try:
                # Create message for LLM
                prompt = f"""
                Provide a comprehensive analysis of {company_name} for M&A purposes with the following structure:
                1. Company Overview (brief description, industry, founding year)
                2. Financial Health (revenue, profit margins, growth trends)
                3. Market Position (market share, competitive advantage, threats)
                4. Key Assets (intellectual property, talent, technology)
                5. Potential Synergies (areas of value for acquisition/merger)
                6. Risk Assessment (regulatory, financial, operational risks)
                7. Valuation Estimate (approximate worth and justification)
                
                Format the information clearly with headers.
                """
                
                # Get response from LLM
                messages = [HumanMessage(content=prompt)]
                updated_messages, input_tokens, output_tokens = chat_instance.invoke_llm_langchain(
                    messages, 
                    model=model, 
                    temperature=temperature
                )
                
                # Extract and display AI response
                company_analysis = updated_messages[-1].content
                
                # Display token usage
                col1, col2 = st.columns(2)
                with col1:
                    st.caption(f"Input tokens: {input_tokens}")
                with col2:
                    st.caption(f"Output tokens: {output_tokens}")
                
                # Display the analysis in an expandable container
                with st.expander("Company Analysis Results", expanded=True):
                    st.markdown(company_analysis)
                
                # Create mock data for dashboard visualizations
                st.subheader("Financial Overview")
                
                # Mock financial data visualization
                col1, col2 = st.columns(2)
                
                with col1:
                    # Revenue chart
                    chart_data = pd.DataFrame({
                        'Year': ['2022', '2023', '2024', '2025 (Proj)'],
                        'Revenue (millions)': [100, 120, 160, 200]
                    })
                    
                    chart = alt.Chart(chart_data).mark_bar().encode(
                        x='Year',
                        y='Revenue (millions)',
                        color=alt.value('#1f77b4')
                    ).properties(
                        title=f"{company_name} Revenue Trend"
                    )
                    st.altair_chart(chart, use_container_width=True)
                
                with col2:
                    # Profitability chart
                    profit_data = pd.DataFrame({
                        'Metric': ['Gross Margin', 'Operating Margin', 'Net Margin'],
                        'Percentage': [45, 22, 15]
                    })
                    
                    chart = alt.Chart(profit_data).mark_bar().encode(
                        x='Metric',
                        y='Percentage',
                        color=alt.value('#2ca02c')
                    ).properties(
                        title=f"{company_name} Profitability Metrics (%)"
                    )
                    st.altair_chart(chart, use_container_width=True)
                
                # SWOT Analysis section
                st.subheader("SWOT Analysis")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("##### Strengths")
                    st.info("• Generated based on LLM analysis\n• Key company capabilities\n• Competitive advantages")
                    
                    st.markdown("##### Weaknesses")
                    st.warning("• Generated based on LLM analysis\n• Areas for improvement\n• Competitive disadvantages")
                
                with col2:
                    st.markdown("##### Opportunities")
                    st.success("• Generated based on LLM analysis\n• Market trends favorable to company\n• Potential growth areas")
                    
                    st.markdown("##### Threats")
                    st.error("• Generated based on LLM analysis\n• Market challenges\n• Competitive pressures")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your API connection and try again.")

elif page == "M&A Recommendations":
    st.header("M&A Recommendation Engine")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Target Company")
        target_company = st.text_input("Enter target company:", "")
    
    with col2:
        st.subheader("Acquiring Company")
        acquiring_company = st.text_input("Enter acquiring company:", "")
    
    if st.button("Generate M&A Analysis"):
        if target_company and acquiring_company:
            with st.spinner(f"Analyzing potential merger between {acquiring_company} and {target_company}..."):
                try:
                    # Create message for LLM
                    prompt = f"""
                    Provide a comprehensive M&A analysis for {acquiring_company} acquiring {target_company}:
                    1. Strategic Fit (alignment of business models, cultures, and goals)
                    2. Financial Analysis (deal structure, premium, expected synergies)
                    3. Integration Challenges (technical, cultural, operational)
                    4. Regulatory Concerns (antitrust issues, required approvals)
                    5. Market Response (likely stakeholder reactions)
                    6. Recommendation (proceed, reconsider, or alternative approaches)
                    
                    Format the information clearly with headers.
                    """
                    
                    # Get response from LLM
                    messages = [HumanMessage(content=prompt)]
                    updated_messages, input_tokens, output_tokens = chat_instance.invoke_llm_langchain(
                        messages, 
                        model=model, 
                        temperature=temperature
                    )
                    
                    # Extract and display AI response
                    analysis = updated_messages[-1].content
                    
                    # Display token usage
                    col1, col2 = st.columns(2)
                    with col1:
                        st.caption(f"Input tokens: {input_tokens}")
                    with col2:
                        st.caption(f"Output tokens: {output_tokens}")
                    
                    # Display the analysis
                    st.markdown(analysis)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.info("Please check your API connection and try again.")
        else:
            st.warning("Please enter both target and acquiring company names.")

else:  # About page
    st.header("About SAMAR.AI")
    
    st.markdown("""
    ## Strategic Acquisition & Merger Analysis Resource
    
    SAMAR.AI is an advanced platform designed to assist in mergers and acquisitions analysis, 
    similar to services provided by top consulting firms like BCG. Our platform leverages 
    state-of-the-art language models to provide comprehensive insights and analysis.
    
    ### Key Features:
    - Company analysis and evaluation
    - M&A compatibility assessment
    - Financial projection modeling
    - Risk assessment and mitigation strategies
    - Integration planning assistance
    
    ### Technology Stack:
    - Advanced LLM integration via Databricks (Llama 3 70B)
    - Interactive visualizations with Streamlit
    - Custom analytics engine for M&A-specific insights
    
    ### Contact Us:
    For more information or to schedule a demo, please contact our team at info@samar-ai.com
    """)

# Add a footer
st.markdown("---")
st.caption("SAMAR.AI - Powered by advanced LLM technology")