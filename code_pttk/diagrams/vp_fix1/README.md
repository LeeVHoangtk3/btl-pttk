# Biểu đồ báo cáo theo mẫu fix1

Mẫu trực tiếp: `code_pttk/docs/N13 Nhóm 10_fix1.docx`. Tool chỉ đọc tệp này và xác minh SHA-256 trước, sau khi xử lý. Không sử dụng skill thiết kế Visual Paradigm trước đây.

- `vp_diagram_canvas.py`: ký hiệu SVG, khối lớp, boundary/control, bảng ERD và bộ tìm đường nối vuông góc.
- `vp_report_models.py`: tên lớp, thuộc tính và phương thức đối chiếu từ ảnh mẫu.
- `redesign_report_from_fix1.py`: lấy ảnh mẫu, dựng biểu đồ và tạo bản Word kiểm tra.
- `render_vp_svg.cjs`: chuyển SVG sang PNG dự phòng cho Word. DOCX chứa cả SVG và PNG đối với các hình dựng lại.

Chạy lần lượt bằng Python/Node của workspace:

```text
python code_pttk/scripts/redesign_report_from_fix1.py assets
node code_pttk/scripts/render_vp_svg.cjs
python code_pttk/scripts/redesign_report_from_fix1.py assemble
```

Ảnh Use Case, lớp, ERD, trạng thái, thành phần và triển khai được dựng lại bằng tool của dự án theo hình thức của mẫu. Ảnh trình tự và hoạt động dùng bản xuất gốc, giữ các nhãn, thông điệp và ký pháp; chỉ bỏ khoảng trắng giữa các đoạn thẳng và thêm lề trắng. Các sơ đồ lớp thiết kế nhiều nội dung có phần (a) giao diện, điều khiển, DAO và phần (b) thực thể, kiểu liệt kê.

Bản thử và bản sao trước chỉnh nằm trong `build/vp_redesign/`. Cần dàn trang, xem ảnh kết xuất và chạy `verify` trước `finalize`. `finalize` chỉ ghi vào báo cáo ĐATN24 nếu tệp đích và tệp mẫu không bị sửa đồng thời. Bản Word vẫn giữ nguyên phần văn bản và bảng; chỉ cập nhật ảnh, chú thích và bố cục liên quan. Các hình SVG do tool tạo, không được mô tả là bản xuất trực tiếp từ Visual Paradigm.
