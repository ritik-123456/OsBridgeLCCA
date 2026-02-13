import os
import json
import uuid
import datetime
import platform
import hashlib
import shutil
from PySide6.QtCore import QObject, Signal
from .database import DatabaseManager

# Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECTS_ROOT = os.path.join(BASE_DIR, "projects")
DB_PATH = os.path.join(PROJECTS_ROOT, "project_manager.db")

class ProjectCreator(QObject):
    # Signals
    projectCreated = Signal(str)
    errorOccurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager(DB_PATH)

    # --- Helper: Hashing (Restored from your code) ---
    def _calculate_file_hash(self, file_path):
        if not os.path.exists(file_path):
            return None
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    # --- Helper: System Info (Restored from your code) ---
    def _get_sys_info(self):
        return {
            "os": platform.system(),
            "architecture": platform.machine(),
            "app_version": "1.0.0" 
        }

    def create_new_project(self, form_data):
        try:
            # 1. Generate UUID and Time
            project_uuid = str(uuid.uuid4())
            timestamp = datetime.datetime.now().isoformat()
            
            # 2. Setup Directories
            project_folder = os.path.join(PROJECTS_ROOT, project_uuid)
            temp_folder = os.path.join(project_folder, "temp")
            os.makedirs(temp_folder, exist_ok=True)

            # Define Paths
            meta_path = os.path.join(project_folder, "meta_data.json")
            main_path = os.path.join(project_folder, "main_file.json")
            temp_path = os.path.join(temp_folder, "autosave.json")

            # 3. Create meta_data.json
            sys_info = self._get_sys_info()
            meta_data = {
                "id": project_uuid,
                "name": form_data['project_title'],
                "status": "draft",
                "user_name": os.getlogin(),
                "sys_info": sys_info,
                "created_on": timestamp,
                "version": 1
            }
            with open(meta_path, 'w') as f:
                json.dump(meta_data, f, indent=4)

            # 4. Create Main Content JSON
            project_content = {
                "general_info": {
                    "project_id": project_uuid,
                    "project_name": form_data['project_title'],
                    "company_name": form_data['company_name'],
                    "description": form_data['description'],
                    "valuer": form_data['valuer'],
                    "job_number": form_data['job_number'],
                    "client": form_data['client'],
                    "country": form_data.get('country', ''),
                    "region": form_data.get('region', ''),
                    "sor": form_data.get('sor', ''),
                    "base_year": form_data['base_year'],
                    "currency": form_data.get('currency', 'INR'),
                    "created_on": timestamp,
                    "modified_on": timestamp,
                    "version": 1
                },
                "input_param": {  },
                "Financial": {  } ,
                "Maintenace_repair":{  },
                "Carbon_emission":{  },
                "Bridge_and_traffic":{  },
                "Demolition_and_recycling":{  }
            }

            # 5. Write Main File
            with open(main_path, 'w') as f:
                json.dump(project_content, f, indent=4)
                
            # 6. Create Autosave (Copy Main -> Temp)
            # Using copy2 preserves metadata, safer than writing twice
            shutil.copy2(main_path, temp_path)

            # 7. Calculate Hash
            file_hash = self._calculate_file_hash(main_path)

            # 8. Insert into Database
            db_record = {
                "id": project_uuid,
                "name": form_data['project_title'],
                "main_path": main_path,
                "temp_path": temp_path,
                "status": "draft",
                "hash_key": file_hash,  # Added Hashing
                "user_name": os.getlogin(),
                "sys_info": json.dumps(sys_info),
                "created_on": timestamp,
                "modified_on": timestamp,
                "last_opened": timestamp, # Added Last Opened
                "version": 1
            }
            self.db.insert_project(db_record)

            self.projectCreated.emit(project_uuid)

        except Exception as e:
            # Print full trace for debugging if needed
            import traceback
            traceback.print_exc()
            self.errorOccurred.emit(str(e))