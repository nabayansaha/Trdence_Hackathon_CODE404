import streamlit as st
import os
from RAG.rag_llama_demo import RAG
import tempfile
import uuid

st.set_page_config(page_title="Document Q&A System", page_icon="📚", layout="wide")

# Initialize session state variables if they don't exist
if "rag_instances" not in st.session_state:
    st.session_state.rag_instances = {}
if "indexes" not in st.session_state:
    st.session_state.indexes = {}
if "retrievers" not in st.session_state:
    st.session_state.retrievers = {}
if "company_files" not in st.session_state:
    st.session_state.company_files = {"company_a": None, "company_b": None}
if "db_names" not in st.session_state:
    st.session_state.db_names = {"company_a": None, "company_b": None}


def get_unique_db_name(company):
    """Generate a unique database name for a company"""
    if st.session_state.db_names[company] is None:
        st.session_state.db_names[company] = f"{company}_{str(uuid.uuid4())[:8]}"
    return st.session_state.db_names[company]


def save_uploaded_file(uploaded_file):
    """Save uploaded file and return the path"""
    if uploaded_file is not None:
        # Create a temporary file
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, uploaded_file.name)

        # Write the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None


def initialize_rag(company, file_path):
    """Initialize or update RAG instance for a company"""
    if file_path:
        # Clear existing database name if it exists
        if st.session_state.db_names[company] is not None:
            # Clean up old database if needed
            try:
                import shutil

                old_db_path = os.path.join(
                    "chroma_db", st.session_state.db_names[company]
                )
                if os.path.exists(old_db_path):
                    shutil.rmtree(old_db_path)
            except Exception as e:
                st.error(f"Error cleaning up old database: {str(e)}")
            st.session_state.db_names[company] = None
            # Clear other resources
            if company in st.session_state.rag_instances:
                del st.session_state.rag_instances[company]
            if company in st.session_state.indexes:
                del st.session_state.indexes[company]
            if company in st.session_state.retrievers:
                del st.session_state.retrievers[company]

        # Generate new unique database name
        db_name = get_unique_db_name(company)

        try:
            # Initialize new RAG instance
            st.session_state.rag_instances[company] = RAG(file_path)
            st.session_state.indexes[company] = st.session_state.rag_instances[
                company
            ].create_db(db_name=db_name)
            st.session_state.retrievers[company] = st.session_state.indexes[
                company
            ].as_retriever()
            st.session_state.company_files[company] = file_path
            return True
        except Exception as e:
            st.error(f"Error initializing RAG: {str(e)}")
            # Clean up on failure
            if os.path.exists(os.path.join("chroma_db", db_name)):
                shutil.rmtree(os.path.join("chroma_db", db_name))
            st.session_state.db_names[company] = None
            return False
    return False


# Sidebar for file uploads and system status
with st.sidebar:
    st.title("📚 Document Upload")
    st.write("Upload documents for both companies")

    # File upload for Company A
    company_a_file = st.file_uploader(
        "Upload Company A Document (PDF/TXT)", type=["pdf", "txt"], key="company_a"
    )
    if company_a_file and company_a_file != st.session_state.company_files["company_a"]:
        file_path = save_uploaded_file(company_a_file)
        if initialize_rag("company_a", file_path):
            st.success("Company A document processed successfully!")

    # File upload for Company B
    company_b_file = st.file_uploader(
        "Upload Company B Document (PDF/TXT)", type=["pdf", "txt"], key="company_b"
    )
    if company_b_file and company_b_file != st.session_state.company_files["company_b"]:
        file_path = save_uploaded_file(company_b_file)
        if initialize_rag("company_b", file_path):
            st.success("Company B document processed successfully!")

# Main content area
st.title("🤖 Document Q&A System")

# Action selection
action = st.radio(
    "Choose an action:", ["Query Documents", "Update Documents"], horizontal=True
)

if action == "Query Documents":
    # Query interface
    company = st.selectbox(
        "Select Company:",
        ["company_a", "company_b"],
        format_func=lambda x: "Company A" if x == "company_a" else "Company B",
    )

    if (
        company not in st.session_state.retrievers
        or not st.session_state.retrievers[company]
    ):
        st.warning(
            f"Please upload a document for {company.replace('_', ' ').title()} first!"
        )
    else:
        query = st.text_input("Enter your query:")
        if st.button("Submit Query") and query:
            with st.spinner("Processing query..."):
                try:
                    response = st.session_state.rag_instances[company].rag_query(
                        query, st.session_state.retrievers[company]
                    )
                    st.write("### Answer:")
                    st.write(response["result"])
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

elif action == "Update Documents":
    # Update interface
    company = st.selectbox(
        "Select Company to Update:",
        ["company_a", "company_b"],
        format_func=lambda x: "Company A" if x == "company_a" else "Company B",
    )

    update_type = st.radio(
        "Choose update method:", ["Upload File", "Enter Text"], horizontal=True
    )

    if update_type == "Upload File":
        new_file = st.file_uploader("Upload new document", type=["pdf", "txt"])
        if new_file:
            file_path = save_uploaded_file(new_file)
            if st.button("Update Database"):
                with st.spinner("Updating database..."):
                    try:
                        with open(file_path, "r", encoding="utf-8") as file:
                            new_text = file.read()
                        if company in st.session_state.rag_instances:
                            db_name = st.session_state.db_names[company]
                            st.session_state.rag_instances[company].text = new_text
                            st.session_state.indexes[company] = (
                                st.session_state.rag_instances[company].update_db(
                                    db_name=db_name, new_text=new_text
                                )
                            )
                            st.session_state.retrievers[company] = (
                                st.session_state.indexes[company].as_retriever()
                            )
                            st.success("Database updated successfully!")
                        else:
                            st.error("Please upload initial document first!")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

    else:  # Enter Text
        new_text = st.text_area("Enter new text to add:", height=200)
        if st.button("Update Database") and new_text:
            with st.spinner("Updating database..."):
                try:
                    if company in st.session_state.rag_instances:
                        db_name = st.session_state.db_names[company]
                        st.session_state.rag_instances[company].text = new_text
                        st.session_state.indexes[company] = (
                            st.session_state.rag_instances[company].update_db(
                                db_name=db_name, new_text=new_text
                            )
                        )
                        st.session_state.retrievers[company] = st.session_state.indexes[
                            company
                        ].as_retriever()
                        st.success("Database updated successfully!")
                    else:
                        st.error("Please upload initial document first!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Team CODE404")
