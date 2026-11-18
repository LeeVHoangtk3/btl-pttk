import com.qltc.model.*;
import com.qltc.controller.XemDiemController;
import com.qltc.dao.DiemDAO;
import java.sql.*;
import java.util.*;
import java.lang.reflect.*;

/** Small executable checks for grade rules and transaction failure paths. */
public class Verification {
    static boolean fail, committed, rolled, restored, closed;
    static int checks;
    static void check(boolean ok, String what) {
        checks++; if (!ok) throw new AssertionError(what);
    }
    static Object zero(Class<?> type) {
        if (type == boolean.class) return false;
        if (type == int.class) return 0;
        if (type == long.class) return 0L;
        return null;
    }
    static Object proxy(Class<?> type, InvocationHandler handler) {
        return Proxy.newProxyInstance(type.getClassLoader(), new Class[]{type}, handler);
    }
    static List<Map<String,Object>> rows = new ArrayList<>();
    static Map<String,Object> row(String code,int credits,float score) {
        Map<String,Object> r=new HashMap<>();
        r.put("id",1);r.put("ma_sv","S1");r.put("ma_lhp","L1");
        r.put("diem_cc",score);r.put("diem_kt",score);r.put("diem_thi",score);
        r.put("ma_mh",code);r.put("ten_mh",code);r.put("so_tin_chi",credits);
        r.put("he_so_cc",.2f);r.put("he_so_kt",.3f);r.put("he_so_thi",.5f);
        return r;
    }
    static ResultSet result() {
        int[] cursor={-1};
        return (ResultSet)proxy(ResultSet.class,(o,m,v)->{
            String name=m.getName();
            if(name.equals("next"))return ++cursor[0]<rows.size();
            if(name.startsWith("get")) {
                Object value=rows.get(cursor[0]).get(v[0]);
                if(name.equals("getInt"))return value==null?0:((Number)value).intValue();
                if(name.equals("getFloat"))return value==null?0f:((Number)value).floatValue();
                return value;
            }
            return zero(m.getReturnType());
        });
    }
    static Diem grade(String code, int credits, float value) {
        MonHoc m = new MonHoc(); m.setMaMH(code); m.setSoTinChi(credits);
        m.setHeSoCC(.2f); m.setHeSoKT(.3f); m.setHeSoThi(.5f);
        LopHocPhan l = new LopHocPhan(); l.setMonHoc(m); l.setMaLHP("L1");
        Diem d = new Diem(); d.setLopHocPhan(l); d.setMaSV("S1"); d.setMaLHP("L1");
        d.setDiemCC(value); d.setDiemKT(value); d.setDiemThi(value); d.tinhDiemTB();
        return d;
    }
    public static void main(String[] args) throws Exception {
        Diem a = grade("A",3,8.5f), b = grade("B",2,5.5f);
        check(a.getDiemHe4()==4f && b.getDiemHe4()==2f,"conversion thresholds");
        a.setDiemCC(10f); a.setDiemKT(5f); a.setDiemThi(8f); a.tinhDiemTB();
        check(a.getDiemTB()==7.5f,"subject weights instead of fixed 10/20/70");
        a.setDiemCC(null); a.tinhDiemTB();
        check(a.getDiemTB()==null && a.getDiemHe4()==null,"clear stale totals");
        a.setDiemCC(Float.NaN); check(!a.kiemTraHopLe(),"reject NaN");
        a.setDiemCC(Float.POSITIVE_INFINITY);check(!a.kiemTraHopLe(),"reject infinity");
        a.setDiemCC(-1f);check(!a.kiemTraHopLe(),"reject negative");
        a=grade("A",3,8.5f);
        XemDiemController c=new XemDiemController();
        check(c.tinhGPA(Arrays.asList(a,b))==3.2f,"weighted GPA");
        check(c.tinhGPA(Collections.emptyList())==0f,"empty GPA");
        check(c.tinhTinChiTichLuy(Arrays.asList(a,b,grade("A",3,5f),grade("F",4,2f)))==5,
            "repeat and failed course credit policy");
        DriverManager.registerDriver(new Driver() {
            public boolean acceptsURL(String u) {return u.startsWith("jdbc:mysql:");}
            public Connection connect(String u,Properties p) {
                return (Connection)proxy(Connection.class,(o,m,v)->{
                    switch(m.getName()) {
                    case "getAutoCommit": return true;
                    case "setAutoCommit": if ((boolean)v[0]) restored=true; return null;
                    case "commit":committed=true;return null;
                    case "rollback":rolled=true;return null;
                    case "close":closed=true;return null;
                    case "prepareStatement":return proxy(PreparedStatement.class,(o2,m2,v2)->{
                        if(m2.getName().equals("executeQuery"))return result();
                        if(m2.getName().equals("executeBatch")) {
                            if(fail)throw new SQLException("injected batch failure");
                            return new int[]{1};
                        }
                        return zero(m2.getReturnType());
                    });
                    default:return zero(m.getReturnType());
                    }
                });
            }
            public int getMajorVersion(){return 1;}
            public int getMinorVersion(){return 0;}
            public boolean jdbcCompliant(){return false;}
            public DriverPropertyInfo[] getPropertyInfo(String u,Properties p){return new DriverPropertyInfo[0];}
            public java.util.logging.Logger getParentLogger(){return java.util.logging.Logger.getGlobal();}
        });
        rows=Arrays.asList(row("A",3,8.5f),row("B",2,5.5f),row("A",3,5f));
        check(c.tinhCPA("S1")==3.2f,"CPA queries all terms and selects best repeated course");
        rows=Arrays.asList(row("F",4,2f),row("B",2,5.5f));
        check(c.tinhCPA("S1")==.67f,"CPA includes failed course in denominator");
        DiemDAO dao=new DiemDAO();
        committed=rolled=restored=closed=false;
        check(dao.saveBangDiem(Arrays.asList(a)),"batch save result");
        check(committed && !rolled && restored && closed,"success cleanup");
        fail=true;committed=rolled=restored=closed=false;
        try {dao.saveBangDiem(Arrays.asList(a));throw new AssertionError("expected SQL error");}
        catch(SQLException expected){}
        check(!committed && rolled && restored && closed,"rollback and cleanup after SQL failure");
        fail=false;committed=rolled=restored=closed=false;a.setDiemThi(11f);
        try {dao.saveBangDiem(Arrays.asList(a));throw new AssertionError("expected validation error");}
        catch(IllegalArgumentException expected){}
        check(!committed && rolled && restored && closed,"rollback after validation failure");
        System.out.println("PASS "+checks+" checks; JDBC uses a test double, not a live MySQL server");
    }
}
