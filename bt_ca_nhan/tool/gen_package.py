"""
gen_package.py - Generates Package Diagram for Câu 5.a
Hệ thống Quản lý học tập theo tín chỉ (QLTC)
Tổ chức các lớp từ Câu 3.a vào các gói kiến trúc phân tầng:
- com.qltc.ui (Presentation / Boundary)
- com.qltc.controller (Business / Control)
- com.qltc.model (Domain / Entity)
- com.qltc.dao (Persistence / DAO)
- com.qltc.util (Utilities / DB Connection)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys

# Import shared VP style library
sys.path.append(os.path.dirname(__file__))
from vp_style import (setup_canvas, add_vp_watermark, draw_package_box, 
                      VP_BLUE, VP_BORDER, VP_TEXT, VP_BG_WHITE)

def draw_package_with_classes(ax, x, y, w, h, pkg_name, classes=[]):
    """Draws a package folder with inner class names."""
    # Folder tab
    tab_w = min(2.8, w * 0.55)
    tab_h = 0.45
    tab = patches.Rectangle((x, y), tab_w, tab_h, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=4)
    ax.add_patch(tab)
    ax.text(x + tab_w/2, y + tab_h/2, pkg_name, ha='center', va='center', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)

    # Folder body
    body = patches.Rectangle((x, y - h), w, h, edgecolor=VP_BORDER, facecolor='#F9FBFD', lw=1.2, zorder=3)
    ax.add_patch(body)

    # Inner classes (drawn as miniature VP class cards)
    for i, cls_name in enumerate(classes):
        card_w = w - 0.5
        card_h = 0.42
        card_x = x + 0.25
        card_y = y - 0.35 - (i + 1) * 0.52
        card = patches.Rectangle((card_x, card_y), card_w, card_h, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=0.9, zorder=5)
        ax.add_patch(card)
        ax.text(card_x + card_w/2, card_y + card_h/2, cls_name, ha='center', va='center', fontsize=8, fontweight='bold', color=VP_TEXT, zorder=6)

def generate_package_diagram(output_path=None):
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'diagrams', 'cau5a_package.png')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = setup_canvas(width=15.0, height=10.5, dpi=240)
    ax.set_xlim(-0.5, 15.0)
    ax.set_ylim(-0.5, 10.5)

    # Title
    ax.text(7.2, 10.0, "BIỂU ĐỒ GÓI (PACKAGE DIAGRAM) - HỆ THỐNG QLTC", 
            ha='center', va='center', fontsize=11, fontweight='bold', color=VP_TEXT)

    # 1. Package: com.qltc.ui (Top Left)
    draw_package_with_classes(ax, 0.8, 9.0, 3.6, 2.2, "com.qltc.ui", 
                              classes=["ThemMonHocUI", "DangKyMonHocUI"])

    # 2. Package: com.qltc.controller (Top Right)
    draw_package_with_classes(ax, 6.2, 9.0, 4.2, 2.2, "com.qltc.controller",
                              classes=["ThemMonHocController", "DangKyMonHocController"])

    # 3. Package: com.qltc.model (Middle / Bottom Left)
    draw_package_with_classes(ax, 11.5, 5.8, 3.2, 2.8, "com.qltc.model",
                              classes=["MonHoc", "LopHocPhan", "DangKy"])

    # 4. Package: com.qltc.dao (Middle / Bottom Center)
    draw_package_with_classes(ax, 6.2, 5.2, 4.2, 2.8, "com.qltc.dao",
                              classes=["MonHocDAO", "LopHocPhanDAO", "DangKyDAO"])

    # 5. Package: com.qltc.util (Bottom Left)
    draw_package_with_classes(ax, 0.8, 3.8, 3.6, 1.8, "com.qltc.util",
                              classes=["DatabaseConnection"])

    # =======================================================
    # Dependencies (Dashed arrows with <<use>>)
    # =======================================================

    # ui ---> controller
    ax.annotate('', xy=(6.2, 8.0), xytext=(4.4, 8.0),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.2), zorder=6)
    ax.text(5.3, 8.2, "<<use>>", ha='center', fontsize=8, color='#333333', style='italic')

    # controller ---> dao
    ax.annotate('', xy=(8.3, 5.2), xytext=(8.3, 6.8),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.2), zorder=6)
    ax.text(8.7, 6.0, "<<use>>", ha='left', fontsize=8, color='#333333', style='italic')

    # controller ---> model
    ax.annotate('', xy=(11.5, 6.5), xytext=(10.4, 7.8),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.2), zorder=6)
    ax.text(11.2, 7.4, "<<use>>", ha='center', fontsize=8, color='#333333', style='italic')

    # dao ---> model
    ax.annotate('', xy=(11.5, 4.2), xytext=(10.4, 4.2),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.2), zorder=6)
    ax.text(10.95, 4.4, "<<use>>", ha='center', fontsize=8, color='#333333', style='italic')

    # dao ---> util
    ax.annotate('', xy=(4.4, 2.8), xytext=(6.2, 3.6),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.2), zorder=6)
    ax.text(5.1, 3.4, "<<use>>", ha='center', fontsize=8, color='#333333', style='italic')

    add_vp_watermark(ax, coord_type='axes')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[OK] Package diagram generated successfully at: {output_path}")

if __name__ == '__main__':
    generate_package_diagram()
