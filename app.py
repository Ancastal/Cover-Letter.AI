"""An application to generate cover letters based on user information and job postings."""
import streamlit as st
from src.cover_letter import scrape_job_posting, query, user_persona
import subprocess
import sys
import os
import time
import re

try:
    from linkedin_api import Linkedin
except ModuleNotFoundError as e:
    subprocess.Popen([f'{sys.executable} -m pip install git+https://github.com/tomquirk/linkedin-api.git'], shell=True)
    time.sleep(90)

# Page configuration
st.set_page_config(
    page_title='Cover Letter Generator',
    page_icon=':page_with_curl:',
    layout='centered',
    initial_sidebar_state='expanded'
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-top: 20px;
        border-radius: 8px;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .cover-letter-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 2rem 0;
        font-family: 'Times New Roman', serif;
        line-height: 1.6;
    }
    .success-message {
        padding: 1rem;
        border-radius: 8px;
        background-color: #d4edda;
        color: #155724;
        margin-bottom: 1rem;
        text-align: center;
    }
    .download-button {
        text-align: center;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def validate_linkedin_url(url, type="job"):
    """Validate LinkedIn URL format."""
    if not url:
        return False
    
    if type == "job":
        pattern = r'https?://(www\.)?linkedin\.com/jobs/view/\d+'
    else:  # profile
        pattern = r'https?://(www\.)?linkedin\.com/in/[\w\-]+'

    
    return bool(re.match(pattern, url))

def scrape_profile(profile_id):
    """Scrape LinkedIn profile with proper error handling."""
    try:
        # First try secrets
        email = st.secrets['LINKEDIN_EMAIL']
        pwd = st.secrets['LINKEDIN_PASSWORD']
    except Exception:
        # Fallback to environment variables
        email = os.getenv('LINKEDIN_EMAIL')
        pwd = os.getenv('LINKEDIN_PASSWORD')
        if not email or not pwd:
            raise ValueError("LinkedIn credentials not found in secrets or environment variables")

    try:
        api = Linkedin(email, pwd)
        profile = api.get_profile(profile_id)
        name = f"{profile['firstName']} {profile['lastName']}"
        education = [
            f"{edu['schoolName']} ({edu['timePeriod']['startDate']['year']}) - {edu.get('description', 'No description available')}"
            for edu in profile.get('education', [])
        ]
        experience = [
            f"{exp['title']} at {exp['companyName']} - {exp.get('description', 'No description available')}"
            for exp in profile.get('experience', [])
        ]
        certifications = [
            f"{cert['name']} from {cert['authority']}"
            for cert in profile.get('certifications', [])
        ]
        skills = [skill['name'] for skill in api.get_profile_skills(profile_id)]
        
        return user_persona.UserPersona(name, education, experience, skills, certifications)
    except Exception as e:
        raise Exception(f"Failed to scrape LinkedIn profile: {str(e)}")

def main():
    # Sidebar for app information
    with st.sidebar:
        st.title("ℹ️ About")
        st.markdown("""
        This app helps you generate professional cover letters using:
        - Your LinkedIn profile or manual input
        - Job posting details
        - AI-powered content generation
        
        **Note:** For privacy and security, use the local version for automatic profile scraping.
        """)
        
        st.markdown("---")
        st.caption("Made with ❤️ using Streamlit")

    # Main content
    st.title('Cover Letter Generator :page_with_curl:')
    st.write('Generate personalized cover letters based on your profile and job postings.')

    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["🔗 LinkedIn Integration", "✍️ Manual Input"])

    with tab1:
        st.info("Currently, only LinkedIn job postings are supported (e.g., https://www.linkedin.com/jobs/view/3544765357/)")
        
        # Job Posting URL input with validation
        job_url = st.text_input('Job Posting URL', key='job_url', placeholder='https://www.linkedin.com/jobs/view/3544765357/')
        if job_url and not validate_linkedin_url(job_url, "job"):
            st.error("Please enter a valid LinkedIn job posting URL")
        
        # Profile URL input with validation
        profile_url = st.text_input('Your LinkedIn Profile URL', key='profile_url', placeholder='https://www.linkedin.com/in/johndoe/')
        if profile_url and not validate_linkedin_url(profile_url, "profile"):
            st.error("Please enter a valid LinkedIn profile URL")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input('Full Name', placeholder='John Doe')
            education_level = st.selectbox('Education Level', 
                ['High School', 'Associate Degree', 'Bachelor\'s Degree', 'Master\'s Degree', 'PhD'])
        
        with col2:
            fields = [
                'Computer Science', 'Engineering', 'Business', 'Finance', 'Marketing',
                'Data Science', 'Healthcare', 'Education', 'Other'
            ]
            education_field = st.selectbox('Field of Study', fields)
            
        experience = st.text_area('Work Experience', 
            placeholder="Describe your relevant work experience...",
            help="Include your job titles, companies, and key achievements")
            
        skills = st.multiselect('Skills',
            ['Python', 'SQL', 'Java', 'JavaScript', 'C#', 'C++', 'PHP', 'Swift', 'Rust',
             'Data Analysis', 'Project Management', 'Communication', 'Leadership'],
            help="Select all relevant skills")
            
        certifications = st.multiselect('Certifications',
            ['AWS', 'Google Cloud', 'Azure', 'Cisco', 'CompTIA', 'PMP', 'CISSP'],
            help="Select any relevant certifications")

    # Generate button
    if st.button('Generate Cover Letter', type='primary'):
        with st.spinner("Generating your cover letter..."):
            try:
                # Get user data based on selected tab
                if tab1.active:  # LinkedIn Integration tab
                    if not job_url:
                        st.error("Please enter a job posting URL")
                        return
                    if not profile_url:
                        st.error("Please enter your LinkedIn profile URL")
                        return
                    profile_id = profile_url.rstrip('/').split('/')[-1]
                    user = scrape_profile(profile_id)
                else:  # Manual Input tab
                    if not name or not experience:
                        st.error("Please fill in all required fields")
                        return
                    education = f"{education_level} in {education_field}"
                    user = user_persona.UserPersona(name, education, experience, skills, certifications)

                # Generate cover letter
                job_posting = scrape_job_posting(job_url)
                response = query(user, job_posting, 'src/prompts/cover_letter.txt')

                # Display result in a nice format
                st.markdown('<div class="success-message">✨ Cover letter generated successfully!</div>', unsafe_allow_html=True)
                st.markdown("""<div class="cover-letter-container">
                            <p>{}</p>
                            </div>""".format(response['text']), unsafe_allow_html=True)
                
                # Add download button with centered styling
                st.markdown('<div class="download-button">', unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Cover Letter",
                    data=response['text'],
                    file_name="cover_letter.txt",
                    mime="text/plain"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                if "credentials not found" in str(e):
                    st.info("Please use the manual input method or run the app locally for LinkedIn integration.")

if __name__ == '__main__':
    main()
