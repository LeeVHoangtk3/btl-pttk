package com.qltc.ui;

import com.qltc.controller.NhapDiemController;
import com.qltc.model.Diem;
import java.util.List;
import java.sql.SQLException;
public class NhapDiemUI {
private final NhapDiemController controller = new NhapDiemController();
    /** Boundary web: JSP goi de tao model bang HTML; nv lay tu session. */
    public List<Diem> taiDanhSach(String nv, String lhp) throws SQLException {
        return controller.layBangDiemLHP(nv,lhp);
    }
    /** Nhan du lieu form da chuyen thanh Float; null la o trong. */
    public boolean guiBangDiem(String nv, String lhp, List<Diem> ds)
            throws SQLException {
        return controller.luuBangDiem(nv,lhp,ds);
    }
}
