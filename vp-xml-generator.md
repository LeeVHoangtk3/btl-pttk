# Hướng dẫn bộ sinh XML cho Visual Paradigm

Tài liệu này phân giải gói `vp-xml-generator.skill` thành một tệp Markdown, đồng thời hiệu đính tiếng Việt và đối chiếu hướng dẫn với mã nguồn. Tên thư mục trong gói là `vp-xml-generator`; tên skill được khai báo trong `SKILL.md` là `visual-paradigm-xml`. Hai tên này có vai trò khác nhau và không cần tự ý đổi cho giống nhau.

Gói dùng đặc tả JSON để sinh XML mô phỏng cấu trúc Project XML do Visual Paradigm xuất ra. **Chưa có bằng chứng rằng mọi XML do công cụ sinh ra đều nhập được vào Visual Paradigm.** Kết quả kiểm tra bằng script chỉ phản ánh một phần tính toàn vẹn tham chiếu, không xác nhận đầy đủ ngữ nghĩa UML, kiểu dữ liệu hay bố cục sơ đồ.

Ba tệp hướng dẫn được viết lại trong phần chính: `SKILL.md`, `references/spec-format.md` và `references/xml-structure.md`. Mười bảy tệp kỹ thuật còn lại được giữ nguyên trong phụ lục, gồm script Python, ví dụ JSON, mẫu thuộc tính và XML mẫu. Tên hàm, khóa JSON, tên thẻ XML và giá trị liệt kê của công cụ được giữ đúng cách viết để có thể đối chiếu với mã nguồn.

## Mục lục

- [Hướng dẫn sử dụng đã hiệu đính](#huong-dan)
- [Cấu trúc đặc tả JSON](#dac-ta-json)
- [Cấu trúc XML và kiểm tra tham chiếu](#cau-truc-xml)
- [Kết quả kiểm tra và các điểm đã sửa](#kiem-tra)
- [Mã nguồn và tài nguyên nguyên gốc](#phu-luc)

<a id="huong-dan"></a>

## Hướng dẫn sử dụng đã hiệu đính

### Nội dung tương ứng với SKILL.md

```yaml
name: visual-paradigm-xml
description: Sinh Project XML cho Visual Paradigm từ đặc tả JSON, với các giới hạn được mô tả trong tài liệu. Không phải bộ sinh XMI, PlantUML, Mermaid hoặc draw.io.
```

### Mục đích và phạm vi

Công cụ phù hợp khi cần tạo dữ liệu mô hình và hình biểu diễn của một số loại sơ đồ trong Visual Paradigm. Tệp đầu ra dựa trên các mẫu đi kèm có `ExporterVersion="16.1.1"` và `Xml_structure="simple"`. Những giá trị này mô tả mẫu xuất được sử dụng; chúng không chứng minh khả năng tương thích với mọi phiên bản Visual Paradigm.

Các nhánh xử lý hiện có trong mã nguồn:

- `class`: biểu đồ lớp; có thuộc tính, phương thức, tham số, nhãn khuôn mẫu và các quan hệ liên kết, kết tập, hợp thành, khái quát hóa.
- `state`: biểu đồ trạng thái; có nút khởi đầu, trạng thái, nút kết thúc và chuyển trạng thái, kể cả tự chuyển.
- `sequence`: biểu đồ trình tự; có tác nhân, đường sống, thông điệp, thanh thực thi và một số dạng khung tương tác kết hợp.
- `communication`: biểu đồ giao tiếp; có tác nhân, đường sống, liên kết và thông điệp được đánh số.
- `package`: biểu đồ gói; phần hình biểu diễn hiện chỉ bố trí gói con trực tiếp bên trong gói cha.
- `er`: biểu đồ thực thể và quan hệ; có bảng, cột và quan hệ khóa ngoại, nhưng còn hạn chế khi tạo cột khóa ngoại hoặc xác định chi tiết kiểu dữ liệu.
- `deployment`: biểu đồ triển khai; có nút triển khai, thành phần, hiện vật triển khai và các quan hệ liên kết hoặc phụ thuộc. Đây chưa phải bộ hỗ trợ đầy đủ mọi ký pháp của biểu đồ triển khai.
- `activity`: biểu đồ hoạt động ở mức hạn chế; chỉ sinh nút hành động và nút đối tượng. Chưa sinh luồng điều khiển, nút quyết định, nút rẽ nhánh song song, nút đồng bộ hoặc làn trách nhiệm.

Mã nguồn chưa có nhánh sinh biểu đồ Use Case, BPMN, Requirement hoặc biểu đồ thành phần độc lập (`component`). Việc đặt một thành phần bên trong nút triển khai không đồng nghĩa với hỗ trợ biểu đồ thành phần độc lập. Đây là giới hạn của bộ sinh, không phải giới hạn của Visual Paradigm.

Không thay biểu đồ hoạt động bằng biểu đồ trạng thái chỉ để vượt qua giới hạn của công cụ. Biểu đồ hoạt động mô tả luồng công việc; biểu đồ trạng thái mô tả trạng thái và phản ứng theo sự kiện của một thực thể. Khi cần biểu đồ hoạt động đầy đủ, hãy vẽ hoặc bổ sung các phần còn thiếu bằng trình biên tập phù hợp.

### Quy trình sử dụng trên Windows

Các lệnh dưới đây chạy từ thư mục chứa `vp-xml-generator.skill`. `python` cần trỏ tới Python 3.9 trở lên vì bộ sinh gọi `xml.etree.ElementTree.indent`.

1. Giải nén gói vào một thư mục làm việc:

   ```powershell
   python -m zipfile -e .\vp-xml-generator.skill .\build\vp-xml-work
   ```

2. Đọc ví dụ phù hợp trong `build/vp-xml-work/vp-xml-generator/examples`, rồi tạo đặc tả JSON. Nên thử một sơ đồ nhỏ trước khi ghép nhiều sơ đồ.

3. Sinh XML, chẳng hạn với ví dụ biểu đồ lớp:

   ```powershell
   python .\build\vp-xml-work\vp-xml-generator\scripts\vpgen.py .\build\vp-xml-work\vp-xml-generator\examples\class.json -o .\build\vp-xml-work\class.xml
   ```

4. Chạy kiểm tra với đường dẫn XML được ghi rõ:

   ```powershell
   python .\build\vp-xml-work\vp-xml-generator\scripts\validate_vp.py .\build\vp-xml-work\class.xml
   ```

5. Đọc cả lỗi và cảnh báo. `OK` có nghĩa là script chưa phát hiện lỗi thuộc phạm vi kiểm tra của nó; không có nghĩa là sơ đồ đã đúng nghiệp vụ hoặc chắc chắn nhập được vào Visual Paradigm.

6. Thử nhập vào một dự án thử nghiệm trong Visual Paradigm. Hướng dẫn chính thức mô tả lệnh `Project > Import > XML...`; tên menu có thể khác theo giao diện. Không xem tệp XML là tệp dự án `.vpp` để mở trực tiếp. Tài liệu chính thức cũng lưu ý việc nhập có thể ghi đè dữ liệu mô hình hiện có.

7. Sau khi nhập, kiểm tra nhãn tiếng Việt, quan hệ, bội số, kiểu dữ liệu, thanh thực thi và bố cục. Việc điều chỉnh bố cục trong trình biên tập không tự sửa các lỗi ngữ nghĩa của mô hình.

Khi giao tệp cho người dùng, cung cấp liên kết hoặc đường dẫn thực tế tới tệp XML. `present_files` trong hướng dẫn cũ là tên công cụ phụ thuộc môi trường, không phải một bước bắt buộc của bộ sinh này.

### Thuật ngữ sử dụng trong tài liệu

- **Model element**: phần tử mô hình, lưu dữ liệu về lớp, trạng thái, bảng hoặc quan hệ.
- **Diagram**: sơ đồ hoặc biểu đồ biểu diễn mô hình.
- **Shape**: hình biểu diễn của một phần tử trên sơ đồ.
- **Connector**: đường nối biểu diễn một quan hệ hoặc thông điệp.
- **Stereotype**: nhãn khuôn mẫu, như `boundary`, `control`, `entity` hoặc `enumeration`.
- **Multiplicity**: bội số của đầu quan hệ.
- **Lifeline**: đường sống trong biểu đồ tương tác.
- **Activation**: thanh thực thi; không phải trạng thái của đối tượng.
- **Combined fragment**: khung tương tác kết hợp; **operand** là một phần tương tác bên trong khung; **guard** là điều kiện gác.
- **Artifact**: hiện vật triển khai, chẳng hạn một tệp phần mềm được bố trí trên nút triển khai.
- **PK / FK**: khóa chính / khóa ngoại.

<a id="dac-ta-json"></a>

## Cấu trúc đặc tả JSON

### Nội dung tương ứng với references/spec-format.md

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

<a id="cau-truc-xml"></a>

## Cấu trúc XML và kiểm tra tham chiếu

### Nội dung tương ứng với references/xml-structure.md

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

<a id="kiem-tra"></a>

## Kết quả kiểm tra và các điểm đã sửa

Kết quả kiểm tra trong lần hiệu đính ngày 22 tháng 11 năm 2026:

- Cả 8 ví dụ JSON đi kèm đều sinh được XML và qua validator với 0 cảnh báo.
- Cả 5 tệp trong `references/real-samples` đều qua validator với 0 cảnh báo. Gói được cung cấp chứa 5 tệp XML mẫu, không phải 9 tệp như một câu trong hướng dẫn cũ.
- Trường hợp kiểm tra có cột `parentId` khai báo sẵn vẫn bị thêm một cột `parentId` nữa. Cột mới có chiều dài 10 thay vì 150 của cột tham chiếu; validator vẫn báo không có lỗi hoặc cảnh báo.
- Khi truyền `scale: 2` cho cột `decimal`, XML thử nghiệm vẫn có `Scale="0"`.
- Khi đặt `x: 9999` cho thành phần tham gia biểu đồ trình tự, vị trí xuất vẫn là vị trí do script tự tính.
- Khai báo lại lớp `A` với một thuộc tính khác trong sơ đồ sau không cập nhật thuộc tính của lớp đã tạo ở sơ đồ trước.
- Validator chạy không có đối số tệp trả mã thoát 0 và không in kết quả kiểm tra.

Những kết quả trên xác nhận công cụ chạy được với các ví dụ đã thử và giúp xác định giới hạn của hướng dẫn. Chúng không thay thế phép thử nhập XML vào Visual Paradigm; chưa thực hiện phép thử nhập đó trong lần hiệu đính này.

Các chỉnh sửa về ngôn ngữ gồm khôi phục toàn bộ tiêu đề và đoạn văn bị thay bằng dấu hỏi, thống nhất thuật ngữ tiếng Việt và giải thích các thuật ngữ tiếng Anh ở lần sử dụng. Các chỉnh sửa về nội dung gồm bỏ mức đánh giá độ tin cậy chưa có tiêu chí, sửa đường dẫn phụ thuộc môi trường, phân biệt kiểm tra tham chiếu với kiểm tra khả năng nhập và ghi rõ các hạn chế được xác nhận từ mã.

<a id="phu-luc"></a>

## Mã nguồn và tài nguyên nguyên gốc

Phần dưới giữ nguyên nội dung 17 tệp kỹ thuật trong gói để đối chiếu và khôi phục khi cần. Chú thích hoặc thông báo không dấu trong script nguyên gốc không phải phần hướng dẫn đã hiệu đính. Nếu nội dung chú thích cũ khẳng định nhiều hơn kết quả kiểm tra thực tế, áp dụng phạm vi đã nêu trong phần chính.

### `scripts/vpgen.py`

<details>
<summary>Mở nội dung tệp</summary>

```python
#!/usr/bin/env python3
"""vpgen.py - sinh file XML (Visual Paradigm "Project" XML, ExporterVersion 16.1.1)
tu mot JSON spec don gian, de import bang  File > Import > ... XML  trong Visual Paradigm.

Dung:
    python3 vpgen.py spec.json -o out.xml
Xem references/spec-format.md de biet cau truc spec.

Nguyen tac cot loi (rut ra tu cac file export that):
  * Moi phan tu model co Id 16 ky tu; shape/connector tren diagram co Id RIENG va
    tro ve model bang  Model= / MetaModelElement=.
  * Model.<MasterView> liet ke Idref cua cac shape/connector (khong phai Id cua model).
  * Connector.From / To la Id cua SHAPE; relationship model.From / To la Id cua MODEL.
  * Thuoc tinh XML duoc sap xep theo ASCII (giong VP).
"""
import argparse, copy, datetime, html, json, math, os, random, string, sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')
T = json.load(open(os.path.join(ASSETS, 'attr_templates.json'), encoding='utf8'))
HEADER = open(os.path.join(ASSETS, 'project_header.tmpl'), encoding='utf8').read()

ID_CHARS = string.ascii_letters + string.digits + '_'
PRIO = {'Stereotypes': 0, 'ActionType': 1, 'CoveredLifeLines': 1, 'SubDiagrams': 1, 'ModelChildren': 2,
        'Activations': 2, 'Messages': 2, 'ForeignKeyConstraints': 2, 'Guard': 3, 'VerticalPartitions': 3,
        'FromSimpleRelationships': 4, 'ToSimpleRelationships': 5, 'FromEnd': 6, 'ToEnd': 7, 'MasterView': 9}
BLUE = 'rgb(122, 207, 245)'
ORANGE = 'rgb(245, 182, 122)'
INT_MIN = '-2147483648'


def tw(s, k=7, pad=14, mn=20):
    return max(int(len(s or '') * k + pad), mn)


class Diagram(ET.Element):
    pass


class Gen:
    def __init__(self, spec):
        self.spec = spec
        p = spec.get('project', {})
        self.pname = p.get('name', 'Project')
        self.author = p.get('author', 'SinhVien')
        n = datetime.datetime.now()
        self.now = n.strftime('%Y-%m-%dT%H:%M:%S.') + '%03d' % (n.microsecond // 1000)
        self.ids = set()
        self.z = 0
        self.models = ET.Element('Models')
        self.diagrams = ET.Element('Diagrams')
        self.reg = {}          # (kind, name) -> model Element
        self.rel_containers = {}
        self.rel_root = None
        self.stereo = {}
        self.uses_orm = False
        for n_ in ['boolean', 'byte', 'char', 'double', 'float', 'int', 'long', 'short', 'void', 'string']:
            self.models.append(self.mk('m:DataType', Name=n_))

    # ---------- primitives ----------
    def nid(self):
        while True:
            i = ''.join(random.choice(ID_CHARS) for _ in range(16))
            if i not in self.ids:
                self.ids.add(i)
                return i

    def mk(self, key, **over):
        tag = key.split(':')[-1]
        a = copy.deepcopy(T[key][0])
        a.pop('Documentation', None)
        if 'Documentation_plain' in a:
            a['Documentation_plain'] = ''
        known = set(a)
        for k, v in over.items():
            if v is not None and (k in known or k + '_IsNull' in known or k in ('Documentation',)):
                a.pop(k + '_IsNull', None)
                a[k] = str(v).lower() if isinstance(v, bool) else str(v)
        for k in ('FromActivation', 'ToActivation', 'ParentFrame', 'ForeignKey', 'RefColumn'):
            if k not in over:
                a.pop(k, None)
        if 'Id' in a:
            a['Id'] = over.get('Id') or self.nid()
        if 'PmAuthor' in a:
            a['PmAuthor'] = self.author
        if 'PmCreateDateTime' in a:
            a['PmCreateDateTime'] = self.now
        if 'PmLastModified' in a:
            a['PmLastModified'] = self.now
        return ET.Element(tag, a)

    def doc(self, el, text):
        if text:
            el.set('Documentation', '<HTML><BODY><p style="margin-top: 0">%s</p></BODY></HTML>' % html.escape(text))
            el.set('Documentation_plain', text)

    def sub(self, parent, tag, **a):
        return ET.SubElement(parent, tag, {k: str(v) for k, v in a.items()})

    def ref(self, parent, tag, el_or_id, name=''):
        i = el_or_id.get('Id') if isinstance(el_or_id, ET.Element) else el_or_id
        return self.sub(parent, tag, Idref=i, Name=name)

    def mv(self, model_el, tag, shape_id, name='', mvtag=None):
        tag = mvtag or tag
        m = model_el.find('MasterView')
        if m is None:
            m = ET.SubElement(model_el, 'MasterView')
        if tag in ('Generalization', 'Dependency', 'InteractionLifeLineLink', 'Realization'):
            self.sub(m, tag, Idref=shape_id)       # VP khong ghi Name cho cac loai nay
        else:
            self.ref(m, tag, shape_id, name or '')

    def children(self, el):
        c = el.find('ModelChildren')
        return c if c is not None else ET.SubElement(el, 'ModelChildren')

    def rel_container(self, kind):
        if self.rel_root is None:
            self.rel_root = self.mk('m:ModelRelationshipContainer', Name='relationships')
            self.sub(self.rel_root, 'ModelChildren')
            self.models.append(self.rel_root)
        if kind not in self.rel_containers:
            c = self.mk('m:ModelRelationshipContainer', Name=kind)
            self.sub(c, 'ModelChildren')
            self.rel_root.find('ModelChildren').append(c)
            self.rel_containers[kind] = c
        return self.rel_containers[kind].find('ModelChildren')

    def stereotype(self, name, base):
        k = (name, base)
        if k not in self.stereo:
            s = self.mk('m:Stereotype', Name=name, BaseType=base)
            self.models.append(s)
            self.stereo[k] = s
        return self.stereo[k]

    def nz(self):
        self.z += 2
        return self.z

    # ---------- diagram / shape / connector building ----------
    def new_diagram(self, dtag, name, **over):
        d0 = self.mk('d:' + dtag, Name=name, **over)
        d = Diagram(d0.tag, d0.attrib)
        d.set('PmAuthor', self.author)
        for k in ('PmCreateDateTime', 'PmLastModified'):
            d.set(k, self.now)
        self.diagrams.append(d)
        d.shapes = ET.SubElement(d, 'Shapes')
        d.conns = ET.SubElement(d, 'Connectors')
        d.sh = {}   # name -> dict(id,x,y,w,h)
        return d

    def deco(self, el, cap, fill=BLUE, transp=0, comp=False, stroke='1.0'):
        self.sub(el, 'ElementFont', Color='rgb(0, 0, 0)', Name='Dialog', Size='11', Style='0')
        ln = self.sub(el, 'Line', Cap='0', Color='rgb(0, 0, 0)', Transparency='0', Weight=stroke)
        ET.SubElement(ln, 'Stroke')
        self.sub(el, 'Caption', Height=cap['h'], InternalHeight=INT_MIN, InternalWidth=INT_MIN,
                 Side=cap.get('side', 'None'), Visible=cap.get('vis', 'true'), Width=cap['w'],
                 X=cap['x'], Y=cap['y'])
        if fill:
            self.sub(el, 'FillColor', Color=fill, Style='1', Transparency=transp, Type='1')
        if comp:
            self.sub(el, 'CompartmentFont', Value='none')

    def shape(self, d, key, model, name, x, y, w, h, parent=None, cap_side='FreeMove', fill=BLUE,
              transp=0, comp=False, cap_h=15, cap_pos=None, mvtag=None, **over):
        sid = self.nid()
        mid = model.get('Id') if model is not None else None
        a = dict(Id=sid, Name=name, X=int(x), Y=int(y), Width=int(w), Height=int(h), ZOrder=self.nz())
        if mid:
            a.update(MetaModelElement=mid, Model=mid)
        a.update(over)
        el = self.mk('s:%s:%s' % (d.tag, key), **a)
        for k in ('MetaModelElement', 'Model'):
            if k in el.attrib and not mid:
                del el.attrib[k]
        (parent if parent is not None else d.shapes).append(el)
        cx, cy = cap_pos if cap_pos else (x, y)
        self.deco(el, dict(h=cap_h, w=w, x=int(cx), y=int(cy), side=cap_side,
                           vis='false' if cap_side == 'Invisible' else 'true'), fill, transp, comp)
        d.sh[name if name not in d.sh else '%s#%s' % (name, sid)] = dict(id=sid, x=x, y=y, w=w, h=h, el=el)
        if model is not None:
            self.mv(model, key, sid, name, mvtag)
        return sid

    @staticmethod
    def edge(a, b):
        ax, ay = a['x'] + a['w'] / 2, a['y'] + a['h'] / 2
        bx, by = b['x'] + b['w'] / 2, b['y'] + b['h'] / 2
        dx, dy = bx - ax, by - ay
        if dx == 0 and dy == 0:
            return ax, ay
        sx = (a['w'] / 2) / abs(dx) if dx else 1e9
        sy = (a['h'] / 2) / abs(dy) if dy else 1e9
        t = min(sx, sy)
        return round(ax + dx * t), round(ay + dy * t)

    def connector(self, d, key, model, name, fs, ts, pts=None, extra=None, assoc_ends=None, **over):
        """fs/ts: dict shape (co 'id'). pts: list (x,y) hoac None -> tu tinh."""
        if pts is None:
            if fs is ts:
                x, y, w, h = fs['x'], fs['y'], fs['w'], fs['h']
                pts = [(x + 40, y), (x + 40, y - 40), (x + w + 50, y - 40), (x + w + 50, y + h / 2), (x + w, y + h / 2)]
            else:
                pts = [self.edge(fs, ts), self.edge(ts, fs)]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        cid = self.nid()
        a = dict(Id=cid, From=fs['id'], To=ts['id'], X=int(min(xs) - 50), Y=int(min(ys) - 50),
                 Width=int(max(xs) - min(xs) + 100), Height=int(max(ys) - min(ys) + 100), ZOrder=self.nz())
        if model is not None:
            a.update(MetaModelElement=model.get('Id'), Model=model.get('Id'))
        if name or name == '':
            a['Name'] = name
        a.update(over)
        if extra:
            a.update(extra)
        el = self.mk('c:%s:%s' % (d.tag, key), **a)
        if not name and 'Name' in el.attrib and key not in ('Association',):
            pass
        d.conns.append(el)
        mx, my = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        if assoc_ends:
            ma, mb = assoc_ends
            self.sub(el, 'MultiplicityBRectangle', Height=40, Width=40, X=int(pts[-1][0] - 20), Y=int(pts[-1][1] - 20))
            self.sub(el, 'MultiplicityARectangle', Height=40, Width=40, X=int(pts[0][0] - 20), Y=int(pts[0][1] - 20))
        cw = tw(name) if name else 20
        self.deco(el, dict(h=15 if name else 0, w=cw, x=int(mx - cw / 2), y=int(my - 21), side='None'), fill=None)
        if assoc_ends:
            ra = self.sub(el, 'RoleA')
            self.sub(ra, 'MultiplicityCaption', Height=40, Width=40, X=int(pts[0][0] - 20), Y=int(pts[0][1] - 20))
            rb = self.sub(el, 'RoleB')
            self.sub(rb, 'MultiplicityCaption', Height=40, Width=40, X=int(pts[-1][0] - 20), Y=int(pts[-1][1] - 20))
        pe = self.sub(el, 'Points')
        for (px, py) in pts:
            self.sub(pe, 'Point', X='%.1f' % px, Y='%.1f' % py)
        if model is not None:
            self.mv(model, key, cid, name or '')
        return cid, el

    @staticmethod
    def grid(i, n, cw=240, ch=170, x0=60, y0=60, cols=None):
        cols = cols or max(1, math.ceil(math.sqrt(n)))
        return x0 + (i % cols) * cw, y0 + (i // cols) * ch

    # ================= CLASS =================
    def class_el(self, c):
        k = ('class', c['name'])
        if k in self.reg:
            return self.reg[k]
        el = self.mk('m:Class', Name=c['name'], Visibility=c.get('visibility', 'public'),
                     Abstract=c.get('abstract', False))
        self.doc(el, c.get('documentation'))
        st = c.get('stereotype')
        if st:
            s = self.stereotype(st, 'Class')
            self.ref(self.sub(el, 'Stereotypes'), 'Stereotype', s, st)
        mc = self.sub(el, 'ModelChildren')
        for a in c.get('attributes', []):
            ae = self.mk('m:Attribute', Name=a['name'], Type=a.get('type', 'String'),
                         Visibility=a.get('visibility', 'private'), Scope='classifier' if a.get('static') else 'instance',
                         Multiplicity=a.get('multiplicity', 'Unspecified'))
            self.doc(ae, a.get('documentation'))
            mc.append(ae)
        for o in c.get('operations', []):
            oe = self.mk('m:Operation', Name=o['name'], ReturnType=o.get('returnType', 'void'),
                         Visibility=o.get('visibility', 'public'), Static=o.get('static', False),
                         Abstract=o.get('abstract', False), Scope='classifier' if o.get('static') else 'instance')
            self.doc(oe, o.get('documentation'))
            pc = self.sub(oe, 'ModelChildren')
            for p in o.get('params', []):
                pc.append(self.mk('m:Parameter', Name=p['name'], Type=p.get('type', 'String'),
                                  Direction=p.get('direction', 'in')))
            if not len(pc):
                oe.remove(pc)
            mc.append(oe)
        if not len(mc):
            el.remove(mc)
        self.models.append(el)
        self.reg[k] = el
        return el

    def class_size(self, c):
        st = c.get('stereotype')
        if st in ('boundary', 'control', 'entity'):
            return 80, 40
        na, no = len(c.get('attributes', [])), len(c.get('operations', []))
        texts = [c['name']] + ['- %s : %s' % (a['name'], a.get('type', '')) for a in c.get('attributes', [])] + \
                ['+ %s()' % o['name'] for o in c.get('operations', [])]
        w = max(80, max(len(t) for t in texts) * 7 + 20)
        h = max(38, 23 + 15 * (na + no) + (8 if na and no else 0)) + (11 if st else 0)
        return w, h

    def build_class(self, d):
        dg = self.new_diagram('ClassDiagram', d['name'])
        self.uses_orm = True
        classes = d.get('classes', [])
        for i, c in enumerate(classes):
            known = ('class', c['name']) in self.reg
            full = c if (not known or c.get('attributes') or c.get('operations') or c.get('stereotype')) else \
                {'name': c['name']}
            el = self.class_el(full)
            if known and not (c.get('attributes') or c.get('operations')):
                # lay lai thong tin kich thuoc tu model
                full = dict(c)
            w, h = self.class_size(c)
            x, y = (c['x'], c['y']) if 'x' in c else self.grid(i, len(classes), 260, 200)
            icon = c.get('stereotype') in ('boundary', 'control', 'entity')
            self.shape(dg, 'Class', el, c['name'], x, y, w, h, cap_side='South' if (icon or c.get('stereotype')) else 'FreeMove',
                       comp=True, cap_h=30 if c.get('stereotype') else 15,
                       cap_pos=(x - 4, y + h) if icon else None)
        for r in d.get('relationships', []):
            self.class_rel(dg, r)

    def class_rel(self, dg, r):
        kind = r.get('kind', 'association')
        fc, tc = self.reg[('class', r['from'])], self.reg[('class', r['to'])]
        fs, ts = dg.sh[r['from']], dg.sh[r['to']]
        name = r.get('name', '')
        k = (kind, r['from'], r['to'], name)
        if kind == 'generalization':
            el = self.reg.get(k)
            if el is None:
                el = self.mk('m:Generalization', From=fc.get('Id'), To=tc.get('Id'))   # From = con, To = cha
                self.rel_container('Generalization').append(el)
                self.ref(self.sub_once(fc, 'FromSimpleRelationships'), 'Generalization', el)
                self.ref(self.sub_once(tc, 'ToSimpleRelationships'), 'Generalization', el)
                self.reg[k] = el
            self.connector(dg, 'Generalization', el, None, fs, ts)
            return
        el = self.reg.get(k)
        if el is None:
            el = self.mk('m:Association', Name=name, EndRelationshipFromMetaModelElement=fc.get('Id'),
                         EndRelationshipToMetaModelElement=tc.get('Id'), Direction='From To')
            for side, cls, m, nav, agg in (
                    ('FromEnd', fc, r.get('fromMultiplicity', 'Unspecified'), r.get('fromNavigable', 'Unspecified'),
                     {'aggregation': 'Shared', 'composition': 'Composite'}.get(kind, 'None')),
                    ('ToEnd', tc, r.get('toMultiplicity', 'Unspecified'), r.get('toNavigable', 'Navigable'), 'None')):
                end = self.sub(el, side)
                ae = self.mk('m:AssociationEnd', EndModelElement=cls.get('Id'), Multiplicity=m, Navigable=nav,
                             AggregationKind=agg)
                if side == 'FromEnd' and r.get('fromRole'):
                    ae.set('Name', r['fromRole'])
                if side == 'ToEnd' and r.get('toRole'):
                    ae.set('Name', r['toRole'])
                end.append(ae)
                q = self.sub(ae, 'Qualifier')
                q.append(self.mk('m:Qualifier'))
                self.ref(self.sub(ae, 'Type'), 'Class', cls, cls.get('Name'))
            self.rel_container('Association').append(el)
            self.reg[k] = el
        has_m = any(r.get(x) for x in ('fromMultiplicity', 'toMultiplicity'))
        ex = dict(HasMultiplicityAShape='true', HasMultiplicityBShape='true') if has_m else {}
        # chon bien the connector co RoleA/RoleB khi co multiplicity
        self.connector(dg, 'Association', el, name, fs, ts, extra=ex, assoc_ends=(1, 1) if has_m else None)

    def sub_once(self, el, tag):
        e = el.find(tag)
        return e if e is not None else ET.SubElement(el, tag)

    # ================= STATE =================
    def build_state(self, d):
        dg = self.new_diagram('StateDiagram', d['name'])
        nodes = []
        if d.get('initial', True):
            nodes.append(('InitialPseudoState', 'initial', ''))
        for s in d.get('states', []):
            nodes.append(('State2', s['name'], s))
        for f in d.get('finals', []):
            nodes.append(('FinalState2', f if isinstance(f, str) else f['name'], {}))
        els = {}
        for i, (tag, name, s) in enumerate(nodes):
            nm = '' if tag == 'InitialPseudoState' else name
            el = self.mk('m:' + tag, Name=nm)
            if tag == 'State2':
                self.doc(el, s.get('documentation'))
            self.models.append(el)
            els[name] = el
            if 'x' in s if isinstance(s, dict) else False:
                x, y = s['x'], s['y']
            else:
                x, y = 50 + i * 250, 170
            if tag == 'State2':
                w, h = max(160, tw(name, 8, 40)), 50
                self.shape(dg, tag, el, nm, x, y, w, h, cap_side='None', cap_h=15)
            else:
                self.shape(dg, tag, el, nm, x, y, 20, 20, cap_side='None', cap_h=0 if tag == 'InitialPseudoState' else 15,
                           fill='rgb(0, 0, 0)')
            dg.sh['@' + name] = dg.sh[nm]
        for t in d.get('transitions', []):
            fn = 'initial' if t['from'] in ('initial', '[*]') else t['from']
            tn = t['to']
            fe, te = els[fn], els[tn]
            tr = self.mk('m:Transition2', From=fe.get('Id'), To=te.get('Id'), Name=t.get('name', ''), Kind='External')
            self.rel_container('Transition2').append(tr)
            self.ref(self.sub_once(fe, 'FromSimpleRelationships'), 'Transition2', tr, t.get('name', ''))
            self.ref(self.sub_once(te, 'ToSimpleRelationships'), 'Transition2', tr, t.get('name', ''))
            self.connector(dg, 'Transition2', tr, t.get('name', ''), dg.sh['@' + fn], dg.sh['@' + tn])

    # ================= SEQUENCE / COMMUNICATION =================
    def _seq_data(self, d):
        parts = {}
        for i, p in enumerate(d['participants']):
            kind = p.get('kind', 'lifeline')
            w = 60 if kind == 'actor' else max(90, tw(p['name'], 7, 24))
            parts[p['name']] = dict(spec=p, kind=kind, cx=120 + i * 230, w=w, acts=[], stack=[])
        ycur = 130
        rows = []
        msgs = d['messages']
        counter = 0

        def new_act(pt, y, caller=None):
            a = dict(mid=self.nid(), sid=self.nid(), part=pt, y0=y, y1=y, caller=caller)
            pt['acts'].append(a)
            pt['stack'].append(a)
            return a

        def touch(a, y):
            if a:
                a['y0'] = min(a['y0'], y)
                a['y1'] = max(a['y1'], y)
        for idx, m in enumerate(msgs):
            kind = m.get('kind', 'call')
            s, t = parts[m['from']], parts[m['to']]
            y = ycur
            ycur += 70 if kind == 'self' else 50
            counter += 1 if kind != 'self' or True else 0
            if kind == 'return':
                af = s['stack'][-1] if s['stack'] else None
                at = af['caller'] if af else None
                nxt = msgs[idx + 1] if idx + 1 < len(msgs) else None
                if af and not (nxt and nxt.get('kind') == 'return' and nxt['from'] == m['from']):
                    s['stack'].pop()
            elif kind == 'self':
                af = s['stack'][-1] if s['stack'] else (new_act(s, y) if s['kind'] == 'lifeline' else None)
                at = af
            else:
                af = s['stack'][-1] if s['stack'] else (new_act(s, y) if s['kind'] == 'lifeline' else None)
                at = new_act(t, y, af) if t['kind'] == 'lifeline' else None
            touch(af, y)
            touch(at, y + (26 if kind == 'self' else 0))
            rows.append(dict(m=m, kind=kind, y=y, af=af, at=at, s=s, t=t, seq=m.get('seq') or str(counter)))
        return parts, rows, ycur

    def build_sequence(self, d, comm=False):
        parts, rows, yend = self._seq_data(d)
        frame = self.mk('m:Frame', Name=d.get('frame', d['name']), Type='sd', BaseY='40')
        self.models.append(frame)
        fmc = self.sub(frame, 'ModelChildren')
        dg = self.new_diagram('CommunicationDiagram' if comm else 'InteractionDiagram', d['name'])
        height = yend + 60
        # ---- model: participants
        for nm, pt in parts.items():
            sp = pt['spec']
            if pt['kind'] == 'actor':
                pt['el'] = self.mk('m:InteractionActor', Name=nm)
            else:
                pt['el'] = self.mk('m:InteractionLifeLine', Name=nm)
                if sp.get('stereotype'):
                    s = self.stereotype(sp['stereotype'], 'InteractionLifeLine')
                    self.ref(self.sub(pt['el'], 'Stereotypes'), 'Stereotype', s, sp['stereotype'])
                if pt['acts']:
                    ac = self.sub(pt['el'], 'Activations')
                    for a in pt['acts']:
                        ae = self.mk('m:Activation', Id=a['mid'])
                        ac.append(ae)
                        a['el'] = ae
            fmc.append(pt['el'])
        # ---- model: messages
        links = {}
        for r in rows:
            m = r['m']
            s, t = r['s'], r['t']
            over = dict(Name=m['text'], SequenceNumber=r['seq'], EndRelationshipFromMetaModelElement=s['el'].get('Id'),
                        EndRelationshipToMetaModelElement=t['el'].get('Id'),
                        Type='Self Message' if r['kind'] == 'self' else 'Message',
                        Asynchronous=r['kind'] == 'async')
            if r['af']:
                over['FromActivation'] = r['af']['mid']
            if r['at']:
                over['ToActivation'] = r['at']['mid']
            me = self.mk('m:Message', **over)
            if r['kind'] == 'return':
                at_ = self.sub(me, 'ActionType')
                at_.append(self.mk('m:ActionTypeReturn'))
            fe, te = self.sub(me, 'FromEnd'), self.sub(me, 'ToEnd')
            fe.append(self.mk('m:MessageEnd', EndModelElement=s['el'].get('Id')))
            te.append(self.mk('m:MessageEnd', EndModelElement=t['el'].get('Id')))
            r['el'] = me
            if comm:
                key = tuple(sorted([m['from'], m['to']]))
                if key not in links:
                    f, t_ = (m['from'], m['to'])
                    le = self.mk('m:InteractionLifeLineLink', EndRelationshipFromMetaModelElement=parts[f]['el'].get('Id'),
                                 EndRelationshipToMetaModelElement=parts[t_]['el'].get('Id'))
                    for side, nme in (('FromEnd', f), ('ToEnd', t_)):
                        e = self.sub(le, side)
                        e.append(self.mk('m:InteractionLifeLineLinkEnd', EndModelElement=parts[nme]['el'].get('Id')))
                    self.sub(le, 'ModelChildren')
                    self.rel_container('InteractionLifeLineLink').append(le)
                    links[key] = dict(el=le, f=f, t=t_)
                links[key]['el'].find('ModelChildren').append(me)
                r['link'] = links[key]
            else:
                self.rel_container('Message').append(me)
        # ---- model: combined fragments
        frags = []
        for fg in d.get('fragments', []):
            covered = []
            for i in range(fg['from'], fg['to'] + 1):
                for nm in (rows[i]['m']['from'], rows[i]['m']['to']):
                    if parts[nm]['kind'] == 'lifeline' and nm not in covered:
                        covered.append(nm)
            fe = self.mk('m:CombinedFragment', Name='', OperatorKind=fg.get('operator', 'alt'))
            cl = self.sub(fe, 'CoveredLifeLines')
            for nm in covered:
                self.ref(cl, 'InteractionLifeLine', parts[nm]['el'], nm)
            fmc2 = self.sub(fe, 'ModelChildren')
            ops = []
            for k, op in enumerate(fg['operands']):
                oe = self.mk('m:InteractionOperand', Name='Operand' if k == 0 else 'Operand%d' % (k + 1))
                ms = self.sub(oe, 'Messages')
                for i in range(op['from'], op['to'] + 1):
                    self.ref(ms, 'Message', rows[i]['el'], rows[i]['m']['text'])
                g = self.sub(oe, 'Guard')
                if op.get('guard'):
                    g.append(self.mk('m:InteractionConstraint', Constraint=op['guard']))
                    g[-1].attrib.pop('Constraint_IsNull', None)
                else:
                    g.append(self.mk('m:InteractionConstraint'))
                fmc2.append(oe)
                ops.append((oe, op))
            fmc.append(fe)
            frags.append((fe, fg, covered, ops))
        # ---- diagram shapes
        sid = {}
        if comm:
            return self._comm_shapes(dg, parts, rows, links, frame)
        for fe, fg, covered, ops in frags:
            xs0 = min(parts[n]['cx'] - parts[n]['w'] / 2 for n in covered) - 20
            xs1 = max(parts[n]['cx'] + parts[n]['w'] / 2 for n in covered) + 20
            y0 = rows[fg['from']]['y'] - 30
            y1 = rows[fg['to']]['y'] + (70 if rows[fg['to']]['kind'] == 'self' else 40)
            starts = [rows[op['from']]['y'] - 30 for _, op in ops] + [y1]
            starts[0] = y0
            for k, (oe, op) in enumerate(ops):
                self.shape(dg, 'InteractionOperand', oe, oe.get('Name'), xs0, starts[k], xs1 - xs0, starts[k + 1] - starts[k],
                           cap_side='Invisible', cap_h=starts[k + 1] - starts[k])
                dg.sh['op:%s' % oe.get('Id')] = dg.sh[oe.get('Name')]
            fg['_box'] = (xs0, y0, xs1 - xs0, y1 - y0, fe)
        for pt in parts.values():
            for a in pt['acts']:
                self.shape(dg, 'Activation', a['el'], 'Activation', pt['cx'] - 4, a['y0'], 8, max(a['y1'] - a['y0'] + 30, 40),
                           cap_side='Invisible', fill=BLUE, cap_pos=(pt['cx'] - 4, a['y0'] + 4))
                a['shape'] = dg.sh['Activation'] if 'Activation' in dg.sh else None
                a['sdict'] = dict(id=dg.shapes[-1].get('Id'))
                dg.sh.pop('Activation', None)
        for fe, fg, covered, ops in frags:
            x, y, w, h, fe_ = fg['_box']
            self.shape(dg, 'CombinedFragment', fe_, '', x, y, w, h, cap_side='FreeMove', cap_h=18, transp=100,
                       fill='rgba(122, 207, 245, 0.0)', cap_pos=(0, 0))
        fid = frame.get('Id')
        for nm, pt in parts.items():
            if pt['kind'] == 'actor':
                sidv = self.shape(dg, 'InteractionActor', pt['el'], nm, pt['cx'] - 30, 40, 60, height - 40, cap_side='None',
                                  cap_pos=(pt['cx'] - 32, 75), ParentFrame=fid)
            else:
                sidv = self.shape(dg, 'InteractionLifeLine', pt['el'], nm, pt['cx'] - pt['w'] / 2, 40, pt['w'], height - 40,
                                  cap_side='South', cap_pos=(pt['cx'] - pt['w'] / 2, 75), ParentFrame=fid, ShowClassifier='true')
            pt['sid'] = sidv
        # ---- connectors (messages)
        for r in rows:
            s, t = r['s'], r['t']
            y = r['y']
            if r['kind'] == 'self':
                x = s['cx'] + 4
                pts = [(x, y), (x + 48, y), (x + 48, y + 26), (x, y + 26)]
            else:
                right = t['cx'] > s['cx']
                xs_ = s['cx'] + (4 if right else -4) if r['af'] else s['cx']
                xe_ = t['cx'] - (4 if right else -4) if r['at'] else t['cx']
                pts = [(xs_, y), (xe_, y)]
            fsd = dict(id=s['sid'])
            tsd = dict(id=t['sid'])
            self.connector(dg, 'Message', r['el'], r['m']['text'], fsd, tsd, pts=pts)

    def _comm_shapes(self, dg, parts, rows, links, frame):
        n = len(parts)
        for i, (nm, pt) in enumerate(parts.items()):
            x, y = (pt['spec']['x'], pt['spec']['y']) if 'x' in pt['spec'] else (80 + (i % 3) * 300, 80 + (i // 3) * 220)
            if pt['kind'] == 'actor':
                pt['sid'] = self.shape(dg, 'CommunicationActor', pt['el'], nm, x, y, 30, 60, cap_side='South', cap_pos=(x - 30, y + 60), mvtag='InteractionActor')
            else:
                w = max(79, tw(nm, 7, 24))
                pt['sid'] = self.shape(dg, 'CommunicationLifeLine', pt['el'], nm, x, y, w, 40, cap_side='South',
                                       cap_pos=(x, y + 40), mvtag='InteractionLifeLine')
            pt['box'] = dict(id=pt['sid'], x=x, y=y, w=30 if pt['kind'] == 'actor' else max(79, tw(nm, 7, 24)),
                             h=60 if pt['kind'] == 'actor' else 40)
        for key, lk in links.items():
            fb, tb = parts[lk['f']]['box'], parts[lk['t']]['box']
            cid, cel = self.connector(dg, 'InteractionLifeLineLink', lk['el'], None, fb, tb)
            cel.attrib.pop('Name', None)
            kids = self.sub(cel, 'DiagramElementChildren')
            cel.remove(kids)
            cel.insert(list(cel).index(cel.find('Points')), kids)
            pa, pb = self.edge(fb, tb), self.edge(tb, fb)
            msgs = [r for r in rows if r.get('link') is lk]
            for j, r in enumerate(msgs):
                fwd = r['m']['from'] == lk['f']
                key_ = 'CommunicationMessage' if fwd else 'CommunicationReverseMessage'
                mx = (pa[0] + pb[0]) / 2 - 30
                my = (pa[1] + pb[1]) / 2 + 20 * j - 30
                text = '%s: %s' % (r['seq'], r['m']['text'])
                a = dict(Id=self.nid(), MetaModelElement=r['el'].get('Id'), Model=r['el'].get('Id'), Name=r['m']['text'],
                         X=int(mx), Y=int(my), Width=60, Height=60, ZOrder=self.nz())
                me = self.mk('c:CommunicationDiagram:' + key_, **a)
                kids.append(me)
                self.deco(me, dict(h=15, w=tw(text), x=int(mx - 30), y=int(my - 8), side='None'), fill='rgb(0, 0, 0)')
                self.mv(r['el'], 'Message', a['Id'], r['m']['text'])

    # ================= PACKAGE =================
    def build_package(self, d):
        wrapper = self.mk('m:Model', Name=d['name'])
        self.models.append(wrapper)
        dg = self.new_diagram('PackageDiagram', d['name'])
        self.sub(self.sub(wrapper, 'SubDiagrams'), 'PackageDiagram', Idref=dg.get('Id'))
        mc = self.sub(wrapper, 'ModelChildren')
        pk = {}
        for p in d['packages']:
            el = self.mk('m:Package', Name=p['name'])
            pk[p['name']] = (el, p)
            parent = pk[p['parent']][0] if p.get('parent') else wrapper
            self.children(parent).append(el)
        tops = [n for n, (e, p) in pk.items() if not p.get('parent')]
        shape_parent = {}
        for i, n in enumerate(tops):
            el, p = pk[n]
            kids = [k for k, (e, q) in pk.items() if q.get('parent') == n]
            x, y = (p['x'], p['y']) if 'x' in p else self.grid(i, len(tops), 280, 220)
            w = max(140, tw(n, 8, 30)) if not kids else max(300, 140 * len(kids) + 40)
            h = 60 if not kids else 160
            sid = self.shape(dg, 'Package', el, n, x, y, w, h, cap_side='FreeMove')
            shape_parent[n] = dg.sh[n]
            if kids:
                dec = self.sub(dg.sh[n]['el'], 'DiagramElementChildren')
                dg.sh[n]['el'].remove(dec)
                dg.sh[n]['el'].insert(list(dg.sh[n]['el']).index(dg.sh[n]['el'].find('FillColor')), dec)
                for j, k in enumerate(kids):
                    kel, kp = pk[k]
                    self.shape(dg, 'Package', kel, k, x + 20 + j * 140, y + 50, 120, 60, parent=dec, cap_side='FreeMove')
        for dep in d.get('dependencies', []):
            fe, te = pk[dep['from']][0], pk[dep['to']][0]
            de = self.mk('m:Dependency', From=fe.get('Id'), To=te.get('Id'), Name=dep.get('name', ''))
            self.rel_container('Dependency').append(de)
            self.ref(self.sub_once(fe, 'FromSimpleRelationships'), 'Dependency', de)
            self.ref(self.sub_once(te, 'ToSimpleRelationships'), 'Dependency', de)
            self.connector(dg, 'Dependency', de, dep.get('name', ''), dg.sh[dep['from']], dg.sh[dep['to']])

    # ================= ER =================
    def build_er(self, d):
        dg = self.new_diagram('ERDiagram', d['name'])
        self.uses_orm = True
        tabs = {}
        for i, t in enumerate(d['tables']):
            el = self.mk('m:DBTable', Name=t['name'])
            mc = self.sub(el, 'ModelChildren')
            cols = {}
            for c in t.get('columns', []):
                ce = self.mk('m:DBColumn', Name=c['name'], Type=c.get('type', 'integer'),
                             PrimaryKey=bool(c.get('pk')), Nullable=bool(c.get('nullable', not c.get('pk'))),
                             Unique=bool(c.get('unique')), Length=c.get('length', 10))
                mc.append(ce)
                cols[c['name']] = ce
            self.models.append(el)
            x, y = (t['x'], t['y']) if 'x' in t else self.grid(i, len(d['tables']), 260, 220)
            w = max(110, max([len(c['name']) + len(c.get('type', 'integer')) for c in t.get('columns', [])] + [8]) * 8 + 40)
            h = 40 + 20 * max(len(t.get('columns', [])), 1)
            self.shape(dg, 'DBTable', el, t['name'], x, y, w, h, fill=ORANGE, comp=True)
            tabs[t['name']] = dict(el=el, cols=cols, spec=t)
        fk_proto = next((v for v in T['m:DBColumn'] if 'IdGenerator' in v), T['m:DBColumn'][0])
        for fk in d.get('foreignKeys', []):
            parent, child = tabs[fk['from']], tabs[fk['to']]   # from = bang tham chieu (PK), to = bang giu FK
            pkcol = fk.get('refColumn') or next((n for n, c in parent['cols'].items() if c.get('PrimaryKey') == 'true'), None)
            fe = self.mk('m:DBForeignKey', From=parent['el'].get('Id'), To=child['el'].get('Id'),
                         FromMultiplicity=fk.get('fromMultiplicity', '1'), ToMultiplicity=fk.get('toMultiplicity', '0..*'),
                         Identifying=bool(fk.get('identifying')), Name=fk.get('name', ''))
            self.rel_container('DBForeignKey').append(fe)
            colname = fk.get('column') or (fk['from'] + (pkcol[0].upper() + pkcol[1:] if pkcol else 'Id'))
            ce = self.mk('m:DBColumn', Name=colname, Type=parent['cols'][pkcol].get('Type', 'integer') if pkcol else 'integer',
                         Nullable=bool(fk.get('nullable', True)))
            for k, v in fk_proto.items():
                if k in ('ForeignKeyNamePattern', 'IdGenerator'):
                    ce.set(k, v)
            ce.attrib.pop('ForeignKeyNamePattern_IsNull', None)
            ce.attrib.pop('IdGenerator_IsNull', None)
            fc = self.sub(ce, 'ForeignKeyConstraints')
            fc.append(self.mk('m:DBForeignKeyConstraint', ForeignKey=fe.get('Id'),
                              RefColumn=parent['cols'][pkcol].get('Id') if pkcol else ''))
            self.children(child['el']).append(ce)
            self.ref(self.sub_once(parent['el'], 'FromSimpleRelationships'), 'DBForeignKey', fe)
            self.ref(self.sub_once(child['el'], 'ToSimpleRelationships'), 'DBForeignKey', fe)
            self.connector(dg, 'DBForeignKey', fe, '', dg.sh[fk['from']], dg.sh[fk['to']])

    # ================= DEPLOYMENT =================
    def build_deployment(self, d):
        wrapper = self.mk('m:Model', Name=d['name'])
        self.models.append(wrapper)
        dg = self.new_diagram('DeploymentDiagram', d['name'])
        self.sub(self.sub(wrapper, 'SubDiagrams'), 'DeploymentDiagram', Idref=dg.get('Id'))
        self.sub(wrapper, 'ModelChildren')
        els = {}
        for i, n in enumerate(d['nodes']):
            ne = self.mk('m:Node', Name=n['name'])
            self.children(wrapper).append(ne)
            els[n['name']] = ne
            kids = n.get('children', [])
            for k in kids:
                tag = 'Component' if k.get('kind', 'component') == 'component' else 'Artifact'
                ke = self.mk('m:' + tag, Name=k['name'])
                self.children(ne).append(ke)
                els[k['name']] = ke
            x, y = (n['x'], n['y']) if 'x' in n else self.grid(i, len(d['nodes']), 320, 260)
            w, h = max(220, 150 * len(kids) + 40), 200
            self.shape(dg, 'Node', ne, n['name'], x, y, w, h, comp=True)
            if kids:
                dec = self.sub(dg.sh[n['name']]['el'], 'DiagramElementChildren')
                nel = dg.sh[n['name']]['el']
                nel.remove(dec)
                nel.insert(list(nel).index(nel.find('FillColor')), dec)
                for j, k in enumerate(kids):
                    tag = 'Component' if k.get('kind', 'component') == 'component' else 'Artifact'
                    self.shape(dg, tag, els[k['name']], k['name'], x + 20 + j * 150, y + 60, 130, 70, parent=dec,
                               cap_side='InsideNorth' if tag == 'Component' else 'FreeMove', comp=(tag == 'Component'))
        for a in d.get('associations', []):
            fe, te = els[a['from']], els[a['to']]
            ae = self.mk('m:Association', Name=a.get('name', ''), EndRelationshipFromMetaModelElement=fe.get('Id'),
                         EndRelationshipToMetaModelElement=te.get('Id'), Direction='From To')
            for side, el_ in (('FromEnd', fe), ('ToEnd', te)):
                e = self.sub(ae, side)
                x_ = self.mk('m:AssociationEnd', EndModelElement=el_.get('Id'))
                e.append(x_)
                q = self.sub(x_, 'Qualifier')
                q.append(self.mk('m:Qualifier'))
                tag = el_.tag
                self.ref(self.sub(x_, 'Type'), tag, el_, el_.get('Name'))
            self.rel_container('Association').append(ae)
            self.connector(dg, 'Association', ae, a.get('name', ''), dg.sh[a['from']], dg.sh[a['to']])
        for a in d.get('dependencies', []):
            fe, te = els[a['from']], els[a['to']]
            de = self.mk('m:Dependency', From=fe.get('Id'), To=te.get('Id'), Name=a.get('name', ''))
            self.rel_container('Dependency').append(de)
            self.ref(self.sub_once(fe, 'FromSimpleRelationships'), 'Dependency', de)
            self.ref(self.sub_once(te, 'ToSimpleRelationships'), 'Dependency', de)
            self.connector(dg, 'Dependency', de, a.get('name', ''), dg.sh[a['from']], dg.sh[a['to']])

    # ================= ACTIVITY (chi cac node co mau that) =================
    def build_activity(self, d):
        dg = self.new_diagram('ActivityDiagram', d['name'])
        for i, a in enumerate(d.get('actions', [])):
            el = self.mk('m:ActivityAction', Name=a['name'])
            self.models.append(el)
            x, y = (a['x'], a['y']) if 'x' in a else (60 + i * 140, 60)
            self.shape(dg, 'ActivityAction', el, a['name'], x, y, max(60, tw(a['name'], 7, 20)), 40, cap_side='Center', cap_h=40,
                       cap_pos=(0, 0))
        for i, o in enumerate(d.get('objectNodes', [])):
            el = self.mk('m:ObjectNode', Name=o['name'])
            self.models.append(el)
            x, y = (o['x'], o['y']) if 'x' in o else (60 + i * 140, 200)
            self.shape(dg, 'ObjectNode', el, o['name'], x, y, 80, 40, cap_side='FreeMove', cap_pos=(0, 0))

    # ---------- finish ----------
    def build(self):
        fn = dict(class_=self.build_class, state=self.build_state, sequence=self.build_sequence,
                  communication=lambda d: self.build_sequence(d, comm=True), package=self.build_package,
                  er=self.build_er, deployment=self.build_deployment, activity=self.build_activity)
        for d in self.spec['diagrams']:
            t = d['type'].replace('class', 'class_') if d['type'] == 'class' else d['type']
            fn[t](d)

    @staticmethod
    def order(el):
        kids = list(el)
        if any(c.tag in PRIO for c in kids):
            kids.sort(key=lambda c: PRIO.get(c.tag, 5))
            for c in list(el):
                el.remove(c)
            for c in kids:
                el.append(c)
        for c in el:
            Gen.order(c)

    @staticmethod
    def sort_attrs(el):
        items = sorted(el.attrib.items())
        el.attrib.clear()
        el.attrib.update(items)
        for c in el:
            Gen.sort_attrs(c)

    def xml(self):
        self.build()
        self.order(self.models)
        for dg in self.diagrams:
            for sec in list(dg):
                if sec.tag in ('Shapes', 'Connectors') and not len(sec):
                    dg.remove(sec)
        for root in (self.models, self.diagrams):
            self.sort_attrs(root)
        orm = '<OrmInfo DefaultDatabase="1" SupportDatabases="0"/>\n\t\t' if self.uses_orm else ''
        head = (HEADER.replace('{NAME}', html.escape(self.pname, quote=True))
                .replace('{AUTHOR}', html.escape(self.author, quote=True)).replace('{ORMINFO}', orm))
        out = [head]
        for root in (self.models, self.diagrams):
            ET.indent(root, space='\t', level=1)
            out.append('\t' + ET.tostring(root, encoding='unicode') + '\n')
        out.append('</Project>\n')
        return ''.join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('spec')
    ap.add_argument('-o', '--out', default='project.xml')
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding='utf8'))
    xml = Gen(spec).xml()
    open(a.out, 'w', encoding='utf8', newline='\n').write(xml)
    print('Da ghi', a.out, '(%d bytes)' % len(xml.encode('utf8')))


if __name__ == '__main__':
    main()
```

</details>

### `scripts/validate_vp.py`

<details>
<summary>Mở nội dung tệp</summary>

```python
#!/usr/bin/env python3
"""validate_vp.py - kiem tra tinh toan ven tham chieu cua file XML Visual Paradigm.

Dung:  python3 validate_vp.py file.xml [file2.xml ...]
Thoat 0 neu khong co loi; 1 neu co loi. Chay lai tren file export that cung cho 0 loi.
"""
import sys
import xml.etree.ElementTree as ET

REF_ATTRS = ['From', 'To', 'Model', 'MetaModelElement', 'EndModelElement', 'EndRelationshipFromMetaModelElement',
             'EndRelationshipToMetaModelElement', 'ToActivation', 'FromActivation', 'ForeignKey', 'RefColumn',
             'ParentFrame', 'VerticalPartitionId']


def check(path):
    errs, warns = [], []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return ['XML khong hop le: %s' % e], []
    if root.tag != 'Project':
        errs.append('Root phai la <Project>, hien la <%s>' % root.tag)
    for need in ('ProjectInfo', 'Models', 'Diagrams'):
        if root.find(need) is None:
            errs.append('Thieu <%s>' % need)
    ids = {}
    for e in root.iter():
        i = e.get('Id')
        if i is not None:
            if i in ids:
                errs.append('Id trung: %s (<%s> va <%s>)' % (i, ids[i], e.tag))
            ids[i] = e.tag
    mv_children = set()
    for mv in root.iter('MasterView'):
        for c in mv:
            mv_children.add(id(c))
    for e in root.iter():
        i = e.get('Idref')
        if id(e) in mv_children:
            continue
        if i is not None and i not in ids and e.tag != 'EAViewpointProperty':
            errs.append('Idref khong ton tai: %s trong <%s Name="%s">' % (i, e.tag, e.get('Name')))
        for a in REF_ATTRS:
            v = e.get(a)
            if v and v not in ids:
                errs.append('Thuoc tinh %s="%s" tro toi Id khong ton tai (<%s Name="%s">)' % (a, v, e.tag, e.get('Name')))
    models, diagrams = root.find('Models'), root.find('Diagrams')
    if models is not None and diagrams is not None:
        shape_ids = set()
        for dg in diagrams:
            for sec in ('Shapes', 'Connectors'):
                s = dg.find(sec)
                if s is not None:
                    for e in s.iter():
                        if e.get('Id'):
                            shape_ids.add(e.get('Id'))
        # MasterView phai tro toi shape/connector
        for mv in models.iter('MasterView'):
            for c in mv:
                if c.get('Idref') not in shape_ids:
                    warns.append('MasterView <%s> Idref=%s khong phai shape/connector (VP van chap nhan neu diagram da bi xoa)' % (c.tag, c.get('Idref')))
        # shape.Model phai la model co MasterView tro nguoc lai
        back = {}
        for mv in models.iter('MasterView'):
            owner = None
        for el in models.iter():
            mv = el.find('MasterView')
            if mv is not None and el.get('Id'):
                for c in mv:
                    back.setdefault(c.get('Idref'), el.get('Id'))
        for dg in diagrams:
            for sec in ('Shapes', 'Connectors'):
                s = dg.find(sec)
                if s is None:
                    continue
                for e in s.iter():
                    m = e.get('Model')
                    if m and back.get(e.get('Id')) != m:
                        warns.append('Shape <%s Name="%s"> tro toi model %s nhung model khong co MasterView tro lai' %
                                     (e.tag, e.get('Name'), m))
                    if sec == 'Connectors' and e.get('From'):
                        for k in ('From', 'To'):
                            if e.get(k) not in shape_ids:
                                errs.append('Connector <%s> %s=%s khong phai Id cua shape' % (e.tag, k, e.get(k)))
    return errs, warns


def main():
    bad = 0
    for p in sys.argv[1:]:
        errs, warns = check(p)
        print('==', p, '->', 'OK' if not errs else '%d LOI' % len(errs), '(%d canh bao)' % len(warns))
        for e in errs[:40]:
            print('  LOI:', e)
        for w in warns[:10]:
            print('  canh bao:', w)
        bad += bool(errs)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
```

</details>

### `examples/class.json`

<details>
<summary>Mở nội dung tệp</summary>

```json
{"project":{"name":"QuanLyQuan","author":"SinhVien"},
 "diagrams":[{"type":"class","name":"Class Diagram - Dat mon",
  "classes":[
   {"name":"OrderUI","stereotype":"boundary","operations":[{"name":"chonBan"},{"name":"guiOrder"}]},
   {"name":"OrderController","stereotype":"control","operations":[{"name":"taoOrder","returnType":"Order","params":[{"name":"maBan","type":"int"}]}]},
   {"name":"Order","attributes":[{"name":"maDon","type":"String","visibility":"protected"},{"name":"tongTien","type":"double"}],"operations":[{"name":"tinhTongTien","returnType":"double"}]},
   {"name":"OrderItem","attributes":[{"name":"soLuong","type":"int"}]},
   {"name":"OrderTaiCho","attributes":[{"name":"soBan","type":"int"}]}
  ],
  "relationships":[
   {"kind":"association","from":"OrderUI","to":"OrderController","name":"goi"},
   {"kind":"association","from":"OrderController","to":"Order","name":"tao","toMultiplicity":"0..*","fromMultiplicity":"1"},
   {"kind":"composition","from":"Order","to":"OrderItem","fromMultiplicity":"1","toMultiplicity":"1..*"},
   {"kind":"generalization","from":"OrderTaiCho","to":"Order"}
  ]}]}
```

</details>

### `examples/sequence.json`

<details>
<summary>Mở nội dung tệp</summary>

```json
{"project":{"name":"Seq"},"diagrams":[{"type":"sequence","name":"UC11 - Quan ly nhan vien",
 "participants":[{"name":"Manager","kind":"actor"},{"name":"UI_ManageEmployee","stereotype":"boundary"},{"name":"EmployeeController","stereotype":"control"},{"name":"Database","stereotype":"entity"}],
 "messages":[
  {"from":"Manager","to":"UI_ManageEmployee","text":"Nhap thong tin & Luu"},
  {"from":"UI_ManageEmployee","to":"EmployeeController","text":"POST /create"},
  {"from":"EmployeeController","to":"EmployeeController","text":"Kiem tra du lieu","kind":"self"},
  {"from":"EmployeeController","to":"Database","text":"Luu nhan vien"},
  {"from":"Database","to":"EmployeeController","text":"OK","kind":"return"},
  {"from":"EmployeeController","to":"UI_ManageEmployee","text":"Thanh cong","kind":"return"},
  {"from":"EmployeeController","to":"UI_ManageEmployee","text":"Loi trung","kind":"return"}],
 "fragments":[{"operator":"alt","from":5,"to":6,"operands":[{"guard":"hop le","from":5,"to":5},{"guard":"trung","from":6,"to":6}]}]}]}
```

</details>

### `examples/communication.json`

<details>
<summary>Mở nội dung tệp</summary>

```json
{"project":{"name":"Comm"},"diagrams":[{"type":"communication","name":"Comm - Chon ban",
 "participants":[{"name":"Nhan vien","kind":"actor"},{"name":":TableUI","stereotype":"boundary"},{"name":":OrderController","stereotype":"control"}],
 "messages":[{"from":"Nhan vien","to":":TableUI","text":"Chon ban"},{"from":":TableUI","to":":OrderController","text":"layBan()"},{"from":":OrderController","to":":TableUI","text":"danh sach","kind":"return"}]}]}
```

</details>

### `examples/state.json`

<details>
<summary>Mở nội dung tệp</summary>

```json
{"project":{"name":"State"},"diagrams":[{"type":"state","name":"State - Don hang",
 "states":[{"name":"MOI_TAO","documentation":"Hoa don nhap"},{"name":"DANG_PHUC_VU"}],
 "finals":["DA_THANH_TOAN"],
 "transitions":[{"from":"initial","to":"MOI_TAO","name":"Chon ban"},{"from":"MOI_TAO","to":"DANG_PHUC_VU","name":"Luu"},
  {"from":"DANG_PHUC_VU","to":"DANG_PHUC_VU","name":"Goi them mon"},{"from":"DANG_PHUC_VU","to":"DA_THANH_TOAN","name":"Thanh toan"}]}]}
```

</details>

### `examples/activity.json`

<details>
<summary>Mở nội dung tệp</summary>

```json
{"project":{"name":"Act"},"diagrams":[{"type":"activity","name":"Activity","actions":[{"name":"Chon ban"},{"name":"Dat mon"}],"objectNodes":[{"name":"Order"}]}]}
```

</details>

### `examples/er.json`

<details>
<summary>Mở nội dung tệp</summary>

```json
{"project":{"name":"ER"},"diagrams":[{"type":"er","name":"ERD",
 "tables":[{"name":"BanAn","columns":[{"name":"maBan","type":"integer","pk":true},{"name":"soBan","type":"integer","unique":true}]},
           {"name":"DonHang","columns":[{"name":"maDon","type":"integer","pk":true},{"name":"tongTien","type":"decimal"}]}],
 "foreignKeys":[{"from":"BanAn","to":"DonHang"}]}]}
```

</details>

### `examples/package.json`

<details>
<summary>Mở nội dung tệp</summary>

```json
{"project":{"name":"Pkg"},"diagrams":[{"type":"package","name":"Package - He thong",
 "packages":[{"name":"UI"},{"name":"Business"},{"name":"Ordering","parent":"Business"},{"name":"Shipping","parent":"Business"},{"name":"Data"}],
 "dependencies":[{"from":"UI","to":"Business"},{"from":"Business","to":"Data"}]}]}
```

</details>

### `examples/deployment.json`

<details>
<summary>Mở nội dung tệp</summary>

```json
{"project":{"name":"Dep"},"diagrams":[{"type":"deployment","name":"Deployment",
 "nodes":[{"name":"Client PC","children":[{"name":"POS App"}]},{"name":"Server","children":[{"name":"API","kind":"component"},{"name":"db.sql","kind":"artifact"}]}],
 "associations":[{"from":"Client PC","to":"Server","name":"HTTPS"}],
 "dependencies":[{"from":"POS App","to":"API"}]}]}
```

</details>

### `assets/attr_templates.json`

<details>
<summary>Mở nội dung tệp</summary>

```json
{
 "m:DataType": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "oHH3uoWFYCy6_Q4C",
   "Name": "boolean",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-09-16T09:35:15.312",
   "PmLastModified": "2026-10-21T10:30:48.325",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:Stereotype": [
  {
   "Abstract": "false",
   "BacklogActivityId": "0",
   "BaseType": "Class",
   "Documentation_plain": "",
   "IconPath_IsNull": "true",
   "Id": "7Y2Ju6EhWcdaycXc",
   "Leaf": "false",
   "Name": "enumeration",
   "PmAuthor": "SinhVien",
   "PmCreateDateTime": "2026-10-14T10:00:00.000",
   "PmLastModified": "2026-10-21T17:10:13.174",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Root": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  },
  {
   "Abstract": "false",
   "BacklogActivityId": "0",
   "BaseType": "Class",
   "Documentation_plain": "",
   "IconPath": "",
   "Id": "SHw_uoWFYCy6_RqX",
   "Leaf": "false",
   "Name": "Interface",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-04-02T22:42:50.659",
   "PmLastModified": "2026-10-21T17:23:47.195",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Root": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:Class": [
  {
   "Abstract": "false",
   "Active": "false",
   "BacklogActivityId": "0",
   "BusinessKeyMutable": "true",
   "BusinessModel": "false",
   "ConnectToCodeModel": "1",
   "Documentation": "<head>\n    \n  </head>\n  <body>\n    <p style=\"margin-top:0;\">\n      M&#224;n h&#236;nh T&#7845;t c&#7843; &#273;&#417;n. B&#7893; sung/&#273;&#7873; xu&#7845;t cho k&#7883;ch b&#7843;n UC-01.\n    </p>\n  </body>",
   "Documentation_plain": "",
   "FinalSpecialization": "false",
   "Id": "FaKw01MpKTA1z876",
   "Leaf": "false",
   "Name": "AllOrdersUI",
   "PmAuthor": "SinhVien",
   "PmCreateDateTime": "2026-10-20T10:00:00.000",
   "PmLastModified": "2026-10-21T17:23:47.200",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Root": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "public"
  },
  {
   "Abstract": "false",
   "Active": "false",
   "BacklogActivityId": "0",
   "BusinessKeyMutable": "true",
   "BusinessModel": "false",
   "ConnectToCodeModel": "1",
   "Documentation_plain": "",
   "FinalSpecialization": "false",
   "Id": "KWjRk4WFYCyCBxNQ",
   "Leaf": "false",
   "Name": "IMortgageApplication",
   "PmAuthor": "",
   "PmCreateDateTime": "2017-06-22T09:42:49.020",
   "PmLastModified": "2026-11-11T14:38:18.400",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Root": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "public"
  }
 ],
 "m:Operation": [
  {
   "Abstract": "false",
   "BacklogActivityId": "0",
   "BodyCondition_IsNull": "true",
   "ConnectToCodeModel": "1",
   "Documentation_plain": "",
   "Id": "L9Kr0jydHk8Pyi76",
   "Leaf": "false",
   "Lower_IsNull": "true",
   "Name": "moLuotChonBan",
   "Ordered": "false",
   "PmAuthor": "SinhVien",
   "PmCreateDateTime": "2026-10-20T10:00:00.000",
   "PmLastModified": "2026-10-21T17:10:13.192",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Query": "false",
   "ReturnType": "",
   "ReturnTypeDocumentation_plain": "",
   "Scope": "instance",
   "Static": "false",
   "TypeModifier": "",
   "Unique": "true",
   "Upper_IsNull": "true",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "public",
   "Visible": "true"
  }
 ],
 "m:Parameter": [
  {
   "BacklogActivityId": "0",
   "Direction": "inout",
   "Documentation_plain": "",
   "Id": "2LlwZRUp02yax0Wh",
   "Multiplicity": "Unspecified",
   "Name": "danhSach",
   "PmAuthor": "SinhVien",
   "PmCreateDateTime": "2026-10-20T10:00:00.000",
   "PmLastModified": "2026-10-21T17:10:13.192",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Type": "List<Order>",
   "TypeModifier": "",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:Attribute": [
  {
   "Abstract": "false",
   "Aggregation": "None",
   "AllowEmptyName": "false",
   "BacklogActivityId": "0",
   "ConnectToCodeModel": "1",
   "Derived": "false",
   "DerivedUnion": "false",
   "Documentation_plain": "",
   "HasGetter": "false",
   "HasSetter": "false",
   "Id": "2wQHHgnx2G08r4WH",
   "IsID": "false",
   "Leaf": "false",
   "Multiplicity": "Unspecified",
   "Name": "maKhuVuc",
   "PmAuthor": "SinhVien",
   "PmCreateDateTime": "2026-10-20T10:00:00.000",
   "PmLastModified": "2026-10-21T17:10:13.168",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "ReadOnly": "false",
   "Scope": "instance",
   "Type": "String",
   "TypeModifier": "",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "private",
   "Visible": "true"
  }
 ],
 "m:ModelRelationshipContainer": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "S1EmI1ncDroXYMtb",
   "Name": "relationships",
   "PmAuthor": "SinhVien",
   "PmCreateDateTime": "2026-10-14T10:00:00.000",
   "PmLastModified": "2026-11-04T17:17:12.828",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:Association": [
  {
   "Abstract": "false",
   "BacklogActivityId": "0",
   "Derived": "false",
   "Direction": "From To",
   "Documentation_plain": "",
   "EndRelationshipFromMetaModelElement": "FaKw01MpKTA1z876",
   "EndRelationshipToMetaModelElement": "5qT8d1qc3IRTviIj",
   "FinalSpecialization": "false",
   "Id": "EkDEkbxDWHUAaq3U",
   "Leaf": "false",
   "Name": "",
   "OrderingInProfile": "-1",
   "PmAuthor": "SinhVien",
   "PmCreateDateTime": "2026-10-14T10:00:00.000",
   "PmLastModified": "2026-10-21T17:10:13.178",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "Unspecified"
  },
  {
   "Abstract": "false",
   "BacklogActivityId": "0",
   "Derived": "false",
   "Direction": "From To",
   "Documentation_plain": "",
   "EndRelationshipFromMetaModelElement": "58lIa7gfwyWpNKRD",
   "EndRelationshipToMetaModelElement": "VDgVeY7WsP4Z4jrz",
   "FinalSpecialization": "false",
   "Id": "KmfwSZLFsH40JVah",
   "Leaf": "false",
   "OrderingInProfile": "-1",
   "PmAuthor": "SinhVien",
   "PmCreateDateTime": "2026-10-14T10:00:00.000",
   "PmLastModified": "2026-10-21T17:10:13.174",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "Unspecified"
  }
 ],
 "m:AssociationEnd": [
  {
   "AggregationKind": "None",
   "BacklogActivityId": "0",
   "ConnectToCodeModel": "1",
   "DefaultValue_IsNull": "true",
   "Derived": "false",
   "DerivedUnion": "false",
   "Documentation_plain": "",
   "EndModelElement": "FaKw01MpKTA1z876",
   "Id": "lhtQ88U93Int7ShT",
   "JavaCodeAttributeName": "",
   "Leaf": "false",
   "Multiplicity": "Unspecified",
   "Navigable": "Unspecified",
   "PmAuthor": "SinhVien",
   "PmCreateDateTime": "2026-10-14T10:00:00.000",
   "PmLastModified_IsNull": "true",
   "ProvidePropertyGetterMethod": "false",
   "ProvidePropertySetterMethod": "false",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "ReadOnly": "false",
   "Static": "false",
   "TypeModifier": "",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "Unspecified"
  }
 ],
 "m:Qualifier": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "aaZq8kxidFrFtZmy",
   "Name": "",
   "PmAuthor": "SinhVien",
   "PmCreateDateTime": "2026-10-14T10:00:00.000",
   "PmLastModified_IsNull": "true",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:Generalization": [
  {
   "BacklogActivityId": "0",
   "ConnectToCodeModel": "1",
   "Documentation_plain": "",
   "From": "ebZ5akXemVsYiUQU",
   "Id": "Lp7vUSD1FL59vrof",
   "PmAuthor": "SinhVien",
   "PmCreateDateTime": "2026-10-20T10:00:00.000",
   "PmLastModified": "2026-10-21T17:10:13.174",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Substitutable": "false",
   "To": "1p2rJhJZ6fqur7O0",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "Unspecified"
  }
 ],
 "d:ClassDiagram": [
  {
   "AlignToGrid": "false",
   "AutoFitShapesSize": "false",
   "ClassFitSizeWhenShowHideMember": "false",
   "ConnectionPointStyle": "0",
   "ConnectorLabelOrientation": "0",
   "ConnectorLineJumps": "0",
   "ConnectorLineJumpsSize": "0",
   "ConnectorModelElementNameAlignment": "4",
   "ConnectorStyle": "1",
   "DiagramBackground": "rgb(255, 255, 255)",
   "Editable": "true",
   "FilterByViewpointLegend": "true",
   "FollowDiagramParentElement": "true",
   "GeneralizationSetNotation": "2",
   "GridColor": "rgb(192, 192, 192)",
   "GridHeight": "10",
   "GridVisible": "false",
   "GridWidth": "10",
   "Height": "598",
   "HideConnectorIfFromToIsHidden": "0",
   "HideEmptyTaggedValues": "false",
   "Id": "0g3mQziUvSOUnHK2",
   "ImageHeight": "0",
   "ImageScale": "1.0",
   "ImageWidth": "0",
   "InitializeDiagramForCreate": "true",
   "Maximized": "true",
   "ModelElementNameAlignment": "4",
   "Name": "",
   "PaintConnectorThroughLabel": "1",
   "PmAuthor": "SinhVien",
   "PmCreateDateTime": "2026-10-20T10:00:00.000",
   "PmLastModified": "2026-11-04T17:12:12.161",
   "PointConnectorEndToCompartmentMember": "true",
   "QualityScore": "-1",
   "RequestFitSizeWithPromptUser": "false",
   "RequestValidateSnapToGrid": "false",
   "ShapePresentationOption": "0",
   "ShowActivityStateNodeCaption": "524287",
   "ShowAllocatedFrom": "true",
   "ShowAllocatedTo": "true",
   "ShowAssociationNavigationArrows": "3",
   "ShowAttributeGetterSetter": "false",
   "ShowAttributesCodeDetails": "2",
   "ShowAttributesPropertyModifiers": "2",
   "ShowAttributesType": "1",
   "ShowClassEmptyCompartments": "2",
   "ShowClassOwner": "2",
   "ShowClassReferencedAttributes": "true",
   "ShowColorLegend": "false",
   "ShowConnectorLegend": "false",
   "ShowConnectorName": "0",
   "ShowConstraints": "false",
   "ShowDefaultPackage": "true",
   "ShowEllipsisForUnshownClassMembers": "2",
   "ShowInformationItemOption": "2",
   "ShowOperationsCodeDetails": "2",
   "ShowOperationsParameters": "1",
   "ShowOperationsReturnType": "1",
   "ShowPMAuthor": "false",
   "ShowPMDifficulty": "false",
   "ShowPMDiscipline": "false",
   "ShowPMIteration": "false",
   "ShowPMPhase": "false",
   "ShowPMPriority": "false",
   "ShowPMStatus": "false",
   "ShowPMVersion": "false",
   "ShowPackageNameStyle": "0",
   "ShowPackageOwner": "2",
   "ShowParametersCodeDetails": "2",
   "ShowRelationshipConstraintExpression": "false",
   "ShowShapeLegend": "false",
   "ShowShapeStereotypeIconName": "true",
   "ShowStereotypes": "true",
   "ShowTaggedValues": "false",
   "ShowTemplateInfoOfGeneralizationAndRealization": "false",
   "SuppressImplied1MultiplicityForAttributeAndAssociationEnd": "false",
   "TeamworkCreateDateTime": "0",
   "TrimmedHeight": "0",
   "TrimmedWidth": "0",
   "Width": "1255",
   "X": "0",
   "Y": "0",
   "ZoomRatio": "0.7",
   "_globalPaletteOption": "true",
   "documentation": "<html>\r\n  <head>\r\n    <style type=\"text/css\">\n      <!--\n        body { color: #000000; font-family: Dialog; font-size: 12px }\n      -->\n    </style>\n    \r\n  </head>\r\n  <body>\r\n  </body>\r\n</html>\r\n"
  }
 ],
 "s:ClassDiagram:Class": [
  {
   "AttributeSortType": "0",
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "DisplayAsRobustnessAnalysisIcon": "true",
   "EnumerationLiteralSortType": "0",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "40",
   "Id": "tspYgdbEqRY22idl",
   "InterfaceBall": "false",
   "KShDrOp": "false",
   "KSwCsMbSt": "true",
   "LShCmMl": "false",
   "LshRfAts": "0",
   "MShDrAt": "false",
   "MSwTpPts": "true",
   "MetaModelElement": "FaKw01MpKTA1z876",
   "Model": "FaKw01MpKTA1z876",
   "ModelElementNameAlignment": "9",
   "Name": "AllOrdersUI",
   "OperationSortType": "0",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "ReceptionSortType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowAttributeType": "1",
   "ShowAttributesCodeDetails": "0",
   "ShowAttributesPropertyModifiers": "0",
   "ShowAttributesType": "0",
   "ShowClassMemberConstraints": "true",
   "ShowEllipsisForUnshownMembers": "0",
   "ShowEmptyCompartments": "0",
   "ShowEnumerationLiteralType": "1",
   "ShowInitialAttributeValue": "true",
   "ShowOperationParameterDirection": "false",
   "ShowOperationProperties": "false",
   "ShowOperationRaisedExceptions": "false",
   "ShowOperationSignature": "true",
   "ShowOperationTemplateParameters": "false",
   "ShowOperationType": "1",
   "ShowOperationsCodeDetails": "0",
   "ShowOperationsParameters": "0",
   "ShowOperationsReturnType": "0",
   "ShowOwnerOption": "3",
   "ShowParameterNameInOperationSignature": "true",
   "ShowParametersCodeDetails": "0",
   "ShowReceptionType": "1",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "ShowTypeOption": "0",
   "SuppressImplied1MultiplicityForAttribute": "0",
   "VisibilityStyle": "1",
   "Width": "80",
   "WpMbs": "false",
   "X": "98",
   "Y": "45",
   "ZOrder": "2"
  }
 ],
 "c:ClassDiagram:Association": [
  {
   "AssociationEndPropertyStringsAInternalHeight": "-2147483648",
   "AssociationEndPropertyStringsAInternalWidth": "-2147483648",
   "AssociationEndPropertyStringsBInternalHeight": "-2147483648",
   "AssociationEndPropertyStringsBInternalWidth": "-2147483648",
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "tspYgdbEqRY22idl",
   "FromConnectType": "0",
   "FromMultiplicityInternalHeight": "-2147483648",
   "FromMultiplicityInternalWidth": "-2147483648",
   "FromPinType": "1",
   "FromRoleInternalHeight": "-2147483648",
   "FromRoleInternalWidth": "-2147483648",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "HasAssociationEndPropertyStringsAShape": "false",
   "HasAssociationEndPropertyStringsBShape": "false",
   "HasMultiplicityAShape": "false",
   "HasMultiplicityBShape": "false",
   "HasRoleAShape": "false",
   "HasRoleBShape": "false",
   "Height": "240",
   "Id": "Yb0RTE6v9m7JQtx0",
   "MetaModelElement": "EkDEkbxDWHUAaq3U",
   "Model": "EkDEkbxDWHUAaq3U",
   "ModelElementNameAlignment": "9",
   "Name": "",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowAssociationEndPropertyStrings": "false",
   "ShowConnectorName": "2",
   "ShowDirection": "false",
   "ShowFromMultiplicity": "true",
   "ShowFromRoleName": "true",
   "ShowFromRoleVisibility": "true",
   "ShowMultiplicityConstraints": "false",
   "ShowNavigationArrows": "0",
   "ShowOrderedMultiplicityConstraint": "true",
   "ShowStereotypes": "true",
   "ShowToMultiplicity": "true",
   "ShowToRoleName": "true",
   "ShowToRoleVisibility": "true",
   "ShowUniqueMultiplicityConstraint": "true",
   "SuppressImplied1MultiplicityForAssociationEnd": "0",
   "To": "uiI5EM8nCOQ9yIAP",
   "ToConnectType": "0",
   "ToMultiplicityInternalHeight": "-2147483648",
   "ToMultiplicityInternalWidth": "-2147483648",
   "ToPinType": "1",
   "ToRoleInternalHeight": "-2147483648",
   "ToRoleInternalWidth": "-2147483648",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "493",
   "X": "129",
   "Y": "35",
   "ZOrder": "34"
  },
  {
   "AssociationEndPropertyStringsAInternalHeight": "-2147483648",
   "AssociationEndPropertyStringsAInternalWidth": "-2147483648",
   "AssociationEndPropertyStringsBInternalHeight": "-2147483648",
   "AssociationEndPropertyStringsBInternalWidth": "-2147483648",
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "CreatorDiagramType": "ClassDiagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "uiI5EM8nCOQ9yIAP",
   "FromConnectType": "0",
   "FromMultiplicityInternalHeight": "-2147483648",
   "FromMultiplicityInternalWidth": "-2147483648",
   "FromPinType": "1",
   "FromRoleInternalHeight": "-2147483648",
   "FromRoleInternalWidth": "-2147483648",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "HasAssociationEndPropertyStringsAShape": "false",
   "HasAssociationEndPropertyStringsBShape": "false",
   "HasMultiplicityAShape": "false",
   "HasMultiplicityBShape": "false",
   "HasRoleAShape": "false",
   "HasRoleBShape": "false",
   "Height": "100",
   "Id": "tg2_uoWFYCy6_Rrj",
   "MetaModelElement": "Rg2_uoWFYCy6_Rre",
   "Model": "Rg2_uoWFYCy6_Rre",
   "ModelElementNameAlignment": "9",
   "Name": "",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowAssociationEndPropertyStrings": "false",
   "ShowConnectorName": "2",
   "ShowDirection": "false",
   "ShowFromMultiplicity": "true",
   "ShowFromRoleName": "true",
   "ShowFromRoleVisibility": "true",
   "ShowMultiplicityConstraints": "false",
   "ShowNavigationArrows": "0",
   "ShowOrderedMultiplicityConstraint": "true",
   "ShowStereotypes": "true",
   "ShowToMultiplicity": "true",
   "ShowToRoleName": "true",
   "ShowToRoleVisibility": "true",
   "ShowUniqueMultiplicityConstraint": "true",
   "SuppressImplied1MultiplicityForAssociationEnd": "0",
   "To": "WJosyIhTvm89N7fr",
   "ToConnectType": "0",
   "ToMultiplicityInternalHeight": "-2147483648",
   "ToMultiplicityInternalWidth": "-2147483648",
   "ToPinType": "1",
   "ToRoleInternalHeight": "-2147483648",
   "ToRoleInternalWidth": "-2147483648",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "521",
   "X": "604",
   "Y": "175",
   "ZOrder": "66"
  },
  {
   "AssociationEndPropertyStringsAInternalHeight": "-2147483648",
   "AssociationEndPropertyStringsAInternalWidth": "-2147483648",
   "AssociationEndPropertyStringsBInternalHeight": "-2147483648",
   "AssociationEndPropertyStringsBInternalWidth": "-2147483648",
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "WJosyIhTvm89N7fr",
   "FromConnectType": "0",
   "FromMultiplicityInternalHeight": "-2147483648",
   "FromMultiplicityInternalWidth": "-2147483648",
   "FromPinType": "1",
   "FromRoleInternalHeight": "-2147483648",
   "FromRoleInternalWidth": "-2147483648",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "HasAssociationEndPropertyStringsAShape": "false",
   "HasAssociationEndPropertyStringsBShape": "false",
   "HasMultiplicityAShape": "false",
   "HasMultiplicityBShape": "false",
   "HasRoleAShape": "false",
   "HasRoleBShape": "false",
   "Height": "100",
   "Id": "vrJyjlm5Z7bwYWIS",
   "MetaModelElement": "KmfwSZLFsH40JVah",
   "Model": "KmfwSZLFsH40JVah",
   "ModelElementNameAlignment": "9",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowAssociationEndPropertyStrings": "false",
   "ShowConnectorName": "2",
   "ShowDirection": "false",
   "ShowFromMultiplicity": "true",
   "ShowFromRoleName": "true",
   "ShowFromRoleVisibility": "true",
   "ShowMultiplicityConstraints": "false",
   "ShowNavigationArrows": "0",
   "ShowOrderedMultiplicityConstraint": "true",
   "ShowStereotypes": "true",
   "ShowToMultiplicity": "true",
   "ShowToRoleName": "true",
   "ShowToRoleVisibility": "true",
   "ShowUniqueMultiplicityConstraint": "true",
   "SuppressImplied1MultiplicityForAssociationEnd": "0",
   "To": "SWEf5Arke2eE5QEm",
   "ToConnectType": "0",
   "ToMultiplicityInternalHeight": "-2147483648",
   "ToMultiplicityInternalWidth": "-2147483648",
   "ToPinType": "1",
   "ToRoleInternalHeight": "-2147483648",
   "ToRoleInternalWidth": "-2147483648",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "268",
   "X": "1163",
   "Y": "175",
   "ZOrder": "50"
  }
 ],
 "c:ClassDiagram:Generalization": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "ee6aiaKLuxuTvpB0",
   "FromConnectType": "0",
   "FromPinType": "1",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "Height": "100",
   "Id": "obyNMj0he2OoJQuV",
   "MetaModelElement": "Lp7vUSD1FL59vrof",
   "Model": "Lp7vUSD1FL59vrof",
   "ModelElementNameAlignment": "9",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowConnectorName": "2",
   "To": "EzrRuMEZJDdweONW",
   "ToConnectType": "0",
   "ToPinType": "1",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "280",
   "X": "1163",
   "Y": "307",
   "ZOrder": "52"
  }
 ],
 "m:ActivityAction": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Effect_IsNull": "true",
   "Id": "lCDupYWFYC1QOgwT",
   "Leaf": "false",
   "MustIsolate": "false",
   "Name": "Action",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T14:30:02.921",
   "PmLastModified": "2026-11-04T14:30:39.742",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "Unspecified"
  }
 ],
 "m:ObjectNode": [
  {
   "BacklogActivityId": "0",
   "ControlType": "false",
   "Documentation_plain": "",
   "Id": "PILupYWFYC1QOgwu",
   "Leaf": "false",
   "MustIsolate": "false",
   "Name": "ObjectNode",
   "OrderingKind": "FIFO",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T14:30:18.556",
   "PmLastModified": "2026-11-04T14:30:39.746",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "TypeModifier": "",
   "UpperBound": "",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "Unspecified"
  }
 ],
 "m:ExpansionRegion": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "GnLupYWFYC1QOgw6",
   "Leaf": "false",
   "Mode": "Iterative",
   "MustIsolate": "false",
   "Name": "Region",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T14:30:21.912",
   "PmLastModified": "2026-11-04T14:30:39.744",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "Unspecified"
  }
 ],
 "m:ActivitySwimlane2": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "XjbupYWFYC1QOgxD",
   "Name": "Swimlane",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T14:30:29.626",
   "PmLastModified": "2026-11-04T14:30:39.742",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:ActivityPartition": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "6TbupYWFYC1QOgxH",
   "Name": "Partition",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T14:30:29.655",
   "PmLastModified": "2026-11-04T14:30:39.730",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "d:ActivityDiagram": [
  {
   "AlignToGrid": "false",
   "AutoFitShapesSize": "false",
   "ConnectionPointStyle": "0",
   "ConnectorLabelOrientation": "0",
   "ConnectorLineJumps": "0",
   "ConnectorLineJumpsSize": "0",
   "ConnectorModelElementNameAlignment": "4",
   "ConnectorStyle": "1",
   "ControlFlowDisplayOption": "0",
   "DecisionMergeNodeConnectionPointStyle": "1",
   "DiagramBackground": "rgb(255, 255, 255)",
   "Editable": "true",
   "FilterByViewpointLegend": "true",
   "FollowDiagramParentElement": "true",
   "GridColor": "rgb(192, 192, 192)",
   "GridHeight": "10",
   "GridVisible": "false",
   "GridWidth": "10",
   "Height": "598",
   "HideConnectorIfFromToIsHidden": "0",
   "HideEmptyTaggedValues": "false",
   "Id": "x11upYWFYC1QOgv2",
   "ImageHeight": "0",
   "ImageScale": "1.0",
   "ImageWidth": "0",
   "InitializeDiagramForCreate": "true",
   "Maximized": "true",
   "ModelElementNameAlignment": "4",
   "Name": "Activity Diagram1",
   "ObjectNodeShowInStates": "2",
   "ObjectNodeShowType": "true",
   "PaintConnectorThroughLabel": "1",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T14:29:44.163",
   "PmLastModified": "2026-11-04T14:30:29.712",
   "PointConnectorEndToCompartmentMember": "true",
   "QualityScore": "-1",
   "RequestFitSizeWithPromptUser": "false",
   "RequestValidateSnapToGrid": "false",
   "ShapePresentationOption": "0",
   "ShowActionCallBehaviorOption": "1",
   "ShowActivityEdgeWeight": "true",
   "ShowActivityStateNodeCaption": "524287",
   "ShowAllocatedFrom": "true",
   "ShowAllocatedTo": "true",
   "ShowColorLegend": "false",
   "ShowConnectorLegend": "false",
   "ShowConnectorName": "0",
   "ShowConstraints": "false",
   "ShowDefaultPackage": "false",
   "ShowDiagramFrame": "true",
   "ShowInformationItemOption": "2",
   "ShowPMAuthor": "false",
   "ShowPMDifficulty": "false",
   "ShowPMDiscipline": "false",
   "ShowPMIteration": "false",
   "ShowPMPhase": "false",
   "ShowPMPriority": "false",
   "ShowPMStatus": "false",
   "ShowPMVersion": "false",
   "ShowPackageNameStyle": "0",
   "ShowPartitionHeader": "0",
   "ShowRelationshipConstraintExpression": "false",
   "ShowShapeLegend": "false",
   "ShowShapeStereotypeIconName": "true",
   "ShowStereotypes": "true",
   "ShowTaggedValues": "false",
   "TeamworkCreateDateTime": "0",
   "TrimmedHeight": "0",
   "TrimmedWidth": "0",
   "Width": "1255",
   "X": "0",
   "Y": "0",
   "ZoomRatio": "1.0",
   "_globalPaletteOption": "true"
  }
 ],
 "s:ActivityDiagram:ActivityAction": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "40",
   "Id": "5CDupYWFYC1QOgwS",
   "MetaModelElement": "lCDupYWFYC1QOgwT",
   "Model": "lCDupYWFYC1QOgwT",
   "ModelElementNameAlignment": "9",
   "Name": "Action",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowCallBehaviorOption": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "60",
   "X": "233",
   "Y": "24",
   "ZOrder": "18"
  }
 ],
 "s:ActivityDiagram:ObjectNode": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "40",
   "Id": "XILupYWFYC1QOgwt",
   "MetaModelElement": "PILupYWFYC1QOgwu",
   "Model": "PILupYWFYC1QOgwu",
   "ModelElementNameAlignment": "9",
   "Name": "ObjectNode",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowConstraints": "false",
   "ShowInStates": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "80",
   "X": "232",
   "Y": "267",
   "ZOrder": "14"
  }
 ],
 "s:ActivityDiagram:ExpansionRegion": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "0",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "50",
   "Id": "6nLupYWFYC1QOgw5",
   "MetaModelElement": "GnLupYWFYC1QOgw6",
   "Model": "GnLupYWFYC1QOgw6",
   "ModelElementNameAlignment": "9",
   "Name": "Region",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "120",
   "X": "166",
   "Y": "382",
   "ZOrder": "12"
  }
 ],
 "s:ActivityDiagram:ActivitySwimlane2": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "200",
   "Id": "XjbupYWFYC1QOgxC",
   "MetaModelElement": "XjbupYWFYC1QOgxD",
   "Model": "XjbupYWFYC1QOgxD",
   "ModelElementNameAlignment": "9",
   "Name": "Swimlane",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitPartitionHeadersHeight": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "ValidatePartitionsForConvert": "false",
   "Width": "200",
   "X": "556",
   "Y": "236",
   "ZOrder": "10"
  }
 ],
 "s:ActivityDiagram:ActivityPartitionHeader": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "15",
   "Horizontal": "false",
   "Id": "6TbupYWFYC1QOgxG",
   "MetaModelElement": "6TbupYWFYC1QOgxH",
   "Model": "6TbupYWFYC1QOgxH",
   "ModelElementNameAlignment": "9",
   "Name": "Partition",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "100",
   "X": "556",
   "Y": "236",
   "ZOrder": "8"
  }
 ],
 "s:ActivityDiagram:ActivitySwimlane2Compartment": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "185",
   "Id": "jTbupYWFYC1QOgxK",
   "ModelElementNameAlignment": "9",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "VerticalPartitionId": "6TbupYWFYC1QOgxG",
   "Width": "100",
   "X": "556",
   "Y": "251",
   "ZOrder": "6"
  }
 ],
 "m:Dependency": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "From": "yauRk4WFYCyCBxAz",
   "Id": "pauRk4WFYCyCBxA7",
   "PmAuthor": "",
   "PmCreateDateTime": "2017-06-22T10:55:22.623",
   "PmLastModified": "2026-11-11T14:36:56.275",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "To": "yauRk4WFYCyCBxAw",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "Unspecified"
  }
 ],
 "m:Model": [
  {
   "Abstract": "false",
   "BacklogActivityId": "0",
   "ConnectToCodeModel": "1",
   "Documentation_plain": "",
   "Id": "nquRk4WFYCyCBxAt",
   "Leaf": "false",
   "Name": "Package Diagram - General Business System",
   "PmAuthor": "",
   "PmCreateDateTime": "2017-06-22T10:53:44.705",
   "PmLastModified": "2026-11-11T14:36:56.275",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Root": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:Package": [
  {
   "Abstract": "false",
   "BacklogActivityId": "0",
   "ConnectToCodeModel": "1",
   "DefaultDiagramId_IsNull": "true",
   "Documentation_plain": "",
   "Id": "yauRk4WFYCyCBxAv",
   "Leaf": "false",
   "Name": "com.aBusiness",
   "PmAuthor": "",
   "PmCreateDateTime": "2017-06-22T10:55:00.834",
   "PmLastModified": "2026-11-11T14:36:56.289",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Root": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "public"
  }
 ],
 "d:PackageDiagram": [
  {
   "AlignToGrid": "false",
   "AutoFitShapesSize": "false",
   "ConnectionPointStyle": "0",
   "ConnectorLabelOrientation": "0",
   "ConnectorLineJumps": "0",
   "ConnectorLineJumpsSize": "0",
   "ConnectorModelElementNameAlignment": "4",
   "ConnectorStyle": "1",
   "DiagramBackground": "rgb(255, 255, 255)",
   "Editable": "true",
   "FilterByViewpointLegend": "true",
   "FollowDiagramParentElement": "true",
   "GridColor": "rgb(192, 192, 192)",
   "GridHeight": "10",
   "GridVisible": "false",
   "GridWidth": "10",
   "Height": "598",
   "HideConnectorIfFromToIsHidden": "0",
   "HideEmptyTaggedValues": "false",
   "Id": "XauRk4WFYCyCBxBD",
   "ImageHeight": "0",
   "ImageScale": "1.0",
   "ImageWidth": "0",
   "InitializeDiagramForCreate": "true",
   "Maximized": "true",
   "ModelElementNameAlignment": "4",
   "Name": "General Business System",
   "PaintConnectorThroughLabel": "1",
   "ParentModel": "nquRk4WFYCyCBxAt",
   "PmAuthor": "",
   "PmCreateDateTime": "2017-06-22T10:53:59.666",
   "PmLastModified": "2017-06-22T15:44:54.600",
   "PointConnectorEndToCompartmentMember": "true",
   "QualityScore": "-1",
   "RequestFitSizeWithPromptUser": "false",
   "RequestValidateSnapToGrid": "false",
   "ShapePresentationOption": "0",
   "ShowActivityStateNodeCaption": "65535",
   "ShowAllocatedFrom": "true",
   "ShowAllocatedTo": "true",
   "ShowColorLegend": "false",
   "ShowConnectorLegend": "false",
   "ShowConnectorName": "0",
   "ShowConstraints": "false",
   "ShowDefaultPackage": "true",
   "ShowDiagramFrame": "true",
   "ShowInformationItemOption": "2",
   "ShowPMAuthor": "false",
   "ShowPMDifficulty": "false",
   "ShowPMDiscipline": "false",
   "ShowPMIteration": "false",
   "ShowPMPhase": "false",
   "ShowPMPriority": "false",
   "ShowPMStatus": "false",
   "ShowPMVersion": "false",
   "ShowPackageNameStyle": "0",
   "ShowRelationshipConstraintExpression": "false",
   "ShowShapeLegend": "false",
   "ShowShapeStereotypeIconName": "true",
   "ShowStereotypes": "true",
   "ShowTaggedValues": "false",
   "TeamworkAuthor": "Jick Yeung",
   "TeamworkCreateDateTime": "1498117490291",
   "TrimmedHeight": "0",
   "TrimmedWidth": "0",
   "Width": "1255",
   "X": "0",
   "Y": "0",
   "ZoomRatio": "1.0",
   "_globalPaletteOption": "true",
   "documentation": "<html>\r\n  <head>\r\n    <style type=\"text/css\">\n      <!--\n        body { color: #000000; font-family: Dialog; font-size: 12px }\n      -->\n    </style>\r\n    \r\n  </head>\r\n  <body>\r\n    <p>\r\n      \r\n    </p>\r\n  </body>\r\n</html>\r\n"
  }
 ],
 "s:PackageDiagram:Package": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "161",
   "Id": "k6uRk4WFYCyCBxBF",
   "MetaModelElement": "yauRk4WFYCyCBxA1",
   "Model": "yauRk4WFYCyCBxA1",
   "ModelElementNameAlignment": "1",
   "Name": "DataManagement",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowOwnerOption": "3",
   "ShowPackageNameStyle": "2",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "301",
   "X": "219",
   "Y": "283",
   "ZOrder": "6"
  },
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "CreatorDiagramType": "PackageDiagram",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "71",
   "Id": "y6uRk4WFYCyCBxBN",
   "MetaModelElement": "yauRk4WFYCyCBxAz",
   "Model": "yauRk4WFYCyCBxAz",
   "ModelElementNameAlignment": "1",
   "Name": "UI",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowOwnerOption": "3",
   "ShowPackageNameStyle": "2",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "92",
   "X": "75",
   "Y": "166",
   "ZOrder": "16"
  }
 ],
 "c:PackageDiagram:Dependency": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "CreatorDiagramType": "PackageDiagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "y6uRk4WFYCyCBxBN",
   "FromConnectType": "0",
   "FromPinType": "1",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "Height": "200",
   "Id": "x6uRk4WFYCyCBxBX",
   "MetaModelElement": "pauRk4WFYCyCBxA7",
   "Model": "pauRk4WFYCyCBxA7",
   "ModelElementNameAlignment": "9",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowConnectorName": "2",
   "To": "x6uRk4WFYCyCBxBV",
   "ToConnectType": "0",
   "ToPinType": "1",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "277",
   "X": "68",
   "Y": "112",
   "ZOrder": "20"
  }
 ],
 "m:ApiProfile": [
  {
   "BasePath": "/",
   "ContactEmail_IsNull": "true",
   "ContactName_IsNull": "true",
   "ContactUrl_IsNull": "true",
   "Documentation_plain": "",
   "ExternalDocsDescription_plain": "",
   "ExternalDocsUrl_IsNull": "true",
   "Host": "",
   "Id": "iddgWbmA0I2A4gX4",
   "LicenseName_IsNull": "true",
   "LicenseUrl_IsNull": "true",
   "Name": "",
   "TermsOfService_IsNull": "true",
   "Title_IsNull": "true",
   "Version": "1.0.0"
  }
 ],
 "m:WSDLContainer": [
  {
   "Id": "iddgWbmA0I2A4gX5",
   "Name": "WSDLContainer"
  }
 ],
 "m:XSDSchema": [
  {
   "AttributeFormDefault": "unspecified",
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "ElementFormDefault": "unspecified",
   "Id": "iddgWbmA0I2A4gX6",
   "Import": "false",
   "ImportLocation_IsNull": "true",
   "Name": "http://www.w3.org/2001/XMLSchema",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.033",
   "PmLastModified": "2026-04-17T13:00:48.709",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "TargetNamespace": "http://www.w3.org/2001/XMLSchema",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Version_IsNull": "true",
   "XmlLang_IsNull": "true",
   "XsdId_IsNull": "true"
  }
 ],
 "m:XSDSimpleType": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "SddgWbmA0I2A4gX7",
   "Import": "false",
   "ImportLocation_IsNull": "true",
   "Name": "ENTITIES",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.034",
   "PmLastModified": "2026-04-17T13:00:48.711",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "XsdId_IsNull": "true"
  }
 ],
 "m:PMStatusContainer": [
  {
   "Id": "6ddgWbmA0I2A4gYn",
   "Name": ""
  }
 ],
 "m:PMStatus": [
  {
   "Id": "6ddgWbmA0I2A4gYo",
   "Name": "Proposed"
  }
 ],
 "m:PMDifficultyContainer": [
  {
   "Id": "6ddgWbmA0I2A4gYv",
   "Name": ""
  }
 ],
 "m:PMDifficulty": [
  {
   "Id": "6ddgWbmA0I2A4gYw",
   "Name": "Easy"
  }
 ],
 "m:PMPriorityContainer": [
  {
   "Id": "6ddgWbmA0I2A4gYz",
   "Name": ""
  }
 ],
 "m:PMPriority": [
  {
   "Id": "6ddgWbmA0I2A4gY0",
   "Name": "Low"
  }
 ],
 "m:PMVersionContainer": [
  {
   "Id": "6ddgWbmA0I2A4gY3",
   "Name": ""
  }
 ],
 "m:PMVersion": [
  {
   "Id": "6ddgWbmA0I2A4gY4",
   "Name": "1.0"
  }
 ],
 "m:PMIterationContainer": [
  {
   "Id": "2ddgWbmA0I2A4gY6",
   "Name": ""
  }
 ],
 "m:PMIteration": [
  {
   "Id": "2ddgWbmA0I2A4gY7",
   "Name": "Iteration 1"
  }
 ],
 "m:PMPhaseContainer": [
  {
   "Id": "2ddgWbmA0I2A4gY9",
   "Name": ""
  }
 ],
 "m:PMPhase": [
  {
   "Id": "2ddgWbmA0I2A4gY.",
   "Name": "Inception"
  }
 ],
 "m:PMDisciplineContainer": [
  {
   "Id": "2ddgWbmA0I2A4gZC",
   "Name": ""
  }
 ],
 "m:PMDiscipline": [
  {
   "Id": "2ddgWbmA0I2A4gZD",
   "Name": "Business Modeling"
  }
 ],
 "m:PMAuthorContainer": [
  {
   "DefaultValue": "2ddgWbmA0I2A4gZK",
   "Id": "2ddgWbmA0I2A4gZJ",
   "Name": ""
  }
 ],
 "m:ValueSpecification": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "2ddgWbmA0I2A4gZK",
   "Name": "Admin",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.043",
   "PmLastModified": "2026-04-17T13:00:48.683",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:BRKeywords": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "2ddgWbmA0I2A4gZL",
   "Name": "",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.043",
   "PmLastModified": "2026-04-17T13:00:48.681",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:BRKeyword": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": ".ddgWbmA0I2A4gZM",
   "Name": "must",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.047",
   "PmLastModified": "2026-04-17T13:00:48.738",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:ChartTypeContainer": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": ".ddgWbmA0I2A4gZW",
   "Name": "ChartTypeContainer",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.047",
   "PmLastModified": "2026-04-17T13:00:48.737",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:ChartType": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": ".ddgWbmA0I2A4gZX",
   "Name": "RACI",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.047",
   "PmLastModified": "2026-04-17T13:00:48.737",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:ChartCode": [
  {
   "BacklogActivityId": "0",
   "Code": "R",
   "Color": "-1",
   "Documentation_plain": "",
   "Id": ".ddgWbmA0I2A4gZY",
   "Name": "Responsible",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.047",
   "PmLastModified_IsNull": "true",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:BMMInfluencerCategoryContainer": [
  {
   "Id": "xddgWbmA0I2A4gZh",
   "Name": ""
  }
 ],
 "m:BMMInfluencerCategory": [
  {
   "BacklogActivityId": "0",
   "Documentation": "<HTML><BODY><p style=\"margin-top: 0\">A rival enterprise in a struggle for advantage over the subject enterprise.</p></BODY></HTML>",
   "Documentation_plain": "A rival enterprise in a struggle for advantage over the subject enterprise.",
   "Id": "xddgWbmA0I2A4gZi",
   "Name": "Competitor",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.053",
   "PmLastModified": "2026-04-17T13:00:48.697",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:BMMBusinessRuleEnforcementLevelContainer": [
  {
   "Id": "VddgWbmA0I2A4gZy",
   "Name": ""
  }
 ],
 "m:BMMBusinessRuleEnforcementLevel": [
  {
   "BacklogActivityId": "0",
   "Documentation": "<HTML><BODY><p style=\"margin-top: 0\">If the rule is violated, the penalty is always applied.</p></BODY></HTML>",
   "Documentation_plain": "If the rule is violated, the penalty is always applied.",
   "Id": "VddgWbmA0I2A4gZz",
   "Name": "Strictly enforced",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.058",
   "PmLastModified": "2026-04-17T13:00:48.725",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:BMMAssetCategoryContainer": [
  {
   "Id": "NddgWbmA0I2A4gZ5",
   "Name": ""
  }
 ],
 "m:BMMAssetCategory": [
  {
   "BacklogActivityId": "0",
   "Documentation": "<HTML><BODY><p style=\"margin-top: 0\">Things that are kept long-term, maintained, reused, and perhaps eventually replaced. They can be tangible, such as equipment and buildings, or intangible, such as patents and licenses.</p></BODY></HTML>",
   "Documentation_plain": "Things that are kept long-term, maintained, reused, and perhaps eventually replaced. They can be tangible, such as equipment and buildings, or intangible, such as patents and licenses.",
   "Id": "NddgWbmA0I2A4gZ6",
   "Name": "Fixed Assets",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.060",
   "PmLastModified": "2026-04-17T13:00:48.711",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:BMMAssessmentCategoryContainer": [
  {
   "Id": "tddgWbmA0I2A4gZ9",
   "Name": ""
  }
 ],
 "m:BMMAssessmentCategory": [
  {
   "BacklogActivityId": "0",
   "Documentation": "<HTML><BODY><p style=\"margin-top: 0\">Some advantage or area of excellence within the enterprise that can impact its employment of Means or achievement of Ends.</p></BODY></HTML>",
   "Documentation_plain": "Some advantage or area of excellence within the enterprise that can impact its employment of Means or achievement of Ends.",
   "Id": "tddgWbmA0I2A4gZ.",
   "Name": "Strength",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.061",
   "PmLastModified": "2026-04-17T13:00:48.697",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:ProjectFormat": [
  {
   "ConnectorLineColor": "-16777216",
   "ConnectorLineModelCap": "None",
   "ConnectorLineModelStrokeNull": "false",
   "ConnectorLineTransparency": "0",
   "ConnectorLineWeight": "1.0",
   "DefaultCompartmentFontName": "",
   "DefaultCompartmentFontSize": "0",
   "DefaultCompartmentFontStyle": "0",
   "DefaultConnectorFontColor": "-16777216",
   "DefaultConnectorFontName": "Dialog",
   "DefaultConnectorFontSize": "11",
   "DefaultConnectorFontStyle": "0",
   "DefaultConnectorModelElementNameAlignment": "9",
   "DefaultFontColor": "-16777216",
   "DefaultFontName": "Dialog",
   "DefaultFontSize": "11",
   "DefaultFontStyle": "0",
   "DefaultModelElementNameAlignment": "9",
   "DefaultShapeBackground": "-8728587",
   "DefaultShapeForeground": "-16777216",
   "GlobalConnectorFillColorModel": "dddgWbmA0I2A4gaE",
   "GlobalFillColorModel": "dddgWbmA0I2A4gaD",
   "Id": "dddgWbmA0I2A4gaC",
   "LineColor": "-16777216",
   "LineModelCap": "None",
   "LineModelStrokeNull": "false",
   "LineTransparency": "0",
   "LineWeight": "1.0",
   "Name": "ProjectFormat"
  }
 ],
 "m:ProjectFillColorModel": [
  {
   "BaseType": "Global",
   "FillColorColor1": "-8728587",
   "FillColorColor2": "0",
   "FillColorGradientStyle": "S-N",
   "FillColorTransparency": "0",
   "FillColorType": "Solid",
   "Id": "dddgWbmA0I2A4gaD",
   "Name": ""
  }
 ],
 "m:ProjectDefaultLineModel": [
  {
   "BaseType": "Callout",
   "Id": "S9dgWbmA0I2A4ggL",
   "LineColor": "-3370015",
   "LineModelCap": "None",
   "LineModelStrokeNull": "false",
   "LineTransparency": "0",
   "LineWeight": "1.0",
   "Name": ""
  }
 ],
 "m:ProjectElementFontModel": [
  {
   "BaseType": "DBViewTable",
   "Color": "-12566464",
   "CompartmentFontName": "",
   "CompartmentFontSize": "0",
   "CompartmentFontStyle": "0",
   "FontName": "Dialog",
   "FontSize": "11",
   "FontStyle": "0",
   "Id": "K9dgWbmA0I2A4ggl",
   "ModelElementNameAlignment": "9",
   "Name": ""
  }
 ],
 "m:BusinessRuleTypeContainer": [
  {
   "Id": "W9dgWbmA0I2A4ghO",
   "Name": ""
  }
 ],
 "m:BusinessRuleType": [
  {
   "Description": "Statements that are true about the business",
   "Id": "W9dgWbmA0I2A4ghP",
   "Name": "Facts"
  }
 ],
 "m:BrainstormNoteTagContainer": [
  {
   "Id": "W9dgWbmA0I2A4ghU",
   "Name": ""
  }
 ],
 "m:BrainstormNoteTag": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "W9dgWbmA0I2A4ghV",
   "Name": "Task",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.106",
   "PmLastModified": "2026-04-17T13:00:48.709",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:StringValue": [
  {
   "Id": "W9dgWbmA0I2A4ghW",
   "Name": "BPTask"
  }
 ],
 "m:TaggedValueDefinitionContainer": [
  {
   "Id": "UjdgWbmA0I2A4ghf",
   "Name": ""
  }
 ],
 "m:TaggedValueDefinition": [
  {
   "BacklogActivityId": "0",
   "DefaultHTMLValue": "",
   "DefaultValue": "",
   "Documentation_plain": "",
   "Id": "0jdgWbmA0I2A4ghg",
   "Name": "Level",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.220",
   "PmLastModified": "2026-04-17T13:00:48.725",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "TagDefStereotype": "4jdgWbmA0I2A4ghe",
   "Type": "Enumeration",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:DBLookupContainer": [
  {
   "Id": "NjdgWbmA0I2A4ghr",
   "Name": ""
  }
 ],
 "m:ViewpointLookup": [
  {
   "Id": "fjdgWbmA0I2A4gh3",
   "Name": "Viewpoint Lookup"
  }
 ],
 "m:ViewpointStakeholder": [
  {
   "Id": "ATdgWbmA0I2A4gh4",
   "Name": "Enterprise Architects"
  }
 ],
 "m:Viewpoint": [
  {
   "ApplyPalette": "false",
   "Concerns": "Identification of competencies, authority, and responsibilities",
   "Deciding": "true",
   "Designing": "true",
   "EnterpriseArchitecture": "false",
   "FilterConnector": "false",
   "FilterShape": "true",
   "Id": "EbdgWbmA0I2A4gmN",
   "Informing": "true",
   "Name": "Organization Viewpoint"
  },
  {
   "ApplyPalette": "false",
   "Concerns_IsNull": "true",
   "Deciding": "false",
   "Designing": "false",
   "EnterpriseArchitecture": "false",
   "FilterConnector": "false",
   "FilterShape": "true",
   "Id": "BTdgWbmA0I2A4giO",
   "Informing": "false",
   "Name": "TOGAF - Organization Impacted"
  }
 ],
 "m:ShapeLegend": [
  {
   "IconPath_IsNull": "true",
   "Id": "RTdgWbmA0I2A4giP",
   "Name": "Business Actor",
   "ShapeType": "ArchiMateBusinessActor",
   "Style": "pTdgWbmA0I2A4giR",
   "Viewpoint": "BTdgWbmA0I2A4giO"
  }
 ],
 "m:ColorLegend": [
  {
   "Id": "5TdgWbmA0I2A4giW",
   "Name": "Core impacted units",
   "Style": "5TdgWbmA0I2A4giX",
   "TaskPoolId": "0",
   "TaskPoolName_IsNull": "true",
   "Viewpoint": "BTdgWbmA0I2A4giO"
  }
 ],
 "m:StyleSetContainer": [
  {
   "Id": "RTdgWbmA0I2A4giQ",
   "Name": "StyleSet"
  }
 ],
 "m:Style": [
  {
   "Background": "-65639",
   "Background2": "-16777216",
   "BacklogActivityId": "0",
   "BeginArrowFillColor": "0",
   "BeginArrowHeight": "0",
   "BeginArrowName": "None",
   "BeginArrowSize": "Medium",
   "BeginArrowUseFillColor": "false",
   "BeginArrowWidth": "0",
   "BorderColor": "-16777216",
   "BorderStrokeNull": "false",
   "BorderTransparency": "0",
   "BorderWeight": "1.0",
   "CompartmentFontName_IsNull": "true",
   "CompartmentFontSize": "0",
   "CompartmentFontStyle": "0",
   "CustomText_IsNull": "true",
   "Documentation_plain": "",
   "EndArrowFillColor": "0",
   "EndArrowHeight": "0",
   "EndArrowName": "None",
   "EndArrowSize": "Medium",
   "EndArrowUseFillColor": "false",
   "EndArrowWidth": "0",
   "FillColorGradientStyle": "S-N",
   "FillColorTransparency": "0",
   "FillColorType": "Solid",
   "FontName": "Dialog",
   "FontSize": "11",
   "FontStyle": "0",
   "Foreground": "-16777216",
   "Id": "pTdgWbmA0I2A4giR",
   "ModelElementNameAlignment": "Follow Diagram",
   "Name": "TOGAF - Organization Impacted - Business Actor",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.309",
   "PmLastModified": "2026-04-17T13:00:48.727",
   "PrimitiveShapeType": "Unspecified",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "ShapeLegend": "RTdgWbmA0I2A4giP",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  },
  {
   "Background": "-31098",
   "Background2": "-16777216",
   "BacklogActivityId": "0",
   "BeginArrowFillColor": "0",
   "BeginArrowHeight": "0",
   "BeginArrowName": "None",
   "BeginArrowSize": "Medium",
   "BeginArrowUseFillColor": "false",
   "BeginArrowWidth": "0",
   "BorderColor": "-16777216",
   "BorderStrokeNull": "false",
   "BorderTransparency": "0",
   "BorderWeight": "1.0",
   "ColorLegend": "5TdgWbmA0I2A4giW",
   "CompartmentFontName_IsNull": "true",
   "CompartmentFontSize": "0",
   "CompartmentFontStyle": "0",
   "CustomText_IsNull": "true",
   "Documentation_plain": "",
   "EndArrowFillColor": "0",
   "EndArrowHeight": "0",
   "EndArrowName": "None",
   "EndArrowSize": "Medium",
   "EndArrowUseFillColor": "false",
   "EndArrowWidth": "0",
   "FillColorGradientStyle": "S-N",
   "FillColorTransparency": "0",
   "FillColorType": "Solid",
   "FontName": "Dialog",
   "FontSize": "11",
   "FontStyle": "0",
   "Foreground": "-16777216",
   "Id": "5TdgWbmA0I2A4giX",
   "ModelElementNameAlignment": "Follow Diagram",
   "Name": "TOGAF - Organization Impacted - Core impacted units",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:00:38.311",
   "PmLastModified": "2026-04-17T13:00:48.727",
   "PrimitiveShapeType": "Unspecified",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:Frame": [
  {
   "BacklogActivityId": "0",
   "BaseY": "40",
   "Documentation_plain": "",
   "Id": "6ZrgWbmA0I2A4gnA",
   "Name": "UC11 - Quan ly nhan vien",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:01:06.199",
   "PmLastModified": "2026-04-17T14:44:06.580",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Type": "sd",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:InteractionActor": [
  {
   "Abstract": "false",
   "Active": "false",
   "BacklogActivityId": "0",
   "BusinessModel": "false",
   "Documentation_plain": "",
   "FinalSpecialization": "false",
   "Id": "GCTwWbmA0I2A4gnQ",
   "Leaf": "false",
   "Name": "Manager",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:09:36.792",
   "PmLastModified": "2026-04-17T14:44:06.580",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Root": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "public"
  }
 ],
 "m:InteractionLifeLine": [
  {
   "Active": "false",
   "BacklogActivityId": "0",
   "Class": "false",
   "ClassLevelStereotype": "false",
   "Documentation_plain": "",
   "Id": "SFRIWbmA0I2A4gnj",
   "MultiObject": "false",
   "Multiplicity": "Unspecified",
   "Name": "UI_ManageEmployee",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:12:54.930",
   "PmLastModified": "2026-04-17T14:44:06.579",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Stopped": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:Activation": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "7EjsWbmA0I2A4hCg",
   "Name": "Activation",
   "OverlappingExecutionOccurrence": "false",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:53:13.655",
   "PmLastModified_IsNull": "true",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:CombinedFragment": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "RsVcWbmA0I2A4hGn",
   "Name": "",
   "OperatorKind": "alt",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:57:07.426",
   "PmLastModified": "2026-04-17T16:39:07.804",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:InteractionOperand": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "5sVcWbmA0I2A4hGr",
   "Name": "Operand",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:57:07.431",
   "PmLastModified": "2026-04-17T16:40:48.531",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:InteractionConstraint": [
  {
   "BacklogActivityId": "0",
   "Constraint_IsNull": "true",
   "Documentation_plain": "",
   "Id": "tsVcWbmA0I2A4hGy",
   "Maxint_IsNull": "true",
   "Minint_IsNull": "true",
   "Name": "InteractionConstraint",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:57:07.437",
   "PmLastModified_IsNull": "true",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  },
  {
   "BacklogActivityId": "0",
   "Constraint": "",
   "Documentation_plain": "",
   "Id": "0uLGWbmA0I2A4hfh",
   "Maxint_IsNull": "true",
   "Minint_IsNull": "true",
   "Name": "InteractionConstraint",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T14:41:30.827",
   "PmLastModified_IsNull": "true",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:Message": [
  {
   "Asynchronous": "false",
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "DurationHeight": "30",
   "EndRelationshipFromMetaModelElement": "drxIWbmA0I2A4gn3",
   "EndRelationshipToMetaModelElement": "SFRIWbmA0I2A4gnj",
   "FromActivation": "gEjGWbmA0I2A4hfR",
   "Id": "Mh6cWbmA0I2A4hEo",
   "Name": "",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:55:50.860",
   "PmLastModified": "2026-04-17T14:44:06.575",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "SequenceNumber": "1.2",
   "ToActivation": "7EjsWbmA0I2A4hCg",
   "Type": "Message",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  },
  {
   "Asynchronous": "false",
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "DurationHeight": "30",
   "EndRelationshipFromMetaModelElement": "SFRIWbmA0I2A4gnj",
   "EndRelationshipToMetaModelElement": "drxIWbmA0I2A4gn3",
   "FromActivation": "7EjsWbmA0I2A4hCg",
   "Id": "UKccWbmA0I2A4hEN",
   "Name": "GET /employees",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:55:13.162",
   "PmLastModified": "2026-04-17T14:44:06.576",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "ReturnMessage": "Mh6cWbmA0I2A4hEo",
   "SequenceNumber": "1.1",
   "ToActivation": "gEjGWbmA0I2A4hfR",
   "Type": "Message",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  },
  {
   "Asynchronous": "false",
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "DurationHeight": "30",
   "EndRelationshipFromMetaModelElement": "GCTwWbmA0I2A4gnQ",
   "EndRelationshipToMetaModelElement": "SFRIWbmA0I2A4gnj",
   "Id": "DEjsWbmA0I2A4hCZ",
   "Name": "Chon \"Quan ly nhan vien\"",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:53:13.648",
   "PmLastModified": "2026-04-17T14:44:06.578",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "SequenceNumber": "1",
   "ToActivation": "7EjsWbmA0I2A4hCg",
   "Type": "Message",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:MessageEnd": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "EndModelElement": "GCTwWbmA0I2A4gnQ",
   "Id": "DEjsWbmA0I2A4hCa",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:53:13.648",
   "PmLastModified_IsNull": "true",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:ActionTypeReturn": [
  {
   "Asynchronous": "false",
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "2h6cWbmA0I2A4hEt",
   "Iteration": "false",
   "Name": "Return",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:55:50.875",
   "PmLastModified_IsNull": "true",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "RecurrenceCondition_IsNull": "true",
   "Script_IsNull": "true",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:Anchor": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "From": "wntmWbmA0I2A4hmz",
   "Id": "8Ad2WbmA0I2A4hvZ",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T14:54:10.831",
   "PmLastModified": "2026-04-17T14:54:49.213",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "To": "J_t2WbmA0I2A4hvV",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:NOTE": [
  {
   "BacklogActivityId": "0",
   "Documentation": "<head>\r\n    <style type=\"text/css\">\n      <!--\n        body { color: #000000; font-family: Dialog; font-size: 12px }\n      -->\n    </style>\r\n    \r\n  </head>\r\n  <body>\r\n    User ph&#7843;i &#273;&#432;&#7907;c g&#225;n Role: Staff ho&#7863;c Manager (BR-UC16-02)\r\n  </body>",
   "Documentation_plain": "",
   "Id": "J_t2WbmA0I2A4hvV",
   "Name": "",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T14:54:10.788",
   "PmLastModified": "2026-04-17T14:54:49.214",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "d:InteractionDiagram": [
  {
   "AlignToGrid": "false",
   "AutoExtendActivations": "true",
   "AutoFitShapesSize": "false",
   "ConnectionPointStyle": "0",
   "ConnectorLabelOrientation": "0",
   "ConnectorLineJumps": "0",
   "ConnectorLineJumpsSize": "0",
   "ConnectorModelElementNameAlignment": "4",
   "ConnectorStyle": "1",
   "DiagramBackground": "rgb(255, 255, 255)",
   "DisplayLifeLinesAsRobustnessAnalysisIcon": "0",
   "Editable": "true",
   "FilterByViewpointLegend": "true",
   "FollowDiagramParentElement": "true",
   "GridColor": "rgb(192, 192, 192)",
   "GridHeight": "10",
   "GridVisible": "false",
   "GridWidth": "10",
   "Height": "598",
   "HideConnectorIfFromToIsHidden": "0",
   "HideEmptyTaggedValues": "false",
   "Id": "nRrgWbmA0I2A4gm7",
   "ImageHeight": "0",
   "ImageScale": "1.0",
   "ImageWidth": "0",
   "InitializeDiagramForCreate": "true",
   "InteractionLifeLinePresentationOption": "0",
   "Maximized": "true",
   "ModelElementNameAlignment": "4",
   "Name": "UC11 - Quan ly nhan vien",
   "PaintConnectorThroughLabel": "1",
   "PmAuthor": "Admin",
   "PmCreateDateTime": "2026-04-17T13:01:05.977",
   "PmLastModified": "2026-04-17T16:40:38.514",
   "PointConnectorEndToCompartmentMember": "true",
   "QualityScore": "-1",
   "RequestFitSizeWithPromptUser": "false",
   "RequestValidateSnapToGrid": "false",
   "SequenceNumberHandling": "1",
   "SequenceNumbering": "0",
   "ShapePresentationOption": "0",
   "ShowActivations": "true",
   "ShowActivityStateNodeCaption": "524287",
   "ShowAllocatedFrom": "true",
   "ShowAllocatedTo": "true",
   "ShowArgumentsInMessagesOperationSignature": "true",
   "ShowColorLegend": "false",
   "ShowConnectorLegend": "false",
   "ShowConnectorName": "0",
   "ShowConstraints": "false",
   "ShowDefaultPackage": "false",
   "ShowDiagramFrame": "true",
   "ShowInformationItemOption": "2",
   "ShowMessageName": "true",
   "ShowMessageStereotype": "true",
   "ShowMessagesOperationSignature": "true",
   "ShowPMAuthor": "false",
   "ShowPMDifficulty": "false",
   "ShowPMDiscipline": "false",
   "ShowPMIteration": "false",
   "ShowPMPhase": "false",
   "ShowPMPriority": "false",
   "ShowPMStatus": "false",
   "ShowPMVersion": "false",
   "ShowPackageNameStyle": "0",
   "ShowParameterNamesInMessageOperationSignature": "true",
   "ShowParameterTypesInMessageOperationSignature": "true",
   "ShowRelationshipConstraintExpression": "false",
   "ShowReturnTypeInMessagesOperationSignature": "true",
   "ShowSequenceNumbers": "true",
   "ShowShapeLegend": "false",
   "ShowShapeStereotypeIconName": "true",
   "ShowStereotypes": "true",
   "ShowTaggedValues": "false",
   "TeamworkCreateDateTime": "0",
   "TrimmedHeight": "0",
   "TrimmedWidth": "0",
   "Width": "1255",
   "X": "0",
   "Y": "0",
   "ZoomRatio": "1.0",
   "_globalPaletteOption": "true",
   "_requestFixDiagramForRoseImport": "false",
   "_requestRecalculateSequenceNumbers": "false",
   "_rootFrame": "6ZrgWbmA0I2A4gnA",
   "documentation": "<html>\r\n  <head>\r\n    <style type=\"text/css\">\n      <!--\n        body { color: #000000; font-family: Dialog; font-size: 12px }\n      -->\n    </style>\r\n    \r\n  </head>\r\n  <body>\r\n    <p>\r\n      \r\n    </p>\r\n  </body>\r\n</html>\r\n"
  }
 ],
 "s:InteractionDiagram:InteractionOperand": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "109",
   "Id": "5sVcWbmA0I2A4hGq",
   "MetaModelElement": "5sVcWbmA0I2A4hGr",
   "Model": "5sVcWbmA0I2A4hGr",
   "ModelElementNameAlignment": "9",
   "Name": "Operand",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "697",
   "X": "341",
   "Y": "470",
   "ZOrder": "2"
  }
 ],
 "s:InteractionDiagram:Activation": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "80",
   "Id": "YEjGWbmA0I2A4hfT",
   "MetaModelElement": "gEjGWbmA0I2A4hfR",
   "Model": "gEjGWbmA0I2A4hfR",
   "ModelElementNameAlignment": "9",
   "Name": "Activation",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "8",
   "X": "656",
   "Y": "151",
   "ZOrder": "6"
  }
 ],
 "s:InteractionDiagram:CombinedFragment": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "207",
   "Id": "RsVcWbmA0I2A4hGm",
   "MetaModelElement": "RsVcWbmA0I2A4hGn",
   "Model": "RsVcWbmA0I2A4hGn",
   "ModelElementNameAlignment": "9",
   "Name": "",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "697",
   "X": "341",
   "Y": "452",
   "ZOrder": "14"
  }
 ],
 "s:InteractionDiagram:InteractionLifeLine": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "640",
   "Id": "drxIWbmA0I2A4gn2",
   "MetaModelElement": "drxIWbmA0I2A4gn3",
   "Model": "drxIWbmA0I2A4gn3",
   "ModelElementNameAlignment": "1",
   "Name": "EmployeeController",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "ParentFrame": "6ZrgWbmA0I2A4gnA",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowClassifier": "true",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "116",
   "X": "602",
   "Y": "40",
   "ZOrder": "18"
  }
 ],
 "s:InteractionDiagram:InteractionActor": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "640",
   "Id": "KCTwWbmA0I2A4gnP",
   "MetaModelElement": "GCTwWbmA0I2A4gnQ",
   "Model": "GCTwWbmA0I2A4gnQ",
   "ModelElementNameAlignment": "9",
   "Name": "Manager",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "ParentFrame": "6ZrgWbmA0I2A4gnA",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "60",
   "X": "73",
   "Y": "40",
   "ZOrder": "24"
  }
 ],
 "c:InteractionDiagram:Message": [
  {
   "Background": "rgb(0, 0, 0)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "Folded": "false",
   "Foreground": "rgb(0, 0, 0)",
   "From": "KCTwWbmA0I2A4gnP",
   "FromConnectType": "0",
   "FromPinType": "1",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "Height": "100",
   "Id": "TEjsWbmA0I2A4hCc",
   "MetaModelElement": "DEjsWbmA0I2A4hCZ",
   "Model": "DEjsWbmA0I2A4hCZ",
   "ModelElementNameAlignment": "9",
   "Name": "Chon \"Quan ly nhan vien\"",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowArgumentsInMessageOperationSignature": "0",
   "ShowConnectorName": "2",
   "ShowMessageName": "0",
   "ShowMessageOperationSignature": "0",
   "ShowParameterNamesInMessageOperationSignature": "0",
   "ShowParameterTypesInMessageOperationSignature": "0",
   "ShowReturnTypeInMessageOperationSignature": "0",
   "To": "CFRIWbmA0I2A4gni",
   "ToConnectType": "0",
   "ToPinType": "1",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "361",
   "X": "57",
   "Y": "86",
   "ZOrder": "26"
  }
 ],
 "s:InteractionDiagram:NOTE": [
  {
   "Angle": "0",
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "CreatorDiagramType": "InteractionDiagram",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "40",
   "Id": "J_t2WbmA0I2A4hvU",
   "MetaModelElement": "J_t2WbmA0I2A4hvV",
   "Model": "J_t2WbmA0I2A4hvV",
   "ModelElementNameAlignment": "9",
   "Name": "",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "208",
   "X": "362",
   "Y": "372",
   "ZOrder": "2"
  }
 ],
 "c:InteractionDiagram:Anchor": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "CreatorDiagramType": "InteractionDiagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "antmWbmA0I2A4hm2",
   "FromConnectType": "0",
   "FromPinType": "1",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "Height": "117",
   "Id": "CAd2WbmA0I2A4hva",
   "MetaModelElement": "8Ad2WbmA0I2A4hvZ",
   "Model": "8Ad2WbmA0I2A4hvZ",
   "ModelElementNameAlignment": "9",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowConnectorName": "2",
   "To": "J_t2WbmA0I2A4hvU",
   "ToConnectType": "0",
   "ToPinType": "1",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "100",
   "X": "408",
   "Y": "304",
   "ZOrder": "60"
  }
 ],
 "m:InteractionLifeLineLink": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "EndRelationshipFromMetaModelElement": "iv3ZVEEUG27Q4r73",
   "EndRelationshipToMetaModelElement": "7vzAKT08fDNFsNRA",
   "Id": "1hMLgYWFYCwGKQvN",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-10-28T16:21:46.091",
   "PmLastModified": "2026-10-28T16:22:11.613",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:InteractionLifeLineLinkEnd": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "EndModelElement": "iv3ZVEEUG27Q4r73",
   "Id": "LhMLgYWFYCwGKQvP",
   "Instance_IsNull": "true",
   "Multiplicity": "Unspecified",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-10-28T16:21:46.100",
   "PmLastModified_IsNull": "true",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "d:CommunicationDiagram": [
  {
   "AlignToGrid": "false",
   "AutoFitShapesSize": "false",
   "ConnectionPointStyle": "0",
   "ConnectorLabelOrientation": "0",
   "ConnectorLineJumps": "0",
   "ConnectorLineJumpsSize": "0",
   "ConnectorModelElementNameAlignment": "4",
   "ConnectorStyle": "1",
   "CreateOneMessagePerDirection": "true",
   "DiagramBackground": "rgb(255, 255, 255)",
   "Editable": "true",
   "FilterByViewpointLegend": "true",
   "FollowDiagramParentElement": "true",
   "GridColor": "rgb(192, 192, 192)",
   "GridHeight": "10",
   "GridVisible": "false",
   "GridWidth": "10",
   "Height": "598",
   "HideConnectorIfFromToIsHidden": "0",
   "HideEmptyTaggedValues": "false",
   "Id": "z2MLgYWFYCwGKQuq",
   "ImageHeight": "0",
   "ImageScale": "1.0",
   "ImageWidth": "0",
   "InitializeDiagramForCreate": "true",
   "InteractionLifeLinePresentationOption": "0",
   "Maximized": "true",
   "ModelElementNameAlignment": "4",
   "Name": "",
   "PaintConnectorThroughLabel": "1",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-10-28T16:21:45.715",
   "PmLastModified": "2026-10-28T16:22:47.101",
   "PointConnectorEndToCompartmentMember": "true",
   "QualityScore": "-1",
   "RequestFitSizeWithPromptUser": "false",
   "RequestValidateSnapToGrid": "false",
   "ShapePresentationOption": "0",
   "ShowActivityStateNodeCaption": "524287",
   "ShowAllocatedFrom": "true",
   "ShowAllocatedTo": "true",
   "ShowArgumentsInMessagesOperationSignature": "true",
   "ShowColorLegend": "false",
   "ShowConnectorLegend": "false",
   "ShowConnectorName": "0",
   "ShowConstraints": "false",
   "ShowDefaultPackage": "false",
   "ShowInformationItemOption": "2",
   "ShowMessagesOperationSignature": "true",
   "ShowPMAuthor": "false",
   "ShowPMDifficulty": "false",
   "ShowPMDiscipline": "false",
   "ShowPMIteration": "false",
   "ShowPMPhase": "false",
   "ShowPMPriority": "false",
   "ShowPMStatus": "false",
   "ShowPMVersion": "false",
   "ShowPackageNameStyle": "0",
   "ShowParameterNamesInMessageOperationSignature": "true",
   "ShowParameterTypesInMessageOperationSignature": "true",
   "ShowRelationshipConstraintExpression": "false",
   "ShowReturnTypeInMessagesOperationSignature": "true",
   "ShowSequenceNumbers": "true",
   "ShowShapeLegend": "false",
   "ShowShapeStereotypeIconName": "true",
   "ShowStereotypes": "true",
   "ShowTaggedValues": "false",
   "TeamworkCreateDateTime": "0",
   "TrimmedHeight": "0",
   "TrimmedWidth": "0",
   "Width": "1255",
   "X": "0",
   "Y": "0",
   "ZoomRatio": "1.0",
   "_globalPaletteOption": "true",
   "_interactionDiagram": "sj9Ebcwe0vHOxbGF",
   "_rootFrame": "SOMLgYWFYCwGKQuu"
  }
 ],
 "s:CommunicationDiagram:CommunicationActor": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "false",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "60",
   "Id": "KhMLgYWFYCwGKQuz",
   "MetaModelElement": "iv3ZVEEUG27Q4r73",
   "Model": "iv3ZVEEUG27Q4r73",
   "ModelElementNameAlignment": "9",
   "Name": "",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "0",
   "ParentConnectorLineLength": "0",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "true",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "30",
   "X": "1818",
   "Y": "80",
   "ZOrder": "84"
  }
 ],
 "s:CommunicationDiagram:CommunicationLifeLine": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "false",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "40",
   "Id": "GhMLgYWFYCwGKQu1",
   "MetaModelElement": "oRYPpY2tyicc2ZRQ",
   "Model": "oRYPpY2tyicc2ZRQ",
   "ModelElementNameAlignment": "9",
   "Name": ":TableMapUI",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "0",
   "ParentConnectorLineLength": "0",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "79",
   "X": "2165",
   "Y": "90",
   "ZOrder": "82"
  }
 ],
 "c:CommunicationDiagram:InteractionLifeLineLink": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "KhMLgYWFYCwGKQuz",
   "FromConnectType": "0",
   "FromPinType": "1",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "HasMultiplicityAShape": "false",
   "HasMultiplicityBShape": "false",
   "HasRoleAShape": "false",
   "HasRoleBShape": "false",
   "Height": "159",
   "Id": "ZhMLgYWFYCwGKQvL",
   "MetaModelElement": "1hMLgYWFYCwGKQvN",
   "Model": "1hMLgYWFYCwGKQvN",
   "ModelElementNameAlignment": "9",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowConnectorName": "2",
   "ShowMultiplicityConstraints": "false",
   "To": "JhMLgYWFYCwGKQvJ",
   "ToConnectType": "0",
   "ToPinType": "1",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "701",
   "X": "1182",
   "Y": "-20",
   "ZOrder": "86"
  }
 ],
 "c:CommunicationDiagram:CommunicationMessage": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "false",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "60",
   "Id": "IRMLgYWFYCwGKQvS",
   "MetaModelElement": "HgEP0ilTVREe1EHe",
   "Model": "HgEP0ilTVREe1EHe",
   "ModelElementNameAlignment": "9",
   "Name": "",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "-0.05092254653196247",
   "ParentConnectorHeaderLength": "81",
   "ParentConnectorLineLength": "29",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "60",
   "X": "1771",
   "Y": "29",
   "ZOrder": "60"
  }
 ],
 "c:CommunicationDiagram:CommunicationReverseMessage": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "60",
   "Id": "u5MLgYWFYCwGKQxN",
   "MetaModelElement": "SkqZUYro0Nfo0P3Y",
   "Model": "SkqZUYro0Nfo0P3Y",
   "ModelElementNameAlignment": "9",
   "Name": "",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "-1.008298395725824",
   "ParentConnectorHeaderLength": "20",
   "ParentConnectorLineLength": "46",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "60",
   "X": "889",
   "Y": "536",
   "ZOrder": "2"
  }
 ],
 "m:InitialPseudoState": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "Id": "BsSGbYSu1NxVKM7F",
   "Name": "",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-10-20T10:00:00.000",
   "PmLastModified": "2026-10-21T10:30:48.313",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "Unspecified"
  }
 ],
 "m:State2": [
  {
   "BacklogActivityId": "0",
   "DataModel_IsNull": "true",
   "Documentation": "",
   "Documentation_plain": "",
   "Id": "yeNTUF1pnKynQiQQ",
   "Name": "",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-10-20T10:00:00.000",
   "PmLastModified": "2026-10-21T10:30:48.296",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "StateInvariant": "",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:Transition2": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "From": "BsSGbYSu1NxVKM7F",
   "Id": "GYV3VsjjT421VoT9",
   "Kind": "External",
   "Name": "",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-10-20T10:00:00.000",
   "PmLastModified": "2026-10-21T10:30:48.296",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "To": "yeNTUF1pnKynQiQQ",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:FinalState2": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "DoneData_IsNull": "true",
   "Id": "sSZPpYWFYC1QOhVW",
   "Name": "123",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T16:44:48.525",
   "PmLastModified": "2026-11-04T16:45:10.132",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "StateInvariant": "",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "d:StateDiagram": [
  {
   "AlignToGrid": "false",
   "AutoFitShapesSize": "false",
   "ConnectionPointStyle": "0",
   "ConnectorLabelOrientation": "0",
   "ConnectorLineJumps": "0",
   "ConnectorLineJumpsSize": "0",
   "ConnectorModelElementNameAlignment": "4",
   "ConnectorStyle": "1",
   "DiagramBackground": "rgb(255, 255, 255)",
   "Editable": "true",
   "FilterByViewpointLegend": "true",
   "FollowDiagramParentElement": "true",
   "GridColor": "rgb(192, 192, 192)",
   "GridHeight": "10",
   "GridVisible": "false",
   "GridWidth": "10",
   "Height": "598",
   "HideConnectorIfFromToIsHidden": "0",
   "HideEmptyTaggedValues": "false",
   "Id": "xlDDZVqE7Iz4vOtY",
   "ImageHeight": "0",
   "ImageScale": "1.0",
   "ImageWidth": "0",
   "InitializeDiagramForCreate": "false",
   "Maximized": "true",
   "ModelElementNameAlignment": "4",
   "Name": "",
   "PaintConnectorThroughLabel": "1",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-10-20T10:00:00.000",
   "PmLastModified": "2026-11-04T16:45:09.950",
   "PointConnectorEndToCompartmentMember": "true",
   "ProtocolStateMachine": "false",
   "QualityScore": "-1",
   "RequestFitSizeWithPromptUser": "false",
   "RequestValidateSnapToGrid": "false",
   "ShapePresentationOption": "0",
   "ShowActivityStateNodeCaption": "524287",
   "ShowAllocatedFrom": "true",
   "ShowAllocatedTo": "true",
   "ShowColorLegend": "false",
   "ShowConnectorLegend": "false",
   "ShowConnectorName": "0",
   "ShowConstraints": "false",
   "ShowDefaultPackage": "false",
   "ShowDiagramFrame": "true",
   "ShowInformationItemOption": "2",
   "ShowPMAuthor": "false",
   "ShowPMDifficulty": "false",
   "ShowPMDiscipline": "false",
   "ShowPMIteration": "false",
   "ShowPMPhase": "false",
   "ShowPMPriority": "false",
   "ShowPMStatus": "false",
   "ShowPMVersion": "false",
   "ShowPackageNameStyle": "0",
   "ShowRelationshipConstraintExpression": "false",
   "ShowShapeLegend": "false",
   "ShowShapeStereotypeIconName": "true",
   "ShowStereotypes": "true",
   "ShowTaggedValues": "false",
   "ShowTransitionEffectBody": "false",
   "StateUseNameTab": "2",
   "TeamworkCreateDateTime": "0",
   "TrimmedHeight": "0",
   "TrimmedWidth": "0",
   "Width": "1255",
   "X": "0",
   "Y": "0",
   "ZoomRatio": "1.0",
   "_centerStateCaptionVertically": "false",
   "_globalPaletteOption": "true",
   "_showRegionName": "2",
   "_showTransitionOperation": "false",
   "_showTransitionOperationParameter": "true",
   "_showTransitionTriggers": "true",
   "_stateShowParametersOfInternalActivities": "false",
   "_stateShowPreconditionPostconditionAndBodyOfInternalActivities": "true"
  }
 ],
 "s:StateDiagram:InitialPseudoState": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "1",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "20",
   "Id": "chsgjVHxPxO3hONX",
   "MetaModelElement": "BsSGbYSu1NxVKM7F",
   "Model": "BsSGbYSu1NxVKM7F",
   "ModelElementNameAlignment": "9",
   "Name": "",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "20",
   "X": "50",
   "Y": "170",
   "ZOrder": "4"
  }
 ],
 "s:StateDiagram:State2": [
  {
   "Background": "rgb(122, 207, 245)",
   "CenterCaptionVertically": "0",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "50",
   "Id": "bpsgN4m6AsDdAhKZ",
   "MetaModelElement": "yeNTUF1pnKynQiQQ",
   "Model": "yeNTUF1pnKynQiQQ",
   "ModelElementNameAlignment": "9",
   "Name": "",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RegionOrientation": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowInternalActivities": "true",
   "ShowInternalTransitions": "true",
   "ShowParametersOfInternalActivities": "0",
   "ShowPreconditionPostconditionAndBodyOfInternalActivities": "0",
   "ShowRegionName": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "UseNameTab": "0",
   "Width": "200",
   "X": "282",
   "Y": "155",
   "ZOrder": "6"
  }
 ],
 "s:StateDiagram:FinalState2": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "1",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "20",
   "Id": "0SZPpYWFYC1QOhVV",
   "MetaModelElement": "sSZPpYWFYC1QOhVW",
   "Model": "sSZPpYWFYC1QOhVW",
   "ModelElementNameAlignment": "9",
   "Name": "123",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "20",
   "X": "802",
   "Y": "277",
   "ZOrder": "2"
  }
 ],
 "c:StateDiagram:Transition2": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "chsgjVHxPxO3hONX",
   "FromConnectType": "0",
   "FromPinType": "1",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "Height": "100",
   "Id": "OyUdXBsxeX4VQ2gu",
   "MetaModelElement": "GYV3VsjjT421VoT9",
   "Model": "GYV3VsjjT421VoT9",
   "ModelElementNameAlignment": "9",
   "Name": "",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowConnectorName": "2",
   "ShowOperation": "0",
   "ShowOperationParameter": "0",
   "To": "bpsgN4m6AsDdAhKZ",
   "ToConnectType": "0",
   "ToPinType": "1",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "313",
   "X": "18",
   "Y": "130",
   "ZOrder": "10"
  }
 ],
 "m:DBForeignKey": [
  {
   "BacklogActivityId": "0",
   "DataModel": "Physical",
   "Documentation_plain": "",
   "ForeignKeyRelationshipPattern": "{association_name}",
   "From": "U4igZYWFYC1QOghP",
   "FromMultiplicity": "1",
   "FromPhrase_IsNull": "true",
   "Id": "4sPgZYWFYC1QOgmC",
   "Identifying": "false",
   "Name": "",
   "OnDelete": "",
   "OnUpdate": "",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T17:08:09.031",
   "PmLastModified": "2026-11-04T17:08:29.638",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Subtype": "false",
   "SyncToAssociation": "Yes",
   "SyncType": "Not Sync",
   "To": "RwKgZYWFYC1QOghk",
   "ToMultiplicity": "1",
   "ToPhrase_IsNull": "true",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:DBTable": [
  {
   "BacklogActivityId": "0",
   "DDLClauses_IsNull": "true",
   "DataModel": "Physical",
   "Documentation_plain": "",
   "Id": "U4igZYWFYC1QOghP",
   "Location_IsNull": "true",
   "Name": "Table",
   "OrmSyncState": "Not Sync",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T17:05:12.522",
   "PmLastModified": "2026-11-04T17:08:29.638",
   "PrimaryKeyClustered": "Unspecified",
   "PrimaryKeyConstraintNamePattern": "",
   "PrimaryKeyConstraintName_IsNull": "true",
   "PrimaryKeyDDLClauses_IsNull": "true",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "SyncType": "Not Sync",
   "Temporal": "false",
   "TemporalEndTimeColumn_IsNull": "true",
   "TemporalHistoryTable_IsNull": "true",
   "TemporalStartTimeColumn_IsNull": "true",
   "Type": "0",
   "Unlogged": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:DBColumn": [
  {
   "BacklogActivityId": "0",
   "CheckConstraint_IsNull": "true",
   "Collation_IsNull": "true",
   "DDLClauses_IsNull": "true",
   "DbColumnName_IsNull": "true",
   "DefaultValue_IsNull": "true",
   "Documentation_plain": "",
   "ForeignKeyNamePattern_IsNull": "true",
   "Generated": "Unspecified",
   "Id": "mDFgZYWFYC1QOgky",
   "IdGenerator_IsNull": "true",
   "IdentityIncrement": "-1",
   "IdentitySeed": "-1",
   "Index": "false",
   "Length": "10",
   "Name": "maBan",
   "Nullable": "false",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T17:06:49.369",
   "PmLastModified": "2026-11-04T17:07:28.503",
   "PrimaryKey": "true",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Scale": "0",
   "SequenceAllocationSize": "-1",
   "SyncToAttribute": "Yes",
   "SyncType": "Not Sync",
   "Type": "integer",
   "TypeName_IsNull": "true",
   "Type_internalValue": "9",
   "Unique": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  },
  {
   "BacklogActivityId": "0",
   "CheckConstraint_IsNull": "true",
   "Collation_IsNull": "true",
   "DDLClauses_IsNull": "true",
   "DbColumnName_IsNull": "true",
   "DefaultValue_IsNull": "true",
   "Documentation_plain": "",
   "ForeignKeyNamePattern": "{reference_table_name}{reference_column_name}",
   "Generated": "Unspecified",
   "Id": "VsPgZYWFYC1QOgmF",
   "IdGenerator": "native",
   "IdentityIncrement": "-1",
   "IdentitySeed": "-1",
   "Index": "false",
   "Length": "10",
   "Name": "TablemaBan",
   "Nullable": "false",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T17:08:09.066",
   "PmLastModified": "2026-11-04T17:08:29.638",
   "PrimaryKey": "false",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Scale": "0",
   "SequenceAllocationSize": "-1",
   "SyncToAttribute": "Yes",
   "SyncType": "Not Sync",
   "Type": "integer",
   "TypeName_IsNull": "true",
   "Type_internalValue": "9",
   "Unique": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "m:DBView": [
  {
   "BacklogActivityId": "0",
   "CheckOption": "None",
   "CreateStatement_IsNull": "true",
   "CustomizedCreateStatement": "false",
   "DataModel": "Physical",
   "Distinct": "false",
   "Documentation_plain": "",
   "Id": ".ySgZYWFYC1QOghZ",
   "Insertable": "false",
   "Name": "View",
   "OrmSyncState": "Not Sync",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T17:05:17.407",
   "PmLastModified": "2026-11-04T17:08:29.638",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "SyncType": "Not Sync",
   "Type": "0",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "ViewEditorDiagramId_IsNull": "true"
  }
 ],
 "m:DBForeignKeyConstraint": [
  {
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "ForeignKey": "4sPgZYWFYC1QOgmC",
   "Id": "VsPgZYWFYC1QOgmH",
   "Name": "",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T17:08:09.066",
   "PmLastModified_IsNull": "true",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "RefColumn": "mDFgZYWFYC1QOgky",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true"
  }
 ],
 "d:ERDiagram": [
  {
   "AlignToGrid": "false",
   "AutoFitShapesSize": "false",
   "ConnectionPointStyle": "0",
   "ConnectorLabelOrientation": "0",
   "ConnectorLineJumps": "0",
   "ConnectorLineJumpsSize": "0",
   "ConnectorModelElementNameAlignment": "4",
   "ConnectorStyle": "1",
   "DataModel": "2",
   "DiagramBackground": "rgb(255, 255, 255)",
   "Editable": "true",
   "FilterByViewpointLegend": "true",
   "FollowDiagramParentElement": "true",
   "ForeignKeyArrowHeadSize": "3",
   "GridColor": "rgb(192, 192, 192)",
   "GridHeight": "10",
   "GridVisible": "false",
   "GridWidth": "10",
   "Height": "598",
   "HideConnectorIfFromToIsHidden": "0",
   "HideEmptyTaggedValues": "false",
   "Id": "in8gZYWFYC1QOggy",
   "ImageHeight": "0",
   "ImageScale": "1.0",
   "ImageWidth": "0",
   "InitializeDiagramForCreate": "true",
   "LogicalPhysicalColumnNameAbbreviationSetAddress": "",
   "LogicalPhysicalEntityNameAbbreviationSetAddress": "",
   "LogicalPhysicalSchemaNameAbbreviationSetAddress": "",
   "Maximized": "true",
   "ModelElementNameAlignment": "4",
   "Name": "Entity Relationship Diagram1",
   "PaintConnectorThroughLabel": "1",
   "PmAuthor": "phanb",
   "PmCreateDateTime": "2026-11-04T17:05:07.537",
   "PmLastModified": "2026-11-04T17:08:45.708",
   "PointConnectorEndToCompartmentMember": "true",
   "QualityScore": "-1",
   "RequestFitSizeWithPromptUser": "false",
   "RequestValidateSnapToGrid": "false",
   "ShapePresentationOption": "0",
   "ShowActivityStateNodeCaption": "524287",
   "ShowAllocatedFrom": "true",
   "ShowAllocatedTo": "true",
   "ShowColorLegend": "false",
   "ShowConnectorLegend": "false",
   "ShowConnectorName": "0",
   "ShowConstraints": "false",
   "ShowDefaultPackage": "false",
   "ShowInformationItemOption": "2",
   "ShowPMAuthor": "false",
   "ShowPMDifficulty": "false",
   "ShowPMDiscipline": "false",
   "ShowPMIteration": "false",
   "ShowPMPhase": "false",
   "ShowPMPriority": "false",
   "ShowPMStatus": "false",
   "ShowPMVersion": "false",
   "ShowPackageNameStyle": "0",
   "ShowRelationshipConstraintExpression": "false",
   "ShowSchemaName": "true",
   "ShowShapeLegend": "false",
   "ShowShapeStereotypeIconName": "true",
   "ShowStereotypes": "true",
   "ShowTaggedValues": "false",
   "TeamworkCreateDateTime": "0",
   "TrimmedHeight": "0",
   "TrimmedWidth": "0",
   "Width": "1255",
   "X": "0",
   "Y": "0",
   "ZoomRatio": "1.0",
   "_alignColumnProperties": "true",
   "_columnConstraintsDisplayOption": "2",
   "_globalPaletteOption": "true",
   "_pointForeignKeyEndToColumn": "false",
   "_showColumnDefaultValue": "false",
   "_showColumnStereotypes": "true",
   "_showColumnTypes": "true",
   "_showColumnUserType": "false",
   "_showDBTableColumnsMode": "1",
   "_showDBViewColumnsMode": "1",
   "_showExtraColumnProperties": "true",
   "_showProcedureStereotypes": "true",
   "_showStoredProcedureResultSetColumns": "true",
   "_showStoredProcedures": "true",
   "_showTriggerStereotypes": "true",
   "_showTriggers": "true"
  }
 ],
 "s:ERDiagram:DBTable": [
  {
   "Background": "rgb(245, 182, 122)",
   "ColSortType": "0",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "CreatorDiagramType": "ERDiagram",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "77",
   "Id": "E4igZYWFYC1QOghO",
   "MetaModelElement": "U4igZYWFYC1QOghP",
   "Model": "U4igZYWFYC1QOghP",
   "ModelElementNameAlignment": "9",
   "Name": "Table",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowColumnStereotypes": "0",
   "ShowColumnsMode": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "173",
   "X": "125",
   "Y": "84",
   "ZOrder": "12"
  }
 ],
 "s:ERDiagram:DBView": [
  {
   "Background": "rgb(245, 182, 122)",
   "ColSortType": "0",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "CreatorDiagramType": "ERDiagram",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "41",
   "Id": "uySgZYWFYC1QOghY",
   "MetaModelElement": ".ySgZYWFYC1QOghZ",
   "Model": ".ySgZYWFYC1QOghZ",
   "ModelElementNameAlignment": "9",
   "Name": "View",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowColumnStereotypes": "0",
   "ShowColumnsMode": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "88",
   "X": "490",
   "Y": "70",
   "ZOrder": "10"
  }
 ],
 "c:ERDiagram:DBForeignKey": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "CreatorDiagramType": "ERDiagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "E4igZYWFYC1QOghO",
   "FromConnectType": "0",
   "FromPinType": "1",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "HasFromLabel": "false",
   "HasToLabel": "false",
   "Height": "176",
   "Id": "WsPgZYWFYC1QOgmD",
   "MetaModelElement": "4sPgZYWFYC1QOgmC",
   "Model": "4sPgZYWFYC1QOgmC",
   "ModelElementNameAlignment": "9",
   "Name": "",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestResetLabels": "false",
   "Selectable": "true",
   "ShowConnectorName": "2",
   "To": "RwKgZYWFYC1QOghj",
   "ToConnectType": "0",
   "ToPinType": "1",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "100",
   "X": "137",
   "Y": "111",
   "ZOrder": "14"
  }
 ],
 "m:Realization": [
  {
   "BacklogActivityId": "0",
   "ConnectToCodeModel": "1",
   "Documentation_plain": "",
   "From": "KWjRk4WFYCyCBxNQ",
   "Id": "_WjRk4WFYCyCBxNx",
   "Mapping_IsNull": "true",
   "PmAuthor": "",
   "PmCreateDateTime": "2017-06-22T09:42:49.077",
   "PmLastModified": "2026-11-11T14:38:18.400",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "To": "wWjRk4WFYCyCBxNP",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "Unspecified"
  }
 ],
 "m:Node": [
  {
   "Abstract": "false",
   "Active": "false",
   "BacklogActivityId": "0",
   "BusinessKeyMutable": "true",
   "BusinessModel": "false",
   "ConnectToCodeModel": "1",
   "Documentation_plain": "",
   "FinalSpecialization": "false",
   "Id": "LmjRk4WFYCyCBxNK",
   "Leaf": "false",
   "Name": "Bank Server",
   "PmAuthor": "",
   "PmCreateDateTime": "2017-06-22T09:41:19.656",
   "PmLastModified": "2026-11-11T14:38:18.400",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Root": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "public"
  }
 ],
 "m:Artifact": [
  {
   "Abstract": "false",
   "BacklogActivityId": "0",
   "Documentation_plain": "",
   "FileName_IsNull": "true",
   "FinalSpecialization": "false",
   "Id": "wWjRk4WFYCyCBxNN",
   "Leaf": "false",
   "Name": "Customer DB",
   "PmAuthor": "",
   "PmCreateDateTime": "2017-06-22T09:41:50.692",
   "PmLastModified": "2026-11-11T14:38:18.400",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "Unspecified"
  }
 ],
 "m:Component": [
  {
   "Abstract": "false",
   "Active": "false",
   "BacklogActivityId": "0",
   "BusinessKeyMutable": "true",
   "BusinessModel": "false",
   "ConnectToCodeModel": "1",
   "Documentation_plain": "",
   "FinalSpecialization": "false",
   "Id": "wWjRk4WFYCyCBxNP",
   "IndirectlyInstantiated": "true",
   "Leaf": "false",
   "Name": "Mortgage Application",
   "PmAuthor": "",
   "PmCreateDateTime": "2017-06-22T09:42:27.054",
   "PmLastModified": "2026-11-11T14:38:18.400",
   "QualityReason_IsNull": "true",
   "QualityScore": "-1",
   "Root": "false",
   "UserIDLastNumericValue": "0",
   "UserID_IsNull": "true",
   "Visibility": "public"
  }
 ],
 "d:DeploymentDiagram": [
  {
   "AlignToGrid": "false",
   "AutoFitShapesSize": "false",
   "ConnectionPointStyle": "0",
   "ConnectorLabelOrientation": "0",
   "ConnectorLineJumps": "0",
   "ConnectorLineJumpsSize": "0",
   "ConnectorModelElementNameAlignment": "4",
   "ConnectorStyle": "1",
   "DiagramBackground": "rgb(255, 255, 255)",
   "Editable": "true",
   "FilterByViewpointLegend": "true",
   "FollowDiagramParentElement": "true",
   "GridColor": "rgb(192, 192, 192)",
   "GridHeight": "10",
   "GridVisible": "false",
   "GridWidth": "10",
   "Height": "598",
   "HideConnectorIfFromToIsHidden": "0",
   "HideEmptyTaggedValues": "false",
   "Id": "42jRk4WFYCyCBxN4",
   "ImageHeight": "0",
   "ImageScale": "1.0",
   "ImageWidth": "0",
   "InitializeDiagramForCreate": "true",
   "Maximized": "true",
   "ModelElementNameAlignment": "4",
   "Name": "Deployment Diagram with Components",
   "PaintConnectorThroughLabel": "1",
   "ParentModel": "LmjRk4WFYCyCBxNH",
   "PmAuthor": "",
   "PmCreateDateTime": "2017-06-22T09:41:16.300",
   "PmLastModified": "2017-06-22T15:44:54.591",
   "PointConnectorEndToCompartmentMember": "true",
   "QualityScore": "-1",
   "RequestFitSizeWithPromptUser": "false",
   "RequestValidateSnapToGrid": "false",
   "ShapePresentationOption": "0",
   "ShowActivityStateNodeCaption": "65535",
   "ShowAllocatedFrom": "true",
   "ShowAllocatedTo": "true",
   "ShowColorLegend": "false",
   "ShowComponentAttributes": "false",
   "ShowComponentOperations": "false",
   "ShowConnectorLegend": "false",
   "ShowConnectorName": "0",
   "ShowConstraints": "false",
   "ShowDefaultPackage": "false",
   "ShowInformationItemOption": "2",
   "ShowNodeAttributes": "false",
   "ShowNodeOperations": "false",
   "ShowPMAuthor": "false",
   "ShowPMDifficulty": "false",
   "ShowPMDiscipline": "false",
   "ShowPMIteration": "false",
   "ShowPMPhase": "false",
   "ShowPMPriority": "false",
   "ShowPMStatus": "false",
   "ShowPMVersion": "false",
   "ShowPackageNameStyle": "0",
   "ShowPortMultiplicityOption": "3",
   "ShowRelationshipConstraintExpression": "false",
   "ShowShapeLegend": "false",
   "ShowShapeStereotypeIconName": "true",
   "ShowStereotypes": "true",
   "ShowTaggedValues": "false",
   "TeamworkAuthor": "Jick Yeung",
   "TeamworkCreateDateTime": "1498117490289",
   "TrimmedHeight": "0",
   "TrimmedWidth": "0",
   "Width": "1255",
   "X": "0",
   "Y": "0",
   "ZoomRatio": "1.0",
   "_globalPaletteOption": "true",
   "_showArtifactOption": "2",
   "_showComponentOption": "2",
   "documentation": "<html>\r\n  <head>\r\n    <style type=\"text/css\">\n      <!--\n        body { color: #000000; font-family: Dialog; font-size: 12px }\n      -->\n    </style>\r\n    \r\n  </head>\r\n  <body>\r\n    <p>\r\n      \r\n    </p>\r\n  </body>\r\n</html>\r\n"
  }
 ],
 "s:DeploymentDiagram:Node": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "94",
   "Id": "m2jRk4WFYCyCBxN6",
   "MetaModelElement": "KWjRk4WFYCyCBxNV",
   "Model": "KWjRk4WFYCyCBxNV",
   "ModelElementNameAlignment": "9",
   "Name": "PC",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowAttributesMode": "0",
   "ShowOperationsMode": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "177",
   "X": "312",
   "Y": "236",
   "ZOrder": "4"
  }
 ],
 "s:DeploymentDiagram:Component": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "DisplayOption": "0",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "40",
   "Id": "p2jRk4WFYCyCBxN8",
   "MetaModelElement": "KWjRk4WFYCyCBxNW",
   "Model": "KWjRk4WFYCyCBxNW",
   "ModelElementNameAlignment": "1",
   "Name": "BuyerInterface",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowAttributesMode": "0",
   "ShowOperationsMode": "0",
   "ShowOption": "-1",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "153",
   "X": "321",
   "Y": "274",
   "ZOrder": "2"
  },
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "CreatorDiagramType": "DeploymentDiagram",
   "DisplayOption": "0",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "40",
   "Id": "j2jRk4WFYCyCBxOK",
   "MetaModelElement": "wWjRk4WFYCyCBxNP",
   "Model": "wWjRk4WFYCyCBxNP",
   "ModelElementNameAlignment": "1",
   "Name": "Mortgage Application",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowAttributesMode": "0",
   "ShowOperationsMode": "0",
   "ShowOption": "-1",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "153",
   "X": "48",
   "Y": "73",
   "ZOrder": "16"
  }
 ],
 "s:DeploymentDiagram:StructuredInterface": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "1",
   "CoverConnector": "false",
   "DisplayOption": "0",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "20",
   "Id": "l2jRk4WFYCyCBxN.",
   "MetaModelElement": "KWjRk4WFYCyCBxNU",
   "Model": "KWjRk4WFYCyCBxNU",
   "ModelElementNameAlignment": "9",
   "Name": "ILIsting",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "20",
   "X": "489",
   "Y": "141",
   "ZOrder": "6"
  },
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "1",
   "CoverConnector": "false",
   "CreatorDiagramType": "DeploymentDiagram",
   "DisplayOption": "0",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "20",
   "Id": "d2jRk4WFYCyCBxOG",
   "MetaModelElement": "KWjRk4WFYCyCBxNQ",
   "Model": "KWjRk4WFYCyCBxNQ",
   "ModelElementNameAlignment": "9",
   "Name": "IMortgageApplication",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "20",
   "X": "114",
   "Y": "141",
   "ZOrder": "14"
  }
 ],
 "s:DeploymentDiagram:Artifact": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "40",
   "Id": "12jRk4WFYCyCBxOE",
   "MetaModelElement": "KWjRk4WFYCyCBxNS",
   "Model": "KWjRk4WFYCyCBxNS",
   "ModelElementNameAlignment": "1",
   "Name": "Multiple Listings",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowOption": "-1",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "136",
   "X": "622",
   "Y": "73",
   "ZOrder": "10"
  },
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectToPoint": "true",
   "ConnectionPointType": "2",
   "CoverConnector": "false",
   "CreatorDiagramType": "DeploymentDiagram",
   "Foreground": "rgb(0, 0, 0)",
   "Height": "40",
   "Id": "r2jRk4WFYCyCBxOM",
   "MetaModelElement": "wWjRk4WFYCyCBxNN",
   "Model": "wWjRk4WFYCyCBxNN",
   "ModelElementNameAlignment": "1",
   "Name": "Customer DB",
   "OverrideAppearanceWithStereotypeIcon": "true",
   "ParentConnectorDTheta": "0.0",
   "ParentConnectorHeaderLength": "40",
   "ParentConnectorLineLength": "10",
   "PresentationOption": "4",
   "PrimitiveShapeType": "0",
   "RequestDefaultSize": "false",
   "RequestFitSize": "false",
   "RequestFitSizeFromCenter": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "RequestSetSizeOption": "0",
   "Selectable": "true",
   "ShowAllocatedFrom": "0",
   "ShowAllocatedTo": "0",
   "ShowOption": "-1",
   "ShowStereotypeIconName": "0",
   "ShowTaggedValues": "0",
   "Width": "120",
   "X": "251",
   "Y": "73",
   "ZOrder": "18"
  }
 ],
 "c:DeploymentDiagram:Realization": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "CreatorDiagramType": "DeploymentDiagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "d2jRk4WFYCyCBxOG",
   "FromConnectType": "0",
   "FromPinType": "1",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "Height": "228",
   "Id": "72jRk4WFYCyCBxOO",
   "MetaModelElement": "_WjRk4WFYCyCBxNx",
   "Model": "_WjRk4WFYCyCBxNx",
   "ModelElementNameAlignment": "9",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowConnectorName": "2",
   "To": "j2jRk4WFYCyCBxOK",
   "ToConnectType": "0",
   "ToPinType": "1",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "200",
   "X": "24",
   "Y": "14",
   "ZOrder": "22"
  },
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "l2jRk4WFYCyCBxN.",
   "FromConnectType": "0",
   "FromPinType": "1",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "Height": "228",
   "Id": "32jRk4WFYCyCBxOU",
   "MetaModelElement": "_WjRk4WFYCyCBxNy",
   "Model": "_WjRk4WFYCyCBxNy",
   "ModelElementNameAlignment": "9",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowConnectorName": "2",
   "To": "12jRk4WFYCyCBxOC",
   "ToConnectType": "0",
   "ToPinType": "1",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "200",
   "X": "399",
   "Y": "14",
   "ZOrder": "28"
  }
 ],
 "c:DeploymentDiagram:Dependency": [
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "CreatorDiagramType": "DeploymentDiagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "j2jRk4WFYCyCBxOK",
   "FromConnectType": "0",
   "FromPinType": "1",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "Height": "200",
   "Id": "n2jRk4WFYCyCBxOQ",
   "MetaModelElement": "g2jRk4WFYCyCBxN0",
   "Model": "g2jRk4WFYCyCBxN0",
   "ModelElementNameAlignment": "9",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowConnectorName": "2",
   "To": "r2jRk4WFYCyCBxOM",
   "ToConnectType": "0",
   "ToPinType": "1",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "248",
   "X": "102",
   "Y": "-7",
   "ZOrder": "24"
  },
  {
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "12jRk4WFYCyCBxOC",
   "FromConnectType": "0",
   "FromPinType": "1",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "Height": "200",
   "Id": "n2jRk4WFYCyCBxOS",
   "MetaModelElement": "g2jRk4WFYCyCBxN1",
   "Model": "g2jRk4WFYCyCBxN1",
   "ModelElementNameAlignment": "9",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowConnectorName": "2",
   "To": "12jRk4WFYCyCBxOE",
   "ToConnectType": "0",
   "ToPinType": "1",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "254",
   "X": "467",
   "Y": "-7",
   "ZOrder": "26"
  }
 ],
 "c:DeploymentDiagram:Association": [
  {
   "AssociationEndPropertyStringsAInternalHeight": "-2147483648",
   "AssociationEndPropertyStringsAInternalWidth": "-2147483648",
   "AssociationEndPropertyStringsBInternalHeight": "-2147483648",
   "AssociationEndPropertyStringsBInternalWidth": "-2147483648",
   "Background": "rgb(122, 207, 245)",
   "ConnectorLabelOrientation": "4",
   "ConnectorLineJumps": "4",
   "ConnectorStyle": "Follow Diagram",
   "CreatorDiagramType": "DeploymentDiagram",
   "Foreground": "rgb(0, 0, 0)",
   "From": "m2jRk4WFYCyCBxN6",
   "FromConnectType": "0",
   "FromMultiplicityInternalHeight": "-2147483648",
   "FromMultiplicityInternalWidth": "-2147483648",
   "FromPinType": "1",
   "FromRoleInternalHeight": "-2147483648",
   "FromRoleInternalWidth": "-2147483648",
   "FromShapeXDiff": "0",
   "FromShapeYDiff": "0",
   "HasAssociationEndPropertyStringsAShape": "false",
   "HasAssociationEndPropertyStringsBShape": "false",
   "HasMultiplicityAShape": "false",
   "HasMultiplicityBShape": "false",
   "HasRoleAShape": "false",
   "HasRoleBShape": "false",
   "Height": "286",
   "Id": "v2jRk4WFYCyCBxOa",
   "MetaModelElement": "KWjRk4WFYCyCBxNZ",
   "Model": "KWjRk4WFYCyCBxNZ",
   "ModelElementNameAlignment": "9",
   "Name": "TCP/IP",
   "PaintThroughLabel": "2",
   "RequestRebuild": "false",
   "RequestRebuildFromEnd": "false",
   "RequestRebuildToEnd": "false",
   "RequestResetCaption": "false",
   "RequestResetCaptionFitWidth": "false",
   "RequestResetCaptionSize": "false",
   "Selectable": "true",
   "ShowAssociationEndPropertyStrings": "false",
   "ShowConnectorName": "2",
   "ShowDirection": "false",
   "ShowFromMultiplicity": "true",
   "ShowFromRoleName": "true",
   "ShowFromRoleVisibility": "true",
   "ShowMultiplicityConstraints": "false",
   "ShowNavigationArrows": "0",
   "ShowOrderedMultiplicityConstraint": "true",
   "ShowStereotypes": "true",
   "ShowToMultiplicity": "true",
   "ShowToRoleName": "true",
   "ShowToRoleVisibility": "true",
   "ShowUniqueMultiplicityConstraint": "true",
   "SuppressImplied1MultiplicityForAssociationEnd": "0",
   "To": "l2jRk4WFYCyCBxOA",
   "ToConnectType": "0",
   "ToMultiplicityInternalHeight": "-2147483648",
   "ToMultiplicityInternalWidth": "-2147483648",
   "ToPinType": "1",
   "ToRoleInternalHeight": "-2147483648",
   "ToRoleInternalWidth": "-2147483648",
   "ToShapeXDiff": "0",
   "ToShapeYDiff": "0",
   "UseFromShapeCenter": "true",
   "UseToShapeCenter": "true",
   "Width": "314",
   "X": "388",
   "Y": "97",
   "ZOrder": "34"
  }
 ]
}
```

</details>

### `assets/project_header.tmpl`

<details>
<summary>Mở nội dung tệp</summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Project Author="{AUTHOR}" CommentTableSortAscending="false" CommentTableSortColumn="Date Time" Description="&lt;html&gt;&#13;&#10;  &lt;head&gt;&#13;&#10;    &lt;style type=&quot;text/css&quot;&gt;&#10;      &lt;!--&#10;        body { color: #000000; font-family: Dialog; font-size: 12px }&#10;      --&gt;&#10;    &lt;/style&gt;&#13;&#10;    &#13;&#10;  &lt;/head&gt;&#13;&#10;  &lt;body&gt;&#13;&#10;  &lt;/body&gt;&#13;&#10;&lt;/html&gt;&#13;&#10;" DocumentationType="html" ExportedFromDifferentName="false" ExporterVersion="16.1.1" Name="{NAME}" TextualAnalysisHighlightOptionCaseSensitive="false" UmlVersion="2.x" Xml_structure="simple">
	<ProjectInfo>
		{ORMINFO}<LogicalView/>
		<ProjectOptions>
			<DiagramOptions ActivityDiagramControlFlowDisplayOption="\u0000" ActivityDiagramShowActionCallBehaviorOption="\u0000" ActivityDiagramShowActivityEdgeWeight="true" ActivityDiagramShowDiagramFrame="true" ActivityDiagramShowObjectNodeType="true" ActivityDiagramShowPartitionHandle="\u0000" AddDataStoresExtEntitiesToDecomposedDFD="\u0002" AlignColumnProperties="true" AllowConfigShowInOutFlowButtonsInDataFlowDiagram="false" AutoGenerateRoleName="false" AutoSetAttributeType="true" AutoSetColumnType="true" AutoSyncRoleName="true" BlockDefinitionDiagramShowDiagramFrame="true" BpPoolLaneDefaultOrientation="\u0000" BpdAutoStretchPools="true" BpdConnectGatewayWithFlowObjectInDifferentPool="\u0000" BpdDefaultConnectionPointStyle="\u0001" BpdDefaultConnectorStyle="\u0005" BpdDhowIdOption="\u0000" BpdShowActivitiesTypeIcon="true" BusinessProcessDiagramDefaultLanguage="English" ClassVisibilityStyle="\u0001" ConnectorLabelOrientation="\u0000" CreateOneMessagePerDirection="true" DecisionMergeNodeConnectionPointStyle="\u0000" DefaultAssociationEndNavigable="\u0001" DefaultAssociationEndVisibility="\u0000" DefaultAssociationShowFromMultiplicity="true" DefaultAssociationShowFromRoleName="true" DefaultAssociationShowFromRoleVisibility="true" DefaultAssociationShowStereotypes="true" DefaultAssociationShowToMultiplicity="true" DefaultAssociationShowToRoleName="true" DefaultAssociationShowToRoleVisibility="true" DefaultAttributeMultiplicity="false" DefaultAttributeType="" DefaultAttributeVisibility="\u0001" DefaultClassAttributeMultiplicity="" DefaultClassAttributeMultiplicityOrdered="false" DefaultClassAttributeMultiplicityUnique="true" DefaultClassInterfaceBall="false" DefaultClassVisibility="\u0004" DefaultColumnType="integer(10)" DefaultConnectionPointStyle="\u0000" DefaultConnectorStyle="\u0001" DefaultDiagramBackground="rgb(255, 255, 255)" DefaultDisplayAsRobustnessAnalysisIcon="true" DefaultDisplayAsRobustnessAnalysisIconInSequenceDiagram="true" DefaultDisplayAsStereotypeIcon="false" DefaultFontColor="rgb(0, 0, 0)" DefaultGenDiagramTypeFromScenario="\u0000" DefaultHtmlDocFontColor="rgb(0, 0, 0)" DefaultLineJumps="\u0000" DefaultOperationVisibility="\u0004" DefaultParameterDirection="\u0002" DefaultShowAttributeInitialValue="true" DefaultShowAttributeOption="\u0001" DefaultShowClassMemberStereotype="true" DefaultShowDirection="false" DefaultShowMultiplicityConstraints="false" DefaultShowOperationOption="\u0001" DefaultShowOperationSignature="true" DefaultShowOrderedMultiplicityConstraint="true" DefaultShowOwnedAssociationEndAsAttribute="true" DefaultShowOwner="false" DefaultShowOwnerSkipModelInFullyQualifiedOwnerSignature="true" DefaultShowReceptionOption="\u0001" DefaultShowTemplateParameter="true" DefaultShowTypeOption="\u0001" DefaultShowUniqueMultiplicityConstraint="true" DefaultTypeOfSubProcess="\u0000" DefaultWrapClassMember="false" DrawTextAnnotationOpenRectangleFollowConnectorEnd="true" EnableMinimumSize="true" EntityColumnConstraintsPresentation="\u0002" ErdIndexNumOfDigits="-1" ErdIndexPattern="{table_name}" ErdIndexPatternSyncAutomatically="true" ErdManyToManyJoinTableDelimiter="_" EtlTableDiagramFontSize="14" ExpandedSubProcessDiagramContent="\u0001" ForeignKeyArrowHeadSize="\u0002" ForeignKeyConnectorEndPointAssociatedColumn="false" ForeignKeyNamePattern="{reference_table_name}{reference_column_name}" ForeignKeyNamePatternCaseHandling="0" ForeignKeyRelationshipPattern="{association_name}" FractionalMetrics="true" GeneralizationSetNotation="\u0001" GraphicAntiAliasing="true" GridDiagramFontSize="14" InteractionDiagramShowDiagramFrame="true" InternalBlockDiagramShowDiagramFrame="true" LineJumpSize="\u0000" ModelElementNameAlignment="\u0004" MultipleLineClassName="\u0001" PackageDiagramShowDiagramFrame="true" PaintConnectorThroughLabel="false" ParametricDiagramShowDiagramFrame="true" PointConnectorEndToCompartmentMember="true" PrimaryKeyConstraintPattern="" PrimaryKeyNamePattern="ID" RenameConstructorAfterRenameClass="\u0000" RenameExtensionPointToFollowExtendUseCase="\u0000" RequirementDiagramShowDiagramFrame="true" ShapeAutoFitSize="false" ShowActivationsInSequenceDiagram="true" ShowActivityStateNodeCaption="524287" ShowArtifactOption="\u0002" ShowAssociatedDiagramNameOfInteraction="false" ShowAssociationRoleStereotypes="true" ShowAttributeGetterSetter="false" ShowBSElementCode="true" ShowClassEmptyCompartments="false" ShowColumnDefaultValue="false" ShowColumnNullable="true" ShowColumnType="true" ShowColumnUniqueConstraintName="false" ShowColumnUserType="false" ShowComponentOption="\u0002" ShowExtraColumnProperties="true" ShowInOutFlowButtonsInDataFlowDiagram="false" ShowInOutFlowsInSubLevelDiagram="true" ShowMessageOperationSignatureForSequenceAndCommunicationDiagram="true" ShowMessageStereotypeInSequenceAndCommunicationDiagram="true" ShowNumberInCollaborationDiagram="true" ShowNumberInSequenceDiagram="true" ShowPackageNameStyle="\u0000" ShowParameterNameInOperationSignature="true" ShowRowGridLineWithinCompClassDiagram="false" ShowRowGridLineWithinCompERD="true" ShowRowGridLineWithinORMDiagram="true" ShowSchemaNameInERD="true" ShowTransitionTrigger="\u0000" ShowUseCaseExtensionPoint="true" ShowUseCaseID="false" SnapConnectorsAfterZoom="false" StateDiagramShowDiagramFrame="true" StateShowParametersOfInternalActivities="false" StateShowPrePostConditionAndBodyOfInternalActivities="true" StopTargetLifelineOnCreateDestroyMessage="\u0002" SupportHtmlTaggedValue="true" SupportMultipleLineAttribute="true" SuppressImpliedMultiplicityForAttributeAssociationEnd="false" SyncAssociationNameWithAssociationClass="\u0000" SyncAssociationRoleNameWithReferencedAttributeName="true" SyncDocOfInterfaceToSubClass="\u0000" TextAntiAliasing="true" TextualAnalysisGenerateRequirementTextOption="\u0001" TextualAnalysisHighlightOption="\u0000" UnnamedIndexPattern="{table_name}_{column_name}" UseCaseDiagramShowDiagramFrame="true" UseStateNameTab="false" WireflowDiagramDevice="0" WireflowDiagramShowActiveFlowLabel="true" WireflowDiagramTheme="0" WireflowDiagramWireflowShowPreview="true" WireflowDiagramWireflowShowScreenId="true">
				<DefaultHtmlDocFont Family="Dialog" Size="12" Style="0"/>
			</DiagramOptions>
			<GeneralOptions ConfirmSubLevelIdWithDot="true" QuickAddGlossaryTermParentModelId="default"/>
			<InstantReverseOptions CalculateGeneralizationAndRealization="false" CreateShapeForParentModelOfDraggedClassPackage="false" ReverseGetterSetter="\u0000" ReverseOperationImplementation="false" ShowPackageForNewDiagram="\u0001" ShowPackageOwner="\u0000"/>
			<ModelQualityOptions EnableModelQualityChecking="false"/>
			<ORMOptions AlterColumnUserType="true" DecimalPrecision="19" DecimalScale="0" ExportCommentToDatabase="true" FormattedSQL="false" GenerateAssociationWithAttribute="false" GenerateDiagramFromORMWizards="true" GetterSetterVisibility="\u0000" IdGeneratorType="native" MappingFileColumnOrder="\u0000" NumericToClassType="\u0000" QuoteSQLIdentifier="\u0000" RecreateShapeWhenSync="false" SyncToClassDiagramAttributeName="\u0001" SyncToClassDiagramAttributeNamePrefix="" SyncToClassDiagramAttributeNameSuffix="" SyncToClassDiagramClassName="\u0000" SyncToClassDiagramClassNamePrefix="" SyncToClassDiagramClassNameSuffix="" SyncToERDColumnName="\u0000" SyncToERDColumnNamePrefix="" SyncToERDColumnNameSuffix="" SyncToERDTableName="\u0004" SyncToERDTableNamePrefix="" SyncToERDTableNameSuffix="" SynchronizeDefaultValueToColumn="false" SynchronizeName="\u0002" TablePerSubclassFKMapping="\u0000" UpperCaseSQL="true" UseDefaultDecimal="true" WrappingServletRequest="\u0001"/>
			<RequirementDiagramOptions DefaultWrapMember="true" ShowAttributes="\u0001" SupportHTMLAttribute="false"/>
			<StateCodeEngineOptions AutoCreateInitialStateInStateDiagram="true" AutoCreateTransitionMethods="true" DefaultInitialStateLocationX="-1" DefaultInitialStateLocationY="-1" GenerateDebugMessage="false" GenerateSample="true" GenerateTryCatch="true" Language="\u0000" RegenerateTransitionMethods="false" SyncTransitionMethods="true"/>
			<WarningOptions CreateORMClassInDefaultPackage="true"/>
			<PORepository>
				<POUserIDFormats>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAmy" LastNumericValue="0" ModelType="BPMNElement" Prefix="BP" Suffix=""/>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAmz" LastNumericValue="11" ModelType="Actor" Prefix="AC" Suffix=""/>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAm0" LastNumericValue="35" ModelType="UseCase" Prefix="UC" Suffix=""/>
					<POUserIDFormat Digits="3" Guid="false" Id="p01BOoWGAqCOCAm1" LastNumericValue="0" ModelType="Requirement" Prefix="REQ" Suffix=""/>
					<POUserIDFormat Digits="3" Guid="false" Id="p01BOoWGAqCOCAm2" LastNumericValue="0" ModelType="BusinessRule" Prefix="BR" Suffix=""/>
					<POUserIDFormat Digits="-1" Guid="false" Id="p01BOoWGAqCOCAm3" LastNumericValue="0" ModelType="BusinessProcessDiagram" Prefix="" Suffix=""/>
				</POUserIDFormats>
			</PORepository>
		</ProjectOptions>
	</ProjectInfo>
	
```

</details>

### `references/real-samples/package_diagram.xml`

<details>
<summary>Mở nội dung tệp</summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Project Author="SinhVien" CommentTableSortAscending="false" CommentTableSortColumn="Date Time" Description="&lt;html&gt;&#13;&#10;  &lt;head&gt;&#13;&#10;    &lt;style type=&quot;text/css&quot;&gt;&#10;      &lt;!--&#10;        body { color: #000000; font-family: Dialog; font-size: 12px }&#10;      --&gt;&#10;    &lt;/style&gt;&#13;&#10;    &#13;&#10;  &lt;/head&gt;&#13;&#10;  &lt;body&gt;&#13;&#10;  &lt;/body&gt;&#13;&#10;&lt;/html&gt;&#13;&#10;" DocumentationType="html" ExportedFromDifferentName="false" ExporterVersion="16.1.1" Name="btl2" TextualAnalysisHighlightOptionCaseSensitive="false" UmlVersion="2.x" Xml_structure="simple">
	<ProjectInfo>
		<OrmInfo DefaultDatabase="1" SupportDatabases="0"/>
		<LogicalView/>
		<ProjectOptions>
			<DiagramOptions ActivityDiagramControlFlowDisplayOption="\u0000" ActivityDiagramShowActionCallBehaviorOption="\u0000" ActivityDiagramShowActivityEdgeWeight="true" ActivityDiagramShowDiagramFrame="true" ActivityDiagramShowObjectNodeType="true" ActivityDiagramShowPartitionHandle="\u0000" AddDataStoresExtEntitiesToDecomposedDFD="\u0002" AlignColumnProperties="true" AllowConfigShowInOutFlowButtonsInDataFlowDiagram="false" AutoGenerateRoleName="false" AutoSetAttributeType="true" AutoSetColumnType="true" AutoSyncRoleName="true" BlockDefinitionDiagramShowDiagramFrame="true" BpPoolLaneDefaultOrientation="\u0000" BpdAutoStretchPools="true" BpdConnectGatewayWithFlowObjectInDifferentPool="\u0000" BpdDefaultConnectionPointStyle="\u0001" BpdDefaultConnectorStyle="\u0005" BpdDhowIdOption="\u0000" BpdShowActivitiesTypeIcon="true" BusinessProcessDiagramDefaultLanguage="English" ClassVisibilityStyle="\u0001" ConnectorLabelOrientation="\u0000" CreateOneMessagePerDirection="true" DecisionMergeNodeConnectionPointStyle="\u0000" DefaultAssociationEndNavigable="\u0001" DefaultAssociationEndVisibility="\u0000" DefaultAssociationShowFromMultiplicity="true" DefaultAssociationShowFromRoleName="true" DefaultAssociationShowFromRoleVisibility="true" DefaultAssociationShowStereotypes="true" DefaultAssociationShowToMultiplicity="true" DefaultAssociationShowToRoleName="true" DefaultAssociationShowToRoleVisibility="true" DefaultAttributeMultiplicity="false" DefaultAttributeType="" DefaultAttributeVisibility="\u0001" DefaultClassAttributeMultiplicity="" DefaultClassAttributeMultiplicityOrdered="false" DefaultClassAttributeMultiplicityUnique="true" DefaultClassInterfaceBall="false" DefaultClassVisibility="\u0004" DefaultColumnType="integer(10)" DefaultConnectionPointStyle="\u0000" DefaultConnectorStyle="\u0001" DefaultDiagramBackground="rgb(255, 255, 255)" DefaultDisplayAsRobustnessAnalysisIcon="true" DefaultDisplayAsRobustnessAnalysisIconInSequenceDiagram="true" DefaultDisplayAsStereotypeIcon="false" DefaultFontColor="rgb(0, 0, 0)" DefaultGenDiagramTypeFromScenario="\u0000" DefaultHtmlDocFontColor="rgb(0, 0, 0)" DefaultLineJumps="\u0000" DefaultOperationVisibility="\u0004" DefaultParameterDirection="\u0002" DefaultShowAttributeInitialValue="true" DefaultShowAttributeOption="\u0001" DefaultShowClassMemberStereotype="true" DefaultShowDirection="false" DefaultShowMultiplicityConstraints="false" DefaultShowOperationOption="\u0001" DefaultShowOperationSignature="true" DefaultShowOrderedMultiplicityConstraint="true" DefaultShowOwnedAssociationEndAsAttribute="true" DefaultShowOwner="false" DefaultShowOwnerSkipModelInFullyQualifiedOwnerSignature="true" DefaultShowReceptionOption="\u0001" DefaultShowTemplateParameter="true" DefaultShowTypeOption="\u0001" DefaultShowUniqueMultiplicityConstraint="true" DefaultTypeOfSubProcess="\u0000" DefaultWrapClassMember="false" DrawTextAnnotationOpenRectangleFollowConnectorEnd="true" EnableMinimumSize="true" EntityColumnConstraintsPresentation="\u0002" ErdIndexNumOfDigits="-1" ErdIndexPattern="{table_name}" ErdIndexPatternSyncAutomatically="true" ErdManyToManyJoinTableDelimiter="_" EtlTableDiagramFontSize="14" ExpandedSubProcessDiagramContent="\u0001" ForeignKeyArrowHeadSize="\u0002" ForeignKeyConnectorEndPointAssociatedColumn="false" ForeignKeyNamePattern="{reference_table_name}{reference_column_name}" ForeignKeyNamePatternCaseHandling="0" ForeignKeyRelationshipPattern="{association_name}" FractionalMetrics="true" GeneralizationSetNotation="\u0001" GraphicAntiAliasing="true" GridDiagramFontSize="14" InteractionDiagramShowDiagramFrame="true" InternalBlockDiagramShowDiagramFrame="true" LineJumpSize="\u0000" ModelElementNameAlignment="\u0004" MultipleLineClassName="\u0001" PackageDiagramShowDiagramFrame="true" PaintConnectorThroughLabel="false" ParametricDiagramShowDiagramFrame="true" PointConnectorEndToCompartmentMember="true" PrimaryKeyConstraintPattern="" PrimaryKeyNamePattern="ID" RenameConstructorAfterRenameClass="\u0000" RenameExtensionPointToFollowExtendUseCase="\u0000" RequirementDiagramShowDiagramFrame="true" ShapeAutoFitSize="false" ShowActivationsInSequenceDiagram="true" ShowActivityStateNodeCaption="524287" ShowArtifactOption="\u0002" ShowAssociatedDiagramNameOfInteraction="false" ShowAssociationRoleStereotypes="true" ShowAttributeGetterSetter="false" ShowBSElementCode="true" ShowClassEmptyCompartments="false" ShowColumnDefaultValue="false" ShowColumnNullable="true" ShowColumnType="true" ShowColumnUniqueConstraintName="false" ShowColumnUserType="false" ShowComponentOption="\u0002" ShowExtraColumnProperties="true" ShowInOutFlowButtonsInDataFlowDiagram="false" ShowInOutFlowsInSubLevelDiagram="true" ShowMessageOperationSignatureForSequenceAndCommunicationDiagram="true" ShowMessageStereotypeInSequenceAndCommunicationDiagram="true" ShowNumberInCollaborationDiagram="true" ShowNumberInSequenceDiagram="true" ShowPackageNameStyle="\u0000" ShowParameterNameInOperationSignature="true" ShowRowGridLineWithinCompClassDiagram="false" ShowRowGridLineWithinCompERD="true" ShowRowGridLineWithinORMDiagram="true" ShowSchemaNameInERD="true" ShowTransitionTrigger="\u0000" ShowUseCaseExtensionPoint="true" ShowUseCaseID="false" SnapConnectorsAfterZoom="false" StateDiagramShowDiagramFrame="true" StateShowParametersOfInternalActivities="false" StateShowPrePostConditionAndBodyOfInternalActivities="true" StopTargetLifelineOnCreateDestroyMessage="\u0002" SupportHtmlTaggedValue="true" SupportMultipleLineAttribute="true" SuppressImpliedMultiplicityForAttributeAssociationEnd="false" SyncAssociationNameWithAssociationClass="\u0000" SyncAssociationRoleNameWithReferencedAttributeName="true" SyncDocOfInterfaceToSubClass="\u0000" TextAntiAliasing="true" TextualAnalysisGenerateRequirementTextOption="\u0001" TextualAnalysisHighlightOption="\u0000" UnnamedIndexPattern="{table_name}_{column_name}" UseCaseDiagramShowDiagramFrame="true" UseStateNameTab="false" WireflowDiagramDevice="0" WireflowDiagramShowActiveFlowLabel="true" WireflowDiagramTheme="0" WireflowDiagramWireflowShowPreview="true" WireflowDiagramWireflowShowScreenId="true">
				<DefaultHtmlDocFont Family="Dialog" Size="12" Style="0"/>
			</DiagramOptions>
			<GeneralOptions ConfirmSubLevelIdWithDot="true" QuickAddGlossaryTermParentModelId="default"/>
			<InstantReverseOptions CalculateGeneralizationAndRealization="false" CreateShapeForParentModelOfDraggedClassPackage="false" ReverseGetterSetter="\u0000" ReverseOperationImplementation="false" ShowPackageForNewDiagram="\u0001" ShowPackageOwner="\u0000"/>
			<ModelQualityOptions EnableModelQualityChecking="false"/>
			<ORMOptions AlterColumnUserType="true" DecimalPrecision="19" DecimalScale="0" ExportCommentToDatabase="true" FormattedSQL="false" GenerateAssociationWithAttribute="false" GenerateDiagramFromORMWizards="true" GetterSetterVisibility="\u0000" IdGeneratorType="native" MappingFileColumnOrder="\u0000" NumericToClassType="\u0000" QuoteSQLIdentifier="\u0000" RecreateShapeWhenSync="false" SyncToClassDiagramAttributeName="\u0001" SyncToClassDiagramAttributeNamePrefix="" SyncToClassDiagramAttributeNameSuffix="" SyncToClassDiagramClassName="\u0000" SyncToClassDiagramClassNamePrefix="" SyncToClassDiagramClassNameSuffix="" SyncToERDColumnName="\u0000" SyncToERDColumnNamePrefix="" SyncToERDColumnNameSuffix="" SyncToERDTableName="\u0004" SyncToERDTableNamePrefix="" SyncToERDTableNameSuffix="" SynchronizeDefaultValueToColumn="false" SynchronizeName="\u0002" TablePerSubclassFKMapping="\u0000" UpperCaseSQL="true" UseDefaultDecimal="true" WrappingServletRequest="\u0001"/>
			<RequirementDiagramOptions DefaultWrapMember="true" ShowAttributes="\u0001" SupportHTMLAttribute="false"/>
			<StateCodeEngineOptions AutoCreateInitialStateInStateDiagram="true" AutoCreateTransitionMethods="true" DefaultInitialStateLocationX="-1" DefaultInitialStateLocationY="-1" GenerateDebugMessage="false" GenerateSample="true" GenerateTryCatch="true" Language="\u0000" RegenerateTransitionMethods="false" SyncTransitionMethods="true"/>
			<WarningOptions CreateORMClassInDefaultPackage="true"/>
			<PORepository>
				<POUserIDFormats>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAmy" LastNumericValue="0" ModelType="BPMNElement" Prefix="BP" Suffix=""/>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAmz" LastNumericValue="11" ModelType="Actor" Prefix="AC" Suffix=""/>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAm0" LastNumericValue="35" ModelType="UseCase" Prefix="UC" Suffix=""/>
					<POUserIDFormat Digits="3" Guid="false" Id="p01BOoWGAqCOCAm1" LastNumericValue="0" ModelType="Requirement" Prefix="REQ" Suffix=""/>
					<POUserIDFormat Digits="3" Guid="false" Id="p01BOoWGAqCOCAm2" LastNumericValue="0" ModelType="BusinessRule" Prefix="BR" Suffix=""/>
					<POUserIDFormat Digits="-1" Guid="false" Id="p01BOoWGAqCOCAm3" LastNumericValue="0" ModelType="BusinessProcessDiagram" Prefix="" Suffix=""/>
				</POUserIDFormats>
			</PORepository>
		</ProjectOptions>
	</ProjectInfo>
	<Models>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="9PVBOoWGAqCOCAXu" Name="boolean" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.441" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="HPVBOoWGAqCOCAXv" Name="byte" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.443" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXw" Name="char" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.443" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXx" Name="double" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.444" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXy" Name="float" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.444" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXz" Name="int" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.445" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX0" Name="long" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.445" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX1" Name="short" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.446" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX2" Name="void" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.446" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX3" Name="string" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.446" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<ModelRelationshipContainer BacklogActivityId="0" Documentation_plain="" Id="DoBBLFK3EBJFH71i" Name="relationships" PmAuthor="SinhVien" PmCreateDateTime="2026-10-14T10:00:00.000" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
			<ModelChildren>
				<ModelRelationshipContainer BacklogActivityId="0" Documentation_plain="" Id="y2uRk4WFYCyCBxBn" Name="Dependency" PmAuthor="phanb" PmCreateDateTime="2026-11-11T14:36:56.275" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
					<ModelChildren>
						<Dependency BacklogActivityId="0" Documentation_plain="" From="yauRk4WFYCyCBxAz" Id="pauRk4WFYCyCBxA7" PmAuthor="" PmCreateDateTime="2017-06-22T10:55:22.623" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" To="yauRk4WFYCyCBxAw" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Dependency Idref="x6uRk4WFYCyCBxBX"/>
							</MasterView>
						</Dependency>
						<Dependency BacklogActivityId="0" Documentation_plain="" From="yauRk4WFYCyCBxAw" Id="zauRk4WFYCyCBxA8" PmAuthor="" PmCreateDateTime="2017-06-22T10:56:06.155" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" To="yauRk4WFYCyCBxAx" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Dependency Idref="x6uRk4WFYCyCBxBZ"/>
							</MasterView>
						</Dependency>
						<Dependency BacklogActivityId="0" Documentation_plain="" From="yauRk4WFYCyCBxAw" Id="zauRk4WFYCyCBxA9" PmAuthor="" PmCreateDateTime="2017-06-22T10:56:33.977" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" To="yauRk4WFYCyCBxAy" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Dependency Idref="16uRk4WFYCyCBxBb"/>
							</MasterView>
						</Dependency>
						<Dependency BacklogActivityId="0" Documentation_plain="" From="yauRk4WFYCyCBxA0" Id="zauRk4WFYCyCBxA." PmAuthor="" PmCreateDateTime="2017-06-22T10:56:48.984" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" To="yauRk4WFYCyCBxAy" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Dependency Idref="16uRk4WFYCyCBxBd"/>
							</MasterView>
						</Dependency>
						<Dependency BacklogActivityId="0" Documentation_plain="" From="yauRk4WFYCyCBxAw" Id="HauRk4WFYCyCBxA_" PmAuthor="" PmCreateDateTime="2017-06-22T10:58:13.722" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" To="xauRk4WFYCyCBxA2" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Dependency Idref="16uRk4WFYCyCBxBf"/>
							</MasterView>
						</Dependency>
						<Dependency BacklogActivityId="0" Documentation_plain="" From="xauRk4WFYCyCBxA2" Id="XauRk4WFYCyCBxBA" PmAuthor="" PmCreateDateTime="2017-06-22T10:58:15.102" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" To="yauRk4WFYCyCBxAw" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Dependency Idref="16uRk4WFYCyCBxBh"/>
							</MasterView>
						</Dependency>
						<Dependency BacklogActivityId="0" Documentation_plain="" From="yauRk4WFYCyCBxAx" Id="XauRk4WFYCyCBxBB" PmAuthor="" PmCreateDateTime="2017-06-22T10:58:16.783" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" To="xauRk4WFYCyCBxA3" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Dependency Idref="16uRk4WFYCyCBxBj"/>
							</MasterView>
						</Dependency>
						<Dependency BacklogActivityId="0" Documentation_plain="" From="xauRk4WFYCyCBxA3" Id="XauRk4WFYCyCBxBC" PmAuthor="" PmCreateDateTime="2017-06-22T10:58:17.878" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" To="yauRk4WFYCyCBxAx" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Dependency Idref="16uRk4WFYCyCBxBl"/>
							</MasterView>
						</Dependency>
					</ModelChildren>
				</ModelRelationshipContainer>
			</ModelChildren>
		</ModelRelationshipContainer>
		<Model Abstract="false" BacklogActivityId="0" ConnectToCodeModel="1" Documentation_plain="" Id="nquRk4WFYCyCBxAt" Leaf="false" Name="Package Diagram - General Business System" PmAuthor="" PmCreateDateTime="2017-06-22T10:53:44.705" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true">
			<SubDiagrams>
				<PackageDiagram Idref="XauRk4WFYCyCBxBD"/>
			</SubDiagrams>
			<ModelChildren>
				<Package Abstract="false" BacklogActivityId="0" ConnectToCodeModel="1" DefaultDiagramId_IsNull="true" Documentation_plain="" Id="yauRk4WFYCyCBxAv" Leaf="false" Name="com.aBusiness" PmAuthor="" PmCreateDateTime="2017-06-22T10:55:00.834" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
					<MasterView>
						<Package Idref="y6uRk4WFYCyCBxBP" Name="com.aBusiness"/>
					</MasterView>
					<ModelChildren>
						<Package Abstract="false" BacklogActivityId="0" ConnectToCodeModel="1" DefaultDiagramId_IsNull="true" Documentation_plain="" Id="yauRk4WFYCyCBxAw" Leaf="false" Name="Ordering" PmAuthor="" PmCreateDateTime="2017-06-22T10:55:22.601" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
							<FromSimpleRelationships>
								<Dependency Idref="zauRk4WFYCyCBxA8" Name=""/>
								<Dependency Idref="zauRk4WFYCyCBxA9" Name=""/>
								<Dependency Idref="HauRk4WFYCyCBxA_" Name=""/>
							</FromSimpleRelationships>
							<ToSimpleRelationships>
								<Dependency Idref="pauRk4WFYCyCBxA7" Name=""/>
								<Dependency Idref="XauRk4WFYCyCBxBA" Name=""/>
							</ToSimpleRelationships>
							<MasterView>
								<Package Idref="x6uRk4WFYCyCBxBV" Name="Ordering"/>
							</MasterView>
						</Package>
						<Package Abstract="false" BacklogActivityId="0" ConnectToCodeModel="1" DefaultDiagramId_IsNull="true" Documentation_plain="" Id="yauRk4WFYCyCBxAx" Leaf="false" Name="Shipping" PmAuthor="" PmCreateDateTime="2017-06-22T10:56:06.132" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
							<FromSimpleRelationships>
								<Dependency Idref="XauRk4WFYCyCBxBB" Name=""/>
							</FromSimpleRelationships>
							<ToSimpleRelationships>
								<Dependency Idref="zauRk4WFYCyCBxA8" Name=""/>
								<Dependency Idref="XauRk4WFYCyCBxBC" Name=""/>
							</ToSimpleRelationships>
							<MasterView>
								<Package Idref="y6uRk4WFYCyCBxBT" Name="Shipping"/>
							</MasterView>
						</Package>
						<Package Abstract="false" BacklogActivityId="0" ConnectToCodeModel="1" DefaultDiagramId_IsNull="true" Documentation_plain="" Id="yauRk4WFYCyCBxAy" Leaf="false" Name="Accounting" PmAuthor="" PmCreateDateTime="2017-06-22T10:56:19.519" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
							<ToSimpleRelationships>
								<Dependency Idref="zauRk4WFYCyCBxA9" Name=""/>
								<Dependency Idref="zauRk4WFYCyCBxA." Name=""/>
							</ToSimpleRelationships>
							<MasterView>
								<Package Idref="y6uRk4WFYCyCBxBR" Name="Accounting"/>
							</MasterView>
						</Package>
					</ModelChildren>
				</Package>
				<Package Abstract="false" BacklogActivityId="0" ConnectToCodeModel="1" DefaultDiagramId_IsNull="true" Documentation_plain="" Id="yauRk4WFYCyCBxAz" Leaf="false" Name="UI" PmAuthor="" PmCreateDateTime="2017-06-22T10:55:11.134" PmLastModified="2026-11-11T14:36:56.275" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
					<FromSimpleRelationships>
						<Dependency Idref="pauRk4WFYCyCBxA7" Name=""/>
					</FromSimpleRelationships>
					<MasterView>
						<Package Idref="y6uRk4WFYCyCBxBN" Name="UI"/>
					</MasterView>
				</Package>
				<Package Abstract="false" BacklogActivityId="0" ConnectToCodeModel="1" DefaultDiagramId_IsNull="true" Documentation_plain="" Id="yauRk4WFYCyCBxA0" Leaf="false" Name="Bank" PmAuthor="" PmCreateDateTime="2017-06-22T10:56:43.967" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
					<FromSimpleRelationships>
						<Dependency Idref="zauRk4WFYCyCBxA." Name=""/>
					</FromSimpleRelationships>
					<MasterView>
						<Package Idref="y6uRk4WFYCyCBxBL" Name="Bank"/>
					</MasterView>
				</Package>
				<Package Abstract="false" BacklogActivityId="0" ConnectToCodeModel="1" DefaultDiagramId_IsNull="true" Documentation_plain="" Id="yauRk4WFYCyCBxA1" Leaf="false" Name="DataManagement" PmAuthor="" PmCreateDateTime="2017-06-22T10:57:03.475" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
					<MasterView>
						<Package Idref="k6uRk4WFYCyCBxBF" Name="DataManagement"/>
					</MasterView>
					<ModelChildren>
						<Package Abstract="false" BacklogActivityId="0" ConnectToCodeModel="1" DefaultDiagramId_IsNull="true" Documentation_plain="" Id="xauRk4WFYCyCBxA2" Leaf="false" Name="CustomerDB" PmAuthor="" PmCreateDateTime="2017-06-22T10:57:03.490" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
							<FromSimpleRelationships>
								<Dependency Idref="XauRk4WFYCyCBxBA" Name=""/>
							</FromSimpleRelationships>
							<ToSimpleRelationships>
								<Dependency Idref="HauRk4WFYCyCBxA_" Name=""/>
							</ToSimpleRelationships>
							<MasterView>
								<Package Idref="y6uRk4WFYCyCBxBJ" Name="CustomerDB"/>
							</MasterView>
						</Package>
						<Package Abstract="false" BacklogActivityId="0" ConnectToCodeModel="1" DefaultDiagramId_IsNull="true" Documentation_plain="" Id="xauRk4WFYCyCBxA3" Leaf="false" Name="StockDB" PmAuthor="" PmCreateDateTime="2017-06-22T10:57:03.502" PmLastModified="2026-11-11T14:36:56.289" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
							<FromSimpleRelationships>
								<Dependency Idref="XauRk4WFYCyCBxBC" Name=""/>
							</FromSimpleRelationships>
							<ToSimpleRelationships>
								<Dependency Idref="XauRk4WFYCyCBxBB" Name=""/>
							</ToSimpleRelationships>
							<MasterView>
								<Package Idref="y6uRk4WFYCyCBxBH" Name="StockDB"/>
							</MasterView>
						</Package>
					</ModelChildren>
				</Package>
			</ModelChildren>
		</Model>
	</Models>
	<Diagrams>
		<PackageDiagram AlignToGrid="false" AutoFitShapesSize="false" ConnectionPointStyle="0" ConnectorLabelOrientation="0" ConnectorLineJumps="0" ConnectorLineJumpsSize="0" ConnectorModelElementNameAlignment="4" ConnectorStyle="1" DiagramBackground="rgb(255, 255, 255)" Editable="true" FilterByViewpointLegend="true" FollowDiagramParentElement="true" GridColor="rgb(192, 192, 192)" GridHeight="10" GridVisible="false" GridWidth="10" Height="598" HideConnectorIfFromToIsHidden="0" HideEmptyTaggedValues="false" Id="XauRk4WFYCyCBxBD" ImageHeight="0" ImageScale="1.0" ImageWidth="0" InitializeDiagramForCreate="true" Maximized="true" ModelElementNameAlignment="4" Name="General Business System" PaintConnectorThroughLabel="1" ParentModel="nquRk4WFYCyCBxAt" PmAuthor="" PmCreateDateTime="2017-06-22T10:53:59.666" PmLastModified="2017-06-22T15:44:54.600" PointConnectorEndToCompartmentMember="true" QualityScore="-1" RequestFitSizeWithPromptUser="false" RequestValidateSnapToGrid="false" ShapePresentationOption="0" ShowActivityStateNodeCaption="65535" ShowAllocatedFrom="true" ShowAllocatedTo="true" ShowColorLegend="false" ShowConnectorLegend="false" ShowConnectorName="0" ShowConstraints="false" ShowDefaultPackage="true" ShowDiagramFrame="true" ShowInformationItemOption="2" ShowPMAuthor="false" ShowPMDifficulty="false" ShowPMDiscipline="false" ShowPMIteration="false" ShowPMPhase="false" ShowPMPriority="false" ShowPMStatus="false" ShowPMVersion="false" ShowPackageNameStyle="0" ShowRelationshipConstraintExpression="false" ShowShapeLegend="false" ShowShapeStereotypeIconName="true" ShowStereotypes="true" ShowTaggedValues="false" TeamworkAuthor="Jick Yeung" TeamworkCreateDateTime="1498117490291" TrimmedHeight="0" TrimmedWidth="0" Width="1255" X="0" Y="0" ZoomRatio="1.0" _globalPaletteOption="true" documentation="&lt;html&gt;&#13;&#10;  &lt;head&gt;&#13;&#10;    &lt;style type=&quot;text/css&quot;&gt;&#10;      &lt;!--&#10;        body { color: #000000; font-family: Dialog; font-size: 12px }&#10;      --&gt;&#10;    &lt;/style&gt;&#13;&#10;    &#13;&#10;  &lt;/head&gt;&#13;&#10;  &lt;body&gt;&#13;&#10;    &lt;p&gt;&#13;&#10;      &#13;&#10;    &lt;/p&gt;&#13;&#10;  &lt;/body&gt;&#13;&#10;&lt;/html&gt;&#13;&#10;">
			<Shapes>
				<Package Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="161" Id="k6uRk4WFYCyCBxBF" MetaModelElement="yauRk4WFYCyCBxA1" Model="yauRk4WFYCyCBxA1" ModelElementNameAlignment="1" Name="DataManagement" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowOwnerOption="3" ShowPackageNameStyle="2" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="301" X="219" Y="283" ZOrder="6">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="141" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="301" X="0" Y="20"/>
					<DiagramElementChildren>
						<Package Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="71" Id="y6uRk4WFYCyCBxBH" MetaModelElement="xauRk4WFYCyCBxA3" Model="xauRk4WFYCyCBxA3" ModelElementNameAlignment="1" Name="StockDB" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowOwnerOption="3" ShowPackageNameStyle="2" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="92" X="402" Y="344" ZOrder="2">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
								<Stroke/>
							</Line>
							<Caption Height="51" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="92" X="0" Y="20"/>
							<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
						</Package>
						<Package Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="71" Id="y6uRk4WFYCyCBxBJ" MetaModelElement="xauRk4WFYCyCBxA2" Model="xauRk4WFYCyCBxA2" ModelElementNameAlignment="1" Name="CustomerDB" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowOwnerOption="3" ShowPackageNameStyle="2" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="92" X="245" Y="344" ZOrder="4">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
								<Stroke/>
							</Line>
							<Caption Height="51" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="92" X="0" Y="20"/>
							<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
						</Package>
					</DiagramElementChildren>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
				</Package>
				<Package Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="71" Id="y6uRk4WFYCyCBxBL" MetaModelElement="yauRk4WFYCyCBxA0" Model="yauRk4WFYCyCBxA0" ModelElementNameAlignment="1" Name="Bank" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowOwnerOption="3" ShowPackageNameStyle="2" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="92" X="75" Y="68" ZOrder="8">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="51" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="92" X="0" Y="20"/>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
				</Package>
				<Package Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" CreatorDiagramType="PackageDiagram" Foreground="rgb(0, 0, 0)" Height="71" Id="y6uRk4WFYCyCBxBN" MetaModelElement="yauRk4WFYCyCBxAz" Model="yauRk4WFYCyCBxAz" ModelElementNameAlignment="1" Name="UI" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowOwnerOption="3" ShowPackageNameStyle="2" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="92" X="75" Y="166" ZOrder="16">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="51" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="92" X="0" Y="20"/>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
				</Package>
				<Package Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" CreatorDiagramType="PackageDiagram" Foreground="rgb(0, 0, 0)" Height="240" Id="y6uRk4WFYCyCBxBP" MetaModelElement="yauRk4WFYCyCBxAv" Model="yauRk4WFYCyCBxAv" ModelElementNameAlignment="1" Name="com.aBusiness" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowOwnerOption="3" ShowPackageNameStyle="2" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="301" X="219" Y="25" ZOrder="18">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="220" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="301" X="0" Y="20"/>
					<DiagramElementChildren>
						<Package Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="71" Id="y6uRk4WFYCyCBxBR" MetaModelElement="yauRk4WFYCyCBxAy" Model="yauRk4WFYCyCBxAy" ModelElementNameAlignment="1" Name="Accounting" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowOwnerOption="3" ShowPackageNameStyle="2" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="92" X="245" Y="68" ZOrder="10">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
								<Stroke/>
							</Line>
							<Caption Height="51" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="92" X="0" Y="20"/>
							<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
						</Package>
						<Package Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" CreatorDiagramType="PackageDiagram" Foreground="rgb(0, 0, 0)" Height="71" Id="y6uRk4WFYCyCBxBT" MetaModelElement="yauRk4WFYCyCBxAx" Model="yauRk4WFYCyCBxAx" ModelElementNameAlignment="1" Name="Shipping" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowOwnerOption="3" ShowPackageNameStyle="2" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="92" X="403" Y="166" ZOrder="12">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
								<Stroke/>
							</Line>
							<Caption Height="51" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="92" X="0" Y="20"/>
							<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
						</Package>
						<Package Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" CreatorDiagramType="PackageDiagram" Foreground="rgb(0, 0, 0)" Height="71" Id="x6uRk4WFYCyCBxBV" MetaModelElement="yauRk4WFYCyCBxAw" Model="yauRk4WFYCyCBxAw" ModelElementNameAlignment="1" Name="Ordering" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowOwnerOption="3" ShowPackageNameStyle="2" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="92" X="246" Y="166" ZOrder="14">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
								<Stroke/>
							</Line>
							<Caption Height="51" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="92" X="0" Y="20"/>
							<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
						</Package>
					</DiagramElementChildren>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
				</Package>
			</Shapes>
			<Connectors>
				<Dependency Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="PackageDiagram" Foreground="rgb(0, 0, 0)" From="y6uRk4WFYCyCBxBN" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="200" Id="x6uRk4WFYCyCBxBX" MetaModelElement="pauRk4WFYCyCBxA7" Model="pauRk4WFYCyCBxA7" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="x6uRk4WFYCyCBxBV" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="277" X="68" Y="112" ZOrder="20">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="194" Y="212"/>
					<Points>
						<Point X="168.0" Y="212.0"/>
						<Point X="245.0" Y="212.0"/>
					</Points>
				</Dependency>
				<Dependency Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="PackageDiagram" Foreground="rgb(0, 0, 0)" From="x6uRk4WFYCyCBxBV" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="200" Id="x6uRk4WFYCyCBxBZ" MetaModelElement="zauRk4WFYCyCBxA8" Model="zauRk4WFYCyCBxA8" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="y6uRk4WFYCyCBxBT" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="263" X="239" Y="112" ZOrder="22">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="360" Y="212"/>
					<Points>
						<Point X="339.0" Y="212.0"/>
						<Point X="402.0" Y="212.0"/>
					</Points>
				</Dependency>
				<Dependency Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="PackageDiagram" Foreground="rgb(0, 0, 0)" From="x6uRk4WFYCyCBxBV" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="225" Id="16uRk4WFYCyCBxBb" MetaModelElement="zauRk4WFYCyCBxA9" Model="zauRk4WFYCyCBxA9" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="y6uRk4WFYCyCBxBR" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="200" X="192" Y="40" ZOrder="24">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="282" Y="152"/>
					<Points>
						<Point X="292.0" Y="165.0"/>
						<Point X="292.0" Y="140.0"/>
					</Points>
				</Dependency>
				<Dependency Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="PackageDiagram" Foreground="rgb(0, 0, 0)" From="y6uRk4WFYCyCBxBL" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="200" Id="16uRk4WFYCyCBxBd" MetaModelElement="zauRk4WFYCyCBxA." Model="zauRk4WFYCyCBxA." ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="y6uRk4WFYCyCBxBR" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="276" X="68" Y="13" ZOrder="26">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="0" Y="0"/>
					<Points>
						<Point X="168.0" Y="113.0"/>
						<Point X="244.0" Y="113.0"/>
					</Points>
				</Dependency>
				<Dependency Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="PackageDiagram" Foreground="rgb(0, 0, 0)" From="x6uRk4WFYCyCBxBV" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="305" Id="16uRk4WFYCyCBxBf" MetaModelElement="HauRk4WFYCyCBxA_" Model="HauRk4WFYCyCBxA_" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="y6uRk4WFYCyCBxBJ" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="200" X="192" Y="138" ZOrder="28">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="292" Y="290"/>
					<Points>
						<Point X="292.0" Y="238.0"/>
						<Point X="292.0" Y="343.0"/>
					</Points>
				</Dependency>
				<Dependency Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="PackageDiagram" Foreground="rgb(0, 0, 0)" From="y6uRk4WFYCyCBxBJ" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="305" Id="16uRk4WFYCyCBxBh" MetaModelElement="XauRk4WFYCyCBxBA" Model="XauRk4WFYCyCBxBA" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="x6uRk4WFYCyCBxBV" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="200" X="210" Y="138" ZOrder="30">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="310" Y="290"/>
					<Points>
						<Point X="310.0" Y="343.0"/>
						<Point X="310.0" Y="238.0"/>
					</Points>
				</Dependency>
				<Dependency Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="PackageDiagram" Foreground="rgb(0, 0, 0)" From="y6uRk4WFYCyCBxBT" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="305" Id="16uRk4WFYCyCBxBj" MetaModelElement="XauRk4WFYCyCBxBB" Model="XauRk4WFYCyCBxBB" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="y6uRk4WFYCyCBxBH" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="200" X="348" Y="138" ZOrder="32">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="448" Y="290"/>
					<Points>
						<Point X="448.0" Y="238.0"/>
						<Point X="448.0" Y="343.0"/>
					</Points>
				</Dependency>
				<Dependency Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="PackageDiagram" Foreground="rgb(0, 0, 0)" From="y6uRk4WFYCyCBxBH" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="305" Id="16uRk4WFYCyCBxBl" MetaModelElement="XauRk4WFYCyCBxBC" Model="XauRk4WFYCyCBxBC" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="y6uRk4WFYCyCBxBT" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="200" X="366" Y="138" ZOrder="34">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="468" Y="290"/>
					<Points>
						<Point X="466.0" Y="343.0"/>
						<Point X="466.0" Y="238.0"/>
					</Points>
				</Dependency>
			</Connectors>
		</PackageDiagram>
	</Diagrams>
</Project>
```

</details>

### `references/real-samples/er_diagram.xml`

<details>
<summary>Mở nội dung tệp</summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Project Author="SinhVien" CommentTableSortAscending="false" CommentTableSortColumn="Date Time" Description="&lt;html&gt;&#13;&#10;  &lt;head&gt;&#13;&#10;    &lt;style type=&quot;text/css&quot;&gt;&#10;      &lt;!--&#10;        body { color: #000000; font-family: Dialog; font-size: 12px }&#10;      --&gt;&#10;    &lt;/style&gt;&#13;&#10;    &#13;&#10;  &lt;/head&gt;&#13;&#10;  &lt;body&gt;&#13;&#10;  &lt;/body&gt;&#13;&#10;&lt;/html&gt;&#13;&#10;" DocumentationType="html" ExportedFromDifferentName="false" ExporterVersion="16.1.1" Name="btl2" TextualAnalysisHighlightOptionCaseSensitive="false" UmlVersion="2.x" Xml_structure="simple">
	<ProjectInfo>
		<OrmInfo DefaultDatabase="1" SupportDatabases="0"/>
		<LogicalView/>
		<ProjectOptions>
			<DiagramOptions ActivityDiagramControlFlowDisplayOption="\u0000" ActivityDiagramShowActionCallBehaviorOption="\u0000" ActivityDiagramShowActivityEdgeWeight="true" ActivityDiagramShowDiagramFrame="true" ActivityDiagramShowObjectNodeType="true" ActivityDiagramShowPartitionHandle="\u0000" AddDataStoresExtEntitiesToDecomposedDFD="\u0002" AlignColumnProperties="true" AllowConfigShowInOutFlowButtonsInDataFlowDiagram="false" AutoGenerateRoleName="false" AutoSetAttributeType="true" AutoSetColumnType="true" AutoSyncRoleName="true" BlockDefinitionDiagramShowDiagramFrame="true" BpPoolLaneDefaultOrientation="\u0000" BpdAutoStretchPools="true" BpdConnectGatewayWithFlowObjectInDifferentPool="\u0000" BpdDefaultConnectionPointStyle="\u0001" BpdDefaultConnectorStyle="\u0005" BpdDhowIdOption="\u0000" BpdShowActivitiesTypeIcon="true" BusinessProcessDiagramDefaultLanguage="English" ClassVisibilityStyle="\u0001" ConnectorLabelOrientation="\u0000" CreateOneMessagePerDirection="true" DecisionMergeNodeConnectionPointStyle="\u0000" DefaultAssociationEndNavigable="\u0001" DefaultAssociationEndVisibility="\u0000" DefaultAssociationShowFromMultiplicity="true" DefaultAssociationShowFromRoleName="true" DefaultAssociationShowFromRoleVisibility="true" DefaultAssociationShowStereotypes="true" DefaultAssociationShowToMultiplicity="true" DefaultAssociationShowToRoleName="true" DefaultAssociationShowToRoleVisibility="true" DefaultAttributeMultiplicity="false" DefaultAttributeType="" DefaultAttributeVisibility="\u0001" DefaultClassAttributeMultiplicity="" DefaultClassAttributeMultiplicityOrdered="false" DefaultClassAttributeMultiplicityUnique="true" DefaultClassInterfaceBall="false" DefaultClassVisibility="\u0004" DefaultColumnType="integer(10)" DefaultConnectionPointStyle="\u0000" DefaultConnectorStyle="\u0001" DefaultDiagramBackground="rgb(255, 255, 255)" DefaultDisplayAsRobustnessAnalysisIcon="true" DefaultDisplayAsRobustnessAnalysisIconInSequenceDiagram="true" DefaultDisplayAsStereotypeIcon="false" DefaultFontColor="rgb(0, 0, 0)" DefaultGenDiagramTypeFromScenario="\u0000" DefaultHtmlDocFontColor="rgb(0, 0, 0)" DefaultLineJumps="\u0000" DefaultOperationVisibility="\u0004" DefaultParameterDirection="\u0002" DefaultShowAttributeInitialValue="true" DefaultShowAttributeOption="\u0001" DefaultShowClassMemberStereotype="true" DefaultShowDirection="false" DefaultShowMultiplicityConstraints="false" DefaultShowOperationOption="\u0001" DefaultShowOperationSignature="true" DefaultShowOrderedMultiplicityConstraint="true" DefaultShowOwnedAssociationEndAsAttribute="true" DefaultShowOwner="false" DefaultShowOwnerSkipModelInFullyQualifiedOwnerSignature="true" DefaultShowReceptionOption="\u0001" DefaultShowTemplateParameter="true" DefaultShowTypeOption="\u0001" DefaultShowUniqueMultiplicityConstraint="true" DefaultTypeOfSubProcess="\u0000" DefaultWrapClassMember="false" DrawTextAnnotationOpenRectangleFollowConnectorEnd="true" EnableMinimumSize="true" EntityColumnConstraintsPresentation="\u0002" ErdIndexNumOfDigits="-1" ErdIndexPattern="{table_name}" ErdIndexPatternSyncAutomatically="true" ErdManyToManyJoinTableDelimiter="_" EtlTableDiagramFontSize="14" ExpandedSubProcessDiagramContent="\u0001" ForeignKeyArrowHeadSize="\u0002" ForeignKeyConnectorEndPointAssociatedColumn="false" ForeignKeyNamePattern="{reference_table_name}{reference_column_name}" ForeignKeyNamePatternCaseHandling="0" ForeignKeyRelationshipPattern="{association_name}" FractionalMetrics="true" GeneralizationSetNotation="\u0001" GraphicAntiAliasing="true" GridDiagramFontSize="14" InteractionDiagramShowDiagramFrame="true" InternalBlockDiagramShowDiagramFrame="true" LineJumpSize="\u0000" ModelElementNameAlignment="\u0004" MultipleLineClassName="\u0001" PackageDiagramShowDiagramFrame="true" PaintConnectorThroughLabel="false" ParametricDiagramShowDiagramFrame="true" PointConnectorEndToCompartmentMember="true" PrimaryKeyConstraintPattern="" PrimaryKeyNamePattern="ID" RenameConstructorAfterRenameClass="\u0000" RenameExtensionPointToFollowExtendUseCase="\u0000" RequirementDiagramShowDiagramFrame="true" ShapeAutoFitSize="false" ShowActivationsInSequenceDiagram="true" ShowActivityStateNodeCaption="524287" ShowArtifactOption="\u0002" ShowAssociatedDiagramNameOfInteraction="false" ShowAssociationRoleStereotypes="true" ShowAttributeGetterSetter="false" ShowBSElementCode="true" ShowClassEmptyCompartments="false" ShowColumnDefaultValue="false" ShowColumnNullable="true" ShowColumnType="true" ShowColumnUniqueConstraintName="false" ShowColumnUserType="false" ShowComponentOption="\u0002" ShowExtraColumnProperties="true" ShowInOutFlowButtonsInDataFlowDiagram="false" ShowInOutFlowsInSubLevelDiagram="true" ShowMessageOperationSignatureForSequenceAndCommunicationDiagram="true" ShowMessageStereotypeInSequenceAndCommunicationDiagram="true" ShowNumberInCollaborationDiagram="true" ShowNumberInSequenceDiagram="true" ShowPackageNameStyle="\u0000" ShowParameterNameInOperationSignature="true" ShowRowGridLineWithinCompClassDiagram="false" ShowRowGridLineWithinCompERD="true" ShowRowGridLineWithinORMDiagram="true" ShowSchemaNameInERD="true" ShowTransitionTrigger="\u0000" ShowUseCaseExtensionPoint="true" ShowUseCaseID="false" SnapConnectorsAfterZoom="false" StateDiagramShowDiagramFrame="true" StateShowParametersOfInternalActivities="false" StateShowPrePostConditionAndBodyOfInternalActivities="true" StopTargetLifelineOnCreateDestroyMessage="\u0002" SupportHtmlTaggedValue="true" SupportMultipleLineAttribute="true" SuppressImpliedMultiplicityForAttributeAssociationEnd="false" SyncAssociationNameWithAssociationClass="\u0000" SyncAssociationRoleNameWithReferencedAttributeName="true" SyncDocOfInterfaceToSubClass="\u0000" TextAntiAliasing="true" TextualAnalysisGenerateRequirementTextOption="\u0001" TextualAnalysisHighlightOption="\u0000" UnnamedIndexPattern="{table_name}_{column_name}" UseCaseDiagramShowDiagramFrame="true" UseStateNameTab="false" WireflowDiagramDevice="0" WireflowDiagramShowActiveFlowLabel="true" WireflowDiagramTheme="0" WireflowDiagramWireflowShowPreview="true" WireflowDiagramWireflowShowScreenId="true">
				<DefaultHtmlDocFont Family="Dialog" Size="12" Style="0"/>
			</DiagramOptions>
			<GeneralOptions ConfirmSubLevelIdWithDot="true" QuickAddGlossaryTermParentModelId="default"/>
			<InstantReverseOptions CalculateGeneralizationAndRealization="false" CreateShapeForParentModelOfDraggedClassPackage="false" ReverseGetterSetter="\u0000" ReverseOperationImplementation="false" ShowPackageForNewDiagram="\u0001" ShowPackageOwner="\u0000"/>
			<ModelQualityOptions EnableModelQualityChecking="false"/>
			<ORMOptions AlterColumnUserType="true" DecimalPrecision="19" DecimalScale="0" ExportCommentToDatabase="true" FormattedSQL="false" GenerateAssociationWithAttribute="false" GenerateDiagramFromORMWizards="true" GetterSetterVisibility="\u0000" IdGeneratorType="native" MappingFileColumnOrder="\u0000" NumericToClassType="\u0000" QuoteSQLIdentifier="\u0000" RecreateShapeWhenSync="false" SyncToClassDiagramAttributeName="\u0001" SyncToClassDiagramAttributeNamePrefix="" SyncToClassDiagramAttributeNameSuffix="" SyncToClassDiagramClassName="\u0000" SyncToClassDiagramClassNamePrefix="" SyncToClassDiagramClassNameSuffix="" SyncToERDColumnName="\u0000" SyncToERDColumnNamePrefix="" SyncToERDColumnNameSuffix="" SyncToERDTableName="\u0004" SyncToERDTableNamePrefix="" SyncToERDTableNameSuffix="" SynchronizeDefaultValueToColumn="false" SynchronizeName="\u0002" TablePerSubclassFKMapping="\u0000" UpperCaseSQL="true" UseDefaultDecimal="true" WrappingServletRequest="\u0001"/>
			<RequirementDiagramOptions DefaultWrapMember="true" ShowAttributes="\u0001" SupportHTMLAttribute="false"/>
			<StateCodeEngineOptions AutoCreateInitialStateInStateDiagram="true" AutoCreateTransitionMethods="true" DefaultInitialStateLocationX="-1" DefaultInitialStateLocationY="-1" GenerateDebugMessage="false" GenerateSample="true" GenerateTryCatch="true" Language="\u0000" RegenerateTransitionMethods="false" SyncTransitionMethods="true"/>
			<WarningOptions CreateORMClassInDefaultPackage="true"/>
			<PORepository>
				<POUserIDFormats>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAmy" LastNumericValue="0" ModelType="BPMNElement" Prefix="BP" Suffix=""/>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAmz" LastNumericValue="11" ModelType="Actor" Prefix="AC" Suffix=""/>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAm0" LastNumericValue="35" ModelType="UseCase" Prefix="UC" Suffix=""/>
					<POUserIDFormat Digits="3" Guid="false" Id="p01BOoWGAqCOCAm1" LastNumericValue="0" ModelType="Requirement" Prefix="REQ" Suffix=""/>
					<POUserIDFormat Digits="3" Guid="false" Id="p01BOoWGAqCOCAm2" LastNumericValue="0" ModelType="BusinessRule" Prefix="BR" Suffix=""/>
					<POUserIDFormat Digits="-1" Guid="false" Id="p01BOoWGAqCOCAm3" LastNumericValue="0" ModelType="BusinessProcessDiagram" Prefix="" Suffix=""/>
				</POUserIDFormats>
			</PORepository>
		</ProjectOptions>
	</ProjectInfo>
	<Models>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="9PVBOoWGAqCOCAXu" Name="boolean" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.312" PmLastModified="2026-10-21T10:30:48.325" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="HPVBOoWGAqCOCAXv" Name="byte" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.315" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXw" Name="char" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXx" Name="double" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXy" Name="float" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXz" Name="int" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX0" Name="long" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.323" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX1" Name="short" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.314" PmLastModified="2026-10-21T10:30:48.323" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX2" Name="void" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.314" PmLastModified="2026-10-21T10:30:48.323" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX3" Name="string" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.314" PmLastModified="2026-10-21T10:30:48.323" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<ModelRelationshipContainer BacklogActivityId="0" Documentation_plain="" Id="DoBBLFK3EBJFH71i" Name="relationships" PmAuthor="SinhVien" PmCreateDateTime="2026-10-14T10:00:00.000" PmLastModified="2026-11-04T17:08:29.638" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
			<ModelChildren>
				<ModelRelationshipContainer BacklogActivityId="0" Documentation_plain="" Id="Q8gQZYWFYC1QOgmr" Name="DBForeignKey" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:08:29.634" PmLastModified="2026-11-04T17:08:29.634" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
					<ModelChildren>
						<DBForeignKey BacklogActivityId="0" DataModel="Physical" Documentation_plain="" ForeignKeyRelationshipPattern="{association_name}" From="U4igZYWFYC1QOghP" FromMultiplicity="1" FromPhrase_IsNull="true" Id="4sPgZYWFYC1QOgmC" Identifying="false" Name="" OnDelete="" OnUpdate="" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:08:09.031" PmLastModified="2026-11-04T17:08:29.638" QualityReason_IsNull="true" QualityScore="-1" Subtype="false" SyncToAssociation="Yes" SyncType="Not Sync" To="RwKgZYWFYC1QOghk" ToMultiplicity="1" ToPhrase_IsNull="true" UserIDLastNumericValue="0" UserID_IsNull="true">
							<MasterView>
								<DBForeignKey Idref="WsPgZYWFYC1QOgmD" Name=""/>
							</MasterView>
						</DBForeignKey>
						<DBForeignKey BacklogActivityId="0" DataModel="Physical" Documentation_plain="" ForeignKeyRelationshipPattern="{association_name}" From="RwKgZYWFYC1QOghk" FromMultiplicity="1" FromPhrase_IsNull="true" Id="y_PgZYWFYC1QOgmJ" Identifying="false" Name="" OnDelete="" OnUpdate="" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:08:12.243" PmLastModified="2026-11-04T17:08:29.638" QualityReason_IsNull="true" QualityScore="-1" Subtype="false" SyncToAssociation="Yes" SyncType="Not Sync" To="H5JgZYWFYC1QOgkf" ToMultiplicity="0..*" ToPhrase_IsNull="true" UserIDLastNumericValue="0" UserID_IsNull="true">
							<MasterView>
								<DBForeignKey Idref="O_PgZYWFYC1QOgmK" Name=""/>
							</MasterView>
						</DBForeignKey>
						<DBForeignKey BacklogActivityId="0" DataModel="Physical" Documentation_plain="" ForeignKeyRelationshipPattern="{association_name}" From=".ySgZYWFYC1QOghZ" FromMultiplicity="1" FromPhrase_IsNull="true" Id="8TvgZYWFYC1QOgmP" Identifying="false" Name="" OnDelete="" OnUpdate="" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:08:15.503" PmLastModified="2026-11-04T17:08:29.638" QualityReason_IsNull="true" QualityScore="-1" Subtype="false" SyncToAssociation="Yes" SyncType="Not Sync" To="H5JgZYWFYC1QOgkf" ToMultiplicity="0..*" ToPhrase_IsNull="true" UserIDLastNumericValue="0" UserID_IsNull="true">
							<MasterView>
								<DBForeignKey Idref="qTvgZYWFYC1QOgmQ" Name=""/>
							</MasterView>
						</DBForeignKey>
						<DBForeignKey BacklogActivityId="0" DataModel="Physical" Documentation_plain="" ForeignKeyRelationshipPattern="{association_name}" From="U4igZYWFYC1QOghP" FromMultiplicity="1" FromPhrase_IsNull="true" Id="0ZfgZYWFYC1QOgmV" Identifying="true" Name="" OnDelete="" OnUpdate="" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:08:18.828" PmLastModified="2026-11-04T17:08:29.638" QualityReason_IsNull="true" QualityScore="-1" Subtype="false" SyncToAssociation="Yes" SyncType="Not Sync" To="eZfgZYWFYC1QOgma" ToMultiplicity="0..*" ToPhrase_IsNull="true" UserIDLastNumericValue="0" UserID_IsNull="true">
							<MasterView>
								<DBForeignKey Idref="qZfgZYWFYC1QOgmW" Name=""/>
							</MasterView>
						</DBForeignKey>
						<DBForeignKey BacklogActivityId="0" DataModel="Physical" Documentation_plain="" ForeignKeyRelationshipPattern="{association_name}" From=".ySgZYWFYC1QOghZ" FromMultiplicity="1" FromPhrase_IsNull="true" Id="3ZfgZYWFYC1QOgmf" Identifying="true" Name="" OnDelete="" OnUpdate="" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:08:18.875" PmLastModified="2026-11-04T17:08:29.638" QualityReason_IsNull="true" QualityScore="-1" Subtype="false" SyncToAssociation="Yes" SyncType="Not Sync" To="eZfgZYWFYC1QOgma" ToMultiplicity="0..*" ToPhrase_IsNull="true" UserIDLastNumericValue="0" UserID_IsNull="true">
							<MasterView>
								<DBForeignKey Idref="g5fgZYWFYC1QOgmg" Name=""/>
							</MasterView>
						</DBForeignKey>
					</ModelChildren>
				</ModelRelationshipContainer>
			</ModelChildren>
		</ModelRelationshipContainer>
		<DBTable BacklogActivityId="0" DDLClauses_IsNull="true" DataModel="Physical" Documentation_plain="" Id="U4igZYWFYC1QOghP" Location_IsNull="true" Name="Table" OrmSyncState="Not Sync" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:05:12.522" PmLastModified="2026-11-04T17:08:29.638" PrimaryKeyClustered="Unspecified" PrimaryKeyConstraintNamePattern="" PrimaryKeyConstraintName_IsNull="true" PrimaryKeyDDLClauses_IsNull="true" QualityReason_IsNull="true" QualityScore="-1" SyncType="Not Sync" Temporal="false" TemporalEndTimeColumn_IsNull="true" TemporalHistoryTable_IsNull="true" TemporalStartTimeColumn_IsNull="true" Type="0" Unlogged="false" UserIDLastNumericValue="0" UserID_IsNull="true">
			<ModelChildren>
				<DBColumn BacklogActivityId="0" CheckConstraint_IsNull="true" Collation_IsNull="true" DDLClauses_IsNull="true" DbColumnName_IsNull="true" DefaultValue_IsNull="true" Documentation_plain="" ForeignKeyNamePattern_IsNull="true" Generated="Unspecified" Id="mDFgZYWFYC1QOgky" IdGenerator_IsNull="true" IdentityIncrement="-1" IdentitySeed="-1" Index="false" Length="10" Name="maBan" Nullable="false" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:06:49.369" PmLastModified="2026-11-04T17:07:28.503" PrimaryKey="true" QualityReason_IsNull="true" QualityScore="-1" Scale="0" SequenceAllocationSize="-1" SyncToAttribute="Yes" SyncType="Not Sync" Type="integer" TypeName_IsNull="true" Type_internalValue="9" Unique="false" UserIDLastNumericValue="0" UserID_IsNull="true"/>
				<DBColumn BacklogActivityId="0" CheckConstraint_IsNull="true" Collation_IsNull="true" DDLClauses_IsNull="true" DbColumnName_IsNull="true" DefaultValue_IsNull="true" Documentation_plain="" ForeignKeyNamePattern_IsNull="true" Generated="Unspecified" Id="0yzgZYWFYC1QOglm" IdGenerator_IsNull="true" IdentityIncrement="-1" IdentitySeed="-1" Index="false" Length="10" Name="soBan" Nullable="false" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:07:32.555" PmLastModified="2026-11-04T17:08:29.638" PrimaryKey="false" QualityReason_IsNull="true" QualityScore="-1" Scale="0" SequenceAllocationSize="-1" SyncToAttribute="Yes" SyncType="Not Sync" Type="integer" TypeName_IsNull="true" Type_internalValue="9" Unique="true" UserIDLastNumericValue="0" UserID_IsNull="true"/>
				<DBColumn BacklogActivityId="0" CheckConstraint_IsNull="true" Collation_IsNull="true" DDLClauses_IsNull="true" DbColumnName_IsNull="true" DefaultValue_IsNull="true" Documentation_plain="" ForeignKeyNamePattern_IsNull="true" Generated="Unspecified" Id="24bgZYWFYC1QOglo" IdGenerator_IsNull="true" IdentityIncrement="-1" IdentitySeed="-1" Index="false" Length="10" Name="trangThai" Nullable="false" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:07:44.091" PmLastModified="2026-11-04T17:08:29.638" PrimaryKey="false" QualityReason_IsNull="true" QualityScore="-1" Scale="0" SequenceAllocationSize="-1" SyncToAttribute="Yes" SyncType="Not Sync" Type="integer" TypeName_IsNull="true" Type_internalValue="9" Unique="false" UserIDLastNumericValue="0" UserID_IsNull="true"/>
			</ModelChildren>
			<FromSimpleRelationships>
				<DBForeignKey Idref="4sPgZYWFYC1QOgmC" Name=""/>
				<DBForeignKey Idref="0ZfgZYWFYC1QOgmV" Name=""/>
			</FromSimpleRelationships>
			<MasterView>
				<DBTable Idref="E4igZYWFYC1QOghO" Name="Table"/>
			</MasterView>
		</DBTable>
		<DBView BacklogActivityId="0" CheckOption="None" CreateStatement_IsNull="true" CustomizedCreateStatement="false" DataModel="Physical" Distinct="false" Documentation_plain="" Id=".ySgZYWFYC1QOghZ" Insertable="false" Name="View" OrmSyncState="Not Sync" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:05:17.407" PmLastModified="2026-11-04T17:08:29.638" QualityReason_IsNull="true" QualityScore="-1" SyncType="Not Sync" Type="0" UserIDLastNumericValue="0" UserID_IsNull="true" ViewEditorDiagramId_IsNull="true">
			<FromSimpleRelationships>
				<DBForeignKey Idref="8TvgZYWFYC1QOgmP" Name=""/>
				<DBForeignKey Idref="3ZfgZYWFYC1QOgmf" Name=""/>
			</FromSimpleRelationships>
			<MasterView>
				<DBView Idref="uySgZYWFYC1QOghY" Name="View"/>
			</MasterView>
		</DBView>
		<DBTable BacklogActivityId="0" DDLClauses_IsNull="true" DataModel="Physical" Documentation_plain="" Id="RwKgZYWFYC1QOghk" Location_IsNull="true" Name="Entity2" OrmSyncState="Not Sync" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:05:24.578" PmLastModified="2026-11-04T17:08:29.638" PrimaryKeyClustered="Unspecified" PrimaryKeyConstraintNamePattern="" PrimaryKeyConstraintName_IsNull="true" PrimaryKeyDDLClauses_IsNull="true" QualityReason_IsNull="true" QualityScore="-1" SyncType="Not Sync" Temporal="false" TemporalEndTimeColumn_IsNull="true" TemporalHistoryTable_IsNull="true" TemporalStartTimeColumn_IsNull="true" Type="0" Unlogged="false" UserIDLastNumericValue="0" UserID_IsNull="true">
			<ModelChildren>
				<DBColumn BacklogActivityId="0" CheckConstraint_IsNull="true" Collation_IsNull="true" DDLClauses_IsNull="true" DbColumnName_IsNull="true" DefaultValue_IsNull="true" Documentation_plain="" ForeignKeyNamePattern="{reference_table_name}{reference_column_name}" Generated="Unspecified" Id="VsPgZYWFYC1QOgmF" IdGenerator="native" IdentityIncrement="-1" IdentitySeed="-1" Index="false" Length="10" Name="TablemaBan" Nullable="false" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:08:09.066" PmLastModified="2026-11-04T17:08:29.638" PrimaryKey="false" QualityReason_IsNull="true" QualityScore="-1" Scale="0" SequenceAllocationSize="-1" SyncToAttribute="Yes" SyncType="Not Sync" Type="integer" TypeName_IsNull="true" Type_internalValue="9" Unique="false" UserIDLastNumericValue="0" UserID_IsNull="true">
					<ForeignKeyConstraints>
						<DBForeignKeyConstraint BacklogActivityId="0" Documentation_plain="" ForeignKey="4sPgZYWFYC1QOgmC" Id="VsPgZYWFYC1QOgmH" Name="" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:08:09.066" PmLastModified_IsNull="true" QualityReason_IsNull="true" QualityScore="-1" RefColumn="mDFgZYWFYC1QOgky" UserIDLastNumericValue="0" UserID_IsNull="true"/>
					</ForeignKeyConstraints>
				</DBColumn>
			</ModelChildren>
			<FromSimpleRelationships>
				<DBForeignKey Idref="y_PgZYWFYC1QOgmJ" Name=""/>
			</FromSimpleRelationships>
			<ToSimpleRelationships>
				<DBForeignKey Idref="4sPgZYWFYC1QOgmC" Name=""/>
			</ToSimpleRelationships>
			<MasterView>
				<DBTable Idref="RwKgZYWFYC1QOghj" Name="Entity2"/>
			</MasterView>
		</DBTable>
		<DBTable BacklogActivityId="0" DDLClauses_IsNull="true" DataModel="Physical" Documentation_plain="" Id="H5JgZYWFYC1QOgkf" Location_IsNull="true" Name="Entity3" OrmSyncState="Not Sync" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:06:32.440" PmLastModified="2026-11-04T17:08:29.638" PrimaryKeyClustered="Unspecified" PrimaryKeyConstraintNamePattern="" PrimaryKeyConstraintName_IsNull="true" PrimaryKeyDDLClauses_IsNull="true" QualityReason_IsNull="true" QualityScore="-1" SyncType="Not Sync" Temporal="false" TemporalEndTimeColumn_IsNull="true" TemporalHistoryTable_IsNull="true" TemporalStartTimeColumn_IsNull="true" Type="0" Unlogged="false" UserIDLastNumericValue="0" UserID_IsNull="true">
			<ToSimpleRelationships>
				<DBForeignKey Idref="y_PgZYWFYC1QOgmJ" Name=""/>
				<DBForeignKey Idref="8TvgZYWFYC1QOgmP" Name=""/>
			</ToSimpleRelationships>
			<MasterView>
				<DBTable Idref="H5JgZYWFYC1QOgke" Name="Entity3"/>
			</MasterView>
		</DBTable>
		<DBTable BacklogActivityId="0" DDLClauses_IsNull="true" DataModel="Physical" Documentation_plain="" Id="eZfgZYWFYC1QOgma" Location_IsNull="true" Name="Table_View" OrmSyncState="Not Sync" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:08:18.846" PmLastModified="2026-11-04T17:08:29.638" PrimaryKeyClustered="Unspecified" PrimaryKeyConstraintNamePattern="" PrimaryKeyConstraintName_IsNull="true" PrimaryKeyDDLClauses_IsNull="true" QualityReason_IsNull="true" QualityScore="-1" SyncType="Sync" Temporal="false" TemporalEndTimeColumn_IsNull="true" TemporalHistoryTable_IsNull="true" TemporalStartTimeColumn_IsNull="true" Type="0" Unlogged="false" UserIDLastNumericValue="0" UserID_IsNull="true">
			<ModelChildren>
				<DBColumn BacklogActivityId="0" CheckConstraint_IsNull="true" Collation_IsNull="true" DDLClauses_IsNull="true" DbColumnName_IsNull="true" DefaultValue_IsNull="true" Documentation_plain="" ForeignKeyNamePattern="{reference_table_name}{reference_column_name}" Generated="Unspecified" Id="TZfgZYWFYC1QOgmc" IdGenerator="native" IdentityIncrement="-1" IdentitySeed="-1" Index="false" Length="10" Name="TablemaBan" Nullable="false" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:08:18.866" PmLastModified="2026-11-04T17:08:29.638" PrimaryKey="true" QualityReason_IsNull="true" QualityScore="-1" Scale="0" SequenceAllocationSize="-1" SyncToAttribute="Yes" SyncType="Not Sync" Type="integer" TypeName_IsNull="true" Type_internalValue="9" Unique="false" UserIDLastNumericValue="0" UserID_IsNull="true">
					<ForeignKeyConstraints>
						<DBForeignKeyConstraint BacklogActivityId="0" Documentation_plain="" ForeignKey="0ZfgZYWFYC1QOgmV" Id="zZfgZYWFYC1QOgmd" Name="" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:08:18.867" PmLastModified_IsNull="true" QualityReason_IsNull="true" QualityScore="-1" RefColumn="mDFgZYWFYC1QOgky" UserIDLastNumericValue="0" UserID_IsNull="true"/>
					</ForeignKeyConstraints>
				</DBColumn>
			</ModelChildren>
			<ToSimpleRelationships>
				<DBForeignKey Idref="0ZfgZYWFYC1QOgmV" Name=""/>
				<DBForeignKey Idref="3ZfgZYWFYC1QOgmf" Name=""/>
			</ToSimpleRelationships>
			<MasterView>
				<DBTable Idref="eZfgZYWFYC1QOgmZ" Name="Table_View"/>
			</MasterView>
		</DBTable>
		<DBTable BacklogActivityId="0" DDLClauses_IsNull="true" DataModel="Physical" Documentation_plain="" Id="O_QQZYWFYC1QOgmx" Location_IsNull="true" Name="Entity" OrmSyncState="Not Sync" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:08:36.828" PmLastModified="2026-11-04T17:08:47.741" PrimaryKeyClustered="Unspecified" PrimaryKeyConstraintNamePattern="" PrimaryKeyConstraintName_IsNull="true" PrimaryKeyDDLClauses_IsNull="true" QualityReason_IsNull="true" QualityScore="-1" SyncType="Not Sync" Temporal="false" TemporalEndTimeColumn_IsNull="true" TemporalHistoryTable_IsNull="true" TemporalStartTimeColumn_IsNull="true" Type="0" Unlogged="false" UserIDLastNumericValue="0" UserID_IsNull="true">
			<MasterView>
				<DBTable Idref="O_QQZYWFYC1QOgmw" Name="Entity"/>
			</MasterView>
		</DBTable>
	</Models>
	<Diagrams>
		<ERDiagram AlignToGrid="false" AutoFitShapesSize="false" ConnectionPointStyle="0" ConnectorLabelOrientation="0" ConnectorLineJumps="0" ConnectorLineJumpsSize="0" ConnectorModelElementNameAlignment="4" ConnectorStyle="1" DataModel="2" DiagramBackground="rgb(255, 255, 255)" Editable="true" FilterByViewpointLegend="true" FollowDiagramParentElement="true" ForeignKeyArrowHeadSize="3" GridColor="rgb(192, 192, 192)" GridHeight="10" GridVisible="false" GridWidth="10" Height="598" HideConnectorIfFromToIsHidden="0" HideEmptyTaggedValues="false" Id="in8gZYWFYC1QOggy" ImageHeight="0" ImageScale="1.0" ImageWidth="0" InitializeDiagramForCreate="true" LogicalPhysicalColumnNameAbbreviationSetAddress="" LogicalPhysicalEntityNameAbbreviationSetAddress="" LogicalPhysicalSchemaNameAbbreviationSetAddress="" Maximized="true" ModelElementNameAlignment="4" Name="Entity Relationship Diagram1" PaintConnectorThroughLabel="1" PmAuthor="phanb" PmCreateDateTime="2026-11-04T17:05:07.537" PmLastModified="2026-11-04T17:08:45.708" PointConnectorEndToCompartmentMember="true" QualityScore="-1" RequestFitSizeWithPromptUser="false" RequestValidateSnapToGrid="false" ShapePresentationOption="0" ShowActivityStateNodeCaption="524287" ShowAllocatedFrom="true" ShowAllocatedTo="true" ShowColorLegend="false" ShowConnectorLegend="false" ShowConnectorName="0" ShowConstraints="false" ShowDefaultPackage="false" ShowInformationItemOption="2" ShowPMAuthor="false" ShowPMDifficulty="false" ShowPMDiscipline="false" ShowPMIteration="false" ShowPMPhase="false" ShowPMPriority="false" ShowPMStatus="false" ShowPMVersion="false" ShowPackageNameStyle="0" ShowRelationshipConstraintExpression="false" ShowSchemaName="true" ShowShapeLegend="false" ShowShapeStereotypeIconName="true" ShowStereotypes="true" ShowTaggedValues="false" TeamworkCreateDateTime="0" TrimmedHeight="0" TrimmedWidth="0" Width="1255" X="0" Y="0" ZoomRatio="1.0" _alignColumnProperties="true" _columnConstraintsDisplayOption="2" _globalPaletteOption="true" _pointForeignKeyEndToColumn="false" _showColumnDefaultValue="false" _showColumnStereotypes="true" _showColumnTypes="true" _showColumnUserType="false" _showDBTableColumnsMode="1" _showDBViewColumnsMode="1" _showExtraColumnProperties="true" _showProcedureStereotypes="true" _showStoredProcedureResultSetColumns="true" _showStoredProcedures="true" _showTriggerStereotypes="true" _showTriggers="true">
			<Shapes>
				<DBTable Background="rgb(245, 182, 122)" ColSortType="0" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" CreatorDiagramType="ERDiagram" Foreground="rgb(0, 0, 0)" Height="77" Id="E4igZYWFYC1QOghO" MetaModelElement="U4igZYWFYC1QOghP" Model="U4igZYWFYC1QOghP" ModelElementNameAlignment="9" Name="Table" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowColumnStereotypes="0" ShowColumnsMode="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="173" X="125" Y="84" ZOrder="12">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="165" X="0" Y="0"/>
					<FillColor Color="rgb(245, 182, 122)" Style="1" Transparency="0" Type="1"/>
					<CompartmentFont Value="none"/>
				</DBTable>
				<DBView Background="rgb(245, 182, 122)" ColSortType="0" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" CreatorDiagramType="ERDiagram" Foreground="rgb(0, 0, 0)" Height="41" Id="uySgZYWFYC1QOghY" MetaModelElement=".ySgZYWFYC1QOghZ" Model=".ySgZYWFYC1QOghZ" ModelElementNameAlignment="9" Name="View" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowColumnStereotypes="0" ShowColumnsMode="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="88" X="490" Y="70" ZOrder="10">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="32" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="88" X="0" Y="0"/>
					<FillColor Color="rgb(245, 182, 122)" Style="1" Transparency="0" Type="1"/>
					<CompartmentFont Value="none"/>
				</DBView>
				<DBTable Background="rgb(245, 182, 122)" ColSortType="0" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" CreatorDiagramType="ERDiagram" Foreground="rgb(0, 0, 0)" Height="41" Id="RwKgZYWFYC1QOghj" MetaModelElement="RwKgZYWFYC1QOghk" Model="RwKgZYWFYC1QOghk" ModelElementNameAlignment="9" Name="Entity2" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowColumnStereotypes="0" ShowColumnsMode="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="164" X="167" Y="238" ZOrder="8">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="70" X="0" Y="0"/>
					<FillColor Color="rgb(245, 182, 122)" Style="1" Transparency="0" Type="1"/>
					<CompartmentFont Value="none"/>
				</DBTable>
				<DBTable Background="rgb(245, 182, 122)" ColSortType="0" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" CreatorDiagramType="ERDiagram" Foreground="rgb(0, 0, 0)" Height="40" Id="H5JgZYWFYC1QOgke" MetaModelElement="H5JgZYWFYC1QOgkf" Model="H5JgZYWFYC1QOgkf" ModelElementNameAlignment="9" Name="Entity3" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowColumnStereotypes="0" ShowColumnsMode="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="70" X="433" Y="256" ZOrder="6">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="70" X="0" Y="0"/>
					<FillColor Color="rgb(245, 182, 122)" Style="1" Transparency="0" Type="1"/>
					<CompartmentFont Value="none"/>
				</DBTable>
				<DBTable Background="rgb(245, 182, 122)" ColSortType="0" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" CreatorDiagramType="ERDiagram" Foreground="rgb(0, 0, 0)" Height="41" Id="eZfgZYWFYC1QOgmZ" MetaModelElement="eZfgZYWFYC1QOgma" Model="eZfgZYWFYC1QOgma" ModelElementNameAlignment="9" Name="Table_View" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowColumnStereotypes="0" ShowColumnsMode="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="166" X="316" Y="63" ZOrder="4">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="160" X="0" Y="0"/>
					<FillColor Color="rgb(245, 182, 122)" Style="1" Transparency="0" Type="1"/>
					<CompartmentFont Value="none"/>
				</DBTable>
				<DBTable Background="rgb(245, 182, 122)" ColSortType="0" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" CreatorDiagramType="ERDiagram" Foreground="rgb(0, 0, 0)" Height="40" Id="O_QQZYWFYC1QOgmw" MetaModelElement="O_QQZYWFYC1QOgmx" Model="O_QQZYWFYC1QOgmx" ModelElementNameAlignment="9" Name="Entity" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowColumnStereotypes="0" ShowColumnsMode="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="70" X="323" Y="401" ZOrder="2">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="70" X="0" Y="0"/>
					<FillColor Color="rgb(245, 182, 122)" Style="1" Transparency="0" Type="1"/>
					<CompartmentFont Value="none"/>
				</DBTable>
			</Shapes>
			<Connectors>
				<DBForeignKey Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="ERDiagram" Foreground="rgb(0, 0, 0)" From="E4igZYWFYC1QOghO" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" HasFromLabel="false" HasToLabel="false" Height="176" Id="WsPgZYWFYC1QOgmD" MetaModelElement="4sPgZYWFYC1QOgmC" Model="4sPgZYWFYC1QOgmC" ModelElementNameAlignment="9" Name="" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestResetLabels="false" Selectable="true" ShowConnectorName="2" To="RwKgZYWFYC1QOghj" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="100" X="137" Y="111" ZOrder="14">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="188" Y="199"/>
					<Points>
						<Point X="187.0" Y="161.0"/>
						<Point X="187.0" Y="237.0"/>
					</Points>
				</DBForeignKey>
				<DBForeignKey Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="ERDiagram" Foreground="rgb(0, 0, 0)" From="RwKgZYWFYC1QOghj" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" HasFromLabel="false" HasToLabel="false" Height="100" Id="O_PgZYWFYC1QOgmK" MetaModelElement="y_PgZYWFYC1QOgmJ" Model="y_PgZYWFYC1QOgmJ" ModelElementNameAlignment="9" Name="" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestResetLabels="false" Selectable="true" ShowConnectorName="2" To="H5JgZYWFYC1QOgke" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="206" X="276" Y="228" ZOrder="16">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="369" Y="277"/>
					<Points>
						<Point X="326.0" Y="278.0"/>
						<Point X="432.0" Y="278.0"/>
					</Points>
				</DBForeignKey>
				<DBForeignKey Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="ERDiagram" Foreground="rgb(0, 0, 0)" From="uySgZYWFYC1QOghY" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" HasFromLabel="false" HasToLabel="false" Height="250" Id="qTvgZYWFYC1QOgmQ" MetaModelElement="8TvgZYWFYC1QOgmP" Model="8TvgZYWFYC1QOgmP" ModelElementNameAlignment="9" Name="" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestResetLabels="false" Selectable="true" ShowConnectorName="2" To="H5JgZYWFYC1QOgke" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="100" X="452" Y="61" ZOrder="18">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="503" Y="186"/>
					<Points>
						<Point X="502.0" Y="111.0"/>
						<Point X="502.0" Y="261.0"/>
					</Points>
				</DBForeignKey>
				<DBForeignKey Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="ERDiagram" Foreground="rgb(0, 0, 0)" From="E4igZYWFYC1QOghO" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" HasFromLabel="false" HasToLabel="false" Height="100" Id="qZfgZYWFYC1QOgmW" MetaModelElement="0ZfgZYWFYC1QOgmV" Model="0ZfgZYWFYC1QOgmV" ModelElementNameAlignment="9" Name="" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestResetLabels="false" Selectable="true" ShowConnectorName="2" To="eZfgZYWFYC1QOgmZ" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="126" X="239" Y="34" ZOrder="20">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="292" Y="83"/>
					<Points>
						<Point X="289.0" Y="84.0"/>
						<Point X="315.0" Y="84.0"/>
					</Points>
				</DBForeignKey>
				<DBForeignKey Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="ERDiagram" Foreground="rgb(0, 0, 0)" From="uySgZYWFYC1QOghY" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" HasFromLabel="false" HasToLabel="false" Height="100" Id="g5fgZYWFYC1QOgmg" MetaModelElement="3ZfgZYWFYC1QOgmf" Model="3ZfgZYWFYC1QOgmf" ModelElementNameAlignment="9" Name="" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestResetLabels="false" Selectable="true" ShowConnectorName="2" To="eZfgZYWFYC1QOgmZ" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="107" X="432" Y="32" ZOrder="22">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="474" Y="78"/>
					<Points>
						<Point X="489.0" Y="82.0"/>
						<Point X="482.0" Y="82.0"/>
					</Points>
				</DBForeignKey>
			</Connectors>
		</ERDiagram>
	</Diagrams>
</Project>
```

</details>

### `references/real-samples/state_diagram.xml`

<details>
<summary>Mở nội dung tệp</summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Project Author="SinhVien" CommentTableSortAscending="false" CommentTableSortColumn="Date Time" Description="&lt;html&gt;&#13;&#10;  &lt;head&gt;&#13;&#10;    &lt;style type=&quot;text/css&quot;&gt;&#10;      &lt;!--&#10;        body { color: #000000; font-family: Dialog; font-size: 12px }&#10;      --&gt;&#10;    &lt;/style&gt;&#13;&#10;    &#13;&#10;  &lt;/head&gt;&#13;&#10;  &lt;body&gt;&#13;&#10;  &lt;/body&gt;&#13;&#10;&lt;/html&gt;&#13;&#10;" DocumentationType="html" ExportedFromDifferentName="false" ExporterVersion="16.1.1" Name="btl2" TextualAnalysisHighlightOptionCaseSensitive="false" UmlVersion="2.x" Xml_structure="simple">
	<ProjectInfo>
		<LogicalView/>
		<ProjectOptions>
			<DiagramOptions ActivityDiagramControlFlowDisplayOption="\u0000" ActivityDiagramShowActionCallBehaviorOption="\u0000" ActivityDiagramShowActivityEdgeWeight="true" ActivityDiagramShowDiagramFrame="true" ActivityDiagramShowObjectNodeType="true" ActivityDiagramShowPartitionHandle="\u0000" AddDataStoresExtEntitiesToDecomposedDFD="\u0002" AlignColumnProperties="true" AllowConfigShowInOutFlowButtonsInDataFlowDiagram="false" AutoGenerateRoleName="false" AutoSetAttributeType="true" AutoSetColumnType="true" AutoSyncRoleName="true" BlockDefinitionDiagramShowDiagramFrame="true" BpPoolLaneDefaultOrientation="\u0000" BpdAutoStretchPools="true" BpdConnectGatewayWithFlowObjectInDifferentPool="\u0000" BpdDefaultConnectionPointStyle="\u0001" BpdDefaultConnectorStyle="\u0005" BpdDhowIdOption="\u0000" BpdShowActivitiesTypeIcon="true" BusinessProcessDiagramDefaultLanguage="English" ClassVisibilityStyle="\u0001" ConnectorLabelOrientation="\u0000" CreateOneMessagePerDirection="true" DecisionMergeNodeConnectionPointStyle="\u0000" DefaultAssociationEndNavigable="\u0001" DefaultAssociationEndVisibility="\u0000" DefaultAssociationShowFromMultiplicity="true" DefaultAssociationShowFromRoleName="true" DefaultAssociationShowFromRoleVisibility="true" DefaultAssociationShowStereotypes="true" DefaultAssociationShowToMultiplicity="true" DefaultAssociationShowToRoleName="true" DefaultAssociationShowToRoleVisibility="true" DefaultAttributeMultiplicity="false" DefaultAttributeType="" DefaultAttributeVisibility="\u0001" DefaultClassAttributeMultiplicity="" DefaultClassAttributeMultiplicityOrdered="false" DefaultClassAttributeMultiplicityUnique="true" DefaultClassInterfaceBall="false" DefaultClassVisibility="\u0004" DefaultColumnType="integer(10)" DefaultConnectionPointStyle="\u0000" DefaultConnectorStyle="\u0001" DefaultDiagramBackground="rgb(255, 255, 255)" DefaultDisplayAsRobustnessAnalysisIcon="true" DefaultDisplayAsRobustnessAnalysisIconInSequenceDiagram="true" DefaultDisplayAsStereotypeIcon="false" DefaultFontColor="rgb(0, 0, 0)" DefaultGenDiagramTypeFromScenario="\u0000" DefaultHtmlDocFontColor="rgb(0, 0, 0)" DefaultLineJumps="\u0000" DefaultOperationVisibility="\u0004" DefaultParameterDirection="\u0002" DefaultShowAttributeInitialValue="true" DefaultShowAttributeOption="\u0001" DefaultShowClassMemberStereotype="true" DefaultShowDirection="false" DefaultShowMultiplicityConstraints="false" DefaultShowOperationOption="\u0001" DefaultShowOperationSignature="true" DefaultShowOrderedMultiplicityConstraint="true" DefaultShowOwnedAssociationEndAsAttribute="true" DefaultShowOwner="false" DefaultShowOwnerSkipModelInFullyQualifiedOwnerSignature="true" DefaultShowReceptionOption="\u0001" DefaultShowTemplateParameter="true" DefaultShowTypeOption="\u0001" DefaultShowUniqueMultiplicityConstraint="true" DefaultTypeOfSubProcess="\u0000" DefaultWrapClassMember="false" DrawTextAnnotationOpenRectangleFollowConnectorEnd="true" EnableMinimumSize="true" EntityColumnConstraintsPresentation="\u0002" ErdIndexNumOfDigits="-1" ErdIndexPattern="{table_name}" ErdIndexPatternSyncAutomatically="true" ErdManyToManyJoinTableDelimiter="_" EtlTableDiagramFontSize="14" ExpandedSubProcessDiagramContent="\u0001" ForeignKeyArrowHeadSize="\u0002" ForeignKeyConnectorEndPointAssociatedColumn="false" ForeignKeyNamePattern="{reference_table_name}{reference_column_name}" ForeignKeyNamePatternCaseHandling="0" ForeignKeyRelationshipPattern="{association_name}" FractionalMetrics="true" GeneralizationSetNotation="\u0001" GraphicAntiAliasing="true" GridDiagramFontSize="14" InteractionDiagramShowDiagramFrame="true" InternalBlockDiagramShowDiagramFrame="true" LineJumpSize="\u0000" ModelElementNameAlignment="\u0004" MultipleLineClassName="\u0001" PackageDiagramShowDiagramFrame="true" PaintConnectorThroughLabel="false" ParametricDiagramShowDiagramFrame="true" PointConnectorEndToCompartmentMember="true" PrimaryKeyConstraintPattern="" PrimaryKeyNamePattern="ID" RenameConstructorAfterRenameClass="\u0000" RenameExtensionPointToFollowExtendUseCase="\u0000" RequirementDiagramShowDiagramFrame="true" ShapeAutoFitSize="false" ShowActivationsInSequenceDiagram="true" ShowActivityStateNodeCaption="524287" ShowArtifactOption="\u0002" ShowAssociatedDiagramNameOfInteraction="false" ShowAssociationRoleStereotypes="true" ShowAttributeGetterSetter="false" ShowBSElementCode="true" ShowClassEmptyCompartments="false" ShowColumnDefaultValue="false" ShowColumnNullable="true" ShowColumnType="true" ShowColumnUniqueConstraintName="false" ShowColumnUserType="false" ShowComponentOption="\u0002" ShowExtraColumnProperties="true" ShowInOutFlowButtonsInDataFlowDiagram="false" ShowInOutFlowsInSubLevelDiagram="true" ShowMessageOperationSignatureForSequenceAndCommunicationDiagram="true" ShowMessageStereotypeInSequenceAndCommunicationDiagram="true" ShowNumberInCollaborationDiagram="true" ShowNumberInSequenceDiagram="true" ShowPackageNameStyle="\u0000" ShowParameterNameInOperationSignature="true" ShowRowGridLineWithinCompClassDiagram="false" ShowRowGridLineWithinCompERD="true" ShowRowGridLineWithinORMDiagram="true" ShowSchemaNameInERD="true" ShowTransitionTrigger="\u0000" ShowUseCaseExtensionPoint="true" ShowUseCaseID="false" SnapConnectorsAfterZoom="false" StateDiagramShowDiagramFrame="true" StateShowParametersOfInternalActivities="false" StateShowPrePostConditionAndBodyOfInternalActivities="true" StopTargetLifelineOnCreateDestroyMessage="\u0002" SupportHtmlTaggedValue="true" SupportMultipleLineAttribute="true" SuppressImpliedMultiplicityForAttributeAssociationEnd="false" SyncAssociationNameWithAssociationClass="\u0000" SyncAssociationRoleNameWithReferencedAttributeName="true" SyncDocOfInterfaceToSubClass="\u0000" TextAntiAliasing="true" TextualAnalysisGenerateRequirementTextOption="\u0001" TextualAnalysisHighlightOption="\u0000" UnnamedIndexPattern="{table_name}_{column_name}" UseCaseDiagramShowDiagramFrame="true" UseStateNameTab="false" WireflowDiagramDevice="0" WireflowDiagramShowActiveFlowLabel="true" WireflowDiagramTheme="0" WireflowDiagramWireflowShowPreview="true" WireflowDiagramWireflowShowScreenId="true">
				<DefaultHtmlDocFont Family="Dialog" Size="12" Style="0"/>
			</DiagramOptions>
			<GeneralOptions ConfirmSubLevelIdWithDot="true" QuickAddGlossaryTermParentModelId="default"/>
			<InstantReverseOptions CalculateGeneralizationAndRealization="false" CreateShapeForParentModelOfDraggedClassPackage="false" ReverseGetterSetter="\u0000" ReverseOperationImplementation="false" ShowPackageForNewDiagram="\u0001" ShowPackageOwner="\u0000"/>
			<ModelQualityOptions EnableModelQualityChecking="false"/>
			<ORMOptions AlterColumnUserType="true" DecimalPrecision="19" DecimalScale="0" ExportCommentToDatabase="true" FormattedSQL="false" GenerateAssociationWithAttribute="false" GenerateDiagramFromORMWizards="true" GetterSetterVisibility="\u0000" IdGeneratorType="native" MappingFileColumnOrder="\u0000" NumericToClassType="\u0000" QuoteSQLIdentifier="\u0000" RecreateShapeWhenSync="false" SyncToClassDiagramAttributeName="\u0001" SyncToClassDiagramAttributeNamePrefix="" SyncToClassDiagramAttributeNameSuffix="" SyncToClassDiagramClassName="\u0000" SyncToClassDiagramClassNamePrefix="" SyncToClassDiagramClassNameSuffix="" SyncToERDColumnName="\u0000" SyncToERDColumnNamePrefix="" SyncToERDColumnNameSuffix="" SyncToERDTableName="\u0004" SyncToERDTableNamePrefix="" SyncToERDTableNameSuffix="" SynchronizeDefaultValueToColumn="false" SynchronizeName="\u0002" TablePerSubclassFKMapping="\u0000" UpperCaseSQL="true" UseDefaultDecimal="true" WrappingServletRequest="\u0001"/>
			<RequirementDiagramOptions DefaultWrapMember="true" ShowAttributes="\u0001" SupportHTMLAttribute="false"/>
			<StateCodeEngineOptions AutoCreateInitialStateInStateDiagram="true" AutoCreateTransitionMethods="true" DefaultInitialStateLocationX="-1" DefaultInitialStateLocationY="-1" GenerateDebugMessage="false" GenerateSample="true" GenerateTryCatch="true" Language="\u0000" RegenerateTransitionMethods="false" SyncTransitionMethods="true"/>
			<WarningOptions CreateORMClassInDefaultPackage="true"/>
			<PORepository>
				<POUserIDFormats>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAmy" LastNumericValue="0" ModelType="BPMNElement" Prefix="BP" Suffix=""/>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAmz" LastNumericValue="11" ModelType="Actor" Prefix="AC" Suffix=""/>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAm0" LastNumericValue="35" ModelType="UseCase" Prefix="UC" Suffix=""/>
					<POUserIDFormat Digits="3" Guid="false" Id="p01BOoWGAqCOCAm1" LastNumericValue="0" ModelType="Requirement" Prefix="REQ" Suffix=""/>
					<POUserIDFormat Digits="3" Guid="false" Id="p01BOoWGAqCOCAm2" LastNumericValue="0" ModelType="BusinessRule" Prefix="BR" Suffix=""/>
					<POUserIDFormat Digits="-1" Guid="false" Id="p01BOoWGAqCOCAm3" LastNumericValue="0" ModelType="BusinessProcessDiagram" Prefix="" Suffix=""/>
				</POUserIDFormats>
			</PORepository>
		</ProjectOptions>
	</ProjectInfo>
	<Models>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="9PVBOoWGAqCOCAXu" Name="boolean" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.312" PmLastModified="2026-10-21T10:30:48.325" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="HPVBOoWGAqCOCAXv" Name="byte" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.315" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXw" Name="char" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXx" Name="double" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXy" Name="float" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXz" Name="int" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX0" Name="long" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.323" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX1" Name="short" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.314" PmLastModified="2026-10-21T10:30:48.323" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX2" Name="void" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.314" PmLastModified="2026-10-21T10:30:48.323" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX3" Name="string" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.314" PmLastModified="2026-10-21T10:30:48.323" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<InitialPseudoState BacklogActivityId="0" Documentation_plain="" Id="BsSGbYSu1NxVKM7F" Name="" PmAuthor="phanb" PmCreateDateTime="2026-10-20T10:00:00.000" PmLastModified="2026-10-21T10:30:48.313" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
			<FromSimpleRelationships>
				<Transition2 Idref="GYV3VsjjT421VoT9" Name="Chọn bàn, hệ thống chuẩn bị hóa đơn"/>
			</FromSimpleRelationships>
			<MasterView>
				<InitialPseudoState Idref="chsgjVHxPxO3hONX" Name=""/>
			</MasterView>
		</InitialPseudoState>
		<State2 BacklogActivityId="0" DataModel_IsNull="true" Documentation="&lt;HTML&gt;&lt;BODY&gt;&lt;p style=&quot;margin-top: 0&quot;&gt;Hóa đơn nháp, chưa lưu.&lt;/p&gt;&lt;/BODY&gt;&lt;/HTML&gt;" Documentation_plain="Hóa đơn nháp, chưa lưu." Id="yeNTUF1pnKynQiQQ" Name="MOI_TAO (nháp, chưa lưu)" PmAuthor="phanb" PmCreateDateTime="2026-10-20T10:00:00.000" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" StateInvariant="" UserIDLastNumericValue="0" UserID_IsNull="true">
			<FromSimpleRelationships>
				<Transition2 Idref="RnvwW3wTVXTYIlSr" Name="Bấm Lưu [có ít nhất một món], lưu thành công"/>
			</FromSimpleRelationships>
			<ToSimpleRelationships>
				<Transition2 Idref="GYV3VsjjT421VoT9" Name="Chọn bàn, hệ thống chuẩn bị hóa đơn"/>
			</ToSimpleRelationships>
			<MasterView>
				<State2 Idref="bpsgN4m6AsDdAhKZ" Name="MOI_TAO (nháp, chưa lưu)"/>
			</MasterView>
		</State2>
		<State2 BacklogActivityId="0" DataModel_IsNull="true" Documentation="&lt;HTML&gt;&lt;BODY&gt;&lt;p style=&quot;margin-top: 0&quot;&gt;Đơn đã lưu và đang phục vụ.&lt;/p&gt;&lt;/BODY&gt;&lt;/HTML&gt;" Documentation_plain="Đơn đã lưu và đang phục vụ." Id="iYYlUSarGNS4sB4j" Name="DANG_PHUC_VU" PmAuthor="phanb" PmCreateDateTime="2026-10-20T10:00:00.000" PmLastModified="2026-11-04T16:45:10.136" QualityReason_IsNull="true" QualityScore="-1" StateInvariant="" UserIDLastNumericValue="0" UserID_IsNull="true">
			<FromSimpleRelationships>
				<Transition2 Idref="sbuhOoWGAqCOCBAl" Name="Gọi thêm món, lưu thay đổi, gửi lại phiếu bếp"/>
				<Transition2 Idref="XDVPpYWFYC1QOhV1" Name="fdmvk"/>
			</FromSimpleRelationships>
			<ToSimpleRelationships>
				<Transition2 Idref="RnvwW3wTVXTYIlSr" Name="Bấm Lưu [có ít nhất một món], lưu thành công"/>
				<Transition2 Idref="sbuhOoWGAqCOCBAl" Name="Gọi thêm món, lưu thay đổi, gửi lại phiếu bếp"/>
			</ToSimpleRelationships>
			<MasterView>
				<State2 Idref="noGydrahGBBLoHya" Name="DANG_PHUC_VU"/>
			</MasterView>
		</State2>
		<ModelRelationshipContainer BacklogActivityId="0" Documentation_plain="" Id="DoBBLFK3EBJFH71i" Name="relationships" PmAuthor="SinhVien" PmCreateDateTime="2026-10-14T10:00:00.000" PmLastModified="2026-11-04T14:42:40.501" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
			<ModelChildren>
				<ModelRelationshipContainer BacklogActivityId="0" Documentation_plain="" Id="Ayq2yBkxqC6Qj7Vg" Name="Transition2" PmAuthor="SinhVien" PmCreateDateTime="2026-10-20T10:00:00.000" PmLastModified="2026-11-04T16:45:10.135" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
					<ModelChildren>
						<Transition2 BacklogActivityId="0" Documentation_plain="" From="BsSGbYSu1NxVKM7F" Id="GYV3VsjjT421VoT9" Kind="External" Name="Chọn bàn, hệ thống chuẩn bị hóa đơn" PmAuthor="phanb" PmCreateDateTime="2026-10-20T10:00:00.000" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" To="yeNTUF1pnKynQiQQ" UserIDLastNumericValue="0" UserID_IsNull="true">
							<MasterView>
								<Transition2 Idref="OyUdXBsxeX4VQ2gu" Name="Chọn bàn, hệ thống chuẩn bị hóa đơn"/>
							</MasterView>
						</Transition2>
						<Transition2 BacklogActivityId="0" Documentation_plain="" From="yeNTUF1pnKynQiQQ" Id="RnvwW3wTVXTYIlSr" Kind="External" Name="Bấm Lưu [có ít nhất một món], lưu thành công" PmAuthor="phanb" PmCreateDateTime="2026-10-20T10:00:00.000" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" To="iYYlUSarGNS4sB4j" UserIDLastNumericValue="0" UserID_IsNull="true">
							<MasterView>
								<Transition2 Idref="UtmIhPPOqLdfp5vz" Name="Bấm Lưu [có ít nhất một món], lưu thành công"/>
							</MasterView>
						</Transition2>
						<Transition2 BacklogActivityId="0" Documentation_plain="" From="iYYlUSarGNS4sB4j" Id="sbuhOoWGAqCOCBAl" Kind="External" Name="Gọi thêm món, lưu thay đổi, gửi lại phiếu bếp" PmAuthor="phanb" PmCreateDateTime="2026-10-21T10:33:59.309" PmLastModified="2026-10-21T10:34:09.617" QualityReason_IsNull="true" QualityScore="-1" To="iYYlUSarGNS4sB4j" UserIDLastNumericValue="0" UserID_IsNull="true">
							<MasterView>
								<Transition2 Idref="ubuhOoWGAqCOCBAm" Name="Gọi thêm món, lưu thay đổi, gửi lại phiếu bếp"/>
							</MasterView>
						</Transition2>
						<Transition2 BacklogActivityId="0" Documentation_plain="" From="iYYlUSarGNS4sB4j" Id="XDVPpYWFYC1QOhV1" Kind="External" Name="fdmvk" PmAuthor="phanb" PmCreateDateTime="2026-11-04T16:45:06.874" PmLastModified="2026-11-04T16:45:10.132" QualityReason_IsNull="true" QualityScore="-1" To="sSZPpYWFYC1QOhVW" UserIDLastNumericValue="0" UserID_IsNull="true">
							<MasterView>
								<Transition2 Idref="wjVPpYWFYC1QOhV2" Name="fdmvk"/>
							</MasterView>
						</Transition2>
					</ModelChildren>
				</ModelRelationshipContainer>
			</ModelChildren>
		</ModelRelationshipContainer>
		<FinalState2 BacklogActivityId="0" Documentation_plain="" DoneData_IsNull="true" Id="sSZPpYWFYC1QOhVW" Name="123" PmAuthor="phanb" PmCreateDateTime="2026-11-04T16:44:48.525" PmLastModified="2026-11-04T16:45:10.132" QualityReason_IsNull="true" QualityScore="-1" StateInvariant="" UserIDLastNumericValue="0" UserID_IsNull="true">
			<ToSimpleRelationships>
				<Transition2 Idref="XDVPpYWFYC1QOhV1" Name="fdmvk"/>
			</ToSimpleRelationships>
			<MasterView>
				<FinalState2 Idref="0SZPpYWFYC1QOhVV" Name="123"/>
			</MasterView>
		</FinalState2>
	</Models>
	<Diagrams>
		<StateDiagram AlignToGrid="false" AutoFitShapesSize="false" ConnectionPointStyle="0" ConnectorLabelOrientation="0" ConnectorLineJumps="0" ConnectorLineJumpsSize="0" ConnectorModelElementNameAlignment="4" ConnectorStyle="1" DiagramBackground="rgb(255, 255, 255)" Editable="true" FilterByViewpointLegend="true" FollowDiagramParentElement="true" GridColor="rgb(192, 192, 192)" GridHeight="10" GridVisible="false" GridWidth="10" Height="598" HideConnectorIfFromToIsHidden="0" HideEmptyTaggedValues="false" Id="xlDDZVqE7Iz4vOtY" ImageHeight="0" ImageScale="1.0" ImageWidth="0" InitializeDiagramForCreate="false" Maximized="true" ModelElementNameAlignment="4" Name="State Machine – Trạng thái đơn hàng" PaintConnectorThroughLabel="1" PmAuthor="phanb" PmCreateDateTime="2026-10-20T10:00:00.000" PmLastModified="2026-11-04T16:45:09.950" PointConnectorEndToCompartmentMember="true" ProtocolStateMachine="false" QualityScore="-1" RequestFitSizeWithPromptUser="false" RequestValidateSnapToGrid="false" ShapePresentationOption="0" ShowActivityStateNodeCaption="524287" ShowAllocatedFrom="true" ShowAllocatedTo="true" ShowColorLegend="false" ShowConnectorLegend="false" ShowConnectorName="0" ShowConstraints="false" ShowDefaultPackage="false" ShowDiagramFrame="true" ShowInformationItemOption="2" ShowPMAuthor="false" ShowPMDifficulty="false" ShowPMDiscipline="false" ShowPMIteration="false" ShowPMPhase="false" ShowPMPriority="false" ShowPMStatus="false" ShowPMVersion="false" ShowPackageNameStyle="0" ShowRelationshipConstraintExpression="false" ShowShapeLegend="false" ShowShapeStereotypeIconName="true" ShowStereotypes="true" ShowTaggedValues="false" ShowTransitionEffectBody="false" StateUseNameTab="2" TeamworkCreateDateTime="0" TrimmedHeight="0" TrimmedWidth="0" Width="1255" X="0" Y="0" ZoomRatio="1.0" _centerStateCaptionVertically="false" _globalPaletteOption="true" _showRegionName="2" _showTransitionOperation="false" _showTransitionOperationParameter="true" _showTransitionTriggers="true" _stateShowParametersOfInternalActivities="false" _stateShowPreconditionPostconditionAndBodyOfInternalActivities="true">
			<Shapes>
				<InitialPseudoState Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="1" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="20" Id="chsgjVHxPxO3hONX" MetaModelElement="BsSGbYSu1NxVKM7F" Model="BsSGbYSu1NxVKM7F" ModelElementNameAlignment="9" Name="" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="20" X="50" Y="170" ZOrder="4">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="50" Y="190"/>
					<FillColor Color="rgb(0, 0, 0)" Style="1" Transparency="0" Type="1"/>
				</InitialPseudoState>
				<State2 Background="rgb(122, 207, 245)" CenterCaptionVertically="0" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="50" Id="bpsgN4m6AsDdAhKZ" MetaModelElement="yeNTUF1pnKynQiQQ" Model="yeNTUF1pnKynQiQQ" ModelElementNameAlignment="9" Name="MOI_TAO (nháp, chưa lưu)" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RegionOrientation="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowInternalActivities="true" ShowInternalTransitions="true" ShowParametersOfInternalActivities="0" ShowPreconditionPostconditionAndBodyOfInternalActivities="0" ShowRegionName="0" ShowStereotypeIconName="0" ShowTaggedValues="0" UseNameTab="0" Width="200" X="282" Y="155" ZOrder="6">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="200" X="282" Y="155"/>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
				</State2>
				<State2 Background="rgb(122, 207, 245)" CenterCaptionVertically="0" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="50" Id="noGydrahGBBLoHya" MetaModelElement="iYYlUSarGNS4sB4j" Model="iYYlUSarGNS4sB4j" ModelElementNameAlignment="9" Name="DANG_PHUC_VU" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RegionOrientation="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowInternalActivities="true" ShowInternalTransitions="true" ShowParametersOfInternalActivities="0" ShowPreconditionPostconditionAndBodyOfInternalActivities="0" ShowRegionName="0" ShowStereotypeIconName="0" ShowTaggedValues="0" UseNameTab="0" Width="160" X="720" Y="155" ZOrder="8">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="160" X="720" Y="155"/>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
				</State2>
				<FinalState2 Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="1" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="20" Id="0SZPpYWFYC1QOhVV" MetaModelElement="sSZPpYWFYC1QOhVW" Model="sSZPpYWFYC1QOhVW" ModelElementNameAlignment="9" Name="123" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="20" X="802" Y="277" ZOrder="2">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="39" X="792" Y="297"/>
					<FillColor Color="rgb(0, 0, 0)" Style="1" Transparency="0" Type="1"/>
				</FinalState2>
			</Shapes>
			<Connectors>
				<Transition2 Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" Foreground="rgb(0, 0, 0)" From="chsgjVHxPxO3hONX" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="100" Id="OyUdXBsxeX4VQ2gu" MetaModelElement="GYV3VsjjT421VoT9" Model="GYV3VsjjT421VoT9" ModelElementNameAlignment="9" Name="Chọn bàn, hệ thống chuẩn bị hóa đơn" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" ShowOperation="0" ShowOperationParameter="0" To="bpsgN4m6AsDdAhKZ" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="313" X="18" Y="130" ZOrder="10">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="232" X="59" Y="158"/>
					<Points>
						<Point X="68.0" Y="180.0"/>
						<Point X="281.0" Y="180.0"/>
					</Points>
				</Transition2>
				<Transition2 Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" Foreground="rgb(0, 0, 0)" From="bpsgN4m6AsDdAhKZ" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="100" Id="UtmIhPPOqLdfp5vz" MetaModelElement="RnvwW3wTVXTYIlSr" Model="RnvwW3wTVXTYIlSr" ModelElementNameAlignment="9" Name="Bấm Lưu [có ít nhất một món], lưu thành công" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" ShowOperation="0" ShowOperationParameter="0" To="noGydrahGBBLoHya" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="337" X="432" Y="130" ZOrder="12">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="289" X="456" Y="158"/>
					<Points>
						<Point X="482.0" Y="180.0"/>
						<Point X="719.0" Y="180.0"/>
					</Points>
				</Transition2>
				<Transition2 Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" Foreground="rgb(0, 0, 0)" From="noGydrahGBBLoHya" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="165" Id="ubuhOoWGAqCOCBAm" MetaModelElement="sbuhOoWGAqCOCBAl" Model="sbuhOoWGAqCOCBAl" ModelElementNameAlignment="9" Name="Gọi thêm món, lưu thay đổi, gửi lại phiếu bếp" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" ShowOperation="0" ShowOperationParameter="0" To="noGydrahGBBLoHya" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="210" X="760" Y="65" ZOrder="14">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="241" X="745" Y="99"/>
					<Points>
						<Point X="810.0" Y="154.0"/>
						<Point X="810.0" Y="115.0"/>
						<Point X="920.0" Y="115.0"/>
						<Point X="920.0" Y="180.0"/>
						<Point X="880.0" Y="180.0"/>
					</Points>
				</Transition2>
				<Transition2 Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" Foreground="rgb(0, 0, 0)" From="noGydrahGBBLoHya" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="173" Id="wjVPpYWFYC1QOhV2" MetaModelElement="XDVPpYWFYC1QOhV1" Model="XDVPpYWFYC1QOhV1" ModelElementNameAlignment="9" Name="fdmvk" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" ShowOperation="0" ShowOperationParameter="0" To="0SZPpYWFYC1QOhVV" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="100" X="762" Y="155" ZOrder="16">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="50" X="813" Y="234"/>
					<Points>
						<Point X="812.0" Y="205.0"/>
						<Point X="812.0" Y="278.0"/>
					</Points>
				</Transition2>
			</Connectors>
		</StateDiagram>
	</Diagrams>
</Project>
```

</details>

### `references/real-samples/activity_diagram.xml`

<details>
<summary>Mở nội dung tệp</summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Project Author="SinhVien" CommentTableSortAscending="false" CommentTableSortColumn="Date Time" Description="&lt;html&gt;&#13;&#10;  &lt;head&gt;&#13;&#10;    &lt;style type=&quot;text/css&quot;&gt;&#10;      &lt;!--&#10;        body { color: #000000; font-family: Dialog; font-size: 12px }&#10;      --&gt;&#10;    &lt;/style&gt;&#13;&#10;    &#13;&#10;  &lt;/head&gt;&#13;&#10;  &lt;body&gt;&#13;&#10;  &lt;/body&gt;&#13;&#10;&lt;/html&gt;&#13;&#10;" DocumentationType="html" ExportedFromDifferentName="false" ExporterVersion="16.1.1" Name="btl2" TextualAnalysisHighlightOptionCaseSensitive="false" UmlVersion="2.x" Xml_structure="simple">
	<ProjectInfo>
		<LogicalView/>
		<ProjectOptions>
			<DiagramOptions ActivityDiagramControlFlowDisplayOption="\u0000" ActivityDiagramShowActionCallBehaviorOption="\u0000" ActivityDiagramShowActivityEdgeWeight="true" ActivityDiagramShowDiagramFrame="true" ActivityDiagramShowObjectNodeType="true" ActivityDiagramShowPartitionHandle="\u0000" AddDataStoresExtEntitiesToDecomposedDFD="\u0002" AlignColumnProperties="true" AllowConfigShowInOutFlowButtonsInDataFlowDiagram="false" AutoGenerateRoleName="false" AutoSetAttributeType="true" AutoSetColumnType="true" AutoSyncRoleName="true" BlockDefinitionDiagramShowDiagramFrame="true" BpPoolLaneDefaultOrientation="\u0000" BpdAutoStretchPools="true" BpdConnectGatewayWithFlowObjectInDifferentPool="\u0000" BpdDefaultConnectionPointStyle="\u0001" BpdDefaultConnectorStyle="\u0005" BpdDhowIdOption="\u0000" BpdShowActivitiesTypeIcon="true" BusinessProcessDiagramDefaultLanguage="English" ClassVisibilityStyle="\u0001" ConnectorLabelOrientation="\u0000" CreateOneMessagePerDirection="true" DecisionMergeNodeConnectionPointStyle="\u0000" DefaultAssociationEndNavigable="\u0001" DefaultAssociationEndVisibility="\u0000" DefaultAssociationShowFromMultiplicity="true" DefaultAssociationShowFromRoleName="true" DefaultAssociationShowFromRoleVisibility="true" DefaultAssociationShowStereotypes="true" DefaultAssociationShowToMultiplicity="true" DefaultAssociationShowToRoleName="true" DefaultAssociationShowToRoleVisibility="true" DefaultAttributeMultiplicity="false" DefaultAttributeType="" DefaultAttributeVisibility="\u0001" DefaultClassAttributeMultiplicity="" DefaultClassAttributeMultiplicityOrdered="false" DefaultClassAttributeMultiplicityUnique="true" DefaultClassInterfaceBall="false" DefaultClassVisibility="\u0004" DefaultColumnType="integer(10)" DefaultConnectionPointStyle="\u0000" DefaultConnectorStyle="\u0001" DefaultDiagramBackground="rgb(255, 255, 255)" DefaultDisplayAsRobustnessAnalysisIcon="true" DefaultDisplayAsRobustnessAnalysisIconInSequenceDiagram="true" DefaultDisplayAsStereotypeIcon="false" DefaultFontColor="rgb(0, 0, 0)" DefaultGenDiagramTypeFromScenario="\u0000" DefaultHtmlDocFontColor="rgb(0, 0, 0)" DefaultLineJumps="\u0000" DefaultOperationVisibility="\u0004" DefaultParameterDirection="\u0002" DefaultShowAttributeInitialValue="true" DefaultShowAttributeOption="\u0001" DefaultShowClassMemberStereotype="true" DefaultShowDirection="false" DefaultShowMultiplicityConstraints="false" DefaultShowOperationOption="\u0001" DefaultShowOperationSignature="true" DefaultShowOrderedMultiplicityConstraint="true" DefaultShowOwnedAssociationEndAsAttribute="true" DefaultShowOwner="false" DefaultShowOwnerSkipModelInFullyQualifiedOwnerSignature="true" DefaultShowReceptionOption="\u0001" DefaultShowTemplateParameter="true" DefaultShowTypeOption="\u0001" DefaultShowUniqueMultiplicityConstraint="true" DefaultTypeOfSubProcess="\u0000" DefaultWrapClassMember="false" DrawTextAnnotationOpenRectangleFollowConnectorEnd="true" EnableMinimumSize="true" EntityColumnConstraintsPresentation="\u0002" ErdIndexNumOfDigits="-1" ErdIndexPattern="{table_name}" ErdIndexPatternSyncAutomatically="true" ErdManyToManyJoinTableDelimiter="_" EtlTableDiagramFontSize="14" ExpandedSubProcessDiagramContent="\u0001" ForeignKeyArrowHeadSize="\u0002" ForeignKeyConnectorEndPointAssociatedColumn="false" ForeignKeyNamePattern="{reference_table_name}{reference_column_name}" ForeignKeyNamePatternCaseHandling="0" ForeignKeyRelationshipPattern="{association_name}" FractionalMetrics="true" GeneralizationSetNotation="\u0001" GraphicAntiAliasing="true" GridDiagramFontSize="14" InteractionDiagramShowDiagramFrame="true" InternalBlockDiagramShowDiagramFrame="true" LineJumpSize="\u0000" ModelElementNameAlignment="\u0004" MultipleLineClassName="\u0001" PackageDiagramShowDiagramFrame="true" PaintConnectorThroughLabel="false" ParametricDiagramShowDiagramFrame="true" PointConnectorEndToCompartmentMember="true" PrimaryKeyConstraintPattern="" PrimaryKeyNamePattern="ID" RenameConstructorAfterRenameClass="\u0000" RenameExtensionPointToFollowExtendUseCase="\u0000" RequirementDiagramShowDiagramFrame="true" ShapeAutoFitSize="false" ShowActivationsInSequenceDiagram="true" ShowActivityStateNodeCaption="524287" ShowArtifactOption="\u0002" ShowAssociatedDiagramNameOfInteraction="false" ShowAssociationRoleStereotypes="true" ShowAttributeGetterSetter="false" ShowBSElementCode="true" ShowClassEmptyCompartments="false" ShowColumnDefaultValue="false" ShowColumnNullable="true" ShowColumnType="true" ShowColumnUniqueConstraintName="false" ShowColumnUserType="false" ShowComponentOption="\u0002" ShowExtraColumnProperties="true" ShowInOutFlowButtonsInDataFlowDiagram="false" ShowInOutFlowsInSubLevelDiagram="true" ShowMessageOperationSignatureForSequenceAndCommunicationDiagram="true" ShowMessageStereotypeInSequenceAndCommunicationDiagram="true" ShowNumberInCollaborationDiagram="true" ShowNumberInSequenceDiagram="true" ShowPackageNameStyle="\u0000" ShowParameterNameInOperationSignature="true" ShowRowGridLineWithinCompClassDiagram="false" ShowRowGridLineWithinCompERD="true" ShowRowGridLineWithinORMDiagram="true" ShowSchemaNameInERD="true" ShowTransitionTrigger="\u0000" ShowUseCaseExtensionPoint="true" ShowUseCaseID="false" SnapConnectorsAfterZoom="false" StateDiagramShowDiagramFrame="true" StateShowParametersOfInternalActivities="false" StateShowPrePostConditionAndBodyOfInternalActivities="true" StopTargetLifelineOnCreateDestroyMessage="\u0002" SupportHtmlTaggedValue="true" SupportMultipleLineAttribute="true" SuppressImpliedMultiplicityForAttributeAssociationEnd="false" SyncAssociationNameWithAssociationClass="\u0000" SyncAssociationRoleNameWithReferencedAttributeName="true" SyncDocOfInterfaceToSubClass="\u0000" TextAntiAliasing="true" TextualAnalysisGenerateRequirementTextOption="\u0001" TextualAnalysisHighlightOption="\u0000" UnnamedIndexPattern="{table_name}_{column_name}" UseCaseDiagramShowDiagramFrame="true" UseStateNameTab="false" WireflowDiagramDevice="0" WireflowDiagramShowActiveFlowLabel="true" WireflowDiagramTheme="0" WireflowDiagramWireflowShowPreview="true" WireflowDiagramWireflowShowScreenId="true">
				<DefaultHtmlDocFont Family="Dialog" Size="12" Style="0"/>
			</DiagramOptions>
			<GeneralOptions ConfirmSubLevelIdWithDot="true" QuickAddGlossaryTermParentModelId="default"/>
			<InstantReverseOptions CalculateGeneralizationAndRealization="false" CreateShapeForParentModelOfDraggedClassPackage="false" ReverseGetterSetter="\u0000" ReverseOperationImplementation="false" ShowPackageForNewDiagram="\u0001" ShowPackageOwner="\u0000"/>
			<ModelQualityOptions EnableModelQualityChecking="false"/>
			<ORMOptions AlterColumnUserType="true" DecimalPrecision="19" DecimalScale="0" ExportCommentToDatabase="true" FormattedSQL="false" GenerateAssociationWithAttribute="false" GenerateDiagramFromORMWizards="true" GetterSetterVisibility="\u0000" IdGeneratorType="native" MappingFileColumnOrder="\u0000" NumericToClassType="\u0000" QuoteSQLIdentifier="\u0000" RecreateShapeWhenSync="false" SyncToClassDiagramAttributeName="\u0001" SyncToClassDiagramAttributeNamePrefix="" SyncToClassDiagramAttributeNameSuffix="" SyncToClassDiagramClassName="\u0000" SyncToClassDiagramClassNamePrefix="" SyncToClassDiagramClassNameSuffix="" SyncToERDColumnName="\u0000" SyncToERDColumnNamePrefix="" SyncToERDColumnNameSuffix="" SyncToERDTableName="\u0004" SyncToERDTableNamePrefix="" SyncToERDTableNameSuffix="" SynchronizeDefaultValueToColumn="false" SynchronizeName="\u0002" TablePerSubclassFKMapping="\u0000" UpperCaseSQL="true" UseDefaultDecimal="true" WrappingServletRequest="\u0001"/>
			<RequirementDiagramOptions DefaultWrapMember="true" ShowAttributes="\u0001" SupportHTMLAttribute="false"/>
			<StateCodeEngineOptions AutoCreateInitialStateInStateDiagram="true" AutoCreateTransitionMethods="true" DefaultInitialStateLocationX="-1" DefaultInitialStateLocationY="-1" GenerateDebugMessage="false" GenerateSample="true" GenerateTryCatch="true" Language="\u0000" RegenerateTransitionMethods="false" SyncTransitionMethods="true"/>
			<WarningOptions CreateORMClassInDefaultPackage="true"/>
			<PORepository>
				<POUserIDFormats>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAmy" LastNumericValue="0" ModelType="BPMNElement" Prefix="BP" Suffix=""/>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAmz" LastNumericValue="11" ModelType="Actor" Prefix="AC" Suffix=""/>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAm0" LastNumericValue="35" ModelType="UseCase" Prefix="UC" Suffix=""/>
					<POUserIDFormat Digits="3" Guid="false" Id="p01BOoWGAqCOCAm1" LastNumericValue="0" ModelType="Requirement" Prefix="REQ" Suffix=""/>
					<POUserIDFormat Digits="3" Guid="false" Id="p01BOoWGAqCOCAm2" LastNumericValue="0" ModelType="BusinessRule" Prefix="BR" Suffix=""/>
					<POUserIDFormat Digits="-1" Guid="false" Id="p01BOoWGAqCOCAm3" LastNumericValue="0" ModelType="BusinessProcessDiagram" Prefix="" Suffix=""/>
				</POUserIDFormats>
			</PORepository>
		</ProjectOptions>
	</ProjectInfo>
	<Models>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="9PVBOoWGAqCOCAXu" Name="boolean" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.312" PmLastModified="2026-10-21T10:30:48.325" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="HPVBOoWGAqCOCAXv" Name="byte" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.315" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXw" Name="char" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXx" Name="double" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXy" Name="float" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXz" Name="int" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.296" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX0" Name="long" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.313" PmLastModified="2026-10-21T10:30:48.323" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX1" Name="short" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.314" PmLastModified="2026-10-21T10:30:48.323" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX2" Name="void" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.314" PmLastModified="2026-10-21T10:30:48.323" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX3" Name="string" PmAuthor="phanb" PmCreateDateTime="2026-09-16T09:35:15.314" PmLastModified="2026-10-21T10:30:48.323" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<ActivityAction BacklogActivityId="0" Documentation_plain="" Effect_IsNull="true" Id="lCDupYWFYC1QOgwT" Leaf="false" MustIsolate="false" Name="Action" PmAuthor="phanb" PmCreateDateTime="2026-11-04T14:30:02.921" PmLastModified="2026-11-04T14:30:39.742" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
			<MasterView>
				<ActivityAction Idref="5CDupYWFYC1QOgwS" Name="Action"/>
			</MasterView>
		</ActivityAction>
		<ActivityAction BacklogActivityId="0" Documentation_plain="" Effect_IsNull="true" Id="iFTupYWFYC1QOgwj" Leaf="false" MustIsolate="false" Name="Action2" PmAuthor="phanb" PmCreateDateTime="2026-11-04T14:30:12.625" PmLastModified="2026-11-04T14:30:39.744" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
			<MasterView>
				<ActivityAction Idref="iFTupYWFYC1QOgwi" Name="Action2"/>
			</MasterView>
		</ActivityAction>
		<ObjectNode BacklogActivityId="0" ControlType="false" Documentation_plain="" Id="PILupYWFYC1QOgwu" Leaf="false" MustIsolate="false" Name="ObjectNode" OrderingKind="FIFO" PmAuthor="phanb" PmCreateDateTime="2026-11-04T14:30:18.556" PmLastModified="2026-11-04T14:30:39.746" QualityReason_IsNull="true" QualityScore="-1" TypeModifier="" UpperBound="" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
			<MasterView>
				<ObjectNode Idref="XILupYWFYC1QOgwt" Name="ObjectNode"/>
			</MasterView>
		</ObjectNode>
		<ExpansionRegion BacklogActivityId="0" Documentation_plain="" Id="GnLupYWFYC1QOgw6" Leaf="false" Mode="Iterative" MustIsolate="false" Name="Region" PmAuthor="phanb" PmCreateDateTime="2026-11-04T14:30:21.912" PmLastModified="2026-11-04T14:30:39.744" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
			<MasterView>
				<ExpansionRegion Idref="6nLupYWFYC1QOgw5" Name="Region"/>
			</MasterView>
		</ExpansionRegion>
		<ActivitySwimlane2 BacklogActivityId="0" Documentation_plain="" Id="XjbupYWFYC1QOgxD" Name="Swimlane" PmAuthor="phanb" PmCreateDateTime="2026-11-04T14:30:29.626" PmLastModified="2026-11-04T14:30:39.742" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
			<VerticalPartitions>
				<ActivityPartition Idref="6TbupYWFYC1QOgxH" Name="Partition"/>
				<ActivityPartition Idref="7TbupYWFYC1QOgxN" Name="Partition2"/>
			</VerticalPartitions>
			<MasterView>
				<ActivitySwimlane2 Idref="XjbupYWFYC1QOgxC" Name="Swimlane"/>
			</MasterView>
			<ModelChildren>
				<ActivityPartition BacklogActivityId="0" Documentation_plain="" Id="6TbupYWFYC1QOgxH" Name="Partition" PmAuthor="phanb" PmCreateDateTime="2026-11-04T14:30:29.655" PmLastModified="2026-11-04T14:30:39.730" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
					<MasterView>
						<ActivityPartitionHeader Idref="6TbupYWFYC1QOgxG" Name="Partition"/>
					</MasterView>
				</ActivityPartition>
				<ActivityPartition BacklogActivityId="0" Documentation_plain="" Id="7TbupYWFYC1QOgxN" Name="Partition2" PmAuthor="phanb" PmCreateDateTime="2026-11-04T14:30:29.687" PmLastModified="2026-11-04T14:30:39.744" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
					<MasterView>
						<ActivityPartitionHeader Idref="bTbupYWFYC1QOgxM" Name="Partition2"/>
					</MasterView>
				</ActivityPartition>
			</ModelChildren>
		</ActivitySwimlane2>
	</Models>
	<Diagrams>
		<ActivityDiagram AlignToGrid="false" AutoFitShapesSize="false" ConnectionPointStyle="0" ConnectorLabelOrientation="0" ConnectorLineJumps="0" ConnectorLineJumpsSize="0" ConnectorModelElementNameAlignment="4" ConnectorStyle="1" ControlFlowDisplayOption="0" DecisionMergeNodeConnectionPointStyle="1" DiagramBackground="rgb(255, 255, 255)" Editable="true" FilterByViewpointLegend="true" FollowDiagramParentElement="true" GridColor="rgb(192, 192, 192)" GridHeight="10" GridVisible="false" GridWidth="10" Height="598" HideConnectorIfFromToIsHidden="0" HideEmptyTaggedValues="false" Id="x11upYWFYC1QOgv2" ImageHeight="0" ImageScale="1.0" ImageWidth="0" InitializeDiagramForCreate="true" Maximized="true" ModelElementNameAlignment="4" Name="Activity Diagram1" ObjectNodeShowInStates="2" ObjectNodeShowType="true" PaintConnectorThroughLabel="1" PmAuthor="phanb" PmCreateDateTime="2026-11-04T14:29:44.163" PmLastModified="2026-11-04T14:30:29.712" PointConnectorEndToCompartmentMember="true" QualityScore="-1" RequestFitSizeWithPromptUser="false" RequestValidateSnapToGrid="false" ShapePresentationOption="0" ShowActionCallBehaviorOption="1" ShowActivityEdgeWeight="true" ShowActivityStateNodeCaption="524287" ShowAllocatedFrom="true" ShowAllocatedTo="true" ShowColorLegend="false" ShowConnectorLegend="false" ShowConnectorName="0" ShowConstraints="false" ShowDefaultPackage="false" ShowDiagramFrame="true" ShowInformationItemOption="2" ShowPMAuthor="false" ShowPMDifficulty="false" ShowPMDiscipline="false" ShowPMIteration="false" ShowPMPhase="false" ShowPMPriority="false" ShowPMStatus="false" ShowPMVersion="false" ShowPackageNameStyle="0" ShowPartitionHeader="0" ShowRelationshipConstraintExpression="false" ShowShapeLegend="false" ShowShapeStereotypeIconName="true" ShowStereotypes="true" ShowTaggedValues="false" TeamworkCreateDateTime="0" TrimmedHeight="0" TrimmedWidth="0" Width="1255" X="0" Y="0" ZoomRatio="1.0" _globalPaletteOption="true">
			<Shapes>
				<ActivityAction Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="40" Id="5CDupYWFYC1QOgwS" MetaModelElement="lCDupYWFYC1QOgwT" Model="lCDupYWFYC1QOgwT" ModelElementNameAlignment="9" Name="Action" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowCallBehaviorOption="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="60" X="233" Y="24" ZOrder="18">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="40" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="Center" Visible="true" Width="60" X="0" Y="0"/>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
				</ActivityAction>
				<ActivityAction Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="40" Id="iFTupYWFYC1QOgwi" MetaModelElement="iFTupYWFYC1QOgwj" Model="iFTupYWFYC1QOgwj" ModelElementNameAlignment="9" Name="Action2" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowCallBehaviorOption="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="60" X="121" Y="136" ZOrder="16">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="40" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="Center" Visible="true" Width="60" X="0" Y="0"/>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
				</ActivityAction>
				<ObjectNode Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="40" Id="XILupYWFYC1QOgwt" MetaModelElement="PILupYWFYC1QOgwu" Model="PILupYWFYC1QOgwu" ModelElementNameAlignment="9" Name="ObjectNode" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowConstraints="false" ShowInStates="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="80" X="232" Y="267" ZOrder="14">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="80" X="0" Y="0"/>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
				</ObjectNode>
				<ExpansionRegion Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="0" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="50" Id="6nLupYWFYC1QOgw5" MetaModelElement="GnLupYWFYC1QOgw6" Model="GnLupYWFYC1QOgw6" ModelElementNameAlignment="9" Name="Region" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="120" X="166" Y="382" ZOrder="12">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="120" X="0" Y="0"/>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
				</ExpansionRegion>
				<ActivitySwimlane2 Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="200" Id="XjbupYWFYC1QOgxC" MetaModelElement="XjbupYWFYC1QOgxD" Model="XjbupYWFYC1QOgxD" ModelElementNameAlignment="9" Name="Swimlane" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitPartitionHeadersHeight="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowStereotypeIconName="0" ShowTaggedValues="0" ValidatePartitionsForConvert="false" Width="200" X="556" Y="236" ZOrder="10">
					<VerticalPartitionIds>
						<Value Value="6TbupYWFYC1QOgxG"/>
						<Value Value="bTbupYWFYC1QOgxM"/>
					</VerticalPartitionIds>
					<CompartmentIds>
						<Value Value="jTbupYWFYC1QOgxK"/>
						<Value Value="kzbupYWFYC1QOgxQ"/>
					</CompartmentIds>
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="2.0">
						<Stroke/>
					</Line>
					<Caption Height="200" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="Invisible" Visible="false" Width="200" X="556" Y="236"/>
					<DiagramElementChildren>
						<ActivityPartitionHeader Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="15" Horizontal="false" Id="6TbupYWFYC1QOgxG" MetaModelElement="6TbupYWFYC1QOgxH" Model="6TbupYWFYC1QOgxH" ModelElementNameAlignment="9" Name="Partition" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="100" X="556" Y="236" ZOrder="8">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="2.0">
								<Stroke/>
							</Line>
							<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="InsideNorth" Visible="true" Width="100" X="0" Y="0"/>
							<FillColor Color="rgba(255, 255, 255, 0.0)" Style="1" Transparency="100" Type="1"/>
						</ActivityPartitionHeader>
						<ActivitySwimlane2Compartment Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="185" Id="jTbupYWFYC1QOgxK" ModelElementNameAlignment="9" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowStereotypeIconName="0" ShowTaggedValues="0" VerticalPartitionId="6TbupYWFYC1QOgxG" Width="100" X="556" Y="251" ZOrder="6">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="2.0">
								<Stroke/>
							</Line>
							<Caption Height="185" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="Center" Visible="true" Width="100" X="0" Y="0"/>
							<FillColor Color="rgba(255, 255, 255, 0.0)" Style="1" Transparency="100" Type="1"/>
						</ActivitySwimlane2Compartment>
						<ActivityPartitionHeader Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="15" Horizontal="false" Id="bTbupYWFYC1QOgxM" MetaModelElement="7TbupYWFYC1QOgxN" Model="7TbupYWFYC1QOgxN" ModelElementNameAlignment="9" Name="Partition2" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="100" X="656" Y="236" ZOrder="4">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="2.0">
								<Stroke/>
							</Line>
							<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="InsideNorth" Visible="true" Width="100" X="0" Y="0"/>
							<FillColor Color="rgba(255, 255, 255, 0.0)" Style="1" Transparency="100" Type="1"/>
						</ActivityPartitionHeader>
						<ActivitySwimlane2Compartment Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="185" Id="kzbupYWFYC1QOgxQ" ModelElementNameAlignment="9" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowStereotypeIconName="0" ShowTaggedValues="0" VerticalPartitionId="bTbupYWFYC1QOgxM" Width="100" X="656" Y="251" ZOrder="2">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="2.0">
								<Stroke/>
							</Line>
							<Caption Height="185" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="Center" Visible="true" Width="100" X="0" Y="0"/>
							<FillColor Color="rgba(255, 255, 255, 0.0)" Style="1" Transparency="100" Type="1"/>
						</ActivitySwimlane2Compartment>
					</DiagramElementChildren>
					<FillColor Color="rgba(255, 255, 255, 0.0)" Style="1" Transparency="100" Type="1"/>
				</ActivitySwimlane2>
			</Shapes>
		</ActivityDiagram>
	</Diagrams>
</Project>
```

</details>

### `references/real-samples/deployment_diagram.xml`

<details>
<summary>Mở nội dung tệp</summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Project Author="SinhVien" CommentTableSortAscending="false" CommentTableSortColumn="Date Time" Description="&lt;html&gt;&#13;&#10;  &lt;head&gt;&#13;&#10;    &lt;style type=&quot;text/css&quot;&gt;&#10;      &lt;!--&#10;        body { color: #000000; font-family: Dialog; font-size: 12px }&#10;      --&gt;&#10;    &lt;/style&gt;&#13;&#10;    &#13;&#10;  &lt;/head&gt;&#13;&#10;  &lt;body&gt;&#13;&#10;  &lt;/body&gt;&#13;&#10;&lt;/html&gt;&#13;&#10;" DocumentationType="html" ExportedFromDifferentName="false" ExporterVersion="16.1.1" Name="btl2" TextualAnalysisHighlightOptionCaseSensitive="false" UmlVersion="2.x" Xml_structure="simple">
	<ProjectInfo>
		<OrmInfo DefaultDatabase="1" SupportDatabases="0"/>
		<LogicalView/>
		<ProjectOptions>
			<DiagramOptions ActivityDiagramControlFlowDisplayOption="\u0000" ActivityDiagramShowActionCallBehaviorOption="\u0000" ActivityDiagramShowActivityEdgeWeight="true" ActivityDiagramShowDiagramFrame="true" ActivityDiagramShowObjectNodeType="true" ActivityDiagramShowPartitionHandle="\u0000" AddDataStoresExtEntitiesToDecomposedDFD="\u0002" AlignColumnProperties="true" AllowConfigShowInOutFlowButtonsInDataFlowDiagram="false" AutoGenerateRoleName="false" AutoSetAttributeType="true" AutoSetColumnType="true" AutoSyncRoleName="true" BlockDefinitionDiagramShowDiagramFrame="true" BpPoolLaneDefaultOrientation="\u0000" BpdAutoStretchPools="true" BpdConnectGatewayWithFlowObjectInDifferentPool="\u0000" BpdDefaultConnectionPointStyle="\u0001" BpdDefaultConnectorStyle="\u0005" BpdDhowIdOption="\u0000" BpdShowActivitiesTypeIcon="true" BusinessProcessDiagramDefaultLanguage="English" ClassVisibilityStyle="\u0001" ConnectorLabelOrientation="\u0000" CreateOneMessagePerDirection="true" DecisionMergeNodeConnectionPointStyle="\u0000" DefaultAssociationEndNavigable="\u0001" DefaultAssociationEndVisibility="\u0000" DefaultAssociationShowFromMultiplicity="true" DefaultAssociationShowFromRoleName="true" DefaultAssociationShowFromRoleVisibility="true" DefaultAssociationShowStereotypes="true" DefaultAssociationShowToMultiplicity="true" DefaultAssociationShowToRoleName="true" DefaultAssociationShowToRoleVisibility="true" DefaultAttributeMultiplicity="false" DefaultAttributeType="" DefaultAttributeVisibility="\u0001" DefaultClassAttributeMultiplicity="" DefaultClassAttributeMultiplicityOrdered="false" DefaultClassAttributeMultiplicityUnique="true" DefaultClassInterfaceBall="false" DefaultClassVisibility="\u0004" DefaultColumnType="integer(10)" DefaultConnectionPointStyle="\u0000" DefaultConnectorStyle="\u0001" DefaultDiagramBackground="rgb(255, 255, 255)" DefaultDisplayAsRobustnessAnalysisIcon="true" DefaultDisplayAsRobustnessAnalysisIconInSequenceDiagram="true" DefaultDisplayAsStereotypeIcon="false" DefaultFontColor="rgb(0, 0, 0)" DefaultGenDiagramTypeFromScenario="\u0000" DefaultHtmlDocFontColor="rgb(0, 0, 0)" DefaultLineJumps="\u0000" DefaultOperationVisibility="\u0004" DefaultParameterDirection="\u0002" DefaultShowAttributeInitialValue="true" DefaultShowAttributeOption="\u0001" DefaultShowClassMemberStereotype="true" DefaultShowDirection="false" DefaultShowMultiplicityConstraints="false" DefaultShowOperationOption="\u0001" DefaultShowOperationSignature="true" DefaultShowOrderedMultiplicityConstraint="true" DefaultShowOwnedAssociationEndAsAttribute="true" DefaultShowOwner="false" DefaultShowOwnerSkipModelInFullyQualifiedOwnerSignature="true" DefaultShowReceptionOption="\u0001" DefaultShowTemplateParameter="true" DefaultShowTypeOption="\u0001" DefaultShowUniqueMultiplicityConstraint="true" DefaultTypeOfSubProcess="\u0000" DefaultWrapClassMember="false" DrawTextAnnotationOpenRectangleFollowConnectorEnd="true" EnableMinimumSize="true" EntityColumnConstraintsPresentation="\u0002" ErdIndexNumOfDigits="-1" ErdIndexPattern="{table_name}" ErdIndexPatternSyncAutomatically="true" ErdManyToManyJoinTableDelimiter="_" EtlTableDiagramFontSize="14" ExpandedSubProcessDiagramContent="\u0001" ForeignKeyArrowHeadSize="\u0002" ForeignKeyConnectorEndPointAssociatedColumn="false" ForeignKeyNamePattern="{reference_table_name}{reference_column_name}" ForeignKeyNamePatternCaseHandling="0" ForeignKeyRelationshipPattern="{association_name}" FractionalMetrics="true" GeneralizationSetNotation="\u0001" GraphicAntiAliasing="true" GridDiagramFontSize="14" InteractionDiagramShowDiagramFrame="true" InternalBlockDiagramShowDiagramFrame="true" LineJumpSize="\u0000" ModelElementNameAlignment="\u0004" MultipleLineClassName="\u0001" PackageDiagramShowDiagramFrame="true" PaintConnectorThroughLabel="false" ParametricDiagramShowDiagramFrame="true" PointConnectorEndToCompartmentMember="true" PrimaryKeyConstraintPattern="" PrimaryKeyNamePattern="ID" RenameConstructorAfterRenameClass="\u0000" RenameExtensionPointToFollowExtendUseCase="\u0000" RequirementDiagramShowDiagramFrame="true" ShapeAutoFitSize="false" ShowActivationsInSequenceDiagram="true" ShowActivityStateNodeCaption="524287" ShowArtifactOption="\u0002" ShowAssociatedDiagramNameOfInteraction="false" ShowAssociationRoleStereotypes="true" ShowAttributeGetterSetter="false" ShowBSElementCode="true" ShowClassEmptyCompartments="false" ShowColumnDefaultValue="false" ShowColumnNullable="true" ShowColumnType="true" ShowColumnUniqueConstraintName="false" ShowColumnUserType="false" ShowComponentOption="\u0002" ShowExtraColumnProperties="true" ShowInOutFlowButtonsInDataFlowDiagram="false" ShowInOutFlowsInSubLevelDiagram="true" ShowMessageOperationSignatureForSequenceAndCommunicationDiagram="true" ShowMessageStereotypeInSequenceAndCommunicationDiagram="true" ShowNumberInCollaborationDiagram="true" ShowNumberInSequenceDiagram="true" ShowPackageNameStyle="\u0000" ShowParameterNameInOperationSignature="true" ShowRowGridLineWithinCompClassDiagram="false" ShowRowGridLineWithinCompERD="true" ShowRowGridLineWithinORMDiagram="true" ShowSchemaNameInERD="true" ShowTransitionTrigger="\u0000" ShowUseCaseExtensionPoint="true" ShowUseCaseID="false" SnapConnectorsAfterZoom="false" StateDiagramShowDiagramFrame="true" StateShowParametersOfInternalActivities="false" StateShowPrePostConditionAndBodyOfInternalActivities="true" StopTargetLifelineOnCreateDestroyMessage="\u0002" SupportHtmlTaggedValue="true" SupportMultipleLineAttribute="true" SuppressImpliedMultiplicityForAttributeAssociationEnd="false" SyncAssociationNameWithAssociationClass="\u0000" SyncAssociationRoleNameWithReferencedAttributeName="true" SyncDocOfInterfaceToSubClass="\u0000" TextAntiAliasing="true" TextualAnalysisGenerateRequirementTextOption="\u0001" TextualAnalysisHighlightOption="\u0000" UnnamedIndexPattern="{table_name}_{column_name}" UseCaseDiagramShowDiagramFrame="true" UseStateNameTab="false" WireflowDiagramDevice="0" WireflowDiagramShowActiveFlowLabel="true" WireflowDiagramTheme="0" WireflowDiagramWireflowShowPreview="true" WireflowDiagramWireflowShowScreenId="true">
				<DefaultHtmlDocFont Family="Dialog" Size="12" Style="0"/>
			</DiagramOptions>
			<GeneralOptions ConfirmSubLevelIdWithDot="true" QuickAddGlossaryTermParentModelId="default"/>
			<InstantReverseOptions CalculateGeneralizationAndRealization="false" CreateShapeForParentModelOfDraggedClassPackage="false" ReverseGetterSetter="\u0000" ReverseOperationImplementation="false" ShowPackageForNewDiagram="\u0001" ShowPackageOwner="\u0000"/>
			<ModelQualityOptions EnableModelQualityChecking="false"/>
			<ORMOptions AlterColumnUserType="true" DecimalPrecision="19" DecimalScale="0" ExportCommentToDatabase="true" FormattedSQL="false" GenerateAssociationWithAttribute="false" GenerateDiagramFromORMWizards="true" GetterSetterVisibility="\u0000" IdGeneratorType="native" MappingFileColumnOrder="\u0000" NumericToClassType="\u0000" QuoteSQLIdentifier="\u0000" RecreateShapeWhenSync="false" SyncToClassDiagramAttributeName="\u0001" SyncToClassDiagramAttributeNamePrefix="" SyncToClassDiagramAttributeNameSuffix="" SyncToClassDiagramClassName="\u0000" SyncToClassDiagramClassNamePrefix="" SyncToClassDiagramClassNameSuffix="" SyncToERDColumnName="\u0000" SyncToERDColumnNamePrefix="" SyncToERDColumnNameSuffix="" SyncToERDTableName="\u0004" SyncToERDTableNamePrefix="" SyncToERDTableNameSuffix="" SynchronizeDefaultValueToColumn="false" SynchronizeName="\u0002" TablePerSubclassFKMapping="\u0000" UpperCaseSQL="true" UseDefaultDecimal="true" WrappingServletRequest="\u0001"/>
			<RequirementDiagramOptions DefaultWrapMember="true" ShowAttributes="\u0001" SupportHTMLAttribute="false"/>
			<StateCodeEngineOptions AutoCreateInitialStateInStateDiagram="true" AutoCreateTransitionMethods="true" DefaultInitialStateLocationX="-1" DefaultInitialStateLocationY="-1" GenerateDebugMessage="false" GenerateSample="true" GenerateTryCatch="true" Language="\u0000" RegenerateTransitionMethods="false" SyncTransitionMethods="true"/>
			<WarningOptions CreateORMClassInDefaultPackage="true"/>
			<PORepository>
				<POUserIDFormats>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAmy" LastNumericValue="0" ModelType="BPMNElement" Prefix="BP" Suffix=""/>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAmz" LastNumericValue="11" ModelType="Actor" Prefix="AC" Suffix=""/>
					<POUserIDFormat Digits="2" Guid="false" Id="p01BOoWGAqCOCAm0" LastNumericValue="35" ModelType="UseCase" Prefix="UC" Suffix=""/>
					<POUserIDFormat Digits="3" Guid="false" Id="p01BOoWGAqCOCAm1" LastNumericValue="0" ModelType="Requirement" Prefix="REQ" Suffix=""/>
					<POUserIDFormat Digits="3" Guid="false" Id="p01BOoWGAqCOCAm2" LastNumericValue="0" ModelType="BusinessRule" Prefix="BR" Suffix=""/>
					<POUserIDFormat Digits="-1" Guid="false" Id="p01BOoWGAqCOCAm3" LastNumericValue="0" ModelType="BusinessProcessDiagram" Prefix="" Suffix=""/>
				</POUserIDFormats>
			</PORepository>
		</ProjectOptions>
	</ProjectInfo>
	<Models>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="9PVBOoWGAqCOCAXu" Name="boolean" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.441" PmLastModified="2017-06-22T15:44:54.371" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="HPVBOoWGAqCOCAXv" Name="byte" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.443" PmLastModified="2017-06-22T15:44:54.427" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXw" Name="char" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.443" PmLastModified="2017-06-22T15:44:54.427" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXx" Name="double" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.444" PmLastModified="2017-06-22T15:44:54.446" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXy" Name="float" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.444" PmLastModified="2017-06-22T15:44:54.445" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="XPVBOoWGAqCOCAXz" Name="int" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.445" PmLastModified="2017-06-22T15:44:54.399" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX0" Name="long" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.445" PmLastModified="2017-06-22T15:44:54.399" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX1" Name="short" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.446" PmLastModified="2017-06-22T15:44:54.327" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX2" Name="void" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.446" PmLastModified="2017-06-22T15:44:54.326" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<DataType BacklogActivityId="0" Documentation_plain="" Id="PPVBOoWGAqCOCAX3" Name="string" PmAuthor="" PmCreateDateTime="2017-06-21T18:09:47.446" PmLastModified="2017-06-22T15:44:54.325" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<ModelRelationshipContainer BacklogActivityId="0" Documentation_plain="" Id="DoBBLFK3EBJFH71i" Name="relationships" PmAuthor="SinhVien" PmCreateDateTime="2026-10-14T10:00:00.000" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
			<ModelChildren>
				<ModelRelationshipContainer BacklogActivityId="0" Documentation_plain="" Id="zmXENBqSy1UzRawa" Name="Association" PmAuthor="SinhVien" PmCreateDateTime="2026-10-20T10:00:00.000" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
					<ModelChildren>
						<Association Abstract="false" BacklogActivityId="0" Derived="false" Direction="From To" Documentation_plain="" EndRelationshipFromMetaModelElement="KWjRk4WFYCyCBxNV" EndRelationshipToMetaModelElement="KWjRk4WFYCyCBxNR" FinalSpecialization="false" Id="KWjRk4WFYCyCBxNZ" Leaf="false" Name="TCP/IP" OrderingInProfile="-1" PmAuthor="" PmCreateDateTime="2017-06-22T09:48:09.621" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<FromEnd>
								<AssociationEnd AggregationKind="None" BacklogActivityId="0" ConnectToCodeModel="1" DefaultValue_IsNull="true" Derived="false" DerivedUnion="false" Documentation_plain="" EndModelElement="KWjRk4WFYCyCBxNV" Id="JWjRk4WFYCyCBxNe" JavaCodeAttributeName="" Leaf="false" Multiplicity="Unspecified" Navigable="Navigable" PmAuthor="" PmCreateDateTime="2017-06-22T09:48:09.621" PmLastModified_IsNull="true" ProvidePropertyGetterMethod="false" ProvidePropertySetterMethod="false" QualityReason_IsNull="true" QualityScore="-1" ReadOnly="false" Static="false" TypeModifier="" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
									<Qualifier>
										<Qualifier BacklogActivityId="0" Documentation_plain="" Id="JWjRk4WFYCyCBxNg" Name="" PmAuthor="" PmCreateDateTime="2017-06-22T09:48:09.621" PmLastModified_IsNull="true" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
									</Qualifier>
									<Type>
										<Node Idref="KWjRk4WFYCyCBxNV" Name="PC"/>
									</Type>
								</AssociationEnd>
							</FromEnd>
							<ToEnd>
								<AssociationEnd AggregationKind="None" BacklogActivityId="0" ConnectToCodeModel="1" DefaultValue_IsNull="true" Derived="false" DerivedUnion="false" Documentation_plain="" EndModelElement="KWjRk4WFYCyCBxNR" Id="JWjRk4WFYCyCBxNh" JavaCodeAttributeName="" Leaf="false" Multiplicity="Unspecified" Navigable="Navigable" PmAuthor="" PmCreateDateTime="2017-06-22T09:48:09.621" PmLastModified_IsNull="true" ProvidePropertyGetterMethod="false" ProvidePropertySetterMethod="false" QualityReason_IsNull="true" QualityScore="-1" ReadOnly="false" Static="false" TypeModifier="" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
									<Qualifier>
										<Qualifier BacklogActivityId="0" Documentation_plain="" Id="JWjRk4WFYCyCBxNj" Name="" PmAuthor="" PmCreateDateTime="2017-06-22T09:48:09.621" PmLastModified_IsNull="true" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
									</Qualifier>
									<Type>
										<Node Idref="KWjRk4WFYCyCBxNR" Name="Real Estate Server"/>
									</Type>
								</AssociationEnd>
							</ToEnd>
							<MasterView>
								<Association Idref="v2jRk4WFYCyCBxOa" Name="TCP/IP"/>
							</MasterView>
						</Association>
						<Association Abstract="false" BacklogActivityId="0" Derived="false" Direction="From To" Documentation_plain="" EndRelationshipFromMetaModelElement="KWjRk4WFYCyCBxNV" EndRelationshipToMetaModelElement="LmjRk4WFYCyCBxNK" FinalSpecialization="false" Id="JWjRk4WFYCyCBxNk" Leaf="false" Name="TCP/IP" OrderingInProfile="-1" PmAuthor="" PmCreateDateTime="2017-06-22T09:48:26.344" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<FromEnd>
								<AssociationEnd AggregationKind="None" BacklogActivityId="0" ConnectToCodeModel="1" DefaultValue_IsNull="true" Derived="false" DerivedUnion="false" Documentation_plain="" EndModelElement="KWjRk4WFYCyCBxNV" Id="JWjRk4WFYCyCBxNp" JavaCodeAttributeName="" Leaf="false" Multiplicity="Unspecified" Navigable="Navigable" PmAuthor="" PmCreateDateTime="2017-06-22T09:48:26.344" PmLastModified_IsNull="true" ProvidePropertyGetterMethod="false" ProvidePropertySetterMethod="false" QualityReason_IsNull="true" QualityScore="-1" ReadOnly="false" Static="false" TypeModifier="" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
									<Qualifier>
										<Qualifier BacklogActivityId="0" Documentation_plain="" Id="LWjRk4WFYCyCBxNr" Name="" PmAuthor="" PmCreateDateTime="2017-06-22T09:48:26.344" PmLastModified_IsNull="true" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
									</Qualifier>
									<Type>
										<Node Idref="KWjRk4WFYCyCBxNV" Name="PC"/>
									</Type>
								</AssociationEnd>
							</FromEnd>
							<ToEnd>
								<AssociationEnd AggregationKind="None" BacklogActivityId="0" ConnectToCodeModel="1" DefaultValue_IsNull="true" Derived="false" DerivedUnion="false" Documentation_plain="" EndModelElement="LmjRk4WFYCyCBxNK" Id="LWjRk4WFYCyCBxNs" JavaCodeAttributeName="" Leaf="false" Multiplicity="Unspecified" Navigable="Navigable" PmAuthor="" PmCreateDateTime="2017-06-22T09:48:26.344" PmLastModified_IsNull="true" ProvidePropertyGetterMethod="false" ProvidePropertySetterMethod="false" QualityReason_IsNull="true" QualityScore="-1" ReadOnly="false" Static="false" TypeModifier="" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
									<Qualifier>
										<Qualifier BacklogActivityId="0" Documentation_plain="" Id="LWjRk4WFYCyCBxNu" Name="" PmAuthor="" PmCreateDateTime="2017-06-22T09:48:26.344" PmLastModified_IsNull="true" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true"/>
									</Qualifier>
									<Type>
										<Node Idref="LmjRk4WFYCyCBxNK" Name="Bank Server"/>
									</Type>
								</AssociationEnd>
							</ToEnd>
							<MasterView>
								<Association Idref="v2jRk4WFYCyCBxOc" Name="TCP/IP"/>
							</MasterView>
						</Association>
					</ModelChildren>
				</ModelRelationshipContainer>
				<ModelRelationshipContainer BacklogActivityId="0" Documentation_plain="" Id="y2uRk4WFYCyCBxBn" Name="Dependency" PmAuthor="phanb" PmCreateDateTime="2026-11-11T14:36:56.275" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
					<ModelChildren>
						<Dependency BacklogActivityId="0" Documentation_plain="" From="wWjRk4WFYCyCBxNP" Id="g2jRk4WFYCyCBxN0" PmAuthor="" PmCreateDateTime="2017-06-22T09:43:03.149" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" To="wWjRk4WFYCyCBxNN" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Dependency Idref="n2jRk4WFYCyCBxOQ"/>
							</MasterView>
						</Dependency>
						<Dependency BacklogActivityId="0" Documentation_plain="" From="KWjRk4WFYCyCBxNT" Id="g2jRk4WFYCyCBxN1" PmAuthor="" PmCreateDateTime="2017-06-22T09:43:42.194" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" To="KWjRk4WFYCyCBxNS" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Dependency Idref="n2jRk4WFYCyCBxOS"/>
							</MasterView>
						</Dependency>
						<Dependency BacklogActivityId="0" Documentation_plain="" From="KWjRk4WFYCyCBxNW" Id="g2jRk4WFYCyCBxN2" PmAuthor="" PmCreateDateTime="2017-06-22T09:45:01.090" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" To="KWjRk4WFYCyCBxNQ" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Dependency Idref="32jRk4WFYCyCBxOW"/>
							</MasterView>
						</Dependency>
						<Dependency BacklogActivityId="0" Documentation_plain="" From="KWjRk4WFYCyCBxNW" Id="g2jRk4WFYCyCBxN3" PmAuthor="" PmCreateDateTime="2017-06-22T09:45:04.698" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" To="KWjRk4WFYCyCBxNU" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Dependency Idref="v2jRk4WFYCyCBxOY"/>
							</MasterView>
						</Dependency>
					</ModelChildren>
				</ModelRelationshipContainer>
				<ModelRelationshipContainer BacklogActivityId="0" Documentation_plain="" Id="BejRk4WFYCyCBxOe" Name="Realization" PmAuthor="phanb" PmCreateDateTime="2026-11-11T14:38:18.400" PmLastModified="2026-11-11T14:38:18.413" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true">
					<ModelChildren>
						<Realization BacklogActivityId="0" ConnectToCodeModel="1" Documentation_plain="" From="KWjRk4WFYCyCBxNQ" Id="_WjRk4WFYCyCBxNx" Mapping_IsNull="true" PmAuthor="" PmCreateDateTime="2017-06-22T09:42:49.077" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" To="wWjRk4WFYCyCBxNP" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Realization Idref="72jRk4WFYCyCBxOO"/>
							</MasterView>
						</Realization>
						<Realization BacklogActivityId="0" ConnectToCodeModel="1" Documentation_plain="" From="KWjRk4WFYCyCBxNU" Id="_WjRk4WFYCyCBxNy" Mapping_IsNull="true" PmAuthor="" PmCreateDateTime="2017-06-22T09:43:42.198" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" To="KWjRk4WFYCyCBxNT" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<MasterView>
								<Realization Idref="32jRk4WFYCyCBxOU"/>
							</MasterView>
						</Realization>
					</ModelChildren>
				</ModelRelationshipContainer>
			</ModelChildren>
		</ModelRelationshipContainer>
		<Stereotype Abstract="false" BacklogActivityId="0" BaseType="Class" Documentation_plain="" IconPath="" Id="JmjRk4WFYCyCBxNF" Leaf="false" Name="Interface" PmAuthor="" PmCreateDateTime="2017-06-21T18:14:22.656" PmLastModified="2026-11-11T14:38:18.411" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true"/>
		<Model Abstract="false" BacklogActivityId="0" ConnectToCodeModel="1" Documentation_plain="" Id="LmjRk4WFYCyCBxNH" Leaf="false" Name="Deployment Diagram - Mortgage Application" PmAuthor="" PmCreateDateTime="2017-06-22T09:41:02.072" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true">
			<SubDiagrams>
				<DeploymentDiagram Idref="42jRk4WFYCyCBxN4"/>
			</SubDiagrams>
			<ModelChildren>
				<Node Abstract="false" Active="false" BacklogActivityId="0" BusinessKeyMutable="true" BusinessModel="false" ConnectToCodeModel="1" Documentation_plain="" FinalSpecialization="false" Id="LmjRk4WFYCyCBxNK" Leaf="false" Name="Bank Server" PmAuthor="" PmCreateDateTime="2017-06-22T09:41:19.656" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
					<MasterView>
						<Node Idref="j2jRk4WFYCyCBxOI" Name="Bank Server"/>
					</MasterView>
					<ModelChildren>
						<Artifact Abstract="false" BacklogActivityId="0" Documentation_plain="" FileName_IsNull="true" FinalSpecialization="false" Id="wWjRk4WFYCyCBxNN" Leaf="false" Name="Customer DB" PmAuthor="" PmCreateDateTime="2017-06-22T09:41:50.692" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<ToSimpleRelationships>
								<Dependency Idref="g2jRk4WFYCyCBxN0" Name=""/>
							</ToSimpleRelationships>
							<MasterView>
								<Artifact Idref="r2jRk4WFYCyCBxOM" Name="Customer DB"/>
							</MasterView>
						</Artifact>
						<Component Abstract="false" Active="false" BacklogActivityId="0" BusinessKeyMutable="true" BusinessModel="false" ConnectToCodeModel="1" Documentation_plain="" FinalSpecialization="false" Id="wWjRk4WFYCyCBxNP" IndirectlyInstantiated="true" Leaf="false" Name="Mortgage Application" PmAuthor="" PmCreateDateTime="2017-06-22T09:42:27.054" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
							<FromSimpleRelationships>
								<Dependency Idref="g2jRk4WFYCyCBxN0" Name=""/>
							</FromSimpleRelationships>
							<ToSimpleRelationships>
								<Realization Idref="_WjRk4WFYCyCBxNx" Name=""/>
							</ToSimpleRelationships>
							<MasterView>
								<Component Idref="j2jRk4WFYCyCBxOK" Name="Mortgage Application"/>
							</MasterView>
						</Component>
					</ModelChildren>
				</Node>
				<Class Abstract="false" Active="false" BacklogActivityId="0" BusinessKeyMutable="true" BusinessModel="false" ConnectToCodeModel="1" Documentation_plain="" FinalSpecialization="false" Id="KWjRk4WFYCyCBxNQ" Leaf="false" Name="IMortgageApplication" PmAuthor="" PmCreateDateTime="2017-06-22T09:42:49.020" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
					<Stereotypes>
						<Stereotype Idref="JmjRk4WFYCyCBxNF" Name="Interface"/>
					</Stereotypes>
					<FromSimpleRelationships>
						<Realization Idref="_WjRk4WFYCyCBxNx" Name=""/>
					</FromSimpleRelationships>
					<ToSimpleRelationships>
						<Dependency Idref="g2jRk4WFYCyCBxN2" Name=""/>
					</ToSimpleRelationships>
					<MasterView>
						<StructuredInterface Idref="d2jRk4WFYCyCBxOG" Name="IMortgageApplication"/>
					</MasterView>
				</Class>
				<Node Abstract="false" Active="false" BacklogActivityId="0" BusinessKeyMutable="true" BusinessModel="false" ConnectToCodeModel="1" Documentation_plain="" FinalSpecialization="false" Id="KWjRk4WFYCyCBxNR" Leaf="false" Name="Real Estate Server" PmAuthor="" PmCreateDateTime="2017-06-22T09:43:42.139" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
					<MasterView>
						<Node Idref="l2jRk4WFYCyCBxOA" Name="Real Estate Server"/>
					</MasterView>
					<ModelChildren>
						<Artifact Abstract="false" BacklogActivityId="0" Documentation_plain="" FileName_IsNull="true" FinalSpecialization="false" Id="KWjRk4WFYCyCBxNS" Leaf="false" Name="Multiple Listings" PmAuthor="" PmCreateDateTime="2017-06-22T09:43:42.158" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="Unspecified">
							<ToSimpleRelationships>
								<Dependency Idref="g2jRk4WFYCyCBxN1" Name=""/>
							</ToSimpleRelationships>
							<MasterView>
								<Artifact Idref="12jRk4WFYCyCBxOE" Name="Multiple Listings"/>
							</MasterView>
						</Artifact>
						<Component Abstract="false" Active="false" BacklogActivityId="0" BusinessKeyMutable="true" BusinessModel="false" ConnectToCodeModel="1" Documentation_plain="" FinalSpecialization="false" Id="KWjRk4WFYCyCBxNT" IndirectlyInstantiated="true" Leaf="false" Name="Listing" PmAuthor="" PmCreateDateTime="2017-06-22T09:43:42.173" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
							<FromSimpleRelationships>
								<Dependency Idref="g2jRk4WFYCyCBxN1" Name=""/>
							</FromSimpleRelationships>
							<ToSimpleRelationships>
								<Realization Idref="_WjRk4WFYCyCBxNy" Name=""/>
							</ToSimpleRelationships>
							<MasterView>
								<Component Idref="12jRk4WFYCyCBxOC" Name="Listing"/>
							</MasterView>
						</Component>
					</ModelChildren>
				</Node>
				<Class Abstract="false" Active="false" BacklogActivityId="0" BusinessKeyMutable="true" BusinessModel="false" ConnectToCodeModel="1" Documentation_plain="" FinalSpecialization="false" Id="KWjRk4WFYCyCBxNU" Leaf="false" Name="ILIsting" PmAuthor="" PmCreateDateTime="2017-06-22T09:43:42.188" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
					<Stereotypes>
						<Stereotype Idref="JmjRk4WFYCyCBxNF" Name="Interface"/>
					</Stereotypes>
					<FromSimpleRelationships>
						<Realization Idref="_WjRk4WFYCyCBxNy" Name=""/>
					</FromSimpleRelationships>
					<ToSimpleRelationships>
						<Dependency Idref="g2jRk4WFYCyCBxN3" Name=""/>
					</ToSimpleRelationships>
					<MasterView>
						<StructuredInterface Idref="l2jRk4WFYCyCBxN." Name="ILIsting"/>
					</MasterView>
				</Class>
				<Node Abstract="false" Active="false" BacklogActivityId="0" BusinessKeyMutable="true" BusinessModel="false" ConnectToCodeModel="1" Documentation_plain="" FinalSpecialization="false" Id="KWjRk4WFYCyCBxNV" Leaf="false" Name="PC" PmAuthor="" PmCreateDateTime="2017-06-22T09:44:36.143" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
					<MasterView>
						<Node Idref="m2jRk4WFYCyCBxN6" Name="PC"/>
					</MasterView>
					<ModelChildren>
						<Component Abstract="false" Active="false" BacklogActivityId="0" BusinessKeyMutable="true" BusinessModel="false" ConnectToCodeModel="1" Documentation_plain="" FinalSpecialization="false" Id="KWjRk4WFYCyCBxNW" IndirectlyInstantiated="true" Leaf="false" Name="BuyerInterface" PmAuthor="" PmCreateDateTime="2017-06-22T09:44:36.173" PmLastModified="2026-11-11T14:38:18.400" QualityReason_IsNull="true" QualityScore="-1" Root="false" UserIDLastNumericValue="0" UserID_IsNull="true" Visibility="public">
							<FromSimpleRelationships>
								<Dependency Idref="g2jRk4WFYCyCBxN2" Name=""/>
								<Dependency Idref="g2jRk4WFYCyCBxN3" Name=""/>
							</FromSimpleRelationships>
							<MasterView>
								<Component Idref="p2jRk4WFYCyCBxN8" Name="BuyerInterface"/>
							</MasterView>
						</Component>
					</ModelChildren>
				</Node>
			</ModelChildren>
		</Model>
	</Models>
	<Diagrams>
		<DeploymentDiagram AlignToGrid="false" AutoFitShapesSize="false" ConnectionPointStyle="0" ConnectorLabelOrientation="0" ConnectorLineJumps="0" ConnectorLineJumpsSize="0" ConnectorModelElementNameAlignment="4" ConnectorStyle="1" DiagramBackground="rgb(255, 255, 255)" Editable="true" FilterByViewpointLegend="true" FollowDiagramParentElement="true" GridColor="rgb(192, 192, 192)" GridHeight="10" GridVisible="false" GridWidth="10" Height="598" HideConnectorIfFromToIsHidden="0" HideEmptyTaggedValues="false" Id="42jRk4WFYCyCBxN4" ImageHeight="0" ImageScale="1.0" ImageWidth="0" InitializeDiagramForCreate="true" Maximized="true" ModelElementNameAlignment="4" Name="Deployment Diagram with Components" PaintConnectorThroughLabel="1" ParentModel="LmjRk4WFYCyCBxNH" PmAuthor="" PmCreateDateTime="2017-06-22T09:41:16.300" PmLastModified="2017-06-22T15:44:54.591" PointConnectorEndToCompartmentMember="true" QualityScore="-1" RequestFitSizeWithPromptUser="false" RequestValidateSnapToGrid="false" ShapePresentationOption="0" ShowActivityStateNodeCaption="65535" ShowAllocatedFrom="true" ShowAllocatedTo="true" ShowColorLegend="false" ShowComponentAttributes="false" ShowComponentOperations="false" ShowConnectorLegend="false" ShowConnectorName="0" ShowConstraints="false" ShowDefaultPackage="false" ShowInformationItemOption="2" ShowNodeAttributes="false" ShowNodeOperations="false" ShowPMAuthor="false" ShowPMDifficulty="false" ShowPMDiscipline="false" ShowPMIteration="false" ShowPMPhase="false" ShowPMPriority="false" ShowPMStatus="false" ShowPMVersion="false" ShowPackageNameStyle="0" ShowPortMultiplicityOption="3" ShowRelationshipConstraintExpression="false" ShowShapeLegend="false" ShowShapeStereotypeIconName="true" ShowStereotypes="true" ShowTaggedValues="false" TeamworkAuthor="Jick Yeung" TeamworkCreateDateTime="1498117490289" TrimmedHeight="0" TrimmedWidth="0" Width="1255" X="0" Y="0" ZoomRatio="1.0" _globalPaletteOption="true" _showArtifactOption="2" _showComponentOption="2" documentation="&lt;html&gt;&#13;&#10;  &lt;head&gt;&#13;&#10;    &lt;style type=&quot;text/css&quot;&gt;&#10;      &lt;!--&#10;        body { color: #000000; font-family: Dialog; font-size: 12px }&#10;      --&gt;&#10;    &lt;/style&gt;&#13;&#10;    &#13;&#10;  &lt;/head&gt;&#13;&#10;  &lt;body&gt;&#13;&#10;    &lt;p&gt;&#13;&#10;      &#13;&#10;    &lt;/p&gt;&#13;&#10;  &lt;/body&gt;&#13;&#10;&lt;/html&gt;&#13;&#10;">
			<Shapes>
				<Node Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="94" Id="m2jRk4WFYCyCBxN6" MetaModelElement="KWjRk4WFYCyCBxNV" Model="KWjRk4WFYCyCBxNV" ModelElementNameAlignment="9" Name="PC" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowAttributesMode="0" ShowOperationsMode="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="177" X="312" Y="236" ZOrder="4">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="19" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="169" X="0" Y="8"/>
					<DiagramElementChildren>
						<Component Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" DisplayOption="0" Foreground="rgb(0, 0, 0)" Height="40" Id="p2jRk4WFYCyCBxN8" MetaModelElement="KWjRk4WFYCyCBxNW" Model="KWjRk4WFYCyCBxNW" ModelElementNameAlignment="1" Name="BuyerInterface" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowAttributesMode="0" ShowOperationsMode="0" ShowOption="-1" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="153" X="321" Y="274" ZOrder="2">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
								<Stroke/>
							</Line>
							<Caption Height="40" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="InsideNorth" Visible="true" Width="129" X="0" Y="0"/>
							<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
							<CompartmentFont Value="none"/>
						</Component>
					</DiagramElementChildren>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
					<CompartmentFont Value="none"/>
				</Node>
				<StructuredInterface Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="1" CoverConnector="false" DisplayOption="0" Foreground="rgb(0, 0, 0)" Height="20" Id="l2jRk4WFYCyCBxN." MetaModelElement="KWjRk4WFYCyCBxNU" Model="KWjRk4WFYCyCBxNU" ModelElementNameAlignment="9" Name="ILIsting" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="20" X="489" Y="141" ZOrder="6">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="60" X="509" Y="144"/>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
					<CompartmentFont Value="none"/>
				</StructuredInterface>
				<Node Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="169" Id="l2jRk4WFYCyCBxOA" MetaModelElement="KWjRk4WFYCyCBxNR" Model="KWjRk4WFYCyCBxNR" ModelElementNameAlignment="9" Name="Real Estate Server" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowAttributesMode="0" ShowOperationsMode="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="362" X="421" Y="29" ZOrder="12">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="19" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="354" X="0" Y="8"/>
					<DiagramElementChildren>
						<Component Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" DisplayOption="0" Foreground="rgb(0, 0, 0)" Height="40" Id="12jRk4WFYCyCBxOC" MetaModelElement="KWjRk4WFYCyCBxNT" Model="KWjRk4WFYCyCBxNT" ModelElementNameAlignment="1" Name="Listing" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowAttributesMode="0" ShowOperationsMode="0" ShowOption="-1" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="133" X="433" Y="73" ZOrder="8">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
								<Stroke/>
							</Line>
							<Caption Height="40" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="InsideNorth" Visible="true" Width="109" X="0" Y="0"/>
							<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
							<CompartmentFont Value="none"/>
						</Component>
						<Artifact Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="40" Id="12jRk4WFYCyCBxOE" MetaModelElement="KWjRk4WFYCyCBxNS" Model="KWjRk4WFYCyCBxNS" ModelElementNameAlignment="1" Name="Multiple Listings" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowOption="-1" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="136" X="622" Y="73" ZOrder="10">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
								<Stroke/>
							</Line>
							<Caption Height="40" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="112" X="0" Y="0"/>
							<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
						</Artifact>
					</DiagramElementChildren>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
					<CompartmentFont Value="none"/>
				</Node>
				<StructuredInterface Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="1" CoverConnector="false" CreatorDiagramType="DeploymentDiagram" DisplayOption="0" Foreground="rgb(0, 0, 0)" Height="20" Id="d2jRk4WFYCyCBxOG" MetaModelElement="KWjRk4WFYCyCBxNQ" Model="KWjRk4WFYCyCBxNQ" ModelElementNameAlignment="9" Name="IMortgageApplication" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="20" X="114" Y="141" ZOrder="14">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="133" X="134" Y="144"/>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
					<CompartmentFont Value="none"/>
				</StructuredInterface>
				<Node Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" Foreground="rgb(0, 0, 0)" Height="169" Id="j2jRk4WFYCyCBxOI" MetaModelElement="LmjRk4WFYCyCBxNK" Model="LmjRk4WFYCyCBxNK" ModelElementNameAlignment="9" Name="Bank Server" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowAttributesMode="0" ShowOperationsMode="0" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="362" X="34" Y="29" ZOrder="20">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="19" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="354" X="0" Y="8"/>
					<DiagramElementChildren>
						<Component Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" CreatorDiagramType="DeploymentDiagram" DisplayOption="0" Foreground="rgb(0, 0, 0)" Height="40" Id="j2jRk4WFYCyCBxOK" MetaModelElement="wWjRk4WFYCyCBxNP" Model="wWjRk4WFYCyCBxNP" ModelElementNameAlignment="1" Name="Mortgage Application" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowAttributesMode="0" ShowOperationsMode="0" ShowOption="-1" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="153" X="48" Y="73" ZOrder="16">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
								<Stroke/>
							</Line>
							<Caption Height="40" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="InsideNorth" Visible="true" Width="129" X="0" Y="0"/>
							<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
							<CompartmentFont Value="none"/>
						</Component>
						<Artifact Background="rgb(122, 207, 245)" ConnectToPoint="true" ConnectionPointType="2" CoverConnector="false" CreatorDiagramType="DeploymentDiagram" Foreground="rgb(0, 0, 0)" Height="40" Id="r2jRk4WFYCyCBxOM" MetaModelElement="wWjRk4WFYCyCBxNN" Model="wWjRk4WFYCyCBxNN" ModelElementNameAlignment="1" Name="Customer DB" OverrideAppearanceWithStereotypeIcon="true" ParentConnectorDTheta="0.0" ParentConnectorHeaderLength="40" ParentConnectorLineLength="10" PresentationOption="4" PrimitiveShapeType="0" RequestDefaultSize="false" RequestFitSize="false" RequestFitSizeFromCenter="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" RequestSetSizeOption="0" Selectable="true" ShowAllocatedFrom="0" ShowAllocatedTo="0" ShowOption="-1" ShowStereotypeIconName="0" ShowTaggedValues="0" Width="120" X="251" Y="73" ZOrder="18">
							<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
							<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
								<Stroke/>
							</Line>
							<Caption Height="40" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="FreeMove" Visible="true" Width="96" X="0" Y="0"/>
							<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
						</Artifact>
					</DiagramElementChildren>
					<FillColor Color="rgb(122, 207, 245)" Style="1" Transparency="0" Type="1"/>
					<CompartmentFont Value="none"/>
				</Node>
			</Shapes>
			<Connectors>
				<Realization Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="DeploymentDiagram" Foreground="rgb(0, 0, 0)" From="d2jRk4WFYCyCBxOG" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="228" Id="72jRk4WFYCyCBxOO" MetaModelElement="_WjRk4WFYCyCBxNx" Model="_WjRk4WFYCyCBxNx" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="j2jRk4WFYCyCBxOK" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="200" X="24" Y="14" ZOrder="22">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="124" Y="128"/>
					<Points>
						<Point X="124.0" Y="142.0"/>
						<Point X="124.0" Y="114.0"/>
					</Points>
				</Realization>
				<Dependency Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="DeploymentDiagram" Foreground="rgb(0, 0, 0)" From="j2jRk4WFYCyCBxOK" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="200" Id="n2jRk4WFYCyCBxOQ" MetaModelElement="g2jRk4WFYCyCBxN0" Model="g2jRk4WFYCyCBxN0" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="r2jRk4WFYCyCBxOM" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="248" X="102" Y="-7" ZOrder="24">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="215" Y="93"/>
					<Points>
						<Point X="202.0" Y="93.0"/>
						<Point X="250.0" Y="93.0"/>
					</Points>
				</Dependency>
				<Dependency Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" Foreground="rgb(0, 0, 0)" From="12jRk4WFYCyCBxOC" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="200" Id="n2jRk4WFYCyCBxOS" MetaModelElement="g2jRk4WFYCyCBxN1" Model="g2jRk4WFYCyCBxN1" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="12jRk4WFYCyCBxOE" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="254" X="467" Y="-7" ZOrder="26">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="560" Y="93"/>
					<Points>
						<Point X="567.0" Y="93.0"/>
						<Point X="621.0" Y="93.0"/>
					</Points>
				</Dependency>
				<Realization Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" Foreground="rgb(0, 0, 0)" From="l2jRk4WFYCyCBxN." FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="228" Id="32jRk4WFYCyCBxOU" MetaModelElement="_WjRk4WFYCyCBxNy" Model="_WjRk4WFYCyCBxNy" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="12jRk4WFYCyCBxOC" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="200" X="399" Y="14" ZOrder="28">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="499" Y="128"/>
					<Points>
						<Point X="499.0" Y="142.0"/>
						<Point X="499.0" Y="114.0"/>
					</Points>
				</Realization>
				<Dependency Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="DeploymentDiagram" Foreground="rgb(0, 0, 0)" From="p2jRk4WFYCyCBxN8" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="314" Id="32jRk4WFYCyCBxOW" MetaModelElement="g2jRk4WFYCyCBxN2" Model="g2jRk4WFYCyCBxN2" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="d2jRk4WFYCyCBxOG" ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="482" X="24" Y="59" ZOrder="30">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="257" Y="210"/>
					<Points>
						<Point X="406.0" Y="273.0"/>
						<Point X="406.0" Y="219.0"/>
						<Point X="124.0" Y="219.0"/>
						<Point X="124.0" Y="159.0"/>
					</Points>
				</Dependency>
				<Dependency Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="DeploymentDiagram" Foreground="rgb(0, 0, 0)" From="p2jRk4WFYCyCBxN8" FromConnectType="0" FromPinType="1" FromShapeXDiff="0" FromShapeYDiff="0" Height="314" Id="v2jRk4WFYCyCBxOY" MetaModelElement="g2jRk4WFYCyCBxN3" Model="g2jRk4WFYCyCBxN3" ModelElementNameAlignment="9" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowConnectorName="2" To="l2jRk4WFYCyCBxN." ToConnectType="0" ToPinType="1" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="293" X="306" Y="59" ZOrder="32">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="0" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="20" X="445" Y="218"/>
					<Points>
						<Point X="406.0" Y="273.0"/>
						<Point X="406.0" Y="219.0"/>
						<Point X="499.0" Y="219.0"/>
						<Point X="499.0" Y="159.0"/>
					</Points>
				</Dependency>
				<Association AssociationEndPropertyStringsAInternalHeight="-2147483648" AssociationEndPropertyStringsAInternalWidth="-2147483648" AssociationEndPropertyStringsBInternalHeight="-2147483648" AssociationEndPropertyStringsBInternalWidth="-2147483648" Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="DeploymentDiagram" Foreground="rgb(0, 0, 0)" From="m2jRk4WFYCyCBxN6" FromConnectType="0" FromMultiplicityInternalHeight="-2147483648" FromMultiplicityInternalWidth="-2147483648" FromPinType="1" FromRoleInternalHeight="-2147483648" FromRoleInternalWidth="-2147483648" FromShapeXDiff="0" FromShapeYDiff="0" HasAssociationEndPropertyStringsAShape="false" HasAssociationEndPropertyStringsBShape="false" HasMultiplicityAShape="false" HasMultiplicityBShape="false" HasRoleAShape="false" HasRoleBShape="false" Height="286" Id="v2jRk4WFYCyCBxOa" MetaModelElement="KWjRk4WFYCyCBxNZ" Model="KWjRk4WFYCyCBxNZ" ModelElementNameAlignment="9" Name="TCP/IP" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowAssociationEndPropertyStrings="false" ShowConnectorName="2" ShowDirection="false" ShowFromMultiplicity="true" ShowFromRoleName="true" ShowFromRoleVisibility="true" ShowMultiplicityConstraints="false" ShowNavigationArrows="0" ShowOrderedMultiplicityConstraint="true" ShowStereotypes="true" ShowToMultiplicity="true" ShowToRoleName="true" ShowToRoleVisibility="true" ShowUniqueMultiplicityConstraint="true" SuppressImplied1MultiplicityForAssociationEnd="0" To="l2jRk4WFYCyCBxOA" ToConnectType="0" ToMultiplicityInternalHeight="-2147483648" ToMultiplicityInternalWidth="-2147483648" ToPinType="1" ToRoleInternalHeight="-2147483648" ToRoleInternalWidth="-2147483648" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="314" X="388" Y="97" ZOrder="34">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="56" X="525" Y="287"/>
					<Points>
						<Point X="488.0" Y="283.0"/>
						<Point X="602.0" Y="283.0"/>
						<Point X="602.0" Y="197.0"/>
					</Points>
				</Association>
				<Association AssociationEndPropertyStringsAInternalHeight="-2147483648" AssociationEndPropertyStringsAInternalWidth="-2147483648" AssociationEndPropertyStringsBInternalHeight="-2147483648" AssociationEndPropertyStringsBInternalWidth="-2147483648" Background="rgb(122, 207, 245)" ConnectorLabelOrientation="4" ConnectorLineJumps="4" ConnectorStyle="Follow Diagram" CreatorDiagramType="DeploymentDiagram" Foreground="rgb(0, 0, 0)" From="m2jRk4WFYCyCBxN6" FromConnectType="0" FromMultiplicityInternalHeight="-2147483648" FromMultiplicityInternalWidth="-2147483648" FromPinType="1" FromRoleInternalHeight="-2147483648" FromRoleInternalWidth="-2147483648" FromShapeXDiff="0" FromShapeYDiff="0" HasAssociationEndPropertyStringsAShape="false" HasAssociationEndPropertyStringsBShape="false" HasMultiplicityAShape="false" HasMultiplicityBShape="false" HasRoleAShape="false" HasRoleBShape="false" Height="286" Id="v2jRk4WFYCyCBxOc" MetaModelElement="JWjRk4WFYCyCBxNk" Model="JWjRk4WFYCyCBxNk" ModelElementNameAlignment="9" Name="TCP/IP" PaintThroughLabel="2" RequestRebuild="false" RequestRebuildFromEnd="false" RequestRebuildToEnd="false" RequestResetCaption="false" RequestResetCaptionFitWidth="false" RequestResetCaptionSize="false" Selectable="true" ShowAssociationEndPropertyStrings="false" ShowConnectorName="2" ShowDirection="false" ShowFromMultiplicity="true" ShowFromRoleName="true" ShowFromRoleVisibility="true" ShowMultiplicityConstraints="false" ShowNavigationArrows="0" ShowOrderedMultiplicityConstraint="true" ShowStereotypes="true" ShowToMultiplicity="true" ShowToRoleName="true" ShowToRoleVisibility="true" ShowUniqueMultiplicityConstraint="true" SuppressImplied1MultiplicityForAssociationEnd="0" To="j2jRk4WFYCyCBxOI" ToConnectType="0" ToMultiplicityInternalHeight="-2147483648" ToMultiplicityInternalWidth="-2147483648" ToPinType="1" ToRoleInternalHeight="-2147483648" ToRoleInternalWidth="-2147483648" ToShapeXDiff="0" ToShapeYDiff="0" UseFromShapeCenter="true" UseToShapeCenter="true" Width="415" X="-4" Y="97" ZOrder="36">
					<ElementFont Color="rgb(0, 0, 0)" Name="Dialog" Size="11" Style="0"/>
					<Line Cap="0" Color="rgb(0, 0, 0)" Transparency="0" Weight="1.0">
						<Stroke/>
					</Line>
					<Caption Height="15" InternalHeight="-2147483648" InternalWidth="-2147483648" Side="None" Visible="true" Width="56" X="161" Y="276"/>
					<Points>
						<Point X="311.0" Y="283.0"/>
						<Point X="96.0" Y="283.0"/>
						<Point X="96.0" Y="197.0"/>
					</Points>
				</Association>
			</Connectors>
		</DeploymentDiagram>
	</Diagrams>
</Project>
```

</details>
