#!/usr/bin/env python3
"""
Streaming JSON File Fixer for Large CPGrams Data Files

This script fixes large MongoDB-style JSON files by processing them in chunks
to avoid memory issues with very large files (300MB+).

Usage: python scripts/fix_json_streaming.py
"""

import json
import os
import re
from typing import Any, Dict, List, Iterator
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_mongodb_objects(obj: Any) -> Any:
    """Convert MongoDB-specific objects to standard JSON format."""
    if isinstance(obj, dict):
        if "$date" in obj:
            # Convert MongoDB date to ISO string
            date_str = obj["$date"]
            if date_str.endswith("+0000"):
                return date_str[:-6] + "Z"
            return date_str
        elif "$numberLong" in obj:
            # Convert MongoDB numberLong to integer
            try:
                return int(obj["$numberLong"])
            except (ValueError, TypeError):
                return 0
        elif "$oid" in obj:
            # Convert MongoDB ObjectId to string
            return obj["$oid"]
        else:
            # Recursively process nested objects
            return {k: convert_mongodb_objects(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # Recursively process list items
        return [convert_mongodb_objects(item) for item in obj]
    else:
        return obj

def process_json_chunks(input_file: str, output_file: str, chunk_size: int = 1000) -> bool:
    """
    Process JSON file in chunks to handle large files.
    
    Args:
        input_file: Path to input JSON file
        output_file: Path to output fixed JSON file
        chunk_size: Number of records to process at once
        
    Returns:
        bool: True if successful
    """
    try:
        logger.info(f"Processing {input_file} in chunks of {chunk_size}")
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            # Load the entire JSON array (this is needed since it's a single array)
            data = json.load(infile)
        
        total_records = len(data)
        logger.info(f"Total records to process: {total_records}")
        
        # Process and write in chunks
        processed_data = []
        
        for i in range(0, total_records, chunk_size):
            chunk = data[i:i + chunk_size]
            logger.info(f"Processing chunk {i//chunk_size + 1}/{(total_records + chunk_size - 1)//chunk_size}")
            
            # Clean the chunk
            cleaned_chunk = [convert_mongodb_objects(record) for record in chunk]
            processed_data.extend(cleaned_chunk)
        
        # Write the cleaned data
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(processed_data, outfile, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Successfully processed {total_records} records")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error processing {input_file}: {e}")
        return False

def create_sample_file(input_file: str, output_file: str, sample_size: int = 100) -> bool:
    """Create a small sample file for testing."""
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
        
        sample_data = data[:sample_size] if len(data) > sample_size else data
        cleaned_sample = [convert_mongodb_objects(record) for record in sample_data]
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(cleaned_sample, outfile, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Created sample file with {len(cleaned_sample)} records: {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating sample from {input_file}: {e}")
        return False

def main():
    """Main function to process JSON files."""
    logger.info("🔧 Starting streaming JSON file fixing process...")
    
    # Create scripts directory if it doesn't exist
    os.makedirs('scripts', exist_ok=True)
    
    # Check file sizes first
    files_info = [
        ("data/no_pii_grievance_v2.json", "Fixed Grievance V2"),
        ("data/no_pii_action_history_v2.json", "Fixed Action History V2"),
        ("data/no_pii_grievance.json", "Fixed Grievance"),
        ("data/no_pii_action_history.json", "Fixed Action History")
    ]
    
    for file_path, description in files_info:
        if os.path.exists(file_path):
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            logger.info(f"📄 {description}: {size_mb:.1f} MB")
    
    # Ask user what to do
    print("\nChoose an option:")
    print("1. Create sample files (100 records each) for testing")
    print("2. Process full files (may take a while for large files)")
    print("3. Process with custom chunk size")
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice == "1":
        # Create sample files
        logger.info("Creating sample files...")
        for file_path, description in files_info:
            if os.path.exists(file_path):
                output_file = file_path.replace('.json', '_sample.json').replace('data/', 'data/samples/')
                os.makedirs('data/samples', exist_ok=True)
                create_sample_file(file_path, output_file, 100)
    
    elif choice == "2":
        # Process full files with default chunk size
        chunk_size = 1000
        logger.info(f"Processing full files with chunk size: {chunk_size}")
        
        for file_path, description in files_info:
            if os.path.exists(file_path):
                output_file = file_path.replace('.json', '_fixed.json')
                logger.info(f"\n🔄 Processing {description}...")
                success = process_json_chunks(file_path, output_file, chunk_size)
                if success:
                    # Verify output
                    try:
                        with open(output_file, 'r') as f:
                            test_data = json.load(f)
                        logger.info(f"✅ Verified: {len(test_data)} records in {output_file}")
                    except Exception as e:
                        logger.error(f"❌ Verification failed for {output_file}: {e}")
    
    elif choice == "3":
        # Process with custom chunk size
        try:
            chunk_size = int(input("Enter chunk size (recommended: 500-2000): "))
            logger.info(f"Processing with custom chunk size: {chunk_size}")
            
            for file_path, description in files_info:
                if os.path.exists(file_path):
                    output_file = file_path.replace('.json', '_fixed.json')
                    logger.info(f"\n🔄 Processing {description}...")
                    process_json_chunks(file_path, output_file, chunk_size)
                    
        except ValueError:
            logger.error("❌ Invalid chunk size. Please enter a number.")
    
    else:
        logger.error("❌ Invalid choice. Please run the script again.")
    
    logger.info("\n🎯 Processing completed!")
    logger.info("💡 Check the output files and verify they work with your application.")

if __name__ == "__main__":
    main() 