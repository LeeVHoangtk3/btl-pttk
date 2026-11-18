package com.qltc.dao;

import com.qltc.model.*;
import com.qltc.util.DatabaseConnection;
import java.sql.*;
import java.util.*;
public class LopHocPhanDAO {
/** Tai day du mon hoc, trong so, hoc ky va ma giang vien. */
    private List<LopHocPhan> query(String where, String value) throws SQLException {
        List<LopHocPhan> out = new ArrayList<>();
        String sql = "SELECT l.*,m.ten_mh,m.so_tin_chi,m.he_so_cc,"
            + "m.he_so_kt,m.he_so_thi,h.ten_hoc_ky,h.nam_hoc "
            + "FROM tbl_lop_hoc_phan l JOIN tbl_mon_hoc m ON l.ma_mh=m.ma_mh "
            + "JOIN tbl_hoc_ky h ON l.ma_hoc_ky=h.ma_hoc_ky WHERE " + where;
        try (Connection c = DatabaseConnection.open();
             PreparedStatement p = c.prepareStatement(sql)) {
            p.setString(1, value);
            try (ResultSet r = p.executeQuery()) {
                while (r.next()) {
                    LopHocPhan l = new LopHocPhan(); MonHoc m = new MonHoc();
                    l.setMaLHP(r.getString("ma_lhp")); l.setTenLHP(r.getString("ten_lhp"));
                    l.setSiSo(r.getInt("si_so")); l.setPhongHoc(r.getString("phong_hoc"));
                    m.setMaMH(r.getString("ma_mh")); m.setTenMH(r.getString("ten_mh"));
                    m.setSoTinChi(r.getInt("so_tin_chi"));
                    m.setHeSoCC(r.getFloat("he_so_cc")); m.setHeSoKT(r.getFloat("he_so_kt"));
                    m.setHeSoThi(r.getFloat("he_so_thi")); l.setMonHoc(m);
                    HocKy h = new HocKy(); h.setMaHocKy(r.getString("ma_hoc_ky"));
                    h.setTenHocKy(r.getString("ten_hoc_ky")); h.setNamHoc(r.getString("nam_hoc"));
                    l.setHocKy(h); NhanVien n = new NhanVien();
                    n.setMaNV(r.getString("ma_nv")); l.setGiangVien(n); out.add(l);
                }
            }
        }
        return out;
    }
    /** Loc cac lop duoc phan cong cho nhan vien. */
    public List<LopHocPhan> findByNhanVien(String maNV) throws SQLException {
        return query("l.ma_nv=?", maNV);
    }
    /** Tra ve lop duoc chon, hoac null neu khong ton tai. */
    public LopHocPhan findByMa(String maLHP) throws SQLException {
        List<LopHocPhan> ds = query("l.ma_lhp=?", maLHP);
        return ds.isEmpty() ? null : ds.get(0);
    }
}
