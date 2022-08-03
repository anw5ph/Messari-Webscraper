import pandas as pd
import requests
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

# Gets the about information for a given DAO


def DAO_about(name):
    url = 'https://messari.io/dao/'
    lower_name = str(name).replace(' ', '-').lower()
    gov = '-governance'

    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920, 1200")
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    strange_name_urls = {'SuperRare': 'super-rare', 'Aave Grants DAO': None, 'Pool Together': 'Pool%20Together', 'Uniswap Grants Program': None, 'Curve Finance': 'curve',
                         'B.Protocol': 'bprotocol-governance', 'Polkadot': 'polkadot-dao-governance', 'Olympus': 'olympus-dao-governance', 'RSS3': 'rss-3-governance',
                         'Idle ': 'idle-governance', 'Alpha Venture DAO': 'alpha-finance-governance', 'DopeWars': 'dope', 'Ronin ': 'ronin', 'Ocean DAO': None,
                         'D5 - The Data Science DAO': 'd5-the-data-science-dao', 'Endangered Tokens': 'endangered-tokens', 'TOADz DAO': None, 'Sound.xyz': 'soundxyz', 'GEN.ART': 'genart',
                         'Crypto.com': 'cryptocom', 'H.E.R. DAO': 'her-dao', 'Tinsel  DAO': 'tinsel-dao', 'seen.haus': 'seenhaus', 'Midas DAO': None, 'APY.Finance': 'apyfinance',
                         'Water & Music': 'water-music', 'Crypto, Culture & Society': 'crypto-culture-society', 'AlgoDAO': 'algo-dao', 'Bibliotheca (for Loot)': 'bibliotheca-for-loot',
                         'Myosin.xyz': 'myosin-xyz', 'Own.fund': 'ownfund', 'Graph Advocates DAO\n': None, 'Rari Capital': 'rari-capital-dao-governance', 'Synesis One ': 'synesis-one',
                         'HairDAO': 'hair-dao', 'THiNG.FUND': 'thingfund', '𝔡𝔦𝔳𝔦𝔫𝔢 𝔡𝔞𝔬': 'divine-dao'}
    info = []
    try:
        format_url = url + lower_name + gov
        driver.get(format_url)

        # First error check
        one_error_check = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "p")))

        if one_error_check[0].text == 'Unable to load page':

            try:
                diff_url = url + lower_name
                driver.get(diff_url)

                # Second error check
                two_error_check = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "p")))

                if two_error_check[0].text == 'Unable to load page':

                    for k in strange_name_urls:
                        if k == name:
                            if strange_name_urls[k] != None:
                                try:
                                    strange_url = url + strange_name_urls[k]
                                    driver.get(strange_url)

                                    about = WebDriverWait(driver, 10).until(
                                        EC.presence_of_all_elements_located((By.TAG_NAME, "p")))

                                    info.append(about[2].text)

                                    # More About:
                                    try:
                                        more = WebDriverWait(driver, 10).until(
                                            EC.presence_of_all_elements_located((By.TAG_NAME, "ul")))
                                        for m in range(1, len(more)):
                                            if more[m].text:
                                                info.append(more[m].text)
                                    except:
                                        print("No list")

                                    return info

                                finally:
                                    driver.quit()
                            else:
                                info.append("No information known.")
                                return info

                try:
                    # About DAO
                    about = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, "p")))
                    info.append(about[2].text)

                    # More About:
                    try:
                        more = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.TAG_NAME, "ul")))
                        for m in range(1, len(more)):
                            if more[m].text:
                                info.append(more[m].text)
                    except:
                        print("No list")

                    return info

                finally:
                    driver.quit()
            except:
                exit()

        try:
            # About DAO
            about = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "p")))
            info.append(about[2].text)

            # More About:
            try:
                more = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "ul")))
                for m in range(1, len(more)):
                    if more[m].text:
                        info.append(more[m].text)
            except:
                print("No list")

            return info

        finally:
            driver.quit()

    except:
        info.append(name)
        return info

# Gets the type for a given DAO


def DAO_types():
    def check_exists_by_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    xpath = "//*[contains(text(), 'Load More')]"

    # Get the url
    url = 'https://messari.io/governor/daos?types='
    types_urls = ['Collector', 'Grants', 'Impact', 'Investment',
                  'Media', 'Product', 'Protocol', 'Service', 'Social+%2F+Community']

    result = []
    for t in types_urls:

        options = Options()
        options.headless = False
        options.add_argument("--window-size=1920, 1200")
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

        driver.get(url+t)

        filter_list = []

        # Keep scrolling
        if t == "Protocol":
            SCROLL_PAUSE_TIME = 5
            while check_exists_by_xpath(xpath) == False:
                time.sleep(SCROLL_PAUSE_TIME)

                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight)")

            driver.find_element_by_xpath(xpath).click()

            # SCROLL_PAUSE_TIME = 10
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
        else:
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

    dao_types = {'Collector': result[0], 'Grants': result[1], 'Impact': result[2], 'Investment': result[3],
                 'Media': result[4], 'Product': result[5], 'Protocol': result[6], 'Service': result[7], 'Social+%2F+Community': result[8]}
    return dao_types

# Gets the tags for a DAO


def DAO_tags():
    # Get the url
    url = 'https://messari.io/governor/daos?tags='
    tags_urls = ["Analytics", "Art", "City", "Culture", "DAO+Tool", "DeFi", "Developers", "Education", "Events+%2F+Experiences",
                 "Future+Of+Work", "Gaming", "Incubator", "Infrastructure", "Metaverse", "Music", "NFTs", "P2E", "Public+Good+Funding", "Real+World+Asset+Purchase", "Research", "Science", "Sports", "Sustainability", "Venture"]

    result = []
    for t in tags_urls:

        options = Options()
        options.headless = False
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

    dao_tags = {"Analytics": result[0], "Art": result[1], "City": result[2], "Culture": result[3], "DAO+Tool": result[4], "DeFi": result[5], "Developers": result[6], "Education": result[7], "Events+%2F+Experiences": result[8],
                "Future+Of+Work": result[9], "Gaming": result[10], "Incubator": result[11], "Infrastructure": result[12], "Metaverse": result[13], "Music": result[14], "NFTs": result[15], "P2E": result[16], "Public+Good+Funding": result[17], "Real+World+Asset+Purchase": result[18], "Research": result[19], "Science": result[20], "Sports": result[21], "Sustainability": result[22], "Venture": result[23]}
    return dao_tags


payload = {"requests": [{"indexName": "governance_production", "params": "highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&hitsPerPage=855&attributesToRetrieve=%5B%22id%22%5D&maxValuesPerFacet=100&query=&page=0&facets=%5B%22types%22%2C%22tags%22%5D&tagFilters="}]}
url = 'https://3b439zgym3-2.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)&x-algolia-application-id=3B439ZGYM3&x-algolia-api-key=14a0c8d17665d52e61167cc1b2ae9ff1'
headers = {"content-type": "application/x-www-form-urlencoded"}
req = requests.post(url, headers=headers, json=payload).json()

daos = []

for item in req['results'][0]['hits']:
    daos.append(item['_highlightResult']['name']['value'],
                # "details": item['_highlightResult']['details']['value'],
                )

# print(data)

# Function call for dao tags and dao types
dao_tags = DAO_tags()
dao_types = DAO_types()

result = []

# Adding all info to final results list
for d in daos:
    current = [d, [], [], []]
    current[1].append(DAO_about(d))
    for k1, v1 in dao_types.items():
        if d in v1:
            current[2].append(k1)
    if not current[2]:
        current[2].append('None')
    for k2, v2 in dao_tags.items():
        if d in v2:
            current[3].append(k2)
    if not current[3]:
        current[3].append('None')

    result.append(current)

# print(result)
names_l = []
about_l = []
type_l = []
tags_l = []
for r in range(len(result)):
    names_l.append(result[r][0])
    about_l.append(result[r][1])
    type_l.append(result[r][2])
    tags_l.append(result[r][3])


df = pd.DataFrame({"Name": names_l, "About": about_l,
                  "Type": type_l, "Tags": tags_l})
# print(df)
df.to_excel(r'C:\Users\Student\webScrape\messari_dataframe_final.xlsx',
            index=False, header=True)
