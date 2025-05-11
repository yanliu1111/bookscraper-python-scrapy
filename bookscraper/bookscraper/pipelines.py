import os
from dotenv import load_dotenv
from supabase import create_client, Client
from itemadapter import ItemAdapter

class SupabasePipeline:
    def __init__(self):
        load_dotenv()
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_api_key = os.getenv("SUPABASE_API_KEY")

        if not supabase_url or not supabase_api_key:
            raise ValueError("Supabase URL or API Key is missing in environment variables.")

        self.supabase: Client = create_client(supabase_url, supabase_api_key)

    def clean_price(self, price_str):
        # Remove currency symbol and convert to float
        return float(price_str.replace("£", "").strip())

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Clean and normalize fields
        for field_name in adapter.field_names():
            value = adapter.get(field_name)
            if isinstance(value, tuple):  # If the value is a tuple, extract the first element
                value = value[0]
            if value and field_name != 'description':  # Skip description for stripping
                adapter[field_name] = value.strip()

        # Convert specific fields to lowercase
        lowercase_keys = ['category', 'product_type']
        for key in lowercase_keys:
            value = adapter.get(key)
            if value:
                adapter[key] = value.lower()

        # Clean price fields
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for key in price_keys:
            value = adapter.get(key)
            if value:
                adapter[key] = self.clean_price(value)

        # Parse availability
        availability_string = adapter.get('availability', '')
        if '(' in availability_string:
            availability = availability_string.split('(')[1].split(' ')[0]
            adapter['availability'] = int(availability)
        else:
            adapter['availability'] = 0

        # Convert number of reviews to integer
        num_reviews = adapter.get('num_reviews', '0')
        adapter['num_reviews'] = int(num_reviews)

        # Parse star ratings
        stars_string = adapter.get('stars', '')
        if stars_string:
            stars_text = stars_string.split(' ')[1].lower()
            stars_map = {
                "zero": 0,
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
                "five": 5,
            }
            adapter['stars'] = stars_map.get(stars_text, 0)

        # Prepare data for Supabase
        data = {
            "url": adapter.get("url"),
            "title": adapter.get("title"),
            "upc": adapter.get("upc"),
            "product_type": adapter.get("product_type"),
            "price_excl_tax": adapter.get("price_excl_tax"),
            "price_incl_tax": adapter.get("price_incl_tax"),
            "tax": adapter.get("tax"),
            "availability": adapter.get("availability"),
            "num_reviews": adapter.get("num_reviews"),
            "stars": adapter.get("stars"),
            "category": adapter.get("category"),
            "description": adapter.get("description"),
            "price": adapter.get("price"),
        }

        # Send data to Supabase
        response = self.supabase.table("books").insert(data).execute()

        # Handle Supabase response
        if response.error:
            spider.logger.error(f"Failed to insert item into Supabase: {response.error}")
        else:
            spider.logger.info(f"Item successfully inserted into Supabase: {response.data}")

        return item

    def close_spider(self, spider):
        spider.logger.info("Finished scraping. Supabase pipeline closed.")