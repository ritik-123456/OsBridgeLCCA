import json
import os
import re
from PySide6.QtCore import QObject, Signal

# Define the directory where JSON files will be stored
DB_DIR = os.path.join(os.path.dirname(__file__), "sor_db")
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

class SORManager(QObject):
    # Signal emitted when the registry is refreshed (e.g., new file uploaded)
    registry_updated = Signal()

    def __init__(self):
        super().__init__()
        self.registry = {}  # { "India": { "Bihar SOR 2024": "path/to/file.json" } }
        self.current_data = [] # The currently loaded JSON content
        self.searcher = None   # Instance of AdvancedMaterialSearch
        self.refresh_registry()

    def refresh_registry(self):
        """Scans the sor_db folder and builds the registry."""
        self.registry = {}
        # Ensure directory exists before scanning
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
            
        for filename in os.listdir(DB_DIR):
            if filename.endswith(".json"):
                path = os.path.join(DB_DIR, filename)
                try:
                    with open(path, 'r') as f:
                        meta = json.load(f)
                        # We expect specific metadata keys in the JSON wrapper created by main_template.py
                        region = meta.get('metadata', {}).get('region', 'Unknown')
                        name = meta.get('metadata', {}).get('sor_name', filename)
                        
                        if region not in self.registry:
                            self.registry[region] = {}
                        self.registry[region][name] = path
                except Exception as e:
                    print(f"Error loading registry for {filename}: {e}")
        
        # Notify listeners (UI) that data availability has changed
        self.registry_updated.emit()

    def get_regions(self):
        """Returns a sorted list of available regions."""
        return sorted(list(self.registry.keys()))

    def get_sors_for_region(self, region):
        """Returns a sorted list of SOR names for a given region."""
        return sorted(list(self.registry.get(region, {}).keys()))

    def set_active_sor(self, region, sor_name):
        """Loads the selected JSON file into memory and initializes the searcher."""
        path = self.registry.get(region, {}).get(sor_name)
        if path:
            try:
                with open(path, 'r') as f:
                    full_content = json.load(f)
                    # The actual material list is inside the 'data' key based on the structure defined in main_template.py
                    self.current_data = full_content.get('data', [])
                    self.searcher = AdvancedMaterialSearch(self.current_data)
                    return True, f"Loaded {sor_name}"
            except Exception as e:
                return False, str(e)
        return False, "SOR not found"

class AdvancedMaterialSearch:
    def __init__(self, json_source):
        # 1. ROBUST INIT: Handle potential double-nested lists from JSON loads
        if isinstance(json_source, list) and len(json_source) > 0 and isinstance(json_source[0], list):
            self.json_data = json_source[0]
        else:
            self.json_data = json_source
            
        self.all_categories = []

    def _normalize_text(self, text):
        """
        Rule 1: Input Normalization
        - Converts to lowercase.
        - Removes special characters ((), -, /) using Regex.
        - Collapses multiple spaces.
        - Trims leading/trailing whitespace.
        """
        if not isinstance(text, str):
            return ""
        
        # 1. Lowercase
        text = text.lower()
        
        # 2. Remove special chars: Keep only alphanumeric, spaces, and dots (for decimals)
        text = re.sub(r'[^a-z0-9\s.]', ' ', text)
        
        # 3. Collapse multiple spaces into one and trim
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def getAllCategories(self):
        """Helper to retrieve available 'type' categories."""
        self.all_categories = []
        for item in self.json_data:
            if isinstance(item, dict):
                cat = item.get("type")
                if cat and cat not in self.all_categories:
                    self.all_categories.append(cat)
        return self.all_categories

    def performSearch(self, selected_categories, user_input):
        """
        Implements Rules 2 & 3: Tokenized Matching & Type-based Filtering.
        """
        results = []
        normalized_input = self._normalize_text(user_input)
        search_tokens = [t for t in normalized_input.split(" ") if t]

        if not search_tokens:
            return [] 

        for category_item in self.json_data:
            if not isinstance(category_item, dict): continue

            current_type = category_item.get("type", "").lower()
            
            # --- MODIFIED: Flexible Category Matching ---
            # Instead of strict equality, check if one of the selected categories
            # is a substring of the current type (or vice versa) to handle variations.
            match_category = False
            if not selected_categories:
                # If no specific categories provided, search everything
                match_category = True
            else:
                for sel in selected_categories:
                    if sel.lower() in current_type:
                        match_category = True
                        break
            
            if not match_category:
                continue

            data_list = category_item.get("data", [])
            for material in data_list:
                if not isinstance(material, dict): continue

                material_name = material.get("name", "")
                norm_mat_name = self._normalize_text(material_name)

                all_tokens_match = True
                for token in search_tokens:
                    if token not in norm_mat_name:
                        all_tokens_match = False
                        break
                
                if all_tokens_match:
                    results.append(material)

        return results

    # NEW FUNCTION: Get Detail By Name
    def getDetailByName(self, material_name):
        """
        Searches for an exact material by name (normalized).
        Returns the full dictionary if found, otherwise None.
        """
        # Normalize the input name so exact punctuation/case doesn't matter
        target_name_norm = self._normalize_text(material_name)
        
        for category_item in self.json_data:
            if not isinstance(category_item, dict): continue
            
            # Search through all items in this category
            data_list = category_item.get("data", [])
            for material in data_list:
                if not isinstance(material, dict): continue
                
                # Normalize the stored name to compare matches
                stored_name_norm = self._normalize_text(material.get("name", ""))
                
                # Check for exact match of the normalized strings
                if target_name_norm == stored_name_norm:
                    return material
        
        return None

# Initialize Singleton Manager
sor_manager = SORManager()

# Expose a default searcher proxy or instance
# Initially this might be None or empty until an SOR is selected via the GUI
searcher = sor_manager.searcher 

# For backwards compatibility if searcher is imported directly before selection, 
# we can initialize it with empty data.
if searcher is None:
    searcher = AdvancedMaterialSearch([])