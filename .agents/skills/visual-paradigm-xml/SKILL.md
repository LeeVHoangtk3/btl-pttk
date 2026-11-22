---
name: visual-paradigm-xml
description: Use when a user requests Visual Paradigm Project XML, edits to existing VP XML, or review of UML and ER diagrams intended for Visual Paradigm. Does not apply to PlantUML, Mermaid, draw.io or XMI generation.
---

# XML và nhận xét biểu đồ Visual Paradigm

Chọn chế độ theo yêu cầu: **nhận xét**, **sinh XML**, hoặc **sửa XML đã có**. Bộ sinh dùng mẫu Project XML; chưa có bằng chứng bảo đảm nhập được mọi đầu ra vào Visual Paradigm.

## Nhận xét biểu đồ

Khi người dùng yêu cầu chỉ nhận xét, đọc báo cáo, ảnh và mã sơ đồ; không thay đổi chúng hoặc chạy công cụ sinh đè đầu ra. Đọc [checklist rà soát](references/review-checklist.md).

Mỗi nhận xét phải có: **phần hoặc mục, số trang, số hoặc tên hình, quan sát cụ thể, ảnh hưởng và hướng xử lý dự kiến**. Phân biệt lỗi chắc chắn với điểm cần xác minh; nêu mức ưu tiên. Xác định rõ phiên bản báo cáo dùng để đánh số trang. Lấy số trang từ bản kết xuất khớp tài liệu hiện tại; không suy từ số hình. Nếu chữ trong ảnh không đọc được, ghi giới hạn đó.

Đối chiếu cùng một chức năng qua kịch bản, Use Case, lớp, trình tự, trạng thái, hoạt động, ERD và SQL. Số lượng sơ đồ không chứng minh tính đúng hoặc đầy đủ.

## Sinh Project XML

Đọc phần loại sơ đồ tương ứng trong [đặc tả JSON](references/spec-format.md) và [giới hạn bộ sinh](references/limitations.md). Dùng ví dụ trong `examples/` để chuẩn bị đầu vào. Đường dẫn dưới đây được tính từ thư mục chứa skill; đặt đầu ra tại thư mục tác vụ:

```text
python "<skill>/scripts/vpgen.py" "<task>/spec.json" -o "<task>/diagram.xml"
python "<skill>/scripts/validate_vp.py" "<task>/diagram.xml"
```

Cần Python 3.9 trở lên và JSON UTF-8 không BOM. Đọc cả lỗi lẫn cảnh báo, đối chiếu số tệp thực sự được kiểm tra. `OK` chỉ xác nhận phạm vi kiểm tra của script. Chỉ báo đã nhập thành công khi có bằng chứng thử nhập trực tiếp.

Các nhánh hiện có: `class`, `state`, `sequence`, `communication`, `package`, `er`, `deployment`, `activity`. Nhánh `activity` chỉ có các nút rời. Chưa sinh Use Case hoặc biểu đồ thành phần độc lập. Đừng đổi loại sơ đồ mà người dùng cần chỉ để vượt giới hạn bộ sinh.

## Sửa XML đã có

Đọc [cấu trúc XML](references/xml-structure.md). Giữ nguyên định danh hiện hữu và cập nhật nhất quán mọi tham chiếu có liên quan. Bộ sinh JSON tạo mã mới; không dùng nó để mặc định cập nhật XML cũ mà vẫn giữ `Id`.

## Khi bàn giao

Nêu tệp đã tạo hoặc nhận xét, các kiểm tra thực hiện và giới hạn còn lại. Với chế độ nhận xét, ghi rõ chưa sửa sơ đồ. Không thêm danh mục nguồn tham khảo bên ngoài nếu người dùng chưa yêu cầu.

