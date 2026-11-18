import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, 'diagrams', 'generated')
os.makedirs(OUT_DIR, exist_ok=True)

VP_BLUE = '#7ACFF5'
VP_BORDER = '#000000'
VP_TEXT = '#000000'
VP_BG_WHITE = '#FFFFFF'

# ==============================================================================
# HELPER PRIMITIVES (CHUẨN VISUAL PARADIGM COMMUNITY EDITION)
# ==============================================================================
def add_vp_footer(ax, x_max, y_min):
    ax.text(x_max - 0.15, y_min + 0.12, "Powered By Visual Paradigm Community Edition",
            ha='right', va='bottom', fontsize=7.5, color='#666666', style='italic')

def get_ky(ax):
    fig = ax.figure
    w_in, h_in = fig.get_size_inches()
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    return ((y1 - y0) / h_in) / ((x1 - x0) / w_in)

def draw_actor(ax, x, y, name):
    ky = get_ky(ax)
    r = 0.14
    head_y = y + 0.36 * ky
    circle = patches.Ellipse((x, head_y), 2 * r, 2 * r * ky, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=6)
    ax.add_patch(circle)
    ax.plot([x, x], [head_y - r * ky, y + 0.04 * ky], color=VP_BORDER, lw=1.3, zorder=6)
    ax.plot([x - 0.20, x + 0.20], [y + 0.18 * ky, y + 0.18 * ky], color=VP_BORDER, lw=1.3, zorder=6)
    ax.plot([x, x - 0.16], [y + 0.04 * ky, y - 0.22 * ky], color=VP_BORDER, lw=1.3, zorder=6)
    ax.plot([x, x + 0.16], [y + 0.04 * ky, y - 0.22 * ky], color=VP_BORDER, lw=1.3, zorder=6)
    ax.text(x, y - 0.32 * ky, name, ha='center', va='top', fontsize=8.5, color=VP_TEXT, zorder=6)

def draw_boundary_icon(ax, x, y, name):
    ky = get_ky(ax)
    r = 0.24
    circle = patches.Ellipse((x, y), 2 * r, 2 * r * ky, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=5)
    ax.add_patch(circle)
    bar_x = x - r - 0.14
    ax.plot([bar_x, bar_x], [y - r * ky, y + r * ky], color=VP_BORDER, lw=1.2, zorder=5)
    ax.plot([bar_x, x - r], [y, y], color=VP_BORDER, lw=1.2, zorder=5)
    ax.text(x, y - (r + 0.14) * ky, name, ha='center', va='top', fontsize=8.5, color=VP_TEXT, zorder=6)

def draw_controller_icon(ax, x, y, name):
    ky = get_ky(ax)
    r = 0.24
    circle = patches.Ellipse((x, y), 2 * r, 2 * r * ky, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=5)
    ax.add_patch(circle)
    tip_x, tip_y = x - 0.05, y + r * ky
    ax.plot([tip_x + 0.13, tip_x, tip_x + 0.11],
            [tip_y + 0.08 * ky, tip_y, tip_y - 0.07 * ky],
            color=VP_BORDER, lw=1.25, zorder=6)
    ax.text(x, y - (r + 0.14) * ky, name, ha='center', va='top', fontsize=8.5, color=VP_TEXT, zorder=6)

def draw_entity_icon(ax, x, y, name, width=None, height=0.58):
    if width is None:
        width = max(1.45, len(name) * 0.095 + 0.35)
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

def draw_message(ax, x1, x2, y, text, is_return=False, self_call=False, offset_y=0.13):
    if self_call:
        dx = 0.45
        dy = 0.32
        ax.plot([x1, x1 + dx, x1 + dx, x1], [y, y, y - dy, y - dy], color=VP_BORDER, lw=1.1, zorder=6)
        ax.annotate('', xy=(x1, y - dy), xytext=(x1 + 0.08, y - dy),
                    arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.2), zorder=6)
        ax.text(x1 + dx + 0.08, y - dy/2, text, ha='left', va='center', fontsize=8, color=VP_TEXT, zorder=7)
        return

    style = '--' if is_return else '-'
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', linestyle=style, color=VP_BORDER, lw=1.15), zorder=6)
    mid_x = (x1 + x2) / 2
    ax.text(mid_x, y + offset_y, text, ha='center', va='bottom', fontsize=8, color=VP_TEXT, zorder=7)

def draw_fragment(ax, x1, x2, y_top, y_bottom, label, condition1, condition2=None, y_divider=None):
    rect = patches.Rectangle((x1, y_bottom), x2 - x1, y_top - y_bottom,
                             edgecolor=VP_BORDER, facecolor='none', lw=1.0, zorder=3)
    ax.add_patch(rect)
    ax.text(x1 + 0.15, y_top - 0.2, label, fontsize=8, fontweight='bold', color=VP_TEXT, zorder=5)
    ax.text(x1 + 0.65, y_top - 0.2, f'[{condition1}]', fontsize=8, color=VP_TEXT, zorder=5)
    if y_divider and condition2:
        ax.plot([x1, x2], [y_divider, y_divider], linestyle='--', color='#444444', lw=1.0, zorder=3)
        ax.text(x1 + 0.65, y_divider - 0.2, f'[{condition2}]', fontsize=8, color=VP_TEXT, zorder=5)


# ==============================================================================
# PHẦN II.5: 4 BIỂU ĐỒ TRÌNH TỰ PHA PHÂN TÍCH (ANALYSIS SEQUENCE DIAGRAMS)
# ==============================================================================
def gen_seq_pt_tao_combo():
    fig, ax = plt.subplots(figsize=(14.0, 10.0), dpi=220)
    ax.set_xlim(-0.5, 13.5)
    ax.set_ylim(-13.8, 1.8)
    ax.axis('off')

    xs = {'ql': 0.8, 'ui': 3.0, 'ctrl': 5.5, 'dish': 8.0, 'combo': 10.3, 'detail': 12.5}
    yh = 0.8
    draw_actor(ax, xs['ql'], yh, "Quản lý")
    draw_boundary_icon(ax, xs['ui'], yh, ":GiaoDienMenu")
    draw_controller_icon(ax, xs['ctrl'], yh, ":DieuKhienMenu")
    draw_entity_icon(ax, xs['dish'], yh, ":Dish")
    draw_entity_icon(ax, xs['combo'], yh, ":Combo")
    draw_entity_icon(ax, xs['detail'], yh, ":ComboDetail")

    for k, x in xs.items():
        y_top_line = yh - 0.82 if k in ('ql', 'nv', 'tn', 'ui', 'map_ui', 'order_ui', 'ctrl') else yh - 0.29
        draw_lifeline(ax, x, y_top_line, -13.2)

    draw_activation(ax, xs['ql'], -0.8, -12.8)
    draw_activation(ax, xs['ui'], -1.0, -2.5)
    draw_activation(ax, xs['ui'], -3.3, -12.8)
    draw_activation(ax, xs['ctrl'], -1.3, -2.3)
    draw_activation(ax, xs['ctrl'], -3.8, -12.5)
    draw_activation(ax, xs['dish'], -1.5, -2.0)
    draw_activation(ax, xs['combo'], -5.8, -9.8)
    draw_activation(ax, xs['detail'], -7.3, -8.4)

    draw_message(ax, xs['ql'], xs['ui'], -1.0, "1: Chọn chức năng Tạo Combo mới")
    draw_message(ax, xs['ui'], xs['ctrl'], -1.3, "1.1: Yêu cầu mở biểu mẫu tạo Combo")
    draw_message(ax, xs['ctrl'], xs['dish'], -1.5, "1.1.1: Lấy danh sách món lẻ đang kinh doanh")
    draw_message(ax, xs['dish'], xs['ctrl'], -1.9, "1.1.2: Danh sách món lẻ (Dish)", is_return=True)
    draw_message(ax, xs['ctrl'], xs['ui'], -2.1, "1.2: Trả về dữ liệu biểu mẫu & món lẻ", is_return=True)
    draw_message(ax, xs['ui'], xs['ql'], -2.3, "1.3: Hiển thị biểu mẫu tạo Combo mới", is_return=True)

    draw_message(ax, xs['ql'], xs['ui'], -3.3, "2: Nhập tên, giá bán, số người ăn, chọn món lẻ & số lượng")
    draw_message(ax, xs['ql'], xs['ui'], -3.8, "3: Nhấn nút Lưu")
    draw_message(ax, xs['ui'], xs['ctrl'], -4.1, "3.1: Gửi thông tin Combo mới cần tạo")
    draw_message(ax, xs['ctrl'], xs['ctrl'], -4.6, "3.1.1: Kiểm tra tính hợp lệ dữ liệu", self_call=True)

    draw_fragment(ax, 0.3, 13.2, -5.3, -12.6, "alt",
                  "Thông tin hợp lệ (tên hợp lệ, giá > 0, có ≥ 1 món lẻ)",
                  "Thông tin không hợp lệ (thiếu dữ liệu / trùng tên / chưa chọn món)",
                  y_divider=-10.95)

    draw_message(ax, xs['ctrl'], xs['combo'], -5.9, "3.1.2: Khởi tạo thực thể Combo mới")
    draw_fragment(ax, 4.8, 13.0, -6.5, -8.8, "loop", "Với mỗi món lẻ thành phần được chọn")
    draw_message(ax, xs['ctrl'], xs['combo'], -7.1, "3.1.2.1: Gắn món lẻ vào Combo")
    draw_message(ax, xs['combo'], xs['detail'], -7.5, "3.1.2.1.1: Tạo chi tiết ComboDetail (soLuong, ghiChu)")
    draw_message(ax, xs['detail'], xs['combo'], -8.2, "3.1.2.1.2: Xác nhận dòng chi tiết", is_return=True)

    draw_message(ax, xs['ctrl'], xs['combo'], -9.3, "3.1.3: Tính tổng giá gốc tham khảo & lưu Combo")
    draw_message(ax, xs['combo'], xs['ctrl'], -9.7, "3.1.4: Lưu Combo thành công", is_return=True)
    draw_message(ax, xs['ctrl'], xs['ui'], -10.2, "3.1.5: Thông báo tạo Combo thành công", is_return=True)
    draw_message(ax, xs['ui'], xs['ql'], -10.6, "3.1.6: Hiển thị thông báo & làm mới danh sách thực đơn", is_return=True)

    draw_message(ax, xs['ctrl'], xs['ui'], -11.75, "3.1.7: Trả về thông báo lỗi dữ liệu", is_return=True)
    draw_message(ax, xs['ui'], xs['ql'], -12.25, "3.1.8: Hiển thị cảnh báo lỗi & yêu cầu nhập lại", is_return=True)

    add_vp_footer(ax, 13.5, -13.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'seq_pt_tao_combo.png'))
    plt.close()


def gen_seq_pt_tao_don():
    fig, ax = plt.subplots(figsize=(14.5, 10.5), dpi=220)
    ax.set_xlim(-0.5, 14.2)
    ax.set_ylim(-14.2, 1.8)
    ax.axis('off')

    xs = {
        'nv': 0.7, 'map_ui': 2.5, 'order_ui': 4.4, 'ctrl': 6.4,
        'table': 8.4, 'order': 10.3, 'item': 12.1, 'detail': 13.6
    }
    yh = 0.8
    draw_actor(ax, xs['nv'], yh, "Nhân viên order")
    draw_boundary_icon(ax, xs['map_ui'], yh, ":GiaoDienSoDoBan")
    draw_boundary_icon(ax, xs['order_ui'], yh, ":GiaoDienDatMon")
    draw_controller_icon(ax, xs['ctrl'], yh, ":DieuKhienDonHang")
    draw_entity_icon(ax, xs['table'], yh, ":Table")
    draw_entity_icon(ax, xs['order'], yh, ":OrderTaiCho")
    draw_entity_icon(ax, xs['item'], yh, ":MenuItem")
    draw_entity_icon(ax, xs['detail'], yh, ":OrderItem")

    for k, x in xs.items():
        y_top_line = yh - 0.82 if k in ('ql', 'nv', 'tn', 'ui', 'map_ui', 'order_ui', 'ctrl') else yh - 0.29
        draw_lifeline(ax, x, y_top_line, -13.6)

    draw_activation(ax, xs['nv'], -0.8, -13.2)
    draw_activation(ax, xs['map_ui'], -1.0, -4.8)
    draw_activation(ax, xs['order_ui'], -5.4, -13.2)
    draw_activation(ax, xs['ctrl'], -1.3, -12.9)
    draw_activation(ax, xs['table'], -1.5, -2.0)
    draw_activation(ax, xs['table'], -11.5, -12.1)
    draw_activation(ax, xs['order'], -3.3, -4.5)
    draw_activation(ax, xs['order'], -9.0, -11.3)
    draw_activation(ax, xs['item'], -6.5, -7.2)
    draw_activation(ax, xs['detail'], -7.7, -8.5)

    draw_message(ax, xs['nv'], xs['map_ui'], -1.0, "1: Mở màn hình Sơ đồ / Chọn bàn")
    draw_message(ax, xs['map_ui'], xs['ctrl'], -1.3, "1.1: Yêu cầu danh sách khu vực & bàn")
    draw_message(ax, xs['ctrl'], xs['table'], -1.5, "1.1.1: Truy vấn trạng thái bàn theo khu vực")
    draw_message(ax, xs['table'], xs['ctrl'], -1.9, "1.1.2: Danh sách bàn (trống / đang phục vụ)", is_return=True)
    draw_message(ax, xs['ctrl'], xs['map_ui'], -2.2, "1.2: Hiển thị sơ đồ bàn", is_return=True)

    draw_message(ax, xs['nv'], xs['map_ui'], -2.7, "2: Chọn khu vực và chọn bàn phục vụ")
    draw_message(ax, xs['map_ui'], xs['ctrl'], -3.0, "2.1: Xác nhận bàn đã chọn")

    draw_fragment(ax, 2.0, 11.2, -3.2, -4.9, "alt", "Bàn trống", "Bàn đã có khách", y_divider=-4.1)
    draw_message(ax, xs['ctrl'], xs['order'], -3.6, "2.1.1: Khởi tạo đơn hàng mới gắn với bàn")
    draw_message(ax, xs['ctrl'], xs['order'], -4.4, "2.1.2: Tải hóa đơn hiện có trên bàn")

    draw_message(ax, xs['nv'], xs['order_ui'], -5.5, "3: Chọn danh mục, chọn món ăn & nhập số lượng")
    draw_message(ax, xs['order_ui'], xs['ctrl'], -5.9, "3.1: Yêu cầu thêm món vào đơn")
    draw_fragment(ax, 3.8, 14.0, -6.2, -9.8, "loop", "Lặp lại việc chọn thêm các món ăn")
    draw_message(ax, xs['ctrl'], xs['item'], -6.7, "3.1.1: Kiểm tra trạng thái món (MenuItem)")
    draw_message(ax, xs['item'], xs['ctrl'], -7.1, "3.1.2: Món đang kinh doanh & đơn giá", is_return=True)
    draw_message(ax, xs['ctrl'], xs['detail'], -7.8, "3.1.3: Tạo dòng món OrderItem (soLuong, donGia)")
    draw_message(ax, xs['detail'], xs['ctrl'], -8.3, "3.1.4: Chi tiết dòng món", is_return=True)
    draw_message(ax, xs['ctrl'], xs['order'], -9.0, "3.1.5: Cập nhật tổng tiền tạm tính")
    draw_message(ax, xs['ctrl'], xs['order_ui'], -9.5, "3.2: Hiển thị giỏ hàng & tổng tiền tạm tính", is_return=True)

    draw_message(ax, xs['nv'], xs['order_ui'], -10.3, "4: Nhấn nút Lưu đơn hàng")
    draw_message(ax, xs['order_ui'], xs['ctrl'], -10.7, "4.1: Yêu cầu lưu tạm đơn hàng")
    draw_message(ax, xs['ctrl'], xs['order'], -11.1, "4.1.1: Lưu thông tin đơn hàng & các dòng món")
    draw_message(ax, xs['ctrl'], xs['table'], -11.7, "4.1.2: Cập nhật trạng thái bàn -> Đang phục vụ")
    draw_message(ax, xs['ctrl'], xs['order_ui'], -12.3, "4.2: Lưu đơn thành công", is_return=True)
    draw_message(ax, xs['order_ui'], xs['nv'], -12.7, "4.3: Thông báo lưu thành công & trở về màn hình chính", is_return=True)

    add_vp_footer(ax, 14.2, -14.0)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'seq_pt_tao_don.png'))
    plt.close()


def gen_seq_pt_gop_don():
    fig, ax = plt.subplots(figsize=(14.0, 10.0), dpi=220)
    ax.set_xlim(-0.5, 13.8)
    ax.set_ylim(-13.8, 1.8)
    ax.axis('off')

    xs = {
        'tn': 0.8, 'ui': 3.0, 'ctrl': 5.4,
        'table': 7.7, 'dich': 10.0, 'nguon': 12.4
    }
    yh = 0.8
    draw_actor(ax, xs['tn'], yh, "Thu ngân / Phục vụ")
    draw_boundary_icon(ax, xs['ui'], yh, ":GiaoDienGopDon")
    draw_controller_icon(ax, xs['ctrl'], yh, ":DieuKhienDonHang")
    draw_entity_icon(ax, xs['table'], yh, ":Table")
    draw_entity_icon(ax, xs['dich'], yh, ":OrderTaiCho (Đích)")
    draw_entity_icon(ax, xs['nguon'], yh, ":OrderTaiCho (Nguồn)")

    for k, x in xs.items():
        y_top_line = yh - 0.82 if k in ('ql', 'nv', 'tn', 'ui', 'map_ui', 'order_ui', 'ctrl') else yh - 0.29
        draw_lifeline(ax, x, y_top_line, -13.2)

    draw_activation(ax, xs['tn'], -0.8, -12.8)
    draw_activation(ax, xs['ui'], -1.0, -12.8)
    draw_activation(ax, xs['ctrl'], -1.3, -12.5)
    draw_activation(ax, xs['table'], -1.5, -2.1)
    draw_activation(ax, xs['table'], -9.4, -10.1)
    draw_activation(ax, xs['dich'], -6.8, -8.6)
    draw_activation(ax, xs['nguon'], -5.6, -9.2)

    draw_message(ax, xs['tn'], xs['ui'], -1.0, "1: Nhấn nút Gộp đơn hàng")
    draw_message(ax, xs['ui'], xs['ctrl'], -1.3, "1.1: Yêu cầu danh sách bàn đang có khách")
    draw_message(ax, xs['ctrl'], xs['table'], -1.6, "1.1.1: Lấy các bàn đang phục vụ (chưa thanh toán)")
    draw_message(ax, xs['table'], xs['ctrl'], -2.0, "1.1.2: Danh sách bàn đang hoạt động", is_return=True)
    draw_message(ax, xs['ctrl'], xs['ui'], -2.3, "1.2: Hiển thị cửa sổ Gộp Đơn Hàng (3 phân vùng)", is_return=True)

    draw_message(ax, xs['tn'], xs['ui'], -3.1, "2: Chọn các bàn cần gộp (tối thiểu 2 bàn: Bàn 1, Bàn 3)")
    draw_message(ax, xs['ui'], xs['ctrl'], -3.5, "2.1: Yêu cầu xem trước kết quả gộp về Bàn 1")
    draw_message(ax, xs['ctrl'], xs['ctrl'], -4.0, "2.1.1: Gom món trùng, cộng dồn SL & tính tổng cộng", self_call=True)
    draw_message(ax, xs['ctrl'], xs['ui'], -4.5, "2.2: Hiển thị Chi tiết bàn đã chọn & Xem trước kết quả", is_return=True)

    draw_message(ax, xs['tn'], xs['ui'], -5.0, "3: Đối soát và nhấn [ Xác nhận gộp đơn hàng ]")
    draw_message(ax, xs['ui'], xs['ctrl'], -5.3, "3.1: Thực thi yêu cầu gộp đơn")

    draw_fragment(ax, 0.3, 13.4, -5.5, -12.4, "alt",
                  "Đã chọn tối thiểu ≥ 2 bàn hợp lệ",
                  "Chưa chọn đủ 2 bàn (< 2 bàn)",
                  y_divider=-11.1)

    draw_message(ax, xs['ctrl'], xs['nguon'], -6.0, "3.1.1: Lấy toàn bộ danh sách món của đơn bàn nguồn")
    draw_message(ax, xs['nguon'], xs['ctrl'], -6.4, "3.1.2: Danh sách OrderItem bàn nguồn", is_return=True)
    draw_message(ax, xs['ctrl'], xs['dich'], -7.1, "3.1.3: Dồn toàn bộ món sang đơn bàn đích & cộng dồn SL")
    draw_message(ax, xs['ctrl'], xs['dich'], -7.8, "3.1.4: Cập nhật lại Tạm tính, Giảm giá & Tổng cộng mới")
    draw_message(ax, xs['dich'], xs['ctrl'], -8.3, "3.1.5: Xác nhận cập nhật đơn đích", is_return=True)
    draw_message(ax, xs['ctrl'], xs['nguon'], -8.9, "3.1.6: Đóng đơn hàng gốc của bàn nguồn")
    draw_message(ax, xs['ctrl'], xs['table'], -9.6, "3.1.7: Giải phóng bàn nguồn về trạng thái Bàn trống")
    draw_message(ax, xs['ctrl'], xs['ui'], -10.2, "3.1.8: Lưu nhật ký & thông báo gộp đơn thành công", is_return=True)
    draw_message(ax, xs['ui'], xs['tn'], -10.7, "3.1.9: Đóng pop-up & làm mới màn hình Sơ đồ bàn", is_return=True)

    draw_message(ax, xs['ctrl'], xs['ui'], -11.6, "3.1.10: Trả về cảnh báo chưa đủ số bàn", is_return=True)
    draw_message(ax, xs['ui'], xs['tn'], -12.1, "3.1.11: Hiển thị: 'Vui lòng chọn tối thiểu 2 bàn để thực hiện gộp đơn'", is_return=True)

    add_vp_footer(ax, 13.8, -13.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'seq_pt_gop_don.png'))
    plt.close()


def gen_seq_pt_thanh_toan():
    fig, ax = plt.subplots(figsize=(14.0, 10.0), dpi=220)
    ax.set_xlim(-0.5, 13.8)
    ax.set_ylim(-13.8, 1.8)
    ax.axis('off')

    xs = {
        'tn': 0.8, 'ui': 2.9, 'ctrl': 5.2,
        'order': 7.5, 'pay': 9.6, 'table': 11.5, 'log': 13.1
    }
    yh = 0.8
    draw_actor(ax, xs['tn'], yh, "Thu ngân")
    draw_boundary_icon(ax, xs['ui'], yh, ":GiaoDienThanhToan")
    draw_controller_icon(ax, xs['ctrl'], yh, ":DieuKhienThanhToan")
    draw_entity_icon(ax, xs['order'], yh, ":Order")
    draw_entity_icon(ax, xs['pay'], yh, ":Payment")
    draw_entity_icon(ax, xs['table'], yh, ":Table")
    draw_entity_icon(ax, xs['log'], yh, ":PaymentLog")

    for k, x in xs.items():
        y_top_line = yh - 0.82 if k in ('ql', 'nv', 'tn', 'ui', 'map_ui', 'order_ui', 'ctrl') else yh - 0.29
        draw_lifeline(ax, x, y_top_line, -13.2)

    draw_activation(ax, xs['tn'], -0.8, -12.8)
    draw_activation(ax, xs['ui'], -1.0, -12.8)
    draw_activation(ax, xs['ctrl'], -1.3, -12.5)
    draw_activation(ax, xs['order'], -1.5, -2.1)
    draw_activation(ax, xs['order'], -7.5, -8.3)
    draw_activation(ax, xs['pay'], -6.0, -7.2)
    draw_activation(ax, xs['table'], -8.5, -9.2)
    draw_activation(ax, xs['log'], -9.4, -10.0)

    draw_message(ax, xs['tn'], xs['ui'], -1.0, "1: Mở danh sách & chọn đơn hàng cần thanh toán (HD001)")
    draw_message(ax, xs['ui'], xs['ctrl'], -1.3, "1.1: Yêu cầu thông tin chi tiết đơn hàng")
    draw_message(ax, xs['ctrl'], xs['order'], -1.6, "1.1.1: Lấy thông tin đơn & tổng tiền cần thanh toán")
    draw_message(ax, xs['order'], xs['ctrl'], -2.0, "1.1.2: Thông tin đơn hàng (350.000đ)", is_return=True)
    draw_message(ax, xs['ctrl'], xs['ui'], -2.4, "1.2: Hiển thị thông tin đơn & các phương thức thanh toán", is_return=True)

    draw_message(ax, xs['tn'], xs['ui'], -3.1, "2: Chọn phương thức (Tiền mặt / Thẻ) & nhập tiền khách đưa")
    draw_message(ax, xs['ui'], xs['ctrl'], -3.5, "2.1: Kiểm tra số tiền khách đưa & tính tiền thừa")
    draw_message(ax, xs['ctrl'], xs['ui'], -4.0, "2.2: Hiển thị số tiền thừa trả khách", is_return=True)

    draw_message(ax, xs['tn'], xs['ui'], -4.7, "3: Nhấn nút Xác nhận thanh toán")
    draw_message(ax, xs['ui'], xs['ctrl'], -5.1, "3.1: Yêu cầu xử lý thanh toán hóa đơn")

    draw_fragment(ax, 0.3, 13.5, -5.5, -12.6, "alt",
                  "Số tiền khách đưa ≥ Tổng tiền / Giao dịch hợp lệ",
                  "Số tiền khách đưa < Tổng tiền / Giao dịch thất bại",
                  y_divider=-11.0)

    draw_message(ax, xs['ctrl'], xs['pay'], -6.2, "3.1.1: Lưu thông tin thanh toán (Payment / PaymentTienMat)")
    draw_message(ax, xs['pay'], xs['ctrl'], -6.9, "3.1.2: Xác nhận lưu thanh toán", is_return=True)
    draw_message(ax, xs['ctrl'], xs['order'], -7.7, "3.1.3: Cập nhật trạng thái đơn -> Đã thanh toán")
    draw_message(ax, xs['ctrl'], xs['table'], -8.7, "3.1.4: Giải phóng bàn phục vụ về trạng thái Trống")
    draw_message(ax, xs['ctrl'], xs['log'], -9.6, "3.1.5: Ghi nhận lịch sử thanh toán (PaymentLog)")
    draw_message(ax, xs['ctrl'], xs['ui'], -10.2, "3.1.6: Thông báo thanh toán thành công", is_return=True)
    draw_message(ax, xs['ui'], xs['tn'], -10.65, "3.1.7: Hiển thị kết quả thanh toán & in hóa đơn", is_return=True)

    draw_message(ax, xs['ctrl'], xs['ui'], -11.75, "3.1.8: Báo lỗi số tiền không đủ hoặc giao dịch thất bại", is_return=True)
    draw_message(ax, xs['ui'], xs['tn'], -12.25, "3.1.9: Yêu cầu nhập lại số tiền hoặc chọn phương thức khác", is_return=True)

    add_vp_footer(ax, 13.8, -13.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'seq_pt_thanh_toan.png'))
    plt.close()


# ==============================================================================
# PHẦN II.6: BIỂU ĐỒ TRẠNG THÁI CHO CÁC LỚP (STATECHART DIAGRAMS)
# ==============================================================================
def draw_state_box(ax, cx, cy, w, h, title, actions=None):
    box = patches.FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                 boxstyle="round,pad=0.04,rounding_size=0.18",
                                 edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=4)
    ax.add_patch(box)
    if actions:
        header_y = cy + h/2 - 0.32
        ax.text(cx, header_y, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=VP_TEXT, zorder=6)
        div_y = cy + h/2 - 0.56
        ax.plot([cx - w/2, cx + w/2], [div_y, div_y], color=VP_BORDER, lw=1.0, zorder=5)
        for i, act in enumerate(actions):
            ax.text(cx - w/2 + 0.15, div_y - 0.24 - i*0.24, act, ha='left', va='center', fontsize=8, color=VP_TEXT, zorder=6)
    else:
        ax.text(cx, cy, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=VP_TEXT, zorder=6)

def draw_initial_state(ax, x, y, r=0.18):
    c = patches.Circle((x, y), r, edgecolor=VP_BORDER, facecolor=VP_BORDER, lw=1.2, zorder=5)
    ax.add_patch(c)

def draw_final_state(ax, x, y, r=0.22):
    outer = patches.Circle((x, y), r, edgecolor=VP_BORDER, facecolor=VP_BG_WHITE, lw=1.2, zorder=5)
    inner = patches.Circle((x, y), r * 0.62, edgecolor=VP_BORDER, facecolor=VP_BORDER, lw=1.0, zorder=6)
    ax.add_patch(outer)
    ax.add_patch(inner)

def draw_state_arrow(ax, x1, y1, x2, y2, label="", lx=None, ly=None, rad=0.0):
    conn = f"arc3,rad={rad}" if rad != 0 else "arc3,rad=0"
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', connectionstyle=conn, color=VP_BORDER, lw=1.2), zorder=5)
    if label:
        tx = lx if lx is not None else (x1 + x2) / 2
        ty = ly if ly is not None else (y1 + y2) / 2 + 0.16
        ax.text(tx, ty, label, ha='center', va='center', fontsize=8.2, color=VP_TEXT, zorder=7)

def gen_state_diagrams():
    # 1. State Diagram: Lớp Order (Đơn hàng)
    fig, ax = plt.subplots(figsize=(14.5, 8.2), dpi=220)
    ax.set_xlim(0, 14.5)
    ax.set_ylim(0, 8.2)
    ax.axis('off')

    draw_initial_state(ax, 0.6, 4.2)
    draw_state_box(ax, 2.7, 4.2, 2.3, 1.25, "Khởi tạo (Mới tạo)",
                   ["entry / khởi tạo mã đơn", "do / chọn bàn phục vụ"])
    draw_state_box(ax, 6.8, 4.2, 2.9, 1.45, "Đang phục vụ\n(DANG_PHUC_VU)",
                   ["entry / cập nhật bàn có khách", "do / thêm món, tính tổng tiền", "do / in phiếu chế biến tới bếp"])
    draw_state_box(ax, 6.8, 1.3, 2.8, 1.15, "Chờ thanh toán\n(CHO_THANH_TOAN)",
                   ["entry / khóa sửa món, in tạm tính"])
    draw_state_box(ax, 11.2, 6.6, 2.5, 1.1, "Đã gộp đơn\n(DA_GOP)",
                   ["entry / chuyển món sang đơn đích"])
    draw_state_box(ax, 11.2, 4.2, 2.5, 1.1, "Đã hủy\n(DA_HUY)",
                   ["entry / ghi nhận LyDoHuyDon"])
    draw_state_box(ax, 11.2, 1.3, 2.5, 1.15, "Đã thanh toán\n(DA_THANH_TOAN)",
                   ["entry / lưu Payment & PaymentLog"])
    draw_final_state(ax, 13.8, 3.9)

    draw_state_arrow(ax, 0.78, 4.2, 1.55, 4.2, "tạo đơn", lx=1.15, ly=4.45)
    draw_state_arrow(ax, 3.85, 4.2, 5.35, 4.2, "thêm món & Lưu\n[đơn có ≥ 1 món]", lx=4.6, ly=4.62)
    # Orthogonal self-loop above Đang phục vụ
    ax.plot([6.1, 6.1, 7.2, 7.2], [4.93, 5.65, 5.65, 4.93], color=VP_BORDER, lw=1.15, zorder=5)
    ax.annotate('', xy=(7.2, 4.93), xytext=(7.2, 5.15),
                arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.2), zorder=6)
    ax.text(6.65, 5.95, "gọi thêm món / nhận món từ đơn gộp\n/ cập nhật lại tongTien", ha='center', va='center', fontsize=8, color=VP_TEXT)

    draw_state_arrow(ax, 6.8, 3.47, 6.8, 1.88, "khách yêu cầu thanh toán", lx=5.55, ly=2.7)
    draw_state_arrow(ax, 7.9, 4.93, 9.95, 6.6, "gộp vào bàn đích\n[đơn bàn nguồn]", lx=8.7, ly=6.15)
    draw_state_arrow(ax, 8.25, 4.2, 9.95, 4.2, "hủy đơn\n[chọn lý do]", lx=9.1, ly=4.58)
    draw_state_arrow(ax, 8.2, 1.3, 9.95, 1.3, "xác nhận thanh toán\n[tiền nhận ≥ tổng tiền]", lx=9.08, ly=1.72)

    draw_state_arrow(ax, 12.45, 6.6, 13.7, 4.12, "giải phóng bàn nguồn", lx=13.35, ly=5.65)
    draw_state_arrow(ax, 12.45, 4.2, 13.58, 3.9, "kết thúc", lx=13.0, ly=4.35)
    draw_state_arrow(ax, 12.45, 1.3, 13.7, 3.68, "giải phóng bàn", lx=13.35, ly=2.3)

    add_vp_footer(ax, 14.5, 0.05)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'state_order.png'))
    plt.close()

    # 2. State Diagram: Lớp Table / RestaurantTable (Bàn ăn)
    fig, ax = plt.subplots(figsize=(12.0, 5.5), dpi=220)
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    draw_initial_state(ax, 1.0, 2.8)
    draw_state_box(ax, 4.0, 2.8, 2.8, 1.4, "Bàn trống\n(TRONG)",
                   ["entry / sẵn sàng đón khách", "do / hiển thị màu xám trên sơ đồ"])
    draw_state_box(ax, 8.8, 2.8, 3.0, 1.4, "Đang phục vụ\n(DANG_PHUC_VU)",
                   ["entry / gắn OrderTaiCho", "do / hiển thị màu xanh & số đơn"])
    draw_final_state(ax, 4.0, 0.7)

    draw_state_arrow(ax, 1.18, 2.8, 2.6, 2.8, "khởi tạo sơ đồ bàn")
    draw_state_arrow(ax, 5.4, 3.15, 7.3, 3.15, "tạo đơn mới trên bàn / chuyển bàn tới\n/ capNhatTrangThaiBan(DANG_PHUC_VU)", lx=6.35, ly=3.85)
    draw_state_arrow(ax, 7.3, 2.45, 5.4, 2.45, "thanh toán xong / gộp đơn (bàn nguồn) / hủy đơn\n/ giaiPhongBan(TRONG)", lx=6.35, ly=1.75)
    draw_state_arrow(ax, 4.0, 2.1, 4.0, 0.92, "đóng cửa / ngừng sử dụng bàn", lx=5.3, ly=1.45)

    add_vp_footer(ax, 12.0, 0.05)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'state_table.png'))
    plt.close()

    # 3. State Diagram: Lớp MenuItem / Combo (Thực đơn & Combo)
    fig, ax = plt.subplots(figsize=(12.5, 5.8), dpi=220)
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 5.8)
    ax.axis('off')

    draw_initial_state(ax, 0.8, 3.1)
    draw_state_box(ax, 3.1, 3.1, 2.4, 1.25, "Khởi tạo món / Combo",
                   ["entry / nhập tên, giá, món con", "do / kiểm tra hợp lệ"])
    draw_state_box(ax, 6.9, 3.1, 2.8, 1.35, "Đang kinh doanh\n(dangKinhDoanh = true)",
                   ["entry / hiển thị trên Menu gọi món", "do / cho phép chọn vào đơn"])
    draw_state_box(ax, 6.9, 0.9, 2.8, 1.15, "Tạm ngưng / Hết hàng\n(dangKinhDoanh = false)",
                   ["entry / khóa chọn món trên POS"])
    draw_state_box(ax, 10.6, 3.1, 2.2, 1.15, "Đã xóa khỏi Menu",
                   ["entry / ngừng kinh doanh"])
    draw_final_state(ax, 11.9, 1.2)

    draw_state_arrow(ax, 0.98, 3.1, 1.9, 3.1, "mở form tạo mới")
    draw_state_arrow(ax, 4.3, 3.1, 5.5, 3.1, "nhấn Lưu\n[dữ liệu hợp lệ]", lx=4.9, ly=3.55)
    draw_state_arrow(ax, 6.4, 2.42, 6.4, 1.48, "báo hết nguyên liệu", lx=5.45, ly=1.95)
    draw_state_arrow(ax, 7.4, 1.48, 7.4, 2.42, "mở bán lại", lx=8.1, ly=1.95)
    draw_state_arrow(ax, 8.3, 3.1, 9.5, 3.1, "quản lý xóa món/combo", lx=8.9, ly=3.5)
    draw_state_arrow(ax, 10.6, 2.52, 11.75, 1.35, "hoàn tất xóa", lx=11.45, ly=2.1)

    add_vp_footer(ax, 12.5, 0.05)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'state_menuitem.png'))
    plt.close()


# ==============================================================================
# PHẦN II.7: BIỂU ĐỒ HÀNH ĐỘNG CHO CÁC CHỨC NĂNG (ACTIVITY DIAGRAMS)
# Đồng bộ 100% phong cách Visual Paradigm của Activity Diagram1.jpg
# ==============================================================================
def draw_swimlane_frame(ax, total_w, total_h, lanes):
    # Outer border
    rect = patches.Rectangle((0, 0), total_w, total_h, edgecolor=VP_BORDER, facecolor=VP_BG_WHITE, lw=1.4, zorder=1)
    ax.add_patch(rect)
    header_h = 0.45
    ax.plot([0, total_w], [total_h - header_h, total_h - header_h], color=VP_BORDER, lw=1.3, zorder=2)

    x_curr = 0
    for i, (lane_name, lane_w) in enumerate(lanes):
        ax.text(x_curr + lane_w/2, total_h - header_h/2, lane_name,
                ha='center', va='center', fontsize=9.5, fontweight='bold', color=VP_TEXT, zorder=3)
        x_curr += lane_w
        if i < len(lanes) - 1:
            ax.plot([x_curr, x_curr], [0, total_h], color=VP_BORDER, lw=1.3, zorder=2)

def draw_act_node(ax, cx, cy, text, w=2.7, h=0.68):
    box = patches.FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                 boxstyle="round,pad=0.03,rounding_size=0.22",
                                 edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.1, zorder=4)
    ax.add_patch(box)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=8.3, color=VP_TEXT, zorder=5)

def draw_diamond(ax, cx, cy, label="", label_pos='top', w=0.56, h=0.42):
    pts = [(cx, cy + h/2), (cx + w/2, cy), (cx, cy - h/2), (cx - w/2, cy)]
    poly = patches.Polygon(pts, closed=True, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.1, zorder=4)
    ax.add_patch(poly)
    if label:
        if label_pos == 'top':
            ax.text(cx, cy + h/2 + 0.14, label, ha='center', va='bottom', fontsize=8, color=VP_TEXT, zorder=6)
        elif label_pos == 'bottom':
            ax.text(cx, cy - h/2 - 0.14, label, ha='center', va='top', fontsize=8, color=VP_TEXT, zorder=6)
        elif label_pos == 'right':
            ax.text(cx + w/2 + 0.12, cy, label, ha='left', va='center', fontsize=8, color=VP_TEXT, zorder=6)
        elif label_pos == 'left':
            ax.text(cx - w/2 - 0.12, cy, label, ha='right', va='center', fontsize=8, color=VP_TEXT, zorder=6)

def draw_ortho_arrow(ax, points, label="", lx=None, ly=None):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    if len(points) > 2:
        ax.plot(xs[:-1], ys[:-1], color=VP_BORDER, lw=1.05, zorder=3)
    ax.annotate('', xy=points[-1], xytext=points[-2],
                arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.1, shrinkA=0, shrinkB=0), zorder=4)
    if label:
        tx = lx if lx is not None else (points[0][0] + points[1][0]) / 2
        ty = ly if ly is not None else (points[0][1] + points[1][1]) / 2 + 0.12
        ax.text(tx, ty, label, ha='center', va='center', fontsize=8, color=VP_TEXT, zorder=6)

def gen_activity_tao_combo():
    total_w, total_h = 10.0, 14.5
    fig, ax = plt.subplots(figsize=(10.0, 14.5), dpi=220)
    ax.set_xlim(-0.1, total_w + 0.1)
    ax.set_ylim(-0.1, total_h + 0.1)
    ax.axis('off')

    draw_swimlane_frame(ax, total_w, total_h, [("Quản lý", 4.5), ("Hệ thống", 5.5)])
    x_ql = 2.25
    x_sys = 7.25

    draw_initial_state(ax, x_ql, 13.4, r=0.14)
    draw_act_node(ax, x_ql, 12.4, "Truy cập màn hình\nQuản lý thực đơn (Menu)")
    draw_act_node(ax, x_ql, 11.2, "Nhấn chọn chức năng\n[ + Tạo Combo mới ]")
    draw_act_node(ax, x_sys, 11.2, "Hiển thị biểu mẫu Tạo Combo\n& tải danh sách món lẻ đang bán")
    draw_act_node(ax, x_ql, 9.8, "Nhập tên combo, giá bán,\nsố người ăn dự kiến, mô tả")
    draw_act_node(ax, x_ql, 8.5, "Tìm kiếm & tích chọn món lẻ\nthành phần, nhập số lượng")
    draw_act_node(ax, x_sys, 8.5, "Tự động tính tổng giá trị gốc\ntham khảo của các món đã chọn")
    draw_diamond(ax, x_ql, 7.2, "Chọn thêm món lẻ?", label_pos='left')
    draw_act_node(ax, x_ql, 5.9, "Kiểm tra thông tin\nvà nhấn nút [ Lưu ]")
    draw_act_node(ax, x_sys, 5.9, "Kiểm tra tính hợp lệ\n(tên, giá > 0, ≥ 1 món con)")
    draw_diamond(ax, x_sys, 4.6, "Dữ liệu hợp lệ?", label_pos='left')
    draw_act_node(ax, x_sys, 3.3, "Hiển thị cảnh báo lỗi\n& giữ nguyên dữ liệu form", w=2.6)
    draw_act_node(ax, x_sys, 2.1, "Lưu Combo & ComboDetail\nvào cơ sở dữ liệu")
    draw_act_node(ax, x_sys, 1.05, "Thông báo 'Tạo combo thành công'\n& làm mới danh sách thực đơn")
    draw_final_state(ax, x_sys, 0.35, r=0.16)

    draw_ortho_arrow(ax, [(x_ql, 13.26), (x_ql, 12.74)])
    draw_ortho_arrow(ax, [(x_ql, 12.06), (x_ql, 11.54)])
    draw_ortho_arrow(ax, [(x_ql + 1.35, 11.2), (x_sys - 1.35, 11.2)])
    draw_ortho_arrow(ax, [(x_sys, 10.86), (x_sys, 10.35), (x_ql, 10.35), (x_ql, 10.14)])
    draw_ortho_arrow(ax, [(x_ql, 9.46), (x_ql, 8.84)])
    draw_ortho_arrow(ax, [(x_ql + 1.35, 8.5), (x_sys - 1.35, 8.5)])
    draw_ortho_arrow(ax, [(x_sys, 8.16), (x_sys, 7.2), (x_ql + 0.28, 7.2)])
    # Loop back to select more items
    draw_ortho_arrow(ax, [(x_ql, 7.41), (x_ql - 1.75, 7.41), (x_ql - 1.75, 8.5), (x_ql - 1.35, 8.5)],
                     "Có", lx=x_ql - 1.4, ly=7.6)
    draw_ortho_arrow(ax, [(x_ql, 6.99), (x_ql, 6.24)], "Không", lx=x_ql + 0.38, ly=6.65)
    draw_ortho_arrow(ax, [(x_ql + 1.35, 5.9), (x_sys - 1.35, 5.9)])
    draw_ortho_arrow(ax, [(x_sys, 5.56), (x_sys, 4.81)])
    # Invalid branch (straight down from diamond to error box)
    draw_ortho_arrow(ax, [(x_sys, 4.39), (x_sys, 3.64)], "Không", lx=x_sys - 0.38, ly=4.02)
    draw_ortho_arrow(ax, [(x_sys - 1.3, 3.3), (0.4, 3.3), (0.4, 9.8), (x_ql - 1.35, 9.8)])
    # Valid branch (right from diamond to save box)
    draw_ortho_arrow(ax, [(x_sys + 0.28, 4.6), (9.5, 4.6), (9.5, 2.1), (x_sys + 1.35, 2.1)], "Có", lx=8.5, ly=4.78)
    draw_ortho_arrow(ax, [(x_sys, 1.76), (x_sys, 1.39)])
    draw_ortho_arrow(ax, [(x_sys, 0.71), (x_sys, 0.51)])

    add_vp_footer(ax, total_w, 0.05)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'act_tao_combo.png'))
    plt.close()


def gen_activity_gop_don():
    total_w, total_h = 10.0, 14.5
    fig, ax = plt.subplots(figsize=(10.0, 14.5), dpi=220)
    ax.set_xlim(-0.1, total_w + 0.1)
    ax.set_ylim(-0.1, total_h + 0.1)
    ax.axis('off')

    draw_swimlane_frame(ax, total_w, total_h, [("Thu ngân / Nhân viên phục vụ", 4.5), ("Hệ thống", 5.5)])
    x_tn = 2.25
    x_sys = 7.25

    draw_initial_state(ax, x_tn, 13.4, r=0.14)
    draw_act_node(ax, x_tn, 12.4, "Nhấn nút [ Gộp đơn hàng ]\ntrên màn hình quản lý bàn")
    draw_act_node(ax, x_sys, 12.4, "Hiển thị cửa sổ Gộp Đơn Hàng\n& tải danh sách bàn đang có khách")
    draw_act_node(ax, x_tn, 11.0, "Tìm kiếm & tích chọn các bàn\ncần gộp (VD: Bàn 1 và Bàn 3)")
    draw_act_node(ax, x_sys, 11.0, "Đẩy bàn sang cột Chi tiết &\ntính Xem trước kết quả gộp (Bàn 1)")
    draw_act_node(ax, x_tn, 9.5, "Đối soát danh sách món,\nsố lượng, giảm giá & tổng cộng")
    draw_diamond(ax, x_tn, 8.2, "Đồng ý gộp?", label_pos='right')
    draw_act_node(ax, x_tn, 6.9, "Nhấn [ Xác nhận gộp đơn hàng ]")
    draw_diamond(ax, x_sys, 6.9, "Số bàn chọn ≥ 2?", label_pos='top')
    draw_act_node(ax, x_sys, 5.5, "Báo lỗi: 'Vui lòng chọn\ntối thiểu 2 bàn để gộp'", w=2.5)
    draw_act_node(ax, x_sys, 4.1, "Dồn món sang đơn bàn đích (Bàn 1)\n& cộng dồn số lượng, tính lại tiền")
    draw_act_node(ax, x_sys, 2.8, "Đóng đơn gốc bàn nguồn (Bàn 3)\n& giải phóng bàn nguồn về Bàn trống")
    draw_act_node(ax, x_sys, 1.5, "Ghi nhật ký OrderMergeLog\n& làm mới màn hình Sơ đồ bàn")
    draw_final_state(ax, x_sys, 0.45, r=0.16)

    draw_ortho_arrow(ax, [(x_tn, 13.26), (x_tn, 12.74)])
    draw_ortho_arrow(ax, [(x_tn + 1.35, 12.4), (x_sys - 1.35, 12.4)])
    draw_ortho_arrow(ax, [(x_sys, 12.06), (x_sys, 11.6), (x_tn, 11.6), (x_tn, 11.34)])
    draw_ortho_arrow(ax, [(x_tn + 1.35, 11.0), (x_sys - 1.35, 11.0)])
    draw_ortho_arrow(ax, [(x_sys, 10.66), (x_sys, 10.15), (x_tn, 10.15), (x_tn, 9.84)])
    draw_ortho_arrow(ax, [(x_tn, 9.16), (x_tn, 8.41)])
    # Cancel branch
    draw_ortho_arrow(ax, [(x_tn - 0.28, 8.2), (0.45, 8.2), (0.45, 0.45), (x_sys - 0.16, 0.45)],
                     "Hủy bỏ ([ Hủy ])", lx=1.2, ly=8.42)
    draw_ortho_arrow(ax, [(x_tn, 7.99), (x_tn, 7.24)], "Đồng ý", lx=x_tn + 0.42, ly=7.65)
    draw_ortho_arrow(ax, [(x_tn + 1.35, 6.9), (x_sys - 0.28, 6.9)])
    # < 2 tables
    draw_ortho_arrow(ax, [(x_sys, 6.69), (x_sys, 5.84)], "Không (< 2 bàn)", lx=x_sys - 0.75, ly=6.28)
    draw_ortho_arrow(ax, [(x_sys - 1.25, 5.5), (4.8, 5.5), (4.8, 11.0), (x_tn + 1.35, 11.0)])
    # >= 2 tables
    draw_ortho_arrow(ax, [(x_sys + 0.28, 6.9), (9.5, 6.9), (9.5, 4.1), (x_sys + 1.35, 4.1)], "Có (≥ 2 bàn)", lx=8.6, ly=7.12)
    draw_ortho_arrow(ax, [(x_sys, 3.76), (x_sys, 3.14)])
    draw_ortho_arrow(ax, [(x_sys, 2.46), (x_sys, 1.84)])
    draw_ortho_arrow(ax, [(x_sys, 1.16), (x_sys, 0.61)])

    add_vp_footer(ax, total_w, 0.05)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'act_gop_don.png'))
    plt.close()


def gen_activity_thanh_toan():
    total_w, total_h = 10.0, 14.5
    fig, ax = plt.subplots(figsize=(10.0, 14.5), dpi=220)
    ax.set_xlim(-0.1, total_w + 0.1)
    ax.set_ylim(-0.1, total_h + 0.1)
    ax.axis('off')

    draw_swimlane_frame(ax, total_w, total_h, [("Thu ngân", 4.5), ("Hệ thống", 5.5)])
    x_tn = 2.25
    x_sys = 7.25

    draw_initial_state(ax, x_tn, 13.4, r=0.14)
    draw_act_node(ax, x_tn, 12.4, "Mở màn hình Danh sách\nđơn chờ thanh toán")
    draw_act_node(ax, x_sys, 12.4, "Hiển thị danh sách các hóa đơn\nchưa thanh toán (Mã đơn, Bàn, Tiền)")
    draw_act_node(ax, x_tn, 11.1, "Chọn đơn hàng cần thanh toán\n(ví dụ: HD001 - Bàn 9)")
    draw_act_node(ax, x_sys, 11.1, "Hiển thị chi tiết đơn hàng &\nyêu cầu chọn phương thức thanh toán")
    draw_act_node(ax, x_tn, 9.7, "Chọn phương thức thanh toán\n(Tiền mặt / Thẻ / Chuyển khoản)")
    draw_act_node(ax, x_tn, 8.4, "Nhập số tiền khách đưa\nvà tiền tip (nếu có)")
    draw_act_node(ax, x_sys, 8.4, "Kiểm tra số tiền khách đưa\n& tự động tính tiền thừa")
    draw_diamond(ax, x_sys, 7.0, "Tiền nhận ≥ Tổng tiền?", label_pos='right')
    draw_act_node(ax, x_sys, 5.7, "Báo lỗi số tiền không đủ\n& yêu cầu nhập lại", w=2.5)
    draw_act_node(ax, x_tn, 4.4, "Kiểm tra bảng Xác nhận\nvà nhấn nút [ THANH TOÁN ]")
    draw_act_node(ax, x_sys, 3.1, "Lưu Payment / PaymentTienMat,\nđổi trạng thái đơn -> Đã thanh toán")
    draw_act_node(ax, x_sys, 1.7, "Giải phóng bàn về Bàn trống,\nghi PaymentLog & thông báo hoàn tất")
    draw_final_state(ax, x_sys, 0.5, r=0.16)

    draw_ortho_arrow(ax, [(x_tn, 13.26), (x_tn, 12.74)])
    draw_ortho_arrow(ax, [(x_tn + 1.35, 12.4), (x_sys - 1.35, 12.4)])
    draw_ortho_arrow(ax, [(x_sys, 12.06), (x_sys, 11.65), (x_tn, 11.65), (x_tn, 11.44)])
    draw_ortho_arrow(ax, [(x_tn + 1.35, 11.1), (x_sys - 1.35, 11.1)])
    draw_ortho_arrow(ax, [(x_sys, 10.76), (x_sys, 10.25), (x_tn, 10.25), (x_tn, 10.04)])
    draw_ortho_arrow(ax, [(x_tn, 9.36), (x_tn, 8.74)])
    draw_ortho_arrow(ax, [(x_tn + 1.35, 8.4), (x_sys - 1.35, 8.4)])
    draw_ortho_arrow(ax, [(x_sys, 8.06), (x_sys, 7.21)])
    # Not enough money
    draw_ortho_arrow(ax, [(x_sys, 6.79), (x_sys, 6.04)], "Không", lx=x_sys - 0.38, ly=6.42)
    draw_ortho_arrow(ax, [(x_sys - 1.25, 5.7), (0.45, 5.7), (0.45, 8.4), (x_tn - 1.35, 8.4)])
    # Enough money
    draw_ortho_arrow(ax, [(x_sys - 0.28, 7.0), (x_tn, 7.0), (x_tn, 4.74)], "Có", lx=4.9, ly=7.18)
    draw_ortho_arrow(ax, [(x_tn + 1.35, 4.4), (x_sys, 4.4), (x_sys, 3.44)])
    draw_ortho_arrow(ax, [(x_sys, 2.76), (x_sys, 2.04)])
    draw_ortho_arrow(ax, [(x_sys, 1.36), (x_sys, 0.66)])

    add_vp_footer(ax, total_w, 0.05)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'act_thanh_toan.png'))
    plt.close()


if __name__ == '__main__':
    gen_seq_pt_tao_combo()
    gen_seq_pt_tao_don()
    gen_seq_pt_gop_don()
    gen_seq_pt_thanh_toan()
    gen_state_diagrams()
    gen_activity_tao_combo()
    gen_activity_gop_don()
    gen_activity_thanh_toan()
    print("Successfully generated all analysis sequence, statechart, and activity diagrams!")
