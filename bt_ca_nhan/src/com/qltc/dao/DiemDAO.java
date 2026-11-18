package com.qltc.dao;

import com.qltc.model.*;
import com.qltc.util.DatabaseConnection;
import java.sql.*;
import java.util.*;
public class DiemDAO {
/** LEFT JOIN tu dang ky de lay ca sinh vien chua co diem. */
    public List<Diem> getDiemByLHP(String maLHP) throws SQLException {
        String sql = "SELECT k.ma_sv,k.ma_lhp,d.*,s.ho_ten,s.lop "
            + "FROM tbl_dang_ky k JOIN tbl_sinh_vien s ON k.ma_sv=s.ma_sv "
            + "LEFT JOIN tbl_diem d ON k.ma_sv=d.ma_sv AND k.ma_lhp=d.ma_lhp "
            + "WHERE k.ma_lhp=? ORDER BY k.ma_sv";
        List<Diem> out = new ArrayList<>();
        LopHocPhan l = new LopHocPhanDAO().findByMa(maLHP);
        try (Connection c = DatabaseConnection.open();
             PreparedStatement p = c.prepareStatement(sql)) {
            p.setString(1, maLHP);
            try (ResultSet r = p.executeQuery()) {
                while (r.next()) {
                    Diem d = map(r); d.setMaSV(r.getString(1)); d.setMaLHP(maLHP);
                    SinhVien s = new SinhVien(); s.setMaSV(d.getMaSV());
                    s.setHoTen(r.getString("ho_ten")); s.setLop(r.getString("lop"));
                    d.setSinhVien(s); d.setLopHocPhan(l); out.add(d);
                }
            }
        }
        return out;
    }
    /** maHK null la toan khoa; doc ca trong so de tinh lai nhat quan. */
    public List<Diem> getDiemBySinhVienAndHocKy(String maSV, String maHK)
            throws SQLException {
        String sql = "SELECT d.*,m.ma_mh,m.ten_mh,m.so_tin_chi,"
            + "m.he_so_cc,m.he_so_kt,m.he_so_thi FROM tbl_diem d "
            + "JOIN tbl_lop_hoc_phan l ON d.ma_lhp=l.ma_lhp "
            + "JOIN tbl_mon_hoc m ON l.ma_mh=m.ma_mh "
            + "WHERE d.ma_sv=? AND (? IS NULL OR l.ma_hoc_ky=?)";
        List<Diem> out = new ArrayList<>();
        try (Connection c = DatabaseConnection.open();
             PreparedStatement p = c.prepareStatement(sql)) {
            p.setString(1, maSV); p.setString(2, maHK); p.setString(3, maHK);
            try (ResultSet r = p.executeQuery()) {
                while (r.next()) {
                    Diem d = map(r); MonHoc m = new MonHoc();
                    m.setMaMH(r.getString("ma_mh")); m.setTenMH(r.getString("ten_mh"));
                    m.setSoTinChi(r.getInt("so_tin_chi"));
                    m.setHeSoCC(r.getFloat("he_so_cc")); m.setHeSoKT(r.getFloat("he_so_kt"));
                    m.setHeSoThi(r.getFloat("he_so_thi")); LopHocPhan l = new LopHocPhan();
                    l.setMaLHP(d.getMaLHP()); l.setMonHoc(m); d.setLopHocPhan(l);
                    d.tinhDiemTB(); out.add(d);
                }
            }
        }
        return out;
    }
    private Float number(ResultSet r, String name) throws SQLException {
        Number x = (Number) r.getObject(name); return x == null ? null : x.floatValue();
    }
    private Diem map(ResultSet r) throws SQLException {
        Diem d = new Diem(); d.setId(r.getInt("id"));
        d.setMaSV(r.getString("ma_sv")); d.setMaLHP(r.getString("ma_lhp"));
        d.setDiemCC(number(r,"diem_cc")); d.setDiemKT(number(r,"diem_kt"));
        d.setDiemThi(number(r,"diem_thi")); d.setDiemTB(number(r,"diem_tb"));
        d.setDiemChu(r.getString("diem_chu")); d.setDiemHe4(number(r,"diem_he4"));
        d.setGhiChu(r.getString("ghi_chu")); return d;
    }
    /** Transaction rieng: commit ca bang hoac rollback, luon khoi phuc autoCommit. */
    public boolean saveBangDiem(List<Diem> ds) throws SQLException {
        if (ds == null || ds.isEmpty()) return false;
        String sql = "INSERT INTO tbl_diem (ma_sv,ma_lhp,diem_cc,diem_kt,"
            + "diem_thi,diem_tb,diem_chu,diem_he4,ghi_chu) VALUES (?,?,?,?,?,?,?,?,?) "
            + "ON DUPLICATE KEY UPDATE diem_cc=?,diem_kt=?,diem_thi=?,"
            + "diem_tb=?,diem_chu=?,diem_he4=?,ghi_chu=?";
        try (Connection c = DatabaseConnection.open()) {
            boolean old = c.getAutoCommit(); c.setAutoCommit(false);
            try (PreparedStatement p = c.prepareStatement(sql)) {
                for (Diem d : ds) {
                    d.tinhDiemTB(); p.setString(1,d.getMaSV()); p.setString(2,d.getMaLHP());
                    Object[] v = {d.getDiemCC(),d.getDiemKT(),d.getDiemThi(),
                        d.getDiemTB(),d.getDiemChu(),d.getDiemHe4(),d.getGhiChu()};
                    int[] types = {Types.FLOAT,Types.FLOAT,Types.FLOAT,Types.FLOAT,
                        Types.VARCHAR,Types.FLOAT,Types.VARCHAR};
                    for (int i=0; i<v.length; i++) {
                        p.setObject(i+3,v[i],types[i]); p.setObject(i+10,v[i],types[i]);
                    }
                    p.addBatch();
                }
                p.executeBatch(); c.commit(); return true;
            } catch (SQLException | RuntimeException e) {
                try { c.rollback(); } catch (SQLException x) { e.addSuppressed(x); }
                throw e;
            } finally { c.setAutoCommit(old); }
        }
    }
}
