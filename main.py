import time
import random
import streamlit as st
from urllib.parse import quote
from bs4 import BeautifulSoup
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException



def login_to_google(driver, google_email, google_password):
    driver.get(f"https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%"
               f"3Dgoogle%2Blog%2Bin%26rlz%3D1C1YTUH_esES1017ES1017%26oq%3Dgoogle%2Blog%2Bin%26gs_lcrp%3DEgZjaHJvbWUq"
               f"BwgAEAAYgAQyBwgAEAAYgAQyCggBEAAYChgWGB4yCggCEAAYChgWGB4yCAgDEAAYFhgeMgoIBBAAGAoYFhgeMgYIBRBFGDwyBggG"
               f"EEUYPDIGCAcQRRg8qAIAsAIA%26pf%3Dcs%26sourceid%3Dchrome%26ie%3DUTF-8&ec=GAZAAQ&hl=es&ifkv=AaSxoQwOjsz"
               f"xpZm6eeB6YF0NGbHPyxvRVHc1FqhouQkJ4OF89UbmtVPElNPe1bXPOzOD3mmCcRq-Fw&passive=true&flowName=GlifWebSig"
               f"nIn&flowEntry=ServiceLogin&dsh=S486938468%3A1715265339421294&theme=mn&ddm=0")
    driver.maximize_window()

    time.sleep(random.uniform(1, 2))
    google_email_input = driver.find_element(By.ID, "identifierId")
    google_email_input.send_keys(google_email)
    time.sleep(random.uniform(1, 2))

    next_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button/span")
    next_button.click()

    time.sleep(random.uniform(2, 3))
    google_password_input = driver.find_element(By.CLASS_NAME, "whsOnd")
    time.sleep(random.uniform(1, 2))
    google_password_input.send_keys(google_password)

    next_button2 = driver.find_element(By.ID, "passwordNext")
    next_button2.click()
    time.sleep(random.uniform(1, 3))


def login_to_linkedin(driver, linkedin_email, linkedin_password):
    driver.get("https://www.linkedin.com/login")
    linkedin_email_input = driver.find_element(By.ID, "username")
    linkedin_password_input = driver.find_element(By.ID, "password")

    linkedin_email_input.send_keys(linkedin_email)
    linkedin_password_input.send_keys(linkedin_password)
    time.sleep(random.uniform(1, 2))

    next_button3 = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div[1]/form/div[3]/button")
    next_button3.click()
    time.sleep(random.uniform(15, 20))
# def browse_through_pages():


def extract_job_ids(driver, keywords_clean, kms_radius_clean, experience_clean, work_options_clean, location_clean):
    results = -25
    full_job_list = []
    while find_no_results_banner(driver):
        results += 25
        print("results is:", results)

        try:
            driver.get(f"https://www.linkedin.com/jobs/search/?"
                       f"f_AL=true&f_E={experience_clean}&f_WT={work_options_clean}"
                       f"&keywords={keywords_clean}&location={location_clean}"
                       f"&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R&start={results}")
            print("link is:", f"https://www.linkedin.com/jobs/search/?"
                              f"f_AL=true&f_E={experience_clean}&f_WT={work_options_clean}"
                              f"&keywords={keywords_clean}&location={location_clean}"
                              f"&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R&start={results}")
            html_text = driver.page_source
            soup = BeautifulSoup(html_text, 'html.parser')
            li_elements = soup.find_all("li", class_='jobs-search-results__list-item')
            job_ids = [li['data-occludable-job-id'] for li in li_elements]
            full_job_list.extend(job_ids)
            print("list is:", full_job_list)

        except NoSuchElementException:
            print("Something went wrong")

    print("No more results found.")
    return full_job_list


def find_no_results_banner(driver):
    elements = driver.find_elements(By.CLASS_NAME, 'jobs-search-no-results-banner')
    return len(elements) == 0


def find_button(driver, aria_label):
    try:
        html_text = driver.page_source
        soup = BeautifulSoup(html_text, 'html.parser')
        button = soup.find('button', {'aria-label': aria_label})
        if not button:
            return None

        button_id = button.attrs['id']
        button = driver.find_element(By.ID, button_id)
        print(button)
        return button

    except NoSuchElementException:
        return None


def click_available_button(driver, *buttons):
    for button in buttons:
        if button is not None:
            try:
                button.click()
                return True
            except Exception as e:
                print(f"An error occurred while clicking the button: {e}")

    return False


def main():
    st.title("LinkedIn Job Search")

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        col1.subheader("Login Information")
        google_email = st.text_input("Gmail Address:")
        google_password = st.text_input("Password:", type="password")
        st.info("""
                    **Note**: Using Google login is **not mandatory** for using this app. 
                    However, it is **recommend** to reduce the 
                    likelihood of LinkedIn detecting your device as a bot.
                """)

    with col2:
        col2.subheader("Sign Up to LinkedIn")
        linkedin_email = st.text_input("Linkedin email:")
        linkedin_password = st.text_input("Linkedin password:", type="password")

    with col3:
        col3.subheader("Job Search Information")
        keywords = st.text_input("Keywords", placeholder="Ex: Data Analyst")
        location = st.text_input("Location")
        experience_levels = st.multiselect("Experience Levels", ["Internship", "Entry level", "Associate",
                                                                 "Mid-senior level", "Director", "Executive"])
        work_options = st.multiselect("Work Options", ["Hybrid", "On-site", "Remote"])
        kms_radius = st.slider("Radius in kms", 0, 100, 50)

    if st.button("Apply"):
        st.title("LinkedIn Login Page")
        # preparing and cleaning input data

        # Location
        location_clean = ''.join(char for char in location if char.isalpha() or char.isspace())
        location_clean = location_clean.split()[0] if location_clean else ""

        # Keywords
        keywords_clean = quote(keywords)

        # Experience
        experience_map = {
            "Internship": "%2C1",
            "Entry level": "%2C2",
            "Associate": "%2C3",
            "Mid-senior level": "%2C4",
            "Director": "%2C5",
            "Executive": "%2C6"
        }

        experience_clean = "".join(experience_map.get(exp, "") for exp in experience_levels)

        work_options_map = {
            "On-site": "%2C1",
            "Remote": "%2C2",
            "Hybrid": "%2C3"
        }

        work_options_clean = "".join(work_options_map.get(work, "") for work in work_options)

        # Distance in Kms
        kms_radius_clean = str(kms_radius)

        # Chrome Driver
        driver = Driver(uc=True)

        login_to_google(driver, google_email, google_password)
        login_to_linkedin(driver, linkedin_email, linkedin_password)
        job_ids = extract_job_ids(driver, keywords_clean, kms_radius_clean, experience_clean, work_options_clean, location_clean)
        csv_file_path = 'job_ids.csv'
        print('check 1')
        print('check2')

        for job_id in job_ids:
            driver.get("https://www.linkedin.com/jobs/view/" + job_id)
            time.sleep(random.uniform(1, 2))
            print("ID FOR JOB IS:", job_id)

            html_text = driver.get_page_source()
            soup = BeautifulSoup(html_text, 'html.parser')

            # Search for Easy Apply button
            try:
                # Find the Easy Apply button element
                top_card_div = soup.find('div', class_='jobs-apply-button--top-card')
                if top_card_div:
                    button_element = top_card_div.find('button')
                    if button_element:
                        button_id = button_element.attrs['id']
                        easy_apply_button = driver.find_element(By.ID, button_id)
                        easy_apply_button.click()
                        print("Easy Apply found")

                        max_attempts = 6
                        for attempt in range(max_attempts):

                            time.sleep(7)
                            next_button, review_button, submit_button = (
                                find_button(driver, 'Continue to next step'),
                                find_button(driver, 'Review your application'),
                                find_button(driver, 'Submit application'))

                            if submit_button is not None:
                                print("Application successfully submitted")
                                click_available_button(driver, submit_button)
                                break

                            click_available_button(driver, next_button, review_button, submit_button)

                    else:
                        raise Exception("No Easy Apply button found")
                else:
                    raise Exception("No top division container found")
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
