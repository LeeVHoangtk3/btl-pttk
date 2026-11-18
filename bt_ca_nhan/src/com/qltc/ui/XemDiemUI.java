package com.qltc.ui;

import com.qltc.controller.XemDiemController;
import com.qltc.model.Diem;
import java.util.List;
import java.sql.SQLException;
public class XemDiemUI {
private final XemDiemController controller = new XemDiemController();
    /** Boundary web: tra model cho JSP hien thi, maSV lay tu session. */
    public List<Diem> taiKetQua(String sv, String hk) throws SQLException {
        return controller.layKetQuaHocTap(sv,hk);
    }
    /** Tra CPA de hien thi cung bang diem hoc ky. */
    public float taiCPA(String sv) throws SQLException {
        return controller.tinhCPA(sv);
    }
}
