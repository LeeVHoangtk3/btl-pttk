package com.qltc.controller;

import com.qltc.dao.*;
import com.qltc.model.*;
import java.sql.SQLException;
import java.util.*;
public class XemDiemController {
private final DiemDAO diemDAO = new DiemDAO();
    private final SinhVienDAO svDAO = new SinhVienDAO();
    private final HocKyDAO hocKyDAO = new HocKyDAO();
    public List<HocKy> layDanhSachHocKy() throws SQLException {
        return hocKyDAO.getAllHocKy();
    }
    public SinhVien layThongTinSinhVien(String maSV) throws SQLException {
        return svDAO.findByMa(maSV);
    }
    /** maSV lay tu phien sinh vien da dang nhap. */
    public List<Diem> layKetQuaHocTap(String maSV, String maHK) throws SQLException {
        return diemDAO.getDiemBySinhVienAndHocKy(maSV,maHK);
    }
    /** Chi tinh hoc phan du diem; diem F van nam trong mau so. */
    public float tinhGPA(List<Diem> ds) {
        float sum = 0; int credits = 0;
        for (Diem d : ds) if (d.getDiemHe4() != null) {
            int tc = d.getLopHocPhan().getMonHoc().getSoTinChi();
            sum += tc * d.getDiemHe4(); credits += tc;
        }
        return credits == 0 ? 0 : Math.round(sum / credits * 100) / 100f;
    }
    /** Gia dinh hoc lai: lay ket qua tot nhat cua moi ma mon. */
    private List<Diem> totNhat(List<Diem> ds) {
        Map<String,Diem> byMon = new HashMap<>();
        for (Diem d : ds) if (d.getDiemHe4() != null) {
            String key = d.getLopHocPhan().getMonHoc().getMaMH();
            Diem old = byMon.get(key);
            if (old == null || d.getDiemHe4() > old.getDiemHe4()) byMon.put(key,d);
        }
        return new ArrayList<>(byMon.values());
    }
    /** CPA tu du lieu toan khoa, khong tra ve hang so. */
    public float tinhCPA(String maSV) throws SQLException {
        return tinhGPA(totNhat(diemDAO.getDiemBySinhVienAndHocKy(maSV,null)));
    }
    /** Moi mon dat tinh mot lan, nguong dat gia dinh la 4/10. */
    public int tinhTinChiTichLuy(List<Diem> ds) {
        int out = 0;
        for (Diem d : totNhat(ds)) if (d.getDiemTB() >= 4)
            out += d.getLopHocPhan().getMonHoc().getSoTinChi();
        return out;
    }
}
