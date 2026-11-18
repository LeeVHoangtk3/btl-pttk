"""
vp_style.py - Visual Paradigm Style Library for UML Diagrams using Matplotlib
Provides authentic Visual Paradigm Community Edition visual styling:
- Palette: Classic VP Blue (#7ACFF5), Crisp Black borders (#000000), White background (#FFFFFF)
- Standard UML Shapes: Use cases, Actors, Classes (BCE & standard), Packages, Communication links, 3D Deployment nodes
- Authentic VP Community Edition watermark
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# VP Color Constants
VP_BLUE = '#7ACFF5'
VP_BLUE_LIGHT = '#BCE8F9'
VP_BORDER = '#000000'
VP_TEXT = '#000000'
VP_BG_WHITE = '#FFFFFF'
VP_NOTE = '#FFFFCC'
VP_GRAY_LIGHT = '#F4F4F4'
VP_ORANGE = '#F88534'

DEFAULT_FONT = 'DejaVu Sans'

def setup_canvas(width=14.0, height=10.0, dpi=220, bg_color=VP_BG_WHITE):
    """Initializes matplotlib canvas with VP standard margins."""
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi, facecolor=bg_color)
    ax.set_facecolor(bg_color)
    ax.axis('off')
    return fig, ax

def add_vp_watermark(ax, x_max=1.0, y_min=0.0, coord_type='axes'):
    """Draws authentic Visual Paradigm Community Edition watermark."""
    if coord_type == 'axes':
        # Diamond logo
        diamond = patches.RegularPolygon((0.985, 0.02), numVertices=4, radius=0.012, 
                                        orientation=np.pi/4, facecolor='#DC3545', edgecolor='#B02A37', 
                                        lw=0.8, transform=ax.transAxes, zorder=100)
        ax.add_patch(diamond)
        ax.text(0.975, 0.02, "Powered By Visual Paradigm Community Edition", 
                ha='right', va='center', fontsize=8, color='#555555', 
                style='italic', fontfamily=DEFAULT_FONT, transform=ax.transAxes, zorder=100)
    else:
        ax.text(x_max - 0.2, y_min + 0.15, "Powered By Visual Paradigm Community Edition", 
                ha='right', va='bottom', fontsize=8, color='#555555', 
                style='italic', fontfamily=DEFAULT_FONT, zorder=100)

def draw_actor(ax, x, y, name, scale=1.0):
    """Draws standard Visual Paradigm actor stick figure."""
    r = 0.20 * scale
    # Head
    circle = patches.Circle((x, y + 0.55 * scale), r, edgecolor=VP_BORDER, facecolor='none', lw=1.2, zorder=6)
    ax.add_patch(circle)
    # Spine
    ax.plot([x, x], [y + 0.55 * scale - r, y + 0.08 * scale], color=VP_BORDER, lw=1.3, zorder=6)
    # Arms
    ax.plot([x - 0.26 * scale, x + 0.26 * scale], [y + 0.28 * scale, y + 0.28 * scale], color=VP_BORDER, lw=1.3, zorder=6)
    # Legs
    ax.plot([x, x - 0.22 * scale], [y + 0.08 * scale, y - 0.32 * scale], color=VP_BORDER, lw=1.3, zorder=6)
    ax.plot([x, x + 0.22 * scale], [y + 0.08 * scale, y - 0.32 * scale], color=VP_BORDER, lw=1.3, zorder=6)
    # Text
    ax.text(x, y - 0.45 * scale, name, ha='center', va='top', fontsize=9, fontweight='bold', color=VP_TEXT, zorder=6)

def draw_usecase_oval(ax, x, y, w, h, name, fill_color=VP_BLUE):
    """Draws standard Visual Paradigm Use Case ellipse."""
    ellipse = patches.Ellipse((x, y), w, h, edgecolor=VP_BORDER, facecolor=fill_color, lw=1.2, zorder=5)
    ax.add_patch(ellipse)
    ax.text(x, y, name, ha='center', va='center', fontsize=9, color=VP_TEXT, zorder=6, multialignment='center')

def draw_system_boundary(ax, x, y, w, h, title):
    """Draws system boundary box for Use Case diagram."""
    rect = patches.Rectangle((x, y), w, h, edgecolor='#333333', facecolor='#FAFAFA', lw=1.2, zorder=1)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 0.35, title, ha='center', va='top', fontsize=11, fontweight='bold', color=VP_TEXT, zorder=2)

def draw_boundary_icon(ax, x, y, name, r=0.28):
    """Draws BCE Boundary icon (circle with left vertical bar)."""
    circle = patches.Circle((x, y), r, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=5)
    ax.add_patch(circle)
    bar_x = x - r - 0.14
    ax.plot([bar_x, bar_x], [y - r - 0.1, y + r + 0.1], color=VP_BORDER, lw=1.2, zorder=5)
    ax.plot([bar_x, x - r], [y, y], color=VP_BORDER, lw=1.2, zorder=5)
    ax.text(x, y - r - 0.25, name, ha='center', va='top', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)

def draw_controller_icon(ax, x, y, name, r=0.28):
    """Draws BCE Controller icon (circle with clockwise arrow)."""
    circle = patches.Circle((x, y), r, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=5)
    ax.add_patch(circle)
    ax.annotate('', xy=(x + r*0.4, y + r + 0.08), xytext=(x - r*0.4, y + r + 0.08),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.4', color=VP_BORDER, lw=1.2), zorder=6)
    ax.text(x, y - r - 0.25, name, ha='center', va='top', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)

def draw_entity_icon(ax, x, y, name, r=0.28):
    """Draws BCE Entity icon (circle with base line)."""
    circle = patches.Circle((x, y), r, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=5)
    ax.add_patch(circle)
    ax.plot([x - r, x + r], [y - r, y - r], color=VP_BORDER, lw=1.2, zorder=5)
    ax.plot([x - r, x - r], [y - r, y - r - 0.08], color=VP_BORDER, lw=1.2, zorder=5)
    ax.plot([x + r, x + r], [y - r, y - r - 0.08], color=VP_BORDER, lw=1.2, zorder=5)
    ax.text(x, y - r - 0.25, name, ha='center', va='top', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)

def draw_class_box(ax, x, y, w, h=None, class_name="", attributes=[], methods=[], stereotype=None, fill_color=VP_BLUE):
    """
    Draws a standard 3-compartment UML Class diagram box in Visual Paradigm style.
    (x, y) is top-left coordinate.
    Calculates exact compartment heights automatically to avoid overlap.
    Returns (w, total_h, bottom_y).
    """
    header_h = 0.65 if stereotype else 0.45
    line_spacing = 0.22
    
    attr_count = len(attributes)
    attr_h = attr_count * line_spacing + 0.18 if attr_count > 0 else 0.25

    method_count = len(methods)
    method_h = method_count * line_spacing + 0.18 if method_count > 0 else 0.0

    calc_total_h = header_h + attr_h + method_h
    total_h = max(h, calc_total_h) if h is not None else calc_total_h

    # Adjust method_h if extra space
    if total_h > calc_total_h:
        if method_count > 0:
            method_h += (total_h - calc_total_h)
        else:
            attr_h += (total_h - calc_total_h)

    bottom_y = y - total_h

    # Main outer rectangle
    rect = patches.Rectangle((x, bottom_y), w, total_h, edgecolor=VP_BORDER, facecolor=fill_color, lw=1.1, zorder=4)
    ax.add_patch(rect)

    # Header texts
    if stereotype:
        ax.text(x + w/2, y - 0.18, f"<<{stereotype}>>", ha='center', va='center', fontsize=7.5, color='#333333', zorder=6)
        ax.text(x + w/2, y - 0.45, class_name, ha='center', va='center', fontsize=9, fontweight='bold', color=VP_TEXT, zorder=6)
    else:
        ax.text(x + w/2, y - header_h/2, class_name, ha='center', va='center', fontsize=9, fontweight='bold', color=VP_TEXT, zorder=6)

    # Divider below header
    div1_y = y - header_h
    ax.plot([x, x + w], [div1_y, div1_y], color=VP_BORDER, lw=1.0, zorder=5)

    # Attribute compartment
    attr_start_y = div1_y - 0.14
    for i, attr in enumerate(attributes):
        ax.text(x + 0.12, attr_start_y - i * line_spacing, attr, ha='left', va='center', fontsize=7.8, color=VP_TEXT, zorder=6)

    # Divider below attributes (if methods exist)
    if method_count > 0:
        div2_y = div1_y - attr_h
        ax.plot([x, x + w], [div2_y, div2_y], color=VP_BORDER, lw=1.0, zorder=5)

        # Method compartment
        method_start_y = div2_y - 0.14
        for j, m in enumerate(methods):
            ax.text(x + 0.12, method_start_y - j * line_spacing, m, ha='left', va='center', fontsize=7.8, color=VP_TEXT, zorder=6)

    return (w, total_h, bottom_y)

def draw_package_box(ax, x, y, w, h, package_name, fill_color=VP_BG_WHITE, tab_fill=VP_BLUE):
    """Draws a UML Package folder box with tab."""
    tab_w = min(2.2, w * 0.48)
    tab_h = 0.42
    # Tab
    tab = patches.Rectangle((x, y), tab_w, tab_h, edgecolor=VP_BORDER, facecolor=tab_fill, lw=1.1, zorder=4)
    ax.add_patch(tab)
    ax.text(x + tab_w/2, y + tab_h/2, package_name, ha='center', va='center', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)

    # Body
    body = patches.Rectangle((x, y - h), w, h, edgecolor=VP_BORDER, facecolor=fill_color, lw=1.1, zorder=3)
    ax.add_patch(body)

def draw_deployment_node_3d(ax, x, y, w, h, depth=0.35, title="", stereotype="device", fill_color=VP_BLUE):
    """
    Draws authentic Visual Paradigm 3D isometric box for deployment diagrams.
    (x, y) is bottom-left of front face.
    """
    dx = depth * 0.7
    dy = depth * 0.7

    # Front Face
    front = patches.Rectangle((x, y), w, h, edgecolor=VP_BORDER, facecolor=fill_color, lw=1.2, zorder=4)
    ax.add_patch(front)

    # Top Face (Polygon)
    top_coords = [[x, y + h], [x + dx, y + h + dy], [x + w + dx, y + h + dy], [x + w, y + h]]
    top = patches.Polygon(top_coords, closed=True, edgecolor=VP_BORDER, facecolor=fill_color, lw=1.2, zorder=3)
    ax.add_patch(top)

    # Right Face (Polygon)
    right_coords = [[x + w, y], [x + w + dx, y + dy], [x + w + dx, y + h + dy], [x + w, y + h]]
    right = patches.Polygon(right_coords, closed=True, edgecolor=VP_BORDER, facecolor=fill_color, lw=1.2, zorder=3)
    ax.add_patch(right)

    # Stereotype & Title
    if stereotype:
        ax.text(x + w/2, y + h - 0.25, f"<<{stereotype}>>", ha='center', va='top', fontsize=8, color='#333333', zorder=6)
        ax.text(x + w/2, y + h - 0.55, title, ha='center', va='top', fontsize=9.5, fontweight='bold', color=VP_TEXT, zorder=6)
    else:
        ax.text(x + w/2, y + h - 0.35, title, ha='center', va='top', fontsize=9.5, fontweight='bold', color=VP_TEXT, zorder=6)

def draw_artifact_box(ax, x, y, w, h, name, stereotype="artifact"):
    """Draws artifact nested rectangle inside a deployment node."""
    rect = patches.Rectangle((x, y), w, h, edgecolor=VP_BORDER, facecolor=VP_BG_WHITE, lw=1.0, zorder=5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 0.22, f"<<{stereotype}>>", ha='center', va='center', fontsize=7.5, color='#444444', zorder=6)
    ax.text(x + w/2, y + h/2 - 0.08, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6, multialignment='center')

def draw_communication_object(ax, x, y, w, h, obj_name, class_name=None, stereotype=None):
    """Draws object rectangle for UML Communication Diagram."""
    rect = patches.Rectangle((x - w/2, y - h/2), w, h, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.1, zorder=4)
    ax.add_patch(rect)
    label = f"{obj_name}:{class_name}" if class_name else obj_name
    if stereotype:
        ax.text(x, y + 0.15, f"<<{stereotype}>>", ha='center', va='center', fontsize=7.5, color='#333333', zorder=5)
        ax.text(x, y - 0.12, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=5)
    else:
        ax.text(x, y, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=5)

def draw_comm_link(ax, x1, y1, x2, y2, messages, msg_offset=0.25):
    """
    Draws an association link between two objects with numbered communication messages.
    messages is a list of tuples: (text, direction: 'fwd' or 'rev')
    """
    ax.plot([x1, x2], [y1, y2], color=VP_BORDER, lw=1.1, zorder=3)

    dx = x2 - x1
    dy = y2 - y1
    L = np.sqrt(dx*dx + dy*dy)
    if L == 0:
        return

    ux = dx / L
    uy = dy / L
    nx = -uy
    ny = ux

    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    for i, (msg, direction) in enumerate(messages):
        pos_offset = (i - (len(messages)-1)/2) * 0.35
        mx = mid_x + nx * msg_offset + ux * pos_offset
        my = mid_y + ny * msg_offset + uy * pos_offset

        arrow_len = 0.32
        if direction == 'fwd':
            ax.annotate('', xy=(mx + ux * arrow_len, my + uy * arrow_len), 
                        xytext=(mx - ux * arrow_len, my - uy * arrow_len),
                        arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.1), zorder=6)
        else:
            ax.annotate('', xy=(mx - ux * arrow_len, my - uy * arrow_len), 
                        xytext=(mx + ux * arrow_len, my + uy * arrow_len),
                        arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.1), zorder=6)

        text_y_shift = 0.18 if (abs(ux) > abs(uy)) else 0.0
        text_x_shift = 0.18 if (abs(uy) >= abs(ux)) else 0.0
        ax.text(mx + nx * text_y_shift + ux * text_x_shift, my + ny * text_y_shift + uy * text_x_shift, 
                msg, ha='center', va='center', fontsize=7.8, color=VP_TEXT, zorder=7)
