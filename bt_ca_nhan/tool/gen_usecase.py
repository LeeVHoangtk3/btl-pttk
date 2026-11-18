"""
gen_usecase.py - Generates Use Case Diagram for Câu 1.a
Hệ thống Quản lý học tập theo tín chỉ (QLTC)
Yêu cầu đề bài (btap_11-11.png):
1. Nhân viên Nhập điểm của sinh viên
2. Sinh viên Xem thông tin về kết quả học tập
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.dirname(__file__))
from vp_style import (setup_canvas, add_vp_watermark, draw_actor, 
                      draw_usecase_oval, draw_system_boundary, 
                      VP_BLUE, VP_BORDER, VP_TEXT)

def generate_usecase_diagram(output_path=None):
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'diagrams', 'cau1a_usecase.png')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = setup_canvas(width=13.5, height=8.8, dpi=240)
    ax.set_xlim(-1.5, 12.5)
    ax.set_ylim(-0.8, 8.5)

    # 1. System Boundary
    draw_system_boundary(ax, 1.8, -0.2, 8.2, 8.2, "Hệ thống Quản lý học tập theo tín chỉ (QLTC)")

    # 2. Actors
    draw_actor(ax, 0.2, 5.0, "Nhân viên", scale=1.1)
    draw_actor(ax, 11.2, 3.2, "Sinh viên", scale=1.1)

    # 3. Use Cases (Ovals)
    # Common Login Use Case at top center
    draw_usecase_oval(ax, 5.9, 7.0, 2.7, 0.95, "Đăng nhập\nhệ thống")
    
    # Use Case 1: Nhập điểm của sinh viên (Nhân viên)
    draw_usecase_oval(ax, 4.8, 5.0, 3.0, 1.15, "Nhập điểm của\nsinh viên")
    draw_usecase_oval(ax, 8.2, 5.2, 2.6, 0.95, "Tra cứu lớp học phần\n& bảng điểm")
    draw_usecase_oval(ax, 3.8, 3.2, 2.6, 0.95, "Tính điểm tổng kết\n& quy đổi điểm chữ")
    
    # Use Case 2: Xem thông tin về kết quả học tập (Sinh viên)
    draw_usecase_oval(ax, 7.2, 2.8, 3.0, 1.15, "Xem thông tin về\nkết quả học tập")
    draw_usecase_oval(ax, 5.2, 1.1, 2.7, 0.95, "Tra cứu bảng điểm\ntheo học kỳ")
    draw_usecase_oval(ax, 8.8, 0.9, 2.4, 0.90, "In bảng điểm /\nXuất kết quả (PDF)")

    # 4. Association Links (Solid Lines between Actors and Primary Use Cases)
    # Nhan vien -> Nhap diem
    ax.plot([0.5, 3.3], [5.0, 5.0], color=VP_BORDER, lw=1.2, zorder=4)
    # Nhan vien -> Dang nhap
    ax.plot([0.5, 4.55], [5.3, 7.0], color=VP_BORDER, lw=1.2, zorder=4)

    # Sinh vien -> Xem thong tin ket qua hoc tap
    ax.plot([10.9, 8.7], [3.2, 2.8], color=VP_BORDER, lw=1.2, zorder=4)
    # Sinh vien -> Dang nhap
    ax.plot([10.9, 7.25], [3.5, 7.0], color=VP_BORDER, lw=1.2, zorder=4)

    # 5. Stereotype Relationships (<<include>>, <<extend>>)
    # Nhap diem -> <<include>> -> Dang nhap
    ax.annotate('', xy=(5.2, 6.55), xytext=(4.8, 5.6),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(4.6, 6.1, "<<include>>", fontsize=7.8, color='#333333', style='italic', va='center')

    # Nhap diem -> <<include>> -> Tra cuu lop hoc phan
    ax.annotate('', xy=(6.9, 5.2), xytext=(6.3, 5.05),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(6.6, 5.35, "<<include>>", fontsize=7.5, color='#333333', style='italic', ha='center')

    # Nhap diem -> <<include>> -> Tinh diem tong ket
    ax.annotate('', xy=(4.1, 3.7), xytext=(4.5, 4.45),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(3.9, 4.15, "<<include>>", fontsize=7.5, color='#333333', style='italic', ha='center')

    # Sinh vien -> Dang nhap directly via Actor line or Use Case include:
    # Instead of crossing the middle, curve or position it nicely
    ax.annotate('', xy=(6.7, 6.55), xytext=(7.4, 3.4),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(7.35, 4.8, "<<include>>", fontsize=7.8, color='#333333', style='italic', va='center')

    # Xem thong tin -> <<include>> -> Tra cuu bang diem theo hoc ky
    ax.annotate('', xy=(5.8, 1.6), xytext=(6.6, 2.25),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(5.9, 2.1, "<<include>>", fontsize=7.8, color='#333333', style='italic', va='center')

    # In bang diem -> <<extend>> -> Xem thong tin
    ax.annotate('', xy=(7.9, 2.25), xytext=(8.4, 1.35),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(8.4, 1.9, "<<extend>>", fontsize=7.8, color='#333333', style='italic', va='center')

    # Watermark
    add_vp_watermark(ax, coord_type='axes')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[OK] Use Case diagram generated successfully at: {output_path}")

    # Also duplicate into bt_11-11/diagrams/ if exists
    alt_path = os.path.join(os.path.dirname(__file__), '..', 'bt_11-11', 'diagrams', 'cau1a_usecase.png')
    os.makedirs(os.path.dirname(alt_path), exist_ok=True)
    import shutil
    shutil.copy2(output_path, alt_path)

if __name__ == '__main__':
    generate_usecase_diagram()
