# Đặc tả JSON

Ghi đặc tả bằng UTF-8 **không BOM**. Script đọc với `encoding='utf8'` nên từ chối BOM. Windows PowerShell 5.1 `Set-Content -Encoding utf8` có thể thêm BOM; có thể dùng Python `Path.write_text(..., encoding='utf-8')` hoặc .NET `UTF8Encoding(false)` để tránh lỗi này.
Khung đầu vào chung:

```json
{
  "project": {"name": "DuAnMau", "author": "NhomThucHien"},
  "diagrams": [
    {"type": "class", "name": "Biểu đồ lớp", "classes": [], "relationships": []}
  ]
}
```

`project` có thể bỏ qua; `diagrams` phải có khi gọi bộ sinh. Mỗi sơ đồ cần có `type` và `name`. Giá trị `type` phải thuộc một trong tám loại đã liệt kê; mã hiện tại chưa kiểm tra đầu vào bằng một lược đồ JSON đầy đủ.

Không dùng dấu `|` trong giá trị để biểu thị nhiều lựa chọn khi chạy thật. Chẳng hạn, `"kind":"call|return"` trong một mô tả cấu trúc phải được thay bằng đúng một giá trị như `"kind":"call"`.

### Quy tắc chung về tên và tọa độ

Tên dùng trong `from`, `to` hoặc `parent` phải khớp chính xác với phần tử đã khai báo. Tránh dùng trùng tên cho các phần tử cần phân biệt vì nhiều nhánh dùng tên làm khóa tra cứu.

Các nhánh lớp, trạng thái thông thường, bảng, gói cấp cao, nút triển khai, nút hành động và nút đối tượng có đọc tọa độ trong một số trường hợp. Khi chỉ định vị trí, phải cung cấp đủ cả `x` và `y`. Không áp dụng quy tắc này cho mọi phần tử: nhánh trình tự hiện tự tính vị trí và không đọc tọa độ `x`, `y` của thành phần tham gia; một số phần tử con cũng được bố trí theo phần tử cha.

### Biểu đồ lớp với type class

`classes` là danh sách lớp. Một lớp có `name` và có thể có `stereotype`, `abstract`, `documentation`, `attributes`, `operations`. Thuộc tính dùng `name`, `type`, `visibility`, `static`; phương thức có thể có `returnType`, `visibility`, `static`, `abstract`, `documentation`, `params`. Tham số dùng `name`, `type`, `direction`.

`relationships` dùng `kind`, `from`, `to` và các trường tùy chọn như `name`, `fromMultiplicity`, `toMultiplicity`, `fromRole`, `toRole`, `fromNavigable`, `toNavigable`.

- `association`: liên kết.
- `aggregation`: kết tập; `from` là phía toàn thể.
- `composition`: hợp thành; `from` là phía toàn thể.
- `generalization`: khái quát hóa; `from` là lớp con, `to` là lớp cha.

Các giá trị `visibility` thường dùng là `private`, `protected`, `public`; `direction` của tham số có thể là `in`, `out`, `inout`. Bội số cần được chọn theo mô hình, chẳng hạn `1`, `0..1`, `0..*`, `1..*`.

Lớp có cùng tên được tái sử dụng giữa các biểu đồ lớp trong cùng một lần sinh. **Mã hiện tại giữ định nghĩa đầu tiên và không cập nhật thuộc tính từ lần khai báo sau.** Nếu lần sau chỉ ghi `name`, kích thước hình có thể không đủ để chứa nội dung đã có vì kích thước được tính từ khai báo hiện tại. Cần kiểm tra lại phần hình biểu diễn thay vì mặc định nó tự đồng bộ hoàn toàn.

Gói khai báo hỗ trợ `stereotype:"enumeration"` và dùng thuộc tính để biểu diễn các giá trị liệt kê. Cách này cần kiểm tra trong Visual Paradigm; không nên coi việc gắn nhãn khuôn mẫu là bằng chứng đã tạo đầy đủ mô hình Enumeration của UML.

### Biểu đồ trạng thái với type state

`initial` là cờ tạo nút khởi đầu, mặc định là `true`. `states` chứa các đối tượng có `name`, tùy chọn `documentation`, `x`, `y`. `finals` chứa tên các nút kết thúc. `transitions` chứa `from`, `to` và tùy chọn `name`.

Trong đầu chuyển trạng thái, `from:"initial"` hoặc `from:"[*]"` tham chiếu nút khởi đầu. Không đặt tên trạng thái thường là `initial`. Chuyển trạng thái về chính nó được khai báo bằng `from` và `to` giống nhau. Tọa độ trong đối tượng nút kết thúc chưa được nhánh này sử dụng.

Nhãn có thể ghi sự kiện, điều kiện và hành động theo cách thể hiện của mô hình. Script chỉ lưu chuỗi nhãn; không phân tích hoặc xác minh ý nghĩa các biểu thức trong chuỗi.

### Biểu đồ trình tự với type sequence

`participants` khai báo các thành phần tham gia. Mỗi thành phần có `name`; `kind` là `actor` hoặc `lifeline`, mặc định là `lifeline`. Đường sống có thể có `stereotype`.

`messages` chứa `from`, `to`, `text`, tùy chọn `kind` và `seq`. Các giá trị được xử lý riêng gồm `call`, `return`, `self`, `async`. Thứ tự trong danh sách quyết định thứ tự từ trên xuống. Khi dùng `self`, hai đầu phải là cùng một thành phần để giữ đúng ý nghĩa tự gọi. Nếu bỏ `seq`, script tự đánh số liên tiếp; số phân cấp như `1.1` phải được chỉ định.

`fragments` dùng `operator`, `from`, `to`, `operands`. Mỗi phần tương tác có `guard`, `from`, `to`. Các chỉ số bắt đầu từ 0 và bao gồm cả hai đầu. Chỉ số phải nằm trong `messages`; nhánh vẽ khung còn cần ít nhất một đường sống được khung bao phủ.

Thanh thực thi được suy ra từ chuỗi thông điệp bằng thuật toán của script. Vì thuật toán chưa mô phỏng đầy đủ mọi nhánh, lời gọi lồng nhau hoặc tương tác bất đồng bộ, cần kiểm tra lại thanh thực thi sau khi nhập.

### Biểu đồ giao tiếp với type communication

Dùng cấu trúc `participants` và `messages` tương tự biểu đồ trình tự. Các thành phần có vị trí theo cách bố trí tự động. Script tạo liên kết cho từng cặp thành phần và nhãn thông điệp dạng `seq: text`. Không dùng `fragments` để kỳ vọng có khung tương tác trên biểu đồ giao tiếp.

### Biểu đồ gói với type package

`packages` chứa `name` và tùy chọn `parent`. Khai báo gói cha trước gói con vì nhánh xây dựng tra cứu cha ngay khi duyệt. Phần vẽ hiện bố trí gói cấp cao và các gói con trực tiếp; không nên khai báo nhiều cấp lồng rồi kỳ vọng mọi cấp đều có hình tương ứng.

`dependencies` chứa `from`, `to`, tùy chọn `name`. Hai đầu phải có hình biểu diễn trong sơ đồ.

### Biểu đồ thực thể và quan hệ với type er

`tables` chứa `name` và `columns`. Mỗi cột có `name`, tùy chọn `type`, `pk`, `nullable`, `unique`, `length`. Các cờ phải là giá trị JSON `true` hoặc `false`, không phải chuỗi `"true"` hoặc `"false"`.

`foreignKeys` chứa `from`, `to`, tùy chọn `column`, `refColumn`, `name`, `nullable`, `identifying`, `fromMultiplicity`, `toMultiplicity`. Trong cách triển khai của gói, `from` là bảng được tham chiếu; `to` là bảng chứa khóa ngoại. Đây là quy ước của bộ sinh, không được suy thành quy tắc hướng mũi tên cho mọi loại sơ đồ.

Các giới hạn đã xác nhận từ mã và ví dụ kiểm tra:

- Khóa ngoại được tạo bằng cách **thêm một cột mới** vào bảng con. Nếu đã khai báo cột cùng tên trong `columns`, công cụ vẫn thêm nữa và tạo cột trùng tên. Validator hiện không phát hiện trường hợp này.
- Nếu không chỉ định `refColumn`, script lấy cột khóa chính đầu tiên tìm được. Một mục khóa ngoại chưa mô tả đầy đủ quan hệ tham chiếu khóa chính ghép.
- Cột khóa ngoại sao chép tên kiểu từ cột đích nhưng không sao chép đầy đủ chiều dài hoặc phần thập phân. Phải đối chiếu kiểu ở cả hai phía.
- `length` mặc định là 10. Mã không đọc trường `scale` hoặc `precision` từ JSON. Vì vậy, không mô tả `{"type":"decimal","length":12,"scale":2}` là đã tạo chắc chắn `DECIMAL(12,2)`; thử nghiệm cho thấy XML vẫn giữ `Scale="0"` từ mẫu.
- Chuỗi tên kiểu không được kiểm chứng như DDL của một hệ quản trị CSDL. Cần kiểm tra các thuộc tính kiểu nội bộ, phần thập phân và chiều dài trong Visual Paradigm trước khi dùng để sinh DDL.
- Kích thước bảng được tính trước khi bổ sung cột khóa ngoại, nên phần hình có thể cần điều chỉnh lại.

### Biểu đồ triển khai với type deployment

`nodes` khai báo nút triển khai theo `name`. `children` bên trong nút chứa `name` và `kind`, trong đó hai lựa chọn có chủ đích là `component` và `artifact`; mặc định là `component`. Các danh sách `associations` và `dependencies` chứa `from`, `to`, tùy chọn `name`.

Mỗi đầu quan hệ phải tham chiếu đúng một nút hoặc phần tử con đã được tạo. Mã hiện chưa có nhánh riêng cho giao diện, quan hệ hiện thực hóa hoặc đầy đủ mọi quan hệ triển khai của UML.

### Biểu đồ hoạt động với type activity

Đầu vào có `actions` và `objectNodes`, mỗi phần tử gồm `name`, tùy chọn cặp tọa độ `x`, `y`. Nhánh này chưa đọc danh sách luồng nối giữa các nút. Một tệp có nhiều nút rời vẫn có thể qua validator; điều đó chưa tạo thành một quy trình hoạt động đầy đủ.
