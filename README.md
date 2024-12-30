# Cover Letter Generator

[![Version](https://img.shields.io/badge/version-1.2.2-blue.svg)](VERSION)

The Cover Letter Generator is an AI-powered web application that helps you create professional, personalized cover letters for job applications. It leverages web scraping technology to extract job posting details automatically and combines them with your professional background to generate tailored cover letters using advanced language models.

**Live Demo:** [Cover Letter Generator](https://coverletter-generation.streamlit.app/)

## ✨ Features

- **Automated Job Data Extraction**: Scrapes job posting details from URLs, including:
  - Job title
  - Company name
  - Location
  - Job description
  - Salary information (when available)
- **Personalized Content Generation**: 
  - Input your professional background
  - Customize with education, experience, skills, and certifications
  - Generate tailored cover letters matching job requirements
- **Flexible Customization**:
  - Upload custom prompt templates
  - Fine-tune the generation process
  - Multiple output options

**Note:** The profile URL scraping feature is available only in local deployments and is not included in the cloud demo for security reasons.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ancastal/Cover-Letter.AI.git
```

2. Navigate to the project directory:
```bash
cd Cover-Letter.AI
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration

1. Set up your OpenAI API key:
   - Create a `.streamlit/secrets.toml` file
   - Add your API key:
     ```toml
     OPENAI_API_KEY = "your-api-key-here"
     ```
   - Or set it as an environment variable:
     ```bash
     export OPENAI_API_KEY="your-api-key-here"
     ```

### Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided local URL

3. Using the application:
   - Enter a job posting URL
   - Click "Scrape Job Posting" to extract details
   - Fill in your professional information
   - (Optional) Upload a custom prompt template
   - Click "Generate Cover Letter"
   - Review and download your personalized cover letter

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please check our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by OpenAI's language models
- Special thanks to all contributors
