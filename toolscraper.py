from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

options = Options()
options.headless = True
options.add_argument("--window-size=1920, 1200")
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
driver.get('https://messari.io/governor/tools')


def tool_types():
    # Get the url
    url = 'https://messari.io/governor/tools?types='
    types_urls = ['Community', 'Discovery+%26+Analytics', 'Financial', 'Governance+%26+Voting',
                  'HR', 'Infrastructure', 'Operating+Systems', 'Productivity+%26+Collaboration', 'Services']

    result = []
    for t in types_urls:

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920, 1200")
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

        driver.get(url+t)

        filter_list = []

        # Keep scrolling
        SCROLL_PAUSE_TIME = 10
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            # Scroll to bottom
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        try:
            # Gets the text of the DAO names
            names = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "h4")))

            for n in names:
                if n.text:
                    filter_list.append(n.text)

        finally:
            driver.quit()

        result.append(filter_list)

    tool_types = {'Community': result[0], 'Discovery & Analytics': result[1], 'Financial': result[2], 'Governance & Voting': result[3],
                  'HR': result[4], 'Infrastructure': result[5], 'Operating Systems': result[6], 'Productivity & Collaboration': result[7], 'Services': result[8]}

    return tool_types


def tool_tags():

    # Get the url
    url = 'https://messari.io/governor/tools?tags='
    tags_urls = ["Access+Control", "Asset+Management", "Bounty+Board", "Compensation", "Contribution", "Data", "Data+Analytics", "Data+Science", "Design",
                 "Developer+Tooling", "Discussion+%2F+Communication", "Dispute+Resolution", "Education", "Financing", "Forum", "Fundraise", "Governance+Aggregator", "Governance+Framework",
                 "Identity+%26+Reputation", "Incubator+%2F+Accelerator", "Job+Board", "Knowledge+Management", "Legal", "Liquidity+Management", "Marketing", "Moderation", "Multisig", "Newsletter",
                 "Onboarding", "Project+Management", "Protocol+%2F+Governance+Advisory", "Publishing", "Reporting", "Security", "Social+Graphs", "Software+Development", "Taxes", "Treasury+Management",
                 "Voting+Power+Markets+%2F+Metagovernance", "Wiki", "Yield+Management"]

    result = []
    for t in tags_urls:

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920, 1200")
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

        driver.get(url+t)

        filter_list = []

        # Wait for page to load for 10 secs
        SCROLL_PAUSE_TIME = 10

        # Original height of page
        last_height = driver.execute_script(
            "return document.body.scrollHeight")

        # Keep scrolling
        while True:

            # Scroll to bottom
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        try:
            # Gets the text of the DAO names
            names = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "h4")))

            for n in names:
                if n.text:
                    filter_list.append(n.text)

        finally:
            driver.quit()

        result.append(filter_list)

    tool_tags = {"Access Control": result[0], "Asset Management": result[1], "Bounty Board": result[2], "Compensation": result[3], "Contribution": result[4], "Data": result[5], "Data Analytics": result[6],
                 "Data Science": result[7], "Design": result[8], "Developer Tooling": result[9], "Discussion / Communication": result[10], "Dispute Resolution": result[11], "Education": result[12],
                 "Financing": result[13], "Forum": result[14], "Fundraise": result[15], "Governance Aggregator": result[16], "Governance Framework": result[17], "Identity & Reputation": result[18],
                 "Incubator / Accelerator": result[19], "Job Board": result[20], "Knowledge Management": result[21], "Legal": result[22], "Liquidity Management": result[23], "Marketing": result[24],
                 "Moderation": result[25], "Multisig": result[26], "Newsletter": result[27], "Onboarding": result[28], "Project Management": result[29], "Protocol / Governance Advisory": result[30],
                 "Publishing": result[31], "Reporting": result[32], "Security": result[33], "Social Graphs": result[34], "Software Development": result[35], "Taxes": result[36], "Treasury Management": result[37],
                 "Voting Power Markets / Metagovernance": result[38], "Wiki": result[39], "Yield Management": result[40]}

    return tool_tags


def tool_about(name):

    ind_about_list = []
    ind_u_list = []

    driver.find_element(
        By.XPATH, '/html/body/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div/div/div/div[1]/div[1]/div[2]/input').send_keys(name)

    xpath = "//h4[contains(text(), '" + name + "')]"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))).click()

    about = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "p")))

    for a in about:
        if a.text:
            ind_about_list.append(a.text)

    # DAOs that use this tool
    # First check to see if none are known
    if check_exists_by_xpath("//p[contains(text(), 'Help us complete')]") == True:
        ind_u_list.append("Not known.")

    # If there are known users
    else:
        # Scroll to bottom of page
        last_height1 = driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            # Scroll to bottom
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(5)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height1:
                break
            last_height1 = new_height

        # If there is a View More button
        if check_exists_by_xpath("//button[contains(text(), 'View more')]") == True:
            # Click it
            element = driver.find_element_by_xpath(
                "//button[contains(text(), 'View more')]")
            driver.execute_script("arguments[0].click();", element)

            # Scroll down to bottom of page
            last_height2 = driver.execute_script(
                "return document.body.scrollHeight")
            while True:
                # Scroll to bottom
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(5)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script(
                    "return document.body.scrollHeight")
                if new_height == last_height2:
                    break
                last_height2 = new_height

            # If there is a Load More button
            if check_exists_by_xpath("//button[contains(text(), 'Load More')]") == True:
                while check_exists_by_xpath("//button[contains(text(), 'Load More')]") == True:
                    element2 = driver.find_element_by_xpath(
                        "//button[contains(text(), 'Load More')]")
                    driver.execute_script(
                        "arguments[0].click();", element2)

                    last_height2 = driver.execute_script(
                        "return document.body.scrollHeight")

                    while True:
                        # Scroll to bottom
                        driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);")

                        # Wait to load page
                        time.sleep(5)

                        # Calculate new scroll height and compare with last scroll height
                        new_height = driver.execute_script(
                            "return document.body.scrollHeight")
                        if new_height == last_height2:
                            break
                        last_height2 = new_height

            # Get used by info
            used_by = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "h4")))
            for u in used_by:
                if u.text:
                    ind_u_list.append(u.text)
            element3 = driver.find_element(
                By.XPATH, '/html/body/div[2]/div[3]/div/h2/button')
            driver.execute_script("arguments[0].click();", element3)
            time.sleep(2)

        # Not a View More button
        else:
            used_by = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "h4")))
            for u in used_by:
                if u.text:
                    ind_u_list.append(u.text)

    driver.execute_script("window.history.go(-1)")
    time.sleep(5)
    return ind_about_list, ind_u_list


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


xpath = "//*[contains(text(), 'Load More')]"

# First scroll
SCROLL_PAUSE_TIME = 5
while check_exists_by_xpath(xpath) == False:
    time.sleep(SCROLL_PAUSE_TIME)

    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight)")

driver.find_element_by_xpath(xpath).click()

last_height = driver.execute_script(
    "return document.body.scrollHeight")

# Second scroll
while True:
    # Scroll to bottom
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script(
        "return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

driver.find_element_by_xpath(xpath).click()

# Final scroll
last_height = driver.execute_script(
    "return document.body.scrollHeight")
while True:
    # Scroll to bottom
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script(
        "return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

tool_names = []
used_by_list = []
about_list = []
try:
    names = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "h4")))

    for n in names:
        if n.text:
            tool_names.append(n.text)

    for t in tool_names:
        about_info, user_info = tool_about(t)
        about_list.append(about_info)
        used_by_list.append(user_info)

finally:
    driver.quit()

tool_tag = tool_tags()
tool_type = tool_types()
result = []
# Adding all info to final results list
for t in tool_names:
    current = [t, [], []]
    for k1, v1 in tool_type.items():
        if t in v1:
            current[1].append(k1)
    if not current[1]:
        current[1].append('None')
    for k2, v2 in tool_tag.items():
        if t in v2:
            current[2].append(k2)
    if not current[2]:
        current[2].append('None')

    result.append(current)


names_l = []
type_l = []
tags_l = []
for r in range(len(result)):
    names_l.append(result[r][0])
    type_l.append(result[r][1])
    tags_l.append(result[r][2])


df = pd.DataFrame({"Name": names_l, "About": about_list,
                  "Type": type_l, "Tags": tags_l, "Used By": used_by_list})
# df = pd.DataFrame({"Name": tool_names})
# print(df)
df.to_excel(r'C:\Users\Student\webScrape\tools_final.xlsx',
            index=False, header=True)
