# QUICK REFERENCE: Excel Data Mapping

## 🚀 Quick Start

### 1. What Happens When You Upload Excel?

```
File Upload → Parse → Validate → Save DB → Distribute → Display in GUI
```

---

## 📊 Excel Format Requirements

### Sheet Names (Case Insensitive)
- `Foundation` → Foundation widget
- `Sub-Structure` → SubStructure widget
- `Super-Structure` → SuperStructure widget
- `Auxiliary Works` → AuxiliaryWorks widget

### Required Headers
| Column | Purpose | Example |
|--------|---------|---------|
| Type of Material | Material name | "Manual Excavation" |
| Quantity | How much | "100" |
| Unit | Unit type | "cum", "rmt", "m2", "mt" |
| Rate | Price per unit | "500.00" |
| Rate Source | Where rate came from | "SOR 2024" |

### Optional Headers
| Column | Purpose | Example |
|--------|---------|---------|
| Carbon Emission | CO2 per unit | "50.5" |
| Carbon Units | Carbon unit type | "kgCO2e" |
| Conversion Factor | Unit conversion | "2.5" |
| Carbon Source | Where carbon came from | "IPCC" |
| Recyclable | Is it recyclable? | "Yes" / "No" |

---

## 📋 Data Row Example

```
Type of Material | Quantity | Unit | Rate   | Rate Source | Carbon Emission | Carbon Units
Excavation       | 100      | cum  | 500.00 | SOR 2024    | 25.5            | kgCO2e
Concrete         | 50       | cum  | 2500   | SOR 2024    | 120             | kgCO2e
```

---

## 🎯 What Happens to Your Data

### Input Processing
```
Excel Column "Type of Material" 
         ↓
Parser normalizes to "name"
         ↓
Validates: Not empty → YES ✓
         ↓
Maps to GUI field: Material Type
```

### Output to GUI
```
Material Grid Row:
[Excavation | 100 | cum | 500.00 | SOR 2024 | 25.5 | ...]
```

---

## ✅ Valid Values

### Units (Dropdown)
- **cum** - Cubic Meter
- **rmt** - Running Meter  
- **m2** - Square Meter
- **mt** - Metric Ton

### Recyclable
- **Recyclable** or **Yes** → Checkbox CHECKED
- **Non-recyclable** or **No** → Checkbox UNCHECKED

### Carbon Fields
- **Numeric value** → Used as-is (e.g., "50.5")
- **"NA", "N/A", "not available"** → Set to "not_available"
- **Empty** → Set to "not_available"

---

## 🔧 Default Values Applied

If field is missing/invalid:

| Field | Default | When Applied |
|-------|---------|--------------|
| Quantity | "1" | Invalid number or missing |
| Unit | "cum" | Invalid/missing |
| Rate | "0" | Invalid number or missing |
| Rate Source | "Excel Import" | Missing |
| Carbon Emission | "not_available" | Invalid/missing |
| Carbon Units | "kgCO2e" | Missing |
| Conversion Factor | "not_available" | Invalid/missing |
| Carbon Source | "" | Missing |
| Recyclable | False | Missing |

⚠️ **Special Case:** If Material Name is missing → **ENTIRE ROW SKIPPED**

---

## 📝 Console Messages Explained

```
[EXCEL IMPORT] Loading 2 section(s) into Foundation widget
  = Parsing started, 2 sections found

[SECTION 0] Sheet: Foundation, Component: Excavation, Rows: 2
  = Processing section 0: Component "Excavation" with 2 data rows

✓ Set component to: Excavation
  = Component dropdown successfully set

✓ Row 0: Added 'Manual Excavation' [100 cum @ SOR 2024]
  = Row 0 successfully added to grid

[INFO] Row 1: Invalid quantity '?', using default '1'
  = Row 1 had invalid quantity, defaulted to "1"

[WARN] Row 2: Missing material name, skipping
  = Row 2 has no material name, entire row skipped

[ERROR] Row 3: Failed to process - [error details]
  = Row 3 had exception, skipped

[EXCEL IMPORT] Complete. All sections loaded.
  = Import finished successfully
```

---

## 🛠️ How to Use

### Step 1: Prepare Excel
```
1. Open Excel
2. Create sheet named "Foundation"
3. Add headers in row 1
4. Add component name in first data row (single cell)
5. Add material data in following rows
6. Save as .xlsx
```

### Step 2: Upload
```
1. Click "Upload Excel" button
2. Select your .xlsx file
3. Enter Region (e.g., "India")
4. Enter SOR Name (e.g., "Bihar 2024")
5. Click OK
```

### Step 3: Verify
```
1. Check console for any [ERROR] or [WARN]
2. Look at widget - data should appear in grid
3. Each row shows: Material | Qty | Unit | Rate | Source
```

### Step 4: Save
```
1. Click "Save" or "Next"
2. Data persists to database
```

---

## ❌ Common Issues

### Problem: Data not appearing
**Check:**
- [ ] Sheet name matches (Foundation, Sub-Structure, etc.)
- [ ] Material name is not empty
- [ ] Check console for `[SKIP]` or `[WARN]` messages

### Problem: Wrong quantity/rate showing
**Check:**
- [ ] Quantity/Rate column has numeric values
- [ ] Check console for `[INFO]` messages about defaults

### Problem: Wrong unit showing
**Check:**
- [ ] Unit value is one of: cum, rmt, m2, mt
- [ ] Unit column is not empty

### Problem: Recyclable checkbox wrong
**Check:**
- [ ] Column says "Recyclable" or "Recycleable"
- [ ] Value is "Recyclable", "Recycleable", "Yes", or "No"

---

## 🔍 Fields Mapping Reference

### Parser → GUI Mapping

```python
# Parsed Data (from Excel)
{
    "name": "Excavation",              # Material name
    "quantity": "100",                 # Quantity
    "unit": "cum",                     # Unit
    "rate": "500",                     # Rate/Price
    "rate_src": "SOR 2024",           # Rate source
    "carbon_emission": "25.5",         # Carbon emission
    "carbon_emission_units": "kgCO2e", # Carbon units
    "conversion_factor": "2.5",        # Conversion factor
    "carbon_emission_src": "IPCC",     # Carbon source
    "recycleable": "Recyclable"        # Recyclable status
}
        ↓ (Maps to)
# GUI Data (in widget)
{
    KEY_TYPE: "Excavation",
    KEY_QUANTITY: "100",
    KEY_UNIT_M3: "cum",
    KEY_RATE: "500",
    KEY_RATE_DATA_SOURCE: "SOR 2024",
    "carbon_emission": "25.5",
    "carbon_unit": "kgCO2e",
    "conversion_factor": "2.5",
    "carbon_source": "IPCC",
    "recyclable": True
}
        ↓ (Displays as)
# GUI Row
[Excavation | 100 | cum | 500 | SOR 2024 | ...]
```

---

## 📍 Where Everything Is

| What | Where |
|-----|-------|
| Excel Parser | main_template.py (lines 60-230) |
| Data Distributor | main_template.py (lines 420-450) |
| Foundation Loader | foundation_widget.py (lines 1567+) |
| SubStructure Loader | sub_structure_widget.py (lines 1435+) |
| SuperStructure Loader | super_structure_widget.py (lines 1435+) |
| Auxiliary Loader | auxiliary_works_widget.py (lines 1467+) |
| Constants | widgets/utils/data.py |

---

## 🎓 Understanding the Code

### Key Functions:

**parse_and_validate_excel(file_path)**
- Reads Excel, extracts structured data
- Returns: parsed_data with validation_report

**distribute_imported_data(parsed_data)**
- Routes data to correct widgets
- Calls: widget.load_from_excel_sections()

**widget.load_from_excel_sections(sections_data)**
- Displays data in widget
- Creates component layouts
- Adds rows to material grid

---

## 💡 Pro Tips

1. **Use SOR 2024 format name:** "Region_Name_Year" for clarity
2. **Include Rate Source:** Helps track data origin
3. **Test small file first:** Before uploading large Excel
4. **Check console:** Always look for warnings
5. **Save after import:** Don't lose imported data

---

## 📞 Need Help?

**See detailed docs:**
- `COMPREHENSIVE_MAPPING_IMPLEMENTATION.md` - Full system overview
- `EXCEL_DATA_MAPPING_GUIDE.md` - Detailed flow and examples
- `DATA_MAPPING_SUMMARY.md` - Implementation summary

**Check code comments:**
- Look for `#Ritik - START:` and `#Ritik - END:` markers
- Inline comments marked with `# ritik:` explain each step

---

## ✨ Summary

✅ Upload Excel → Parsed & Validated → Saved to DB → Displayed in GUI  
✅ Flexible headers → Intelligent defaults → Error tolerant → Well logged  
✅ All 4 widgets supported → Full field mapping → Production ready

**Status: COMPLETE ✅**

