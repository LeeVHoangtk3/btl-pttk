"""
gen_communication.py - Generates Communication Diagrams for Câu 3.b
Hệ thống Quản lý học tập theo tín chỉ (QLTC)
Tạo 2 biểu đồ giao tiếp (Communication Diagrams):
1. Nhân viên Thêm Môn học vào Danh sách môn học
2. Sinh viên Đăng ký môn học
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

# Import shared VP style library
sys.path.append(os.path.dirname(__file__))
from vp_style import (setup_canvas, add_vp_watermark, draw_actor, 
                      draw_communication_object, VP_BLUE, VP_BORDER, VP_TEXT)

def draw_msg_arrow(ax, x1, y1, x2, y2, text, direction='fwd', offset_y=0.22, offset_x=0.0):
    """Draws a directional message arrow and text alongside a link."""
    mx = (x1 + x2) / 2 + offset_x
    my = (y1 + y2) / 2 + offset_y
    
    dx = x2 - x1
    dy = y2 - y1
    dist = (dx**2 + dy**2)**0.5
    if dist > 0:
        ux = dx / dist
        uy = dy / dist
    else:
        ux, uy = 1, 0

    arrow_len = 0.35
    if direction == 'fwd':
        ax.annotate('', xy=(mx + ux * arrow_len, my + uy * arrow_len), 
                    xytext=(mx - ux * arrow_len, my - uy * arrow_len),
                    arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.2), zorder=6)
    else:
        ax.annotate('', xy=(mx - ux * arrow_len, my - uy * arrow_len), 
                    xytext=(mx + ux * arrow_len, my + uy * arrow_len),
                    arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.2), zorder=6)

    ax.text(mx, my + 0.12, text, ha='center', va='bottom', fontsize=8, fontweight='bold', color=VP_TEXT, zorder=7)

def generate_comm_them_mon(output_path=None):
    """Communication diagram for Thêm môn học."""
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'diagrams', 'cau3b_comm_them_mon.png')
    
    fig, ax = setup_canvas(width=15.5, height=9.0, dpi=240)
    ax.set_xlim(-0.5, 15.5)
    ax.set_ylim(-0.5, 9.0)

    # Title
    ax.text(7.5, 8.4, "BIỂU ĐỒ GIAO TIẾP (COMMUNICATION DIAGRAM) - THÊM MÔN HỌC", 
            ha='center', va='center', fontsize=11, fontweight='bold', color=VP_TEXT)

    # Participants
    # 1. Actor: Nhân viên (Left)
    draw_actor(ax, 0.8, 4.2, "Nhân viên", scale=1.1)

    # 2. Boundary: :ThemMonHocUI
    draw_communication_object(ax, 4.3, 4.2, 2.5, 1.2, ":ThemMonHocUI", stereotype="boundary")

    # 3. Controller: :ThemMonHocController
    draw_communication_object(ax, 9.0, 4.2, 2.9, 1.2, ":ThemMonHocController", stereotype="control")

    # 4. Entity: :MonHoc (Top Right)
    draw_communication_object(ax, 13.6, 6.6, 2.4, 1.1, ":MonHoc", stereotype="entity")

    # 5. DAO: :MonHocDAO (Bottom Right)
    draw_communication_object(ax, 13.6, 1.8, 2.4, 1.1, ":MonHocDAO", stereotype="dao")

    # Links (Solid lines)
    # Link 1: Nhan vien --- ThemMonHocUI
    ax.plot([1.2, 3.05], [4.2, 4.2], color=VP_BORDER, lw=1.2, zorder=3)
    draw_msg_arrow(ax, 1.2, 4.2, 3.05, 4.2, "1: moFormThemMon()\n2: nhapThongTin()\n3: bamLuu()", direction='fwd', offset_y=0.25)

    # Link 2: ThemMonHocUI --- ThemMonHocController
    ax.plot([5.55, 7.55], [4.2, 4.2], color=VP_BORDER, lw=1.2, zorder=3)
    draw_msg_arrow(ax, 5.55, 4.2, 7.55, 4.2, "3.1: themMonHoc(dto)", direction='fwd', offset_y=0.22)
    draw_msg_arrow(ax, 5.55, 4.2, 7.55, 4.2, "3.5: thongBaoKetQua()", direction='rev', offset_y=-0.52)

    # Link 3: ThemMonHocController --- MonHoc
    ax.plot([10.45, 12.4], [4.8, 6.3], color=VP_BORDER, lw=1.2, zorder=3)
    draw_msg_arrow(ax, 10.45, 4.8, 12.4, 6.3, "3.3: taoMonHocMoi()", direction='fwd', offset_y=0.25, offset_x=-0.5)

    # Link 4: ThemMonHocController --- MonHocDAO
    ax.plot([10.45, 12.4], [3.6, 2.1], color=VP_BORDER, lw=1.2, zorder=3)
    draw_msg_arrow(ax, 10.45, 3.6, 12.4, 2.1, "3.2: kiemTraTrungMa()\n3.4: insert(monHoc)", direction='fwd', offset_y=-0.45, offset_x=-0.5)

    # Self-message on controller: 3.1.1: kiemTraHopLe()
    ax.plot([8.4, 8.4, 9.6, 9.6], [4.8, 5.7, 5.7, 4.8], color=VP_BORDER, lw=1.1, zorder=3)
    ax.annotate('', xy=(9.55, 4.9), xytext=(9.55, 5.3),
                arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(9.0, 5.9, "3.1.1: kiemTraHopLe()", ha='center', va='bottom', fontsize=8, fontweight='bold', color=VP_TEXT)

    add_vp_watermark(ax, coord_type='axes')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[OK] Communication diagram (Them mon) generated at: {output_path}")

def generate_comm_dang_ky(output_path=None):
    """Communication diagram for Đăng ký môn học."""
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'diagrams', 'cau3b_comm_dang_ky.png')
    
    fig, ax = setup_canvas(width=16.0, height=9.5, dpi=240)
    ax.set_xlim(-0.5, 16.0)
    ax.set_ylim(-0.5, 9.5)

    # Title
    ax.text(7.8, 8.9, "BIỂU ĐỒ GIAO TIẾP (COMMUNICATION DIAGRAM) - ĐĂNG KÝ MÔN HỌC", 
            ha='center', va='center', fontsize=11, fontweight='bold', color=VP_TEXT)

    # Participants
    # 1. Actor: Sinh viên (Left)
    draw_actor(ax, 0.8, 4.5, "Sinh viên", scale=1.1)

    # 2. Boundary: :DangKyMonHocUI
    draw_communication_object(ax, 4.3, 4.5, 2.6, 1.2, ":DangKyMonHocUI", stereotype="boundary")

    # 3. Controller: :DangKyController
    draw_communication_object(ax, 9.2, 4.5, 2.8, 1.2, ":DangKyController", stereotype="control")

    # 4. Entity: :LopHocPhan (Top Right)
    draw_communication_object(ax, 14.2, 7.3, 2.5, 1.1, ":LopHocPhan", stereotype="entity")

    # 5. Entity: :DangKy (Middle Right)
    draw_communication_object(ax, 14.2, 4.5, 2.5, 1.1, ":DangKy", stereotype="entity")

    # 6. DAO: :DangKyDAO (Bottom Right)
    draw_communication_object(ax, 14.2, 1.7, 2.5, 1.1, ":DangKyDAO", stereotype="dao")

    # Links
    # Link 1: Sinh viên --- DangKyMonHocUI
    ax.plot([1.2, 3.0], [4.5, 4.5], color=VP_BORDER, lw=1.2, zorder=3)
    draw_msg_arrow(ax, 1.2, 4.5, 3.0, 4.5, "1: moGiaoDienDangKy()\n2: chonLopHP(maLop)\n3: bamXacNhanDK()", direction='fwd', offset_y=0.25)

    # Link 2: DangKyMonHocUI --- DangKyController
    ax.plot([5.6, 7.8], [4.5, 4.5], color=VP_BORDER, lw=1.2, zorder=3)
    draw_msg_arrow(ax, 5.6, 4.5, 7.8, 4.5, "3.1: dangKyMon(maSV, maLop)", direction='fwd', offset_y=0.22)
    draw_msg_arrow(ax, 5.6, 4.5, 7.8, 4.5, "3.7: thongBaoKetQua()", direction='rev', offset_y=-0.52)

    # Link 3: DangKyController --- LopHocPhan
    ax.plot([10.6, 12.95], [5.1, 6.8], color=VP_BORDER, lw=1.2, zorder=3)
    draw_msg_arrow(ax, 10.6, 5.1, 12.95, 6.8, "3.2: kiemTraSiSo()\n3.5: tangSiSo()", direction='fwd', offset_y=0.25, offset_x=-0.5)

    # Link 4: DangKyController --- DangKy (Entity)
    ax.plot([10.6, 12.95], [4.5, 4.5], color=VP_BORDER, lw=1.2, zorder=3)
    draw_msg_arrow(ax, 10.6, 4.5, 12.95, 4.5, "3.4: taoPhieuDK()", direction='fwd', offset_y=0.22)

    # Link 5: DangKyController --- DangKyDAO
    ax.plot([10.6, 12.95], [3.9, 2.2], color=VP_BORDER, lw=1.2, zorder=3)
    draw_msg_arrow(ax, 10.6, 3.9, 12.95, 2.2, "3.6: save(dangKy)", direction='fwd', offset_y=-0.45, offset_x=-0.5)

    # Self-messages on controller: 3.1.1: kiemTraTienQuyet(), 3.1.2: kiemTraTrungLich()
    ax.plot([8.5, 8.5, 9.9, 9.9], [5.1, 6.2, 6.2, 5.1], color=VP_BORDER, lw=1.1, zorder=3)
    ax.annotate('', xy=(9.85, 5.2), xytext=(9.85, 5.6),
                arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(9.2, 6.4, "3.1.1: kiemTraTienQuyet()\n3.1.2: kiemTraTrungLich()", ha='center', va='bottom', fontsize=7.8, fontweight='bold', color=VP_TEXT)

    add_vp_watermark(ax, coord_type='axes')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[OK] Communication diagram (Dang ky) generated at: {output_path}")

def generate_all_communication_diagrams():
    generate_comm_them_mon()
    generate_comm_dang_ky()

if __name__ == '__main__':
    generate_all_communication_diagrams()
