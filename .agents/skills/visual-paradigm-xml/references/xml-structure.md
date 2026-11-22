# Cấu trúc XML và kiểm tra tham chiếu
Cấu trúc dưới đây được quan sát từ mẫu và mã nguồn, không phải lược đồ XML chính thức do nhà cung cấp công bố:

```xml
<Project ExporterVersion="16.1.1" UmlVersion="2.x" Xml_structure="simple">
  <ProjectInfo>...</ProjectInfo>
  <Models>...</Models>
  <Diagrams>...</Diagrams>
</Project>
```

Đoạn trên chỉ minh họa cấu trúc; không phải XML đầy đủ để nhập. `ProjectInfo` lấy từ mẫu `assets/project_header.tmpl`. `Models` chứa phần tử mô hình và các quan hệ. `Diagrams` chứa hình và đường nối; một mục `Shapes` hoặc `Connectors` rỗng có thể bị bộ sinh loại bỏ.

### Phân biệt phần tử mô hình với hình biểu diễn

- Phần tử mô hình, hình và đường nối có `Id` riêng. Hàm sinh mã hiện tạo mã mới gồm 16 ký tự và kiểm tra trùng trong tập mã nó đã sinh.
- Các thuộc tính `Model` và `MetaModelElement` trên hình hoặc đường nối tham chiếu về phần tử mô hình.
- `MasterView` trên phần tử mô hình chứa tham chiếu tới hình hoặc đường nối biểu diễn nó.
- `From`, `To` của đường nối tham chiếu tới hình biểu diễn. Các đầu quan hệ ở mức mô hình phải tham chiếu đúng phần tử mô hình hoặc đầu quan hệ tương ứng.
- Với thông điệp trình tự, `FromActivation`, `ToActivation` tham chiếu phần tử thanh thực thi khi được gán. Thông điệp trả về được gắn cấu trúc `ActionTypeReturn`.

Không suy từ việc mẫu chứa nhiều thuộc tính rằng mỗi phần tử bắt buộc phải có “20 đến 80 thuộc tính”. Bộ sinh dùng các mẫu thuộc tính có sẵn; gói không cung cấp lược đồ chính thức để chứng minh số lượng thuộc tính bắt buộc cho mọi phần tử.

### Các nhóm phần tử được sử dụng

- Biểu đồ lớp: `Class`, `Attribute`, `Operation`, `Parameter`, `Association`, `Generalization`.
- Biểu đồ trạng thái: `InitialPseudoState`, `State2`, `FinalState2`, `Transition2`.
- Biểu đồ trình tự: `Frame`, `InteractionActor`, `InteractionLifeLine`, `Activation`, `Message`, `CombinedFragment`, `InteractionOperand`, `InteractionConstraint`.
- Biểu đồ giao tiếp: dùng thêm `InteractionLifeLineLink` và các hình hoặc nhãn thông điệp riêng.
- Biểu đồ gói và triển khai: dùng các phần tử `Model`, `Package`, `Node`, `Component`, `Artifact`, cùng tham chiếu sơ đồ con.
- Biểu đồ thực thể và quan hệ: `DBTable`, `DBColumn`, `DBForeignKey`, `DBForeignKeyConstraint`.
- Nhánh hoạt động của bộ sinh: chỉ sinh `ActivityAction` và `ObjectNode`, dù mẫu nguồn hoặc tài nguyên có thể chứa thêm loại phần tử.

Thứ tự thuộc tính được script sắp theo tên. Một số phần tử con được sắp theo bảng `PRIO` trong mã. Đây là cách công cụ tổ chức đầu ra; không khẳng định bản thân thứ tự thuộc tính là điều kiện bắt buộc của XML. Khi tạo XML bằng `ElementTree`, để thư viện xử lý ký tự đặc biệt; tránh tự thoát ký tự thêm lần nữa làm sai chuỗi hiển thị.

### Validator thực sự kiểm tra những gì

`validate_vp.py` đọc XML, yêu cầu phần tử gốc là `Project`, tìm `ProjectInfo`, `Models`, `Diagrams`, kiểm tra mã `Id` trùng và một số tham chiếu không tồn tại. Script cũng kiểm tra một phần quan hệ giữa phần tử mô hình với hình biểu diễn; một số sai khác trong `MasterView` chỉ trở thành cảnh báo.

Validator **không** kiểm tra đầy đủ lược đồ của Visual Paradigm, ý nghĩa UML, ràng buộc CSDL, tên cột trùng, phần thập phân của kiểu số, độ dài của mọi mã, tính hợp lý của bố cục hoặc khả năng nhập thực tế. Nó cũng chưa bảo đảm rằng hai đầu đường nối thuộc đúng cùng một sơ đồ; tập mã dùng cho kiểm tra được thu thập trên nhiều sơ đồ.

Một lỗi sử dụng cần tránh: chạy validator không kèm đường dẫn tệp hiện vẫn trả mã thoát 0 mà không kiểm tra gì. Vì vậy, luôn ghi rõ đường dẫn và yêu cầu có dòng kết quả cho đúng tệp cần kiểm tra.

### Khi sửa XML đã có

Bộ sinh hiện không đọc XML đầu vào để cập nhật mô hình và không cung cấp trường đặc tả để tự giữ toàn bộ `Id` cũ. Chạy lại từ JSON tạo các mã mới; không thể hứa rằng việc dựng lại đặc tả sẽ giữ nguyên định danh của dự án.

Nếu phải sửa một XML đã xuất, cần đọc cấu trúc, lưu bản trước khi sửa, bảo toàn các định danh và cập nhật nhất quán tham chiếu ở cả mô hình lẫn sơ đồ. Sau đó chạy validator và thử nhập vào bản sao dự án. Không mặc định thay chuỗi toàn cục là đủ an toàn với mọi thay đổi.
