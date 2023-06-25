
# Cover Letter Generator

The Cover Letter Generator is a web application that helps you generate cover letters for job applications. It uses web scraping to extract job posting details from a provided URL and combines them with user inputs to generate personalized cover letters using language models.

**Note:**
The application has an additional feature to scrape the user profile URL and gather user information automatically. However, this feature is only available when running the application locally and is not available in the Cloud implementation provided as a demo.

## Features

- Scrape job posting details from a URL, including job title, company name, location, job description, and salary information.
- Collect user inputs for name, education, experience, skills, and certifications.
- Generate cover letters based on the scraped job posting details and user inputs.
- Utilizes language models and conversation chains to provide personalized responses.

## Installation

1. Clone the repository:

```shell
git clone https://github.com/your-username/job-application-generator.git
```

2. Change into the project directory:

```shell
cd job-application-generator
```

3. Install the required dependencies:

```shell
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:

```shell
streamlit run app.py
```

2. Access the application in your web browser by opening the provided local URL.

3. Enter the URL of the job posting and click "Scrape Job Posting" to retrieve the job details.

4. Fill in the user persona fields with your information, including name, education, experience, skills, and certifications.

5. Optionally, upload a prompt template file for generating personalized cover letters.

6. Click "Generate Cover Letter" to generate a cover letter based on the scraped job posting details and user inputs.

7. The generated cover letter will be displayed on the web page.

## Configuration

- Make sure to set the `OPENAI_API_KEY` environment variable with your OpenAI API key.
```
export OPENAI_API_KEY="YOUR_API_KEY"
```

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
```

Feel free to copy and use this formatted output for your README.md file.
