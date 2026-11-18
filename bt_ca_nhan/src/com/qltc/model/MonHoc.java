package com.qltc.model;


public class MonHoc {
private String maMH;
    private String tenMH;
    private int soTinChi;
    private float heSoCC;
    private float heSoKT;
    private float heSoThi;
    /** Getter doc du lieu; setter gan du lieu khi anh xa JDBC. */
    public String getMaMH() { return maMH; }
    public void setMaMH(String x) { maMH = x; }
    public String getTenMH() { return tenMH; }
    public void setTenMH(String x) { tenMH = x; }
    public int getSoTinChi() { return soTinChi; }
    public void setSoTinChi(int x) { soTinChi = x; }
    public float getHeSoCC() { return heSoCC; }
    public void setHeSoCC(float x) { heSoCC = x; }
    public float getHeSoKT() { return heSoKT; }
    public void setHeSoKT(float x) { heSoKT = x; }
    public float getHeSoThi() { return heSoThi; }
    public void setHeSoThi(float x) { heSoThi = x; }

    /** Kiem tra tin chi va ba trong so khong am, co tong bang 1. */
    public boolean kiemTraHopLe() {
        return soTinChi > 0 && Float.isFinite(heSoCC)
            && Float.isFinite(heSoKT) && Float.isFinite(heSoThi)
            && heSoCC >= 0 && heSoKT >= 0 && heSoThi >= 0
            && Math.abs(heSoCC + heSoKT + heSoThi - 1) < 0.0001f;
    }
}
