import uuid
import datetime
import traceback
import sqlite3
import os
from .lifecycle_manager import LifecycleManager

class ProjectDataManager:
    def __init__(self):
        self.lifecycle = LifecycleManager()
        
        # Define the User Library DB path (creates it in the current directory)
        self.db_path = "user_materials.db"
        self._init_user_db()

    # --- DATABASE HELPER METHODS ---

    def _init_user_db(self):
        """Initializes the SQLite database for saved materials."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS saved_materials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    material_name TEXT NOT NULL,
                    unit TEXT,
                    rate REAL,
                    rate_source TEXT,
                    carbon_emission TEXT,
                    carbon_source TEXT,
                    carbon_unit TEXT,
                    conversion_factor TEXT,
                    category TEXT,
                    UNIQUE(material_name, rate, rate_source)
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ [DB Init Error]: {e}")

    def _save_to_user_library(self, material_values, category_tag):
        """
        Inserts a material into the local SQLite database if 'save_to_db' is True.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Map JSON keys to DB columns
            # We use .get() with defaults to handle potential missing keys safely
            cursor.execute('''
                INSERT OR IGNORE INTO saved_materials (
                    material_name, unit, rate, rate_source, 
                    carbon_emission, carbon_source, carbon_unit, 
                    conversion_factor, category
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                material_values.get('type') or material_values.get('material_name', 'Unknown'),
                material_values.get('unit_m3') or material_values.get('unit_A', ''),
                material_values.get('rate', 0),
                material_values.get('rate_data_source', ''),
                material_values.get('carbon_emission', ''),
                material_values.get('carbon_source', ''),
                material_values.get('carbon_unit', ''),
                material_values.get('conversion_factor', ''),
                category_tag
            ))
            
            conn.commit()
            if cursor.rowcount > 0:
                print(f"✅ [DB] Successfully saved '{material_values.get('type')}' to user library.")
            else:
                print(f"ℹ️ [DB] '{material_values.get('type')}' already exists in library.")
                
            conn.close()
        except Exception as e:
            print(f"❌ [DB Save Error]: {e}")

    # --- CORE METHODS ---

    def add_material_item(self, project_id, category, sub_category, material_data):
        try:
            # 1. Open the project (This loads from autosave.json if it exists)
            project_data = self.lifecycle.open_project(project_id)

            # 2. Ensure Schema Exists
            if "input_param" not in project_data: project_data["input_param"] = {}
            if category not in project_data["input_param"]: project_data["input_param"][category] = {}
            if sub_category not in project_data["input_param"][category]: project_data["input_param"][category][sub_category] = {}
            
            target_node = project_data["input_param"][category][sub_category]
            if "items" not in target_node: target_node["items"] = []

            # 3. Create the Record
            new_item = {
                "id": str(uuid.uuid4()),
                "values": material_data,
                "meta": {
                    "created_on": datetime.datetime.now().isoformat(),
                    "is_active": True
                }
            }

            # 4. Append
            target_node["items"].append(new_item)

            # 5. TRIGGER AUTOSAVE
            self.lifecycle.active_project_id = project_id 
            self.lifecycle.autosave(project_data)

            # 6. DATABASE SYNC (Added Logic)
            # If the user checked "Save to database", save it now.
            if material_data.get("save_to_db") is True:
                self._save_to_user_library(material_data, sub_category)

            return new_item["id"]

        except Exception as e:
            print(f"❌ Data Manager Error: {e}")
            return None
        
    def update_material_item(self, project_id, category, sub_category, item_id, updated_values):
        """
        Updates an existing material item.
        """
        if not project_id: return False

        try:
            project_data = self.lifecycle.open_project(project_id)
            
            # Safe Navigation
            try:
                items_list = project_data["input_param"][category][sub_category]["items"]
            except KeyError:
                print(f"❌ Error: Path {category}/{sub_category}/items not found.")
                return False
            
            for item in items_list:
                if item["id"] == item_id:
                    # Update values
                    item["values"].update(updated_values)
                    item["meta"]["modified_on"] = datetime.datetime.now().isoformat()
                    
                    # Save immediately
                    self.lifecycle.active_project_id = project_id
                    self.lifecycle.autosave(project_data)
                    print(f"✅ Item {item_id} updated.")

                    # DATABASE SYNC (Added Logic)
                    # Check if the updated item should be saved to the library
                    if item["values"].get("save_to_db") is True:
                        self._save_to_user_library(item["values"], sub_category)

                    return True
            
            print(f"⚠️ Item {item_id} not found.")
            return False

        except Exception as e:
            print(f"❌ Update Error: {e}")
            return False

    def get_all_materials(self, project_id, category, sub_category):
        """Helper to populate UI tables."""
        if not project_id: return []
        
        try:
            project_data = self.lifecycle.open_project(project_id)
            return project_data.get("input_param", {}).get(category, {}).get(sub_category, {}).get("items", [])
        except Exception:
            return []
        
    def delete_material_item(self, project_id, category, sub_category, item_id):
        """
        Deletes a material item by ID from autosave.json.
        """
        if not project_id: return False

        try:
            # 1. Open Project
            project_data = self.lifecycle.open_project(project_id)
            
            # 2. Navigate to the list
            try:
                target_node = project_data["input_param"][category][sub_category]
                items_list = target_node.get("items", [])
            except KeyError:
                print(f"⚠️ Path {category}/{sub_category} not found. Nothing to delete.")
                return False

            # 3. Filter out the item to delete
            initial_count = len(items_list)
            # Keep only items that DO NOT match the item_id
            target_node["items"] = [item for item in items_list if item["id"] != item_id]

            # 4. Save if a change occurred
            if len(target_node["items"]) < initial_count:
                self.lifecycle.active_project_id = project_id
                self.lifecycle.autosave(project_data)
                print(f"🗑️ Item {item_id} deleted from autosave.json.")
                return True
            else:
                print(f"⚠️ Item {item_id} not found for deletion.")
                return False

        except Exception as e:
            print(f"❌ Delete Error: {e}")
            return False