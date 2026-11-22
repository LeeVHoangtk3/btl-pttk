# Rà soát biểu đồ mà chưa chỉnh sửa

## Xác định tài liệu và vị trí

- Xác định tên và phiên bản báo cáo được dùng; phân biệt bản gốc, bản đã dàn trang và PDF tham khảo.
- Đối chiếu bản kết xuất với Word hiện tại bằng nội dung hoặc mã băm. Nếu không khớp, kết xuất bản hiện tại trước khi ghi số trang.
- Đọc ảnh sơ đồ ở độ phân giải gốc. Kết hợp nội dung kịch bản và SQL, không dựa riêng vào văn bản OCR hoặc ảnh thu nhỏ.
- Ghi trang và chú thích hình thực sự chứa vấn đề. Nếu dẫn nhiều hình, ghi rõ từng vị trí.

## Các quan hệ cần đối chiếu

### Use Case và kịch bản

- Ca sử dụng có thể hiện mục tiêu của tác nhân hay chỉ là nút giao diện hoặc bước xử lý?
- Điều kiện trước, bước bắt buộc và nhánh có điều kiện có khớp kịch bản?
- `include` đi từ ca bao hàm tới ca được bao hàm; `extend` đi từ ca mở rộng tới ca cơ sở. Không chỉ đảo mũi tên mà bỏ qua ý nghĩa quan hệ.
- Nếu dùng extension point, kiểm tra nó thuộc ca cơ sở. Không dùng include/extend như mũi tên chỉ thứ tự công việc.

### Lớp và dữ liệu

- Tên, kiểu thuộc tính, lớp cha/con, bội số và trách nhiệm có khớp các chức năng?
- Tiền, thời gian, trạng thái và mã nội bộ có cùng ý nghĩa giữa lớp, ERD và SQL? Nếu khác kiểu vì ánh xạ thiết kế, có giải thích rõ?
- Thuộc tính có trên giao diện hoặc kịch bản có chỗ lưu phù hợp? Mô hình tài khoản, người thao tác hoặc phương thức thanh toán có bao phủ yêu cầu đã nêu?
- Phân biệt lỗi trong ảnh hiện có với đề xuất thiết kế vật lý mới chưa được chốt.

### Trình tự và hoạt động

- Đối tượng nhận thông điệp có trách nhiệm hoặc phương thức tương ứng? Hướng gọi và trả về có hợp lý?
- Nhánh lỗi, hủy, thử lại và cập nhật nhiều bảng có thể hiện hoặc được giải thích trong đặc tả?
- Các luồng thay thế trong `alt` có điều kiện rõ ràng; trạng thái và dữ liệu sau mỗi nhánh có nhất quán?
- Dữ liệu có được xác nhận thành công quá sớm, hoặc có thao tác in, thanh toán ngoài hệ thống mà không kiểm tra kết quả?
- Sơ đồ hoạt động có đủ điểm quyết định, đường đi và kết thúc cho các nhánh được mô tả? Không kết luận thiếu chỉ vì một bước không nhìn rõ trong ảnh.

### Trạng thái

- Trạng thái có thuộc đúng thực thể? Sự kiện và điều kiện chuyển trạng thái có khớp kịch bản và các thao tác SQL?
- Sau trạng thái kết thúc có còn cho phép cập nhật hoặc thanh toán lại không?
- Nếu thực thể chứa nhiều phần tử hoạt động, có kiểm tra toàn bộ trước khi chuyển nó sang trạng thái trống hoặc hoàn tất?

### ERD và SQL

- Kiểu dữ liệu có phù hợp ý nghĩa: tên, ảnh, địa chỉ, tiền, thời gian và mã trạng thái?
- PK, FK, UNIQUE và khóa ghép có đủ để thực hiện quy tắc nghiệp vụ? Phân biệt khóa dòng với khóa nhận diện nội dung trùng.
- Công thức tổng tiền, giảm giá, thuế và tiền tip có thống nhất giữa giao diện, dữ liệu và thanh toán?
- Các thao tác tạo, gộp hoặc thanh toán có bảo đảm ranh giới giao dịch và kiểm tra cạnh tranh? Nêu rõ nếu tài liệu chưa đủ căn cứ đánh giá.

### Thành phần và triển khai

- Giao diện cung cấp hoặc yêu cầu có gắn đúng thành phần? Quan hệ phụ thuộc có đúng phía sử dụng?
- Phân biệt phần mềm, thành phần, tệp triển khai và nút phần cứng hoặc môi trường thực thi.
- Nhãn giao thức, phụ thuộc giữa máy chủ, CSDL và dịch vụ ngoài có rõ và đọc được?
- Không khẳng định framework, phiên bản JDK, nhà cung cấp hoặc cấu hình tối thiểu chỉ từ tên WAR, JDBC hay một nhãn cổng thanh toán.

## Hình thức trình bày

Kiểm tra nhãn trùng đường sống, chữ quá nhỏ, đường nối xuyên nội dung, nhãn bị cắt và định dạng chú thích. Bố cục xấu và mô hình sai là hai loại nhận xét khác nhau; ảnh lớn hơn không sửa được chữ chồng nhau trong ảnh gốc.

## Định dạng một nhận xét

**Vị trí:** mục, trang, hình và tên sơ đồ.

**Quan sát:** chi tiết đọc được hoặc điều kiện đối chiếu với kịch bản hoặc SQL.

**Đánh giá:** lỗi chắc chắn, điểm cần xác minh hoặc đề xuất cải thiện; ưu tiên cao, vừa hoặc thấp.

**Ảnh hưởng:** hệ quả cụ thể đối với mô hình, nghiệp vụ hoặc khả năng đọc.

**Hướng xử lý dự kiến:** mô tả thay đổi cần cân nhắc; chưa sửa ảnh, mã nguồn, XML hay tài liệu khi người dùng chỉ yêu cầu nhận xét.

