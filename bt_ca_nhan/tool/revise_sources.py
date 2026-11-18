"""Generate a consistent Java class framework and SQL schema for the assignment."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src/com/qltc'
META = {}

def write(package, name, fields, methods, body, imports=''):
    META[name] = dict(package=package, fields=fields, methods=methods)
    text = f'package com.qltc.{package};\n\n{imports}\npublic class {name} {{\n{body.strip()}\n}}\n'
    path = SRC / package / (name + '.java')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

models = {
 'NhanVien': [('String','maNV'),('String','hoTen'),('String','phongBan'),('String','chucVu'),('String','email'),('String','sdt')],
 'SinhVien': [('String','maSV'),('String','hoTen'),('java.sql.Date','ngaySinh'),('String','gioiTinh'),('String','lop'),('String','khoaHoc'),('String','nganh'),('String','email')],
 'MonHoc': [('String','maMH'),('String','tenMH'),('int','soTinChi'),('float','heSoCC'),('float','heSoKT'),('float','heSoThi')],
 'HocKy': [('String','maHocKy'),('String','tenHocKy'),('String','namHoc')],
 'LopHocPhan': [('String','maLHP'),('String','tenLHP'),('int','siSo'),('String','phongHoc'),('MonHoc','monHoc'),('HocKy','hocKy'),('NhanVien','giangVien')],
 'DangKy': [('String','maSV'),('String','maLHP'),('java.sql.Date','ngayDangKy')],
 'Diem': [('int','id'),('String','maSV'),('String','maLHP'),('Float','diemCC'),('Float','diemKT'),('Float','diemThi'),('Float','diemTB'),('String','diemChu'),('Float','diemHe4'),('String','ghiChu'),('SinhVien','sinhVien'),('LopHocPhan','lopHocPhan')]
}
extras = {
'MonHoc': '''
    /** Kiem tra tin chi va ba trong so khong am, co tong bang 1. */
    public boolean kiemTraHopLe() {
        return soTinChi > 0 && Float.isFinite(heSoCC)
            && Float.isFinite(heSoKT) && Float.isFinite(heSoThi)
            && heSoCC >= 0 && heSoKT >= 0 && heSoThi >= 0
            && Math.abs(heSoCC + heSoKT + heSoThi - 1) < 0.0001f;
    }
''',
'Diem': '''
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
'''
}
for name, fields in models.items():
    body = '\n'.join(f'    private {t} {n};' for t,n in fields) + '\n'
    body += '    /** Getter doc du lieu; setter gan du lieu khi anh xa JDBC. */\n'
    for t,n in fields:
        cap = n[0].upper() + n[1:]
        body += f'    public {t} get{cap}() {{ return {n}; }}\n'
        body += f'    public void set{cap}({t} x) {{ {n} = x; }}\n'
    body += extras.get(name,'')
    methods = ['+ get/set các thuộc tính']
    if name in extras: methods += ['+ kiemTraHopLe(): boolean']
    if name == 'Diem': methods += ['+ tinhDiemTB(): void', '+ quyDoiDiemChuVaHe4(): void']
    write('model',name,[f'- {n}: {t}' for t,n in fields],methods,body)

write('util','DatabaseConnection',[],['+ open(): Connection'],'''
    private DatabaseConnection() { }
    /** Mo ket noi rieng cho tung thao tac; caller phai dong ket noi. */
    public static Connection open() throws SQLException {
        String url = System.getenv("QLTC_DB_URL");
        if (url == null) url = "jdbc:mysql://localhost:3306/qltc_db";
        return DriverManager.getConnection(url,
            System.getenv("QLTC_DB_USER"), System.getenv("QLTC_DB_PASSWORD"));
    }
''','import java.sql.*;')
# Remove the duplicate, shared-connection implementation.
duplicate = SRC / 'dao/DatabaseConnection.java'
if duplicate.exists(): duplicate.unlink()

DAO_IMPORTS = '''import com.qltc.model.*;
import com.qltc.util.DatabaseConnection;
import java.sql.*;
import java.util.*;'''
write('dao','HocKyDAO',[],['+ getAllHocKy(): List<HocKy>'],'''
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
''',DAO_IMPORTS)
write('dao','SinhVienDAO',[],['+ findByMa(maSV): SinhVien'],'''
    /** Tim ho so; null neu ma sinh vien khong ton tai. */
    public SinhVien findByMa(String maSV) throws SQLException {
        try (Connection c = DatabaseConnection.open();
             PreparedStatement p = c.prepareStatement(
                 "SELECT * FROM tbl_sinh_vien WHERE ma_sv=?")) {
            p.setString(1, maSV);
            try (ResultSet r = p.executeQuery()) {
                if (!r.next()) return null;
                SinhVien s = new SinhVien();
                s.setMaSV(maSV); s.setHoTen(r.getString("ho_ten"));
                s.setNgaySinh(r.getDate("ngay_sinh"));
                s.setGioiTinh(r.getString("gioi_tinh"));
                s.setLop(r.getString("lop")); s.setKhoaHoc(r.getString("khoa_hoc"));
                s.setNganh(r.getString("nganh")); s.setEmail(r.getString("email"));
                return s;
            }
        }
    }
''',DAO_IMPORTS)
write('dao','LopHocPhanDAO',[],['+ findByNhanVien(maNV): List<LopHocPhan>', '+ findByMa(maLHP): LopHocPhan'],'''
    /** Tai day du mon hoc, trong so, hoc ky va ma giang vien. */
    private List<LopHocPhan> query(String where, String value) throws SQLException {
        List<LopHocPhan> out = new ArrayList<>();
        String sql = "SELECT l.*,m.ten_mh,m.so_tin_chi,m.he_so_cc,"
            + "m.he_so_kt,m.he_so_thi,h.ten_hoc_ky,h.nam_hoc "
            + "FROM tbl_lop_hoc_phan l JOIN tbl_mon_hoc m ON l.ma_mh=m.ma_mh "
            + "JOIN tbl_hoc_ky h ON l.ma_hoc_ky=h.ma_hoc_ky WHERE " + where;
        try (Connection c = DatabaseConnection.open();
             PreparedStatement p = c.prepareStatement(sql)) {
            p.setString(1, value);
            try (ResultSet r = p.executeQuery()) {
                while (r.next()) {
                    LopHocPhan l = new LopHocPhan(); MonHoc m = new MonHoc();
                    l.setMaLHP(r.getString("ma_lhp")); l.setTenLHP(r.getString("ten_lhp"));
                    l.setSiSo(r.getInt("si_so")); l.setPhongHoc(r.getString("phong_hoc"));
                    m.setMaMH(r.getString("ma_mh")); m.setTenMH(r.getString("ten_mh"));
                    m.setSoTinChi(r.getInt("so_tin_chi"));
                    m.setHeSoCC(r.getFloat("he_so_cc")); m.setHeSoKT(r.getFloat("he_so_kt"));
                    m.setHeSoThi(r.getFloat("he_so_thi")); l.setMonHoc(m);
                    HocKy h = new HocKy(); h.setMaHocKy(r.getString("ma_hoc_ky"));
                    h.setTenHocKy(r.getString("ten_hoc_ky")); h.setNamHoc(r.getString("nam_hoc"));
                    l.setHocKy(h); NhanVien n = new NhanVien();
                    n.setMaNV(r.getString("ma_nv")); l.setGiangVien(n); out.add(l);
                }
            }
        }
        return out;
    }
    /** Loc cac lop duoc phan cong cho nhan vien. */
    public List<LopHocPhan> findByNhanVien(String maNV) throws SQLException {
        return query("l.ma_nv=?", maNV);
    }
    /** Tra ve lop duoc chon, hoac null neu khong ton tai. */
    public LopHocPhan findByMa(String maLHP) throws SQLException {
        List<LopHocPhan> ds = query("l.ma_lhp=?", maLHP);
        return ds.isEmpty() ? null : ds.get(0);
    }
''',DAO_IMPORTS)
write('dao','DiemDAO',[],['+ getDiemByLHP(maLHP): List<Diem>', '+ getDiemBySinhVienAndHocKy(sv,hk): List<Diem>', '+ saveBangDiem(ds): boolean'],'''
    /** LEFT JOIN tu dang ky de lay ca sinh vien chua co diem. */
    public List<Diem> getDiemByLHP(String maLHP) throws SQLException {
        String sql = "SELECT k.ma_sv,k.ma_lhp,d.*,s.ho_ten,s.lop "
            + "FROM tbl_dang_ky k JOIN tbl_sinh_vien s ON k.ma_sv=s.ma_sv "
            + "LEFT JOIN tbl_diem d ON k.ma_sv=d.ma_sv AND k.ma_lhp=d.ma_lhp "
            + "WHERE k.ma_lhp=? ORDER BY k.ma_sv";
        List<Diem> out = new ArrayList<>();
        LopHocPhan l = new LopHocPhanDAO().findByMa(maLHP);
        try (Connection c = DatabaseConnection.open();
             PreparedStatement p = c.prepareStatement(sql)) {
            p.setString(1, maLHP);
            try (ResultSet r = p.executeQuery()) {
                while (r.next()) {
                    Diem d = map(r); d.setMaSV(r.getString(1)); d.setMaLHP(maLHP);
                    SinhVien s = new SinhVien(); s.setMaSV(d.getMaSV());
                    s.setHoTen(r.getString("ho_ten")); s.setLop(r.getString("lop"));
                    d.setSinhVien(s); d.setLopHocPhan(l); out.add(d);
                }
            }
        }
        return out;
    }
    /** maHK null la toan khoa; doc ca trong so de tinh lai nhat quan. */
    public List<Diem> getDiemBySinhVienAndHocKy(String maSV, String maHK)
            throws SQLException {
        String sql = "SELECT d.*,m.ma_mh,m.ten_mh,m.so_tin_chi,"
            + "m.he_so_cc,m.he_so_kt,m.he_so_thi FROM tbl_diem d "
            + "JOIN tbl_lop_hoc_phan l ON d.ma_lhp=l.ma_lhp "
            + "JOIN tbl_mon_hoc m ON l.ma_mh=m.ma_mh "
            + "WHERE d.ma_sv=? AND (? IS NULL OR l.ma_hoc_ky=?)";
        List<Diem> out = new ArrayList<>();
        try (Connection c = DatabaseConnection.open();
             PreparedStatement p = c.prepareStatement(sql)) {
            p.setString(1, maSV); p.setString(2, maHK); p.setString(3, maHK);
            try (ResultSet r = p.executeQuery()) {
                while (r.next()) {
                    Diem d = map(r); MonHoc m = new MonHoc();
                    m.setMaMH(r.getString("ma_mh")); m.setTenMH(r.getString("ten_mh"));
                    m.setSoTinChi(r.getInt("so_tin_chi"));
                    m.setHeSoCC(r.getFloat("he_so_cc")); m.setHeSoKT(r.getFloat("he_so_kt"));
                    m.setHeSoThi(r.getFloat("he_so_thi")); LopHocPhan l = new LopHocPhan();
                    l.setMaLHP(d.getMaLHP()); l.setMonHoc(m); d.setLopHocPhan(l);
                    d.tinhDiemTB(); out.add(d);
                }
            }
        }
        return out;
    }
    private Float number(ResultSet r, String name) throws SQLException {
        Number x = (Number) r.getObject(name); return x == null ? null : x.floatValue();
    }
    private Diem map(ResultSet r) throws SQLException {
        Diem d = new Diem(); d.setId(r.getInt("id"));
        d.setMaSV(r.getString("ma_sv")); d.setMaLHP(r.getString("ma_lhp"));
        d.setDiemCC(number(r,"diem_cc")); d.setDiemKT(number(r,"diem_kt"));
        d.setDiemThi(number(r,"diem_thi")); d.setDiemTB(number(r,"diem_tb"));
        d.setDiemChu(r.getString("diem_chu")); d.setDiemHe4(number(r,"diem_he4"));
        d.setGhiChu(r.getString("ghi_chu")); return d;
    }
    /** Transaction rieng: commit ca bang hoac rollback, luon khoi phuc autoCommit. */
    public boolean saveBangDiem(List<Diem> ds) throws SQLException {
        if (ds == null || ds.isEmpty()) return false;
        String sql = "INSERT INTO tbl_diem (ma_sv,ma_lhp,diem_cc,diem_kt,"
            + "diem_thi,diem_tb,diem_chu,diem_he4,ghi_chu) VALUES (?,?,?,?,?,?,?,?,?) "
            + "ON DUPLICATE KEY UPDATE diem_cc=?,diem_kt=?,diem_thi=?,"
            + "diem_tb=?,diem_chu=?,diem_he4=?,ghi_chu=?";
        try (Connection c = DatabaseConnection.open()) {
            boolean old = c.getAutoCommit(); c.setAutoCommit(false);
            try (PreparedStatement p = c.prepareStatement(sql)) {
                for (Diem d : ds) {
                    d.tinhDiemTB(); p.setString(1,d.getMaSV()); p.setString(2,d.getMaLHP());
                    Object[] v = {d.getDiemCC(),d.getDiemKT(),d.getDiemThi(),
                        d.getDiemTB(),d.getDiemChu(),d.getDiemHe4(),d.getGhiChu()};
                    int[] types = {Types.FLOAT,Types.FLOAT,Types.FLOAT,Types.FLOAT,
                        Types.VARCHAR,Types.FLOAT,Types.VARCHAR};
                    for (int i=0; i<v.length; i++) {
                        p.setObject(i+3,v[i],types[i]); p.setObject(i+10,v[i],types[i]);
                    }
                    p.addBatch();
                }
                p.executeBatch(); c.commit(); return true;
            } catch (SQLException | RuntimeException e) {
                try { c.rollback(); } catch (SQLException x) { e.addSuppressed(x); }
                throw e;
            } finally { c.setAutoCommit(old); }
        }
    }
''',DAO_IMPORTS)

CTRL_IMPORTS = 'import com.qltc.dao.*;\nimport com.qltc.model.*;\nimport java.sql.SQLException;\nimport java.util.*;'
write('controller','NhapDiemController',['- diemDAO: DiemDAO','- lopDAO: LopHocPhanDAO'],[
'+ layDSLHPTheoNV(maNV): List<LopHocPhan>', '+ layBangDiemLHP(nv,lhp): List<Diem>', '+ luuBangDiem(nv,lhp,ds): boolean'],'''
    private final DiemDAO diemDAO = new DiemDAO();
    private final LopHocPhanDAO lopDAO = new LopHocPhanDAO();
    /** maNV lay tu phien dang nhap da xac thuc, khong lay tu form. */
    private LopHocPhan check(String maNV, String maLHP) throws SQLException {
        LopHocPhan l = lopDAO.findByMa(maLHP);
        if (l == null || maNV == null || !maNV.equals(l.getGiangVien().getMaNV()))
            throw new SecurityException("Khong duoc phan cong lop");
        return l;
    }
    public List<LopHocPhan> layDSLHPTheoNV(String maNV) throws SQLException {
        return lopDAO.findByNhanVien(maNV);
    }
    public List<Diem> layBangDiemLHP(String maNV, String maLHP) throws SQLException {
        check(maNV, maLHP); return diemDAO.getDiemByLHP(maLHP);
    }
    /** Nap lai lop tu CSDL de khong tin trong so do client gui len. */
    public boolean luuBangDiem(String maNV, String maLHP, List<Diem> ds)
            throws SQLException {
        LopHocPhan l = check(maNV,maLHP);
        if (ds == null || ds.isEmpty()) return false;
        Set<String> ids = new HashSet<>();
        for (Diem d : ds) {
            if (d == null || !maLHP.equals(d.getMaLHP()) || !ids.add(d.getMaSV()))
                throw new IllegalArgumentException("Sai lop hoac trung sinh vien");
            d.setLopHocPhan(l); d.tinhDiemTB();
        }
        return diemDAO.saveBangDiem(ds);
    }
''',CTRL_IMPORTS)
write('controller','XemDiemController',['- diemDAO: DiemDAO','- svDAO: SinhVienDAO','- hocKyDAO: HocKyDAO'],[
'+ layDanhSachHocKy(): List<HocKy>', '+ layThongTinSinhVien(sv): SinhVien', '+ layKetQuaHocTap(sv,hk): List<Diem>', '+ tinhGPA(ds): float', '+ tinhCPA(sv): float', '+ tinhTinChiTichLuy(ds): int'],'''
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
''',CTRL_IMPORTS)
write('ui','NhapDiemUI',['- controller: NhapDiemController'],[
'+ taiDanhSach(nv,lhp): List<Diem>', '+ guiBangDiem(nv,lhp,ds): boolean'],'''
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
''','import com.qltc.controller.NhapDiemController;\nimport com.qltc.model.Diem;\nimport java.util.List;\nimport java.sql.SQLException;')
write('ui','XemDiemUI',['- controller: XemDiemController'],[
'+ taiKetQua(sv,hk): List<Diem>', '+ taiCPA(sv): float'],'''
    private final XemDiemController controller = new XemDiemController();
    /** Boundary web: tra model cho JSP hien thi, maSV lay tu session. */
    public List<Diem> taiKetQua(String sv, String hk) throws SQLException {
        return controller.layKetQuaHocTap(sv,hk);
    }
    /** Tra CPA de hien thi cung bang diem hoc ky. */
    public float taiCPA(String sv) throws SQLException {
        return controller.tinhCPA(sv);
    }
''','import com.qltc.controller.XemDiemController;\nimport com.qltc.model.Diem;\nimport java.util.List;\nimport java.sql.SQLException;')

# Keep original schema field names, remove destructive reset and unsafe cascade.
sql = (ROOT / 'qltc_database.sql').read_text(encoding='utf-8')
marker='-- =============================================================================\n-- DỮ LIỆU'
if marker in sql:sql = sql[:sql.index(marker)]
sql = sql.replace('DROP DATABASE IF EXISTS qltc_db;\n','')
sql = sql.replace('CREATE DATABASE qltc_db','CREATE DATABASE IF NOT EXISTS qltc_db')
sql = sql.replace('ON DELETE CASCADE','ON DELETE RESTRICT')
if 'ck_trong_so' not in sql:sql = sql.replace('he_so_thi FLOAT NOT NULL DEFAULT 0.70', '''he_so_thi FLOAT NOT NULL DEFAULT 0.70,
    CONSTRAINT ck_trong_so CHECK (he_so_cc >= 0 AND he_so_kt >= 0 AND he_so_thi >= 0
        AND ABS(he_so_cc + he_so_kt + he_so_thi - 1) < 0.0001)''')
insert = '''-- Dang ky ton tai truoc khi co diem.
CREATE TABLE tbl_dang_ky (
    ma_sv VARCHAR(20) NOT NULL,
    ma_lhp VARCHAR(30) NOT NULL,
    ngay_dang_ky DATE NOT NULL,
    PRIMARY KEY (ma_sv,ma_lhp),
    FOREIGN KEY (ma_sv) REFERENCES tbl_sinh_vien(ma_sv) ON DELETE RESTRICT,
    FOREIGN KEY (ma_lhp) REFERENCES tbl_lop_hoc_phan(ma_lhp) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

'''
if 'CREATE TABLE tbl_dang_ky' not in sql:sql = sql.replace('CREATE TABLE tbl_diem (',insert+'CREATE TABLE tbl_diem (')
if 'fk_diem_dangky' not in sql:sql = sql.replace('CONSTRAINT uq_sv_lhp UNIQUE (ma_sv, ma_lhp)', '''CONSTRAINT uq_sv_lhp UNIQUE (ma_sv, ma_lhp),
    CONSTRAINT fk_diem_dangky FOREIGN KEY (ma_sv,ma_lhp)
        REFERENCES tbl_dang_ky(ma_sv,ma_lhp) ON DELETE RESTRICT''')
if '-- Khong chua du lieu' not in sql:sql += '\n-- Khong chua du lieu ca nhan gia lap hoac thong tin giang vien chua xac minh.\n'
(ROOT / 'qltc_database.sql').write_text(sql,encoding='utf-8')
(ROOT / 'tool/revision_manifest.json').write_text(json.dumps(META,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Generated {len(META)} Java classes and seven SQL tables')
