"""
gen_class_analysis.py - Generates Analysis Class Diagram for Câu 2.b
Hệ thống Quản lý học tập theo tín chỉ (QLTC)
Tập trung vào 2 ca sử dụng:
1. Nhân viên Nhập điểm của sinh viên
2. Sinh viên Xem thông tin về kết quả học tập
Bao gồm các lớp thực thể:
- NhanVien, SinhVien, MonHoc, HocKy, LopHocPhan, Diem
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.dirname(__file__))
from vp_style import (setup_canvas, add_vp_watermark, draw_class_box, 
                      VP_BLUE, VP_BORDER, VP_TEXT)

def generate_analysis_class_diagram(output_path=None):
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'diagrams', 'cau2b_class_analysis.png')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = setup_canvas(width=15.5, height=10.5, dpi=240)
    ax.set_xlim(-0.5, 15.2)
    ax.set_ylim(-0.3, 10.5)

    # =========================================================================
    # ROW 1 (Top): NhanVien, LopHocPhan, MonHoc
    # =========================================================================
    # 1. NhanVien (Top Left)
    draw_class_box(ax, 0.5, 10.0, 3.4, 
                   class_name="NhanVien", 
                   attributes=[
                       "- maNV: String",
                       "- hoTen: String",
                       "- phongBan: String",
                       "- chucVu: String",
                       "- email: String",
                       "- sdt: String"
                   ],
                   methods=[
                       "+ getMaNV(): String",
                       "+ getHoTen(): String",
                       "+ nhapDiem(d: Diem): boolean",
                       "+ traCuuLop(maLHP: String): LopHocPhan"
                   ],
                   stereotype="entity")

    # 2. LopHocPhan (Top Center)
    draw_class_box(ax, 5.7, 10.0, 3.8,
                   class_name="LopHocPhan",
                   attributes=[
                       "- maLHP: String",
                       "- tenLHP: String",
                       "- siSo: int",
                       "- phongHoc: String",
                       "- monHoc: MonHoc",
                       "- hocKy: HocKy",
                       "- giangVien: NhanVien"
                   ],
                   methods=[
                       "+ getMaLHP(): String",
                       "+ getTenLHP(): String",
                       "+ getDanhSachSV(): List<SinhVien>",
                       "+ getBangDiem(): List<Diem>"
                   ],
                   stereotype="entity")

    # 3. MonHoc (Top Right)
    draw_class_box(ax, 11.2, 10.0, 3.5,
                   class_name="MonHoc",
                   attributes=[
                       "- maMH: String",
                       "- tenMH: String",
                       "- soTinChi: int",
                       "- heSoCC: float",
                       "- heSoKT: float",
                       "- heSoThi: float"
                   ],
                   methods=[
                       "+ getMaMH(): String",
                       "+ getTenMH(): String",
                       "+ getSoTinChi(): int",
                       "+ tinhDiemMon(): float"
                   ],
                   stereotype="entity")

    # =========================================================================
    # ROW 2 (Bottom): SinhVien, Diem, HocKy
    # =========================================================================
    # 4. SinhVien (Bottom Left)
    draw_class_box(ax, 0.5, 4.6, 3.4,
                   class_name="SinhVien",
                   attributes=[
                       "- maSV: String",
                       "- hoTen: String",
                       "- ngaySinh: Date",
                       "- gioiTinh: String",
                       "- lop: String",
                       "- khoaHoc: String",
                       "- nganh: String",
                       "- email: String"
                   ],
                   methods=[
                       "+ getMaSV(): String",
                       "+ getHoTen(): String",
                       "+ xemDiem(maHK: String): List<Diem>",
                       "+ tinhGPA(maHK: String): float",
                       "+ tinhCPA(): float"
                   ],
                   stereotype="entity")

    # 5. Diem (Bottom Center)
    draw_class_box(ax, 5.7, 4.6, 3.8,
                   class_name="Diem",
                   attributes=[
                       "- id: int",
                       "- sinhVien: SinhVien",
                       "- lopHocPhan: LopHocPhan",
                       "- diemCC: float",
                       "- diemKT: float",
                       "- diemThi: float",
                       "- diemTB: float",
                       "- diemChu: String",
                       "- diemHe4: float"
                   ],
                   methods=[
                       "+ tinhDiemTB(): float",
                       "+ quyDoiDiemChu(): String",
                       "+ quyDoiDiemHe4(): float",
                       "+ getDiemTB(): float",
                       "+ setDiemCC(d: float): void",
                       "+ setDiemKT(d: float): void",
                       "+ setDiemThi(d: float): void"
                   ],
                   stereotype="entity")

    # 6. HocKy (Bottom Right)
    draw_class_box(ax, 11.2, 4.6, 3.5,
                   class_name="HocKy",
                   attributes=[
                       "- maHocKy: String",
                       "- tenHocKy: String",
                       "- namHoc: String"
                   ],
                   methods=[
                       "+ getMaHocKy(): String",
                       "+ getTenHocKy(): String",
                       "+ getNamHoc(): String"
                   ],
                   stereotype="entity")

    # =========================================================================
    # ASSOCIATIONS & MULTIPLICITIES
    # =========================================================================
    # 1. NhanVien (1) ─── (*) LopHocPhan
    ax.plot([3.9, 5.7], [8.2, 8.2], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(4.05, 8.35, "1", fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)
    ax.text(5.45, 8.35, "0..*", fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)
    ax.text(4.8, 8.38, "phụ trách", ha='center', va='bottom', fontsize=7.8, color='#333333', style='italic', zorder=6)

    # 2. LopHocPhan (*) ─── (1) MonHoc
    ax.plot([9.5, 11.2], [8.2, 8.2], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(9.65, 8.35, "*", fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)
    ax.text(10.95, 8.35, "1", fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)
    ax.text(10.35, 8.38, "thuộc về", ha='center', va='bottom', fontsize=7.8, color='#333333', style='italic', zorder=6)

    # 3. LopHocPhan (1) ─── (*) Diem (Vertical between LopHocPhan and Diem)
    ax.plot([7.6, 7.6], [6.2, 4.6], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(7.75, 6.0, "1", fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)
    ax.text(7.75, 4.8, "*", fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)
    ax.text(7.9, 5.4, "có bảng điểm", ha='left', va='center', fontsize=7.8, color='#333333', style='italic', zorder=6)

    # 4. SinhVien (1) ─── (*) Diem (Horizontal between SinhVien and Diem)
    ax.plot([3.9, 5.7], [2.6, 2.6], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(4.05, 2.75, "1", fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)
    ax.text(5.45, 2.75, "*", fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)
    ax.text(4.8, 2.78, "kết quả", ha='center', va='bottom', fontsize=7.8, color='#333333', style='italic', zorder=6)

    # 5. LopHocPhan (*) ─── (1) HocKy (Orthogonal connection routed nicely)
    ax.plot([9.5, 10.35, 10.35, 11.2], [7.2, 7.2, 3.8, 3.8], color=VP_BORDER, lw=1.2, zorder=3)
    ax.text(9.65, 7.35, "*", fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)
    ax.text(10.9, 3.95, "1", fontsize=8.5, fontweight='bold', color=VP_TEXT, zorder=6)
    ax.text(10.45, 5.5, "trong kỳ", ha='left', va='center', fontsize=7.8, color='#333333', style='italic', zorder=6)

    # Watermark
    add_vp_watermark(ax, coord_type='axes')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[OK] Analysis Class diagram generated successfully at: {output_path}")

    alt_path = os.path.join(os.path.dirname(__file__), '..', 'bt_11-11', 'diagrams', 'cau2b_class_analysis.png')
    os.makedirs(os.path.dirname(alt_path), exist_ok=True)
    import shutil
    shutil.copy2(output_path, alt_path)

if __name__ == '__main__':
    generate_analysis_class_diagram()
