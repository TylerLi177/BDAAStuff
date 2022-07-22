from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime

# Access chrome headless mode as to not open anything
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# Configure path for chromedriver to access chrome using Service object
service = Service("C:\\Users\\tydud\\Documents\\BDAA Stuff\\chromedriver_win32\\chromedriver.exe")


def downloadSpeech(year, month, day):

    # Set preferences for how and where to download the speech
    preferences = {
        # Configure download path for PDF
        "download.default_directory": "C:\\Users\\tydud\\Documents\\BDAA Stuff\\House Congressional Speeches\\{year}".format(year=year),
        # Auto download the pdf
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        # Open the pdf externally as to not open it in chrome
        "plugins.always_open_pdf_externally": True
    }
    options.add_experimental_option("prefs", preferences)

    # Go to the url of the website for the speeches
    browser = webdriver.Chrome(options=options, service=service)
    browser.get("https://www.congress.gov/bound-congressional-record/{year}/{month}/{day}/house-section".format
                (year=year, month=month, day=day))

    # Find the link by the partial name; the name has the text "Vol" for every page
    pdfLink = browser.find_element(By.PARTIAL_LINK_TEXT, "Vol")

    # Click the link to the pdf
    pdfLink.click()


# Initialize start and end date for speeches
current_date = datetime.date(1995, 1, 1)
end_date = datetime.date(1995, 12, 31)
delta = datetime.timedelta(days=1)

# Loop through every day from the start date to the end date
while current_date <= end_date:
    # Store the current year, month, and day in variables
    current_year = current_date.strftime("%Y")
    current_month = current_date.strftime("%m")
    current_day = current_date.strftime("%d")

    # Use a try-except block to call the function to download the speech on that day
    try:
        downloadSpeech(year=current_year, month=current_month, day=current_day)
        print(current_date, "speech successfully downloaded", sep=" ")

    # Consider if there is no button
    except NoSuchElementException:
        print(current_date, "has no speech", sep=" ")

    # Go to the next day
    current_date += delta
