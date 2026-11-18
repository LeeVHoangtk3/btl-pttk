package com.qltc.controller;

import com.qltc.dao.*;
import com.qltc.model.*;
import java.sql.SQLException;
import java.util.*;
public class NhapDiemController {
private final DiemDAO diemDAO = new DiemDAO();
    private final LopHocPhanDAO lopDAO = new LopHocPhanDAO();
    /** maNV lay tu phien dang nhap da xac thuc, khong lay tu form. */
    private LopHocPhan check(String maNV, String maLHP) throws SQLException {
        LopHocPhan l = lopDAO.findByMa(maLHP);
        if (l == null || maNV == null || !maNV.equals(l.getGiangVien().getMaNV()))
            throw new SecurityException("Khong duoc phan cong lop");
        return l;
    }
    public List<LopHocPhan> layDSLHPTheoNV(String maNV) throws SQLException {
        return lopDAO.findByNhanVien(maNV);
    }
    public List<Diem> layBangDiemLHP(String maNV, String maLHP) throws SQLException {
        check(maNV, maLHP); return diemDAO.getDiemByLHP(maLHP);
    }
    /** Nap lai lop tu CSDL de khong tin trong so do client gui len. */
    public boolean luuBangDiem(String maNV, String maLHP, List<Diem> ds)
            throws SQLException {
        LopHocPhan l = check(maNV,maLHP);
        if (ds == null || ds.isEmpty()) return false;
        Set<String> ids = new HashSet<>();
        for (Diem d : ds) {
            if (d == null || !maLHP.equals(d.getMaLHP()) || !ids.add(d.getMaSV()))
                throw new IllegalArgumentException("Sai lop hoac trung sinh vien");
            d.setLopHocPhan(l); d.tinhDiemTB();
        }
        return diemDAO.saveBangDiem(ds);
    }
}
