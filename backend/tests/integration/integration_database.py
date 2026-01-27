# tests/integration/integration_database.py
"""
Окрема фейкова база даних ТІЛЬКИ для integration тестів.
Не впливає на unit тести та розробку.
"""

import sys
import types

def setup_integration_database():
    """
    Підміняє реальну базу на фейкову ТІЛЬКИ для integration тестів.
    Викликається в conftest.py перед імпортом app.
    """
    print("🧪 INTEGRATION TEST MODE: Setting up FAKE database")
    
    # Створюємо новий модуль
    fake_db = types.ModuleType('integration_database')
    
    class FakeCollection:
        def __init__(self, name="collection"):
            self.name = name
            self.data = []
            print(f"   📁 Created integration fake collection: {name}")
        
        def insert_one(self, document):
            import random
            doc_id = f"integration_fake_{self.name}_{len(self.data)+1}"
            if "_id" not in document:
                document["_id"] = doc_id
            
            # Копіюємо документ щоб не змінювати оригінал
            doc_copy = document.copy()
            doc_copy["_id"] = doc_id
            self.data.append(doc_copy)
            
            print(f"   📝 Integration {self.name}.insert_one: {document.get('email', 'no email')}")
            return type('obj', (), {'inserted_id': doc_id})
        
        def find(self, filter=None):
            if filter is None:
                return [item.copy() for item in self.data]
            
            # Фільтрація
            result = []
            for item in self.data:
                match = True
                for key, value in filter.items():
                    if item.get(key) != value:
                        match = False
                        break
                if match:
                    result.append(item.copy())
            return result
        
        def find_one(self, filter):
            for item in self.data:
                match = True
                for key, value in filter.items():
                    if item.get(key) != value:
                        match = False
                        break
                if match:
                    return item.copy()
            return None
        
        def update_one(self, filter, update):
            item = self.find_one(filter)
            if item:
                if "$set" in update:
                    # Шукаємо оригінал в data
                    for i, orig_item in enumerate(self.data):
                        if all(orig_item.get(k) == v for k, v in filter.items()):
                            self.data[i].update(update["$set"])
                            break
                return type('obj', (), {'matched_count': 1, 'modified_count': 1})
            return type('obj', (), {'matched_count': 0, 'modified_count': 0})
        
        def delete_one(self, filter):
            for i, item in enumerate(self.data):
                match = True
                for key, value in filter.items():
                    if item.get(key) != value:
                        match = False
                        break
                if match:
                    del self.data[i]
                    return type('obj', (), {'deleted_count': 1})
            return type('obj', (), {'deleted_count': 0})
        
        def delete_many(self, filter=None):
            if filter is None:
                count = len(self.data)
                self.data.clear()
                return type('obj', (), {'deleted_count': count})
            
            # Фільтроване видалення
            initial = len(self.data)
            self.data = [item for item in self.data 
                        if not all(item.get(k) == v for k, v in filter.items())]
            return type('obj', (), {'deleted_count': initial - len(self.data)})
        
        def count_documents(self, filter={}):
            return len(self.find(filter))
    
    # Створюємо всі колекції
    fake_db.users_collection = FakeCollection("users")
    fake_db.quizzes_collection = FakeCollection("quizzes")
    fake_db.questions_collection = FakeCollection("questions")
    fake_db.results_collection = FakeCollection("results")
    
    # Додаткові атрибути для сумісності
    fake_db.client = None
    fake_db.db = None
    
    # Підміняємо оригінальний модуль database
    sys.modules['database'] = fake_db
    sys.modules['backend.database'] = fake_db
    
    print("✅ Integration fake database setup complete")
    return fake_db