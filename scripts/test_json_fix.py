#!/usr/bin/env python3
"""
Test script to validate JSON fixing process with a small sample.
"""

import json
import os
from fix_json_streaming import convert_mongodb_objects

def test_conversion():
    """Test the MongoDB object conversion with sample data."""
    
    # Sample MongoDB-style data (similar to what we see in the files)
    sample_data = [
        {
            "_id": "TEST/E/2023/0000001",
            "CategoryV7": {"$numberLong": "11578"},
            "DiaryDate": {"$date": "2023-01-01T00:00:19.977+0000"},
            "UserCode": "110124",
            "closing_date": {"$date": "2023-01-04T00:00:00.000+0000"},
            "dist_name": "Test District",
            "org_code": "TEST",
            "pincode": "700130",
            "recvd_date": {"$date": "2023-01-01T00:00:19.977+0000"},
            "registration_no": "TEST/E/2023/0000001",
            "sex": "M",
            "state": "TS"
        }
    ]
    
    print("🧪 Testing MongoDB object conversion...")
    print("\n📋 Original data:")
    print(json.dumps(sample_data[0], indent=2))
    
    # Convert the data
    converted_data = [convert_mongodb_objects(record) for record in sample_data]
    
    print("\n✨ Converted data:")
    print(json.dumps(converted_data[0], indent=2))
    
    # Validate the conversion
    first_record = converted_data[0]
    
    # Check that MongoDB objects were converted
    tests = [
        ("CategoryV7 is now int", isinstance(first_record.get("CategoryV7"), int)),
        ("DiaryDate is now string", isinstance(first_record.get("DiaryDate"), str)),
        ("closing_date is now string", isinstance(first_record.get("closing_date"), str)),
        ("No $date objects remain", "$date" not in json.dumps(first_record)),
        ("No $numberLong objects remain", "$numberLong" not in json.dumps(first_record)),
    ]
    
    print("\n🔍 Validation results:")
    all_passed = True
    for test_name, result in tests:
        status = "✅" if result else "❌"
        print(f"  {status} {test_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! The conversion is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the conversion logic.")
    
    return all_passed

def check_actual_files():
    """Check if the actual data files exist and show their structure."""
    
    files_to_check = [
        "data/no_pii_grievance_v2.json",
        "data/no_pii_action_history_v2.json"
    ]
    
    print("\n📂 Checking actual data files...")
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"\n📄 {file_path}:")
            print(f"   Size: {size_mb:.1f} MB")
            
            try:
                with open(file_path, 'r') as f:
                    # Read just the first record to show structure
                    content = f.read(2000)  # First 2KB
                    
                print("   First few lines:")
                lines = content.split('\n')[:5]
                for i, line in enumerate(lines, 1):
                    print(f"   {i}: {line[:100]}{'...' if len(line) > 100 else ''}")
                    
            except Exception as e:
                print(f"   ❌ Error reading file: {e}")
        else:
            print(f"⚠️  File not found: {file_path}")

def main():
    """Main test function."""
    print("🔧 JSON Fix Test Suite")
    print("=" * 50)
    
    # Test the conversion logic
    conversion_test_passed = test_conversion()
    
    # Check actual files
    check_actual_files()
    
    print("\n💡 Next steps:")
    if conversion_test_passed:
        print("1. Run: python scripts/fix_json_streaming.py")
        print("2. Choose option 1 to create sample files first")
        print("3. Then choose option 2 to process full files")
    else:
        print("1. Fix the conversion logic in fix_json_streaming.py")
        print("2. Re-run this test script")
    
    print("\n📚 Available scripts:")
    print("- scripts/fix_json_files.py - Full-featured fixer with logging")
    print("- scripts/fix_json_streaming.py - Streaming fixer for large files")
    print("- scripts/test_json_fix.py - This test script")

if __name__ == "__main__":
    main() 