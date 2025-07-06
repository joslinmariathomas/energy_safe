from bs4 import BeautifulSoup, Tag


# Functions to find html tags and values from a html url
def find_by_id(soup: BeautifulSoup, tag: str, value: str | None):
    return soup.find(name=tag, id=value)


def find_by_class(soup: BeautifulSoup, tag: str, value: str | None):
    return soup.find(name=tag, class_=value)


def find_by_itemprop(soup: BeautifulSoup, tag: str, value: str | None):
    return soup.find(name=tag, itemprop=value)


def find_tag_only(soup: BeautifulSoup, tag: str, value: str | None = None):
    return soup.find(name=tag)


def cleanup_html_tag(item: str, html_retrieved_value: Tag) -> str:
    """Cleans and formats extracted HTML content based on item type."""
    if not html_retrieved_value:
        return ""
    if item == "price" and html_retrieved_value:
        html_retrieved_value = html_retrieved_value.find("div")
    if item == "posting_date":
        retrieved_value = (
            html_retrieved_value.get_text(" ", strip=True)
            .replace("Posted:", "")
            .strip()
        )
        return retrieved_value
    html_retrieved_value = (
        html_retrieved_value.get_text(strip=True) if html_retrieved_value else ""
    )
    return html_retrieved_value
