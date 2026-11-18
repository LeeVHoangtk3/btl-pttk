package com.qltc.model;


public class NhanVien {
private String maNV;
    private String hoTen;
    private String phongBan;
    private String chucVu;
    private String email;
    private String sdt;
    /** Getter doc du lieu; setter gan du lieu khi anh xa JDBC. */
    public String getMaNV() { return maNV; }
    public void setMaNV(String x) { maNV = x; }
    public String getHoTen() { return hoTen; }
    public void setHoTen(String x) { hoTen = x; }
    public String getPhongBan() { return phongBan; }
    public void setPhongBan(String x) { phongBan = x; }
    public String getChucVu() { return chucVu; }
    public void setChucVu(String x) { chucVu = x; }
    public String getEmail() { return email; }
    public void setEmail(String x) { email = x; }
    public String getSdt() { return sdt; }
    public void setSdt(String x) { sdt = x; }
}
