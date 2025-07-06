import cloudscraper
import datetime as dt

import pandas as pd
from bs4 import BeautifulSoup

from Project_1_web_scraping.web_scraping.config import (
    ITEMS_TO_SCRAPE,
    ITEM_HTML_TAG_MAPPING,
    ITEM_HTML_ATTRIBUTE_MAPPING,
    ITEM_SEARCH_STRATEGY,
    SEARCH_STRATEGIES,
    BASE_URL,
)
from Project_1_web_scraping.web_scraping.helper_functions import cleanup_html_tag


def get_soup(url: str) -> BeautifulSoup:
    """Fetches and parses HTML content from a URL using a scraper."""
    scraper = cloudscraper.create_scraper()
    res = scraper.get(url, timeout=60)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def get_individual_ads_html(soup: BeautifulSoup) -> list[str]:
    """Extracts individual ad URLs from the soup object."""
    ads_list = list(soup.select("a[href*='ID_']"))
    ads_html_list = [link["href"] for link in ads_list]
    return ads_html_list


def parse_ad_detail(url: str) -> dict:
    """Scrapes and parses the details of a single ad page."""
    print(f"[+] Scraping: {url}")
    soup = get_soup(url)
    html_dict = {}
    for item in ITEMS_TO_SCRAPE:
        tag = ITEM_HTML_TAG_MAPPING.get(item)
        attr_value = ITEM_HTML_ATTRIBUTE_MAPPING.get(item)
        strategy = ITEM_SEARCH_STRATEGY.get(item, "tag_only")
        html_tag_finder = SEARCH_STRATEGIES[strategy]
        try:
            html_retrieved_value = html_tag_finder(soup=soup, tag=tag, value=attr_value)
            cleaned = cleanup_html_tag(
                html_retrieved_value=html_retrieved_value, item=item
            )
            html_dict[item] = cleaned
        except Exception as e:
            print(f"[Not OK] {item}")
    if html_dict:
        html_dict["extraction_date"] = dt.datetime.now().astimezone().date()
    return html_dict


def get_ads_from_a_single_page(url: str) -> list[dict]:
    """Collects ad details from all listings on a single search result page."""
    soup = get_soup(url)
    ad_html_list = get_individual_ads_html(soup=soup)
    html_info_dict_list = []
    for ad_html in ad_html_list:
        ad_detail = parse_ad_detail(ad_html)
        html_info_dict_list.append(ad_detail)
    return html_info_dict_list


if __name__ == "__main__":
    combined_html_info_list = []
    for page_index in range(20):
        url = f"{BASE_URL}&page={page_index}"
        html_info_list = get_ads_from_a_single_page(url=url)
        combined_html_info_list.extend(html_info_list)
    df = pd.DataFrame(combined_html_info_list)
    df = df.dropna(how="all")
    df["extraction_date"] = dt.datetime.now().astimezone().date()
    df.to_csv("./data/locanto_ads.csv", index=False)
