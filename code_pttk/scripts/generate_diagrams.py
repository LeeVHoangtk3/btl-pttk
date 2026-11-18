import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, 'diagrams', 'generated')
os.makedirs(OUT_DIR, exist_ok=True)

VP_BLUE = '#7ACFF5'
VP_BORDER = '#000000'
VP_TEXT = '#000000'
VP_BG_WHITE = '#FFFFFF'

def get_ky(ax):
    fig = ax.figure
    w_in, h_in = fig.get_size_inches()
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    return ((y1 - y0) / h_in) / ((x1 - x0) / w_in)

def draw_actor(ax, x, y, name):
    ky = get_ky(ax)
    r = 0.14
    # Head (filled with VP_BLUE, perfect circle)
    head_y = y + 0.36 * ky
    circle = patches.Ellipse((x, head_y), 2 * r, 2 * r * ky, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=6)
    ax.add_patch(circle)
    # Body
    ax.plot([x, x], [head_y - r * ky, y + 0.04 * ky], color=VP_BORDER, lw=1.3, zorder=6)
    # Arms
    ax.plot([x - 0.20, x + 0.20], [y + 0.18 * ky, y + 0.18 * ky], color=VP_BORDER, lw=1.3, zorder=6)
    # Legs
    ax.plot([x, x - 0.16], [y + 0.04 * ky, y - 0.22 * ky], color=VP_BORDER, lw=1.3, zorder=6)
    ax.plot([x, x + 0.16], [y + 0.04 * ky, y - 0.22 * ky], color=VP_BORDER, lw=1.3, zorder=6)
    ax.text(x, y - 0.32 * ky, name, ha='center', va='top', fontsize=8.5, color=VP_TEXT, zorder=6)

def draw_boundary_icon(ax, x, y, name):
    ky = get_ky(ax)
    r = 0.24
    # Perfect Circle
    circle = patches.Ellipse((x, y), 2 * r, 2 * r * ky, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=5)
    ax.add_patch(circle)
    # Vertical line to the left
    bar_x = x - r - 0.14
    ax.plot([bar_x, bar_x], [y - r * ky, y + r * ky], color=VP_BORDER, lw=1.2, zorder=5)
    # Connector
    ax.plot([bar_x, x - r], [y, y], color=VP_BORDER, lw=1.2, zorder=5)
    ax.text(x, y - (r + 0.14) * ky, name, ha='center', va='top', fontsize=8.5, color=VP_TEXT, zorder=6)

def draw_controller_icon(ax, x, y, name):
    ky = get_ky(ax)
    r = 0.24
    # Perfect Circle
    circle = patches.Ellipse((x, y), 2 * r, 2 * r * ky, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=5)
    ax.add_patch(circle)
    # Visual Paradigm Controller Arrowhead at top of circle
    tip_x, tip_y = x - 0.05, y + r * ky
    ax.plot([tip_x + 0.13, tip_x, tip_x + 0.11],
            [tip_y + 0.08 * ky, tip_y, tip_y - 0.07 * ky],
            color=VP_BORDER, lw=1.25, zorder=6)
    ax.text(x, y - (r + 0.14) * ky, name, ha='center', va='top', fontsize=8.5, color=VP_TEXT, zorder=6)

def draw_entity_box(ax, x, y, name, width=1.5, height=0.55):
    rect = patches.Rectangle((x - width/2, y - height/2), width, height, 
                             edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=5)
    ax.add_patch(rect)
    ax.text(x, y, name, ha='center', va='center', fontsize=8.5, color=VP_TEXT, zorder=6)

def draw_lifeline(ax, x, y_start, y_end):
    ax.plot([x, x], [y_start, y_end], linestyle='--', color='#222222', lw=0.9, zorder=2)

def draw_activation(ax, x, y_top, y_bottom, width=0.18):
    rect = patches.Rectangle((x - width/2, y_bottom), width, y_top - y_bottom,
                             edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.0, zorder=4)
    ax.add_patch(rect)

def draw_message(ax, x1, x2, y, text, is_return=False, self_call=False, offset_y=0.14):
    if self_call:
        dx = 0.45
        dy = 0.32
        ax.plot([x1, x1 + dx, x1 + dx, x1], [y, y, y - dy, y - dy], color=VP_BORDER, lw=1.1, zorder=6)
        ax.annotate('', xy=(x1, y - dy), xytext=(x1 + 0.08, y - dy),
                    arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.2), zorder=6)
        ax.text(x1 + dx + 0.08, y - dy/2, text, ha='left', va='center', fontsize=8, color=VP_TEXT, zorder=7)
        return

    if is_return:
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=6)
    else:
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', linestyle='-', color=VP_BORDER, lw=1.2), zorder=6)
    
    mid_x = (x1 + x2) / 2
    ax.text(mid_x, y + offset_y, text, ha='center', va='bottom', fontsize=8, color=VP_TEXT, zorder=7)

def draw_fragment(ax, x1, x2, y_top, y_bottom, label, condition1, condition2=None, y_divider=None):
    rect = patches.Rectangle((x1, y_bottom), x2 - x1, y_top - y_bottom,
                             edgecolor=VP_BORDER, facecolor='none', lw=1.0, zorder=3)
    ax.add_patch(rect)
    # Small corner box with label
    ax.text(x1 + 0.15, y_top - 0.2, label, fontsize=8, fontweight='bold', color=VP_TEXT, zorder=5)
    ax.text(x1 + 0.6, y_top - 0.2, f'[{condition1}]', fontsize=8, color=VP_TEXT, zorder=5)
    
    if y_divider and condition2:
        ax.plot([x1, x2], [y_divider, y_divider], linestyle='--', color='#444444', lw=1.0, zorder=3)
        ax.text(x1 + 0.6, y_divider - 0.2, f'[{condition2}]', fontsize=8, color=VP_TEXT, zorder=5)

def add_vp_footer(ax, x_max, y_min):
    ax.text(x_max - 0.2, y_min + 0.15, "Powered By Visual Paradigm Community Edition", 
            ha='right', va='bottom', fontsize=7.5, color='#666666', style='italic')


# ==============================================================================
# 1. SEQUENCE DIAGRAM: TẠO COMBO (STYLE CHUẨN CHON-BAN-VA-DAT-MON)
# ==============================================================================
def gen_seq_tao_combo():
    fig, ax = plt.subplots(figsize=(14.0, 10.5), dpi=220)
    ax.set_xlim(-0.5, 13.5)
    ax.set_ylim(-14.2, 1.8)
    ax.axis('off')

    xs = {
        'ql': 0.8,
        'ui': 2.8,
        'ctrl': 5.0,
        'dish': 7.4,
        'combo': 9.4,
        'detail': 11.2,
        'category': 12.7
    }
    y_header = 0.8

    draw_actor(ax, xs['ql'], y_header, "Quản lý")
    draw_boundary_icon(ax, xs['ui'], y_header, ":MenuUI")
    draw_controller_icon(ax, xs['ctrl'], y_header, ":MenuController")
    draw_entity_box(ax, xs['dish'], y_header, ":Dish", width=1.4)
    draw_entity_box(ax, xs['combo'], y_header, ":Combo", width=1.4)
    draw_entity_box(ax, xs['detail'], y_header, ":ComboDetail", width=1.5)
    draw_entity_box(ax, xs['category'], y_header, ":Category", width=1.4)

    y_end = -13.6
    for key, x in xs.items():
        y_top_line = y_header - 0.82 if key in ('ql', 'tn', 'ui', 'map_ui', 'merge_ui', 'list_ui', 'pay_ui', 'ctrl') else y_header - 0.275
        draw_lifeline(ax, x, y_top_line, y_end)

    draw_activation(ax, xs['ql'], -0.8, -13.2)
    draw_activation(ax, xs['ui'], -1.0, -2.4)
    draw_activation(ax, xs['ui'], -3.4, -13.2)
    draw_activation(ax, xs['ctrl'], -1.3, -2.2)
    draw_activation(ax, xs['ctrl'], -3.9, -12.8)
    draw_activation(ax, xs['dish'], -1.5, -2.0)
    draw_activation(ax, xs['combo'], -7.7, -10.0)
    draw_activation(ax, xs['detail'], -8.0, -8.7)

    # 1. Mo form
    draw_message(ax, xs['ql'], xs['ui'], -1.0, "1: Bấm + / tab Thực đơn")
    draw_message(ax, xs['ui'], xs['ctrl'], -1.3, "1.1: moLuotTaoCombo()")
    draw_message(ax, xs['ctrl'], xs['dish'], -1.5, "1.1.1: layDanhSachMonLeKhaDung()")
    draw_message(ax, xs['dish'], xs['ctrl'], -1.9, "1.1.2: Danh sách món lẻ", is_return=True)
    draw_message(ax, xs['ctrl'], xs['ui'], -2.1, "1.2: hienThiFormTaoCombo(danhSachMon)", is_return=True)
    draw_message(ax, xs['ui'], xs['ql'], -2.3, "1.3: Hiển thị form tạo combo & món lẻ", is_return=True)

    # 2. Nhap du lieu & Bam Luu
    draw_message(ax, xs['ql'], xs['ui'], -3.4, "2: Nhập thông tin (tên, giá, số người ăn), chọn món lẻ con")
    draw_message(ax, xs['ql'], xs['ui'], -3.8, "3: Bấm Lưu combo")
    draw_message(ax, xs['ui'], xs['ctrl'], -4.1, "3.1: themCombo(comboDTO)")
    draw_message(ax, xs['ctrl'], xs['ctrl'], -4.6, "3.1.1: kiemTraComboHopLe()", self_call=True)

    # Alt Fragment
    draw_fragment(ax, 0.4, 13.2, -5.3, -12.8, "alt", 
                  "Dữ liệu hợp lệ", 
                  "Dữ liệu không hợp lệ (trùng tên / chưa chọn món)", 
                  y_divider=-11.25)

    # Inside Valid
    draw_message(ax, xs['ctrl'], xs['combo'], -5.9, "3.1.2: taoComboMoi(ten, gia, soNguoi)")
    
    # Loop fragment for items
    draw_fragment(ax, 4.4, 12.2, -6.5, -9.1, "loop", "Với mỗi món lẻ được chọn")
    draw_message(ax, xs['ctrl'], xs['combo'], -7.1, "3.1.2.1: themMonCon(dish, soLuong)")
    draw_message(ax, xs['combo'], xs['detail'], -7.5, "3.1.2.1.1: taoDongChiTiet(ComboDetail)")
    draw_message(ax, xs['detail'], xs['combo'], -8.3, "3.1.2.1.2: Chi tiết món con", is_return=True)
    draw_message(ax, xs['combo'], xs['ctrl'], -8.7, "3.1.2.1.3: Thêm món con thành công", is_return=True)

    draw_message(ax, xs['ctrl'], xs['combo'], -9.5, "3.1.3: tinhGiaCombo()")
    draw_message(ax, xs['combo'], xs['ctrl'], -9.8, "3.1.3.1: Tổng giá gốc tham khảo", is_return=True)
    draw_message(ax, xs['ctrl'], xs['ctrl'], -10.3, "3.1.4: luuComboVaoHeThong()", self_call=True)
    draw_message(ax, xs['ctrl'], xs['ui'], -10.75, "3.1.5: Lưu thành công", is_return=True)
    draw_message(ax, xs['ui'], xs['ql'], -11.05, "3.1.6: Làm mới thực đơn & thông báo thành công", is_return=True)

    # Inside Invalid
    draw_message(ax, xs['ctrl'], xs['ui'], -11.95, "3.1.7: Báo lỗi dữ liệu không hợp lệ", is_return=True)
    draw_message(ax, xs['ui'], xs['ql'], -12.35, "3.1.8: Báo lỗi, giữ nguyên nội dung form", is_return=True)

    add_vp_footer(ax, 13.5, -14.0)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'seq_tao_combo.png'))
    plt.close()
    print("Done gen seq_tao_combo (VP style)")


# ==============================================================================
# 2. SEQUENCE DIAGRAM: GỘP ĐƠN HÀNG (STYLE CHUẨN CHON-BAN-VA-DAT-MON)
# ==============================================================================
def gen_seq_gop_don():
    fig, ax = plt.subplots(figsize=(14.5, 10.5), dpi=220)
    ax.set_xlim(-0.5, 14.0)
    ax.set_ylim(-14.2, 1.8)
    ax.axis('off')

    xs = {
        'tn': 0.8,
        'map_ui': 2.6,
        'merge_ui': 4.4,
        'ctrl': 6.4,
        'order_dich': 8.6,
        'order_nguon': 10.4,
        'table': 12.0,
        'log': 13.4
    }
    y_header = 0.8

    draw_actor(ax, xs['tn'], y_header, "Thu ngân / Phục vụ")
    draw_boundary_icon(ax, xs['map_ui'], y_header, ":TableMapUI")
    draw_boundary_icon(ax, xs['merge_ui'], y_header, ":OrderManagementUI")
    draw_controller_icon(ax, xs['ctrl'], y_header, ":OrderController")
    draw_entity_box(ax, xs['order_dich'], y_header, ":OrderTaiCho (Đích)", width=1.7)
    draw_entity_box(ax, xs['order_nguon'], y_header, ":OrderTaiCho (Nguồn)", width=1.7)
    draw_entity_box(ax, xs['table'], y_header, ":RestaurantTable", width=1.5)
    draw_entity_box(ax, xs['log'], y_header, ":OrderMergeLog", width=1.4)

    y_end = -13.6
    for key, x in xs.items():
        y_top_line = y_header - 0.82 if key in ('ql', 'tn', 'ui', 'map_ui', 'merge_ui', 'list_ui', 'pay_ui', 'ctrl') else y_header - 0.275
        draw_lifeline(ax, x, y_top_line, y_end)

    draw_activation(ax, xs['tn'], -0.8, -13.2)
    draw_activation(ax, xs['map_ui'], -1.0, -2.4)
    draw_activation(ax, xs['merge_ui'], -3.2, -13.2)
    draw_activation(ax, xs['ctrl'], -1.3, -2.2)
    draw_activation(ax, xs['ctrl'], -3.6, -12.8)
    draw_activation(ax, xs['order_dich'], -6.8, -8.7)
    draw_activation(ax, xs['order_nguon'], -6.2, -9.5)
    draw_activation(ax, xs['table'], -9.8, -10.4)

    # 1. Mo giao dien
    draw_message(ax, xs['tn'], xs['map_ui'], -1.0, "1: Bấm nút Gộp đơn hàng")
    draw_message(ax, xs['map_ui'], xs['ctrl'], -1.3, "1.1: moLuotGopDon()")
    draw_message(ax, xs['ctrl'], xs['table'], -1.5, "1.1.1: layDanhSachBanDangPhucVu()")
    draw_message(ax, xs['table'], xs['ctrl'], -1.8, "1.1.2: Danh sách bàn đang phục vụ", is_return=True)
    draw_message(ax, xs['ctrl'], xs['merge_ui'], -2.0, "1.2: hienThiGiaoDienGopDon(danhSachBan)", is_return=True)
    draw_message(ax, xs['merge_ui'], xs['tn'], -2.2, "1.3: Hiển thị 3 phân vùng gộp đơn", is_return=True)

    # 2. Chon ban & xem truoc
    draw_message(ax, xs['tn'], xs['merge_ui'], -3.1, "2: Chọn bàn đích (Bàn 1) và bàn nguồn (Bàn 3)")
    draw_message(ax, xs['merge_ui'], xs['ctrl'], -3.4, "2.1: xemTruocKetQuaGop(banDich, banNguon)")
    draw_message(ax, xs['ctrl'], xs['merge_ui'], -3.8, "2.2: Hiển thị chi tiết món & kết quả gộp tạm", is_return=True)

    # 3. Xac nhan gop
    draw_message(ax, xs['tn'], xs['merge_ui'], -4.3, "3: Bấm Xác nhận gộp đơn")
    draw_message(ax, xs['merge_ui'], xs['ctrl'], -4.6, "3.1: gopHoaDon(donDich, donNguon)")

    # Alt Fragment
    draw_fragment(ax, 0.4, 13.8, -5.2, -12.7, "alt", 
                  "Số bàn chọn hợp lệ (≥ 2 bàn)", 
                  "Số bàn chọn < 2 bàn", 
                  y_divider=-11.4)

    draw_message(ax, xs['ctrl'], xs['order_nguon'], -5.8, "3.1.1: layDanhSachMonDonNguon()")
    draw_message(ax, xs['order_nguon'], xs['ctrl'], -6.2, "3.1.2: Danh sách món bàn 3", is_return=True)

    # Loop items in donNguon
    draw_fragment(ax, 5.8, 11.2, -6.6, -8.3, "loop", "Với từng món ăn của bàn nguồn")
    draw_message(ax, xs['ctrl'], xs['order_dich'], -7.2, "3.1.2.1: themHoacCongDonMon(item, soLuong)")
    draw_message(ax, xs['order_dich'], xs['ctrl'], -7.9, "3.1.2.2: Cập nhật dòng món", is_return=True)

    draw_message(ax, xs['ctrl'], xs['order_dich'], -8.7, "3.1.3: tinhTongTienDonGop()")
    draw_message(ax, xs['order_dich'], xs['ctrl'], -9.0, "3.1.4: Tổng tiền mới", is_return=True)

    draw_message(ax, xs['ctrl'], xs['order_nguon'], -9.4, "3.1.5: setTrangThai(DA_GOP)")
    draw_message(ax, xs['ctrl'], xs['table'], -9.8, "3.1.6: capNhatTrangThaiBan(banNguon, TRONG)")
    draw_message(ax, xs['ctrl'], xs['log'], -10.2, "3.1.7: taoNhatKyGop(OrderMergeLog)")
    draw_message(ax, xs['ctrl'], xs['merge_ui'], -10.6, "3.1.8: Gộp đơn thành công", is_return=True)
    draw_message(ax, xs['merge_ui'], xs['tn'], -10.9, "3.1.9: Làm mới sơ đồ bàn & thông báo", is_return=True)

    # Invalid branch
    draw_message(ax, xs['ctrl'], xs['merge_ui'], -11.8, "3.1.10: Báo lỗi số bàn chọn < 2", is_return=True)
    draw_message(ax, xs['merge_ui'], xs['tn'], -12.1, "3.1.11: Báo lỗi: Vui lòng chọn tối thiểu 2 bàn", is_return=True)

    add_vp_footer(ax, 14.0, -14.0)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'seq_gop_don.png'))
    plt.close()
    print("Done gen seq_gop_don (VP style)")


# ==============================================================================
# 3. SEQUENCE DIAGRAM: THANH TOÁN (STYLE CHUẨN CHON-BAN-VA-DAT-MON)
# ==============================================================================
def gen_seq_thanh_toan():
    fig, ax = plt.subplots(figsize=(14.5, 10.5), dpi=220)
    ax.set_xlim(-0.5, 14.0)
    ax.set_ylim(-14.2, 1.8)
    ax.axis('off')

    xs = {
        'tn': 0.8,
        'list_ui': 2.6,
        'pay_ui': 4.4,
        'ctrl': 6.4,
        'order': 8.6,
        'pay': 10.4,
        'table': 12.0,
        'log': 13.4
    }
    y_header = 0.8

    draw_actor(ax, xs['tn'], y_header, "Thu ngân")
    draw_boundary_icon(ax, xs['list_ui'], y_header, ":PaymentListUI")
    draw_boundary_icon(ax, xs['pay_ui'], y_header, ":PaymentUI")
    draw_controller_icon(ax, xs['ctrl'], y_header, ":PaymentController")
    draw_entity_box(ax, xs['order'], y_header, ":Orders", width=1.5)
    draw_entity_box(ax, xs['pay'], y_header, ":PaymentTienMat", width=1.7)
    draw_entity_box(ax, xs['table'], y_header, ":RestaurantTable", width=1.5)
    draw_entity_box(ax, xs['log'], y_header, ":PaymentLog", width=1.4)

    y_end = -13.6
    for key, x in xs.items():
        y_top_line = y_header - 0.82 if key in ('ql', 'tn', 'ui', 'map_ui', 'merge_ui', 'list_ui', 'pay_ui', 'ctrl') else y_header - 0.275
        draw_lifeline(ax, x, y_top_line, y_end)

    draw_activation(ax, xs['tn'], -0.8, -13.2)
    draw_activation(ax, xs['list_ui'], -1.0, -2.4)
    draw_activation(ax, xs['pay_ui'], -3.0, -13.2)
    draw_activation(ax, xs['ctrl'], -1.3, -2.2)
    draw_activation(ax, xs['ctrl'], -3.4, -12.8)
    draw_activation(ax, xs['order'], -1.5, -2.0)
    draw_activation(ax, xs['order'], -7.7, -8.6)
    draw_activation(ax, xs['pay'], -5.8, -8.2)
    draw_activation(ax, xs['table'], -8.6, -9.4)

    # 1. Mo danh sach don cho thanh toan
    draw_message(ax, xs['tn'], xs['list_ui'], -1.0, "1: Bấm tab Đơn chờ thanh toán")
    draw_message(ax, xs['list_ui'], xs['ctrl'], -1.3, "1.1: layDanhSachDonChoThanhToan()")
    draw_message(ax, xs['ctrl'], xs['order'], -1.5, "1.1.1: getDonChoThanhToan()")
    draw_message(ax, xs['order'], xs['ctrl'], -1.8, "1.1.2: Danh sách đơn chờ", is_return=True)
    draw_message(ax, xs['ctrl'], xs['list_ui'], -2.0, "1.2: hienThiDanhSachDon(listDon)", is_return=True)
    draw_message(ax, xs['list_ui'], xs['tn'], -2.2, "1.3: Hiển thị danh sách hóa đơn", is_return=True)

    # 2. Chon don & phuong thuc
    draw_message(ax, xs['tn'], xs['pay_ui'], -2.9, "2: Chọn đơn HD001, chọn phương thức Tiền mặt")
    draw_message(ax, xs['tn'], xs['pay_ui'], -3.4, "3: Nhập số tiền khách đưa & tiền tip")
    draw_message(ax, xs['pay_ui'], xs['ctrl'], -3.8, "3.1: tinhTienThua(soTienNhan, tongTien)")
    draw_message(ax, xs['ctrl'], xs['pay_ui'], -4.2, "3.2: Tiền thừa trả khách", is_return=True)
    draw_message(ax, xs['pay_ui'], xs['tn'], -4.5, "3.3: Hiển thị tiền thừa cho thu ngân", is_return=True)

    # 4. Xac nhan thanh toan
    draw_message(ax, xs['tn'], xs['pay_ui'], -5.0, "4: Bấm Xác nhận thanh toán")
    draw_message(ax, xs['pay_ui'], xs['ctrl'], -5.3, "4.1: xuLyThanhToan(paymentDTO)")

    # Alt Fragment
    draw_fragment(ax, 0.4, 13.8, -5.9, -12.7, "alt", 
                  "Tiền khách đưa ≥ Tổng tiền hóa đơn", 
                  "Tiền khách đưa < Tổng tiền (Không đủ)", 
                  y_divider=-11.4)

    draw_message(ax, xs['ctrl'], xs['pay'], -6.5, "4.1.1: taoThanhToanMoi(PaymentTienMat)")
    draw_message(ax, xs['ctrl'], xs['pay'], -7.1, "4.1.2: xacNhanThanhToan()")
    draw_message(ax, xs['ctrl'], xs['order'], -7.7, "4.1.3: setTrangThai(DA_THANH_TOAN)")
    draw_message(ax, xs['ctrl'], xs['table'], -8.5, "4.1.4: giaiPhongBan(TRONG)")
    draw_message(ax, xs['ctrl'], xs['log'], -9.2, "4.1.5: taoNhatKyThanhToan(PaymentLog)")
    draw_message(ax, xs['ctrl'], xs['ctrl'], -9.8, "4.1.6: inHoaDonToiMayIn()", self_call=True)
    draw_message(ax, xs['ctrl'], xs['pay_ui'], -10.4, "4.1.7: Thanh toán thành công", is_return=True)
    draw_message(ax, xs['pay_ui'], xs['tn'], -10.8, "4.1.8: In hóa đơn & thông báo kết quả", is_return=True)

    # Invalid branch
    draw_message(ax, xs['ctrl'], xs['pay_ui'], -11.8, "4.1.9: Báo lỗi số tiền không đủ", is_return=True)
    draw_message(ax, xs['pay_ui'], xs['tn'], -12.1, "4.1.10: Báo lỗi: Tiền khách đưa không đủ!", is_return=True)

    add_vp_footer(ax, 14.0, -14.0)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'seq_thanh_toan.png'))
    plt.close()
    print("Done gen seq_thanh_toan (VP style)")

if __name__ == '__main__':
    gen_seq_tao_combo()
    gen_seq_gop_don()
    gen_seq_thanh_toan()
    print("Re-generated all sequence diagrams matching chon-ban-va-dat-mon successfully!")
