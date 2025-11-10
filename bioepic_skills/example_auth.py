# -*- coding: utf-8 -*-
"""
Example script showing how to use the bioepic_skills package with authentication.
"""
from bioepic_skills.api_search import APISearch
from bioepic_skills.auth import BioEPICAuth
from bioepic_skills.data_processing import DataProcessing
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """
    Main function demonstrating usage with authentication.
    """
    # Initialize authentication
    auth = BioEPICAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        env=os.getenv("ENV", "prod")
    )
    
    # Verify credentials are loaded
    if not auth.has_credentials():
        logger.error("No credentials found. Please set CLIENT_ID and CLIENT_SECRET in .env file")
        return
    
    logger.info("Authentication initialized successfully")
    
    # Create API client
    api_client = APISearch(collection_name="your_collection", env=os.getenv("ENV", "prod"))
    
    # Create data processing client
    dp = DataProcessing()
    
    # Example: Get records
    try:
        records = api_client.get_records(max_page_size=10)
        logger.info(f"Retrieved {len(records)} records")
        
        if records:
            # Convert to DataFrame
            df = dp.convert_to_df(records)
            logger.info(f"DataFrame shape: {df.shape}")
            logger.info(f"Columns: {df.columns.tolist()}")
    except Exception as e:
        logger.error(f"Error retrieving records: {e}")


if __name__ == "__main__":
    main()
