# Bản sửa bài kiểm tra N13

Bản Word đã sửa: `../ban_da_sua/N13 Lê Việt Hoàng B23DCKH044.docx`.
Bản gốc được giữ nguyên vì đang mở trong Word.

- `revise_sources.py`: sinh 16 lớp Java và cập nhật DDL gồm 7 bảng.
- `revise_diagrams.py`: vẽ 8 hình UML đen trắng từ cùng danh mục lớp.
- `revise_report.py`: dựng đủ 5 câu và toàn bộ mã lớp Java.
- `run_pipeline.py`: dựng lại hình và bản Word đã sửa, không tạo bản N12.
- `revision_manifest.json`: danh mục lớp dùng khi dựng hình.

Chạy bằng Python của Codex primary runtime với python-docx và Pillow.
Các công cụ gen_*.py và build_assignment_docx.py là phiên bản cũ;
dùng run_pipeline.py cho bản đã sửa.

Mã nguồn tại ../src; DDL tại ../qltc_database.sql; CSDL tên qltc_db.
Khóa ngoại dùng RESTRICT; điểm tham chiếu đăng ký học phần.
Không có dữ liệu cá nhân mẫu tự suy đoán.

Biên dịch với javac -encoding UTF-8 -d build/classes và các tệp trong src.
Kiểm tra cốt lõi tại ../review_revision/Verification.java dùng JDBC test double;
chưa xác nhận kết nối MySQL thực tế.

Mã là khung lớp và xử lý cốt lõi theo Câu 4.b. UI là boundary web chuẩn bị
model cho JSP. Trang JSP, đăng nhập, session, ánh xạ request và WAR là phần
tích hợp của phương án triển khai, không phải ứng dụng web đã hoàn thiện.
