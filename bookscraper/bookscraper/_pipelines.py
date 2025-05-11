import os
from dotenv import load_dotenv
from supabase import create_client, Client

class SupabasePipeline:
    def __init__(self):
        load_dotenv()
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_api_key = os.getenv("SUPABASE_API_KEY")

        if not supabase_url or not supabase_api_key:
            raise ValueError("Supabase URL or API Key is missing in environment variables.")

        self.supabase: Client = create_client(supabase_url, supabase_api_key)

    @staticmethod
    def clean_price(price_str):
        # Remove currency symbol and convert to float
        return float(price_str.replace("£", "").strip())

    async def process_item(self, item, spider):
        data = {
            "title": item["name"],
            "price": self.clean_price(item["price"]),
            "url": item["url"]
        }

        try:
            response = self.supabase.table("test").insert(data).execute()
            if not response.data:
                spider.logger.error(f"Failed to insert item into Supabase. Response: {response}")
            else:
                spider.logger.info(f"Item successfully inserted into Supabase: {response.data}")
        except Exception as e:
            spider.logger.error(f"Exception while inserting into Supabase: {e}")

        return item

    def close_spider(self, spider):
        spider.logger.info("Finished scraping. Supabase pipeline closed.")