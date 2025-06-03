# JSON File Fixing Scripts

This directory contains scripts to fix MongoDB-style JSON files from the CPGrams dataset by converting them to standard JSON format.

## Problem Statement

The provided JSON files contain MongoDB-specific objects that need conversion:

- `{ "$date": "2023-01-01T00:00:19.977+0000" }` → `"2023-01-01T00:00:19.977Z"`
- `{ "$numberLong": "11578" }` → `11578`
- `{ "$oid": "507f1f77bcf86cd799439011" }` → `"507f1f77bcf86cd799439011"`

## Available Scripts

### 1. `fix_json_files.py` - Full-Featured Fixer

**Best for**: Comprehensive fixing with detailed logging and validation.

```bash
python scripts/fix_json_files.py
```

**Features:**

- Detailed logging to `data/fix_json.log`
- Automatic backup creation
- File validation before and after processing
- Progress tracking
- Error handling and recovery

**Output Files:**

- `data/fixed_grievance_v2.json`
- `data/fixed_action_history_v2.json`
- `data/fixed_grievance.json`
- `data/fixed_action_history.json`

### 2. `fix_json_streaming.py` - Streaming Processor

**Best for**: Large files (300MB+) that might cause memory issues.

```bash
python scripts/fix_json_streaming.py
```

**Options:**

1. **Create sample files** (100 records each) - Great for testing
2. **Process full files** - Production use
3. **Custom chunk size** - Fine-tune performance

**Features:**

- Memory-efficient chunked processing
- Interactive options
- Sample file creation for testing
- Progress tracking per chunk

### 3. `test_json_fix.py` - Validation & Testing

**Best for**: Testing the conversion logic before processing large files.

```bash
python scripts/test_json_fix.py
```

**Features:**

- Tests conversion logic with sample data
- Validates MongoDB object conversion
- Shows file structure and sizes
- Provides next-step recommendations

## Usage Workflow

### Recommended Approach

1. **Test First:**

   ```bash
   python scripts/test_json_fix.py
   ```

2. **Create Samples:**

   ```bash
   python scripts/fix_json_streaming.py
   # Choose option 1
   ```

3. **Validate Samples:**

   ```bash
   # Check files in data/samples/ directory
   python -c "import json; print(json.load(open('data/samples/no_pii_grievance_v2_sample.json'))[:2])"
   ```

4. **Process Full Files:**
   ```bash
   python scripts/fix_json_streaming.py
   # Choose option 2
   ```

### Quick Fix (If you're confident)

```bash
python scripts/fix_json_files.py
```

## File Information

The scripts process these files from the `data/` directory:

| Original File                   | Size   | Description             |
| ------------------------------- | ------ | ----------------------- |
| `no_pii_grievance_v2.json`      | ~320MB | Updated grievance data  |
| `no_pii_action_history_v2.json` | ~614MB | Updated action history  |
| `no_pii_grievance.json`         | ~326MB | Original grievance data |
| `no_pii_action_history.json`    | ~697MB | Original action history |

## Output Structure

### Original (MongoDB format):

```json
{
  "_id": "MORLY/E/2023/0000001",
  "CategoryV7": { "$numberLong": "11578" },
  "DiaryDate": { "$date": "2023-01-01T00:00:19.977+0000" },
  "closing_date": { "$date": "2023-01-04T00:00:00.000+0000" }
}
```

### Fixed (Standard JSON):

```json
{
  "_id": "MORLY/E/2023/0000001",
  "CategoryV7": 11578,
  "DiaryDate": "2023-01-01T00:00:19.977Z",
  "closing_date": "2023-01-04T00:00:00.000Z"
}
```

## Error Handling

- **Memory Issues**: Use `fix_json_streaming.py` with smaller chunk sizes
- **File Not Found**: Ensure files are in the `data/` directory
- **Invalid JSON**: Check the log files for detailed error messages
- **Disk Space**: Ensure you have enough space (files can be ~2GB total)

## Validation

After processing, verify your files:

```bash
# Check file validity
python -c "import json; json.load(open('data/fixed_grievance_v2.json')); print('Valid JSON!')"

# Check record count
python -c "import json; print(f'Records: {len(json.load(open(\"data/fixed_grievance_v2.json\")))}')"

# Check structure
python -c "import json; data=json.load(open('data/fixed_grievance_v2.json')); print(list(data[0].keys())[:10])"
```

## Integration with Dashboard

Once fixed, you can integrate these files with your FastAPI backend:

1. Update `backend/app/routers/charts.py` to load from the fixed JSON files
2. Create new endpoints for grievance and action history data
3. Add corresponding frontend components to visualize the data

## Troubleshooting

### Common Issues

1. **Out of Memory Error:**

   ```bash
   # Use streaming with smaller chunks
   python scripts/fix_json_streaming.py
   # Choose option 3, enter chunk size: 500
   ```

2. **Permission Denied:**

   ```bash
   chmod +x scripts/*.py
   ```

3. **Import Error:**

   ```bash
   # Make sure you're in the project root
   cd /path/to/cpgrams-trends
   python scripts/fix_json_streaming.py
   ```

4. **Disk Space Issues:**
   ```bash
   # Check available space
   df -h
   # Clean up if needed
   rm -f data/*.backup
   ```

## Performance Tips

- For files > 500MB, use `fix_json_streaming.py`
- Start with small chunk sizes (500-1000) and increase if stable
- Process files one at a time to avoid memory issues
- Consider using SSD storage for faster I/O

## Next Steps

After fixing the JSON files:

1. Integrate with your FastAPI backend
2. Create new chart components for the CPGrams data
3. Build analytics dashboards
4. Consider adding data filtering and search capabilities
