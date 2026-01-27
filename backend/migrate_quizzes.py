# fix.py
print("🚀 Починаємо...")

try:
    from database import quizzes_collection, users_collection
    print("✅ База даних підключена")
    
    # 1. Знайти або створити викладача
    teacher = users_collection.find_one({"role": "teacher"})
    
    if not teacher:
        print("❌ Не знайдено викладача!")
        print("📋 Існуючі користувачі:")
        for user in users_collection.find():
            print(f"  - {user['email']} ({user.get('role', 'no role')})")
    else:
        print(f"✅ Викладач: {teacher['email']} (ID: {teacher['_id']})")
        
        # 2. Перевірити тести
        total = quizzes_collection.count_documents({})
        print(f"📊 Всього тестів: {total}")
        
        # 3. Додати author_id до тестів без нього
        result = quizzes_collection.update_many(
            {"author_id": {"$exists": False}},
            {"$set": {"author_id": str(teacher["_id"])}}
        )
        print(f"✅ Оновлено тестів: {result.modified_count}")
        
except Exception as e:
    print(f"💥 Критична помилка: {e}")
    import traceback
    traceback.print_exc()

input("\nНатисни Enter для виходу...")