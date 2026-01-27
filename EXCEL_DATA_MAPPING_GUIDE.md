# Excel Data Mapping Guide

## Overview
This document describes how Excel data is parsed and mapped into the GUI widgets (Foundation, SubStructure, SuperStructure, AuxiliaryWorks).

---

## 1. EXCEL PARSER FLOW (in main_template.py)

### Function: `parse_and_validate_excel(file_path)`

**Input:** Excel file with multiple sheets

**Process:**
1. Reads all sheets from Excel file
2. Identifies headers (looks for 'CID#' or keywords like 'unit_a', 'rate')
3. Identifies sections (single cell rows = component names)
4. Extracts data rows with proper field mapping
5. Validates and applies defaults for missing values

**Output Structure:**
```python
{
    "validation_report": {
        "errors": [...],
        "warnings": [...]
    },
    "parsed_data": [
        {
            "sheetName": "Foundation",
            "type": "Excavation",  # Component name
            "data": [
                {
                    "name": "Material Name",
                    "quantity": "100",
                    "unit": "cum",
                    "rate": "500.00",
                    "rate_src": "SOR 2024",
                    "carbon_emission": "50.5",
                    "carbon_emission_units": "kgCO2e",
                    "conversion_factor": "2.5",
                    "carbon_emission_src": "IPCC",
                    "recycleable": "Recyclable"
                },
                ...
            ]
        },
        ...
    ]
}
```

---

## 2. EXCEL HEADER MAPPING

The parser converts various Excel header formats to canonical field names:

| Excel Header Examples | Canonical Key | GUI Field |
|---|---|---|
| Type of Material, Material, Item, Description, Particulars, Name | `name` | Material Name |
| Rate Source, Source, Rate Src, Rate Data Source | `rate_src` | Rate Data Source |
| Carbon Emission, Emission, Carbon Emission (kgCO2e/Unit_B) | `carbon_emission` | Carbon Emission |
| Carbon Unit, Emission Unit, Carbon Emission Units | `carbon_emission_units` | Carbon Units |
| Carbon Source, Emission Source, Carbon Factor Source | `carbon_emission_src` | Carbon Source |
| Recyclable, Recycleable | `recycleable` | Recyclable Checkbox |
| Unit, Unit_A | `unit` | Unit Dropdown |
| Quantity, Quantity (Unit_A) | `quantity` | Quantity Field |
| Rate, Rupees/Unit_A | `rate` | Rate Field |
| Conversion Factor (Unit_A → Unit_B) | `conversion_factor` | Conversion Factor Field |

---

## 3. DATA VALIDATION & DEFAULTS

When parsing Excel data, the parser applies intelligent defaults:

| Field | Validation | Default |
|---|---|---|
| **name** | REQUIRED - cannot be empty | SKIP ROW |
| **quantity** | Must be valid number | "1" |
| **unit** | Must match DROPDOWN_UNITS | "cum" |
| **rate** | Must be valid number | "0" |
| **rate_src** | Text field | "Excel Import" |
| **carbon_emission** | Valid number OR "NA" | "not_available" |
| **carbon_emission_units** | Text field | "kgCO2e" |
| **conversion_factor** | Valid number OR "NA" | "not_available" |
| **carbon_emission_src** | Text field | "" (empty) |
| **recycleable** | "Recyclable" / "Non-recyclable" | "Non-recyclable" |

**Valid Unit Values (DROPDOWN_UNITS):**
- `cum` (cubic meter)
- `rmt` (running meter)
- `m2` (square meter)
- `mt` (metric ton)

---

## 4. DATA DISTRIBUTION FLOW

### Step 1: Group by Widget Type
```python
distribute_imported_data(parsed_data)
```

Maps sheet names to widget keys:
- "foundation" → KEY_FOUNDATION
- "sub structure", "sub-structure", "substructure" → KEY_SUBSTRUCTURE
- "super structure", "super-structure", "superstructure" → KEY_SUPERSTRUCTURE
- "auxiliary works", "auxiliary" → KEY_AUXILIARY

### Step 2: Route to Correct Widget
If tabs are active: Route to the tab widget
If single view: Route to the currently visible widget

### Step 3: Call load_from_excel_sections()
Each widget processes the grouped sections

---

## 5. WIDGET-LEVEL MAPPING (Load into GUI)

### Method: `load_from_excel_sections(sections_data)`

Implemented in:
- [foundation_widget.py](foundation_widget.py#L1567) - Foundation widget
- [sub_structure_widget.py](sub_structure_widget.py) - SubStructure widget  
- [super_structure_widget.py](super_structure_widget.py) - SuperStructure widget
- [auxiliary_works_widget.py](auxiliary_works_widget.py) - AuxiliaryWorks widget

**Process:**
1. **Create Component**: Add new component layout for each section
2. **Set Component Type**: Set dropdown to section's component name (e.g., "Excavation", "Concrete")
3. **Clear Rows**: Remove placeholder rows
4. **Map Each Row**: Convert Excel fields → GUI field structure
5. **Add to Grid**: Insert mapped data into material grid

**Mapping Structure:**
```python
mapped_data = {
    KEY_TYPE: material_name,                    # str: Material name/type
    KEY_QUANTITY: quantity_str,                 # str: Quantity in Unit_A
    KEY_UNIT_M3: unit_val,                      # str: Unit of measurement
    KEY_RATE: rate_str,                         # str: Price per unit
    KEY_RATE_DATA_SOURCE: rate_source,          # str: Rate source
    "carbon_emission": carbon_emission_str,      # str: Carbon emission value
    "carbon_unit": carbon_units,                 # str: Carbon units
    "conversion_factor": conversion_factor_str,  # str: Unit_A → Unit_B conversion
    "carbon_source": carbon_source,              # str: Carbon source
    "recyclable": is_recyclable,                 # bool: Is recyclable
    "save_to_db": False,                         # bool: Don't auto-save to DB
    "is_custom": True                            # bool: Mark as custom data
}
```

---

## 6. DATA FLOW DIAGRAM

```
Excel File
    ↓
parse_and_validate_excel()
    ↓
Result: parsed_data (sections with rows)
    ↓
distribute_imported_data()
    ├─ Group by widget type (Foundation, SubStructure, etc.)
    └─ Route to correct widget
        ↓
    load_from_excel_sections() in each widget
        ├─ For each section:
        │  ├─ Create component layout
        │  ├─ Set component name in dropdown
        │  ├─ Clear placeholder rows
        │  └─ For each row:
        │     ├─ Map Excel fields → GUI fields
        │     └─ Add to material grid
        └─ Mark state as changed
        
GUI displays data in material grid
User can view, edit, save
```

---

## 7. ERROR HANDLING

**Parser Logs:**
- `[SKIP]` - Section skipped (no component name)
- `[WARN]` - Warning logged (missing field, using default)
- `[INFO]` - Informational message (default applied)
- `[ERROR]` - Error processing row (skipped)
- `✓` - Successful operation

**Row Skipping:**
- Missing material name → ROW SKIPPED
- Invalid quantity → Use default "1"
- Missing unit → Use default "cum"
- Invalid rate → Use default "0"

---

## 8. EXAMPLE: Complete Flow

### Input Excel Sheet: "Foundation"

| Type of Material | Quantity | Unit | Rate | Rate Source | Carbon Emission | Carbon Units |
|---|---|---|---|---|---|---|
| Excavation | 100 | cum | 500 | SOR 2024 | 25.5 | kgCO2e |
| Concrete | 50 | cum | 2500 | SOR 2024 | 120 | kgCO2e |

### Parse Output:
```python
{
    "sheetName": "Foundation",
    "type": "Excavation",
    "data": [
        {
            "name": "Excavation",
            "quantity": "100",
            "unit": "cum",
            "rate": "500",
            "rate_src": "SOR 2024",
            "carbon_emission": "25.5",
            "carbon_emission_units": "kgCO2e",
            "conversion_factor": "not_available",
            "carbon_emission_src": "",
            "recycleable": "Non-recyclable"
        },
        {
            "name": "Concrete",
            "quantity": "50",
            "unit": "cum",
            "rate": "2500",
            "rate_src": "SOR 2024",
            "carbon_emission": "120",
            "carbon_emission_units": "kgCO2e",
            "conversion_factor": "not_available",
            "carbon_emission_src": "",
            "recycleable": "Non-recyclable"
        }
    ]
}
```

### GUI Output:
Foundation widget displays:
- **Component:** Excavation
- **Row 1:** Excavation | 100 | cum | 500 | SOR 2024
- **Row 2:** Concrete | 50 | cum | 2500 | SOR 2024

---

## 9. CONSTANTS REFERENCE

All KEY_* constants are defined in [widgets/utils/data.py](widgets/utils/data.py):

```python
# Structure Works Keys
KEY_FOUNDATION = "Foundation"
KEY_SUBSTRUCTURE = "Sub-Structure"
KEY_SUPERSTRUCTURE = "Super-Structure"
KEY_AUXILIARY = "Miscellaneous"

# Material Field Keys
KEY_TYPE = "type"
KEY_QUANTITY = "quantity"
KEY_UNIT_M3 = "unit_m3"
KEY_RATE = "rate"
KEY_RATE_DATA_SOURCE = "rate_data_source"
KEY_COMPONENT = "component"
KEY_GRADE = "grade"
```

---

## 10. IMPORTANT NOTES

✅ **Correct Practices:**
- Excel headers are flexible (many variations supported)
- Missing optional fields get sensible defaults
- Quantity defaults to 1 for SOR items
- Rate defaults to 0 if missing
- Carbon emission defaults to "not_available"
- All data is validated before display

⚠️ **Required Fields:**
- Material name (`name`) - MANDATORY, row skipped if missing
- Component name in section header - MANDATORY

📝 **Comments in Code:**
- `#ritik - START:` marks the beginning of mapping logic
- `#ritik - END:` marks the end of mapping logic
- `# ritik:` inline comments explain specific mapping steps

---

## 11. TROUBLESHOOTING

**Issue:** Data not appearing in GUI
- Check console for `[SKIP]` messages
- Verify material names are not empty
- Confirm sheet name matches Foundation/SubStructure/etc.

**Issue:** Wrong units displayed
- Check Excel unit column matches DROPDOWN_UNITS: cum, rmt, m2, mt
- Invalid units default to "cum"

**Issue:** Missing data fields
- Optional fields (carbon, conversion factor) default to "not_available"
- Non-optional fields (name, quantity, rate) use sensible defaults
- Check validation report for warnings

**Issue:** Values showing as 0 or 1
- Quantity defaults to "1" if invalid
- Rate defaults to "0" if invalid
- Check Excel for non-numeric values in quantity/rate columns

---

## 12. TESTING CHECKLIST

- [ ] Excel file has headers with 'CID#' or 'unit', 'rate' keywords
- [ ] Component names (e.g., "Excavation") in single-cell rows
- [ ] Material names are not empty
- [ ] Units match DROPDOWN_UNITS (cum, rmt, m2, mt)
- [ ] Rates are numeric (no text except decimals)
- [ ] Sheet names match widget types (Foundation, Sub-Structure, etc.)
- [ ] Carbon fields are optional (can be "NA" or numeric)
- [ ] Data appears in correct widget after import
- [ ] Material grid rows display correctly
- [ ] Recyclable checkbox state matches Excel data

