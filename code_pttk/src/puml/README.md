# DANH MỤC CÁC SƠ ĐỒ PLANTUML (FOLDER: src/puml)

Thư mục này là phiên bản **PlantUML (`.puml`)** tương ứng 1-1 với thư mục `src/mermaid/` (Mermaid), được chuẩn hóa thiết kế theo phong cách trực quan của Visual Paradigm:

### Đặc điểm thiết kế:
1. **Màu sắc đồng nhất**:
   - Tất cả các lớp chỉ sử dụng duy nhất màu xanh `#7ACFF5` (chuẩn Visual Paradigm), viền đen `#000000` (độ dày 1px).
   - Nền package màu trắng `#FFFFFF`, viền đen `#000000`.
2. **Khoảng cách đều đặn & thoáng đẹp**:
   - `skinparam nodesep 65` & `skinparam ranksep 65`: Khoảng cách giữa các bảng được nới đều thoáng (65px), không bị dính sát nhau.
   - `skinparam linetype ortho`: Đường liên kết vuông góc 90 độ.
   - `skinparam shadowing false`: Tắt đổ bóng.
   - `skinparam classAttributeIconSize 0`: Ký hiệu tầm vực dạng văn bản (`+`, `-`, `#`).
   - `hide circle`: Bỏ biểu tượng hình tròn chữ C đầu tên class.
3. **Mũi tên liên kết & Độ dài tiêu chuẩn**:
   - Mũi tên và đường liên kết sử dụng độ dài tiêu chuẩn (`-down->`, `-right->`, `--down-`, `<|--down-`, `*-right-`, `..down..>`).
   - Bỏ toàn bộ phần mô tả nhãn chữ trên các mũi tên để sơ đồ gọn gàng, thoáng mắt, thể hiện chuẩn bản số (multiplicity) và quan hệ liên kết.
4. **Phần thiết kế (Design Phase)**:
   - Loại bỏ hoàn toàn các stereotype như `<<entity>>`, `<<control>>`, `<<boundary>>`, `<<enumeration>>` theo đúng yêu cầu.
   - Ngăn cách rõ ràng giữa ngăn thuộc tính và ngăn phương thức bằng vạch `--`.

---

### Danh sách các file:

| STT | File PlantUML (`.puml`) | File Mermaid tương ứng | Mô tả nội dung |
|:---:|---|---|---|
| 1 | [pos_class_diagram_pha_phan_tich.puml](./pos_class_diagram_pha_phan_tich.puml) | [pos_class_diagram_pha_phan_tich.mermaid](../mermaid/pos_class_diagram_pha_phan_tich.mermaid) | Sơ đồ lớp tổng thể pha Phân tích (Toàn bộ 3 package: Menu, Order, Thanh toán; bỏ TrangThaiBan, TrangThaiDon, LyDoHuyDon) |
| 2 | [pos_class_diagram_pha_thiet_ke.puml](./pos_class_diagram_pha_thiet_ke.puml) | [pos_class_diagram_pha_thiet_ke.mermaid](../mermaid/pos_class_diagram_pha_thiet_ke.mermaid) | Sơ đồ lớp tổng thể pha Thiết kế (BCE, phương thức, kiểu dữ liệu; đã gộp Đơn vào Order; đầy đủ TrangThaiDon, TrangThaiBan, LyDoHuyDon) |
| 3 | [pos_phan_tich_01_menu.puml](./pos_phan_tich_01_menu.puml) | [pos_phan_tich_01_menu.mermaid](../mermaid/pos_phan_tich_01_menu.mermaid) | Sơ đồ lớp pha Phân tích - Package Menu (Dish: loaiMon, moTa) |
| 4 | [pos_phan_tich_02_order.puml](./pos_phan_tich_02_order.puml) | [pos_phan_tich_02_order.mermaid](../mermaid/pos_phan_tich_02_order.mermaid) | Sơ đồ lớp pha Phân tích - Package Order (Đã gộp nghiệp vụ Đơn; bỏ TrangThaiBan, TrangThaiDon, LyDoHuyDon) |
| 5 | [pos_phan_tich_04_thanhtoan.puml](./pos_phan_tich_04_thanhtoan.puml) | [pos_phan_tich_04_thanhtoan.mermaid](../mermaid/pos_phan_tich_04_thanhtoan.mermaid) | Sơ đồ lớp pha Phân tích - Package Thanh toán |
| 6 | [pos_thiet_ke_01_menu.puml](./pos_thiet_ke_01_menu.puml) | [pos_thiet_ke_01_menu.mermaid](../mermaid/pos_thiet_ke_01_menu.mermaid) | Sơ đồ lớp pha Thiết kế - Package Menu (BCE) |
| 7 | [pos_thiet_ke_02_order.puml](./pos_thiet_ke_02_order.puml) | [pos_thiet_ke_02_order.mermaid](../mermaid/pos_thiet_ke_02_order.mermaid) | Sơ đồ lớp pha Thiết kế - Package Order (BCE: chọn bàn, đặt món, gộp/tách đơn, hủy đơn, chuyển bàn; đầy đủ TrangThaiDon, TrangThaiBan, LyDoHuyDon) |
| 8 | [pos_thiet_ke_04_thanhtoan.puml](./pos_thiet_ke_04_thanhtoan.puml) | [pos_thiet_ke_04_thanhtoan.mermaid](../mermaid/pos_thiet_ke_04_thanhtoan.mermaid) | Sơ đồ lớp pha Thiết kế - Package Thanh toán (BCE) |
