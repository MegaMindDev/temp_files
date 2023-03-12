import sys
print('original path: ')
print(sys.path)
sys.path.append('/home/ec2-user/web-scrape/opt/selenium/python/lib/python3.6/site-packages')
print('revised path: ')
print(sys.path)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main(event, context):
    print('setting options')
    options = Options()
    options.binary_location = '/home/ec2-user/web-scrape/opt/chromedriver/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    print('Opening webriver')
    driver = webdriver.Chrome('/home/ec2-user/web-scrape/opt/chromedriver/chromedriver',chrome_options=options)
    print('retrieving finance.yahoo.com/ACN')
    driver.get('https://finance.yahoo.com/quote/ACN')

    share_name = ''
    try:
       print('looking for consent form...')
       consent_form = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//form[@class="consent-form"]')))
       print('looking for agree button...')
       agree = consent_form.find_element(By.XPATH, '//button[@name="agree"]')
       print('clicking agree button...')
       agree.click()
       print('looking for quote-header-info....')
       element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'quote-header-info')))
       share_name = element.text

    except Exception as e:
       print(e)
       share_name = 'not found'

    print(share_name)

    print('closing driver')
    driver.close();
    driver.quit();

    response = {
        "statusCode": 200,
        "body": share_name
    }

    return response

print(main(None, None))
