# CẤU TRÚC SƠ ĐỒ - MODULE GỘP ĐƠN HÀNG (MERGE ORDERS)

Thư mục này chứa đầy đủ tài liệu, mã nguồn sơ đồ Mermaid và PlantUML cho chức năng **Gộp đơn hàng** trong hệ thống POS nhà hàng:

- **Pha Phân tích (Analysis Phase)**: Tập trung vào mô hình hóa miền nghiệp vụ tự nhiên, tương tác giữa Nhân viên, Giao diện và các thực thể nghiệp vụ. Đã bỏ các enumeration (`TrangThaiBan`, `TrangThaiDon`, `LyDoHuyDon`).
- **Pha Thiết kế (Design Phase)**: Áp dụng kiến trúc BCE chi tiết, đầy đủ phương thức, kiểu dữ liệu, tầm vực, khối rẽ nhánh điều kiện và các enumeration trạng thái (`TrangThaiBan`, `TrangThaiDon`).

---

## 1. Các sơ đồ trong thư mục `diagram/` (Phiên bản đồng bộ Mermaid - PlantUML)

| STT | Pha | Tệp Mermaid | Tệp PlantUML tương ứng | Ảnh PNG kết xuất | Mô tả |
|:---:|:---:|---|---|---|---|
| 1 | **Phân tích** | [pos_phan_tich_gop_don.mermaid](./diagram/pos_phan_tich_gop_don.mermaid) | [pos_phan_tich_gop_don.puml](./diagram/pos_phan_tich_gop_don.puml) | [pos_phan_tich_gop_don.png](../../diagrams/puml_out/chucnang/gop_don/diagram/pos_phan_tich_gop_don.png) | Sơ đồ lớp phân tích chức năng gộp đơn hàng (các bảng có đầy đủ thuộc tính, không để trống) |
| 2 | **Thiết kế** | [pos_thiet_ke_gop_don.mermaid](./diagram/pos_thiet_ke_gop_don.mermaid) | [pos_thiet_ke_gop_don.puml](./diagram/pos_thiet_ke_gop_don.puml) | [pos_thiet_ke_gop_don.png](../../diagrams/puml_out/chucnang/gop_don/diagram/pos_thiet_ke_gop_don.png) | Sơ đồ lớp thiết kế chức năng gộp đơn hàng (BCE, phương thức gopHoaDon, ganBan; đầy đủ TrangThaiBan, TrangThaiDon) |

---

## 2. Quy chuẩn Style PlantUML áp dụng:
1. **Màu sắc đồng nhất**: Lớp sử dụng màu `#7ACFF5` (chuẩn Visual Paradigm), viền `#000000` (độ dày 1px). Nền package màu trắng `#FFFFFF`, viền `#000000`.
2. **Khoảng cách**: `nodesep 65` & `ranksep 65`, `ortho` (đường vuông góc 90 độ), `shadowing false`.
3. **Phân cách**: `hide circle`. Ngăn cách rõ ràng giữa thuộc tính và phương thức bằng vạch `--`.
4. **Pha phân tích**: `hide methods`. Không để trống bảng nào.
