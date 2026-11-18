"""
gen_communication_lanes.py - Generates Swimlane Communication Diagrams for Câu 3.b
Matching the exact Visual Paradigm lecture template from comunivation_diagram.png:
- 4 Horizontal Swimlanes:
  * Actor lane (Top)
  * View lane (Boundary icons)
  * Control lane (Controller icons)
  * Model lane (Entity/DAO icons)
- Solid association links with directional triangle arrows and numbered messages

Generates 2 diagrams:
1. cau3b_comm_nhap_diem.png: Ca sử dụng "Nhân viên Nhập điểm của sinh viên"
2. cau3b_comm_xem_diem.png: Ca sử dụng "Sinh viên Xem thông tin về kết quả học tập"
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys

sys.path.append(os.path.dirname(__file__))
from vp_style import setup_canvas, add_vp_watermark, draw_actor, VP_BLUE, VP_BORDER, VP_TEXT

def draw_swimlanes(ax, x_min, x_max, y_top, y_bottom, lanes):
    """Draws horizontal swimlane dividers and labels on the left."""
    frame = patches.Rectangle((x_min, y_bottom), x_max - x_min, y_top - y_bottom,
                              edgecolor=VP_BORDER, facecolor='#FFFFFF', lw=1.2, zorder=1)
    ax.add_patch(frame)

    for name, yt, yb in lanes:
        ax.plot([x_min, x_max], [yb, yb], color=VP_BORDER, lw=1.0, zorder=2)
        mid_y = (yt + yb) / 2
        ax.text(x_min + 0.3, mid_y, name, ha='left', va='center', fontsize=10, fontweight='bold', color=VP_TEXT, zorder=3)

def draw_vp_bce_icon(ax, x, y, name, bce_type='boundary', r=0.28, label_side='bottom'):
    """Draws authentic Visual Paradigm BCE circular icons."""
    circle = patches.Circle((x, y), r, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=5)
    ax.add_patch(circle)

    if bce_type == 'boundary':
        bar_x = x - r - 0.12
        ax.plot([bar_x, bar_x], [y - r - 0.08, y + r + 0.08], color=VP_BORDER, lw=1.2, zorder=5)
        ax.plot([bar_x, x - r], [y, y], color=VP_BORDER, lw=1.2, zorder=5)
    elif bce_type == 'control':
        ax.annotate('', xy=(x + r*0.4, y + r + 0.08), xytext=(x - r*0.4, y + r + 0.08),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.4', color=VP_BORDER, lw=1.2), zorder=6)
    elif bce_type == 'entity':
        ax.plot([x - r, x + r], [y - r, y - r], color=VP_BORDER, lw=1.2, zorder=5)
        ax.plot([x - r, x - r], [y - r, y - r - 0.06], color=VP_BORDER, lw=1.2, zorder=5)
        ax.plot([x + r, x + r], [y - r, y - r - 0.06], color=VP_BORDER, lw=1.2, zorder=5)

    if label_side == 'bottom':
        ax.text(x, y - r - 0.22, name, ha='center', va='top', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)
    elif label_side == 'right':
        ax.text(x + r + 0.14, y, name, ha='left', va='center', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)
    elif label_side == 'left':
        ax.text(x - r - 0.14, y, name, ha='right', va='center', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)

def draw_triangle_arrow(ax, x, y, orientation=0.0):
    """Draws small directional filled triangle."""
    arrow = patches.RegularPolygon((x, y), numVertices=3, radius=0.08, orientation=orientation, facecolor='#000000', zorder=8)
    ax.add_patch(arrow)

# =============================================================================
# DIAGRAM 1: NHẬP ĐIỂM CỦA SINH VIÊN
# =============================================================================
def generate_swimlane_comm_nhap_diem(output_path=None):
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'diagrams', 'cau3b_comm_nhap_diem.png')
    
    fig, ax = setup_canvas(width=15.0, height=9.2, dpi=240)
    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(-0.2, 9.0)

    lanes = [
        ("Nhân viên", 8.8, 7.0),
        ("View", 7.0, 5.0),
        ("Control", 5.0, 3.0),
        ("Model", 3.0, 0.4)
    ]
    draw_swimlanes(ax, 0.0, 14.0, 8.8, 0.4, lanes)

    draw_actor(ax, 1.8, 7.8, "Nhân viên", scale=0.95)
    draw_vp_bce_icon(ax, 4.2, 6.0, ":NhapDiemUI", bce_type='boundary', label_side='bottom')
    draw_vp_bce_icon(ax, 7.8, 4.0, ":NhapDiemController", bce_type='control', label_side='right')
    draw_vp_bce_icon(ax, 4.8, 1.5, ":Diem", bce_type='entity', label_side='bottom')
    draw_vp_bce_icon(ax, 11.2, 1.5, ":DiemDAO", bce_type='entity', label_side='bottom')

    # Link: Actor -> View
    ax.plot([2.2, 3.8], [7.5, 6.1], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(3.5, 7.4, "1: moFormNhapDiem()\n2: chonLHP(maLHP)\n3: nhapDiemVaLuu()", ha='left', va='center', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 3.2, 6.8, orientation=-0.6)

    # Link: View -> Control
    ax.plot([4.6, 7.4], [5.9, 4.2], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(6.3, 5.65, "2.1: layBangDiem(maLHP)\n3.1: luuBangDiem(dsDiem)", ha='center', va='bottom', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 6.3, 5.35, orientation=-0.4)

    ax.text(5.3, 4.75, "2.2: hienThiBangDiem()\n3.5: thongBaoKetQua()", ha='center', va='top', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 5.3, 5.0, orientation=2.6)

    # Self call on Control: Kiem tra diem hop le
    ax.plot([7.6, 7.6, 8.0, 8.0], [4.35, 4.85, 4.85, 4.35], color=VP_BORDER, lw=1.1, zorder=3)
    ax.text(8.2, 4.7, "3.1.1: kiemTraHopLe()", ha='left', va='center', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 8.0, 4.45, orientation=-1.57)

    # Link: Control -> Diem Entity
    ax.plot([7.5, 5.2], [3.7, 1.8], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(5.5, 3.2, "3.1.2: tinhDiemTB()\n3.1.3: quyDoiDiemChu()", ha='center', va='center', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 6.2, 2.7, orientation=-2.3)

    # Link: Control -> DiemDAO
    ax.plot([8.1, 10.9], [3.7, 1.8], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(9.9, 3.1, "2.1.1: getDiemByLHP(maLHP)\n3.1.4: saveBangDiem(dsDiem)", ha='left', va='center', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 9.4, 2.8, orientation=-0.7)

    ax.text(9.1, 2.2, "2.1.2: traVeDanhSach()", ha='right', va='center', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 9.5, 2.4, orientation=2.4)

    add_vp_watermark(ax, coord_type='axes')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[OK] Communication diagram (Nhap diem) generated successfully at: {output_path}")

    alt_path = os.path.join(os.path.dirname(__file__), '..', 'bt_11-11', 'diagrams', 'cau3b_comm_nhap_diem.png')
    os.makedirs(os.path.dirname(alt_path), exist_ok=True)
    import shutil
    shutil.copy2(output_path, alt_path)

# =============================================================================
# DIAGRAM 2: XEM KẾT QUẢ HỌC TẬP
# =============================================================================
def generate_swimlane_comm_xem_diem(output_path=None):
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'diagrams', 'cau3b_comm_xem_diem.png')
    
    fig, ax = setup_canvas(width=15.0, height=9.2, dpi=240)
    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(-0.2, 9.0)

    lanes = [
        ("Sinh viên", 8.8, 7.0),
        ("View", 7.0, 5.0),
        ("Control", 5.0, 3.0),
        ("Model", 3.0, 0.4)
    ]
    draw_swimlanes(ax, 0.0, 14.0, 8.8, 0.4, lanes)

    draw_actor(ax, 1.8, 7.8, "Sinh viên", scale=0.95)
    draw_vp_bce_icon(ax, 4.2, 6.0, ":XemDiemUI", bce_type='boundary', label_side='bottom')
    draw_vp_bce_icon(ax, 7.8, 4.0, ":XemDiemController", bce_type='control', label_side='right')
    draw_vp_bce_icon(ax, 4.8, 1.5, ":SinhVien", bce_type='entity', label_side='bottom')
    draw_vp_bce_icon(ax, 11.2, 1.5, ":DiemDAO", bce_type='entity', label_side='bottom')

    # Link: Actor -> View
    ax.plot([2.2, 3.8], [7.5, 6.1], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(3.5, 7.4, "1: moTrangXemDiem()\n2: chonHocKy(maHK)\n3: xuatBaoCaoPDF()", ha='left', va='center', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 3.2, 6.8, orientation=-0.6)

    # Link: View -> Control
    ax.plot([4.6, 7.4], [5.9, 4.2], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(6.3, 5.65, "2.1: layKetQua(maSV, maHK)\n3.1: xuatPDF(maSV, maHK)", ha='center', va='bottom', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 6.3, 5.35, orientation=-0.4)

    ax.text(5.3, 4.75, "2.4: hienThiKetQua(dsDiem, GPA)\n3.2: traVeFilePDF()", ha='center', va='top', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 5.3, 5.0, orientation=2.6)

    # Self call on Control: Tinh diem GPA
    ax.plot([7.6, 7.6, 8.0, 8.0], [4.35, 4.85, 4.85, 4.35], color=VP_BORDER, lw=1.1, zorder=3)
    ax.text(8.2, 4.7, "2.2: tinhGPA(dsDiem)", ha='left', va='center', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 8.0, 4.45, orientation=-1.57)

    # Link: Control -> SinhVien Entity
    ax.plot([7.5, 5.2], [3.7, 1.8], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(5.5, 3.2, "2.3: layThongTinSV()\ngetMaSV(), getLop()", ha='center', va='center', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 6.2, 2.7, orientation=-2.3)

    # Link: Control -> DiemDAO
    ax.plot([8.1, 10.9], [3.7, 1.8], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(9.9, 3.1, "2.1.1: getDiemBySV(maSV, maHK)\n2.1.2: getTongTinChi(maSV)", ha='left', va='center', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 9.4, 2.8, orientation=-0.7)

    ax.text(9.1, 2.2, "2.1.3: traVeDanhSachDiem()", ha='right', va='center', fontsize=7.8, color=VP_TEXT, zorder=7)
    draw_triangle_arrow(ax, 9.5, 2.4, orientation=2.4)

    add_vp_watermark(ax, coord_type='axes')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[OK] Communication diagram (Xem diem) generated successfully at: {output_path}")

    alt_path = os.path.join(os.path.dirname(__file__), '..', 'bt_11-11', 'diagrams', 'cau3b_comm_xem_diem.png')
    os.makedirs(os.path.dirname(alt_path), exist_ok=True)
    import shutil
    shutil.copy2(output_path, alt_path)

def generate_all_swimlane_comm(output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'diagrams')
    os.makedirs(output_dir, exist_ok=True)
    
    p1 = os.path.join(output_dir, 'cau3b_comm_nhap_diem.png')
    p2 = os.path.join(output_dir, 'cau3b_comm_xem_diem.png')
    generate_swimlane_comm_nhap_diem(p1)
    generate_swimlane_comm_xem_diem(p2)

if __name__ == '__main__':
    generate_all_swimlane_comm()
