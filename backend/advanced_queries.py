from sqlalchemy import func
from app.database import SessionLocal
from app.models import User, Document, FormulaEntry

def report_user_documents():
    """
    Yêu cầu 1: Thống kê số lượng tài liệu mà mỗi người đã tải lên
    """
    db = SessionLocal()
    try:
        # Sử dụng outerjoin để lấy cả những user chưa tải lên tài liệu nào
        results = db.query(
            User.username_email,
            func.count(Document.id).label('doc_count')
        ).outerjoin(Document, User.user_id == Document.user_id)\
         .group_by(User.user_id).all()
        
        print("--- Thống kê số lượng tài liệu của người dùng ---")
        for username, count in results:
            print(f"Người dùng: {username} | Số tài liệu: {count}")
    finally:
        db.close()

def search_formulas_by_keyword(keyword: str):
    """
    Yêu cầu 2: Tìm kiếm tất cả FormulaEntry có chứa từ khóa trong latex_content
    """
    db = SessionLocal()
    try:
        # Sử dụng ilike để tìm kiếm không phân biệt hoa thường
        formulas = db.query(FormulaEntry).filter(
            FormulaEntry.latex_content.ilike(f'%{keyword}%')
        ).all()
        
        print(f"\n--- Kết quả tìm kiếm công thức cho từ khóa '{keyword}' ---")
        if not formulas:
            print("Không có kết quả nào phù hợp.")
        else:
            for formula in formulas:
                print(f"- ID: {formula.id}")
                print(f"  Document ID: {formula.document_id}")
                print(f"  LaTeX: {formula.latex_content}")
                print(f"  Order: {formula.order_index}\n")
        
        return formulas
    finally:
        db.close()

if __name__ == "__main__":
    # Test Yêu cầu 1
    report_user_documents()
    
    # Test Yêu cầu 2
    search_formulas_by_keyword("sqrt")
