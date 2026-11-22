"""Model labels transcribed from N13 Nhom 10_fix1 screenshots, not the old skill."""
from copy import deepcopy

FIELDS={
 'Category':['maDanhMuc : int','tenDanhMuc : String','moTa : String'],
 'MenuItem':['maMon : int','tenMon : String','gia : BigDecimal','hinhAnh : String','dangKinhDoanh : boolean','kieuMon : KieuMon'],
 'Dish':['loaiMon : String','moTa : String'],
 'Combo':['soLuongNguoiAn : int'],
 'ComboDetail':['soLuong : int','ghiChu : String'],
 'Area':['maKhuVuc : int','tenKhuVuc : String'],
 'RestaurantTable':['maBan : int','soBan : String','trangThai : TrangThaiBan','maKhuVuc : int'],
 'Order':['maDon : int','thoiGianTao : long','trangThai : TrangThaiDon','tongTien : BigDecimal','vat : BigDecimal','chietKhau : BigDecimal'],
 'OrderTaiCho':['maBan : int'],
 'OrderMangVe':['diaChiGiao : String','soDienThoaiKhach : String'],
 'OrderItem':['maOrderItem : int','soLuong : int','donGia : BigDecimal','ghiChu : String','tuyChon : String','maDon : int','maMon : int'],
 'OrderMergeLog':['maLog : int','thoiGian : long','nhanVien : String','maDonDich : int','maDonNguon : int'],
 'Payment':['maThanhToan : int','tongTienDon : BigDecimal','thoiGianThanhToan : long','maDon : int'],
 'PaymentTienMat':['tienDaNhan : BigDecimal','tienThua : BigDecimal','tienTip : BigDecimal'],
 'PaymentThe':['loaiThe : LoaiThe','maGiaoDich : String'],
 'PaymentLog':['maLog : int','maDon : int','tongTien : BigDecimal','thoiGian : long','nhanVien : String','maThanhToan : int'],
 'TrangThaiDon':['DANG_PHUC_VU','CHO_THANH_TOAN','DA_THANH_TOAN','DA_GOP','DA_HUY'],
 'TrangThaiBan':['TRONG','DANG_PHUC_VU'],
 'KieuMon':['MON_LE','COMBO'],
 'LoaiThe':['VISA','MASTER','JCB','ATM'],
}
METHODS={'Combo':['+ tinhTongGiaGoc() : BigDecimal'],'Order':['+ tinhTongTien() : BigDecimal'],'OrderItem':['+ tinhThanhTien() : BigDecimal']}
ENUMS={'TrangThaiDon','TrangThaiBan','KieuMon','LoaiThe'}
RELATIONS=[
 ('Category','MenuItem','arrow',None,'1','0..*'),
 ('Dish','MenuItem','generalization'),('Combo','MenuItem','generalization'),
 ('Combo','ComboDetail','arrow',None,'1','0..*'),('ComboDetail','Dish','arrow',None,'0..*','1'),
 ('Area','RestaurantTable','arrow',None,'1','0..*'),('OrderTaiCho','RestaurantTable','arrow',None,'0..*','1'),
 ('OrderTaiCho','Order','generalization'),('OrderMangVe','Order','generalization'),
 ('Order','OrderItem','arrow',None,'1','0..*'),('OrderItem','MenuItem','arrow',None,'0..*','1'),
 ('OrderMergeLog','Order','arrow',None,'0..*','1'),('Order','Payment','arrow',None,'1','0..1'),
 ('PaymentTienMat','Payment','generalization'),('PaymentThe','Payment','generalization'),
 ('Payment','PaymentLog','arrow',None,'1','0..*'),
]
ANALYSIS_FIELDS={
 'RestaurantTable':['maBan','soBan','trangThai'],
 'Order':['maDon','thoiGianTao','trangThai','tongTien','vat','chietKhau'],
 'OrderTaiCho':[],
 'OrderItem':['maOrderItem','soLuong','donGia','ghiChu','tuyChon'],
 'OrderMergeLog':['maLog','thoiGian','nhanVien'],
 'Payment':['maThanhToan','tongTienDon','thoiGianThanhToan'],
 'PaymentLog':['maLog','maDon','tongTien','thoiGian','nhanVien'],
}

def entity(name,analysis=False):
    fields=FIELDS[name]
    if analysis:fields=ANALYSIS_FIELDS.get(name,[f.split(' : ')[0] for f in fields])
    return {'name':name,'fields':[('-' if name not in ENUMS else '')+f for f in fields],
            'methods':[] if analysis else METHODS.get(name,[]),'kind':'enum' if name in ENUMS else 'class'}

def service(name,methods,kind='class'):
    return {'name':name,'methods':methods,'kind':kind}

COMMON_DAOS={
 'MenuItemDAO':['+ layTatCa() : List<MenuItem>','+ layMonLeDangKinhDoanh() : List<Dish>','+ demTheoTenCombo(tenMon : String) : int','+ layTheoDanhMuc(maDanhMuc : int) : List<MenuItem>','+ layTheoMa(maMon : int) : MenuItem'],
 'OrderDAO':['+ layTheoBan(maBan : int) : List<Order>','+ luu(donHang : Order) : boolean','+ layDangPhucVuTru(maDonDich : int) : List<Order>','+ layTheoMa(maDon : int) : Order','+ layVaKhoa(maDon : int) : Order','+ capNhatTrangThai(maDon : int, trangThai : TrangThaiDon) : boolean','+ capNhatTongTien(maDon : int) : boolean','+ layChoThanhToan() : List<Order>'],
 'TableDAO':['+ layTheoKhuVuc(maKhuVuc : int) : List<RestaurantTable>','+ capNhatTrangThai(maBan : int, trangThai : TrangThaiBan) : boolean','+ layTheoDon(maDon : int) : RestaurantTable','+ giaiPhongNeuHetDon(maBan : int) : boolean'],
 'AreaDAO':['+ layTatCa() : List<Area>'],
 'CategoryDAO':['+ layTatCa() : List<Category>'],
 'ComboDAO':['+ luu(combo : Combo, chiTiet : List<ComboDetail>) : boolean'],
 'OrderItemDAO':['+ chuyenDong(maDonNguon : int, maDonDich : int) : int'],
 'OrderMergeLogDAO':['+ ghi(nhatKy : OrderMergeLog) : boolean'],
 'PaymentDAO':['+ luu(thanhToan : Payment) : boolean'],
 'PaymentLogDAO':['+ luu(nhatKy : PaymentLog) : boolean'],
 'InvoicePrinter':['+ inHoaDon(donHang : Order, thanhToan : Payment) : boolean'],
 'KitchenPrinter':['+ inPhieuBep(donHang : Order) : boolean'],
 'DBTransaction':['+ batDau() : void','+ xacNhan() : void','+ huy() : void'],
}

def build_graphs():
    result={}
    analysis_sets={
     13:['Category','MenuItem','Dish','Combo','ComboDetail','Area','RestaurantTable','Order','OrderTaiCho','OrderMangVe','OrderItem','OrderMergeLog','Payment','PaymentTienMat','PaymentThe','PaymentLog'],
     14:['Category','MenuItem','Dish','Combo','ComboDetail'],
     15:['Area','RestaurantTable','Order','OrderTaiCho','OrderMangVe','OrderItem','MenuItem','Category'],
     16:['Area','RestaurantTable','Order','OrderTaiCho','OrderItem','OrderMergeLog'],
     17:['RestaurantTable','Order','OrderTaiCho','OrderItem','Payment','PaymentTienMat','PaymentThe','PaymentLog']}
    for index,names in analysis_sets.items():
        result[index]={'nodes':[entity(n,True) for n in names],'edges':[r for r in RELATIONS if r[0] in names and r[1] in names],'cols':4 if index==13 else 3}
    names=['Category','MenuItem','Dish','Combo','ComboDetail','Area','RestaurantTable','Order','OrderTaiCho','OrderMangVe','OrderItem','OrderMergeLog','Payment','PaymentTienMat','PaymentThe','PaymentLog','TrangThaiDon','TrangThaiBan','KieuMon','LoaiThe']
    result[30]={'nodes':[entity(n) for n in names],'edges':deepcopy(RELATIONS),'cols':5}
    views={
     31:[service('MenuListView',['+ moManHinhThucDon() : void','+ chonTaoCombo() : void','+ lamMoiDanhSach() : void'],'boundary'),service('ComboFormView',['+ moBieuMau() : void','+ nhapThongTinChung(tenCombo : String, gia : BigDecimal, soLuongNguoiAn : int, maDanhMuc : int, hinhAnh : String) : void','+ chonMonThanhPhan(maMon : int, soLuong : int) : void','+ luu() : void','+ huy() : void','+ hienThiLoi(thongBao : String) : void'],'boundary'),service('MenuController',['+ layDanhSachThucDon() : List<MenuItem>','+ layMonLeDangKinhDoanh() : List<Dish>','+ layDanhMuc() : List<Category>','+ tinhTongGiaGoc(chiTiet : List<ComboDetail>) : BigDecimal','+ taoCombo(combo : Combo, chiTiet : List<ComboDetail>) : boolean'],'control')],
     32:[service('TableSelectionView',['+ moManHinhChonBan() : void','+ chonKhuVuc(maKhuVuc : int) : void','+ chonBan(maBan : int) : void'],'boundary'),service('OrderView',['+ moDon(donHang : Order) : void','+ chonDanhMuc(maDanhMuc : int) : void','+ chonMon(maMon : int, soLuong : int, ghiChu : String, tuyChon : String) : void','+ luuDon() : void'],'boundary'),service('OrderController',['+ layKhuVuc() : List<Area>','+ layBanTheoKhuVuc(maKhuVuc : int) : List<RestaurantTable>','+ taoDonMoi(maBan : int) : Order','+ layDonTheoBan(maBan : int) : List<Order>','+ layMonTheoDanhMuc(maDanhMuc : int) : List<MenuItem>','+ themMon(maMon : int, soLuong : int, ghiChu : String, tuyChon : String) : boolean','+ luuDon(donHang : Order) : boolean'],'control')],
     33:[service('OrderActionView',['+ moThaoTacDon(maDon : int) : void','+ chonGopHoaDon(maDonDich : int) : void'],'boundary'),service('MergeOrderView',['+ moBieuMau() : void','+ hienThiDonCoTheGop(ds : List<Order>) : void','+ chonDonNguon(maDonNguon : int) : void','+ hienThiCanhBao(thongBao : String) : void','+ gopDon(maDonDich : int, maDonNguon : int) : void','+ huy() : void'],'boundary'),service('MergeOrderController',['+ layDonCoTheGop(maDonDich : int) : List<Order>','+ kiemTraDonNguon(maDonDich : int, maDonNguon : int) : boolean','+ gopDon(maDonDich : int, dsDonNguon : List<Integer>, nhanVien : String) : boolean'],'control')],
     34:[service('PaymentListView',['+ moDanhSachDonChoThanhToan() : void','+ chonDon(maDon : int) : void'],'boundary'),service('PaymentView',['+ moHoaDon(donHang : Order) : void','+ chonTienMat() : void','+ chonThe() : void','+ nhapTienKhachDua(tienDaNhan : BigDecimal, tienTip : BigDecimal) : void','+ nhapThongTinThe(loaiThe : LoaiThe, maGiaoDich : String) : void','+ hienThiCanhBao(thongBao : String) : void','+ xacNhanThanhToan() : void'],'boundary'),service('PaymentController',['+ layDonChoThanhToan() : List<Order>','+ layChiTietDon(maDon : int) : Order','+ tinhTienThua(maDon : int, tienDaNhan : BigDecimal) : BigDecimal','+ thanhToanTienMat(maDon : int, tienDaNhan : BigDecimal, tienTip : BigDecimal, nhanVien : String) : boolean','+ thanhToanThe(maDon : int, loaiThe : LoaiThe, maGiaoDich : String, nhanVien : String) : boolean'],'control')]
    }
    # Restore the precise operation labels visible in the high resolution images.
    views[32][1]['methods']=['+ moManHinhDatMon(donHang : Order) : void','+ chonDanhMuc(maDanhMuc : int) : void','+ chonMon(maMon : int, soLuong : int, ghiChu : String, tuyChon : String) : void','+ hienThiCanhBao(thongBao : String) : void','+ luuDon() : void']
    views[32][2]['methods']=[m.replace('layKhuVuc','layDanhSachKhuVuc').replace('taoDonMoi','taoDonTaiCho') for m in views[32][2]['methods']]
    views[33][0]['methods']=['+ chonGopHoaDon(maDonDich : int) : void']
    views[33][1]['methods']=['+ moManHinhGopDon(maDonDich : int) : void','+ chonDonNguon(maDonNguon : int) : void','+ hienThiCanhBao(thongBao : String) : void','+ xacNhanGop() : void','+ huy() : void']
    views[33][2]['methods']=['+ layDonCoTheGop(maDonDich : int) : List<Order>','+ kiemTraDonNguon(maDonDich : int, maDonNguon : int) : boolean','+ gopDon(maDonDich : int, danhSachDonNguon : List<Integer>, nhanVien : String) : boolean']
    views[34][1]['methods']=[m.replace('moHoaDon','hienThiHoaDon') for m in views[34][1]['methods']]
    daos={31:['CategoryDAO','MenuItemDAO','ComboDAO'],32:['AreaDAO','TableDAO','MenuItemDAO','OrderDAO','KitchenPrinter'],33:['OrderDAO','OrderItemDAO','TableDAO','OrderMergeLogDAO','DBTransaction'],34:['OrderDAO','PaymentDAO','TableDAO','PaymentLogDAO','InvoicePrinter']}
    entities={31:['Category','MenuItem','Dish','Combo','ComboDetail','KieuMon'],32:['Area','RestaurantTable','Order','OrderTaiCho','OrderMangVe','OrderItem','MenuItem','TrangThaiDon','TrangThaiBan','KieuMon'],33:['RestaurantTable','Area','Order','OrderTaiCho','OrderItem','OrderMergeLog','TrangThaiDon','TrangThaiBan'],34:['RestaurantTable','Order','OrderTaiCho','OrderItem','Payment','PaymentTienMat','PaymentThe','PaymentLog','TrangThaiDon','TrangThaiBan','LoaiThe']}
    dao_entity={'CategoryDAO':'Category','MenuItemDAO':'MenuItem','ComboDAO':'Combo','AreaDAO':'Area','TableDAO':'RestaurantTable','OrderDAO':'Order','OrderItemDAO':'OrderItem','OrderMergeLogDAO':'OrderMergeLog','PaymentDAO':'Payment','PaymentLogDAO':'PaymentLog'}
    for index in views:
        nn=views[index]+[service(n,COMMON_DAOS[n]) for n in daos[index]]+[entity(n) for n in entities[index]]
        edges=[(views[index][0]['name'],views[index][1]['name'],'arrow'),(views[index][1]['name'],views[index][2]['name'],'arrow')]
        edges += [(views[index][2]['name'],n,'arrow') for n in daos[index]]
        edges += [(n,dao_entity[n],'arrow') for n in daos[index] if n in dao_entity and dao_entity[n] in entities[index]]
        edges += [r for r in RELATIONS if r[0] in entities[index] and r[1] in entities[index]]
        result[index]={'nodes':nn,'edges':edges,'cols':3}
    # Physical entity fields are transcribed independently from the ERD screenshot.
    erd={
     'Category':['PK maDanhMuc : integer(10)','tenDanhMuc : varchar(100)','moTa : varchar(255) [N]'],
     'MenuItem':['PK maMon : integer(10)','tenMon : varchar(150)','gia : decimal(12,0)','hinhAnh : varchar(255) [N]','dangKinhDoanh : tinyint(10)','kieuMon : tinyint(10)','FK maDanhMuc : integer(10) [N]'],
     'Dish':['loaiMon : varchar(50)','moTa : varchar(255) [N]','PK/FK maMon : integer(10)'],
     'Combo':['soLuongNguoiAn : integer(10)','PK/FK maMon : integer(10)'],
     'ComboDetail':['soLuong : integer(10)','ghiChu : varchar(255) [N]','PK/FK maCombo : integer(10)','PK/FK maMonLe : integer(10)'],
     'Area':['PK maKhuVuc : integer(10)','tenKhuVuc : varchar(100)'],
     'RestaurantTable':['PK maBan : integer(10)','soBan : varchar(20) [U]','trangThai : tinyint(10)','FK maKhuVuc : integer(10) [N]'],
     'Orders':['PK maDon : integer(10)','thoiGianTao : bigint(10)','trangThai : tinyint(10)','tongTien : decimal(12,0)','vat : decimal(5,2)','chietKhau : decimal(12,0)'],
     'OrderTaiCho':['PK/FK maDon : integer(10)','FK maBan : integer(10) [N]'],
     'OrderMangVe':['diaChiGiao : varchar(255) [N]','soDienThoaiKhach : varchar(15) [N]','PK/FK maDon : integer(10)'],
     'OrderItem':['PK maOrderItem : integer(10)','soLuong : integer(10)','donGia : decimal(12,0)','ghiChu : varchar(255) [N]','tuyChon : varchar(255) [N]','FK maDon : integer(10) [N]','FK maMon : integer(10) [N]'],
     'OrderMergeLog':['PK maLog : integer(10)','thoiGian : bigint(10)','nhanVien : varchar(100)','FK maDonDich : integer(10) [N]','FK maDonNguon : integer(10) [N]'],
     'Payment':['PK maThanhToan : integer(10)','tongTienDon : decimal(12,0)','thoiGianThanhToan : bigint(10)','FK maDon : integer(10) [N,U]'],
     'PaymentTienMat':['tienDaNhan : decimal(12,0)','tienThua : decimal(12,0)','tienTip : decimal(12,0)','PK/FK maThanhToan : integer(10)'],
     'PaymentThe':['loaiThe : varchar(20)','maGiaoDich : varchar(50)','PK/FK maThanhToan : integer(10)'],
     'PaymentLog':['PK maLog : integer(10)','maDon : integer(10)','tongTien : decimal(12,0)','thoiGian : bigint(10)','nhanVien : varchar(100)','FK maThanhToan : integer(10) [N,U]'],
    }
    erd_relations=[('Category','MenuItem','0..*'),('MenuItem','Dish','0..1'),('MenuItem','Combo','0..1'),('Combo','ComboDetail','0..*'),('Dish','ComboDetail','0..*'),('Area','RestaurantTable','0..*'),('RestaurantTable','OrderTaiCho','0..*'),('Orders','OrderTaiCho','0..1'),('Orders','OrderMangVe','0..1'),('Orders','OrderItem','0..*'),('MenuItem','OrderItem','0..*'),('Orders','OrderMergeLog','0..*'),('Orders','OrderMergeLog','0..*'),('Orders','Payment','0..1'),('Payment','PaymentTienMat','0..1'),('Payment','PaymentThe','0..1'),('Payment','PaymentLog','0..1')]
    nullable_links={('Category','MenuItem'),('Area','RestaurantTable'),('RestaurantTable','OrderTaiCho'),('Orders','OrderItem'),('MenuItem','OrderItem'),('Orders','OrderMergeLog'),('Orders','Payment'),('Payment','PaymentLog')}
    ee=[(a,b,'erd',None,'0..1' if (a,b) in nullable_links else '1',multi) for a,b,multi in erd_relations]
    result[29]={'nodes':[{'name':n,'fields':f,'kind':'erd'} for n,f in erd.items()],'edges':ee,'cols':4}
    return result
