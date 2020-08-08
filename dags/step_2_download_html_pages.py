from time import sleep

import numpy as np
import requests
from bs4 import BeautifulSoup

import context
from avito_page_parser import PageParser
from store import Store


class HtmlPagesDownloader:
    def __init__(self):
        self.store: Store = context.store
        self.parser: PageParser = context.parser
        self.url = context.BASE_URL
        self.max_page_count = context.MAX_PAGE_COUNT

    def execute(self):
        print("\n/////////\n/// HtmlPagesDownloader part\n/////////")

        for page_number in range(1, self.max_page_count):
            response = requests.get(self.url.format(page_number))
            
            if response.status_code != 200:
                raise Exception("Page {} cannot be downloaded".format(page_number))

            tree = BeautifulSoup(response.content, 'html.parser')
            flats = self.parser.get_all_flats(tree)

            # if we come to page after final. Becouse of `response_code` also 200
            try:
                flats[0]
            except Exception:
                break

            self.store.save_html_page(page_number, response.text)
            self.__random_sleep()

    def __random_sleep(self):
        r = np.random.normal(size=1, loc=5, scale=2)[0]
        if r < 1:
            r = 1.2345
        if r > 8:
            r = 6.6666
        sleep(r)