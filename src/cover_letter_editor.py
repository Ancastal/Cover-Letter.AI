import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class CoverLetterEditor:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7)
        self.tone_options = {
            "Professional": "Write in a formal and professional tone",
            "Friendly": "Write in a warm and approachable tone",
            "Confident": "Write in a strong and assertive tone",
            "Enthusiastic": "Write in an energetic and passionate tone"
        }
        self.style_options = {
            "Traditional": "Use classic cover letter formatting and language",
            "Modern": "Use contemporary language and a fresh approach",
            "Creative": "Use innovative language while maintaining professionalism",
            "Concise": "Keep it brief and to the point"
        }
        
    def create_editing_interface(self, original_text):
        st.subheader("✏️ Cover Letter Editor")
        st.write("Customize your cover letter to better match your preferences.")
        
        # Create columns for tone and style selection
        col1, col2 = st.columns(2)
        
        with col1:
            selected_tone = st.selectbox(
                "Select Tone",
                options=list(self.tone_options.keys()),
                help="Choose the overall tone of your cover letter"
            )
            
        with col2:
            selected_style = st.selectbox(
                "Select Style",
                options=list(self.style_options.keys()),
                help="Choose the writing style of your cover letter"
            )
            
        # Additional customization options
        emphasis_skills = st.multiselect(
            "Emphasize Skills",
            ["Technical Skills", "Soft Skills", "Leadership", "Project Management", "Communication"],
            help="Select skills you want to emphasize in your cover letter"
        )
        
        length_preference = st.slider(
            "Length Preference",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Very Concise, 5 = Detailed"
        )
        
        if st.button("Regenerate Cover Letter", type="primary"):
            with st.spinner("Customizing your cover letter..."):
                edited_text = self.edit_cover_letter(
                    original_text,
                    selected_tone,
                    selected_style,
                    emphasis_skills,
                    length_preference
                )
                return edited_text
                
        return original_text
        
    def edit_cover_letter(self, original_text, tone, style, emphasis_skills, length_preference):
        prompt_template = """
        Please rewrite the following cover letter:
        {original_text}
        
        Apply these modifications:
        - Tone: {tone_description}
        - Style: {style_description}
        - Emphasize these skills: {emphasis_skills}
        - Length preference: {length_description}
        
        Keep the same basic information and qualifications, but adjust the writing style and emphasis according to the specifications above.
        Ensure the letter remains professional and appropriate for job applications.
        """
        
        length_descriptions = {
            1: "Make it very concise and to the point",
            2: "Keep it relatively brief",
            3: "Maintain a moderate length",
            4: "Include more detail and examples",
            5: "Provide comprehensive detail and examples"
        }
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["original_text", "tone_description", "style_description", "emphasis_skills", "length_description"]
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        response = chain.run({
            "original_text": original_text,
            "tone_description": self.tone_options[tone],
            "style_description": self.style_options[style],
            "emphasis_skills": ", ".join(emphasis_skills),
            "length_description": length_descriptions[length_preference]
        })
        
        return response 