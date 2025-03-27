import streamlit as st
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="SAMAR.AI - Merger & Acquisition Platform",
    page_icon="💼",
    initial_sidebar_state="expanded"
)

# Apply minimal custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>SAMAR.AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Merger & Acquisition Assistant</h3>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio("", [
    "Dashboard", 
    "Deal Pipeline", 
    "Company Analysis", 
    "Deal Valuation",
    "Due Diligence"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### User Information")
st.sidebar.markdown(f"**Username:** bibhabasuiitkgp")
st.sidebar.markdown(f"**Date:** 2025-03-27")
st.sidebar.markdown(f"**Time:** 04:17:49 UTC")
st.sidebar.markdown("**Role:** M&A Analyst")

# Main content based on selected page
if page == "Dashboard":
    st.header("M&A Dashboard")
    
    st.subheader("Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Deals", "7")
    col2.metric("Completed This Quarter", "3")
    col3.metric("Total Deal Value ($M)", "1,350")
    
    st.markdown("### Recent Activities")
    st.write("- Due diligence completed for TechCorp acquisition (March 25, 2025)")
    st.write("- Initial valuation report for AgriSystems received (March 24, 2025)")
    st.write("- MedInnovate negotiations entered final stage (March 22, 2025)")
    st.write("- FinServe deal successfully closed (March 20, 2025)")
    
    st.markdown("### Upcoming Deadlines")
    st.write("- CloudSoft financial review (March 29, 2025)")
    st.write("- EnergyPlus initial proposal submission (March 31, 2025)")
    st.write("- RetailGiant board presentation (April 2, 2025)")

elif page == "Deal Pipeline":
    st.header("Deal Pipeline")
    
    st.subheader("Active Deals")
    st.table({
        'Company': ['TechCorp', 'AgriSystems', 'MedInnovate', 'RetailGiant', 'EnergyPlus', 'CloudSoft'],
        'Industry': ['Technology', 'Agriculture', 'Healthcare', 'Retail', 'Energy', 'Technology'],
        'Deal Size ($M)': [450, 120, 280, 320, 180, 390],
        'Stage': ['Due Diligence', 'Prospecting', 'Negotiation', 'Negotiation', 'Prospecting', 'Due Diligence'],
        'Expected Close': ['2025-04-15', '2025-06-30', '2025-05-10', '2025-04-22', '2025-07-15', '2025-05-05']
    })
    
    st.subheader("Add New Deal")
    with st.form("new_deal_form"):
        st.text_input("Company Name")
        st.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Retail", "Energy", "Manufacturing", "Agriculture", "Other"])
        st.number_input("Estimated Deal Size ($M)", min_value=1, max_value=10000)
        st.selectbox("Current Stage", ["Initial Contact", "Prospecting", "Negotiation", "Due Diligence", "Closing"])
        st.date_input("Expected Closing Date")
        st.text_area("Deal Notes")
        st.form_submit_button("Add Deal")

elif page == "Company Analysis":
    st.header("Company Analysis")
    
    st.selectbox("Select Company", ["TechCorp", "AgriSystems", "MedInnovate", "FinServe", "RetailGiant", "EnergyPlus", "CloudSoft"])
    
    st.subheader("Company Overview")
    st.write("**Industry:** Technology")
    st.write("**Founded:** 2010")
    st.write("**Employees:** 450")
    st.write("**Annual Revenue:** $85M")
    st.write("**Growth Rate:** 15% YoY")
    
    st.subheader("Financial Summary")
    st.write("**Revenue (FY 2024):** $85M")
    st.write("**EBITDA Margin:** 22%")
    st.write("**Net Income:** $12.5M")
    st.write("**Cash Reserves:** $18M")
    st.write("**Debt:** $7M")
    
    st.subheader("Key Products")
    st.write("1. Enterprise Analytics Platform")
    st.write("2. Mobile Data Security Suite")
    st.write("3. Cloud Integration Services")

elif page == "Deal Valuation":
    st.header("Deal Valuation")
    
    st.selectbox("Select Target Company", ["TechCorp", "AgriSystems", "MedInnovate", "RetailGiant", "EnergyPlus", "CloudSoft"])
    
    st.subheader("Valuation Methods")
    
    st.markdown("### DCF Valuation")
    st.write("**Estimated Value:** $430M")
    st.write("**Discount Rate:** 12%")
    st.write("**Terminal Growth Rate:** 3%")
    
    st.markdown("### Comparable Companies")
    st.write("**Average EV/EBITDA Multiple:** 10.5x")
    st.write("**Estimated Value:** $455M")
    
    st.markdown("### Comparable Transactions")
    st.write("**Average EV/EBITDA Multiple:** 11.2x")
    st.write("**Estimated Value:** $470M")
    
    st.markdown("### Valuation Summary")
    st.write("**Recommended Offer Range:** $440M - $465M")

elif page == "Due Diligence":
    st.header("Due Diligence Tracker")
    
    st.selectbox("Select Deal", ["TechCorp", "MedInnovate", "CloudSoft"])
    
    st.subheader("Due Diligence Categories")
    
    categories = [
        {"name": "Financial", "status": "In Progress", "completion": "75%"},
        {"name": "Legal", "status": "In Progress", "completion": "60%"},
        {"name": "Commercial", "status": "Completed", "completion": "100%"},
        {"name": "IT", "status": "In Progress", "completion": "40%"},
        {"name": "HR", "status": "Not Started", "completion": "0%"},
        {"name": "Intellectual Property", "status": "In Progress", "completion": "80%"},
    ]
    
    for category in categories:
        st.markdown(f"**{category['name']}** - {category['status']} ({category['completion']})")
    
    st.subheader("Recent Findings")
    st.write("- Revenue recognition policies require further investigation")
    st.write("- Two pending legal claims identified in overseas subsidiaries")
    st.write("- Customer concentration higher than initially reported (top client = 25%)")
    
    st.subheader("Document Repository")
    st.write("Total documents: 347")
    st.write("Reviewed documents: 212")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>© 2025 SAMAR.AI | Version 1.0</p>", unsafe_allow_html=True)