# LinkedIn Job Application Automator

This project is a Streamlit-based application that automates the job application process on LinkedIn using the "Easy Apply" feature. It uses SeleniumBase for web automation, BeautifulSoup for parsing HTML, and Streamlit for the user interface.

## Features

- **Login to LinkedIn**: Automatically log in to LinkedIn using your credentials.
- **Google Login**: Option to log in to Google to reduce the likelihood of being detected as a bot by LinkedIn.
- **Job Search**: Search for jobs based on keywords, location, experience level, work options, and radius.
- **Automated Application**: Automatically apply to jobs using the "Easy Apply" button on LinkedIn.

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/linkedin-job-automator.git
    cd linkedin-job-automator
    ```

2. **Create a virtual environment** (optional but recommended):

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. **Install the required packages**:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Streamlit application**:

    ```sh
    streamlit run main.py
    ```

2. **Open your web browser** and navigate to `http://localhost:8501` to access the application.

3. **Fill in the necessary information** in the Streamlit interface:
   - Gmail Address and Password (optional but recommended for reducing bot detection).
   - LinkedIn email and password.
   - Job search criteria: keywords, location, experience levels, work options, and radius.

4. **Click the "Apply" button** to start the automated job application process.

## Project Structure

- `main.py`: The main script containing the Streamlit app and the automation logic.
- `requirements.txt`: List of required Python packages.

## Functions Overview

### `login_to_google(driver, google_email, google_password)`

Logs in to Google to reduce the likelihood of LinkedIn detecting your device as a bot.

### `login_to_linkedin(driver, linkedin_email, linkedin_password)`

Logs in to LinkedIn using the provided credentials.

### `extract_job_ids(driver, keywords_c
