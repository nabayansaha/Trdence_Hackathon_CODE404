import streamlit as st
import os
import tempfile
import logging
from agents.states import MnAagentState
from agents.research_agent import create_research_agent_graph
from RAG.rag_llama_demo import RAG
import uuid
from typing import Dict, Any
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Initialize session state
if "process_state" not in st.session_state:
    st.session_state.process_state = "init"
if "rag_instances" not in st.session_state:
    st.session_state.rag_instances = {}
if "indexes" not in st.session_state:
    st.session_state.indexes = {}
if "retrievers" not in st.session_state:
    st.session_state.retrievers = {}
if "mna_state" not in st.session_state:
    st.session_state.mna_state = None
if "research_graph" not in st.session_state:
    st.session_state.research_graph = None


def save_uploaded_file(uploaded_file) -> str:
    """Save uploaded file and return the path"""
    if uploaded_file is not None:
        try:
            # Create a temporary file
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, uploaded_file.name)

            # Write the file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return file_path
        except Exception as e:
            st.error(f"Error saving file: {e}")
            return None
    return None


def initialize_rag(company_name: str, file_path: str) -> Dict[str, Any]:
    """Initialize RAG instance for a company"""
    try:
        logger.info(f"Initializing RAG for {company_name}")
        rag_instance = RAG(file_path)
        index = rag_instance.create_db(db_name=str(company_name))
        retriever = index.as_retriever()

        return {"rag_instance": rag_instance, "index": index, "retriever": retriever}
    except Exception as e:
        logger.error(f"Error initializing RAG: {e}")
        st.error(f"Error initializing RAG for {company_name}: {e}")
        return None


# Set page config
st.set_page_config(page_title="M&A Research Assistant", page_icon="🔍", layout="wide")

# Main title
st.title("🔍 M&A Research Assistant")
st.markdown("---")

# Initialize companies
if st.session_state.process_state == "init":
    with st.form("company_form"):
        st.subheader("Company Information")
        col1, col2 = st.columns(2)

        with col1:
            company_a_name = st.text_input("Company A Name")
            company_a_file = st.file_uploader(
                "Upload Company A Document", type=["pdf", "txt"]
            )

        with col2:
            company_b_name = st.text_input("Company B Name")
            company_b_file = st.file_uploader(
                "Upload Company B Document", type=["pdf", "txt"]
            )

        submit_button = st.form_submit_button("Initialize Research")

        if submit_button:
            if not all(
                [company_a_name, company_b_name, company_a_file, company_b_file]
            ):
                st.error("Please provide all required information.")
            else:
                with st.spinner("Initializing RAG systems..."):
                    # Save uploaded files
                    company_a_path = save_uploaded_file(company_a_file)
                    company_b_path = save_uploaded_file(company_b_file)

                    if company_a_path and company_b_path:
                        # Initialize RAG for both companies
                        company_a_rag = initialize_rag(company_a_name, company_a_path)
                        company_b_rag = initialize_rag(company_b_name, company_b_path)

                        if company_a_rag and company_b_rag:
                            # Store RAG instances and related objects
                            st.session_state.rag_instances = {
                                company_a_name: company_a_rag["rag_instance"],
                                company_b_name: company_b_rag["rag_instance"],
                            }
                            st.session_state.indexes = {
                                company_a_name: company_a_rag["index"],
                                company_b_name: company_b_rag["index"],
                            }
                            st.session_state.retrievers = {
                                company_a_name: company_a_rag["retriever"],
                                company_b_name: company_b_rag["retriever"],
                            }

                            # Initialize MnAagentState
                            st.session_state.mna_state = MnAagentState(
                                company_a_name=company_a_name,
                                company_b_name=company_b_name,
                                company_a_doc=company_a_path,
                                company_b_doc=company_b_path,
                                rag_instances=st.session_state.rag_instances,
                                indexes=st.session_state.indexes,
                                retrievers=st.session_state.retrievers,
                            )

                            # Create research graph for company A
                            st.session_state.research_graph = (
                                create_research_agent_graph(
                                    st.session_state.mna_state, "a"
                                )
                            )

                            st.session_state.process_state = "research"
                            st.rerun()

# Research Process
elif st.session_state.process_state == "research":
    st.subheader("Research Process")

    # Display company information
    st.info(
        f"Analyzing: {st.session_state.mna_state.company_a_name} and {st.session_state.mna_state.company_b_name}"
    )

    # Create research graphs for both companies
    if "research_graph_a" not in st.session_state:
        st.session_state.research_graph_a = create_research_agent_graph(
            st.session_state.mna_state, "a"
        )
    if "research_graph_b" not in st.session_state:
        st.session_state.research_graph_b = create_research_agent_graph(
            st.session_state.mna_state, "b"
        )

    # Start the research process
    try:
        with st.spinner("Processing research workflow..."):
            # Process Company A
            st.write("### Processing Company A")
            final_state_a = st.session_state.research_graph_a.invoke(
                st.session_state.mna_state, config={"recursion_limit": 1000}
            )

            # Process Company B
            st.write("### Processing Company B")
            final_state_b = st.session_state.research_graph_b.invoke(
                final_state_a,  # Use the state from company A as the starting point
                config={"recursion_limit": 1000},
            )

            st.success("Vector DB Update Complete for both companies")
            st.session_state.process_state = "complete"

    except Exception as e:
        st.error(f"Error during research process: {e}")
        logger.error(f"Research process error: {e}")

# Process Complete
elif st.session_state.process_state == "complete":
    st.success("Research process completed successfully!")

    if st.button("Start New Research"):
        # Reset session state
        st.session_state.process_state = "init"
        st.session_state.rag_instances = {}
        st.session_state.indexes = {}
        st.session_state.retrievers = {}
        st.session_state.mna_state = None
        st.session_state.research_graph = None
        st.rerun()

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Team CODE404")
