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

    def process_item(self, item, spider):
        data = {
            "title": item.get("title"),
            "category": item.get("category"),
            "description": item.get("description"),
        }

        response = self.supabase.table("quotes").insert(data).execute()

        if response.error:
            spider.logger.error(f"Failed to insert item into Supabase: {response.error.message}")
        else:
            spider.logger.info(f"Item successfully inserted into Supabase: {response.data}")

        return item

    def close_spider(self, spider):
        spider.logger.info("Finished scraping. Supabase pipeline closed.")
