import sqlite3
import os

class MaterialDatabaseManager:
    def __init__(self, db_name="user_materials.db"):
        # Store the DB in a central location (e.g., user's home dir or app data folder)
        # For now, we'll put it in the current working directory
        self.db_path = db_name
        self.init_db()

    def init_db(self):
        """Creates the materials table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Define schema based on your JSON structure
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
                category TEXT,  -- e.g., 'Excavation', 'Concrete'
                UNIQUE(material_name, rate, rate_source) -- Prevent exact duplicates
            )
        ''')
        conn.commit()
        conn.close()

    def save_material(self, material_data, category="General"):
        """
        Inserts a material into the database.
        material_data: The dictionary found inside 'values' in your JSON.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR IGNORE INTO saved_materials (
                    material_name, 
                    unit, 
                    rate, 
                    rate_source, 
                    carbon_emission, 
                    carbon_source, 
                    carbon_unit, 
                    conversion_factor,
                    category
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                material_data.get('type'),
                material_data.get('unit_m3') or material_data.get('unit_A'), # Handle varied keys
                material_data.get('rate'),
                material_data.get('rate_data_source'),
                material_data.get('carbon_emission'),
                material_data.get('carbon_source'),
                material_data.get('carbon_unit'),
                material_data.get('conversion_factor'),
                category
            ))
            
            conn.commit()
            if cursor.rowcount > 0:
                print(f"✅ [DB] Saved material: {material_data.get('type')}")
            else:
                print(f"ℹ️ [DB] Skipped duplicate: {material_data.get('type')}")

        except sqlite3.Error as e:
            print(f"❌ [DB] Error saving material: {e}")
        finally:
            conn.close()