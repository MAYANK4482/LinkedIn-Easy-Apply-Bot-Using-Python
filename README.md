**LinkedIn Easy Apply Automation 🚀**

**A Python-based Selenium bot to automate LinkedIn Easy Apply job applications.**

**Features**
Auto-login to LinkedIn.
Search and apply to jobs using Easy Apply.
Automatically fill out job applications based on pre-filled answers.
Handles different question types: text fields, radio buttons, dropdowns, checkboxes, dates, and textareas.
Updates missing questions automatically in your local config.json.

**Setup Instructions**

1. Clone this repository
git clone https://github.com/MAYANK4482/LinkedIn-Easy-Apply-Bot-Using-Python.git
cd YOUR_REPO_NAME

2. Install required Python packages

pip install selenium
You must have Python 3.x installed.
If not, download from python.org.

3. Download ChromeDriver
Download ChromeDriver from ChromeDriver Official Site that matches your Chrome version.

Place the chromedriver executable in your project folder (or adjust Start.py path).

**Configuration**
You need a config.json file  with your LinkedIn credentials and application data.

**Example config.json format:**

{
  "email": "your-email@example.com",
  "password": "your-password",
  "job": "Software Engineer",
  "job2": "Developer",
  "application_data": {
    "Phone number": "1234567890",
    "Address": "New York",
    "Do you have a valid driver's license?": ["Yes"],
    "Salary Expectation": "70000",
    ...
  }
}

**How to Run**

python Start.py

The script will:
  Open LinkedIn.
  Log you in.
  Start applying to available jobs automatically!

**Project Structure**

project/
├── Start.py            # Main automation script
├── config.json         # Application data (excluded in GitHub)
├── chromedriver        # Chrome driver executable
└── README.md           # This documentation

**Notes**
This script works best with Easy Apply jobs only.
Make sure LinkedIn's layout hasn't changed, otherwise small updates might be needed.
Use this bot responsibly and respect LinkedIn’s policies.

**License
This project is for educational purposes only. 📚
The author is not responsible for any misuse.**
