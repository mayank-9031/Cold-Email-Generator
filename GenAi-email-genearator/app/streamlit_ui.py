# streamlit_ui.py
import streamlit as st
import pyperclip
import platform
import subprocess
from langchain_community.document_loaders import WebBaseLoader
from styles import get_css_styles

def copy_to_clipboard(text):
    """
    Cross-platform clipboard copy function
    """
    try:
        # First try pyperclip
        pyperclip.copy(text)
    except Exception as e:
        try:
            # Fallback for Linux systems
            if platform.system() == 'Linux':
                subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'))
            else:
                raise e
        except Exception as e:
            st.error("❌ Clipboard functionality not available. Please copy manually.")
            # Show the text in a text area for easy manual copying
            st.text_area("Copy this text manually:", text, height=100)
            return False
    return True

def create_streamlit_app(llm, portfolio, clean_text):
    # Page Configuration
    st.set_page_config(
        layout="wide",
        page_title="Cold Email Generator | AI Assistant",
        page_icon="📧",
        initial_sidebar_state="expanded"
    )

    # Apply CSS styles from styles.py
    st.markdown(get_css_styles(), unsafe_allow_html=True)

    # Sidebar for inputs
    with st.sidebar:
        st.header("🔗 Input Parameters")
        with st.form("input_form"):
            url_input = st.text_input(
                "Enter Job Posting URL:",
                placeholder="https://example.com/job-post",
                help="Paste the URL of the job posting you want to analyze"
            )
            submitted = st.form_submit_button("Generate Email ✨", use_container_width=True)

        st.markdown("---")
        st.markdown("**Tips:**")
        st.markdown("- Use direct career page URLs for best results")
        st.markdown("- Make sure the URL is publicly accessible")
        st.markdown("- For long posts, processing might take 20-30 seconds")

    # Main content area
    st.title("🤖 AI Cold Email Generator")
    st.caption("Craft perfect cold emails for job applications using AI-powered analysis")

    if submitted:
        if not url_input.startswith('http'):
            st.warning("⚠️ Please enter a valid URL starting with http/https")
            st.stop()

        with st.spinner("🔍 Analyzing job post..."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                
                jobs = llm.extract_jobs(data)
                
                if not jobs:
                    st.error("❌ No job information found. Please try a different URL.")
                    st.stop()

                st.success("✅ Successfully analyzed job post!")

                for idx, job in enumerate(jobs):
                    with st.expander(f"📌 Job {idx+1} Details", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Position:** {job.get('position', 'N/A')}")
                            st.markdown(f"**Company:** {job.get('company', 'N/A')}")
                            st.markdown(f"**Location:** {job.get('location', 'N/A')}")
                        with col2:
                            st.markdown(f"**Experience Required:** {job.get('experience', 'N/A')}")
                            st.markdown(f"**Key Skills:** {', '.join(job.get('skills', []))}")

                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    
                    with st.status(f"📝 Generating Email for Job {idx+1}...", expanded=True) as status:
                        email = llm.write_mail(job, links)
                        status.update(label="Email Generation Complete!", state="complete", expanded=False)
                    
                    with st.container(border=True):
                        st.markdown("**Generated Email** ✉️")
                        st.markdown(email)
                        
                        # Store email content in session state for reliable access
                        st.session_state[f'email_{idx}'] = email
                        
                        left_col, right_col = st.columns(2)
                        with left_col:
                            st.download_button(
                                label="Download Email 📥",
                                data=email,
                                file_name=f"cold_email_{idx+1}.txt",
                                mime="text/plain",
                                key=f"download_{idx}",
                                use_container_width=True
                            )
                        with right_col:
                            if st.button("Copy to Clipboard 📋", key=f"copy_{idx}", use_container_width=True):
                                if copy_to_clipboard(st.session_state[f'email_{idx}']):
                                    st.success("✅ Email copied to clipboard!")
                    st.divider()

            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")
                st.error("Please check the URL or try again later.")