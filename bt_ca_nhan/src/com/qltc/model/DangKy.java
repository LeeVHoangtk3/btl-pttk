package com.qltc.model;


public class DangKy {
private String maSV;
    private String maLHP;
    private java.sql.Date ngayDangKy;
    /** Getter doc du lieu; setter gan du lieu khi anh xa JDBC. */
    public String getMaSV() { return maSV; }
    public void setMaSV(String x) { maSV = x; }
    public String getMaLHP() { return maLHP; }
    public void setMaLHP(String x) { maLHP = x; }
    public java.sql.Date getNgayDangKy() { return ngayDangKy; }
    public void setNgayDangKy(java.sql.Date x) { ngayDangKy = x; }
}
