# Giới hạn đã xác nhận

Đây là giới hạn của script đi kèm, không phải giới hạn của Visual Paradigm.

- Validator chỉ kiểm tra một phần XML và tham chiếu. Nó không xác nhận ngữ nghĩa UML, ràng buộc CSDL, bố cục hoặc khả năng nhập thực tế. Chạy không có đối số tệp còn có thể trả mã thoát 0 mà không kiểm tra gì.
- ERD: nhánh khóa ngoại thêm một cột mới, kể cả khi đã khai báo cột cùng tên. Không tạo đặc tả có cột FK vừa khai báo sẵn vừa yêu cầu script tự thêm; nếu cần liên kết vào cột hiện hữu thì phải điều chỉnh công cụ hoặc sửa XML có kiểm chứng.
- Cột FK chỉ sao chép tên kiểu, không bảo đảm sao chép chiều dài và phần thập phân. Trường hợp khóa cha VARCHAR(150) có thể tạo FK dài 10.
- `scale` và `precision` trong JSON chưa được nhánh ERD đọc. `decimal` với `scale: 2` có thể vẫn sinh `Scale="0"`. Không hứa đã sinh đúng DECIMAL(12,2); nếu đây là yêu cầu bắt buộc, báo giới hạn trước khi tạo đầu ra.
- Khóa ngoại mặc định chọn cột PK đầu tiên; chưa biểu diễn đầy đủ FK tham chiếu khóa chính ghép bằng một mục đặc tả.
- Lớp trùng tên dùng định nghĩa đầu tiên. Định nghĩa sau không cập nhật thuộc tính; hình mới cũng có thể tính kích thước không đủ nếu chỉ khai báo lại tên.
- Tọa độ thành phần tham gia của `sequence` chưa được đọc. `x`, `y` chỉ có hiệu lực ở các nhánh và phần tử thực sự xử lý chúng; nếu đặt thì cung cấp đủ cặp.
- Gói cha phải khai báo trước gói con. Phần vẽ gói chỉ xử lý gói cấp cao và con trực tiếp.
- Bộ sinh tạo `Id` ngẫu nhiên mới. Không có cơ chế nhập dự án cũ để bảo toàn mã qua việc dựng lại JSON.
- `activity` chưa có luồng nối hoặc phân nhánh. Không dùng state diagram thay activity diagram nếu yêu cầu nghiệp vụ cần mô hình luồng hoạt động.
- Chưa sinh Use Case, BPMN, Requirement, biểu đồ thành phần độc lập, hoặc toàn bộ quan hệ của biểu đồ triển khai.

Tám ví dụ đi kèm chạy được với validator không có lỗi hoặc cảnh báo trong lần kiểm tra tích hợp. Điều đó không loại trừ các giới hạn trên; chưa thực hiện thử nhập trực tiếp vào Visual Paradigm.

