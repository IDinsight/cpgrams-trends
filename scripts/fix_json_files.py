#!/usr/bin/env python3
"""
JSON File Fixer for CPGrams Data

This script fixes MongoDB-style JSON files by converting MongoDB-specific 
objects like $date, $numberLong, etc. to standard JSON format.

Usage: python scripts/fix_json_files.py
"""

import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Union
import shutil
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/fix_json.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def convert_mongodb_date(date_obj: Dict[str, str]) -> str:
    """Convert MongoDB $date object to ISO format string."""
    if isinstance(date_obj, dict) and "$date" in date_obj:
        date_str = date_obj["$date"]
        try:
            # Parse the MongoDB date format
            if date_str.endswith("+0000"):
                date_str = date_str[:-6] + "Z"
            elif "+" in date_str and date_str.count("+") == 1:
                date_str = date_str.replace("+0000", "Z")
            
            # Return ISO format
            return date_str
        except Exception as e:
            logger.warning(f"Failed to parse date {date_str}: {e}")
            return date_str
    return date_obj

def convert_mongodb_numberlong(num_obj: Dict[str, str]) -> int:
    """Convert MongoDB $numberLong object to integer."""
    if isinstance(num_obj, dict) and "$numberLong" in num_obj:
        try:
            return int(num_obj["$numberLong"])
        except (ValueError, TypeError) as e:
            logger.warning(f"Failed to parse numberLong {num_obj}: {e}")
            return 0
    return num_obj

def convert_mongodb_objectid(obj_id: Dict[str, str]) -> str:
    """Convert MongoDB $oid object to string."""
    if isinstance(obj_id, dict) and "$oid" in obj_id:
        return obj_id["$oid"]
    return obj_id

def clean_value(value: Any) -> Any:
    """Recursively clean MongoDB-style objects from a value."""
    if isinstance(value, dict):
        if "$date" in value:
            return convert_mongodb_date(value)
        elif "$numberLong" in value:
            return convert_mongodb_numberlong(value)
        elif "$oid" in value:
            return convert_mongodb_objectid(value)
        else:
            # Recursively clean nested dictionaries
            return {k: clean_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        # Recursively clean lists
        return [clean_value(item) for item in value]
    else:
        return value

def fix_json_file(input_file: str, output_file: str) -> bool:
    """
    Fix a JSON file by converting MongoDB objects to standard JSON.
    
    Args:
        input_file: Path to input JSON file
        output_file: Path to output fixed JSON file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info(f"Processing {input_file}...")
        
        # Read the original file
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Loaded {len(data) if isinstance(data, list) else 1} records")
        
        # Clean the data
        cleaned_data = clean_value(data)
        
        # Write the cleaned data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Successfully fixed {input_file} -> {output_file}")
        
        # Verify the output is valid JSON
        with open(output_file, 'r', encoding='utf-8') as f:
            json.load(f)
        
        logger.info(f"✅ Verified {output_file} is valid JSON")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to fix {input_file}: {e}")
        return False

def get_file_size_mb(file_path: str) -> float:
    """Get file size in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)

def create_backup(file_path: str) -> str:
    """Create a backup of the original file."""
    backup_path = f"{file_path}.backup"
    shutil.copy2(file_path, backup_path)
    logger.info(f"Created backup: {backup_path}")
    return backup_path

def validate_json_structure(file_path: str) -> Dict[str, Any]:
    """Validate and analyze JSON file structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        info = {
            "valid": True,
            "type": type(data).__name__,
            "count": len(data) if isinstance(data, list) else 1,
            "sample_keys": []
        }
        
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            if isinstance(first_item, dict):
                info["sample_keys"] = list(first_item.keys())[:10]  # First 10 keys
        
        return info
        
    except Exception as e:
        return {"valid": False, "error": str(e)}

def main():
    """Main function to process JSON files."""
    logger.info("🔧 Starting JSON file fixing process...")
    
    # Define file mappings
    files_to_fix = [
        {
            "input": "data/no_pii_grievance_v2.json",
            "output": "data/fixed_grievance_v2.json",
            "description": "Grievance data"
        },
        {
            "input": "data/no_pii_action_history_v2.json", 
            "output": "data/fixed_action_history_v2.json",
            "description": "Action history data"
        },
        {
            "input": "data/no_pii_grievance.json",
            "output": "data/fixed_grievance.json",
            "description": "Original grievance data"
        },
        {
            "input": "data/no_pii_action_history.json",
            "output": "data/fixed_action_history.json", 
            "description": "Original action history data"
        }
    ]
    
    results = []
    
    for file_info in files_to_fix:
        input_file = file_info["input"]
        output_file = file_info["output"]
        description = file_info["description"]
        
        if not os.path.exists(input_file):
            logger.warning(f"⚠️  File not found: {input_file}")
            continue
        
        # Show file info
        size_mb = get_file_size_mb(input_file)
        logger.info(f"\n📄 Processing {description}")
        logger.info(f"   Input: {input_file} ({size_mb:.1f} MB)")
        logger.info(f"   Output: {output_file}")
        
        # Validate original structure
        original_info = validate_json_structure(input_file)
        if not original_info["valid"]:
            logger.error(f"❌ Invalid JSON in {input_file}: {original_info['error']}")
            continue
        
        logger.info(f"   Original: {original_info['type']} with {original_info['count']} items")
        if original_info["sample_keys"]:
            logger.info(f"   Sample keys: {', '.join(original_info['sample_keys'][:5])}...")
        
        # Create backup
        backup_path = create_backup(input_file)
        
        # Fix the file
        success = fix_json_file(input_file, output_file)
        
        if success:
            # Validate fixed structure
            fixed_info = validate_json_structure(output_file)
            if fixed_info["valid"]:
                fixed_size_mb = get_file_size_mb(output_file)
                logger.info(f"   Fixed: {fixed_info['type']} with {fixed_info['count']} items ({fixed_size_mb:.1f} MB)")
                results.append({"file": description, "status": "✅ Success", "output": output_file})
            else:
                logger.error(f"❌ Fixed file is invalid: {fixed_info['error']}")
                results.append({"file": description, "status": "❌ Failed validation", "output": None})
        else:
            results.append({"file": description, "status": "❌ Failed processing", "output": None})
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 PROCESSING SUMMARY")
    logger.info("="*60)
    
    for result in results:
        logger.info(f"{result['status']} {result['file']}")
        if result['output']:
            logger.info(f"   → {result['output']}")
    
    successful = len([r for r in results if "✅" in r["status"]])
    total = len(results)
    
    logger.info(f"\n🎯 Completed: {successful}/{total} files processed successfully")
    
    if successful > 0:
        logger.info("\n💡 NEXT STEPS:")
        logger.info("1. Review the fixed JSON files in the data/ directory")
        logger.info("2. Update your application to use the fixed files")
        logger.info("3. Original files are backed up with .backup extension")
        logger.info("4. Check fix_json.log for detailed processing information")

if __name__ == "__main__":
    main() 