# CẤU TRÚC SƠ ĐỒ MERMAID - MODULE MENU (QUẢN LÝ THỰC ĐƠN)

Thư mục này chứa đầy đủ mã nguồn Mermaid cho các chức năng trong phần Menu của hệ thống POS:
- **Thêm món lẻ**
- **Sửa món lẻ**
- **Xóa món lẻ**
- **Thêm combo**
- **Sửa combo**
- **Xóa combo**

Được phân loại theo 2 pha chính của môn học **Phân tích Thiết kế Hệ thống Thông tin (PTTKHTTT)**:
1. `phantich/`: Pha Phân tích (Analysis Phase)
2. `thietke/`: Pha Thiết kế (Design Phase)

---

## 1. Pha Phân tích (`phantich/`)
Trong pha phân tích, các sơ đồ tập trung vào miền nghiệp vụ (Domain Model):
- **Biểu đồ lớp (Class Diagram / VOPC)**: Chỉ gồm các khái niệm miền nghiệp vụ, không gắn kiểu dữ liệu chi tiết hay cài đặt kỹ thuật.
- **Biểu đồ tuần tự (Sequence Diagram)**: Thể hiện luồng trao đổi thông điệp nghiệp vụ giữa Người dùng (Actor), Giao diện (Boundary), Điều khiển (Control) và Thực thể (Entity).

| Chức năng | Sơ đồ tuần tự (Sequence Diagram) | Sơ đồ lớp (VOPC Class Diagram) |
|---|---|---|
| **Thêm món** | [sequence_them_mon.mermaid](./phantich/sequence_them_mon.mermaid) | [class_them_mon.mermaid](./phantich/class_them_mon.mermaid) |
| **Sửa món** | [sequence_sua_mon.mermaid](./phantich/sequence_sua_mon.mermaid) | [class_sua_mon.mermaid](./phantich/class_sua_mon.mermaid) |
| **Xóa món** | [sequence_xoa_mon.mermaid](./phantich/sequence_xoa_mon.mermaid) | [class_xoa_mon.mermaid](./phantich/class_xoa_mon.mermaid) |
| **Thêm combo** | [sequence_them_combo.mermaid](./phantich/sequence_them_combo.mermaid) | [class_them_combo.mermaid](./phantich/class_them_combo.mermaid) |
| **Sửa combo** | [sequence_sua_combo.mermaid](./phantich/sequence_sua_combo.mermaid) | [class_sua_combo.mermaid](./phantich/class_sua_combo.mermaid) |
| **Xóa combo** | [sequence_xoa_combo.mermaid](./phantich/sequence_xoa_combo.mermaid) | [class_xoa_combo.mermaid](./phantich/class_xoa_combo.mermaid) |
| **Tổng thể Menu** | - | [class_menu_phan_tich_tong_the.mermaid](./phantich/class_menu_phan_tich_tong_the.mermaid) |

---

## 2. Pha Thiết kế (`thietke/`)
Trong pha thiết kế, các sơ đồ được áp dụng mô hình phân lớp BCE (Boundary - Control - Entity) chi tiết:
- Đầy đủ kiểu dữ liệu (`String`, `double`, `bool`, `List`), tầm vực (`+`, `-`, `#`), các phương thức cụ thể.
- Khối rẽ nhánh (`alt`, `opt`, `loop`) trong biểu đồ tuần tự.

| Chức năng | Sơ đồ tuần tự (Sequence Diagram) | Sơ đồ lớp (VOPC Class Diagram) |
|---|---|---|
| **Thêm món** | [sequence_them_mon.mermaid](./thietke/sequence_them_mon.mermaid) | [class_them_mon.mermaid](./thietke/class_them_mon.mermaid) |
| **Sửa món** | [sequence_sua_mon.mermaid](./thietke/sequence_sua_mon.mermaid) | [class_sua_mon.mermaid](./thietke/class_sua_mon.mermaid) |
| **Xóa món** | [sequence_xoa_mon.mermaid](./thietke/sequence_xoa_mon.mermaid) | [class_xoa_mon.mermaid](./thietke/class_xoa_mon.mermaid) |
| **Thêm combo** | [sequence_them_combo.mermaid](./thietke/sequence_them_combo.mermaid) | [class_them_combo.mermaid](./thietke/class_them_combo.mermaid) |
| **Sửa combo** | [sequence_sua_combo.mermaid](./thietke/sequence_sua_combo.mermaid) | [class_sua_combo.mermaid](./thietke/class_sua_combo.mermaid) |
| **Xóa combo** | [sequence_xoa_combo.mermaid](./thietke/sequence_xoa_combo.mermaid) | [class_xoa_combo.mermaid](./thietke/class_xoa_combo.mermaid) |
| **Tổng thể Menu** | - | [class_menu_thiet_ke_tong_the.mermaid](./thietke/class_menu_thiet_ke_tong_the.mermaid) |
