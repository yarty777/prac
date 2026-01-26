# tests/unit_database.py
import sys
import types

def setup_unit_test_database():
    """
    Налаштовує фейкову базу даних ВИКЛЮЧНО для юніт-тестів.
    Не впливає на integration тести та розробку.
    """
    print("🧪 UNIT TEST MODE: Setting up FAKE database for unit tests")
    
    fake_db = types.ModuleType('unit_database')
    
    class FakeCollection:
        def __init__(self, name=""):
            self.name = name
            self.data = []
            print(f"   📁 Created UNIT fake collection: {name}")
        
        def insert_one(self, item):
            import random
            fake_id = f"unit_fake_{self.name}_{len(self.data)+1}"
            item_copy = item.copy()
            item_copy["_id"] = fake_id
            self.data.append(item_copy)
            
            print(f"   📝 UNIT {self.name}.insert_one: {item.get('email', item.get('text', 'new')[:15])}")
            return type("obj", (), {"inserted_id": fake_id})
        
        def find(self, query=None):
            if query is None:
                return [item.copy() for item in self.data]
            
            result = []
            for item in self.data:
                match = True
                for key, value in query.items():
                    if item.get(key) != value:
                        match = False
                        break
                if match:
                    result.append(item.copy())
            return result
        
        def find_one(self, query):
            for item in self.data:
                match = True
                for key, value in query.items():
                    if item.get(key) != value:
                        match = False
                        break
                if match:
                    return item.copy()
            return None
        
        def delete_many(self, query=None):
            if query is None:
                count = len(self.data)
                self.data.clear()
                return type("obj", (), {"deleted_count": count})
            
            initial = len(self.data)
            self.data = [item for item in self.data 
                       if not all(item.get(k) == v for k, v in query.items())]
            return type("obj", (), {"deleted_count": initial - len(self.data)})
    
    # Створюємо колекції
    fake_db.users_collection = FakeCollection("users")
    fake_db.quizzes_collection = FakeCollection("quizzes")
    fake_db.questions_collection = FakeCollection("questions")
    fake_db.results_collection = FakeCollection("results")
    
    # Підміняємо ТІЛЬКИ для юніт-тестів
    sys.modules['database'] = fake_db
    sys.modules['backend.database'] = fake_db
    
    print("✅ Unit test database setup complete")
    return fake_db