"""
gen_deployment.py - Generates Deployment Diagram for Câu 5.b
Hệ thống Quản lý học tập theo tín chỉ (QLTC)
Kiến trúc 3 tầng dựa trên công nghệ J2EE:
1. Client Tier (Web Browser / Desktop Client)
2. Application / Web Server Tier (J2EE App Server: Tomcat / WildFly)
3. Database Server Tier (MySQL / Oracle DB Server)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys

# Import shared VP style library
sys.path.append(os.path.dirname(__file__))
from vp_style import (setup_canvas, add_vp_watermark, draw_deployment_node_3d, 
                      draw_artifact_box, VP_BLUE, VP_BORDER, VP_TEXT, VP_BG_WHITE)

def generate_deployment_diagram(output_path=None):
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'diagrams', 'cau5b_deployment_j2ee.png')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = setup_canvas(width=16.5, height=11.5, dpi=240)
    ax.set_xlim(-0.5, 16.5)
    ax.set_ylim(-0.5, 11.5)

    # Title
    ax.text(8.0, 11.0, "BIỂU ĐỒ TRIỂN KHAI (DEPLOYMENT DIAGRAM) - KIẾN TRÚC 3 TẦNG J2EE", 
            ha='center', va='center', fontsize=11, fontweight='bold', color=VP_TEXT)

    # =========================================================================
    # TẦNG 1: CLIENT TIER (BÊN TRÁI)
    # =========================================================================
    # Node 1.1: Máy trạm Nhân viên
    draw_deployment_node_3d(ax, 0.5, 6.2, 3.8, 3.8, depth=0.45, 
                            title="Máy trạm Nhân viên (PC / Laptop)", stereotype="device")
    draw_artifact_box(ax, 0.8, 6.6, 3.2, 2.5, 
                      "Web Browser\n(ThemMonHocUI)\n[HTML5/CSS/JS]")

    # Node 1.2: Máy trạm Sinh viên
    draw_deployment_node_3d(ax, 0.5, 1.0, 3.8, 3.8, depth=0.45, 
                            title="Máy trạm Sinh viên (PC / Mobile)", stereotype="device")
    draw_artifact_box(ax, 0.8, 1.4, 3.2, 2.5, 
                      "Web Browser\n(DangKyMonHocUI)\n[Chrome/Edge/Safari]")

    # =========================================================================
    # TẦNG 2: APPLICATION & WEB SERVER TIER - J2EE (Ở GIỮA)
    # =========================================================================
    draw_deployment_node_3d(ax, 5.8, 1.0, 5.4, 9.2, depth=0.55, 
                            title="J2EE Application Server\n(Linux Ubuntu Server)", stereotype="device")
    
    # Execution Environment inside App Server (moved down slightly)
    env_rect = patches.Rectangle((6.2, 1.3), 4.6, 7.3, 
                                 edgecolor=VP_BORDER, facecolor='#E8F5FD', linestyle='--', lw=1.1, zorder=5)
    ax.add_patch(env_rect)
    ax.text(8.5, 8.4, "<<execution environment>>\nApache Tomcat 10 / WildFly J2EE", 
            ha='center', va='top', fontsize=8, color='#333333', zorder=6)

    # Artifact: QLTC_System.war
    draw_artifact_box(ax, 6.5, 1.6, 4.0, 6.0, 
                      "QLTC_System.war\n\n"
                      "-- Web Tier (Boundary) --\n"
                      "ThemMonHocServlet, JSP\n"
                      "DangKyMonHocServlet, JSP\n\n"
                      "-- Business Tier (Controller) --\n"
                      "ThemMonHocController\n"
                      "DangKyMonHocController\n\n"
                      "-- Persistence Tier (DAO/JPA) --\n"
                      "MonHocDAO, DangKyDAO\n"
                      "ConnectionPool (HikariCP)", 
                      stereotype="artifact")

    # =========================================================================
    # TẦNG 3: DATABASE TIER (BÊN PHẢI)
    # =========================================================================
    draw_deployment_node_3d(ax, 12.4, 2.2, 3.8, 7.0, depth=0.45, 
                            title="Database Server", stereotype="device")
    
    # Database System Environment
    db_env = patches.Rectangle((12.7, 2.6), 3.2, 5.6, 
                               edgecolor=VP_BORDER, facecolor='#E8F5FD', linestyle='--', lw=1.1, zorder=5)
    ax.add_patch(db_env)
    ax.text(14.3, 8.0, "<<database system>>\nMySQL 8.0 Server", 
            ha='center', va='top', fontsize=8, color='#333333', zorder=6)

    # Artifact inside DB: Schema & Tables
    draw_artifact_box(ax, 12.9, 3.0, 2.8, 4.2, 
                      "qltc_database.sql\n\n"
                      "tbl_MonHoc\n"
                      "tbl_SinhVien\n"
                      "tbl_LopHocPhan\n"
                      "tbl_DangKy\n"
                      "tbl_Diem", 
                      stereotype="artifact")

    # =========================================================================
    # COMMUNICATION PATHS / PROTOCOLS
    # =========================================================================
    # Link 1: Nhan vien PC ---> J2EE Server
    ax.plot([4.6, 5.8], [8.0, 7.2], color=VP_BORDER, lw=1.3, zorder=4)
    ax.text(5.2, 8.1, "HTTPS\n(Port 443)", ha='center', va='bottom', fontsize=8, fontweight='bold', color=VP_TEXT)

    # Link 2: Sinh vien PC ---> J2EE Server
    ax.plot([4.6, 5.8], [3.0, 3.8], color=VP_BORDER, lw=1.3, zorder=4)
    ax.text(5.2, 3.0, "HTTPS\n(Port 443)", ha='center', va='top', fontsize=8, fontweight='bold', color=VP_TEXT)

    # Link 3: J2EE Server ---> Database Server
    ax.plot([11.7, 12.4], [5.6, 5.6], color=VP_BORDER, lw=1.3, zorder=4)
    ax.text(12.05, 5.8, "JDBC / TCP-IP\n(Port 3306)", ha='center', va='bottom', fontsize=8, fontweight='bold', color=VP_TEXT)

    add_vp_watermark(ax, coord_type='axes')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[OK] Deployment diagram (J2EE 3-tier) generated successfully at: {output_path}")

if __name__ == '__main__':
    generate_deployment_diagram()
