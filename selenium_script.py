from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymongo
import uuid
import requests

# Initialize MongoDB client
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter_trending"]
collection = db["trends"]

# Function to get new IP address from ProxyMesh
def get_new_ip():
    # This is a placeholder function. Implement actual ProxyMesh API usage here.
    response = requests.get("http://example.com/get-new-ip")  # replace with actual ProxyMesh API call
    return response.json()["ip"]

# Configure Selenium with ProxyMesh
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=%s' % get_new_ip())
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Log in to Twitter
driver.get("https://twitter.com/login")
time.sleep(5)
username = driver.find_element(By.NAME, "session[username_or_email]")
password = driver.find_element(By.NAME, "session[password]")
username.send_keys("your_twitter_username")
password.send_keys("your_twitter_password")
driver.find_element(By.XPATH, '//div[@data-testid="LoginForm_Login_Button"]').click()
time.sleep(5)

# Fetch trending topics
trends = []
driver.get("https://twitter.com/explore")
time.sleep(5)
trending_elements = driver.find_elements(By.XPATH, '//div[@aria-label="Timeline: Trending now"]//span')
for elem in trending_elements[:5]:  # Get top 5 trending topics
    trends.append(elem.text)

# Store in MongoDB
record = {
    "_id": str(uuid.uuid4()),
    "trend1": trends[0],
    "trend2": trends[1],
    "trend3": trends[2],
    "trend4": trends[3],
    "trend5": trends[4],
    "start_time": time.time(),
    "end_time": time.time(),
    "ip_address": get_new_ip()
}
collection.insert_one(record)

# Close the browser
driver.quit()

print("Trending topics saved to MongoDB.")
