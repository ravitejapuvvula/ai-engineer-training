import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

try:
    from openpyxl import Workbook
except ImportError as exc:
    raise ImportError(
        "openpyxl is required to export Excel files. Install it with: uv add openpyxl"
    ) from exc

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0 Safari/537.36"
}

class TrolleyDealsScraper:
    BASE_URL = "https://www.trolley.co.uk"
    DEFAULT_DEALS_URL = f"{BASE_URL}/deals/"
    DEFAULT_OUTPUT_FILE = "data/trolley_products.xlsx"
    COLUMNS = [
        "product_id",
        "product_url",
        "product_title",
        "brand",
        "description",
        "size",
        "quantity",
        "store",
        "current_price",
        "previous_price",
        "savings",
        "posted_time",
    ]

    def __init__(self, headers: Optional[Dict[str, str]] = None) -> None:
        self.headers = headers or HEADERS

    def _get_text(self, parent, selector: str) -> str:
        node = parent.select_one(selector)
        return node.get_text(" ", strip=True) if node else ""

    def _extract_store_name(self, card) -> str:
        store_svg = card.select_one("._price svg.store-logo")
        if not store_svg:
            return ""
        class_names = store_svg.get("class", [])
        for class_name in class_names:
            if class_name.startswith("-"):
                return class_name[1:]
        return ""

    def _extract_current_price(self, card) -> str:
        price_block = card.select_one("._price")
        if not price_block:
            return ""
        price_match = re.search(r"£\d+(?:\.\d{1,2})?", price_block.get_text(" ", strip=True))
        return price_match.group(0) if price_match else ""

    def _extract_product(self, card) -> Dict[str, str]:
        link = card.select_one("a[href]")
        product_url = f"{self.BASE_URL}{link['href']}" if link and link.get("href") else ""
        product_title = link.get("title", "").strip() if link else ""

        previous_price_node = card.select_one("._saving strike")

        return {
            "product_id": card.get("data-id", ""),
            "product_url": product_url,
            "product_title": product_title,
            "brand": self._get_text(card, "._brand"),
            "description": self._get_text(card, "._desc"),
            "size": self._get_text(card, "._size > div:first-child"),
            "quantity": self._get_text(card, "._size ._qty"),
            "store": self._extract_store_name(card),
            "current_price": self._extract_current_price(card),
            "previous_price": previous_price_node.get_text(strip=True) if previous_price_node else "",
            "savings": self._get_text(card, "._saving"),
            "posted_time": self._get_text(card, "._time"),
        }

    def scrape_products(self, url: str) -> List[Dict[str, str]]:
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select(".products-grid .product-item")
        return [self._extract_product(card) for card in cards]

    def save_products_to_excel(self, products: List[Dict[str, str]], output_file: str) -> Path:
        workbook = Workbook()
        sheet = workbook.active
        if sheet is None:
            sheet = workbook.create_sheet(title="Daily Deals")
        else:
            sheet.title = "Daily Deals"

        sheet.append(self.COLUMNS)
        for product in products:
            sheet.append([product.get(column, "") for column in self.COLUMNS])

        output_path = Path(output_file)
        workbook.save(output_path)
        return output_path

    def run(
        self,
        url: Optional[str] = None,
        output_file: Optional[str] = None,
    ) -> Tuple[List[Dict[str, str]], Path]:
        scrape_url = url or self.DEFAULT_DEALS_URL
        output_path = output_file or self.DEFAULT_OUTPUT_FILE
        products = self.scrape_products(scrape_url)
        excel_path = self.save_products_to_excel(products, output_path)
        return products, excel_path

if __name__ == "__main__":
    scraper = TrolleyDealsScraper()
    products, excel_path = scraper.run()
    print(f"Scraped {len(products)} products.")
    print(f"Excel file created at: {excel_path.resolve()}")
