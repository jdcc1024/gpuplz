import requests as rq
import json
import datetime
import time
from playsound import playsound
from scrapers.bb_scraper import BestBuyScraper
import util.util as util

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "authority": "www.bestbuy.ca",
        "pragma": "no-cache",
        "accept": "*/*",  # "text/html, application/xhtml+xml, application/xml;",
        "referer": "https://www.bestbuy.ca",
        "accept-encoding": "gzip,deflate,br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1"
        }
check_interval = 5
# bb_scraper = None

def test_init():
    print(f'Beginning Script')
    # logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    test_init()
    # my_skus = get_skus()
    # check_skus(my_skus)
    bb_scraper = BestBuyScraper()
    util.print_yellow("Check Best Buy")
    # Start Selenium to initialize user session

    # Begin Scraping
    for n in range(0, 3600):
        bb_scan = bb_scraper.check_skus()
        if bb_scan['stock_found'] is True:
            for item in bb_scan['in_stock']:
                util.print_red(f"{item.status} - {item.name} ({item.url}) - NOTE: {item.notes}")
            playsound('./mp3/sealedBoxMusic.mp3')  # Playing sound blocks the thread, make sure this is last!
            time.sleep(10)  # Sleep for 10s so user can click in time?
            # Sort by largest stock number
            # Send signal to selenium to fire baskets call via injected html
            # Send signal to selenium to begin cart purchase process
        else:
            for item in bb_scan['out_of_stock']:
                util.print_yellow(f"{item.status} - {item.name} ({item.url}) - NOTE: {item.notes}")
            # playsound('./mp3/type.mp3')
        time.sleep(check_interval)


