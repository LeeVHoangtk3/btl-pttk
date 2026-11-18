"""
gen_deployment_spec.py - Generates Deployment Diagram for Câu 5.b
Matching the exact Visual Paradigm lecture template from deployment_diagram.png:
- Outer node packages: "Clients" and "Server" (with tab)
- 3D perspective boxes: <<processor>> or <<device>>
- Artifact boxes with top-right document dog-ear icon
- <<deploy>> dashed arrows pointing into processors
- Network connection links
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys

sys.path.append(os.path.dirname(__file__))
from vp_style import setup_canvas, add_vp_watermark, VP_BLUE, VP_BORDER, VP_TEXT, VP_BG_WHITE

def draw_dogear_artifact(ax, x, y, w, h, name, stereotype="artifact"):
    """Draws standard UML artifact box with top-right dog-ear page icon."""
    rect = patches.Rectangle((x, y), w, h, edgecolor=VP_BORDER, facecolor='#7ACFF5', lw=1.1, zorder=5)
    ax.add_patch(rect)

    # Dog-ear page icon in top-right
    ix = x + w - 0.40
    iy = y + h - 0.50
    iw, ih = 0.28, 0.38
    # Page rectangle
    ax.add_patch(patches.Rectangle((ix, iy), iw, ih, edgecolor=VP_BORDER, facecolor='#FFFFFF', lw=0.9, zorder=6))
    # Folded corner
    ax.plot([ix + iw - 0.09, ix + iw - 0.09, ix + iw], [iy + ih, iy + ih - 0.09, iy + ih - 0.09], color=VP_BORDER, lw=0.9, zorder=7)

    # Stereotype and name
    ax.text(x + 0.15, y + h - 0.25, f"<<{stereotype}>>", ha='left', va='center', fontsize=7.5, color='#333333', zorder=7)
    ax.text(x + w/2 - 0.1, y + 0.35, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=7)

def draw_3d_box(ax, x, y, w, h, depth=0.35, title="", stereotype=None):
    """Draws 3D isometric box."""
    dx = depth * 0.7
    dy = depth * 0.7

    # Front
    front = patches.Rectangle((x, y), w, h, edgecolor=VP_BORDER, facecolor='#7ACFF5', lw=1.2, zorder=4)
    ax.add_patch(front)

    # Top
    top_coords = [[x, y + h], [x + dx, y + h + dy], [x + w + dx, y + h + dy], [x + w, y + h]]
    top = patches.Polygon(top_coords, closed=True, edgecolor=VP_BORDER, facecolor='#7ACFF5', lw=1.2, zorder=3)
    ax.add_patch(top)

    # Right
    right_coords = [[x + w, y], [x + w + dx, y + dy], [x + w + dx, y + h + dy], [x + w, y + h]]
    right = patches.Polygon(right_coords, closed=True, edgecolor=VP_BORDER, facecolor='#7ACFF5', lw=1.2, zorder=3)
    ax.add_patch(right)

    # Text
    if stereotype:
        ax.text(x + w/2, y + h/2 + 0.22, f"<<{stereotype}>>", ha='center', va='center', fontsize=8, color='#333333', zorder=6)
        ax.text(x + w/2, y + h/2 - 0.15, title, ha='center', va='center', fontsize=9, fontweight='bold', color=VP_TEXT, zorder=6)
    else:
        ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=9, fontweight='bold', color=VP_TEXT, zorder=6)

def generate_spec_deployment_diagram(output_path=None):
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'diagrams', 'cau5b_deployment_j2ee.png')
    
    fig, ax = setup_canvas(width=16.0, height=10.5, dpi=240)
    ax.set_xlim(-0.5, 15.5)
    ax.set_ylim(-0.3, 10.3)

    # Outer Container 1: Clients (Left)
    c_x, c_y, c_w, c_h = 0.5, 2.5, 2.6, 6.2
    # Tab
    ax.add_patch(patches.Rectangle((c_x, c_y + c_h), 0.6, 0.45, edgecolor=VP_BORDER, facecolor='#7ACFF5', lw=1.2, zorder=3))
    # Body
    ax.add_patch(patches.Rectangle((c_x, c_y), c_w, c_h, edgecolor=VP_BORDER, facecolor='#7ACFF5', lw=1.2, zorder=2))
    ax.text(c_x + c_w/2, c_y + c_h - 0.25, "Clients", ha='center', va='center', fontsize=9.5, fontweight='bold', color=VP_TEXT, zorder=4)

    # Inside Clients: 2 3D nodes
    draw_3d_box(ax, 0.8, 6.0, 1.8, 1.6, depth=0.25, title="Máy trạm\nNhân viên")
    draw_3d_box(ax, 0.8, 3.2, 1.8, 1.6, depth=0.25, title="Máy trạm\nSinh viên")

    # Outer Container 2: Server (Right)
    s_x, s_y, s_w, s_h = 3.8, 0.5, 11.2, 9.0
    # Tab
    ax.add_patch(patches.Rectangle((s_x, s_y + s_h), 2.2, 0.45, edgecolor=VP_BORDER, facecolor='#7ACFF5', lw=1.2, zorder=3))
    # Body
    ax.add_patch(patches.Rectangle((s_x, s_y), s_w, s_h, edgecolor=VP_BORDER, facecolor='#7ACFF5', lw=1.2, zorder=2))
    ax.text(s_x + s_w/2, s_y + s_h - 0.25, "J2EE Server Architecture (Hạ tầng Máy chủ)", ha='center', va='center', fontsize=9.5, fontweight='bold', color=VP_TEXT, zorder=4)

    # Inside Server:
    # 1. J2EE Application Server (Middle)
    draw_3d_box(ax, 5.2, 3.8, 3.0, 2.4, depth=0.35, title="J2EE App Server\n(Tomcat 10)", stereotype="processor")

    # 2. Database Server (Right)
    draw_3d_box(ax, 11.0, 3.8, 3.0, 2.4, depth=0.35, title="Database Server\n(MySQL 8.0)", stereotype="processor")

    # Artifacts deployed into J2EE App Server
    draw_dogear_artifact(ax, 4.2, 7.2, 2.4, 1.1, "qltc-backend.war")
    draw_dogear_artifact(ax, 7.2, 7.2, 2.6, 1.1, "NhapDiemCtrl.class\nXemDiemCtrl.class")
    draw_dogear_artifact(ax, 5.4, 1.2, 2.6, 1.1, "DiemDAO.class\nSinhVienDAO.class")

    # Artifact deployed into Database Server
    draw_dogear_artifact(ax, 11.2, 7.2, 2.6, 1.1, "qltc_database.sql\n(MySQL Schema)")

    # Dashed <<deploy>> arrows from artifacts to processors
    # war -> App Server
    ax.annotate('', xy=(5.8, 5.8), xytext=(5.4, 7.2),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=7)
    ax.text(5.3, 6.5, "<<deploy>>", fontsize=7.5, color='#333333', style='italic', ha='right')

    # Controllers -> App Server
    ax.annotate('', xy=(7.2, 5.8), xytext=(8.0, 7.2),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=7)
    ax.text(7.9, 6.5, "<<deploy>>", fontsize=7.5, color='#333333', style='italic', ha='left')

    # DAOs -> App Server
    ax.annotate('', xy=(6.7, 3.8), xytext=(6.7, 2.3),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=7)
    ax.text(6.85, 3.0, "<<deploy>>", fontsize=7.5, color='#333333', style='italic', ha='left')

    # DB Schema -> DB Server
    ax.annotate('', xy=(12.5, 5.8), xytext=(12.5, 7.2),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=7)
    ax.text(12.7, 6.5, "<<deploy>>", fontsize=7.5, color='#333333', style='italic', ha='left')

    # Protocol link: Clients -> App Server (HTTP/HTTPS)
    ax.plot([2.8, 5.2], [6.8, 5.2], color=VP_BORDER, lw=1.3, zorder=6)
    ax.text(3.7, 6.2, "HTTP / HTTPS\n(Port 8080/443)", ha='center', va='bottom', fontsize=7.8, fontweight='bold', color=VP_TEXT, zorder=7)

    ax.plot([2.8, 5.2], [4.0, 4.6], color=VP_BORDER, lw=1.3, zorder=6)
    ax.text(3.7, 3.9, "HTTP / HTTPS\n(Port 8080/443)", ha='center', va='top', fontsize=7.8, fontweight='bold', color=VP_TEXT, zorder=7)

    # Protocol link: App Server -> Database Server (JDBC)
    ax.plot([8.5, 11.0], [5.0, 5.0], color=VP_BORDER, lw=1.3, zorder=6)
    ax.text(9.75, 5.2, "JDBC Driver\n(Port 3306)", ha='center', va='bottom', fontsize=7.8, fontweight='bold', color=VP_TEXT, zorder=7)

    add_vp_watermark(ax, coord_type='axes')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[OK] Deployment diagram generated successfully at: {output_path}")

    alt_path = os.path.join(os.path.dirname(__file__), '..', 'bt_11-11', 'diagrams', 'cau5b_deployment_j2ee.png')
    os.makedirs(os.path.dirname(alt_path), exist_ok=True)
    import shutil
    shutil.copy2(output_path, alt_path)

if __name__ == '__main__':
    generate_spec_deployment_diagram()
