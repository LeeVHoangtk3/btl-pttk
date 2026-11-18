import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def rel_path(p):
    return os.path.join(BASE_DIR, p)

def create_document():
    doc = docx.Document()

    # Set page margins (1 inch = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.2
    normal_style.paragraph_format.space_after = Pt(6)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, size=13, space_before=0, space_after=6, keep_with_next=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.keep_with_next = keep_with_next
        if text:
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_heading_1(text):
        return add_p(text, bold=True, size=15, space_before=14, space_after=6, keep_with_next=True)

    def add_heading_2(text):
        return add_p(text, bold=True, size=14, space_before=10, space_after=4, keep_with_next=True)

    def add_heading_3(text):
        return add_p(text, bold=True, size=13, space_before=8, space_after=4, keep_with_next=True)

    def add_img(img_path, caption="", max_width=6.3, max_height=7.3):
        full_path = rel_path(img_path) if not os.path.isabs(img_path) else img_path
        if os.path.exists(full_path):
            with Image.open(full_path) as im:
                w0, h0 = im.size
            aspect = w0 / float(h0)
            width_in = min(max_width, max_height * aspect)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = bool(caption)
            run = p.add_run()
            run.add_picture(full_path, width=Inches(width_in))
            if caption:
                cp = doc.add_paragraph()
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cp.paragraph_format.space_before = Pt(2)
                cp.paragraph_format.space_after = Pt(8)
                c_run = cp.add_run(caption)
                c_run.font.name = 'Times New Roman'
                c_run.font.size = Pt(12)
                c_run.font.italic = True
                c_run.font.color.rgb = RGBColor(0, 0, 0)
        else:
            raise FileNotFoundError(f"Missing image file: {full_path}")

    def set_cell_white_and_borders(cell):
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="FFFFFF"/>'))
        tcBorders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            </w:tcBorders>
        ''')
        tcPr.append(tcBorders)

    def add_custom_table(headers, data, col_widths=None):
        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            cell = hdr_cells[i]
            set_cell_white_and_borders(cell)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(header_text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)

        for row_idx, row_data in enumerate(data):
            row_cells = table.rows[row_idx + 1].cells
            for col_idx, cell_value in enumerate(row_data):
                cell = row_cells[col_idx]
                set_cell_white_and_borders(cell)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.line_spacing = 1.15

                if col_idx == 0 and len(str(cell_value)) <= 5:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT

                r = p.add_run(str(cell_value))
                r.font.name = 'Times New Roman'
                r.font.size = Pt(13)
                r.font.color.rgb = RGBColor(0, 0, 0)

        if col_widths:
            for row in table.rows:
                for idx, w in enumerate(col_widths):
                    row.cells[idx].width = Inches(w)

        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(0)
        p_space.paragraph_format.space_after = Pt(6)
        return table

    # ==========================================================================
    # TRANG BÌA & PHẦN I: THÔNG TIN NHÓM - ĐỀ TÀI - PHÂN CÔNG THÀNH VIÊN
    # ==========================================================================
    add_p("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=2)
    add_p("KHOA CÔNG NGHỆ THÔNG TIN 1", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=10)
    add_p("--------***--------", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_before=0, space_after=12)

    add_img('diagrams/extracted_media/image1.png', max_width=1.8, max_height=2.0)

    add_p("BÁO CÁO BÀI TẬP LỚN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=14, space_after=4)
    add_p("PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG THÔNG TIN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=0, space_after=16)

    add_heading_1("I. MÃ SỐ NHÓM, TÊN ĐỀ TÀI, HỌ TÊN CÁC THÀNH VIÊN – CHỨC NĂNG")
    add_p("• Nhóm môn học: Lớp N13 – Nhóm 10", bold=True)
    add_p("• Tên đề tài: Hệ thống quản lý nhà hàng Thanh Hoa", bold=True)
    add_p("• Giảng viên hướng dẫn: Nguyễn Đình Hiến", bold=True, space_after=10)
    add_p("Bảng phân công thành viên và chức năng phụ trách:", bold=True)

    members_data = [
        ["1", "Phan Việt Bảo", "B23DCKH006", "Tạo đơn hàng (Chọn bàn và đặt món)"],
        ["2", "Nguyễn Thanh Hòa", "B23DCKH042", "Thanh toán"],
        ["3", "Lê Việt Hoàng", "B23DCKH044", "Tạo combo (Quản lý thực đơn)"],
        ["4", "Ngô Văn Phương", "B23DCKH092", "Gộp đơn hàng (Xử lý đơn)"]
    ]
    add_custom_table(["STT", "Họ và tên", "Mã sinh viên", "Chức năng chính"], members_data, [0.6, 2.1, 1.5, 2.6])

    doc.add_page_break()

    # ==========================================================================
    # PHẦN II. TÀI LIỆU PHÂN TÍCH
    # ==========================================================================
    add_heading_1("II. TÀI LIỆU PHÂN TÍCH")

    # --------------------------------------------------------------------------
    # II.1. Khảo sát yêu cầu
    # --------------------------------------------------------------------------
    add_heading_2("1. Khảo sát yêu cầu")
    add_heading_3("a. Khảo sát hiện trạng và quy trình nghiệp vụ thực tế")
    add_p("Nhóm đã tiến hành khảo sát quy trình vận hành thực tế tại Nhà hàng Thanh Hoa kết hợp nghiên cứu quy trình nghiệp vụ chuẩn trên phần mềm quản lý bán hàng nhà hàng (POS F&B). Hoạt động phục vụ tại nhà hàng xoay quanh 4 nhóm nghiệp vụ cốt lõi:")

    add_p("1. Nghiệp vụ Quản lý thực đơn và Tạo Combo (Tác nhân: Quản lý):", bold=True)
    add_p("Quản lý nhà hàng cần thiết lập danh mục thực đơn (Món lẻ, Đồ uống, Sản phẩm đóng gói) và xây dựng các gói Combo ưu đãi theo số lượng khách (ví dụ: Combo Gia Đình 4 người, Combo Đôi Bạn). Khi tạo mới Combo, hệ thống cho phép chọn các món lẻ đang kinh doanh kèm số lượng tương ứng và tự động tính tổng giá trị gốc tham khảo để Quản lý ấn định mức giá bán Combo hợp lý.")
    add_img("chucnang/menu/images/mh_01_quan_ly_thuc_don_combo.jpg", "Hình khảo sát 1.1: Giao diện quản lý danh sách thực đơn và gói Combo", max_width=5.8)
    add_img("chucnang/menu/images/mh_02_bieu_mau_tao_combo_moi.jpg", "Hình khảo sát 1.2: Biểu mẫu thiết lập thông tin chung và chọn món lẻ thành phần cho Combo", max_width=5.8)

    add_p("2. Nghiệp vụ Chọn bàn và Tạo đơn hàng (Tác nhân: Nhân viên phục vụ / Nhân viên order):", bold=True)
    add_p("Nhà hàng được chia thành nhiều khu vực phục vụ (Tại chỗ, Mang về, Tầng 1, Tầng 2, Tầng Trệt). Nhân viên phục vụ quan sát trạng thái bàn trực quan trên sơ đồ (phân biệt rõ bàn trống màu xám và bàn đang phục vụ màu xanh), chọn bàn cho khách ngồi, tìm chọn món ăn/đồ uống/combo theo danh mục, nhập số lượng và ghi chú chế biến, sau đó lưu đơn và gửi lệnh in phiếu chế biến xuống bộ phận Bếp.")
    add_img("diagrams/survey/khao_sat_so_do_ban.jpg", "Hình khảo sát 1.3: Màn hình theo dõi sơ đồ bàn theo khu vực (Bàn trống / Bàn đang phục vụ)", max_width=5.8)
    add_img("diagrams/survey/khao_sat_chon_mon.jpg", "Hình khảo sát 1.4: Màn hình chọn món ăn theo danh mục và giỏ hàng tạm tính", max_width=5.8)

    add_p("3. Nghiệp vụ Xử lý đơn và Gộp đơn hàng (Tác nhân: Thu ngân / Nhân viên phục vụ):", bold=True)
    add_p("Trong quá trình khách dùng bữa, thường xuyên phát sinh nhu cầu ghép bàn hoặc thanh toán chung hóa đơn giữa nhiều bàn khác nhau. Hệ thống cung cấp các thao tác quản lý đơn tại bàn gồm: In hóa đơn tới bếp, Tạo hóa đơn mới trên bàn, Tách hóa đơn, Gộp hóa đơn, Hủy đơn (kèm lý do) và Di chuyển bàn. Khi thực hiện Gộp đơn hàng, hệ thống dồn toàn bộ món ăn từ các bàn nguồn về bàn đích, cộng dồn số lượng các món trùng nhau, tính lại tổng tiền và giải phóng các bàn nguồn về trạng thái Bàn trống.")
    add_img("diagrams/survey/khao_sat_xu_ly_gop_don.jpg", "Hình khảo sát 1.5: Menu các thao tác xử lý đơn hàng đang phục vụ (Gộp hóa đơn, Tách hóa đơn, Hủy đơn, Chuyển bàn)", max_width=5.8)

    add_p("4. Nghiệp vụ Thanh toán hóa đơn (Tác nhân: Thu ngân):", bold=True)
    add_p("Khi khách yêu cầu thanh toán, Thu ngân mở danh sách các đơn chờ thanh toán, chọn đơn của bàn tương ứng và lựa chọn phương thức thanh toán (Tiền mặt, Thẻ VISA/MasterCard/JCB/ATM hoặc Chuyển khoản). Với thanh toán tiền mặt, hệ thống hỗ trợ nhập số tiền khách đưa (hoặc chọn nhanh mệnh giá gợi ý), tự động tính tiền thừa trả khách, ghi nhận tiền Tip (nếu có), cập nhật trạng thái đơn thành Đã thanh toán, giải phóng bàn ăn và lưu lịch sử giao dịch.")
    add_img("diagrams/survey/khao_sat_thanh_toan.jpg", "Hình khảo sát 1.6: Giao diện chọn phương thức thanh toán, nhập tiền khách đưa và tính tiền thừa", max_width=5.8)
    add_img("diagrams/survey/khao_sat_thanh_toan_thanh_cong.jpg", "Hình khảo sát 1.7: Màn hình xác nhận thanh toán hóa đơn thành công và in hóa đơn", max_width=5.8)

    add_heading_3("b. Tổng hợp các tác nhân và yêu cầu chức năng của hệ thống")
    req_summary = [
        ["1", "Quản lý", "Quản lý thực đơn & Tạo combo", "Thêm/sửa/xóa món ăn lẻ (Dish); tạo mới, cập nhật và xóa gói Combo gồm nhiều món lẻ thành phần kèm số lượng; tính tổng giá gốc tham khảo."],
        ["2", "Nhân viên phục vụ (Order)", "Chọn bàn & Tạo đơn hàng", "Xem sơ đồ bàn theo khu vực; xác định loại đơn (Tại chỗ / Mang về); chọn bàn trống hoặc mở đơn đang có trên bàn; thêm món vào đơn, tính tổng tiền và in phiếu chế biến tới bếp."],
        ["3", "Thu ngân / Nhân viên phục vụ", "Xử lý đơn & Gộp đơn hàng", "Gộp nhiều đơn hàng từ các bàn đang phục vụ về một bàn đích duy nhất; cộng dồn món trùng, tính lại tổng tiền, giải phóng bàn nguồn và lưu nhật ký gộp đơn (OrderMergeLog)."],
        ["4", "Thu ngân", "Thanh toán hóa đơn", "Tra cứu danh sách đơn chờ thanh toán; chọn phương thức thanh toán (Tiền mặt / Thẻ); kiểm tra tiền nhận, tính tiền thừa, cập nhật đơn Đã thanh toán, giải phóng bàn và lưu PaymentLog."]
    ]
    add_custom_table(["STT", "Tác nhân", "Nhóm chức năng", "Mô tả yêu cầu nghiệp vụ"], req_summary, [0.5, 1.5, 1.7, 3.1])

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # II.2. Biểu đồ Use case cho hệ thống và cho các chức năng
    # --------------------------------------------------------------------------
    add_heading_2("2. Biểu đồ Use case cho hệ thống và cho các chức năng")

    add_heading_3("a. Hệ thống")
    add_img("diagrams/extracted_media/image4.jpg", "Hình 2.1: Biểu đồ Use case tổng quát cho hệ thống quản lý nhà hàng", max_width=5.6)

    add_heading_3("b. Quản lý menu (Tạo combo)")
    add_img("diagrams/extracted_media/image8.jpg", "Hình 2.2: Biểu đồ Use case phân hệ Quản lý menu", max_width=5.0)

    add_heading_3("c. Tạo đơn hàng")
    add_img("diagrams/extracted_media/image5.jpg", "Hình 2.3: Biểu đồ Use case chức năng Tạo đơn hàng (Order)", max_width=4.8)

    add_heading_3("d. Xử lý đơn (Gộp đơn hàng)")
    add_img("diagrams/extracted_media/image7.jpg", "Hình 2.4: Biểu đồ Use case phân hệ Xử lý đơn (Gộp đơn, Tách đơn, Hủy đơn)", max_width=5.2)

    add_heading_3("e. Thanh toán")
    add_img("diagrams/extracted_media/image3.jpg", "Hình 2.5: Biểu đồ Use case chức năng Thanh toán", max_width=4.8)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # II.3. Kịch bản cho các chức năng (Pha phân tích)
    # --------------------------------------------------------------------------
    add_heading_2("3. Kịch bản cho các chức năng")

    add_heading_3("a. Kịch bản Tạo combo")
    uc_tao_combo = [
        ["1", "Tác nhân", "Quản lý"],
        ["2", "Mô tả", "Quản lý thiết lập và tạo một gói Combo món ăn mới trên hệ thống, bao gồm các thông tin chung (tên combo, giá bán, số người ăn, mô tả) và danh sách các món lẻ thành phần kèm số lượng tương ứng."],
        ["3", "Điều kiện trước", "1. Quản lý đã đăng nhập thành công vào hệ thống với quyền hạn phù hợp.\n2. Hệ thống đã có sẵn danh mục và danh sách các món lẻ (Dish) đang hoạt động/kinh doanh để chọn làm món thành phần."],
        ["4", "Luồng sự kiện chính", "1. Quản lý truy cập vào màn hình Quản lý thực đơn (Menu).\n2. Quản lý nhấn chọn chức năng Tạo Combo mới (hoặc Thêm Combo).\n3. Hệ thống hiển thị biểu mẫu tạo Combo mới gồm: tên combo, giá bán, số người ăn, mô tả, ảnh đại diện (nếu có) và danh sách các món lẻ đang kinh doanh.\n4. Quản lý nhập các thông tin chung của Combo (tên combo, giá bán, số người ăn dự kiến, mô tả).\n5. Quản lý tìm kiếm hoặc tích chọn các món lẻ thành phần từ danh sách.\n6. Với mỗi món lẻ được chọn, Quản lý nhập số lượng tương ứng trong combo.\n7. Hệ thống tự động tính toán tổng giá trị gốc tham khảo của các món thành phần để quản lý cân đối giá combo.\n8. Quản lý kiểm tra lại toàn bộ thông tin và nhấn nút Lưu.\n9. Hệ thống kiểm tra tính hợp lệ của dữ liệu (tên hợp lệ, giá bán > 0, đã chọn ít nhất 1 món con...).\n10. Hệ thống khởi tạo sau đó hiển thị thông báo 'Tạo combo thành công' và làm mới lại danh sách thực đơn hiển thị combo mới."],
        ["5", "Luồng sự kiện phụ", "- Chưa có món lẻ trong hệ thống: Nếu thực đơn chưa có món lẻ nào, hệ thống hiển thị thông báo nhắc nhở và yêu cầu tạo món ăn lẻ trước khi tạo combo.\n- Hủy thao tác: Quản lý nhấn nút Hủy hoặc đóng biểu mẫu bất cứ lúc nào, hệ thống sẽ hủy bỏ dữ liệu đang nhập và quay lại danh sách thực đơn mà không lưu thay đổi.\n- Chỉnh sửa / Xóa món thành phần khi đang tạo: Quản lý có thể tăng/giảm số lượng hoặc bấm xóa bỏ một món lẻ đã chọn khỏi bảng chi tiết combo trước khi nhấn Lưu."],
        ["6", "Điều kiện sau", "Combo mới được ghi nhận thành công vào cơ sở dữ liệu hệ thống, hiển thị trên giao diện thực đơn và sẵn sàng cho nhân viên order chọn khi phục vụ khách hàng."],
        ["7", "Ngoại lệ", "- Thiếu dữ liệu bắt buộc: Nếu để trống tên combo, giá bán hoặc số người ăn, hệ thống hiển thị cảnh báo đỏ tại các ô nhập tương ứng và không cho phép lưu.\n- Giá trị không hợp lệ: Nhập giá bán ≤ 0 hoặc số lượng món thành phần ≤ 0, hệ thống cảnh báo 'Giá bán và số lượng món phải lớn hơn 0'.\n- Chưa chọn món thành phần: Quản lý nhấn Lưu nhưng chưa chọn món lẻ nào, hệ thống báo lỗi 'Combo phải chứa ít nhất một món ăn thành phần'.\n- Trùng tên combo: Nếu tên combo đã tồn tại trong hệ thống, hệ thống hiển thị thông báo 'Tên combo đã tồn tại, vui lòng chọn tên khác'."]
    ]
    add_custom_table(["STT", "Mục", "Nội dung"], uc_tao_combo, [0.6, 1.6, 4.6])

    add_heading_3("b. Kịch bản Tạo đơn hàng")
    uc_tao_don = [
        ["1", "Tác nhân", "Nhân viên order (Nhân viên phục vụ)"],
        ["2", "Mô tả", "Nhân viên chọn khu vực, bàn phục vụ (hoặc hóa đơn có sẵn) và tiến hành thêm các món ăn/thức uống vào đơn hàng."],
        ["3", "Điều kiện trước", "Nhân viên đã đăng nhập thành công vào hệ thống."],
        ["4", "Luồng sự kiện chính", "1. Nhân viên mở màn hình Sơ đồ / Chọn bàn.\n2. Hệ thống hiển thị danh sách khu vực (Tại chỗ, Mang về, Tầng 1, Tầng 2, Tầng Trệt...).\n3. Nhân viên chọn một khu vực.\n4. Hệ thống hiển thị danh sách bàn tương ứng, phân biệt rõ bàn trống và bàn đang phục vụ.\n5. Nhân viên chọn một bàn:\n- Nếu là bàn trống: Hệ thống khởi tạo và mở màn hình tạo đơn mới.\n- Nếu bàn đã có khách: Hệ thống hiển thị danh sách hóa đơn hiện có trên bàn để nhân viên chọn mở đơn cần xử lý.\n6. Nhân viên chọn danh mục món (Thức ăn, Nước uống, Sản phẩm đóng gói...).\n7. Hệ thống hiển thị danh sách các món thuộc danh mục đã chọn.\n8. Nhân viên tìm kiếm hoặc chọn trực tiếp món cần thêm.\n9. Nhân viên nhập số lượng và ghi chú/tùy chọn.\n10. Hệ thống thêm món vào đơn hàng và tự động cập nhật lại tổng tiền tạm tính.\n11. Nhân viên lặp lại bước 6–10 để thêm các món khác (nếu cần).\n12. Nhân viên nhấn Lưu để lưu tạm đơn hàng và gửi phiếu chế biến tới bếp."],
        ["5", "Luồng sự kiện phụ", "- Khu vực hết bàn trống: Hệ thống hiển thị thông báo và không cho tạo bàn mới tại khu vực đó.\n- Món hết hàng/ngừng phục vụ: Hệ thống hiển thị cảnh báo trạng thái bên cạnh món và khóa chức năng thêm món đó vào đơn."],
        ["6", "Điều kiện sau", "Đơn hàng gắn với bàn đã chọn được lưu thành công trên hệ thống kèm danh sách món và tổng tiền tương ứng; trạng thái bàn cập nhật thành Đang phục vụ."],
        ["7", "Ngoại lệ", "- Đơn hàng chưa có món: Nhân viên bấm Lưu khi chưa chọn món nào, hệ thống nhắc chọn ít nhất 1 món.\n- Lỗi kết nối máy in bếp: Báo lỗi in phiếu nhưng đơn hàng vẫn được lưu trên hệ thống để in lại."]
    ]
    add_custom_table(["STT", "Mục", "Nội dung"], uc_tao_don, [0.6, 1.6, 4.6])

    add_heading_3("c. Kịch bản Gộp đơn hàng")
    uc_gop_don = [
        ["1", "Tác nhân", "Thu ngân (hoặc Nhân viên phục vụ)"],
        ["2", "Mô tả", "Thu ngân thực hiện gộp các đơn hàng từ nhiều bàn khác nhau đang có khách về một bàn đích duy nhất và tự động tính toán lại hóa đơn tổng hợp trước khi giải phóng bàn nguồn."],
        ["3", "Điều kiện trước", "- Thu ngân đã đăng nhập thành công vào hệ thống với phân quyền hợp lệ.\n- Có ít nhất hai bàn đang ở trạng thái hoạt động (đang có khách, đã gọi món và chưa thanh toán)."],
        ["4", "Luồng sự kiện chính", "1. Nhân viên/Thu ngân nhấn nút Gộp đơn hàng từ thanh điều hướng hoặc màn hình quản lý sơ đồ bàn.\n2. Hệ thống mở cửa sổ pop-up/màn hình Gộp Đơn Hàng với bố cục thanh tiêu đề điều hướng và 3 phân vùng chính: Chọn bàn cần gộp, Chi tiết bàn đã chọn và Xem trước kết quả gộp.\n3. Hệ thống tải danh sách toàn bộ các bàn đang có khách (đang phục vụ và chưa thanh toán) hiển thị tại cột Chọn bàn cần gộp. Mỗi thẻ bàn gồm: tên bàn, số lượng khách và tổng tiền hiện thời.\n4. Nhân viên có thể tìm nhanh số bàn qua ô nhập liệu Tìm số bàn.\n5. Nhân viên nhấp chọn các bàn cần gộp lại với nhau (chọn tối thiểu từ 2 bàn trở lên; ví dụ chọn Bàn 1 và Bàn 3).\n6. Hệ thống tự động đẩy các bàn vừa chọn sang cột giữa (Chi tiết bàn đã chọn), liệt kê cụ thể danh sách từng món ăn kèm số lượng tương ứng của mỗi bàn.\n7. Hệ thống mặc định lấy bàn đầu tiên được chọn làm bàn đích (BÀN 01), đồng thời thực hiện tổng hợp dữ liệu và hiển thị bảng tính tại cột bên phải (Xem trước kết quả gộp về BÀN 01):\n- Gom các món giống nhau, tự động cộng dồn số lượng và thành tiền.\n- Tự động cộng tổng Tạm tính, áp dụng mức Giảm giá (voucher) (nếu có) và tính ra Tổng cộng thực thu sau cùng.\n8. Nhân viên đối soát lại toàn bộ danh sách món ăn, số lượng và tổng tiền, sau đó nhấn nút [ Xác nhận gộp đơn hàng ].\n9. Hệ thống thực thi xử lý nghiệp vụ:\n- Dồn toàn bộ danh sách món và số tiền mới vào đơn hàng của bàn đích (Bàn 1).\n- Đóng các đơn hàng gốc của các bàn nguồn (Bàn 3), giải phóng và chuyển trạng thái các bàn nguồn về Bàn trống.\n10. Hệ thống lưu vết nhật ký gộp đơn, hiển thị thông báo gộp đơn thành công và chuyển người dùng về màn hình Sơ đồ bàn."],
        ["5", "Luồng sự kiện phụ", "- 3.a. Tìm kiếm số bàn: Thu ngân nhập số bàn vào ô Tìm số bàn → Hệ thống lọc danh sách thời gian thực và chỉ hiển thị các bàn khớp từ khóa.\n- 7.a. Hủy thao tác: Thu ngân nhấn nút Hủy ở góc trên cùng bên trái → Hệ thống đóng modal, hủy bỏ mọi lựa chọn và giữ nguyên hiện trạng của tất cả các bàn."],
        ["6", "Điều kiện sau", "- Đơn hàng tại bàn đích nhận đầy đủ danh sách món, tiền tạm tính, voucher và tổng cộng mới.\n- Các bàn nguồn được đóng đơn đang phục vụ và chuyển trạng thái về bàn trống sẵn sàng đón khách mới.\n- Lịch sử thao tác gộp đơn được ghi nhận vào hệ thống."],
        ["7", "Ngoại lệ", "- 7.a. Chưa chọn đủ số bàn tối thiểu: Thu ngân chọn dưới 2 bàn mà nhấn Xác nhận gộp đơn hàng → Hệ thống hiển thị cảnh báo: 'Vui lòng chọn tối thiểu 2 bàn để thực hiện gộp đơn'.\n- 7.b. Không tìm thấy số bàn: Nhập số bàn không tồn tại hoặc bàn không có khách vào ô Tìm số bàn → Hệ thống hiển thị danh sách rỗng: 'Không tìm thấy bàn phù hợp'."]
    ]
    add_custom_table(["STT", "Mục", "Nội dung"], uc_gop_don, [0.6, 1.6, 4.6])

    add_heading_3("d. Kịch bản Thanh toán")
    uc_thanh_toan = [
        ["1", "Tác nhân", "Thu ngân"],
        ["2", "Mô tả", "Thu ngân thực hiện thanh toán cho đơn hàng của khách hàng bằng phương thức thanh toán được lựa chọn."],
        ["3", "Điều kiện trước", "Thu ngân đã đăng nhập thành công vào hệ thống. Đơn hàng đã được tạo và chưa được thanh toán."],
        ["4", "Luồng sự kiện chính", "1. Thu ngân chọn một đơn hàng cần thanh toán từ danh sách đơn chờ thanh toán.\n2. Hệ thống hiển thị thông tin đơn hàng và tổng số tiền cần thanh toán.\n3. Thu ngân chọn phương thức thanh toán: tiền mặt, chuyển khoản hoặc thẻ.\n4. Hệ thống hiển thị giao diện tương ứng với phương thức thanh toán đã chọn.\n5. Nếu thanh toán bằng tiền mặt, thu ngân nhập số tiền khách hàng đưa.\n6. Hệ thống kiểm tra số tiền và tính tiền thừa cho khách hàng.\n7. Thu ngân xác nhận thanh toán.\n8. Hệ thống lưu thông tin thanh toán, cập nhật trạng thái đơn hàng thành Đã thanh toán và giải phóng bàn ăn về trạng thái Trống.\n9. Hệ thống lưu lịch sử thanh toán và thông báo thanh toán thành công."],
        ["5", "Luồng sự kiện phụ", "- 5.a. Nếu số tiền khách đưa lớn hơn tổng tiền đơn hàng, hệ thống hiển thị số tiền thừa.\n- 5.b. Nếu thu ngân thay đổi phương thức thanh toán, hệ thống hiển thị lại giao diện tương ứng với phương thức mới."],
        ["6", "Điều kiện sau", "Đơn hàng được cập nhật trạng thái Đã thanh toán. Bàn ăn được giải phóng về trạng thái Trống. Thông tin thanh toán và lịch sử thanh toán được ghi nhận vào hệ thống."],
        ["7", "Ngoại lệ", "- 7.a. Đơn hàng đã được thanh toán → hệ thống thông báo và không thực hiện thanh toán lại.\n- 7.b. Số tiền khách đưa nhỏ hơn tổng tiền đơn hàng → hệ thống thông báo số tiền không đủ và yêu cầu nhập lại.\n- 7.c. Thanh toán bằng thẻ hoặc chuyển khoản thất bại → hệ thống thông báo thanh toán thất bại và yêu cầu thu ngân thực hiện lại hoặc chọn phương thức khác."]
    ]
    add_custom_table(["STT", "Mục", "Nội dung"], uc_thanh_toan, [0.6, 1.6, 4.6])

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # II.4. Biểu đồ lớp thực thể cho hệ thống và cho các chức năng (Pha phân tích)
    # --------------------------------------------------------------------------
    add_heading_2("4. Biểu đồ lớp thực thể cho hệ thống và cho các chức năng")

    add_heading_3("a. Hệ thống")
    add_img("diagrams/extracted_media/image12.png", "Hình 4.1: Biểu đồ lớp thực thể pha phân tích cho toàn hệ thống", max_width=6.3)

    add_heading_3("b. Quản lý menu (Tạo combo)")
    add_img("diagrams/extracted_media/image6.png", "Hình 4.2: Biểu đồ lớp thực thể pha phân tích cho Quản lý menu (Tạo combo)", max_width=4.6)

    add_heading_3("c. Tạo đơn hàng")
    add_img("diagrams/extracted_media/image9.png", "Hình 4.3: Biểu đồ lớp thực thể pha phân tích cho Tạo đơn hàng", max_width=4.6)

    add_heading_3("d. Gộp đơn hàng (Xử lý đơn)")
    add_img("diagrams/extracted_media/image2.png", "Hình 4.4: Biểu đồ lớp thực thể pha phân tích cho Gộp đơn hàng", max_width=3.2, max_height=5.5)

    add_heading_3("e. Thanh toán")
    add_img("diagrams/extracted_media/image13.png", "Hình 4.5: Biểu đồ lớp thực thể pha phân tích cho Thanh toán", max_width=4.6)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # II.5. Biểu đồ trình tự cho các chức năng (Pha phân tích)
    # --------------------------------------------------------------------------
    add_heading_2("5. Biểu đồ trình tự cho các chức năng")

    add_heading_3("a. Tạo combo")
    add_img("diagrams/generated/seq_pt_tao_combo.png", "Hình 5.1: Biểu đồ trình tự pha phân tích – Chức năng Tạo combo", max_width=6.3)

    add_heading_3("b. Tạo đơn hàng")
    add_img("diagrams/generated/seq_pt_tao_don.png", "Hình 5.2: Biểu đồ trình tự pha phân tích – Chức năng Tạo đơn hàng", max_width=6.3)

    add_heading_3("c. Gộp đơn hàng")
    add_img("diagrams/generated/seq_pt_gop_don.png", "Hình 5.3: Biểu đồ trình tự pha phân tích – Chức năng Gộp đơn hàng", max_width=6.3)

    add_heading_3("d. Thanh toán")
    add_img("diagrams/generated/seq_pt_thanh_toan.png", "Hình 5.4: Biểu đồ trình tự pha phân tích – Chức năng Thanh toán", max_width=6.3)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # II.6. Biểu đồ trạng thái cho các lớp
    # --------------------------------------------------------------------------
    add_heading_2("6. Biểu đồ trạng thái cho các lớp")

    add_heading_3("a. Lớp Đơn hàng (Order)")
    add_p("Lớp Order phản ánh vòng đời của một đơn hàng từ khi nhân viên khởi tạo trên bàn, thêm món và phục vụ khách, chuyển sang chờ thanh toán cho đến khi kết thúc ở một trong ba trạng thái: Đã thanh toán (DA_THANH_TOAN), Đã gộp sang đơn bàn đích (DA_GOP) hoặc Đã hủy (DA_HUY).")
    add_img("diagrams/generated/state_order.png", "Hình 6.1: Biểu đồ trạng thái của lớp Đơn hàng (Order)", max_width=6.3)

    add_heading_3("b. Lớp Bàn ăn (Table / RestaurantTable)")
    add_p("Lớp Table quản lý trạng thái vật lý của bàn ăn trên sơ đồ nhà hàng, luân chuyển giữa hai trạng thái chính là Bàn trống (TRONG) và Đang phục vụ (DANG_PHUC_VU) khi phát sinh các sự kiện tạo đơn mới, chuyển bàn, gộp đơn giải phóng bàn nguồn hoặc hoàn tất thanh toán.")
    add_img("diagrams/generated/state_table.png", "Hình 6.2: Biểu đồ trạng thái của lớp Bàn ăn (Table)", max_width=6.0)

    add_heading_3("c. Lớp Món ăn / Gói Combo (MenuItem / Combo)")
    add_p("Lớp MenuItem (bao gồm lớp con Dish và Combo) mô tả trạng thái kinh doanh của mặt hàng trên thực đơn từ lúc được Quản lý khởi tạo, đưa vào Đang kinh doanh, Tạm ngưng khi hết nguyên liệu hoặc Xóa khỏi thực đơn.")
    add_img("diagrams/generated/state_menuitem.png", "Hình 6.3: Biểu đồ trạng thái của lớp Món ăn / Combo (MenuItem)", max_width=6.2)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # II.7. Biểu đồ hành động cho các chức năng (Activity Diagram)
    # --------------------------------------------------------------------------
    add_heading_2("7. Biểu đồ hành động cho các chức năng")

    add_heading_3("a. Tạo combo")
    add_img("diagrams/generated/act_tao_combo.png", "Hình 7.1: Biểu đồ hành động (Activity Diagram) – Chức năng Tạo combo", max_width=5.6, max_height=7.2)

    add_heading_3("b. Tạo đơn hàng (Chọn bàn và đặt món)")
    add_img("chucnang/chon_ban_va_dat_mon/Activity Diagram1.jpg", "Hình 7.2: Biểu đồ hành động (Activity Diagram) – Chức năng Tạo đơn hàng", max_width=5.8, max_height=7.3)

    add_heading_3("c. Gộp đơn hàng")
    add_img("diagrams/generated/act_gop_don.png", "Hình 7.3: Biểu đồ hành động (Activity Diagram) – Chức năng Gộp đơn hàng", max_width=5.6, max_height=7.2)

    add_heading_3("d. Thanh toán")
    add_img("diagrams/generated/act_thanh_toan.png", "Hình 7.4: Biểu đồ hành động (Activity Diagram) – Chức năng Thanh toán", max_width=5.6, max_height=7.2)

    doc.add_page_break()

    # ==========================================================================
    # PHẦN III. TÀI LIỆU THIẾT KẾ
    # ==========================================================================
    add_heading_1("III. TÀI LIỆU THIẾT KẾ")

    # --------------------------------------------------------------------------
    # III.1. Kịch bản và thiết kế giao diện cho các chức năng
    # --------------------------------------------------------------------------
    add_heading_2("1. Kịch bản và thiết kế giao diện cho các chức năng")

    # a. Tao combo
    add_heading_3("a. Tạo combo")
    add_p("1. Quản lý truy cập vào màn hình Quản lý thực đơn (Menu).")
    add_p("2. Quản lý nhấn chọn chức năng Tạo Combo mới (hoặc Thêm Combo).")
    add_p("Giao diện Menu – thao tác tạo Combo:")
    menu_ui_data = [
        ["Danh mục", "Món lẻ | Combo | Đồ uống"],
        ["Danh sách", "Mì Ý Bò Bằm – 85.000đ\nCơm Gà – 65.000đ\nNước Cam – 25.000đ"],
        ["Thao tác", "[ + Tạo món mới ]   [ + Tạo Combo ]"]
    ]
    add_custom_table(["Màn hình", "Quản lý thực đơn (Menu)"], menu_ui_data, [2.2, 4.6])

    add_p("3. Hệ thống hiển thị biểu mẫu tạo Combo mới gồm: Tên combo, giá bán, số người ăn dự kiến, mô tả, ảnh đại diện (nếu có) và danh sách các món lẻ đang kinh doanh.")
    add_p("Biểu mẫu Tạo Combo mới:")
    combo_form_data = [
        ["Tên combo", "Combo Gia Đình"],
        ["Giá bán", "299.000 đ"],
        ["Số người ăn", "3 – 4 người"],
        ["Mô tả", "Mì Ý + gà + nước uống"],
        ["Ảnh đại diện", "[ Chọn ảnh ]"],
        ["Thành phần", "Danh sách món lẻ để tìm kiếm và lựa chọn"]
    ]
    add_custom_table(["Trường thông tin", "Dữ liệu"], combo_form_data, [2.2, 4.6])

    add_p("4. Quản lý nhập các thông tin chung của Combo: tên combo, giá bán, số người ăn dự kiến và mô tả.")
    add_p("5. Quản lý tìm kiếm hoặc tích chọn các món lẻ thành phần.")
    add_p("Danh sách món lẻ – chọn thành phần Combo:")
    dish_select_data = [
        ["Tìm kiếm", "[ mì ] .................................. [ Tìm ]"],
        ["Chọn", "☑ Mì Ý Bò Bằm – 85.000 đ - SL: 1"],
        ["Chọn", "☑ Gà Nướng – 120.000 đ - SL: 1"],
        ["Chọn", "☐ Cơm Chiên – 60.000 đ"],
        ["Chọn", "☑ Nước Cam – 25.000 đ - SL: 2"],
        ["Đã chọn", "3 món"]
    ]
    add_custom_table(["Mục chọn", "Nội dung"], dish_select_data, [2.0, 4.8])

    add_p("6. Với mỗi món lẻ được chọn, Quản lý nhập số lượng tương ứng trong Combo (ví dụ: 1 phần mì Ý, 2 ly nước).")
    add_p("7. Hệ thống tự động tính toán tổng giá trị gốc tham khảo của các món thành phần để Quản lý cân đối giá Combo.")
    add_p("8. Quản lý kiểm tra lại toàn bộ thông tin và nhấn nút Lưu.")
    add_p("9. Hệ thống kiểm tra tính hợp lệ của dữ liệu: tên hợp lệ, giá bán > 0, đã chọn ít nhất 1 món con và số lượng các món thành phần hợp lệ.")
    add_p("10. Hệ thống khởi tạo sau đó hiển thị thông báo “Tạo combo thành công” và làm mới danh sách thực đơn để hiển thị Combo mới.")
    add_p("Menu sau khi tạo Combo thành công:")
    menu_after_combo = [
        ["Thông báo", "✓ Tạo combo thành công"],
        ["Danh sách Menu", "Mì Ý Bò Bằm – 85.000 đ\nGà Nướng – 120.000 đ\nCombo Gia Đình – 299.000 đ"],
        ["Trạng thái Combo", "Đang kinh doanh"],
        ["Thao tác", "[ Xem ]   [ Sửa ]   [ Xóa ]"]
    ]
    add_custom_table(["Mục", "Nội dung hiển thị"], menu_after_combo, [2.0, 4.8])

    # b. Tao don hang
    add_heading_3("b. Tạo đơn hàng")
    add_p("1. Nhân viên mở màn hình Sơ đồ / Chọn bàn.")
    add_p("2. Hệ thống hiển thị danh sách khu vực (Tại chỗ, Mang về, Tầng 1, Tầng 2, Tầng Trệt...).")
    add_p("3. Nhân viên chọn một khu vực.")
    add_p("4. Hệ thống hiển thị danh sách bàn tương ứng, phân biệt rõ bàn trống và bàn đang phục vụ.")
    table_map_data = [
        ["Tại chỗ", "Bàn 0", "Bàn 1", "Bàn 2", "Bàn 3", "Bàn 4"],
        ["Mang về", "Bàn 5", "Bàn 6", "Bàn 7", "Bàn 8", "Bàn 9"],
        ["Tầng 1", "(trống)", "(trống)", "(trống)", "(trống)", "(trống)"],
        ["Tầng 2", "", "", "", "", ""]
    ]
    add_custom_table(["Khu vực", "Vị trí 1", "Vị trí 2", "Vị trí 3", "Vị trí 4", "Vị trí 5"], table_map_data, [1.4, 1.1, 1.1, 1.1, 1.1, 1.0])

    add_p("5. Nhân viên chọn một bàn:")
    add_p("- Nếu là bàn trống: Hệ thống khởi tạo và mở màn hình tạo đơn mới.")
    add_p("- Nếu bàn đã có khách: Hệ thống hiển thị danh sách hóa đơn hiện có trên bàn để nhân viên chọn mở đơn cần xử lý.")
    add_p("6. Nhân viên chọn danh mục món (Thức ăn, Nước uống, Sản phẩm đóng gói...).")
    order_cart_data = [
        ["Thức ăn", "Cơm chay — 50.000đ", "Cơm chay  x1"],
        ["Nước uống", "Cơm gà — 200.000đ", "Kem  x1"],
        ["Sản phẩm đóng gói", "Kem — 100.000đ", "Tổng tiền: 350.000đ"],
        ["Khác", "Trái cây — 130.000đ", "[ Lưu ]   [ Thanh toán ]"]
    ]
    add_custom_table(["Danh mục", "Danh sách món (Tên món — Giá)", "Giỏ hàng"], order_cart_data, [1.8, 2.6, 2.4])

    add_p("7. Hệ thống hiển thị danh sách các món thuộc danh mục đã chọn.")
    add_p("8. Nhân viên chọn trực tiếp món cần thêm.")
    add_p("9. Nhân viên nhập số lượng, chọn tùy chọn hoặc thêm ghi chú cho món (nếu có).")
    qty_data = [
        ["Số lượng", "2"],
        ["Xác nhận", "[ Xác nhận ]"]
    ]
    add_custom_table(["Trường", "Giá trị"], qty_data, [2.5, 4.3])

    add_p("10. Hệ thống thêm món vào đơn hàng và tự động cập nhật lại tổng tiền tạm tính.")
    add_p("11. Nhân viên lặp lại bước 6–10 để thêm các món khác (nếu cần).")
    add_p("12. Nhân viên nhấn Lưu để lưu tạm đơn hàng, trở về màn hình chính.")

    # c. Gop don hang
    add_heading_3("c. Gộp đơn hàng")
    add_p("1. Nhân viên/Thu ngân nhấn nút Gộp đơn hàng từ thanh điều hướng hoặc màn hình quản lý sơ đồ bàn.")
    add_p("2. Hệ thống mở cửa sổ pop-up/màn hình Gộp Đơn Hàng với bố cục thanh tiêu đề điều hướng và 3 phân vùng chính: Chọn bàn cần gộp, Chi tiết bàn đã chọn và Xem trước kết quả gộp.")
    gop_nav = [
        ["[ Hủy ]", "Gộp Đơn Hàng", "[ Xác nhận gộp đơn hàng ]"]
    ]
    add_custom_table(["Thao tác", "Tiêu đề", "Xác nhận"], gop_nav, [2.0, 2.8, 2.0])

    add_p("3. Hệ thống tải danh sách toàn bộ các bàn đang có khách (đang phục vụ và chưa thanh toán) hiển thị tại cột Chọn bàn cần gộp. Mỗi thẻ bàn gồm: tên bàn, số lượng khách và tổng tiền hiện thời.")
    add_p("4. Nhân viên có thể tìm nhanh số bàn qua ô nhập liệu Tìm số bàn.")
    table_select_gop = [
        ["Tìm số bàn:", "[ Tìm số bàn... ]"],
        ["Bàn 1", "4 khách — 900.000đ"],
        ["Bàn 7", "2 khách — 300.000đ"],
        ["Bàn 3", "1 khách — 360.000đ"],
        ["Bàn 4", "4 khách — 500.000đ"]
    ]
    add_custom_table(["Chọn bàn cần gộp", "Thông tin chi tiết"], table_select_gop, [2.4, 4.4])

    add_p("5. Nhân viên nhấp chọn các bàn cần gộp lại với nhau (chọn tối thiểu từ 2 bàn trở lên; ví dụ ở đây nhân viên chọn Bàn 1 và Bàn 3).")
    add_p("6. Hệ thống tự động đẩy các bàn vừa chọn sang cột giữa (Chi tiết bàn đã chọn), liệt kê cụ thể danh sách từng món ăn kèm số lượng tương ứng của mỗi bàn.")
    col2_gop_data = [
        ["Bàn 1", "• Lẩu thái x 1\n• Bò nhúng dấm x 1"],
        ["Bàn 3", "• Bia Tiger x 10\n• Đậu phộng rang x 2"]
    ]
    add_custom_table(["Chi tiết bàn đã chọn", "Danh sách món"], col2_gop_data, [2.4, 4.4])

    add_p("7. Hệ thống mặc định lấy bàn đầu tiên được chọn làm bàn đích (ở đây là BÀN 01), đồng thời thực hiện tổng hợp dữ liệu và hiển thị bảng tính tại cột bên phải (Xem trước kết quả gộp về BÀN 01):")
    add_p("- Gom các món giống nhau, tự động cộng dồn số lượng và thành tiền.")
    add_p("- Tự động cộng tổng Tạm tính, áp dụng mức Giảm giá (voucher) (nếu có) và tính ra Tổng cộng thực thu sau cùng.")
    col3_gop_data = [
        ["Lẩu thái x 1", "500.000đ"],
        ["Bò nhúng dấm x 1", "400.000đ"],
        ["Đậu phộng rang x 2", "60.000đ"],
        ["Bia Tiger x 10", "300.000đ"],
        ["Tạm tính", "1.260.000đ"],
        ["Giảm giá (voucher)", "60.000đ"],
        ["Tổng cộng", "1.200.000đ"]
    ]
    add_custom_table(["Xem trước kết quả gộp về BÀN 01", "Thành tiền"], col3_gop_data, [3.8, 3.0])

    add_p("8. Nhân viên đối soát lại toàn bộ danh sách món ăn, số lượng và tổng tiền:")
    add_p("- Trường hợp hủy bỏ: Nhân viên nhấn nút [ Hủy ] ở góc trên bên trái; hệ thống đóng giao diện gộp đơn và giữ nguyên hiện trạng của tất cả các bàn.")
    add_p("- Trường hợp đồng ý gộp: Nhân viên nhấn nút [ Xác nhận gộp đơn hàng ] ở góc trên bên phải.")
    add_p("9. Hệ thống thực thi xử lý nghiệp vụ:")
    add_p("- Dồn toàn bộ danh sách món và số tiền mới vào đơn hàng của bàn đích (Bàn 1).")
    add_p("- Đóng các đơn hàng gốc của các bàn nguồn (Bàn 3), giải phóng và chuyển trạng thái các bàn nguồn về Bàn trống.")
    add_p("10. Hệ thống lưu vết nhật ký gộp đơn và chuyển người dùng về màn hình Sơ đồ bàn.")

    # d. Thanh toan
    add_heading_3("d. Thanh toán")
    add_p("1. Nhân viên mở màn hình Danh sách đơn chờ thanh toán.")
    add_p("2. Hệ thống hiển thị danh sách các đơn hàng chưa thanh toán, gồm mã đơn, bàn, tổng tiền và thao tác chọn đơn.")
    payment_list_data = [
        ["1", "HD001", "Bàn 9", "350.000đ", "[ CHỌN ]"],
        ["2", "HD002", "Bàn 5", "520.000đ", "[ CHỌN ]"],
        ["3", "HD003", "Bàn 2", "270.000đ", "[ CHỌN ]"]
    ]
    add_custom_table(["STT", "Mã đơn", "Bàn", "Tổng tiền", "Thao tác"], payment_list_data, [0.6, 1.4, 1.4, 1.8, 1.6])

    add_p("3. Nhân viên chọn một đơn hàng cần thanh toán, ví dụ HD001.")
    add_p("4. Hệ thống hiển thị thông tin đơn hàng và yêu cầu nhân viên chọn phương thức thanh toán.")
    pay_choose_data = [
        ["Mã đơn", "HD001"],
        ["Bàn", "Bàn 9"],
        ["Tổng tiền", "350.000đ"],
        ["Phương thức thanh toán", "[ Tiền mặt ]   [ Chuyển khoản ]"]
    ]
    add_custom_table(["Thanh toán – HD001", "Thông tin"], pay_choose_data, [2.4, 4.4])

    add_p("5. Nhân viên chọn một phương thức thanh toán.")
    add_p("Nếu chọn Tiền mặt:")
    add_p("- Hệ thống hiển thị giao diện nhập số tiền khách đưa.")
    add_p("- Nhân viên nhập số tiền khách đưa và tiền tip nếu có.")
    cash_pay_data = [
        ["Tổng tiền", "350.000đ"],
        ["Số tiền khách đưa", "[ 400.000 ] đ"],
        ["Tiền thừa", "50.000đ"],
        ["Tiền tip", "[ 0 ] đ"],
        ["Thao tác", "[ XÁC NHẬN ]"]
    ]
    add_custom_table(["Thanh toán bằng tiền mặt", "Chi tiết"], cash_pay_data, [2.4, 4.4])

    add_p("6. Hệ thống kiểm tra số tiền khách đưa và tính tiền thừa.")
    add_p("7. Nhân viên kiểm tra thông tin và nhấn Xác nhận.")
    confirm_pay_data = [
        ["Mã đơn", "HD001"],
        ["Bàn", "Bàn 9"],
        ["Tổng tiền", "350.000đ"],
        ["Phương thức", "Tiền mặt"],
        ["Số tiền khách đưa", "400.000đ"],
        ["Tiền thừa", "50.000đ"],
        ["Thao tác", "[ HỦY ]   [ THANH TOÁN ]"]
    ]
    add_custom_table(["Xác nhận thanh toán", "Chi tiết"], confirm_pay_data, [2.4, 4.4])

    add_p("8. Hệ thống xử lý thanh toán:")
    add_p("- Nếu thanh toán thành công, hệ thống lưu thông tin thanh toán và lưu lịch sử thanh toán.")
    add_p("- Hệ thống cập nhật trạng thái đơn hàng thành Đã thanh toán và thông báo kết quả.")
    pay_success_data = [
        ["Mã đơn", "HD001"],
        ["Bàn", "Bàn 9"],
        ["Tổng tiền", "350.000đ"],
        ["Phương thức", "Tiền mặt"],
        ["Tiền thừa", "50.000đ"],
        ["Thao tác", "[ ĐÓNG ]"]
    ]
    add_custom_table(["Thanh toán thành công!", "Chi tiết"], pay_success_data, [2.4, 4.4])

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # III.2. Lược đồ quan hệ thực thể cho hệ thống. Truy vấn cho các chức năng
    # --------------------------------------------------------------------------
    add_heading_2("2. Lược đồ quan hệ thực thể cho hệ thống. Truy vấn cho các chức năng")

    add_heading_3("a. Lược đồ quan hệ thực thể (ERD) cho hệ thống")
    add_img("chucnang/chon_ban_va_dat_mon/ERD Nha hang Thanh Hoa.jpg", "Lược đồ quan hệ thực thể (ERD) cho hệ thống", max_width=6.3)

    add_heading_3("b. Truy vấn cho các chức năng")
    add_p("1. Truy vấn cho chức năng: Tạo combo", bold=True)
    sql_combo = [
        ["Lấy danh sách món lẻ đang kinh doanh", "SELECT m.maMon, m.tenMon, m.gia, d.loaiMon\nFROM MenuItem m\nJOIN Dish d ON m.maMon = d.maMon\nWHERE m.dangKinhDoanh = 1;"],
        ["Kiểm tra trùng tên combo", "SELECT COUNT(*)\nFROM MenuItem\nWHERE tenMon = 'Combo Gia Đình' AND kieuMon = 2;"],
        ["Thêm mới Combo vào bảng MenuItem và Combo", "INSERT INTO MenuItem (maMon, tenMon, gia, dangKinhDoanh, kieuMon, maDanhMuc)\nVALUES (301, 'Combo Gia Đình', 299000, 1, 2, 103);\nINSERT INTO Combo (maMon, soLuongNguoiAn)\nVALUES (301, 4);"],
        ["Thêm các món lẻ con vào ComboDetail", "INSERT INTO ComboDetail (maCombo, maMonLe, soLuong, ghiChu)\nVALUES (301, 101, 1, 'Mì Ý bò bằm'),\n       (301, 105, 1, 'Gà nướng nguyên con'),\n       (301, 202, 2, 'Nước cam');"],
        ["Tính tổng giá gốc tham khảo của combo", "SELECT SUM(m.gia * cd.soLuong) AS tongGiaGoc\nFROM ComboDetail cd\nJOIN MenuItem m ON cd.maMonLe = m.maMon\nWHERE cd.maCombo = 301;"]
    ]
    add_custom_table(["Tác vụ", "Truy vấn SQL chuẩn theo ERD"], sql_combo, [2.4, 4.4])

    add_p("2. Truy vấn cho chức năng: Tạo đơn hàng", bold=True)
    sql_order = [
        ["Lấy danh sách bàn theo khu vực và trạng thái", "SELECT t.maBan, t.soBan, t.trangThai, a.tenKhuVuc\nFROM RestaurantTable t\nJOIN Area a ON t.maKhuVuc = a.maKhuVuc\nWHERE a.maKhuVuc = 1;"],
        ["Tạo mới đơn hàng (Orders) và đơn tại chỗ (OrderTaiCho)", "INSERT INTO Orders (maDon, thoiGianTao, trangThai, tongTien, vat, chietKhau)\nVALUES (501, UNIX_TIMESTAMP(), 1, 0, 8, 0);\nINSERT INTO OrderTaiCho (maDon, maBan)\nVALUES (501, 1);"],
        ["Cập nhật trạng thái bàn sang Đang phục vụ", "UPDATE RestaurantTable\nSET trangThai = 2\nWHERE maBan = 1;"],
        ["Thêm món vào đơn hàng (OrderItem)", "INSERT INTO OrderItem (maOrderItem, maDon, maMon, soLuong, donGia, ghiChu, tuyChon)\nVALUES (1001, 501, 101, 2, 85000, 'Ít cay', 'Mì mềm');"],
        ["Cập nhật lại tổng tiền đơn hàng", "UPDATE Orders\nSET tongTien = (SELECT SUM(soLuong * donGia) FROM OrderItem WHERE maDon = 501)\nWHERE maDon = 501;"]
    ]
    add_custom_table(["Tác vụ", "Truy vấn SQL chuẩn theo ERD"], sql_order, [2.4, 4.4])

    add_p("3. Truy vấn cho chức năng: Gộp đơn hàng", bold=True)
    sql_gop = [
        ["Lấy danh sách bàn đang phục vụ để gộp", "SELECT o.maDon, t.maBan, t.soBan, o.tongTien\nFROM Orders o\nJOIN OrderTaiCho otc ON o.maDon = otc.maDon\nJOIN RestaurantTable t ON otc.maBan = t.maBan\nWHERE o.trangThai = 1;"],
        ["Lấy chi tiết món của các bàn cần gộp", "SELECT maMon, soLuong, donGia, ghiChu, tuyChon\nFROM OrderItem\nWHERE maDon = 503;"],
        ["Dồn món sang đơn bàn đích (Bàn 1)", "INSERT INTO OrderItem (maOrderItem, maDon, maMon, soLuong, donGia, ghiChu, tuyChon)\nVALUES (1005, 501, 205, 10, 30000, 'Gộp từ Bàn 3', 'Bia ướp lạnh')\nON DUPLICATE KEY UPDATE soLuong = soLuong + VALUES(soLuong);"],
        ["Cập nhật lại tổng tiền đơn hàng đích", "UPDATE Orders\nSET tongTien = (SELECT SUM(soLuong * donGia) FROM OrderItem WHERE maDon = 501)\nWHERE maDon = 501;"],
        ["Đóng đơn hàng nguồn và giải phóng bàn", "UPDATE Orders SET trangThai = 4 WHERE maDon = 503;\nUPDATE RestaurantTable SET trangThai = 1 WHERE maBan = 3;"],
        ["Ghi nhật ký gộp đơn vào OrderMergeLog", "INSERT INTO OrderMergeLog (maLog, maDonDich, maDonNguon, thoiGian, nhanVien)\nVALUES (1, 501, 503, UNIX_TIMESTAMP(), 'Thu ngân 01');"]
    ]
    add_custom_table(["Tác vụ", "Truy vấn SQL chuẩn theo ERD"], sql_gop, [2.4, 4.4])

    add_p("4. Truy vấn cho chức năng: Thanh toán", bold=True)
    sql_pay = [
        ["Lấy danh sách đơn chờ thanh toán", "SELECT o.maDon, t.soBan, o.tongTien, o.thoiGianTao\nFROM Orders o\nJOIN OrderTaiCho otc ON o.maDon = otc.maDon\nJOIN RestaurantTable t ON otc.maBan = t.maBan\nWHERE o.trangThai IN (1, 2);"],
        ["Lưu thông tin thanh toán tiền mặt", "INSERT INTO Payment (maThanhToan, maDon, tongTienDon, thoiGianThanhToan)\nVALUES (801, 501, 350000, UNIX_TIMESTAMP());\nINSERT INTO PaymentTienMat (maThanhToan, tienDaNhan, tienThua, tienTip)\nVALUES (801, 400000, 50000, 0);"],
        ["Cập nhật trạng thái đơn hàng thành Đã thanh toán", "UPDATE Orders\nSET trangThai = 3\nWHERE maDon = 501;"],
        ["Giải phóng bàn ăn về trạng thái Trống", "UPDATE RestaurantTable\nSET trangThai = 1\nWHERE maBan = (SELECT maBan FROM OrderTaiCho WHERE maDon = 501);"],
        ["Ghi nhật ký thanh toán vào PaymentLog", "INSERT INTO PaymentLog (maLog, maThanhToan, maDon, tongTien, thoiGian, nhanVien)\nVALUES (1, 801, 501, 350000, UNIX_TIMESTAMP(), 'Thu ngân 01');"]
    ]
    add_custom_table(["Tác vụ", "Truy vấn SQL chuẩn theo ERD"], sql_pay, [2.4, 4.4])

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # III.3. Biểu đồ lớp cho hệ thống và cho các chức năng (Pha thiết kế)
    # --------------------------------------------------------------------------
    add_heading_2("3. Biểu đồ lớp cho hệ thống và cho các chức năng")

    add_heading_3("a. Hệ thống")
    add_img("diagrams/extracted_media/image15.png", "Biểu đồ lớp thiết kế cho hệ thống", max_width=6.3)

    add_heading_3("b. Quản lý menu (Tạo combo)")
    add_img("diagrams/extracted_media/image16.png", "Biểu đồ lớp thiết kế cho Quản lý menu", max_width=5.0)

    add_heading_3("c. Tạo đơn hàng")
    add_img("chucnang/chon_ban_va_dat_mon/Class Diagram - Pha thiết kế_ Chọn bàn và đặt món.jpg", "Biểu đồ lớp thiết kế cho Tạo đơn hàng (Chọn bàn và đặt món)", max_width=6.3)

    add_heading_3("d. Gộp đơn hàng")
    add_img("diagrams/extracted_media/image14.png", "Biểu đồ lớp thiết kế cho Gộp đơn hàng", max_width=4.6)

    add_heading_3("e. Thanh toán")
    add_img("diagrams/extracted_media/image10.png", "Biểu đồ lớp thiết kế cho Thanh toán", max_width=4.6)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # III.4. Biểu đồ trình tự cho các chức năng (Pha thiết kế)
    # --------------------------------------------------------------------------
    add_heading_2("4. Biểu đồ trình tự cho các chức năng")

    add_heading_3("a. Tạo combo")
    add_img("diagrams/generated/seq_tao_combo.png", "Biểu đồ trình tự thiết kế: Chức năng Tạo combo", max_width=6.3)

    add_heading_3("b. Tạo đơn hàng")
    add_img("chucnang/chon_ban_va_dat_mon/Sequence Diagram - Chọn bàn và đặt món.jpg", "Biểu đồ trình tự thiết kế: Chức năng Tạo đơn hàng (Chọn bàn và đặt món)", max_width=6.3)

    add_heading_3("c. Gộp đơn hàng")
    add_img("diagrams/generated/seq_gop_don.png", "Biểu đồ trình tự thiết kế: Chức năng Gộp đơn hàng", max_width=6.3)

    add_heading_3("d. Thanh toán")
    add_img("diagrams/generated/seq_thanh_toan.png", "Biểu đồ trình tự thiết kế: Chức năng Thanh toán", max_width=6.3)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # III.5. Biểu đồ thành phần cho hệ thống
    # --------------------------------------------------------------------------
    add_heading_2("5. Biểu đồ thành phần cho hệ thống")
    add_img("diagrams/generated/component_system_corrected.png", "Biểu đồ thành phần cho hệ thống", max_width=6.3)

    # --------------------------------------------------------------------------
    # III.6. Biểu đồ triển khai cho hệ thống
    # --------------------------------------------------------------------------
    add_heading_2("6. Biểu đồ triển khai cho hệ thống")
    add_img("diagrams/system/Biểu đồ triển khai - Hệ thống quản lý nhà hàng.jpg", "Biểu đồ triển khai cho hệ thống", max_width=6.3)

    output_paths = [
        rel_path("docs/N13_Nhom10.docx"),
        rel_path("docs/N13 Nhóm 10.docx")
    ]
    for out_p in output_paths:
        doc.save(out_p)
        print(f"Document successfully updated: {out_p}")

if __name__ == '__main__':
    create_document()
