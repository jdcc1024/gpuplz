from selenium import webdriver

class BestBuySelenium:

    def __init__(self):
        # Turn on Chrome for BB
        driver = webdriver.Chrome()
        driver.get("https://www.bestbuy.ca")

        # Check login status
        # Check get cart data
        # Fire baskets API call?
        # Skip to qti (shipping)
        # Continue -> Shipping, choose Shipping addr
        # Shipping -> CC, choose CC
        # Confirm