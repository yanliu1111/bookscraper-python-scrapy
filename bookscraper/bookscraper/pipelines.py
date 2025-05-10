# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
from dotenv import load_dotenv
from supabase import create_client, Client

class SupabasePipeline:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get Supabase credentials from environment variables
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_api_key = os.getenv("SUPABASE_API_KEY")

        if not supabase_url or not supabase_api_key:
            raise ValueError("Supabase URL or API Key is missing in environment variables.")

        # Initialize Supabase client
        self.supabase: Client = create_client(supabase_url, supabase_api_key)

    def process_item(self, item, spider):
        # Insert item into Supabase database
        data = {
            "field1": item.get("field1"),
            "field2": item.get("field2"),
            # Map your item fields to database columns
        }

        response = self.supabase.table("your_table_name").insert(data).execute()

        if response.status_code != 200:
            spider.logger.error(f"Failed to insert item into Supabase: {response.json()}")
        else:
            spider.logger.info(f"Item successfully inserted into Supabase: {response.json()}")

        return item