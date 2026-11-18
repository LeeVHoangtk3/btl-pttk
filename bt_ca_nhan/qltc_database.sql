-- =============================================================================
-- HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG
-- KHOA CÔNG NGHỆ THÔNG TIN 1
-- BÀI KIỂM TRA PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG THÔNG TIN (QLTC)
-- Sinh viên thực hiện: LÊ VIỆT HOÀNG - MSV: B23DCKH044 - Lớp: N13
-- CƠ SỞ DỮ LIỆU: qltc_db (MySQL 8.0+)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS qltc_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE qltc_db;

-- -----------------------------------------------------------------------------
-- 1. BẢNG NHÂN VIÊN / GIẢNG VIÊN (tbl_nhan_vien)
-- -----------------------------------------------------------------------------
CREATE TABLE tbl_nhan_vien (
    ma_nv VARCHAR(20) NOT NULL PRIMARY KEY,
    ho_ten VARCHAR(100) NOT NULL,
    phong_ban VARCHAR(100) NOT NULL,
    chuc_vu VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    sdt VARCHAR(15)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 2. BẢNG SINH VIÊN (tbl_sinh_vien)
-- -----------------------------------------------------------------------------
CREATE TABLE tbl_sinh_vien (
    ma_sv VARCHAR(20) NOT NULL PRIMARY KEY,
    ho_ten VARCHAR(100) NOT NULL,
    ngay_sinh DATE NOT NULL,
    gioi_tinh VARCHAR(10) NOT NULL,
    lop VARCHAR(30) NOT NULL,
    khoa_hoc VARCHAR(20) NOT NULL,
    nganh VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 3. BẢNG HỌC KỲ (tbl_hoc_ky)
-- -----------------------------------------------------------------------------
CREATE TABLE tbl_hoc_ky (
    ma_hoc_ky VARCHAR(20) NOT NULL PRIMARY KEY,
    ten_hoc_ky VARCHAR(50) NOT NULL,
    nam_hoc VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 4. BẢNG MÔN HỌC (tbl_mon_hoc)
-- -----------------------------------------------------------------------------
CREATE TABLE tbl_mon_hoc (
    ma_mh VARCHAR(20) NOT NULL PRIMARY KEY,
    ten_mh VARCHAR(150) NOT NULL,
    so_tin_chi INT NOT NULL CHECK (so_tin_chi > 0),
    he_so_cc FLOAT NOT NULL DEFAULT 0.10,
    he_so_kt FLOAT NOT NULL DEFAULT 0.20,
    he_so_thi FLOAT NOT NULL DEFAULT 0.70,
    CONSTRAINT ck_trong_so CHECK (he_so_cc >= 0 AND he_so_kt >= 0 AND he_so_thi >= 0
        AND ABS(he_so_cc + he_so_kt + he_so_thi - 1) < 0.0001)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 5. BẢNG LỚP HỌC PHẦN (tbl_lop_hoc_phan)
-- -----------------------------------------------------------------------------
CREATE TABLE tbl_lop_hoc_phan (
    ma_lhp VARCHAR(30) NOT NULL PRIMARY KEY,
    ten_lhp VARCHAR(150) NOT NULL,
    ma_mh VARCHAR(20) NOT NULL,
    ma_hoc_ky VARCHAR(20) NOT NULL,
    ma_nv VARCHAR(20) NOT NULL,
    si_so INT NOT NULL DEFAULT 0,
    phong_hoc VARCHAR(30),
    CONSTRAINT fk_lhp_monhoc FOREIGN KEY (ma_mh) REFERENCES tbl_mon_hoc(ma_mh) ON DELETE RESTRICT,
    CONSTRAINT fk_lhp_hocky FOREIGN KEY (ma_hoc_ky) REFERENCES tbl_hoc_ky(ma_hoc_ky) ON DELETE RESTRICT,
    CONSTRAINT fk_lhp_nhanvien FOREIGN KEY (ma_nv) REFERENCES tbl_nhan_vien(ma_nv) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 6. BẢNG ĐIỂM KẾT QUẢ HỌC TẬP (tbl_diem)
-- -----------------------------------------------------------------------------
-- Dang ky ton tai truoc khi co diem.
CREATE TABLE tbl_dang_ky (
    ma_sv VARCHAR(20) NOT NULL,
    ma_lhp VARCHAR(30) NOT NULL,
    ngay_dang_ky DATE NOT NULL,
    PRIMARY KEY (ma_sv,ma_lhp),
    FOREIGN KEY (ma_sv) REFERENCES tbl_sinh_vien(ma_sv) ON DELETE RESTRICT,
    FOREIGN KEY (ma_lhp) REFERENCES tbl_lop_hoc_phan(ma_lhp) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE tbl_diem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ma_sv VARCHAR(20) NOT NULL,
    ma_lhp VARCHAR(30) NOT NULL,
    diem_cc FLOAT CHECK (diem_cc >= 0.0 AND diem_cc <= 10.0),
    diem_kt FLOAT CHECK (diem_kt >= 0.0 AND diem_kt <= 10.0),
    diem_thi FLOAT CHECK (diem_thi >= 0.0 AND diem_thi <= 10.0),
    diem_tb FLOAT CHECK (diem_tb >= 0.0 AND diem_tb <= 10.0),
    diem_chu VARCHAR(5),
    diem_he4 FLOAT CHECK (diem_he4 >= 0.0 AND diem_he4 <= 4.0),
    ghi_chu VARCHAR(255),
    CONSTRAINT fk_diem_sv FOREIGN KEY (ma_sv) REFERENCES tbl_sinh_vien(ma_sv) ON DELETE RESTRICT,
    CONSTRAINT fk_diem_lhp FOREIGN KEY (ma_lhp) REFERENCES tbl_lop_hoc_phan(ma_lhp) ON DELETE RESTRICT,
    CONSTRAINT uq_sv_lhp UNIQUE (ma_sv, ma_lhp),
    CONSTRAINT fk_diem_dangky FOREIGN KEY (ma_sv,ma_lhp)
        REFERENCES tbl_dang_ky(ma_sv,ma_lhp) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Khong chua du lieu ca nhan gia lap hoac thong tin giang vien chua xac minh.
