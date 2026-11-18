"""
gen_package_spec.py - Generates Subsystem / Package Diagram for Câu 5.a
Matching the exact Visual Paradigm lecture template from package_diagram.png:
- Outer package containers with Specification Elements (left) and Realization Elements (right)
- Subpackages nested inside Realization Elements
- Dashed dependency arrows connecting packages
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys

sys.path.append(os.path.dirname(__file__))
from vp_style import setup_canvas, add_vp_watermark, VP_BLUE, VP_BORDER, VP_TEXT, VP_BG_WHITE

def draw_spec_package(ax, x, y, w, h, title, spec_items=[], subpackages=[]):
    """
    Draws a subsystem package matching package_diagram.png:
    - Tab on top-left with fork icon
    - Vertical divider line for Specification Elements
    - Subpackages in Realization Elements
    """
    # Outer body
    body = patches.Rectangle((x, y - h), w, h, edgecolor=VP_BORDER, facecolor='#7ACFF5', lw=1.2, zorder=2)
    ax.add_patch(body)

    # Tab
    tab_w = 2.4
    tab_h = 0.42
    tab = patches.Rectangle((x, y), tab_w, tab_h, edgecolor=VP_BORDER, facecolor='#7ACFF5', lw=1.2, zorder=3)
    ax.add_patch(tab)
    # Small fork symbol inside tab
    ax.plot([x + tab_w - 0.4, x + tab_w - 0.4, x + tab_w - 0.25, x + tab_w - 0.25], 
            [y + 0.12, y + 0.32, y + 0.32, y + 0.12], color=VP_BORDER, lw=1.0, zorder=4)
    ax.plot([x + tab_w - 0.325, x + tab_w - 0.325], [y + 0.32, y + 0.38], color=VP_BORDER, lw=1.0, zorder=4)

    # Title centered at top of body
    ax.text(x + w/2, y - 0.22, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=VP_TEXT, zorder=4)

    # Vertical divider for Specification Elements
    spec_w = 2.8
    ax.plot([x + spec_w, x + spec_w], [y - 0.45, y - h], color=VP_BORDER, lw=1.1, zorder=3)

    # Specification Elements Header & Items
    ax.text(x + spec_w/2, y - 0.70, "Specification Elements", ha='center', va='center', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=4)
    for i, item in enumerate(spec_items):
        ax.text(x + 0.22, y - 1.15 - i * 0.42, f"• {item}", ha='left', va='center', fontsize=7.8, color=VP_TEXT, zorder=4)

    # Realization Elements Header & Subpackages
    ax.text(x + spec_w + (w - spec_w)/2, y - 0.70, "Realization Elements", ha='center', va='center', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=4)

    # Draw subpackages inside Realization area
    n_sub = len(subpackages)
    sub_w = 2.6
    sub_h = 1.3
    start_x = x + spec_w + 0.6
    spacing = (w - spec_w - 1.2 - n_sub * sub_w) / max(1, n_sub - 1) if n_sub > 1 else 0

    for j, sub_name in enumerate(subpackages):
        sp_x = start_x + j * (sub_w + spacing)
        sp_y = y - 1.05
        
        # Subpackage tab
        sp_tab = patches.Rectangle((sp_x, sp_y), 0.55, 0.28, edgecolor=VP_BORDER, facecolor='#7ACFF5', lw=1.0, zorder=4)
        ax.add_patch(sp_tab)
        
        # Subpackage body
        sp_body = patches.Rectangle((sp_x, sp_y - sub_h), sub_w, sub_h, edgecolor=VP_BORDER, facecolor='#7ACFF5', lw=1.0, zorder=3)
        ax.add_patch(sp_body)
        
        ax.text(sp_x + sub_w/2, sp_y - sub_h/2, sub_name, ha='center', va='center', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=5)

def generate_spec_package_diagram(output_path=None):
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'diagrams', 'cau5a_package.png')
    
    fig, ax = setup_canvas(width=14.5, height=11.5, dpi=240)
    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(-0.2, 11.2)

    # Top Package: Presentation Layer
    draw_spec_package(ax, 0.5, 10.6, 13.0, 2.7, 
                      title="Presentation Layer (Giao diện người dùng)", 
                      spec_items=["INhapDiemUI", "IXemDiemUI"], 
                      subpackages=["NhapDiemUI", "XemDiemUI"])

    # Middle Package: Business Logic Layer
    draw_spec_package(ax, 0.5, 7.1, 13.0, 2.7, 
                      title="Business Logic Layer (Điều khiển nghiệp vụ)", 
                      spec_items=["INhapDiemService", "IXemDiemService"], 
                      subpackages=["NhapDiemController", "XemDiemController"])

    # Bottom Package: Persistence / Domain Layer
    draw_spec_package(ax, 0.5, 3.6, 13.0, 2.8, 
                      title="Persistence & Domain Layer (Dữ liệu & CSDL)", 
                      spec_items=["IDiemDAO", "ILopHocPhanDAO", "ISinhVienDAO"], 
                      subpackages=["DomainModel", "DiemDAO", "SinhVienDAO"])

    # Connecting Dashed Dependency Arrows between Packages
    # Top -> Middle
    ax.annotate('', xy=(7.0, 7.1), xytext=(7.0, 7.9),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.2), zorder=5)
    ax.text(7.25, 7.5, "<<import>>", ha='left', va='center', fontsize=8, color='#333333', style='italic')

    # Middle -> Bottom
    ax.annotate('', xy=(7.0, 3.6), xytext=(7.0, 4.4),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.2), zorder=5)
    ax.text(7.25, 4.0, "<<access>>", ha='left', va='center', fontsize=8, color='#333333', style='italic')

    add_vp_watermark(ax, coord_type='axes')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[OK] Package diagram generated successfully at: {output_path}")

    alt_path = os.path.join(os.path.dirname(__file__), '..', 'bt_11-11', 'diagrams', 'cau5a_package.png')
    os.makedirs(os.path.dirname(alt_path), exist_ok=True)
    import shutil
    shutil.copy2(output_path, alt_path)

if __name__ == '__main__':
    generate_spec_package_diagram()
