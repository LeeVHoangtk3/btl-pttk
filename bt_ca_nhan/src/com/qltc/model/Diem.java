package com.qltc.model;


public class Diem {
private int id;
    private String maSV;
    private String maLHP;
    private Float diemCC;
    private Float diemKT;
    private Float diemThi;
    private Float diemTB;
    private String diemChu;
    private Float diemHe4;
    private String ghiChu;
    private SinhVien sinhVien;
    private LopHocPhan lopHocPhan;
    /** Getter doc du lieu; setter gan du lieu khi anh xa JDBC. */
    public int getId() { return id; }
    public void setId(int x) { id = x; }
    public String getMaSV() { return maSV; }
    public void setMaSV(String x) { maSV = x; }
    public String getMaLHP() { return maLHP; }
    public void setMaLHP(String x) { maLHP = x; }
    public Float getDiemCC() { return diemCC; }
    public void setDiemCC(Float x) { diemCC = x; }
    public Float getDiemKT() { return diemKT; }
    public void setDiemKT(Float x) { diemKT = x; }
    public Float getDiemThi() { return diemThi; }
    public void setDiemThi(Float x) { diemThi = x; }
    public Float getDiemTB() { return diemTB; }
    public void setDiemTB(Float x) { diemTB = x; }
    public String getDiemChu() { return diemChu; }
    public void setDiemChu(String x) { diemChu = x; }
    public Float getDiemHe4() { return diemHe4; }
    public void setDiemHe4(Float x) { diemHe4 = x; }
    public String getGhiChu() { return ghiChu; }
    public void setGhiChu(String x) { ghiChu = x; }
    public SinhVien getSinhVien() { return sinhVien; }
    public void setSinhVien(SinhVien x) { sinhVien = x; }
    public LopHocPhan getLopHocPhan() { return lopHocPhan; }
    public void setLopHocPhan(LopHocPhan x) { lopHocPhan = x; }

    /** Cho phep diem thanh phan chua nhap; tu choi NaN va vo cuc. */
    public boolean kiemTraHopLe() {
        for (Float x : new Float[]{diemCC, diemKT, diemThi})
            if (x != null && (!Float.isFinite(x) || x < 0 || x > 10))
                return false;
        return true;
    }
    /** Tinh bang trong so cua MonHoc; thieu diem thi chua co ket qua. */
    public void tinhDiemTB() {
        diemTB = null; diemChu = null; diemHe4 = null;
        if (!kiemTraHopLe()) throw new IllegalArgumentException("Diem 0..10");
        if (diemCC == null || diemKT == null || diemThi == null) return;
        MonHoc m = lopHocPhan == null ? null : lopHocPhan.getMonHoc();
        if (m == null || !m.kiemTraHopLe())
            throw new IllegalArgumentException("Thieu trong so hop le");
        diemTB = Math.round((diemCC * m.getHeSoCC()
            + diemKT * m.getHeSoKT() + diemThi * m.getHeSoThi()) * 10) / 10f;
        quyDoiDiemChuVaHe4();
    }
    /** Bang quy doi gia dinh cua bai tap, khong gan voi quy che PTIT. */
    public void quyDoiDiemChuVaHe4() {
        if (diemTB == null) { diemChu = null; diemHe4 = null; return; }
        float[] nguong = {8.5f, 8, 7, 6.5f, 5.5f, 5, 4, 0};
        String[] chu = {"A", "B+", "B", "C+", "C", "D+", "D", "F"};
        float[] he4 = {4, 3.5f, 3, 2.5f, 2, 1.5f, 1, 0};
        for (int i = 0; i < nguong.length; i++)
            if (diemTB >= nguong[i]) {
                diemChu = chu[i]; diemHe4 = he4[i]; return;
            }
    }
}
