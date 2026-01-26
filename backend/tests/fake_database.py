import sys
import types

fake_db = types.ModuleType('database')

class FakeCollection:
    def insert_one(self, x): return type('obj', (), {'inserted_id': 'fake'})
    def find(self, *a, **k): return []
    def find_one(self, *a, **k): return None
    def update_one(self, *a, **k): return type('obj', (), {'matched_count': 0})
    def delete_many(self, *a, **k): return type('obj', (), {'deleted_count': 0})

fake_db.quizzes_collection = FakeCollection()
fake_db.questions_collection = FakeCollection()
fake_db.results_collection = FakeCollection()
fake_db.users_collection = FakeCollection()

# Підміняємо реальну базу
sys.modules['database'] = fake_db
sys.modules['backend.database'] = fake_db