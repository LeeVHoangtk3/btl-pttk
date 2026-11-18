import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_document():
    doc = docx.Document()

    # Set page margins (1 inch = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.2
    normal_style.paragraph_format.space_after = Pt(6)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, size=13, space_before=0, space_after=6):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.2
        if text:
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_heading_1(text):
        return add_p(text, bold=True, size=15, space_before=14, space_after=6)

    def add_heading_2(text):
        return add_p(text, bold=True, size=14, space_before=10, space_after=4)

    def add_heading_3(text):
        return add_p(text, bold=True, size=13, space_before=8, space_after=4)

    def add_img(img_path, caption="", width=Inches(6.2)):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run()
            run.add_picture(img_path, width=width)
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
            add_p(f"[Hình ảnh chưa tìm thấy: {img_path}]", italic=True)

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
        
        # Header row
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
            
        # Data rows
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
                
                if col_idx == 0 and len(cell_value) <= 5:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT

                r = p.add_run(cell_value)
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
    # TRANG BÌA & THÔNG TIN DỰ ÁN
    # ==========================================================================
    add_p("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=2)
    add_p("KHOA CÔNG NGHỆ THÔNG TIN 1", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=10)
    add_p("--------***--------", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_before=0, space_after=12)

    if os.path.exists('extracted_media/image1.png'):
        add_img('extracted_media/image1.png', width=Inches(1.8))

    add_p("BÁO CÁO BÀI TẬP LỚN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=14, space_after=4)
    add_p("PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG THÔNG TIN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=0, space_after=12)
    add_p("Đề tài: Hệ thống quản lý nhà hàng Thanh Hoa", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=6)
    add_p("PHẦN III: TÀI LIỆU THIẾT KẾ", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=4, space_after=14)

    add_p("Nhóm thực hiện: Nhóm 10", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_before=0, space_after=2)
    add_p("Giảng viên hướng dẫn: Nguyễn Đình Hiến", align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_before=0, space_after=16)

    members_data = [
        ["1", "Phan Việt Bảo", "B23DCKH006", "Tạo đơn hàng"],
        ["2", "Nguyễn Thanh Hòa", "B23DCKH042", "Thanh toán"],
        ["3", "Lê Việt Hoàng", "B23DCKH044", "Tạo combo"],
        ["4", "Ngô Văn Phương", "B23DCKH092", "Gộp đơn hàng"]
    ]
    add_custom_table(["STT", "Họ và tên", "Mã sinh viên", "Chức năng"], members_data, [0.6, 2.2, 1.6, 2.4])

    doc.add_page_break()

    # ==========================================================================
    # PHẦN III. TÀI LIỆU THIẾT KẾ
    # ==========================================================================
    add_heading_1("III. TÀI LIỆU THIẾT KẾ")

    # --------------------------------------------------------------------------
    # 1. Kịch bản và thiết kế giao diện cho các chức năng
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
    # 2. Lược đồ quan hệ thực thể cho hệ thống. Truy vấn cho các chức năng
    # --------------------------------------------------------------------------
    add_heading_2("2. Lược đồ quan hệ thực thể cho hệ thống. Truy vấn cho các chức năng")

    add_heading_3("a. Lược đồ quan hệ thực thể (ERD) cho hệ thống")
    # Thay the bang anh ERD goc tu folder chon-ban-va-dat-mon
    erd_path = "chon-ban-va-dat-mon/ERD Nha hang Thanh Hoa.jpg"
    add_img(erd_path, "Lược đồ quan hệ thực thể (ERD) cho hệ thống", width=Inches(6.4))

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
    # 3. Biểu đồ lớp cho hệ thống và cho các chức năng
    # --------------------------------------------------------------------------
    add_heading_2("3. Biểu đồ lớp cho hệ thống và cho các chức năng")

    add_heading_3("Hệ thống")
    add_img("extracted_media/image15.png", "Biểu đồ lớp thiết kế cho hệ thống", width=Inches(6.4))

    add_heading_3("Quản lý menu")
    add_img("extracted_media/image16.png", "Biểu đồ lớp thiết kế cho Quản lý menu", width=Inches(5.2))

    add_heading_3("Tạo đơn hàng")
    # Thay the bang anh goc tu folder chon-ban-va-dat-mon
    class_order_path = "chon-ban-va-dat-mon/Class Diagram - Pha thiết kế_ Chọn bàn và đặt món.jpg"
    add_img(class_order_path, "Biểu đồ lớp thiết kế cho Tạo đơn hàng (Chọn bàn và đặt món)", width=Inches(6.4))

    add_heading_3("Gộp đơn hàng")
    add_img("extracted_media/image14.png", "Biểu đồ lớp thiết kế cho Gộp đơn hàng", width=Inches(4.8))

    add_heading_3("Thanh toán")
    add_img("extracted_media/image10.png", "Biểu đồ lớp thiết kế cho Thanh toán", width=Inches(4.8))

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 4. Biểu đồ trình tự cho các chức năng
    # --------------------------------------------------------------------------
    add_heading_2("4. Biểu đồ trình tự cho các chức năng")

    add_heading_3("Tạo combo")
    add_img("gen_diagrams/seq_tao_combo.png", "Biểu đồ trình tự thiết kế: Chức năng Tạo combo", width=Inches(6.4))

    add_heading_3("Tạo đơn hàng")
    # Thay the bang anh goc tu folder chon-ban-va-dat-mon
    seq_order_path = "chon-ban-va-dat-mon/Sequence Diagram - Chọn bàn và đặt món.jpg"
    add_img(seq_order_path, "Biểu đồ trình tự thiết kế: Chức năng Tạo đơn hàng (Chọn bàn và đặt món)", width=Inches(6.4))

    add_heading_3("Gộp đơn hàng")
    add_img("gen_diagrams/seq_gop_don.png", "Biểu đồ trình tự thiết kế: Chức năng Gộp đơn hàng", width=Inches(6.4))

    add_heading_3("Thanh toán")
    add_img("gen_diagrams/seq_thanh_toan.png", "Biểu đồ trình tự thiết kế: Chức năng Thanh toán", width=Inches(6.4))

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 5. Biểu đồ thành phần cho hệ thống
    # --------------------------------------------------------------------------
    add_heading_2("5. Biểu đồ thành phần cho hệ thống")
    component_path = "gen_diagrams/component_system_corrected.png"
    add_img(component_path, "Biểu đồ thành phần cho hệ thống", width=Inches(6.4))

    # --------------------------------------------------------------------------
    # 6. Biểu đồ triển khai cho hệ thống
    # --------------------------------------------------------------------------
    add_heading_2("6. Biểu đồ triển khai cho hệ thống")
    deployment_path = "Biểu đồ triển khai - Hệ thống quản lý nhà hàng.jpg"
    add_img(deployment_path, "Biểu đồ triển khai cho hệ thống", width=Inches(6.4))

    output_filename = "N10_Nhom10_TaiLieuThietKe.docx"
    doc.save(output_filename)
    print(f"Document successfully created: {output_filename}")

if __name__ == '__main__':
    create_document()
