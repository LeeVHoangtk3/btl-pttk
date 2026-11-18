"""
gen_class_design.py - Generates Design Class Diagram (BCE) for Câu 3.a
Hệ thống Quản lý học tập theo tín chỉ (QLTC)
Thiết kế cho 2 ca sử dụng:
1. Nhân viên Nhập điểm của sinh viên
2. Sinh viên Xem thông tin về kết quả học tập
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.dirname(__file__))
from vp_style import (setup_canvas, add_vp_watermark, draw_class_box, 
                      VP_BLUE, VP_BORDER, VP_TEXT)

def generate_design_class_diagram(output_path=None):
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'diagrams', 'cau3a_class_design.png')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = setup_canvas(width=16.8, height=12.2, dpi=240)
    ax.set_xlim(-0.5, 16.8)
    ax.set_ylim(-1.0, 12.0)

    # Section 1 Header
    ax.text(0.5, 11.6, "1. Ca sử dụng: Nhân viên Nhập điểm của sinh viên", 
            fontsize=10, fontweight='bold', color='#003366')

    # =========================================================================
    # PHẦN 1: CA SỬ DỤNG "NHẬP ĐIỂM CỦA SINH VIÊN" (NỬA TRÊN)
    # =========================================================================
    # Boundary 1: NhapDiemUI
    draw_class_box(ax, 0.5, 11.2, 3.4,
                   class_name="NhapDiemUI",
                   attributes=[
                       "- cbHocKy: JComboBox",
                       "- cbLopHP: JComboBox",
                       "- tblBangDiem: JTable",
                       "- btnTaiDS: JButton",
                       "- btnLuuDiem: JButton",
                       "- btnHuy: JButton"
                   ],
                   methods=[
                       "+ hienThiDSLHP(ds: List<LopHocPhan>): void",
                       "+ hienThiBangDiem(ds: List<Diem>): void",
                       "+ docBangDiem(): List<Diem>",
                       "+ hienThiThongBao(msg: String): void"
                   ],
                   stereotype="boundary")

    # Controller 1: NhapDiemController
    draw_class_box(ax, 4.8, 11.2, 3.7,
                   class_name="NhapDiemController",
                   attributes=[
                       "- diemDAO: DiemDAO",
                       "- lhpDAO: LopHocPhanDAO",
                       "- uiNhapDiem: NhapDiemUI"
                   ],
                   methods=[
                       "+ layDSLHPTheoNV(maNV: String): List<LopHocPhan>",
                       "+ layBangDiemLHP(maLHP: String): List<Diem>",
                       "+ kiemTraDiemHopLe(d: Diem): boolean",
                       "+ tinhDiemTongKet(d: Diem): void",
                       "+ luuBangDiem(ds: List<Diem>): boolean"
                   ],
                   stereotype="control")

    # Entity 1: Diem
    draw_class_box(ax, 9.4, 11.2, 3.2,
                   class_name="Diem",
                   attributes=[
                       "- id: int",
                       "- maSV: String",
                       "- maLHP: String",
                       "- diemCC: float",
                       "- diemKT: float",
                       "- diemThi: float",
                       "- diemTB: float",
                       "- diemChu: String"
                   ],
                   methods=[
                       "+ tinhDiemTB(): float",
                       "+ quyDoiDiemChu(): String",
                       "+ quyDoiDiemHe4(): float",
                       "+ kiemTraHopLe(): boolean"
                   ],
                   stereotype="entity")

    # DAO 1: DiemDAO
    draw_class_box(ax, 13.2, 11.2, 3.2,
                   class_name="DiemDAO",
                   attributes=[
                       "- conn: Connection"
                   ],
                   methods=[
                       "+ getDiemByLHP(maLHP: String): List<Diem>",
                       "+ saveBangDiem(ds: List<Diem>): boolean",
                       "+ getDiemBySV(maSV: String, maHK: String): List<Diem>",
                       "+ updateDiem(d: Diem): boolean"
                   ],
                   stereotype="dao")

    # Relationships UC 1
    # NhapDiemUI -> NhapDiemController
    ax.annotate('', xy=(4.8, 9.4), xytext=(3.9, 9.4),
                arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.2), zorder=5)
    ax.text(4.35, 9.6, "<<use>>", ha='center', va='bottom', fontsize=7.5, color='#333333', style='italic')

    # NhapDiemController -> Diem
    ax.annotate('', xy=(9.4, 9.4), xytext=(8.5, 9.4),
                arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.2), zorder=5)
    ax.text(8.95, 9.6, "<<creates>>", ha='center', va='bottom', fontsize=7.5, color='#333333', style='italic')

    # NhapDiemController -> DiemDAO
    ax.annotate('', xy=(13.2, 10.6), xytext=(8.5, 10.6),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(10.85, 10.8, "<<calls>>", ha='center', va='bottom', fontsize=7.5, color='#333333', style='italic')

    # DiemDAO -> Diem
    ax.annotate('', xy=(12.6, 9.4), xytext=(13.2, 9.4),
                arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(12.9, 9.6, "1..*", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=VP_TEXT)

    # Section 2 Header
    ax.text(0.5, 5.8, "2. Ca sử dụng: Sinh viên Xem thông tin về kết quả học tập", 
            fontsize=10, fontweight='bold', color='#003366')

    # =========================================================================
    # PHẦN 2: CA SỬ DỤNG "XEM THÔNG TIN KẾT QUẢ HỌC TẬP" (NỬA DƯỚI)
    # =========================================================================
    # Boundary 2: XemDiemUI
    draw_class_box(ax, 0.5, 5.4, 3.4,
                   class_name="XemDiemUI",
                   attributes=[
                       "- cbHocKy: JComboBox",
                       "- tblKetQua: JTable",
                       "- lblGPA: JLabel",
                       "- lblCPA: JLabel",
                       "- btnTraCuu: JButton",
                       "- btnInPDF: JButton"
                   ],
                   methods=[
                       "+ hienThiDSHocKy(ds: List<HocKy>): void",
                       "+ hienThiKetQua(ds: List<Diem>, gpa: float, cpa: float): void",
                       "+ layHocKyDaChon(): String",
                       "+ xuatBaoCaoPDF(): void"
                   ],
                   stereotype="boundary")

    # Controller 2: XemDiemController
    draw_class_box(ax, 4.8, 5.4, 3.7,
                   class_name="XemDiemController",
                   attributes=[
                       "- diemDAO: DiemDAO",
                       "- sinhVienDAO: SinhVienDAO",
                       "- uiXemDiem: XemDiemUI"
                   ],
                   methods=[
                       "+ layDanhSachHocKy(): List<HocKy>",
                       "+ layKetQuaHocTap(maSV: String, maHK: String): List<Diem>",
                       "+ tinhGPA(ds: List<Diem>): float",
                       "+ tinhCPA(maSV: String): float",
                       "+ tinhTinChiTichLuy(maSV: String): int"
                   ],
                   stereotype="control")

    # Entity 2: SinhVien
    draw_class_box(ax, 9.4, 5.4, 3.2,
                   class_name="SinhVien",
                   attributes=[
                       "- maSV: String",
                       "- hoTen: String",
                       "- ngaySinh: Date",
                       "- gioiTinh: String",
                       "- lop: String",
                       "- khoaHoc: String",
                       "- nganh: String"
                   ],
                   methods=[
                       "+ getMaSV(): String",
                       "+ getHoTen(): String",
                       "+ getLop(): String",
                       "+ getThongTin(): String"
                   ],
                   stereotype="entity")

    # DAO 2: SinhVienDAO & DatabaseConnection
    draw_class_box(ax, 13.2, 5.4, 3.2,
                   class_name="SinhVienDAO",
                   attributes=[
                       "- conn: Connection"
                   ],
                   methods=[
                       "+ findByMa(maSV: String): SinhVien",
                       "+ getAllHocKy(): List<HocKy>",
                       "+ getTongTinChi(maSV: String): int"
                   ],
                   stereotype="dao")

    # Shared Database Connection Box (Bottom right)
    draw_class_box(ax, 13.2, 2.3, 3.2,
                   class_name="DatabaseConnection",
                   attributes=[
                       "- instance: DatabaseConnection",
                       "- conn: Connection",
                       "- URL: String",
                       "- USER: String"
                   ],
                   methods=[
                       "+ getInstance(): DatabaseConnection",
                       "+ getConnection(): Connection",
                       "+ closeConnection(): void"
                   ],
                   stereotype="dao")

    # Relationships UC 2
    # XemDiemUI -> XemDiemController
    ax.annotate('', xy=(4.8, 3.6), xytext=(3.9, 3.6),
                arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.2), zorder=5)
    ax.text(4.35, 3.8, "<<use>>", ha='center', va='bottom', fontsize=7.5, color='#333333', style='italic')

    # XemDiemController -> SinhVien
    ax.annotate('', xy=(9.4, 3.6), xytext=(8.5, 3.6),
                arrowprops=dict(arrowstyle='->', color=VP_BORDER, lw=1.2), zorder=5)
    ax.text(8.95, 3.8, "<<access>>", ha='center', va='bottom', fontsize=7.5, color='#333333', style='italic')

    # XemDiemController -> SinhVienDAO
    ax.annotate('', xy=(13.2, 4.8), xytext=(8.5, 4.8),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(10.85, 5.0, "<<calls>>", ha='center', va='bottom', fontsize=7.5, color='#333333', style='italic')

    # XemDiemController -> DiemDAO: Orthogonal routing below Diem, then up to DiemDAO
    ax.plot([7.2, 7.2, 14.8, 14.8], [5.4, 6.2, 6.2, 7.8], color=VP_BORDER, linestyle='--', lw=1.1, zorder=4)
    ax.annotate('', xy=(14.8, 8.0), xytext=(14.8, 7.7),
                arrowprops=dict(arrowstyle='->', linestyle='-', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(11.0, 6.4, "<<queries DiemDAO>>", ha='center', va='bottom', fontsize=7.5, color='#333333', style='italic')

    # DAOs -> DatabaseConnection
    ax.annotate('', xy=(14.8, 2.3), xytext=(14.8, 2.9),
                arrowprops=dict(arrowstyle='->', linestyle='--', color=VP_BORDER, lw=1.1), zorder=5)
    ax.text(15.0, 2.6, "<<uses>>", ha='left', va='center', fontsize=7.5, color='#333333', style='italic')

    # Watermark
    add_vp_watermark(ax, coord_type='axes')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[OK] Design Class diagram generated successfully at: {output_path}")

    alt_path = os.path.join(os.path.dirname(__file__), '..', 'bt_11-11', 'diagrams', 'cau3a_class_design.png')
    os.makedirs(os.path.dirname(alt_path), exist_ok=True)
    import shutil
    shutil.copy2(output_path, alt_path)

if __name__ == '__main__':
    generate_design_class_diagram()
