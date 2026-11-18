import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs('gen_diagrams', exist_ok=True)

VP_BLUE = '#7ACFF5'
VP_BORDER = '#000000'
VP_TEXT = '#000000'
VP_BG_WHITE = '#FFFFFF'

def draw_actor(ax, x, y, name):
    r = 0.22
    # Head
    circle = patches.Circle((x, y + 0.6), r, edgecolor=VP_BORDER, facecolor='none', lw=1.2, zorder=6)
    ax.add_patch(circle)
    # Body
    ax.plot([x, x], [y + 0.6 - r, y + 0.1], color=VP_BORDER, lw=1.3, zorder=6)
    # Arms
    ax.plot([x - 0.3, x + 0.3], [y + 0.32, y + 0.32], color=VP_BORDER, lw=1.3, zorder=6)
    # Legs
    ax.plot([x, x - 0.24], [y + 0.1, y - 0.35], color=VP_BORDER, lw=1.3, zorder=6)
    ax.plot([x, x + 0.24], [y + 0.1, y - 0.35], color=VP_BORDER, lw=1.3, zorder=6)
    # Text
    ax.text(x, y - 0.55, name, ha='center', va='top', fontsize=8.5, color=VP_TEXT, zorder=6)

def draw_component(ax, x, y, w, h, name, stereotype="component", is_db=False):
    rect = patches.Rectangle((x, y), w, h, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=4)
    ax.add_patch(rect)
    # Component icon in top right
    icon_w, icon_h = 0.35, 0.26
    ix, iy = x + w - icon_w - 0.12, y + h - icon_h - 0.12
    ax.add_patch(patches.Rectangle((ix, iy), icon_w, icon_h, edgecolor=VP_BORDER, facecolor=VP_BG_WHITE, lw=0.9, zorder=5))
    ax.add_patch(patches.Rectangle((ix - 0.08, iy + 0.14), 0.14, 0.06, edgecolor=VP_BORDER, facecolor=VP_BG_WHITE, lw=0.9, zorder=6))
    ax.add_patch(patches.Rectangle((ix - 0.08, iy + 0.05), 0.14, 0.06, edgecolor=VP_BORDER, facecolor=VP_BG_WHITE, lw=0.9, zorder=6))
    
    # Text
    if is_db:
        ax.text(x + w/2 - 0.15, y + h/2 + 0.35, f"<<{stereotype}>>", ha='center', va='center', fontsize=8, color=VP_TEXT, zorder=5)
        ax.text(x + w/2 - 0.15, y + h/2 + 0.1, "<<database>>", ha='center', va='center', fontsize=8, color=VP_TEXT, zorder=5)
        ax.text(x + w/2 - 0.15, y + h/2 - 0.22, name, ha='center', va='center', fontsize=9, fontweight='bold', color=VP_TEXT, zorder=5)
    else:
        ax.text(x + w/2 - 0.12, y + h/2 + 0.14, f"<<{stereotype}>>", ha='center', va='center', fontsize=8, color=VP_TEXT, zorder=5)
        ax.text(x + w/2 - 0.12, y + h/2 - 0.14, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=5)

def draw_ball_socket(ax, x_ball, y, name, x_left_start, x_right_end, label_above=True):
    # Left line to ball
    ax.plot([x_left_start, x_ball], [y, y], color=VP_BORDER, lw=1.2, zorder=3)
    # Ball
    ball = patches.Circle((x_ball, y), 0.14, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=5)
    ax.add_patch(ball)
    
    # Socket arc
    arc = patches.Arc((x_ball, y), 0.42, 0.42, angle=0, theta1=-90, theta2=90, color=VP_BORDER, lw=1.3, zorder=4)
    ax.add_patch(arc)
    # Right line from socket to right component
    ax.plot([x_ball + 0.21, x_right_end], [y, y], color=VP_BORDER, lw=1.2, zorder=3)
    
    # Label
    ly = y + 0.22 if label_above else y - 0.24
    va = 'bottom' if label_above else 'top'
    ax.text(x_ball, ly, name, ha='center', va=va, fontsize=8, color=VP_TEXT, zorder=6)

def generate_corrected_component_diagram():
    fig, ax = plt.subplots(figsize=(15.5, 10.5), dpi=240)
    ax.set_xlim(-0.8, 15.2)
    ax.set_ylim(-0.5, 11.0)
    ax.axis('off')

    # Watermark
    ax.text(14.8, -0.2, "Powered By Visual Paradigm Community Edition", 
            ha='right', va='bottom', fontsize=8, color='#666666', style='italic')

    # 1. Actors on the left
    draw_actor(ax, 0.2, 9.2, "Quản lý")
    draw_actor(ax, 0.2, 6.7, "Nhân viên order")
    draw_actor(ax, 0.2, 3.8, "Thu ngân (Gộp)")
    draw_actor(ax, 0.2, 1.2, "Thu ngân (TT)")

    # 2. UI Components (Boundary Layer)
    ui_x = 1.6
    ui_w = 2.4
    ui_h = 1.2
    draw_component(ax, ui_x, 8.6, ui_w, ui_h, "Giao diện Menu")
    draw_component(ax, ui_x, 6.1, ui_w, ui_h, "Giao diện Đơn hàng")
    draw_component(ax, ui_x, 3.2, ui_w, ui_h, "Giao diện Gộp đơn")
    draw_component(ax, ui_x, 0.6, ui_w, ui_h, "Giao diện Thanh toán")

    # Actor dependency lines (dashed)
    ax.annotate('', xy=(ui_x, 9.2), xytext=(0.5, 9.2), arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1))
    ax.annotate('', xy=(ui_x, 6.7), xytext=(0.5, 6.7), arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1))
    ax.annotate('', xy=(ui_x, 3.8), xytext=(0.5, 3.8), arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1))
    ax.annotate('', xy=(ui_x, 1.2), xytext=(0.5, 1.2), arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1))

    # 3. Service Components (Business Logic Layer)
    svc_x = 6.0
    svc_w = 2.6
    svc_h = 1.2
    draw_component(ax, svc_x, 8.6, svc_w, svc_h, "Dịch vụ Menu")
    draw_component(ax, svc_x, 6.1, svc_w, svc_h, "Dịch vụ Đơn hàng")
    draw_component(ax, svc_x, 3.2, svc_w, svc_h, "Dịch vụ Gộp đơn")
    draw_component(ax, svc_x, 0.6, svc_w, svc_h, "Dịch vụ Thanh toán")

    # CreditCardCharges component
    cc_x = 9.0
    cc_y = 6.8
    cc_w = 2.4
    cc_h = 1.1
    draw_component(ax, cc_x, cc_y, cc_w, cc_h, "CreditCardCharges")
    
    # Actor CreditCardAgency above CreditCardCharges
    draw_actor(ax, cc_x + cc_w/2, 9.3, "CreditCardAgency / VNPay")
    # Line from CreditCardAgency to CreditCardCharges
    ax.annotate('', xy=(cc_x + cc_w/2, cc_y + cc_h), xytext=(cc_x + cc_w/2, 8.7), 
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1))

    # 4. Ball & Socket Interfaces between UI and Services
    ball_x1 = 4.9
    draw_ball_socket(ax, ball_x1, 9.2, "IMenu", ui_x + ui_w, svc_x)
    draw_ball_socket(ax, ball_x1, 6.7, "IOrder", ui_x + ui_w, svc_x)
    draw_ball_socket(ax, ball_x1, 3.8, "IMergeOrder", ui_x + ui_w, svc_x)
    draw_ball_socket(ax, ball_x1, 1.2, "IPayment", ui_x + ui_w, svc_x)

    # Line from Payment Service to CreditCardCharges
    ax.plot([svc_x + svc_w, 8.8, 8.8, cc_x], [1.2, 1.2, cc_y + 0.55, cc_y + 0.55], color=VP_BORDER, lw=1.2)
    # Ball & Socket for Charge
    charge_ball_x = 8.8
    ball_c = patches.Circle((charge_ball_x, 4.0), 0.12, edgecolor=VP_BORDER, facecolor=VP_BLUE, lw=1.2, zorder=5)
    ax.add_patch(ball_c)
    arc_c = patches.Arc((charge_ball_x, 4.0), 0.38, 0.38, angle=90, theta1=-90, theta2=90, color=VP_BORDER, lw=1.2, zorder=4)
    ax.add_patch(arc_c)
    ax.text(charge_ball_x + 0.25, 4.0, "Charge", ha='left', va='center', fontsize=8, color=VP_TEXT)

    # 5. Database Component on the right
    db_x = 12.3
    db_y = 0.5
    db_w = 2.6
    db_h = 9.5
    draw_component(ax, db_x, db_y, db_w, db_h, "CSDL Nhà hàng\n(ThanhHoaRestaurantDB)", is_db=True)

    # 6. Ball & Socket Interfaces between Services and DB
    ball_x2 = 11.2
    draw_ball_socket(ax, ball_x2, 9.2, "IMenuData", svc_x + svc_w, db_x)
    draw_ball_socket(ax, ball_x2, 6.7, "IOrderData", svc_x + svc_w, db_x)
    draw_ball_socket(ax, ball_x2, 3.8, "IMergeData", svc_x + svc_w, db_x)
    draw_ball_socket(ax, ball_x2, 1.2, "IPaymentData", svc_x + svc_w, db_x)

    plt.tight_layout()
    plt.savefig('gen_diagrams/component_system_corrected.png')
    plt.close()
    print("Done generating corrected component diagram!")

if __name__ == '__main__':
    generate_corrected_component_diagram()
