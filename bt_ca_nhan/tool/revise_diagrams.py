"""Draw monochrome UML diagrams without third party branding."""
from pathlib import Path
import math, json
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'diagrams'
OUT.mkdir(exist_ok=True)
META=json.loads((ROOT/'tool/revision_manifest.json').read_text(encoding='utf-8'))
FONT='C:/Windows/Fonts/arial.ttf'
BOLD='C:/Windows/Fonts/arialbd.ttf'

class Diagram:
    def __init__(self,w=1800,h=1500):
        self.im=Image.new('RGB',(w,h),'white'); self.d=ImageDraw.Draw(self.im)
    def text(self,x,y,text,size=30,bold=False,anchor=None):
        f=ImageFont.truetype(BOLD if bold else FONT,size)
        self.d.multiline_text((x,y),text,font=f,fill='black',spacing=9,anchor=anchor)
    def box(self,x,y,w,h,name,lines=(),stereo=None,size=29):
        self.d.rectangle((x,y,x+w,y+h),fill='white',outline='black',width=3)
        offset=15
        if stereo:
            self.text(x+w/2,y+offset,stereo,26,anchor='mt');offset+=38
        self.text(x+w/2,y+offset,name,31,True,'mt');offset+=48
        self.d.line((x,y+offset,x+w,y+offset),fill='black',width=2)
        for line in lines:
            actual=size
            while self.d.textlength(line,font=ImageFont.truetype(FONT,actual))>w-32 and actual>20:actual-=1
            self.text(x+16,y+offset+12,line,actual);offset+=size+12
        return (x,y,w,h)
    def line(self,pts,label=None,pos=None,dash=False,arrow=False):
        if dash:
            for a,b in zip(pts,pts[1:]):
                dist=math.dist(a,b); n=max(1,int(dist/15))
                for i in range(0,n,2):
                    p=tuple(a[j]+(b[j]-a[j])*i/n for j in range(2))
                    q=tuple(a[j]+(b[j]-a[j])*min(i+1,n)/n for j in range(2))
                    self.d.line((p,q),fill='black',width=3)
        else:self.d.line(pts,fill='black',width=3)
        if arrow:
            a,b=pts[-2:]; ang=math.atan2(b[1]-a[1],b[0]-a[0])
            self.d.line((b,(b[0]-20*math.cos(ang-.5),b[1]-20*math.sin(ang-.5))),fill='black',width=3)
            self.d.line((b,(b[0]-20*math.cos(ang+.5),b[1]-20*math.sin(ang+.5))),fill='black',width=3)
        if label and pos:
            f=ImageFont.truetype(FONT,27); bb=self.d.multiline_textbbox(pos,label,font=f,spacing=9)
            self.d.rectangle((bb[0]-5,bb[1]-4,bb[2]+5,bb[3]+4),fill='white')
            self.text(*pos,label,27)
    def actor(self,x,y,label):
        self.d.ellipse((x-25,y,x+25,y+50),outline='black',width=3)
        self.line([(x,y+50),(x,y+125)])
        self.line([(x-45,y+78),(x+45,y+78)])
        self.line([(x-40,y+170),(x,y+125),(x+40,y+170)])
        self.text(x,y+185,label,30,anchor='mt')
    def save(self,name): self.im.save(OUT/(name+'.png'),dpi=(260,260))

def usecase():
    g=Diagram(1800,1250)
    g.d.rectangle((390,70,1740,1150),outline='black',width=3)
    g.text(1065,95,'Hệ thống quản lý học tập theo tín chỉ',34,True,'mt')
    g.actor(170,290,'Nhân viên'); g.actor(170,820,'Sinh viên')
    def uc(box,label):
        g.d.ellipse(box,fill='white',outline='black',width=3)
        g.text((box[0]+box[2])/2,(box[1]+box[3])/2,label,32,anchor='mm')
    uc((510,270,1080,440),'Nhập điểm của sinh viên')
    uc((510,800,1120,980),'Xem thông tin về\nkết quả học tập')
    g.box(1230,490,420,200,'Tiền điều kiện',['Đã đăng nhập','Đúng vai trò'],size=29)
    g.line([(215,368),(510,355)])
    g.line([(215,898),(510,890)])
    # Authentication precedes the two use cases; no misleading include.
    g.line([(1075,355),(1420,355),(1420,490)],dash=True)
    g.line([(1118,890),(1420,890),(1420,690)],dash=True)
    g.text(450,1070,'Đăng nhập thành công là tiền điều kiện của hai ca sử dụng.',29)
    g.save('cau1a_usecase')

def entities(design=False):
    g=Diagram(1800,1900)
    positions={'NhanVien':(50,40,500,340),'MonHoc':(650,40,500,410),'HocKy':(1250,40,500,300),
    'LopHocPhan':(650,650,500,330),'SinhVien':(50,1180,500,440),
    'DangKy':(650,1180,500,300),'Diem':(1250,1180,500,600)}
    if design:
        for n,(x,y,w,h) in positions.items():
            fields=META[n]['fields']
            if n=='Diem':fields=fields[:10]
            if n=='LopHocPhan':fields=fields[:4]
            if n=='Diem':fields=fields+META[n]['methods'][1:]
            if n=='MonHoc':fields=fields+META[n]['methods'][1:]
            g.box(x,y,w,h,n,fields, '<<entity>>',size=26)
    else:
        fields={
        'NhanVien':['- maNV: String','- hoTen: String','+ getMaNV(): String'],
        'SinhVien':['- maSV: String','- hoTen: String','- lop: String','+ getMaSV(): String'],
        'MonHoc':['- maMH, tenMH: String','- soTinChi: int','- heSoCC, heSoKT, heSoThi: float','+ kiemTraHopLe(): boolean'],
        'HocKy':['- maHocKy: String','- tenHocKy, namHoc: String','+ getMaHocKy(): String'],
        'LopHocPhan':['- maLHP, tenLHP: String','- siSo: int','- phongHoc: String','+ getMaLHP(): String'],
        'DangKy':['- ngayDangKy: Date','+ getNgayDangKy(): Date'],
        'Diem':['- id: int','- diemCC, diemKT, diemThi: Float','- diemTB, diemHe4: Float','- diemChu: String',
                '+ kiemTraHopLe(): boolean','+ tinhDiemTB(): void','+ quyDoiDiemChuVaHe4(): void']}
        for n,(x,y,w,h) in positions.items(): g.box(x,y,w,h,n,fields[n],size=27)
    # All associations end on box boundaries. Routes occupy gutters only.
    g.line([(300,380),(300,540),(750,540),(750,650)],'phụ trách',(330,490))
    g.text(310,390,'1',27);g.text(755,605,'0..*',27)
    g.line([(900,450),(900,650)],'thuộc môn',(920,510));g.text(865,455,'1',27);g.text(830,600,'0..*',27)
    g.line([(1500,340),(1500,545),(1050,545),(1050,650)],'mở trong',(1210,490));g.text(1510,350,'1',27);g.text(1055,605,'0..*',27)
    g.line([(900,980),(900,1180)],'có đăng ký',(920,1030));g.text(860,985,'1',27);g.text(820,1130,'0..*',27)
    g.line([(1150,810),(1500,810),(1500,1180)],'có bảng điểm',(1210,760));g.text(1160,820,'1',27);g.text(1505,1130,'0..*',27)
    g.line([(550,1310),(650,1310)]);g.text(565,1265,'1',27);g.text(566,1325,'0..*',27)
    g.line([(300,1620),(300,1830),(1550,1830),(1550,1780)],'nhận kết quả',(740,1790));g.text(310,1625,'1',27);g.text(1560,1780,'0..*',27)
    g.line([(1150,1430),(1250,1430)]);g.text(1160,1380,'1',27);g.text(1160,1445,'0..1',27)
    if design:g.text(55,1860,'Các liên kết đối tượng được thể hiện bằng đường quan hệ; mã khóa và accessor xem Câu 4.b.',25)
    g.save('cau3a_entities' if design else 'cau2b_class_analysis')

def design():
    g=Diagram(1900,1920)
    g.box(60,30,800,260,'NhapDiemUI',META['NhapDiemUI']['fields']+META['NhapDiemUI']['methods'],'<<boundary web>>')
    g.box(1040,30,800,260,'XemDiemUI',META['XemDiemUI']['fields']+META['XemDiemUI']['methods'],'<<boundary web>>')
    g.line([(460,290),(460,440)],'gọi',(480,330),dash=True,arrow=True)
    g.line([(1440,290),(1440,440)],'gọi',(1460,330),dash=True,arrow=True)
    g.box(60,440,800,320,'NhapDiemController',META['NhapDiemController']['fields']+META['NhapDiemController']['methods'],'<<control>>',27)
    g.box(1040,440,800,520,'XemDiemController',META['XemDiemController']['fields']+META['XemDiemController']['methods'],'<<control>>',27)
    # Dependency routing above DAO row and around the outside of boxes.
    g.line([(250,760),(250,1120)],dash=True,arrow=True)
    g.line([(700,760),(700,1120)],dash=True,arrow=True)
    g.line([(1440,960),(1440,1000),(700,1000),(700,1120)],dash=True,arrow=True)
    g.line([(1540,960),(1540,1050),(1150,1050),(1150,1120)],dash=True,arrow=True)
    g.line([(1670,960),(1670,1120)],dash=True,arrow=True)
    g.box(30,1120,430,310,'LopHocPhanDAO',['+ findByNhanVien(maNV)', '  : List<LopHocPhan>','+ findByMa(maLHP)', '  : LopHocPhan'],'<<dao>>',26)
    g.box(500,1120,470,370,'DiemDAO',['+ getDiemByLHP(maLHP)', '  : List<Diem>','+ getDiemBySinhVienAndHocKy', '  (sv,hk): List<Diem>','+ saveBangDiem(ds): boolean'],'<<dao>>',26)
    g.box(1010,1120,400,260,'SinhVienDAO',['+ findByMa(maSV)', '  : SinhVien'],'<<dao>>',26)
    g.box(1450,1120,420,260,'HocKyDAO',['+ getAllHocKy()', '  : List<HocKy>'],'<<dao>>',26)
    for x,y in [(250,1430),(735,1490),(1210,1380),(1660,1380)]:
        g.line([(x,y),(x,1590)],dash=True)
    g.line([(250,1590),(1660,1590)])
    g.line([(950,1590),(950,1680)],dash=True,arrow=True)
    g.box(500,1680,900,190,'DatabaseConnection',['+ open(): Connection {static}'],'<<utility>>')
    g.text(60,1515,'DAO tạo và đọc các entity tại Hình 3.1b.',28)
    g.save('cau3a_class_design')

def communication(view=False):
    g=Diagram(1800,1800)
    actor='Sinh viên' if view else 'Nhân viên'
    ui=':XemDiemUI' if view else ':NhapDiemUI'
    ctrl=':XemDiemController' if view else ':NhapDiemController'
    g.actor(110,55,actor)
    g.box(430,70,760,160,ui)
    g.line([(155,130),(430,130)],'1: mở trang',(175,75),arrow=True)
    g.text(175,170,'2: chọn bộ lọc',27)
    g.box(50,500,650,1100,ctrl)
    g.line([(810,230),(810,365),(375,365),(375,500)],arrow=True)
    g.text(440,265,'2.1: taiKetQua(sv,hk)' if view else '2.1: taiDanhSach(nv,lhp)',28)
    if not view:g.text(830,360,'3: guiBangDiem(nv,lhp,ds)',28)
    # Each numbered DAO/entity message is placed directly above its own link.
    if view:
        g.text(75,640,'1.1: layDanhSachHocKy()\n1.2: layThongTinSinhVien(sv)\n2.1.1: layKetQuaHocTap(sv,hk)',27)
        nodes=[(':HocKyDAO',500,['1.1.1: getAllHocKy()']),
               (':SinhVienDAO',850,['1.2.1: findByMa(sv)']),
               (':DiemDAO',1320,['2.1.1.1: getDiemBySinhVien', 'AndHocKy(sv,hk)',
                                 '2.2.1: getDiemBySinhVien', 'AndHocKy(sv,null)'])]
        for name,y,msgs in nodes:
            g.box(1280,y,470,150,name)
            g.line([(700,y+75),(1280,y+75)],arrow=True)
            for i,m in enumerate(msgs):g.text(730,y-120+i*36,m,25)
        g.text(75,980,'Controller tự gọi\n2.1.2: tinhGPA(ds)\n2.2: tinhCPA(sv)\n2.3: tinhTinChiTichLuy\n(dsToanKhoa)',27)
        g.text(70,1670,'2.4: trả model kết quả cho UI để JSP hiển thị',29)
    else:
        g.text(75,680,'2.1.1: layBangDiemLHP(nv,lhp)\n3.1: luuBangDiem(nv,lhp,ds)',27)
        nodes=[(':LopHocPhanDAO',500,['2.1.1.1: findByMa(lhp)', '[kiểm tra phân công]']),
               (':DiemDAO',930,['2.1.1.2: getDiemByLHP(lhp)', '3.1.3: saveBangDiem(ds)']),
               ('d:Diem',1360,['3.1.1: kiemTraHopLe()', '3.1.2: tinhDiemTB()', '[lặp từng bản ghi]'])]
        for name,y,msgs in nodes:
            g.box(1280,y,470,150,name)
            g.line([(700,y+75),(1280,y+75)],arrow=True)
            for i,m in enumerate(msgs):g.text(730,y-80+i*36,m,25)
        g.text(75,1000,'Mỗi Diem kiểm tra rồi tính\nđiểm tổng kết và quy đổi.\nDAO lưu cả bảng trong\nmột transaction.',27)
        g.text(70,1670,'3.2: trả trạng thái lưu cho UI; lỗi SQL thì rollback và giữ form',29)
    g.text(70,1740,'Số thập phân thể hiện lời gọi lồng nhau; kết quả trả theo chiều ngược lại.',26)
    g.save('cau3b_comm_xem_diem' if view else 'cau3b_comm_nhap_diem')

def packages():
    g=Diagram(1800,1430)
    g.box(70,60,730,270,'com.qltc.ui',['NhapDiemUI','XemDiemUI'],'<<package>>')
    g.box(990,60,730,270,'com.qltc.controller',['NhapDiemController','XemDiemController'],'<<package>>')
    g.box(990,560,730,370,'com.qltc.dao',['DiemDAO','SinhVienDAO','LopHocPhanDAO','HocKyDAO'],'<<package>>')
    g.box(70,560,730,620,'com.qltc.model',list(models for models in META if META[models]['package']=='model'),'<<package>>')
    g.box(990,1160,730,200,'com.qltc.util',['DatabaseConnection'],'<<package>>')
    g.line([(800,190),(990,190)],'gọi',(840,135),dash=True,arrow=True)
    g.line([(1355,330),(1355,560)],'truy cập dữ liệu',(1370,425),dash=True,arrow=True)
    g.line([(990,735),(800,735)],'dùng',(845,680),dash=True,arrow=True)
    g.line([(990,275),(900,275),(900,475),(600,475),(600,560)],'dùng entity',(700,410),dash=True,arrow=True)
    g.line([(435,330),(435,560)],'model hiển thị',(450,370),dash=True,arrow=True)
    g.line([(1355,930),(1355,1160)],'mở JDBC',(1370,1015),dash=True,arrow=True)
    g.save('cau5a_package')

def deploy():
    g=Diagram(1800,1600)
    g.box(90,40,1620,280,'Máy khách',['<<execution environment>> Trình duyệt web',
           'HTML của nhập điểm và xem kết quả học tập'],'<<device>>')
    g.line([(900,320),(900,510)],'HTTPS',(930,385))
    g.box(90,510,1620,610,'Máy chủ ứng dụng',[], '<<device>>')
    g.box(160,645,1480,410,'Servlet JSP container J2EE',[], '<<execution environment>>')
    g.box(230,765,1340,235,'qltc.war',[
        'nhap-diem.jsp, xem-diem.jsp; WEB-INF/classes/com/qltc/',
        'ui, controller, model, dao, util (đủ 16 lớp ở Câu 3.a)',
        'WEB-INF/lib/mysql-connector-j.jar'],'<<artifact>>',29)
    g.line([(900,1120),(900,1300)],'JDBC qua TCP/IP',(930,1185))
    g.box(90,1300,1620,260,'Máy chủ cơ sở dữ liệu',[
        '<<execution environment>> MySQL',
        '<<artifact>> qltc_db  (7 bảng); kịch bản tạo: qltc_database.sql'],'<<device>>')
    g.save('cau5b_deployment_j2ee')

if __name__=='__main__':
    usecase();entities();design();entities(True);communication();communication(True);packages();deploy()
    print('Generated 8 monochrome UML figures')
