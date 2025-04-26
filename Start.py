import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json

chrome_driver_path = './chromedriver'
driver = webdriver.Chrome()
def reload_page(driver):
    print("Reloading the page...")
    driver.refresh()
    time.sleep(3)

def load_qa_from_json(json_file):
    print("Question/Answer File:- Loading...")
    try:
        with open(json_file, 'r') as file:
            qa_data = json.load(file)
            print("Question/Answer File:- Done")
        return qa_data
    except FileNotFoundError:
        print("Question/Answer File:- Error*********")
        return {}


def click_button_by_text(text):
    try:
        button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, f'//button[contains(@class, "artdeco-button--primary") and .//span[text()="{text}"]]')))
        print(f"Clicked {text} button.")
        button.click()
        return True
    except Exception as exception:
        print(f"Could not find {text} button")
        return False

def click_Remove_Application(text):
    try:
        dismiss_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, text))
        )
        # dismiss_button.click()
        # print(f"Clicked Dismiss button for Job ID: {text}")

        aria_label = dismiss_button.get_attribute("aria-label")

        # Click only if it's the first type of button (not already dismissed)
        if "Dismiss" in aria_label:
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.ID, text))
            ).click()
            print(f"Clicked Dismiss button for Job ID: {text}")
        else:
            print(f"Skipping already dismissed job: {text}")
    except Exception as e:
        print("No dismiss button found or error occurred: click_Remove_Application ")

def handle_error_and_fill_zero():
    try:
        # Find the error message element
        error_element = WebDriverWait(driver, 2).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'artdeco-inline-feedback__message')))
        print("error red Text:", error_element.text.strip())
        return False
    except:
        print('Not found Red error messgae ***')
        return True
    
def Application_start_to_Add_question():
    try:
        if handle_error_and_fill_zero():
            print("Process with next page")
        else:
            print('Enter In question/answer page')
            
            if not handle_error_and_fill_zero():
                print("Handling Input Text Question Type...")
                Question_type_input_text()
            if not handle_error_and_fill_zero():
                print("Handling Radio Button Question Type...")
                Question_type_Redio()
            
            if not handle_error_and_fill_zero():
                print("Handling Dropdown Question Type...")
                Question_type_DropDown_List()
            
            if not handle_error_and_fill_zero():
                print("Handling Checkbox Question Type...")
                Question_type_Check_Box()
            
            if not handle_error_and_fill_zero():
                print("Handling Date Select Question Type...")
                Question_type_Date_Select()
            
            if not handle_error_and_fill_zero():
                print("Handling Date Select Question Type...")
                Question_type_textarea_text()
                 
    
    except:
        print('something wrong with question/answer page/view ***')



def Question_type_textarea_text():
    try:
        print('Entering data in textarea fields...')

        # Locate all textarea elements
        textarea_fields = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.XPATH, "//textarea"))
        )

        for textarea in textarea_fields:
            try:
                # Extract the label associated with the textarea
                question_label = textarea.find_element(By.XPATH, "./preceding-sibling::label")
                question_text = question_label.text.strip()
                # print(f"Detected textarea field: {question_text}")

                # Load stored application data
                with open('./config.json', 'r') as file:
                    data = json.load(file)

                if question_text in data["application_data"]:
                    # Clear the existing content and input the stored value
                    textarea.clear()
                    textarea.send_keys(data["application_data"][question_text])
                    # print(f"Filled '{question_text}' with: {data['application_data'][question_text]}")

                else:
                    # If the question is not in JSON, add it with a placeholder value
                    data["application_data"][question_text] = "https://www.linkedin.com/in/zarana-vadaliya-062229180/"
                    
                    with open('./config.json', 'w') as file:
                        json.dump(data, file, indent=2)

                    # print(f"Added '{question_text}' to config.json for future use.")

            except Exception as e:
                print(f"Error processing textarea: {e}")

    except Exception as e:
        print(f"General error: {e}")

def Question_type_Redio():
    try:
        fieldset_containers = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH, "//fieldset[@data-test-form-builder-radio-button-form-component='true']")))
        for fieldset_container in fieldset_containers:
            required_span = fieldset_container.find_element(By.XPATH, ".//span[contains(@class, 'fb-dash-form-element__label-title--is-required')]")
            required_text = required_span.text.strip()
            required_text = required_text.split('\n')[0]
            # Split and take the first part
            options = fieldset_container.find_elements(By.XPATH, ".//div[@data-test-text-selectable-option]//label[@data-test-text-selectable-option__label]")
            option_texts = [option.text.strip() for option in options]
            print(f"{required_text}: {option_texts}")
            # print(fieldset_container.get_attribute("outerHTML"))
            # Check if question and answer are already in JSON file
            with open('./config.json', 'r') as file:
                data = json.load(file)
                if required_text in data["application_data"]:
                    # If question is in JSON, select the corresponding option
                    selected_option_text = data["application_data"][required_text][0]
                    if selected_option_text in option_texts:
                        selected_option_index = option_texts.index(selected_option_text)
                        options[selected_option_index].click()
                    else:
                        print(f"Option '{selected_option_text}' not found in the current form. Performing default action.")
                else:
                    # If question is not in JSON, add it along with the first option
                    data["application_data"][required_text] = option_texts
                    # Write the updated JSON data back to the file
                    with open('./config.json', 'w') as file:
                        json.dump(data, file, indent=2)
    except:
        print("look faild there are something else")



def Question_type_Date_Select():
    try:
        print('Enter In question type Date Select')

        # Wait for the <fieldset> element to be available
        fieldset_container = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'fb-date-range__date-select'))
        )
        print(f"Found fieldset: {fieldset_container.get_attribute('class')}")

        # Extract the label for 'From' or any other required field
        legend = fieldset_container.find_element(By.TAG_NAME, 'legend')
        label_text = legend.text.strip()
        print(f"Label found: {label_text}")

        # Load existing data from the JSON file
        with open('./config.json', 'r') as file:
            data = json.load(file)

        # If the label (e.g., 'Dates of employment') does not exist in the JSON file, add it
        if label_text not in data["application_data"]:
            # Create a new entry with the current date and 3 years ago for the date range
            current_date = datetime.now()
            three_years_ago = current_date - timedelta(days=365*1)
            from_date = three_years_ago.strftime("%Y-%m-%d")
            to_date = current_date.strftime("%Y-%m-%d")
            
            # Add to the JSON structure
            data["application_data"][label_text] = [from_date, to_date]
            with open('./config.json', 'w') as file:
                json.dump(data, file, indent=2)                    
        else:
            print(f"Label '{label_text}' already exists in the JSON data.")

        # Now let's handle the <select> elements within the fieldset container
        select_elements = fieldset_container.find_elements(By.TAG_NAME, 'select')
        for select_element in select_elements:
            options = select_element.find_elements(By.TAG_NAME, 'option')
            option_texts = [option.text.strip() for option in options]

            # Example: Select the "Year" option (could be adapted for Month or others)
            if 'Year' in option_texts:
                select_element.send_keys('2025')  # Example selection, adjust as needed
                print(f"Selected Year: 2025")
            else:
                print("No 'Year' option found in the dropdown.")

    except NoSuchElementException as e:
        print(f"Error: Element not found - {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def Question_type_Check_Box():
    try:
        print('Enter In question type Check Box')
        
        # Wait for fieldset elements to be present
        fieldsets = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.XPATH, "//fieldset[contains(@id, 'checkbox-form-component-formElement')]"))
        )

        # Iterate over the fieldset elements
        for fieldset in fieldsets:
            # Locate the checkbox label inside the fieldset
            checkbox_label = fieldset.find_element(By.XPATH, ".//label").text.strip()

            # Load the data from the JSON file
            with open('./config.json', 'r') as file:
                data = json.load(file)

            # Check if the checkbox label is in the application data in the JSON
            if checkbox_label in data["application_data"]:
                input_checkbox = fieldset.find_element(By.XPATH, ".//input[@type='checkbox']")
                label = fieldset.find_element(By.XPATH, ".//label")  # Locate the label associated with the checkbox
                
                # Get the desired checkbox state from the JSON (True or False)
                checkbox_state = data["application_data"][checkbox_label]
                
                print(f"Current checkbox state: {checkbox_state}")
                
                # If the checkbox needs to be checked and is not already checked, click the label
                if checkbox_state:  # True means it should be checked
                    if not input_checkbox.is_selected():
                        label.click()  # Click the label to toggle the checkbox
                        print(f"Checked the checkbox for: {checkbox_label}")
                    else:
                        print(f"Checkbox for {checkbox_label} is already checked.")
                
                # If the checkbox needs to be unchecked and is checked, click the label
                elif not checkbox_state:  # False means it should be unchecked
                    if input_checkbox.is_selected():
                        label.click()  # Click the label to toggle the checkbox
                        print(f"Unchecked the checkbox for: {checkbox_label}")
                    else:
                        print(f"Checkbox for {checkbox_label} is already unchecked.")
            
            # If the checkbox label is not in the JSON file, assume it should be checked (default to True)
            else:
                checkbox_state = True  # Default to True (checked)
                data["application_data"][checkbox_label] = checkbox_state
                with open('./config.json', 'w') as file:
                    json.dump(data, file, indent=2)
                # Click the label to check the box
                label = fieldset.find_element(By.XPATH, ".//label")
                if not input_checkbox.is_selected():
                    label.click()  # Click the label to toggle the checkbox
                    print(f"Checked the checkbox for: {checkbox_label}")

    except Exception as e:
        print(f"Error in Question_type_Check_Box: {str(e)}")



def Question_type_DropDown_List ():
    try:
        print('Enter In question tyep DropDown List')
        fieldset_containers = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH, "//select")))
        
        for fieldset_container in fieldset_containers:            
            required_span = fieldset_container.find_element(By.XPATH, "preceding-sibling::label")
            # DropDown question find here 
            required_text = required_span.text.strip()
            required_text = required_text.split('\n')[0]
            # Split and take the first part
            options = fieldset_container.find_elements(By.TAG_NAME, 'option')
            option_texts = [option.text.strip() for option in options]
            # print(f"{required_text}: {option_texts}")
            # print(fieldset_container.get_attribute("outerHTML"))

            # Load the file 
            with open('./config.json', 'r') as file:
                data = json.load(file)

            # Check the question in json data
            if required_text in data["application_data"]:
                selected_option_text = data["application_data"][required_text][0]
                if selected_option_text in option_texts:
                    selected_option_index = option_texts.index(selected_option_text)
                    options[selected_option_index].click()
                    print(options[selected_option_index].click())
                    print(f"Selected Option: {selected_option_text}")
                else:
                    print(f"Option '{selected_option_text}' not found in the current form. Performing default action.")
            
            else:
                # If question is not in JSON, add it add the question and all option
                data["application_data"][required_text] = option_texts[1:]
                # Write the updated JSON data back to the file
                with open('./config.json', 'w') as file:
                    json.dump(data, file, indent=2)
                    
            print("Option selected successfully.")     
    except:
        print('something wrong with  question tyep DropDown_List ***')


def Question_type_input_text():
    try:
        print('Enter In question type input text ')
        # Mupltiple type of text input add here 
        text_input_containers = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='artdeco-text-input--container ember-view']"
                                                 " | "
                                                 "//div[@id='ember1124' and contains(@class, 'artdeco-text-input')]")))
        for field_container in text_input_containers:
            question_label = field_container.find_element(By.XPATH, ".//label[@class='artdeco-text-input--label']")
            question_text = question_label.text.strip()
            print(question_text)
            
            with open('./config.json', 'r') as file:
                data = json.load(file)
                
            if question_text in data["application_data"]:
                # If question is in JSON, input the stored value
                input_element = field_container.find_element(By.XPATH, ".//input[@type='text']")
                input_element.clear()
                input_element.send_keys(data["application_data"][question_text])
                print(f"Input Value for {question_text}: {data['application_data'][question_text]}")
            
            else:
                # If question is not in JSON, add it with null value
                data["application_data"][question_text] = 1
                # Write the updated JSON data back to the file
                with open('./config.json', 'w') as file:
                    json.dump(data, file, indent=2)
        
        time.sleep(1)

    except:
        print('something wrong with lable/input text ***')





def Apply_start(al_data, json_file):
    print("start application easy apply")
    try:
        job_listings = driver.find_elements(By.CLASS_NAME, 'job-card-container')

        for job_listing in job_listings:
            job_listing.click()

            # Find the dismiss button inside this job listing
            dismiss_button = job_listing.find_element(By.XPATH, './/button[contains(@class, "job-card-container__action")]')
            dismiss_button_id = dismiss_button.get_attribute("id")
            print(f"Found Dismiss Button ID: {dismiss_button_id}")

            # Add a delay to give the page time to load (you might need to adjust the time)
            time.sleep(1)
            # Locate and click the "Easy Apply" button if available
            if click_button_by_text("Easy Apply") or click_button_by_text("Continue"):
                print("Clicked Easy Apply or Continue.")
                while True:
                    Application_start_to_Add_question()
                    if click_button_by_text("Review") or click_button_by_text("Next"):
                        Application_start_to_Add_question()
                    else:
                        if click_button_by_text("Submit application"):
                            click_button_by_text("Dismiss") 
                            button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//button[contains(@class, "ember-view artdeco-modal__dismiss")]')))
                            button.click()
                            time.sleep(1)
                            click_Remove_Application(dismiss_button_id)
                            time.sleep(1)
                            break

            # break  # exit the loop after submitting the application
            else:
                click_Remove_Application(dismiss_button_id)
                time.sleep(1)
                print("Could not find Easy Apply or Continue *** ")
                
    except Exception as e:
        print(f"Error during job application *** ")


def Search_for_job(al_data, json_file):
    print("Searching Job Loding....")
    try:
        # Now, let's search for jobs:-https://www.linkedin.com/jobs/search?keywords=salesforce%20developer&f_AL=true
        driver.get(f"https://www.linkedin.com/jobs/search?keywords={al_data.get('job')}&f_AL=true")
        time.sleep(3)
        page = 2
        while True:
            Apply_start(al_data, json_file)
            button_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//button[@aria-label='Page {page}']")))
            button_element.click()
            time.sleep(5)
            page = page + 1    
    except Exception as e:
        print(f"Error during job search ***")


def Login_Linkedin(job_url, json_file):
    print("Start Login....")
    # load json file
    try:
        qa_data = load_qa_from_json(json_file)
        print(qa_data)
        time.sleep(2)
        # login process start
        try:
            print("Login Process Start....")
            # Open the LinkedIn login page
            driver.get(job_url)
            time.sleep(3)

            # Find and fill in the email/phone input field
            email_input = driver.find_element("id", "username")
            email_input.send_keys(qa_data.get('email'))
            # Find and fill in the password input field
            password_input = driver.find_element('id', "password")
            password_input.send_keys(qa_data.get('password'))
            login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]")
            login_button.click()
            print("Login Successful!!")
            time.sleep(10)
            Search_for_job(qa_data, json_file)

        except Exception as e:
            print(f"Error during login ***")

    except Exception as e:
        print(f"Loding the file error *** ")


job_url = "https://www.linkedin.com/login"
json_file = "./config.json"
Login_Linkedin(job_url, json_file)