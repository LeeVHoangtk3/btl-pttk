package com.qltc.model;


public class LopHocPhan {
private String maLHP;
    private String tenLHP;
    private int siSo;
    private String phongHoc;
    private MonHoc monHoc;
    private HocKy hocKy;
    private NhanVien giangVien;
    /** Getter doc du lieu; setter gan du lieu khi anh xa JDBC. */
    public String getMaLHP() { return maLHP; }
    public void setMaLHP(String x) { maLHP = x; }
    public String getTenLHP() { return tenLHP; }
    public void setTenLHP(String x) { tenLHP = x; }
    public int getSiSo() { return siSo; }
    public void setSiSo(int x) { siSo = x; }
    public String getPhongHoc() { return phongHoc; }
    public void setPhongHoc(String x) { phongHoc = x; }
    public MonHoc getMonHoc() { return monHoc; }
    public void setMonHoc(MonHoc x) { monHoc = x; }
    public HocKy getHocKy() { return hocKy; }
    public void setHocKy(HocKy x) { hocKy = x; }
    public NhanVien getGiangVien() { return giangVien; }
    public void setGiangVien(NhanVien x) { giangVien = x; }
}
