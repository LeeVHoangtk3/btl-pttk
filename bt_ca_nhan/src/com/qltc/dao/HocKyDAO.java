package com.qltc.dao;

import com.qltc.model.*;
import com.qltc.util.DatabaseConnection;
import java.sql.*;
import java.util.*;
public class HocKyDAO {
/** Doc danh muc hoc ky; loi SQL duoc truyen ve tang goi. */
    public List<HocKy> getAllHocKy() throws SQLException {
        List<HocKy> out = new ArrayList<>();
        String sql = "SELECT * FROM tbl_hoc_ky ORDER BY nam_hoc DESC, ma_hoc_ky DESC";
        try (Connection c = DatabaseConnection.open();
             PreparedStatement p = c.prepareStatement(sql);
             ResultSet r = p.executeQuery()) {
            while (r.next()) {
                HocKy h = new HocKy();
                h.setMaHocKy(r.getString("ma_hoc_ky"));
                h.setTenHocKy(r.getString("ten_hoc_ky"));
                h.setNamHoc(r.getString("nam_hoc")); out.add(h);
            }
        }
        return out;
    }
}
