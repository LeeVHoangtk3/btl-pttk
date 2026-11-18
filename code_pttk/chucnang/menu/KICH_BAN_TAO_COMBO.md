# KỊCH BẢN CHI TIẾT CA SỬ DỤNG: TẠO COMBO MỚI (ADD COMBO)

## 1. Bảng kịch bản ca sử dụng (Use Case Scenario)

| STT | Mục | Nội dung |
|:---:|---|---|
| **1.** | **Tác nhân** | Quản lý nhà hàng (hoặc Nhân viên được phân quyền quản lý thực đơn) |
| **2.** | **Mô tả** | Quản lý thiết lập và tạo một gói Combo món ăn mới trên hệ thống, bao gồm các thông tin chung (tên combo, danh mục, giá bán, số lượng khách phục vụ, mô tả) và danh sách các món ăn lẻ thành phần kèm số lượng tương ứng. |
| **3.** | **Điều kiện trước** | - Quản lý đã đăng nhập thành công vào hệ thống với tài khoản có quyền Quản lý thực đơn.<br>- Hệ thống đã có sẵn danh mục và danh sách các món lẻ (Dish) đang hoạt động/kinh doanh để có thể chọn làm món thành phần. |
| **4.** | **Luồng sự kiện chính** | **1.** Quản lý mở màn hình **Quản lý Thực đơn**, chuyển sang tab **Combo** *(xem Màn hình 1)*.<br>**2.** Quản lý nhấn vào nút **+ Thêm Combo Mới** trên thanh công cụ.<br>**3.** Hệ thống hiển thị hộp thoại pop-up (Modal) **Tạo Combo Mới** *(xem Màn hình 2)* gồm:<br>&nbsp;&nbsp;&nbsp;&nbsp;- *Cột trái (Thông tin chung)*: Tên combo, danh mục, giá bán, số lượng khách, mô tả.<br>&nbsp;&nbsp;&nbsp;&nbsp;- *Cột phải (Chọn món thành phần)*: Danh sách món lẻ kèm ô tích chọn và bộ đếm số lượng (+/-).<br>**4.** Quản lý nhập tên combo (ví dụ: *"Combo Tiệc Gia Đình"*).<br>**5.** Quản lý chọn danh mục cho combo và nhập giá bán (ví dụ: *350.000 đ*).<br>**6.** Quản lý nhập số lượng khách dự kiến phục vụ (ví dụ: *4 người*) và nhập ghi chú mô tả combo.<br>**7.** Quản lý tích chọn các món lẻ thành phần và điều chỉnh số lượng từng món (ví dụ: *2 Gà rán giòn, 1 Mì Ý sốt bò bằm, 1 Khoai tây chiên, 4 lon Coca-Cola*).<br>**8.** Hệ thống tự động tính toán và hiển thị tổng giá trị món thành phần tham khảo để quản lý so sánh với giá bán combo.<br>**9.** Quản lý kiểm tra lại toàn bộ thông tin và nhấn nút **Lưu Combo**.<br>**10.** Hệ thống kiểm tra tính hợp lệ của dữ liệu (tên hợp lệ không trùng, giá > 0, có ít nhất 1 món con).<br>**11.** Hệ thống lưu combo mới vào cơ sở dữ liệu, đóng modal và làm mới danh sách thực đơn với thông báo *"Tạo combo thành công"*. |
| **5.** | **Luồng sự kiện phụ** | - **Hủy thao tác**: Quản lý nhấn nút **Hủy** hoặc biểu tượng **✕** đóng modal, hệ thống hủy dữ liệu đang nhập và giữ nguyên danh sách hiện tại.<br>- **Thay đổi số lượng / bỏ chọn món**: Quản lý có thể bỏ tích chọn hoặc dùng nút `–` để giảm số lượng món con trước khi nhấn Lưu.<br>- **Chưa có món lẻ**: Nếu hệ thống chưa có món lẻ nào, bảng chọn món thành phần hiển thị thông báo *"Chưa có món ăn lẻ khả dụng, vui lòng thêm món ăn trước"*. |
| **6.** | **Điều kiện sau** | Combo mới được lưu thành công trên hệ thống với trạng thái **Đang bán**, hiển thị trong danh sách quản lý thực đơn và sẵn sàng cho nhân viên order chọn khi phục vụ khách. |
| **7.** | **Ngoại lệ** | - **Bỏ trống trường bắt buộc**: Nếu tên combo hoặc giá bán để trống, hệ thống viền đỏ trường đó và cảnh báo *"Vui lòng nhập đầy đủ thông tin bắt buộc"*.<br>- **Giá bán hoặc số lượng không hợp lệ**: Nhập giá bán $\le 0$ hoặc số lượng món $\le 0$, hệ thống báo lỗi *"Giá bán và số lượng phải lớn hơn 0"*.<br>- **Chưa chọn món thành phần**: Quản lý nhấn Lưu nhưng chưa tích chọn món con nào, hệ thống báo lỗi *"Combo phải chứa ít nhất 1 món ăn thành phần"*.<br>- **Trùng tên combo**: Tên combo đã tồn tại trong thực đơn, hệ thống cảnh báo *"Tên combo đã tồn tại, vui lòng chọn tên khác"*. |

---

## 2. Giao diện trực quan minh họa từng bước (UI Mockups)

### Màn hình 1: Quản lý Thực đơn (Menu Management - Tab Combo)
*Tương ứng bước 1 - 2 trong Luồng sự kiện chính:*
- Hiển thị danh sách các Combo hiện có, thanh tìm kiếm, bộ lọc danh mục và nút nhấn **+ Thêm Combo Mới**.
- File ảnh lưu tại: [mh_01_quan_ly_thuc_don_combo.jpg](file:///D:/CODE%20PTIT/PTTKHTTT/BTL/code/chucnang/menu/images/mh_01_quan_ly_thuc_don_combo.jpg)

### Màn hình 2: Biểu mẫu pop-up Tạo Combo Mới (Create Combo Modal)
*Tương ứng bước 3 - 9 trong Luồng sự kiện chính:*
- Cột bên trái: Các trường nhập liệu thông tin combo (Tên, Danh mục, Giá bán, Số lượng khách, Mô tả).
- Cột bên phải: Danh sách món lẻ cho phép tích chọn và nút tăng/giảm số lượng từng món con (`+` / `–`).
- Khu vực tổng hợp: Tổng giá trị món thành phần, giá bán combo ưu đãi và cụm nút **Hủy** / **Lưu Combo**.
- File ảnh lưu tại: [mh_02_bieu_mau_tao_combo_moi.jpg](file:///D:/CODE%20PTIT/PTTKHTTT/BTL/code/chucnang/menu/images/mh_02_bieu_mau_tao_combo_moi.jpg)
