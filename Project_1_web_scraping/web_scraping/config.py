"""'
Lists constants and mappings used in the parent folder - web_scraping
"""

from electrician_ads_scraping_locanto.web_scraping.helper_functions import (
    find_by_id,
    find_by_class,
    find_by_itemprop,
    find_tag_only,
)

WEBSITE_TO_SCRAPE = "https://www.locanto.com.au/"
SERVICE_TO_SEARCH = "electricians"
BASE_URL = f"{WEBSITE_TO_SCRAPE}/g/q/?query={SERVICE_TO_SEARCH}"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
}

ITEMS_TO_SCRAPE = [
    "id",
    "title",
    "description",
    "suburb",
    "postcode",
    "latitude",
    "longitude",
    "posting_date",
    "price",
]
ITEM_HTML_TAG_MAPPING = {
    "id": "a",
    "title": "h1",
    "description": "div",
    "suburb": "span",
    "postcode": "span",
    "latitude": "span",
    "longitude": "span",
    "posting_date": "div",
    "price": "div",
}

ID_VALUE_LIST = ["id"]
CLASS_VALUE_LIST = ["description", "posting_date", "price"]
ITEMPROP_LIST = [
    "suburb",
    "postcode",
    "latitude",
    "longitude",
]
ITEM_HTML_ATTRIBUTE_MAPPING = {
    "id": "adID",
    "title": "",
    "description": "vap__description",
    "suburb": "addressLocality",
    "postcode": "postalCode",
    "latitude": "latitude",
    "longitude": "longitude",
    "posting_date": "vap_user_content__date",
    "price": "vap_user_content__price",
}
SEARCH_STRATEGIES = {
    "id": find_by_id,
    "class": find_by_class,
    "itemprop": find_by_itemprop,
    "tag_only": find_tag_only,
}
ITEM_SEARCH_STRATEGY = {
    "id": "id",
    "title": "tag_only",
    "description": "class",
    "suburb": "itemprop",
    "postcode": "itemprop",
    "latitude": "itemprop",
    "longitude": "itemprop",
    "posting_date": "class",
    "price": "class",
}
