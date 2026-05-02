import json
from app.database import SessionLocal
from app.models import Document, FormulaEntry

def seed_formulas_from_json():
    db = SessionLocal()
    try:
        # Lấy một tài liệu ngẫu nhiên hoặc tài liệu đầu tiên làm mẫu để gán formula
        document = db.query(Document).first()
        if not document:
            print("Chưa có tài liệu nào trong database. Vui lòng chạy seed_faker.py trước!")
            return

        print(f"Sẽ nạp dữ liệu công thức cho tài liệu ID: {document.id}")

        with open('data.json', 'r', encoding='utf-8') as f:
            formulas = json.load(f)

        for index, item in enumerate(formulas):
            entry = FormulaEntry(
                document_id=document.id,
                latex_content=item['latex'],
                order_index=index + 1
            )
            db.add(entry)

        db.commit()
        print(f"Seeding hoàn tất! Đã nạp thành công {len(formulas)} công thức từ tệp data.json.")
    except Exception as e:
        db.rollback()
        print(f"Lỗi xảy ra trong quá trình đọc từ tệp json: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_formulas_from_json()
