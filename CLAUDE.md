# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Alfred Workflow for BMI calculation. Takes height (and optionally weight) as input via Alfred and displays ideal weight ranges or BMI calculations.

## Architecture

### Single-file Python Script
- **Language**: Python 3.9.6 (system Python, no virtual environment)
- **Dependencies**: None (stdlib only)
- **Entry point**: `bmi_calculator.py`

### Alfred Script Filter Integration
This is an Alfred Workflow Script Filter that:
1. Receives input via `sys.argv[1:]` (passed from Alfred's `{query}`)
2. Outputs JSON to stdout in Alfred Script Filter format
3. Must output exactly one item in the `items` array
4. **Critical**: Never print anything to stdout except the final JSON (no debug prints, no intermediate output)

### Input/Output Contract

**Input patterns:**
- `(空入力)`
- `身長` (height in cm, e.g., `170`)
- `身長 体重` (height and weight space-separated, e.g., `170 65`)

**Output format (critical):**
```json
{
  "items": [
    {
      "title": "計算結果",
      "subtitle": "補足情報"
    }
  ]
}
```

Always return a single item with `title` and `subtitle`. Never return multiple items or empty arrays. All Japanese text uses UTF-8 encoding.

## Testing the Script

Test directly via command line:
```bash
# Test height only
python3 bmi_calculator.py "170"

# Test height + weight
python3 bmi_calculator.py "170 65"

# Test error handling
python3 bmi_calculator.py ""
python3 bmi_calculator.py "abc"
python3 bmi_calculator.py "170 65 80"
```

Output must be valid JSON that can be piped to `jq`:
```bash
python3 bmi_calculator.py "170 65" | jq .
```

## BMI Calculation Logic

### No input mode
Show usage instructions:
Display format:
- title: `"身長(cm) を入力してください"`
- subtitle: `"身長(cm) を入力してください"` <ー ここは変更しない

### Height-only mode
Calculate three weight thresholds:
- **理想体重** (Ideal): height(m)² × 22
- **痩せ体重** (Underweight): height(m)² × 18.5
- **肥満体重** (Obese): height(m)² × 25

Display format: 
- title: `"身長: Hcm, 痩せ: Xkg, 理想: Ykg, 肥満: Zkg"`
- subtitle: `"体重(kg) を入力してください"`

### Height + Weight mode
Calculate BMI and category:
- **BMI**: weight(kg) ÷ height(m)²
- **Categories** (日本肥満学会 standards):
  - < 18.5: 痩せ
  - 18.5-24.9: 標準
  - 25-29.9: 肥満(1度)
  - 30-34.9: 肥満(2度)
  - 35-39.9: 肥満(3度)
  - ≥ 40: 肥満(4度)

Display format:
- title: `"身長: Hcm, 体重: Wkg, BMI: X.X (カテゴリー)"`
- subtitle: `""`

## Error Handling Requirements

All errors must return valid JSON with helpful title/subtitle:
- Empty/no arguments: Show usage instructions
- Non-numeric input: Parse error message
- Invalid values (≤0 or >300cm for height, ≤0 or >500kg for weight): Validation error
- Too many arguments (>2): Usage error

**Critical**: Never allow exceptions to reach stdout - always catch and format as JSON. All error messages should be in Japanese.

## Alfred Workflow Configuration

When setting up in Alfred:
- **Keyword**: `bmi`
- **Script**: `python3 bmi_calculator.py "{query}"`
- **Language**: `/usr/bin/python3`

## Code Architecture

The script follows a simple functional structure:
- `create_output(title, subtitle)`: Formats Alfred JSON output with UTF-8 support
- `calculate_weights(height_cm)`: Returns ideal, underweight, and obese weights
- `calculate_bmi(height_cm, weight_kg)`: Returns BMI value and Japanese category
- `main()`: Handles input parsing, validation, routing, and error handling

All functions use descriptive English names but output Japanese text.

## Reference Documentation

- SPECIFICATION.md contains full functional requirements
- README.md contains installation instructions in Japanese
- [Alfred Script Filter docs](https://www.alfredapp.com/help/workflows/inputs/script-filter/json/)
