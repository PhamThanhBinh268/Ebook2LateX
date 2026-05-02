import random
from faker import Faker
from app.database import SessionLocal
from app.models import User, Document

fake = Faker()

def seed_users_and_documents():
    db = SessionLocal()
    try:
        print("Đang tạo 50 người dùng...")
        for _ in range(50):
            # Tạo người dùng
            user = User(
                username_email=fake.unique.email(),
                full_name=fake.name(),
                password_hash="hashed_dummy_password", # Mật khẩu giả
                role=random.choice(['Admin', 'Editor', 'Viewer']),
                is_active=True
            )
            db.add(user)
            db.flush() # Để lấy user_id ngay lập tức mà chưa cần commit chốt danh sách

            # Tạo 2-5 tài liệu cho mỗi người dùng
            num_docs = random.randint(2, 5)
            for _ in range(num_docs):
                doc = Document(
                    user_id=user.user_id,
                    file_name=fake.file_name(extension="pdf"),
                    file_path_url=fake.url(),
                    status=random.choice(['Pending', 'Processed', 'Error'])
                )
                db.add(doc)

        db.commit()
        print("Seeding hoàn tất! Đã tạo 50 người dùng cùng với các tài liệu mẫu.")
    except Exception as e:
        db.rollback()
        print(f"Lỗi xảy ra trong quá trình seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_users_and_documents()
