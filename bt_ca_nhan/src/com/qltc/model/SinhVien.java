package com.qltc.model;


public class SinhVien {
private String maSV;
    private String hoTen;
    private java.sql.Date ngaySinh;
    private String gioiTinh;
    private String lop;
    private String khoaHoc;
    private String nganh;
    private String email;
    /** Getter doc du lieu; setter gan du lieu khi anh xa JDBC. */
    public String getMaSV() { return maSV; }
    public void setMaSV(String x) { maSV = x; }
    public String getHoTen() { return hoTen; }
    public void setHoTen(String x) { hoTen = x; }
    public java.sql.Date getNgaySinh() { return ngaySinh; }
    public void setNgaySinh(java.sql.Date x) { ngaySinh = x; }
    public String getGioiTinh() { return gioiTinh; }
    public void setGioiTinh(String x) { gioiTinh = x; }
    public String getLop() { return lop; }
    public void setLop(String x) { lop = x; }
    public String getKhoaHoc() { return khoaHoc; }
    public void setKhoaHoc(String x) { khoaHoc = x; }
    public String getNganh() { return nganh; }
    public void setNganh(String x) { nganh = x; }
    public String getEmail() { return email; }
    public void setEmail(String x) { email = x; }
}
