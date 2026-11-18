package com.qltc.dao;

import com.qltc.model.*;
import com.qltc.util.DatabaseConnection;
import java.sql.*;
import java.util.*;
public class SinhVienDAO {
/** Tim ho so; null neu ma sinh vien khong ton tai. */
    public SinhVien findByMa(String maSV) throws SQLException {
        try (Connection c = DatabaseConnection.open();
             PreparedStatement p = c.prepareStatement(
                 "SELECT * FROM tbl_sinh_vien WHERE ma_sv=?")) {
            p.setString(1, maSV);
            try (ResultSet r = p.executeQuery()) {
                if (!r.next()) return null;
                SinhVien s = new SinhVien();
                s.setMaSV(maSV); s.setHoTen(r.getString("ho_ten"));
                s.setNgaySinh(r.getDate("ngay_sinh"));
                s.setGioiTinh(r.getString("gioi_tinh"));
                s.setLop(r.getString("lop")); s.setKhoaHoc(r.getString("khoa_hoc"));
                s.setNganh(r.getString("nganh")); s.setEmail(r.getString("email"));
                return s;
            }
        }
    }
}
