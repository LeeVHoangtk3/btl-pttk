"""Create a separate report revision and an evidence based comparison.

Run with the Codex primary Python runtime. Source reports are never overwritten.
The revision preserves the original diagrams; technical limitations are recorded
in the separate comparison, rather than silently presenting them as resolved.
"""
from copy import deepcopy
from pathlib import Path
import re

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "code_pttk" / "docs" / "doi_chieu_datn24"
SOURCE = ROOT / "code_pttk" / "docs" / "N13 Nhóm 10.docx"


def field(p, code, placeholder=""):
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    begin.set(qn("w:dirty"), "true")
    p.add_run()._r.append(begin)
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = " " + code + " "
    p.add_run()._r.append(instruction)
    separator = OxmlElement("w:fldChar")
    separator.set(qn("w:fldCharType"), "separate")
    p.add_run()._r.append(separator)
    p.add_run(placeholder)
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    p.add_run()._r.append(end)


def setup(d):
    for e in list(d.settings.element):
        if e.tag in (qn('w:attachedTemplate'), qn('w:linkStyles')):
            d.settings.element.remove(e)
    for s in d.sections:
        s.page_width, s.page_height = Cm(21), Cm(29.7)
        s.top_margin, s.bottom_margin = Cm(2), Cm(2)
        s.left_margin, s.right_margin = Cm(3), Cm(2)
        s.header_distance, s.footer_distance = Cm(1), Cm(1)
        for h in (s.header, s.footer):
            for p in h.paragraphs:
                p.clear()
        s.different_first_page_header_footer = True
        p = s.footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        field(p, "PAGE")
    for name in ("Normal", "Title", "Subtitle", "Heading 1", "Heading 2", "Heading 3", "Caption"):
        st = d.styles[name]
        st.font.name = "Times New Roman"
        st.font.color.rgb = RGBColor(0, 0, 0)
        st.font.size = Pt(13)
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.line_spacing = 1.25
        st.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Times New Roman")
        fonts = st.element.get_or_add_rPr().get_or_add_rFonts()
        for k in ('asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme'):
            fonts.attrib.pop(qn('w:' + k), None)
        for k in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
            fonts.set(qn('w:' + k), 'Times New Roman')
        for border in st.element.xpath('.//w:pBdr'):
            border.getparent().remove(border)
    for name, size in (("Title", 20), ("Heading 1", 16), ("Heading 2", 14), ("Heading 3", 13)):
        st = d.styles[name]
        st.font.size, st.font.bold = Pt(size), True
        st.paragraph_format.keep_with_next = True
        st.paragraph_format.space_before = Pt(12)
    d.styles["Heading 1"].paragraph_format.page_break_before = True
    for name in ("Figure Caption", "Table Caption"):
        if name not in d.styles:
            st = d.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
            st.base_style = d.styles["Caption"]
        d.styles[name].font.size = Pt(11)
        d.styles[name].font.color.rgb = RGBColor(0, 0, 0)
        d.styles[name].paragraph_format.line_spacing = 1.1
    d.styles["Table Caption"].paragraph_format.keep_with_next = True
    for level in range(1, 4):
        name = f'TOC {level}'
        if name not in d.styles:
            d.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH, builtin=True)
        st = d.styles[name]
        st.font.name, st.font.size = 'Times New Roman', Pt(11)
        st.font.color.rgb = RGBColor(0, 0, 0)
        st.paragraph_format.space_before = Pt(0)
        st.paragraph_format.space_after = Pt(2)
        st.paragraph_format.line_spacing = 1.1
        st.paragraph_format.keep_with_next = False
        st.paragraph_format.left_indent = Cm((level - 1) * .4)
        st.paragraph_format.right_indent = Cm(.6)
        st.paragraph_format.tab_stops.clear_all()
        st.paragraph_format.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    if 'Data Heading' not in d.styles:
        st = d.styles.add_style('Data Heading', WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = d.styles['Heading 3']
        outline = OxmlElement('w:outlineLvl')
        outline.set(qn('w:val'), '9')
        st.element.get_or_add_pPr().append(outline)
    setting = OxmlElement("w:updateFields")
    setting.set(qn("w:val"), "true")
    d.settings.element.append(setting)


def para(d, text, style=None):
    p = d.add_paragraph(text, style)
    if style is None:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p


def heading(d, text, level=2):
    return d.add_heading(text, level)


def table(d, title, headers, rows):
    para(d, title, "Table Caption")
    t = d.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c, text in zip(t.rows[0].cells, headers):
        c.text = str(text)
    for row in rows:
        for c, text in zip(t.add_row().cells, row):
            c.text = str(text)
    return t


def format_tables(d):
    for t in d.tables:
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        pr = t._tbl.tblPr
        borders = pr.find(qn("w:tblBorders"))
        if borders is None:
            borders = OxmlElement("w:tblBorders")
            pr.append(borders)
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            e = OxmlElement("w:" + edge)
            for key, value in (("val", "single"), ("sz", "4"), ("color", "D9D9D9")):
                e.set(qn("w:" + key), value)
            borders.append(e)
        for ri, row in enumerate(t.rows):
            if ri == 0:
                repeat = OxmlElement("w:tblHeader")
                row._tr.get_or_add_trPr().append(repeat)
            for c in row.cells:
                c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                tcpr = c._tc.get_or_add_tcPr()
                margins = OxmlElement("w:tcMar")
                for side in ("top", "left", "bottom", "right"):
                    e = OxmlElement("w:" + side)
                    e.set(qn("w:w"), "85")
                    e.set(qn("w:type"), "dxa")
                    margins.append(e)
                tcpr.append(margins)
                if ri == 0:
                    shade = OxmlElement("w:shd")
                    shade.set(qn("w:fill"), "E7E6E6")
                    tcpr.append(shade)
                for p in c.paragraphs:
                    p.paragraph_format.space_after = Pt(3)
                    p.paragraph_format.line_spacing = 1.08
                    p.paragraph_format.keep_with_next = False
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(10 if len(t.columns) > 3 else 11)
                        r.font.color.rgb = RGBColor(0, 0, 0)
                        if ri == 0:
                            r.bold = True
        if len(t.columns) == 2:
            for row in t.rows:
                row.cells[0].width, row.cells[1].width = Cm(4), Cm(12)
        elif len(t.columns) == 3:
            for row in t.rows:
                for c, width in zip(row.cells, (1.1, 3.3, 11.6)):
                    c.width = Cm(width)
        elif len(t.columns) == 4:
            for row in t.rows:
                for c, width in zip(row.cells, (3.4, 3.1, 3.3, 6.2)):
                    c.width = Cm(width)


SCHEMA = [
    ("Category", "Danh mục thực đơn", [
        ("maDanhMuc", "INT", "PK", "Mã danh mục"),
        ("tenDanhMuc", "VARCHAR(100)", "NOT NULL", "Tên danh mục"),
        ("moTa", "VARCHAR(255)", "NULL", "Mô tả danh mục")]),
    ("MenuItem", "Mặt hàng thực đơn", [
        ("maMon", "INT", "PK", "Mã mặt hàng"),
        ("tenMon", "VARCHAR(150)", "NOT NULL", "Tên món lẻ hoặc combo"),
        ("gia", "DECIMAL(12,0)", "NOT NULL; > 0", "Giá bán bằng đồng Việt Nam"),
        ("hinhAnh", "VARCHAR(255)", "NULL", "Đường dẫn ảnh"),
        ("dangKinhDoanh", "TINYINT", "NOT NULL; 0 hoặc 1", "0 tạm ngừng; 1 đang bán"),
        ("kieuMon", "TINYINT", "NOT NULL; 1 hoặc 2", "1 món lẻ; 2 combo"),
        ("maDanhMuc", "INT", "FK Category", "Danh mục của mặt hàng")]),
    ("Dish", "Món lẻ", [
        ("maMon", "INT", "PK; FK MenuItem", "Cùng mã với mặt hàng cha"),
        ("loaiMon", "VARCHAR(50)", "NOT NULL", "Phân loại món"),
        ("moTa", "VARCHAR(255)", "NULL", "Mô tả món lẻ")]),
    ("Combo", "Gói combo", [
        ("maMon", "INT", "PK; FK MenuItem", "Cùng mã với mặt hàng cha"),
        ("soLuongNguoiAn", "INT", "NOT NULL; > 0", "Số người ăn dự kiến")]),
    ("ComboDetail", "Thành phần combo", [
        ("maCombo", "INT", "PK ghép; FK Combo", "Mã combo"),
        ("maMonLe", "INT", "PK ghép; FK Dish", "Mã món lẻ thành phần"),
        ("soLuong", "INT", "NOT NULL; > 0", "Số phần món trong combo"),
        ("ghiChu", "VARCHAR(255)", "NULL", "Ghi chú thành phần")]),
    ("Area", "Khu vực phục vụ", [
        ("maKhuVuc", "INT", "PK", "Mã khu vực"),
        ("tenKhuVuc", "VARCHAR(100)", "NOT NULL", "Tên tầng hoặc khu vực; loại đơn được xác định riêng")]),
    ("RestaurantTable", "Bàn ăn", [
        ("maBan", "INT", "PK", "Mã bàn"),
        ("soBan", "VARCHAR(20)", "UNIQUE; NOT NULL", "Số hiệu bàn hiển thị"),
        ("trangThai", "TINYINT", "NOT NULL; 1 hoặc 2", "1 trống; 2 đang phục vụ"),
        ("maKhuVuc", "INT", "FK Area", "Khu vực chứa bàn")]),
    ("Orders", "Đơn hàng", [
        ("maDon", "INT", "PK", "Mã đơn nội bộ"),
        ("thoiGianTao", "BIGINT", "NOT NULL", "Unix timestamp theo giây"),
        ("trangThai", "TINYINT", "NOT NULL; 1 đến 5", "Theo bảng quy ước trạng thái"),
        ("tongTien", "DECIMAL(12,0)", "NOT NULL; >= 0", "Giá trị tạm tính đang được cập nhật bởi bộ SQL minh họa"),
        ("vat", "DECIMAL(5,2)", "NOT NULL; 0 đến 100", "Thuế suất theo phần trăm; ví dụ 8 nghĩa là 8%"),
        ("chietKhau", "DECIMAL(12,0)", "NOT NULL; >= 0", "Số tiền giảm giá bằng đồng Việt Nam")]),
    ("OrderTaiCho", "Đơn tại chỗ", [
        ("maDon", "INT", "PK; FK Orders", "Đơn tại chỗ"),
        ("maBan", "INT", "FK RestaurantTable", "Bàn phục vụ; không đặt UNIQUE vì một bàn có thể có nhiều đơn")]),
    ("OrderMangVe", "Đơn mang về", [
        ("maDon", "INT", "PK; FK Orders", "Đơn mang về"),
        ("diaChiGiao", "VARCHAR(255)", "NULL", "Chỉ dùng khi có yêu cầu giao hàng"),
        ("soDienThoaiKhach", "VARCHAR(15)", "Theo điều kiện nghiệp vụ", "Số liên hệ; không mặc định bắt buộc với mọi đơn mang về")]),
    ("OrderItem", "Dòng món của đơn", [
        ("maOrderItem", "INT", "PK", "Mã dòng món"),
        ("maDon", "INT", "FK Orders", "Đơn chứa dòng món"),
        ("maMon", "INT", "FK MenuItem", "Món lẻ hoặc combo"),
        ("soLuong", "INT", "NOT NULL; > 0", "Số lượng gọi"),
        ("donGia", "DECIMAL(12,0)", "NOT NULL; >= 0", "Giá tại thời điểm gọi món"),
        ("ghiChu", "VARCHAR(255)", "NULL", "Yêu cầu chế biến"),
        ("tuyChon", "VARCHAR(255)", "NULL", "Kích cỡ hoặc lựa chọn khác")]),
    ("OrderMergeLog", "Nhật ký gộp đơn", [
        ("maLog", "INT", "PK", "Mã nhật ký"),
        ("maDonDich", "INT", "FK Orders", "Đơn nhận món"),
        ("maDonNguon", "INT", "FK Orders", "Đơn được gộp; phải khác đơn đích"),
        ("thoiGian", "BIGINT", "NOT NULL", "Unix timestamp theo giây"),
        ("nhanVien", "VARCHAR(100)", "NOT NULL", "Định danh người thực hiện; chưa có bảng tài khoản trong ERD")]),
    ("Payment", "Thanh toán", [
        ("maThanhToan", "INT", "PK", "Mã thanh toán"),
        ("maDon", "INT", "FK Orders; UNIQUE", "Tối đa một bản ghi thanh toán hoàn tất cho mỗi đơn"),
        ("tongTienDon", "DECIMAL(12,0)", "NOT NULL; >= 0", "Số tiền phải thu khi chốt thanh toán"),
        ("thoiGianThanhToan", "BIGINT", "NOT NULL", "Unix timestamp theo giây")]),
    ("PaymentTienMat", "Thanh toán tiền mặt", [
        ("maThanhToan", "INT", "PK; FK Payment", "Mã thanh toán cha"),
        ("tienDaNhan", "DECIMAL(12,0)", "NOT NULL; >= 0", "Tiền khách đưa"),
        ("tienThua", "DECIMAL(12,0)", "NOT NULL; >= 0", "Tiền trả lại khách"),
        ("tienTip", "DECIMAL(12,0)", "NOT NULL; mặc định 0", "Tiền tip tách riêng")]),
    ("PaymentThe", "Thanh toán thẻ", [
        ("maThanhToan", "INT", "PK; FK Payment", "Mã thanh toán cha"),
        ("loaiThe", "VARCHAR(20)", "NOT NULL", "VISA, MASTER, JCB hoặc ATM theo mô hình lớp"),
        ("maGiaoDich", "VARCHAR(50)", "NOT NULL", "Mã tham chiếu giao dịch")]),
    ("PaymentLog", "Nhật ký thanh toán", [
        ("maLog", "INT", "PK", "Mã nhật ký"),
        ("maThanhToan", "INT", "FK Payment; UNIQUE", "Một bản ghi tổng kết cho mỗi thanh toán theo ERD hiện tại"),
        ("maDon", "INT", "NOT NULL", "Mã đơn được lưu vết"),
        ("tongTien", "DECIMAL(12,0)", "NOT NULL; >= 0", "Giá trị đã thu"),
        ("thoiGian", "BIGINT", "NOT NULL", "Unix timestamp theo giây"),
        ("nhanVien", "VARCHAR(100)", "NOT NULL", "Định danh thu ngân thực hiện")]),
]


def dictionary(d):
    heading(d, "3.2.2 Mô tả các bảng và quy ước dữ liệu", 3)
    para(d, "Lược đồ gồm 16 bảng. Đặc tả dưới đây đề xuất kiểu dữ liệu vật lý phù hợp với ý nghĩa thuộc tính, khóa và truy vấn hiện có. Các kiểu integer dùng cho tên, địa chỉ, ảnh và thời gian trong hình ERD cần được cập nhật theo đặc tả trước khi tạo CSDL. Đây là thiết kế dữ liệu, chưa phải kết quả kiểm thử một CSDL đã cài đặt.")
    para(d, "Mã nội bộ dùng INT; các mã hiển thị như HD001 là định dạng trên giao diện. Các lớp dùng String cần có quy tắc chuyển đổi khi ánh xạ sang khóa số. Tiền dùng DECIMAL(12,0) cho số đồng nguyên; không dùng số thực dấu phẩy động để lưu tiền. Thời gian BIGINT thống nhất theo giây để khớp UNIX_TIMESTAMP(). PK là khóa chính; FK là khóa ngoại. Với khóa ngoại không ghi cột đích, cột được tham chiếu là khóa chính của bảng đích.")
    table(d, "Quy ước trạng thái và loại mặt hàng", ["Thuộc tính", "Mã", "Ý nghĩa"], [
        ("MenuItem.kieuMon", "1 / 2", "Món lẻ / Combo"),
        ("RestaurantTable.trangThai", "1 / 2", "TRONG / DANG_PHUC_VU"),
        ("Orders.trangThai", "1", "DANG_PHUC_VU; đã được sử dụng trong SQL"),
        ("Orders.trangThai", "2", "CHO_THANH_TOAN; được truy vấn trong SQL"),
        ("Orders.trangThai", "3", "DA_THANH_TOAN; đã được sử dụng trong SQL"),
        ("Orders.trangThai", "4", "DA_GOP; đã được sử dụng trong SQL"),
        ("Orders.trangThai", "5", "DA_HUY; mã đề xuất để bổ sung trạng thái trong mô hình")])
    for name, meaning, rows in SCHEMA:
        para(d, name + " " + meaning, 'Data Heading')
        table(d, "Đặc tả bảng " + name, ["Tên cột", "Kiểu dữ liệu", "Ràng buộc", "Mô tả"], rows)
    para(d, "Quy tắc toàn vẹn và phạm vi đặc tả", 'Data Heading')
    for t in [
        "Mỗi MenuItem thuộc đúng một loại Dish hoặc Combo; mỗi Orders thuộc đúng một loại đơn tại chỗ hoặc mang về. Khóa ngoại đơn thuần không bảo đảm tính loại trừ này; tầng nghiệp vụ phải kiểm tra khi lưu dữ liệu.",
        "Không mặc định rằng các dòng có cùng maMon là cùng một dòng món. Việc gộp còn phải xét đơn giá, tùy chọn và ghi chú chế biến. ERD hiện tại chỉ cho thấy khóa chính maOrderItem, chưa có khóa duy nhất xác định dòng món tương đương.",
        "Bộ SQL hiện tại tính Orders.tongTien bằng SUM(soLuong * donGia), nên đây là tiền món tạm tính. Quy tắc áp dụng VAT, chiết khấu, làm tròn và số tiền chốt trong Payment.tongTienDon phải được chốt cùng kịch bản thanh toán trước khi lập trình.",
        "Mỗi thay đổi tạo combo, tạo đơn, gộp đơn hoặc thanh toán gồm nhiều câu lệnh liên quan cần được thực hiện trong một giao dịch. Phải kiểm tra lại trạng thái khi cập nhật và xử lý rollback nếu một bước thất bại. Không giải phóng bàn nếu bàn vẫn còn đơn khác đang phục vụ.",
        "Mô hình đã mô tả thanh toán tiền mặt và thẻ. Chuyển khoản có trong kịch bản nhưng chưa có kiểu dữ liệu riêng hoặc quy ước nhận diện đầy đủ; cần bổ sung trước khi khẳng định thiết kế đã bao phủ cả ba phương thức.",
        "Trường mô tả combo trên biểu mẫu chưa có thuộc tính lưu tương ứng trong Combo hoặc MenuItem. Phần tài khoản, phân quyền và lịch sử thử thanh toán cũng chưa được đặc tả thành bảng trong ERD 16 bảng này."
    ]:
        para(d, t)


def introduction(d):
    heading(d, "CHƯƠNG 1 TỔNG QUAN ĐỀ TÀI VÀ CƠ SỞ THIẾT KẾ", 1)
    heading(d, "1.1 Lý do chọn đề tài")
    para(d, "Hoạt động phục vụ nhà hàng liên kết nhiều thao tác: xây dựng thực đơn, tiếp nhận gọi món, xử lý đơn đang phục vụ và thanh toán. Thông tin bàn, món và số tiền phải được cập nhật nhất quán khi khách gọi thêm món hoặc nhiều bàn thanh toán chung. Nếu các bước này không được mô tả rõ, hệ thống có thể ghi nhận trùng món, sai tổng tiền hoặc giải phóng bàn không đúng thời điểm.")
    para(d, "Đề tài Hệ thống quản lý nhà hàng Thanh Hoa được thực hiện trong học phần Phân tích và Thiết kế Hệ thống Thông tin nhằm mô hình hóa các quy trình trên. Trọng tâm của báo cáo là hồ sơ phân tích và thiết kế làm cơ sở cho việc xây dựng phần mềm.")
    heading(d, "1.2 Mục tiêu và phạm vi")
    para(d, "Báo cáo tập trung đặc tả bốn chức năng: Tạo combo, Tạo đơn hàng, Gộp đơn hàng và Thanh toán. Với mỗi chức năng, tài liệu trình bày tác nhân, điều kiện thực hiện, luồng chính, luồng thay thế hoặc ngoại lệ, các lớp liên quan và sự trao đổi thông điệp giữa các đối tượng.")
    para(d, "Các nghiệp vụ tách đơn, hủy đơn và di chuyển bàn xuất hiện trong bối cảnh hệ thống, nhưng không được xem là đã đặc tả sâu tương đương bốn chức năng trọng tâm. Quản lý kho, đặt bàn trực tuyến và thống kê doanh thu thuộc hướng mở rộng.")
    heading(d, "1.3 Kết quả dự kiến")
    para(d, "Kết quả của đề tài là bộ tài liệu gồm khảo sát yêu cầu, Use case, kịch bản, biểu đồ lớp và trình tự của pha phân tích và pha thiết kế, biểu đồ trạng thái, biểu đồ hoạt động, thiết kế giao diện, mô hình dữ liệu, truy vấn minh họa, biểu đồ thành phần và biểu đồ triển khai. Các mô hình cần truy vết được về cùng một bộ quy tắc nghiệp vụ.")
    heading(d, "1.4 Công cụ và định hướng công nghệ")
    para(d, "UML được sử dụng để mô tả cấu trúc và hành vi của hệ thống. Các hình trong báo cáo mang dấu xuất của Visual Paradigm Community Edition; kho tài liệu còn có mã sơ đồ PlantUML và Mermaid phục vụ lưu trữ, chỉnh sửa. Mỗi công cụ hỗ trợ cách thể hiện mô hình, còn tính đúng đắn phải được kiểm tra qua quan hệ giữa kịch bản, lớp, dữ liệu và thông điệp.")
    para(d, "Biểu đồ triển khai định hướng một ứng dụng Java Web được đóng gói bằng RestaurantApp.war, kết nối CSDL ThanhHoaRestaurantDB thông qua JDBC. Các truy vấn sử dụng cú pháp MySQL. Đây là cơ sở đề xuất nền tảng Java Web và MySQL cho pha cài đặt; tài liệu chưa xác lập phiên bản JDK, máy chủ ứng dụng, framework hoặc nhà cung cấp thanh toán cụ thể.")
    para(d, "Kiến trúc phân tách giao diện, điều khiển nghiệp vụ và lưu trữ dữ liệu. Khả năng xử lý giao dịch phụ thuộc thiết kế ranh giới giao dịch, ràng buộc CSDL và xử lý lỗi; việc chọn Java tự nó không bảo đảm tính nguyên tử hoặc tính nhất quán.")
    heading(d, "1.5 Kết luận chương")
    para(d, "Chương 1 xác định mục tiêu, phạm vi bốn chức năng trọng tâm và cơ sở công cụ của đề tài. Chương 2 chuyển các yêu cầu nghiệp vụ thành mô hình phân tích; Chương 3 cụ thể hóa giao diện, dữ liệu và phương án triển khai.")


def build_revision():
    d = Document(SOURCE)
    paragraphs, tables = list(d.paragraphs), list(d.tables)
    # Stable references avoid XML proxy identity reuse when walking the body.
    blocks = []
    for el in list(d.element.body):
        if el.tag == qn("w:p"):
            idx = next(i for i, p in enumerate(paragraphs) if p._p is el)
            blocks.append(("p", idx, deepcopy(el)))
        elif el.tag == qn("w:tbl"):
            idx = next(i for i, t in enumerate(tables) if t._tbl is el)
            blocks.append(("t", idx, deepcopy(el)))
    for el in list(d.element.body):
        if el.tag != qn("w:sectPr"):
            d.element.body.remove(el)
    setup(d)
    for text in ("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG", "KHOA CÔNG NGHỆ THÔNG TIN 1"):
        p = para(d, text)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
    logo = deepcopy(paragraphs[3]._p)
    d.element.body.insert(len(d.element.body)-1, logo)
    for el in logo.xpath('.//wp:extent'):
        el.set("cx", str(int(Cm(3))))
        el.set("cy", str(int(Cm(3.04))))
    for text, st in (("BÁO CÁO BÀI TẬP LỚN", "Subtitle"), ("PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG THÔNG TIN", "Subtitle"), ("HỆ THỐNG QUẢN LÝ NHÀ HÀNG\nTHANH HOA", "Title")):
        p = para(d, text, st)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(14)
    for text in ("Lớp N13 Nhóm 10", "Giảng viên hướng dẫn Nguyễn Đình Hiến", "Phan Việt Bảo  B23DCKH006", "Nguyễn Thanh Hòa  B23DCKH042", "Lê Việt Hoàng  B23DCKH044", "Ngô Văn Phương  B23DCKH092", "Hà Nội 2026"):
        p = para(d, text)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    heading(d, "LỜI MỞ ĐẦU", 1)
    para(d, "Báo cáo trình bày kết quả phân tích và thiết kế Hệ thống quản lý nhà hàng Thanh Hoa của Nhóm 10, lớp N13, trong học phần Phân tích và Thiết kế Hệ thống Thông tin. Bốn chức năng được lựa chọn để đặc tả chi tiết là tạo combo, tạo đơn hàng, gộp đơn hàng và thanh toán.")
    para(d, "Tài liệu được tổ chức từ yêu cầu nghiệp vụ đến mô hình đối tượng và thiết kế chi tiết. Các hình giao diện khảo sát minh họa cách thực hiện nghiệp vụ trên phần mềm POS; các bảng giao diện ở phần thiết kế thể hiện phương án tương tác đề xuất cho hệ thống. Các mô hình triển khai và câu SQL là cơ sở cho pha cài đặt, chưa thay thế bằng chứng chạy thử ứng dụng.")
    para(d, "Báo cáo gồm ba chương: Tổng quan đề tài và cơ sở thiết kế; Phân tích hệ thống; Thiết kế hệ thống và cơ sở dữ liệu. Phần cuối tổng kết kết quả của hồ sơ thiết kế, các hạn chế cần xử lý và hướng phát triển.")
    heading(d, "PHÂN CÔNG THÀNH VIÊN", 1)
    para(d, "Phân công chức năng được giữ theo báo cáo của nhóm.")
    para(d, "Phân công thành viên và chức năng phụ trách", "Table Caption")
    d.element.body.insert(len(d.element.body)-1, deepcopy(tables[0]._tbl))
    for title, code in (("MỤC LỤC", 'TOC \\o "1-3" \\h \\z \\u'), ("DANH MỤC HÌNH", 'TOC \\t "Figure Caption,1" \\h \\z'), ("DANH MỤC BẢNG", 'TOC \\t "Table Caption,1" \\h \\z')):
        # Navigation headings are not included in their own table of contents.
        p = para(d, title, "Title")
        p.paragraph_format.page_break_before = True
        field(d.add_paragraph(), code, "Cập nhật trường mục lục trong Word")
    introduction(d)
    # Map the existing hierarchy, keeping every original analysis/design block.
    headings = {
        13:(1,"CHƯƠNG 2 PHÂN TÍCH HỆ THỐNG QUẢN LÝ NHÀ HÀNG THANH HOA"),
        14:(2,"2.1 Khảo sát yêu cầu"),15:(3,"2.1.1 Hiện trạng và quy trình nghiệp vụ"),39:(3,"2.1.2 Tác nhân và yêu cầu chức năng"),
        42:(2,"2.2 Biểu đồ Use case"),43:(3,"2.2.1 Toàn hệ thống"),46:(3,"2.2.2 Quản lý menu và tạo combo"),49:(3,"2.2.3 Tạo đơn hàng"),52:(3,"2.2.4 Xử lý đơn và gộp đơn"),55:(3,"2.2.5 Thanh toán"),
        59:(2,"2.3 Kịch bản chức năng"),60:(3,"2.3.1 Tạo combo"),62:(3,"2.3.2 Tạo đơn hàng"),64:(3,"2.3.3 Gộp đơn hàng"),66:(3,"2.3.4 Thanh toán"),
        69:(2,"2.4 Biểu đồ lớp thực thể"),70:(3,"2.4.1 Toàn hệ thống"),73:(3,"2.4.2 Quản lý menu"),76:(3,"2.4.3 Tạo đơn hàng"),79:(3,"2.4.4 Gộp đơn hàng"),82:(3,"2.4.5 Thanh toán"),
        86:(2,"2.5 Biểu đồ trình tự pha phân tích"),87:(3,"2.5.1 Tạo combo"),90:(3,"2.5.2 Tạo đơn hàng"),93:(3,"2.5.3 Gộp đơn hàng"),96:(3,"2.5.4 Thanh toán"),
        100:(2,"2.6 Biểu đồ trạng thái"),101:(3,"2.6.1 Đơn hàng"),105:(3,"2.6.2 Bàn ăn"),109:(3,"2.6.3 Món ăn và combo"),
        114:(2,"2.7 Biểu đồ hoạt động"),115:(3,"2.7.1 Tạo combo"),118:(3,"2.7.2 Tạo đơn hàng"),121:(3,"2.7.3 Gộp đơn hàng"),124:(3,"2.7.4 Thanh toán"),
        128:(1,"CHƯƠNG 3 THIẾT KẾ HỆ THỐNG VÀ CƠ SỞ DỮ LIỆU"),129:(2,"3.1 Kịch bản và thiết kế giao diện"),130:(3,"3.1.1 Tạo combo"),149:(3,"3.1.2 Tạo đơn hàng"),167:(3,"3.1.3 Gộp đơn hàng"),188:(3,"3.1.4 Thanh toán"),
        208:(2,"3.2 Thiết kế cơ sở dữ liệu và truy vấn"),209:(3,"3.2.1 Lược đồ quan hệ thực thể"),212:(3,"3.2.3 Truy vấn minh họa cho các chức năng"),
        222:(2,"3.3 Biểu đồ lớp pha thiết kế"),223:(3,"3.3.1 Toàn hệ thống"),226:(3,"3.3.2 Quản lý menu"),229:(3,"3.3.3 Tạo đơn hàng"),232:(3,"3.3.4 Gộp đơn hàng"),235:(3,"3.3.5 Thanh toán"),
        239:(2,"3.4 Biểu đồ trình tự pha thiết kế"),240:(3,"3.4.1 Tạo combo"),243:(3,"3.4.2 Tạo đơn hàng"),246:(3,"3.4.3 Gộp đơn hàng"),249:(3,"3.4.4 Thanh toán"),253:(2,"3.5 Biểu đồ thành phần"),256:(2,"3.6 Biểu đồ triển khai")}
    captions = {i for i,p in enumerate(paragraphs) if p.text.startswith("Hình ")}
    captions.update((211,225,228,231,234,237,242,245,248,251,255,258))
    fig_counts = {2:0,3:0}
    section_intros = {
        42: "Biểu đồ Use case xác định phạm vi tương tác của ba vai trò chính: quản lý, nhân viên phục vụ và thu ngân. Sơ đồ tổng quát cho biết các nhóm chức năng; các sơ đồ phân rã cần được đọc cùng kịch bản để hiểu bước bắt buộc, bước có điều kiện và quyền thực hiện. Quan hệ include hoặc extend không biểu diễn đơn thuần thứ tự các bước [2].",
        69: "Mô hình lớp thực thể tổ chức dữ liệu nghiệp vụ quanh ba nhóm Menu, Order và Payment. Các lớp con thể hiện loại món, loại đơn và phương thức thanh toán; quan hệ giữa lớp thể hiện đối tượng cần được liên kết để thực hiện kịch bản. Ở pha phân tích, trọng tâm là ý nghĩa đối tượng và quan hệ, chưa phải chi tiết lưu trữ hay lớp giao diện.",
        86: "Các biểu đồ trình tự mô tả trao đổi giữa tác nhân, giao diện, điều khiển và thực thể trong từng kịch bản. Mỗi thông điệp cần truy vết về một bước nghiệp vụ, đặc biệt là kiểm tra dữ liệu, ghi nhận thành công và nhánh lỗi. Pha thiết kế ở Chương 3 tiếp tục cụ thể hóa các đối tượng và thao tác này.",
        100: "Biểu đồ trạng thái giải thích vòng đời của các thực thể có trạng thái thay đổi trong quá trình phục vụ. Chuyển trạng thái đơn hàng phải đi cùng điều kiện phù hợp; trạng thái bàn chỉ được cập nhật sau khi đã kiểm tra các đơn liên quan. Mã lưu trong CSDL được mô tả tại mục 3.2.2.",
        114: "Các biểu đồ hoạt động mô tả luồng công việc và các điểm quyết định của bốn chức năng trọng tâm. Các nhánh hủy hoặc lỗi cần bảo toàn dữ liệu đã có; kết quả hoạt động phải thống nhất với điều kiện sau trong kịch bản.",
        222: "Các lớp thiết kế bổ sung giao diện, điều khiển, phương thức và kiểu dữ liệu để định hướng cài đặt. Việc chuyển từ thực thể phân tích sang lớp thiết kế cần giữ cùng ý nghĩa nghiệp vụ; tên và kiểu thuộc tính phải tiếp tục được đối chiếu với đặc tả dữ liệu.",
        239: "Biểu đồ trình tự thiết kế thể hiện cách các lớp cộng tác để thực hiện từng chức năng. Các thao tác ghi nhiều bảng cần được đặt trong cùng ranh giới giao dịch; kết quả trả về giao diện phải phản ánh thành công hoặc thất bại của toàn bộ tác vụ.",
        253: "Mô hình thành phần phân chia hệ thống theo bốn dịch vụ nghiệp vụ, các giao diện người dùng và thành phần truy cập dữ liệu. Các giao diện dịch vụ thể hiện điểm liên kết giữa thành phần, giúp tránh để giao diện người dùng trực tiếp thực hiện quy tắc cập nhật CSDL.",
        256: "Mô hình triển khai bố trí giao diện trên thiết bị của quản lý, nhân viên order và thu ngân; các dịch vụ nghiệp vụ trên máy chủ ứng dụng; dữ liệu trên máy chủ CSDL. Dịch vụ thanh toán bên ngoài nằm ngoài phạm vi quản lý trực tiếp của hệ thống. Các giao thức trong sơ đồ là định hướng kết nối, chưa xác nhận một tích hợp đã vận hành."
    }
    original_table_titles = {1:"Tác nhân và yêu cầu chức năng",2:"Kịch bản tạo combo",3:"Kịch bản tạo đơn hàng",4:"Kịch bản gộp đơn hàng",5:"Kịch bản thanh toán",6:"Giao diện quản lý thực đơn",7:"Biểu mẫu tạo combo",8:"Chọn món thành phần",9:"Kết quả tạo combo",10:"Sơ đồ khu vực và bàn",11:"Chọn món và giỏ hàng",12:"Nhập số lượng món",13:"Thao tác gộp đơn",14:"Danh sách bàn cần gộp",15:"Chi tiết bàn đã chọn",16:"Kết quả gộp đơn dự kiến",17:"Danh sách đơn chờ thanh toán",18:"Lựa chọn phương thức thanh toán",19:"Nhập tiền khách đưa",20:"Xác nhận thanh toán",21:"Kết quả thanh toán",22:"Truy vấn tạo combo",23:"Truy vấn tạo đơn hàng",24:"Truy vấn gộp đơn hàng",25:"Truy vấn thanh toán"}
    for kind, idx, el in blocks:
        if kind == "t":
            if idx == 0:
                continue
            para(d, original_table_titles[idx], "Table Caption")
            d.element.body.insert(len(d.element.body)-1, el)
            # The SQL remains illustrative: remove an unsupported promise in its header.
            for c in d.tables[-1].rows[0].cells:
                if "SQL chuẩn" in c.text:
                    c.text = "Truy vấn SQL minh họa"
            if idx == 24:
                for row in d.tables[-1].rows:
                    if "Dồn món" in row.cells[0].text:
                        row.cells[0].text = "Chuyển các dòng món sang đơn đích, giữ đơn giá và tùy chọn"
                        row.cells[1].text = "UPDATE OrderItem\nSET maDon = 501\nWHERE maDon = 503;\n-- Thực hiện trong giao dịch sau khi khóa và kiểm tra hai đơn."
            continue
        if idx < 13:
            continue
        if idx == 128:
            heading(d, "2.8 Kết luận chương")
            para(d, "Chương 2 mô tả bối cảnh nghiệp vụ, tác nhân và bốn kịch bản trọng tâm, sau đó biểu diễn cấu trúc và hành vi bằng UML. Các mô hình này cung cấp đầu vào cho thiết kế giao diện, dữ liệu và kiến trúc. Tính đầy đủ của bộ hình cần đi kèm việc đối chiếu điều kiện, trạng thái và thông điệp giữa các mô hình.")
        if idx == 212:
            dictionary(d)
        if idx in headings:
            level, title = headings[idx]
            heading(d, title, level)
            if idx in section_intros:
                para(d, section_intros[idx])
            if idx == 129:
                para(d, "Các bảng dưới đây là wireframe và dữ liệu minh họa cho tương tác người dùng. Chúng thể hiện phương án thiết kế giao diện, không được coi là ảnh chụp một ứng dụng của nhóm đã cài đặt và vận hành.")
            if idx == 212:
                para(d, "Các câu lệnh dùng số định danh và số tiền minh họa độc lập giữa từng tác vụ. Khi triển khai, ứng dụng phải truyền tham số, quản lý cấp mã và bao các thay đổi liên quan trong giao dịch. Việc chuyển các dòng món giữ nguyên đơn giá, ghi chú và tùy chọn; kết quả hiển thị có thể tổng hợp các dòng tương đương. Không sử dụng ON DUPLICATE KEY UPDATE để mặc định nhận biết món trùng khi chưa có khóa duy nhất tương ứng [3].")
            continue
        if idx in captions:
            chapter = 2 if idx < 128 else 3
            fig_counts[chapter] += 1
            text = paragraphs[idx].text
            text = re.sub(r"^Hình(?: khảo sát)?\s+[\d.]+\s*:\s*", "", text)
            p = para(d, f"Hình {chapter}.{fig_counts[chapter]} {text}", "Figure Caption")
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if idx in (26,28,32,36,38):
                p.paragraph_format.keep_with_next = True
                source_note = para(d, "Nguồn tư liệu khảo sát giao diện Sapo FnB trong báo cáo gốc.")
                source_note.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in source_note.runs:
                    r.font.size = Pt(10)
                    r.italic = True
            continue
        if not paragraphs[idx].text.strip() and not el.xpath('.//a:blip'):
            continue
        # Remove legacy manual page breaks; headings control the new hierarchy.
        for br in el.xpath('.//w:br[@w:type="page"]'):
            br.getparent().remove(br)
        d.element.body.insert(len(d.element.body)-1, el)
        p = d.paragraphs[-1]
        p.paragraph_format.page_break_before = False
        if idx == 16:
            p.text = "Phần khảo sát mô tả quy trình nghiệp vụ của nhà hàng Thanh Hoa kết hợp tư liệu giao diện phần mềm POS dành cho nhà hàng. Các hình Sapo FnB minh họa quy trình tham khảo, không phải bằng chứng về một ứng dụng đã được nhóm triển khai. Nội dung được tổ chức quanh bốn nghiệp vụ trọng tâm dưới đây."
        if el.xpath('.//a:blip'):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
        else:
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(13)
                r.font.color.rgb = RGBColor(0,0,0)
    heading(d, "3.7 Phương án môi trường triển khai")
    para(d, "Mô hình triển khai phân biệt máy trạm quản lý, thiết bị nhân viên order, máy thu ngân, máy chủ ứng dụng, máy chủ CSDL và dịch vụ thanh toán bên ngoài. Tệp RestaurantApp.war thể hiện phương án Java Web; JDBC thể hiện hướng kết nối CSDL. Đây là phương án thiết kế để chuẩn bị cài đặt.")
    para(d, "Khi lựa chọn môi trường thực tế cần chốt phiên bản Java và máy chủ tương thích, phiên bản MySQL, cách quản lý kết nối và giao dịch, cấu hình mạng, phương thức kết nối máy in và hợp đồng API thanh toán. Không đặt cấu hình CPU, RAM hoặc tên nhà cung cấp làm yêu cầu tối thiểu khi chưa có tải dự kiến và kết quả đo.")
    heading(d, "3.8 Kết luận chương")
    para(d, "Chương 3 cụ thể hóa kịch bản thành wireframe, lược đồ và đặc tả 16 bảng, truy vấn minh họa, các mô hình lớp và trình tự thiết kế, thành phần và triển khai. Trước khi cài đặt, cần đồng bộ kiểu dữ liệu trong ERD, quan hệ Use case, quy tắc tính tiền và mô hình thanh toán chuyển khoản với đặc tả nghiệp vụ.")
    heading(d, "KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", 1)
    heading(d, "Kết quả đạt được")
    para(d, "Nhóm đã xây dựng hồ sơ phân tích và thiết kế cho hệ thống quản lý nhà hàng Thanh Hoa, tập trung vào bốn chức năng tạo combo, tạo đơn, gộp đơn và thanh toán. Tài liệu liên kết khảo sát, kịch bản, mô hình UML, thiết kế giao diện và thiết kế dữ liệu; đây là kết quả của pha phân tích và thiết kế trong học phần.")
    heading(d, "Hạn chế")
    para(d, "Báo cáo chưa cung cấp kết quả chạy thử phần mềm, kiểm thử giao dịch trên MySQL, kiểm thử tích hợp thanh toán hoặc đo hiệu năng. Một số chi tiết còn cần thống nhất: kiểu dữ liệu ERD và lớp, lưu mô tả combo, nhận diện chuyển khoản, quy tắc VAT và chiết khấu, điều kiện gộp dòng món, xử lý nhiều đơn trên một bàn và chống thực hiện thanh toán lặp.")
    heading(d, "Hướng phát triển")
    para(d, "Ưu tiên tiếp theo là hoàn thiện các điểm chưa nhất quán, xây dựng DDL và kiểm thử các kịch bản tạo, gộp, thanh toán trong điều kiện lỗi hoặc đồng thời. Sau khi các chức năng cốt lõi ổn định có thể mở rộng quản lý nguyên liệu, đặt bàn, gọi món qua QR và báo cáo doanh thu. Các hướng này là đề xuất phát triển, chưa thuộc kết quả đã thực hiện.")
    heading(d, "TÀI LIỆU THAM KHẢO", 1)
    for text in [
        "[1] Báo cáo tham khảo Đatn24.pdf. Xây dựng ứng dụng nghe nhạc trực tuyến fullstack sử dụng NextJS. Tệp do người dùng cung cấp; tham khảo cách tổ chức nội dung, không dùng để suy ra quy định trình bày bắt buộc của học phần.",
        "[2] Visual Paradigm. Use Case Diagram Notations Guide. https://circle.visual-paradigm.com/docs/uml-and-sysml/use-case-diagram/use-case-diagram-notations-guide/ Truy cập ngày 22 tháng 11 năm 2026.",
        "[3] Oracle. MySQL 8.0 Reference Manual. INSERT ON DUPLICATE KEY UPDATE Statement. https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html Truy cập ngày 22 tháng 11 năm 2026.",
        "[4] Oracle. MySQL 8.4 Reference Manual. Locking Reads. https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html Truy cập ngày 22 tháng 11 năm 2026."]:
        para(d, text)
    # Sequential table captions are collected by the Word table-of-contents field.
    n = 0
    for p in d.paragraphs:
        if p.style.name == "Table Caption":
            n += 1
            p.text = f"Bảng {n} " + p.text
    for shape in d.inline_shapes:
        maxw, maxh = int(Cm(16)), int(Cm(20.8))
        scale = min(1, maxw / shape.width, maxh / shape.height)
        if scale < 1:
            shape.width, shape.height = int(shape.width * scale), int(shape.height * scale)
    format_tables(d)
    path = OUT / "N13 Nhóm 10 cấu trúc tham khảo ĐATN24.docx"
    d.save(path)
    return path


def build_comparison():
    d = Document()
    setup(d)
    para(d, "ĐÁNH GIÁ CẤU TRÚC VÀ NỘI DUNG BÁO CÁO NHÓM 10", "Title")
    para(d, "Đối chiếu Đatn24.pdf với N13 Nhóm 10.docx và phần nhận xét được cung cấp ngày 22 tháng 11 năm 2026.")
    heading(d, "Kết quả đánh giá", 2)
    para(d, "Phần nhận xét xác định đúng nhiều khoảng trống của báo cáo nhóm về mở đầu, tổ chức chương, đặc tả dữ liệu và kết luận. Tuy nhiên, nhận xét chưa đủ căn cứ để gọi tài liệu mẫu là chuẩn bắt buộc của PTIT, khẳng định UML của nhóm đầy đủ hơn về chất lượng hoặc ghép nguyên văn toàn bộ phần công nghệ và triển khai. Có thể áp dụng bố cục và cách dẫn giải; nội dung kỹ thuật phải kiểm chứng riêng.")
    heading(d, "Cấu trúc thực tế của tài liệu mẫu", 2)
    for text in [
        "Tệp có 92 trang PDF. Trang 1 là bìa; trang 2 đến 4 là các mẫu giao đề tài có nhiều chỗ trống và lặp; trang 5 là lời mở đầu; trang 6 đến 8 là mục lục, kèm bảng phân chia công việc ở trang 8; trang 9 đến 10 là danh mục hình.",
        "Chương I từ trang 11 đến 28 gồm lý do chọn đề tài, mục tiêu, kết quả dự kiến, lựa chọn công nghệ và kết luận chương. Chương II từ trang 29 đến 68 gồm yêu cầu, Use case, kịch bản, lớp thực thể, trình tự, mô tả các bảng dữ liệu, lược đồ CSDL và kết luận chương.",
        "Chương III từ trang 69 đến 89 trình bày môi trường và kết quả cài đặt theo từng chức năng. Kết luận bắt đầu ở trang 90; hướng phát triển tiếp tục sang trang 91; tài liệu tham khảo nằm tại trang 91; trang 92 gần như trống.",
        "Điểm nên học là mạch yêu cầu → kịch bản → mô hình → dữ liệu → giao diện, hệ thống đề mục, chú thích hình và kết luận chương. Với mỗi chức năng, báo cáo nhóm nên giải thích điều kiện và kết quả của hình, thay vì chỉ đặt hình liên tiếp.",
        "Tài liệu mẫu không có mục Danh mục bảng trong mục lục trích xuất. Việc bổ sung danh mục bảng cho nhóm là đề xuất phù hợp với số lượng bảng hiện tại, không phải chi tiết đã sao theo mẫu."
    ]:
        para(d, text)
    heading(d, "Đánh giá từng nhóm nhận xét", 2)
    findings = [
        ("Bìa và phần đầu", "Đúng một phần", "Báo cáo hiện tại đã có tên trường, khoa, logo, môn học, tên đề tài, lớp nhóm, giảng viên và bảng họ tên, mã sinh viên. Vì vậy, nói thiếu toàn bộ trang bìa là không chính xác. Thiếu phần mở đầu, mục lục và danh mục tự động; nên chuẩn hóa bìa thay vì tự thêm thông tin khóa hoặc hệ chưa xác nhận."),
        ("Tổ chức ba chương", "Nên áp dụng có điều chỉnh", "Giữ ba chương Tổng quan; Phân tích; Thiết kế. Không đặt tên chương III là Kết quả cài đặt khi tài liệu hiện có chủ yếu là wireframe, UML và SQL minh họa. Giữ bố cục phần phân tích và thiết kế của học phần."),
        ("Đặc tả CSDL", "Nên áp dụng", "ERD thực tế có 16 bảng. Có thể lập từ điển dữ liệu theo tên cột, kiểu, khóa và ý nghĩa. Phải tách ràng buộc có bằng chứng trên ERD với ràng buộc mới đề xuất; không coi bảng mô tả là DDL đã chạy."),
        ("Kiểu dữ liệu ERD", "Nhận xét đúng", "Hình ERD dùng integer cho tên, ảnh, địa chỉ và nhiều chuỗi; cần sửa nguồn mô hình và xuất lại. Nên chọn rõ VARCHAR, DECIMAL và một quy ước thời gian. Bản bổ sung chọn BIGINT theo giây để khớp UNIX_TIMESTAMP; không tùy ý đổi qua lại giữa BIGINT và DATETIME."),
        ("Quan hệ Use case tạo đơn", "Đúng về chiều, cần xét ngữ nghĩa", "Include đi từ ca sử dụng bao hàm đến ca được bao hàm; extend đi từ ca mở rộng đến ca cơ sở. Tuy nhiên không chỉ đảo mũi tên là xong: xác định loại đơn không nên include đặt món; chọn bàn là bước có điều kiện của đơn tại chỗ. Nếu tiếp tục dùng extend, extension point thuộc ca cơ sở, không đặt tại Chọn bàn như hình hiện tại [1]."),
        ("Nhãn biểu đồ trình tự", "Có cơ sở", "Các hình thiết kế tạo combo, gộp đơn và thanh toán có vùng nhãn dày, đường sống đi qua hoặc sát nhãn; cần điều chỉnh nguồn sơ đồ. Chỉ tăng kích thước ảnh trong Word không giải quyết nhãn chồng nhau bên trong ảnh."),
        ("Ánh xạ trạng thái", "Nên bổ sung", "SQL dùng 1 cho phục vụ, 3 cho đã thanh toán, 4 cho đã gộp; truy vấn thanh toán xét 1 và 2. Mã 5 cho đã hủy là bổ sung hợp lý nhưng là quyết định thiết kế mới, chưa có câu cập nhật tương ứng trong báo cáo gốc."),
        ("Java và MySQL", "Có căn cứ định hướng", "WAR và JDBC hỗ trợ định hướng Java Web; cú pháp SQL phù hợp MySQL. Chưa đủ căn cứ để khẳng định Spring Boot, Tomcat, JDK 17, REST/JSON hoặc một nhà cung cấp cụ thể đã được chọn và tích hợp. Java không tự bảo đảm ACID."),
        ("Môi trường phần cứng", "Không nên chép nguyên", "CPU 4 nhân, RAM 8 đến 16 GB, SSD 128 GB chưa có căn cứ tải hoặc phép đo. Chỉ mô tả thành phần triển khai và các thông số cần lựa chọn. Không biến ước lượng thành yêu cầu tối thiểu."),
        ("Giữ toàn bộ UML", "Giữ nội dung, chưa thể công nhận đúng hết", "Có thêm trạng thái, hoạt động, thành phần và triển khai cho thấy phạm vi loại biểu đồ rộng hơn mẫu. Số lượng loại biểu đồ không chứng minh tính đúng, đủ hoặc nhất quán. Chưa nên dùng câu khẳng định chuyên sâu hơn chỉ từ số lượng hình.")]
    for title, verdict, evidence in findings:
        heading(d, title + " " + verdict, 3)
        para(d, evidence)
    heading(d, "Các vấn đề phần nhận xét chưa phát hiện", 2)
    for text in [
        "Câu gộp món ON DUPLICATE KEY UPDATE chỉ chạy nhánh UPDATE khi có xung đột PRIMARY KEY hoặc UNIQUE. ERD chỉ thể hiện maOrderItem là khóa chính, nên một mã dòng mới không tự xung đột chỉ vì trùng maMon. Không được coi câu này là đã xử lý đúng việc cộng dồn món [2].",
        "Định nghĩa món trùng phải xét ít nhất mã món, đơn giá, tùy chọn và ghi chú. Gom mọi dòng chỉ theo mã món có thể làm mất giá đã chốt hoặc yêu cầu chế biến. Các thay đổi gộp đơn cần nằm trong giao dịch và kiểm tra cạnh tranh với thanh toán [3].",
        "Thiết kế cho phép mở nhiều hóa đơn trên một bàn, nhưng SQL thanh toán lại đưa bàn về trống ngay sau thanh toán một đơn. Cần kiểm tra còn đơn chưa kết thúc trên bàn trước khi giải phóng.",
        "Orders.tongTien được tính từ tổng tiền món; VAT và chiết khấu có cột nhưng chưa được đưa vào công thức SQL. Cần chốt giá trị nào là tạm tính, tiền phải thu và tiền đã thu; quy tắc làm tròn và tiền tip cần thống nhất.",
        "Biểu mẫu có mô tả combo nhưng Combo và MenuItem chưa có cột mô tả tương ứng. Chuyển khoản có trong kịch bản nhưng PaymentThe mới chỉ liệt kê loại thẻ. Không nên viết rằng mô hình 16 bảng đã hoàn toàn bao phủ các trường hợp này.",
        "Các mã lớp dùng String trong khi ERD và SQL dùng INT. Có thể thiết kế mã hiển thị khác mã nội bộ, nhưng phải nêu ánh xạ; không thể khẳng định khớp hoàn toàn.",
        "Một số hình khảo sát nhìn rõ giao diện Sapo FnB và khung video. Chúng chứng minh có tư liệu tham khảo POS, chưa đủ để xác nhận khảo sát thực địa hoặc phần mềm do nhóm tự xây dựng. Cần ghi nguồn chính xác của ảnh; nếu có biên bản khảo sát nhà hàng thì bổ sung riêng.",
        "Mẫu cũng có lỗi: mục lục ghi 2.6.6 giữa chuỗi 2.5 ở trang 7; hai bảng mang số 28 ở trang 67; kết luận chương II ở trang 68 nhắc nhầm hệ thống họp trực tuyến. Không nên sao chép các chi tiết này."
    ]:
        para(d, text)
    heading(d, "Những gì đã áp dụng trong bản Word mới", 2)
    for text in [
        "Dựng lại bìa từ thông tin đã có, giữ phân công gốc, thêm lời mở đầu và ba trường mục lục tự động: mục lục nội dung, danh mục hình, danh mục bảng. Không tự suy ra khóa hoặc hệ đào tạo.",
        "Tổ chức ba chương phù hợp bài tập lớn; chuyển đề mục sang Heading 1, Heading 2, Heading 3; đánh lại chú thích hình theo chương và bảng theo thứ tự; giữ 41 đối tượng ảnh và 26 bảng gốc, thêm 17 bảng đặc tả và quy ước dữ liệu.",
        "Bổ sung mục tiêu, phạm vi, kết quả dự kiến, định hướng công nghệ có căn cứ, từ điển 16 bảng, các quy tắc toàn vẹn, kết luận từng chương, môi trường triển khai dự kiến, kết luận chung và tài liệu tham khảo.",
        "Thay ví dụ ON DUPLICATE KEY UPDATE bằng thao tác chuyển dòng món sang đơn đích để không ngầm dựa vào khóa duy nhất chưa tồn tại. Đây vẫn là đoạn minh họa trong quy trình giao dịch, không phải thủ tục gộp đơn hoàn chỉnh đã kiểm thử.",
        "Phân biệt wireframe với kết quả cài đặt, đánh dấu mã hủy đơn là đề xuất và nêu rõ các khoảng trống về công thức tiền, chuyển khoản, mô tả combo và tài khoản. Các nội dung chưa có căn cứ như VNPay, JDK 17 và cấu hình phần cứng tối thiểu không được thêm như sự thật đã xác nhận."
    ]:
        para(d, text)
    heading(d, "Phần còn phải sửa trước khi coi là bản nộp", 2)
    para(d, "Bản mới là bản áp dụng cấu trúc và bổ sung nội dung có chọn lọc. Ảnh UML gốc được giữ để bảo toàn mô hình của nhóm; chưa chỉnh nguồn Visual Paradigm, chưa đảo quan hệ Use case trong ảnh, chưa đổi kiểu dữ liệu ngay trong ảnh ERD và chưa dàn lại nhãn các hình trình tự. Các điểm này vẫn cần xử lý; không được gọi bản này là đã sửa hết lỗi kỹ thuật.")
    para(d, "Sau khi sửa mô hình nguồn, cần đồng bộ ảnh, đặc tả dữ liệu và SQL; chốt quy tắc tính tiền và ba phương thức thanh toán; bổ sung nguồn ảnh khảo sát cụ thể; kiểm tra lại số trang, mục lục và độ đọc của các hình lớn. Chưa có kiểm thử MySQL hoặc tích hợp thanh toán trong lần đối chiếu này.")
    heading(d, "Tài liệu kiểm chứng", 2)
    for t in [
        "Nguồn nội bộ: Đatn24.pdf, 92 trang; code_pttk/docs/N13 Nhóm 10.docx; phần nhận xét người dùng gửi. Các số trang ở trên là số thứ tự trang PDF.",
        "[1] Visual Paradigm. Use Case Diagram Notations Guide. https://circle.visual-paradigm.com/docs/uml-and-sysml/use-case-diagram/use-case-diagram-notations-guide/",
        "[2] Oracle. MySQL 8.0 Reference Manual. INSERT ON DUPLICATE KEY UPDATE Statement. https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html",
        "[3] Oracle. MySQL 8.4 Reference Manual. Locking Reads. https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html",
        "Các trang kiểm chứng trực tuyến được truy cập ngày 22 tháng 11 năm 2026."
    ]:
        para(d, t)
    path = OUT / "Đánh giá đối chiếu ĐATN24 và nhận xét.docx"
    d.save(path)
    return path


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for path in (build_revision(), build_comparison()):
        print(path)
