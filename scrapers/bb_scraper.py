import requests as rq
import json
import datetime
from scrapers.stock_data import StockData

# TODO: Should consolidate all of "BestBuy" into scraper folder, and extend to other sites
class BestBuyScraper:
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
    gpu_skus = "|".join([
        '15078017',
        '15166285',
        '15084753',
        '14954116',
        '14953248',
        '14950588',
        '15147122',
        '15038016',
        '15229237',
        '15053087',
        '15309504',
        '14953249',
        '14967857',
        '15318940',
        '15000077',
        '14954117',
        '14953247',
        '15309513',
        '15309514',
        '14966477',
        '15201200',
        '15178453',
        '15053085',
        '15000079',
        '15000078',
        '14953250',
        '15053086',
        '15324508',
        '15317226',
        '15309503'
    ])
    sku_map = {}
    check_interval = 5

    def __init__(self, interval=5):
        print("Initializing BB Scraper")
        self.check_interval = interval
        # Pull current SKU data
        self.sku_map = self.get_skus_map()
        if self.sku_map == {}:
            print("Error occurred when pulling SKU data from Best Buy")
        # Begin Session
        self.session = rq.session()

    # TODO: When we move to thread based, we can change this to thread.run
    # def run(self):
    #     print(f"Running Bestbuy Scraper {self.headers}")

    # Fill in data for existing SKUs
    def get_skus_map(self):
        # TODO: Turn this into a proper request with params
        gpu_prod_list = "https://www.bestbuy.ca/api/v2/json/sku-collections/349221?categoryid=&currentRegion=ON&include=facets%2C%20redirects&lang=en-CA&page=1&pageSize=48&path=category%3AComputers%20%26%20Tablets%3Bcategory%3APC%20Components%3Bcategory%3AGraphics%20Cards%3Bsoldandshippedby0enrchstring%3ABest%20Buy%3Bcustom0graphicscardmodel%3AGeForce%20RTX%203060%7CGeForce%20RTX%203060%20Ti%7CGeForce%20RTX%203070%7CGeForce%20RTX%203090%7CGeForce%20RTX%203080&query=&exp=&sortBy=relevance&sortDir=desc"
        prod_list = rq.get(gpu_prod_list, headers=self.headers, timeout=20)
        print(f"Product List returned in {prod_list.elapsed}")
        prod_list.encoding = 'utf-8-sig'
        prod_data = json.loads(prod_list.text)
        prod_map = {}
        for product in prod_data['products']:
            prod_map[product['sku']] = product
            print(product['name'])
        return prod_map

    # TODO: Performance can change based on VPN, warn if > 1.5s
    """
    Send Request to check stock
    Return list of items, current status, link to product
    """
    def check_skus(self):
        bb_scan = {'stock_found': False, 'in_stock': [], 'out_of_stock': [], 'timestamp': None}
        # print(f'Checking the following SKUs:\n\t{sku_list}')
        sku_map = self.sku_map
        if sku_map == {}:
            return
        bb_gpu_stock = "https://www.bestbuy.ca/ecomm-api/availability/products?"
        availability_params = {
            "accept": "application/vnd.bestbuy.simpleproduct.v1+json",
            "accept-language": "en-CA",
            "locations": "242|705|952|13|973|994|941|958|961|600|796|915|701|929",
            "postalCode": "V5L1A6",
            "skus": self.gpu_skus
        }
        print(f"Sending request to: {bb_gpu_stock}")
        found_smth = False
        stock = self.session.get(bb_gpu_stock, params=availability_params, headers=self.headers, timeout=20)
        bb_scan['timestamp'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        stock.encoding = 'utf-8-sig'
        resp_data = json.loads(stock.text)
        for product in resp_data['availabilities']:
            status = product['shipping']['status']
            other_status = product['pickup']['status']
            prod_info = sku_map[product['sku']]
            name = prod_info['name']
            url = f"https://www.bestbuy.ca{prod_info['productUrl']}"

            item = StockData(status,name, url, "NONE", f"Pickup Status: {other_status}")
            if sku_map[product['sku']] is None:
                print(f"Unknown SKU: {product['sku']}")
                continue
            # \tPickup: {product['pickup']['status']}
            # print(f"{CGREYBG}[{resp_time}] {status}:\t{name} ({url}){CEND}")
            if status != "ComingSoon" and status != "SoldOutOnline" and status != "Unknown":
                found_smth = True
                bb_scan['in_stock'].append(item)
            else:
                bb_scan['out_of_stock'].append(item)
        bb_scan['stock_found'] = found_smth
        print(f"Best Buy: Data returned in {stock.elapsed}")
        return bb_scan
