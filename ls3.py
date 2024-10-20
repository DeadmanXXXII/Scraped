from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re

# Path to the chromedriver executable
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

# Configure Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")

# Initialize WebDriver with the path to the chromedriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_profile_links(url):
    driver.get(url)
    time.sleep(5)  # Wait for page to load

    # Extract profile links
    links = set()
    elements = driver.find_elements(By.TAG_NAME, 'a')
    for element in elements:
        href = element.get_attribute('href')
        if href and 'linkedin.com' in href:
            links.add(href)

    return links

def get_post_links(url):
    driver.get(url)
    time.sleep(5)  # Wait for page to load

    # Extract post links
    post_links = set()
    posts = driver.find_elements(By.CLASS_NAME, 'post-class-name')  # Update class name as needed
    for post in posts:
        post_text = post.text
        urls = re.findall(r'https://\S+', post_text)
        post_links.update(urls)

    return post_links

# Define URLs
company_url = 'https://www.linkedin.com/company/hackerone/'
profile_url = 'https://www.linkedin.com/in/blu-corbel-bb5700265'

# Extract links
company_links = get_profile_links(company_url)
profile_links = get_profile_links(profile_url)
post_links = get_post_links(company_url)

# Combine and print all links
all_links = company_links.union(profile_links).union(post_links)
for link in all_links:
    print(link)

# Clean up
driver.quit()
