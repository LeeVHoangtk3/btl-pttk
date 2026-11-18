"""Build the corrected submission from the same Java and schema sources."""
from pathlib import Path
import json,re,shutil
from docx import Document
from docx.shared import Inches,Pt,Cm,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
META=json.loads((ROOT/'tool/revision_manifest.json').read_text(encoding='utf-8'))
DEST=ROOT/'ban_da_sua/N13 Lê Việt Hoàng B23DCKH044.docx'
DEST.parent.mkdir(exist_ok=True)
QA=ROOT/'review_revision';QA.mkdir(exist_ok=True)
original=ROOT/DEST.name
if original.exists() and not (QA/'original.docx').exists():shutil.copy2(original,QA/'original.docx')
doc=Document()
sec=doc.sections[0];sec.page_width=Cm(21);sec.page_height=Cm(29.7)
sec.top_margin=Cm(1.7);sec.bottom_margin=Cm(1.7);sec.left_margin=Cm(2);sec.right_margin=Cm(2)
for s in doc.styles:
    if hasattr(s,'font'):
        s.font.name='Times New Roman';s.font.color.rgb=RGBColor(0,0,0)
normal=doc.styles['Normal'];normal.font.size=Pt(11.5)
normal.paragraph_format.line_spacing=1.05;normal.paragraph_format.space_after=Pt(4)
for name,size in [('Title',20),('Heading 1',15),('Heading 2',13),('Heading 3',12)]:
    s=doc.styles[name];s.font.size=Pt(size);s.font.bold=True
    s.paragraph_format.keep_with_next=True;s.paragraph_format.space_after=Pt(7)
    s.paragraph_format.space_before=Pt(9)
code=doc.styles.add_style('JavaCode',1);code.font.name='Consolas';code.font.size=Pt(8.5)
code.paragraph_format.space_after=Pt(0);code.paragraph_format.line_spacing=1.0
code.paragraph_format.widow_control=False

def p(text='',bold=False):
    x=doc.add_paragraph();x.add_run(text).bold=bold;return x
def h(text,level=1):return doc.add_heading(text,level)
def page():doc.add_page_break()
def table(headers,rows,widths):
    t=doc.add_table(rows=1,cols=len(headers));t.autofit=False
    borders=OxmlElement('w:tblBorders')
    for side in ['top','left','bottom','right','insideH','insideV']:
        el=OxmlElement('w:'+side);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'6');el.set(qn('w:color'),'000000');borders.append(el)
    t._tbl.tblPr.append(borders)
    for col,w in zip(t.columns,widths):col.width=Cm(w)
    for i,txt in enumerate(headers):t.rows[0].cells[i].text=txt
    for row in rows:
        for c,txt in zip(t.add_row().cells,row):c.text=str(txt)
    for ri,row in enumerate(t.rows):
        pr=row._tr.get_or_add_trPr()
        no_split=OxmlElement('w:cantSplit');pr.append(no_split)
        if ri==0:
            el=OxmlElement('w:tblHeader');pr.append(el)
        for ci,c in enumerate(row.cells):
            c.width=Cm(widths[ci]);tc=c._tc.get_or_add_tcPr()
            shd=OxmlElement('w:shd');shd.set(qn('w:fill'),'FFFFFF');tc.append(shd)
            borders=OxmlElement('w:tcBorders')
            for side in ['top','left','bottom','right']:
                el=OxmlElement('w:'+side);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'6');el.set(qn('w:color'),'000000');borders.append(el)
            tc.append(borders)
            margins=OxmlElement('w:tcMar')
            for side in ['top','left','bottom','right']:
                el=OxmlElement('w:'+side);el.set(qn('w:w'),'75');el.set(qn('w:type'),'dxa');margins.append(el)
            tc.append(margins)
            for par in c.paragraphs:
                par.paragraph_format.space_after=Pt(3);par.paragraph_format.line_spacing=1.0
                for run in par.runs:run.font.size=Pt(10.5);run.bold=ri==0
    p()
    return t
def image(name,caption,maxheight=22):
    path=ROOT/'diagrams'/(name+'.png')
    with Image.open(path) as im:w0,h0=im.size
    width=min(17,maxheight*w0/h0)
    par=doc.add_paragraph();par.alignment=WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.keep_with_next=True
    par.add_run().add_picture(str(path),width=Cm(width))
    cp=p(caption);cp.alignment=WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.keep_with_next=False
    for run in cp.runs:run.italic=True;run.font.size=Pt(11)
def codes(text):
    lines=[line for line in text.strip().splitlines() if line.strip()]
    for i,line in enumerate(lines):
        cp=doc.add_paragraph(line,'JavaCode')
        if i<7:cp.paragraph_format.keep_with_next=True
    p()

for text in ['HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG','KHOA CÔNG NGHỆ THÔNG TIN 1']:
    x=p(text,True);x.alignment=WD_ALIGN_PARAGRAPH.CENTER
p();p()
x=doc.add_paragraph('BÀI KIỂM TRA\nPHÂN TÍCH VÀ THIẾT KẾ\nHỆ THỐNG THÔNG TIN','Title');x.alignment=WD_ALIGN_PARAGRAPH.CENTER
x=p('Quản lý học tập theo tín chỉ');x.alignment=WD_ALIGN_PARAGRAPH.CENTER
p();p()
for text in ['Họ và tên sinh viên  Lê Việt Hoàng','Mã sinh viên  B23DCKH044','Nhóm môn học  N13','Email nộp bài  ndhien@hotmail.com']:
    x=p(text);x.alignment=WD_ALIGN_PARAGRAPH.CENTER
p();p();x=p('Hà Nội tháng 11 năm 2026');x.alignment=WD_ALIGN_PARAGRAPH.CENTER
page()
h('Phạm vi và giả định')
p('Bài làm phân tích và thiết kế hai ca sử dụng của hệ thống quản lý học tập theo tín chỉ: nhân viên nhập điểm của sinh viên và sinh viên xem thông tin về kết quả học tập. Nội dung trình bày theo thứ tự năm câu của đề bài, từ đặc tả nghiệp vụ đến thiết kế lớp, cơ sở dữ liệu, mã Java và triển khai J2EE ba tầng.')
p('Đăng nhập và phân quyền đã hoàn thành trước khi bắt đầu hai ca sử dụng. Nhân viên chỉ nhập điểm lớp được phân công; sinh viên chỉ xem kết quả gắn với tài khoản của mình. Mã người dùng được lấy từ phiên đã xác thực trên máy chủ.')
p('Danh sách sinh viên của lớp lấy từ đăng ký học phần, kể cả khi chưa có bản ghi điểm. Một đăng ký có tối đa một kết quả điểm. Chức năng tạo và hủy đăng ký nằm ngoài phạm vi hai ca sử dụng đang xét.')
p('Điểm thành phần có thể để trống khi chưa hoàn tất. Điểm tổng kết chỉ được tính khi có đủ ba thành phần. Trọng số được cấu hình trên từng môn học, không âm và có tổng bằng 1; ví dụ giả định 0,1 cho chuyên cần, 0,2 cho kiểm tra và 0,7 cho thi.')
p('Bảng quy đổi giả định: A từ 8,5 tương ứng 4,0; B+ từ 8,0 tương ứng 3,5; B từ 7,0 tương ứng 3,0; C+ từ 6,5 tương ứng 2,5; C từ 5,5 tương ứng 2,0; D+ từ 5,0 tương ứng 1,5; D từ 4,0 tương ứng 1,0; dưới 4,0 là F tương ứng 0. Các mức này phục vụ bài tập và không được khẳng định là quy chế PTIT.')
p('GPA dùng trọng số tín chỉ cho các học phần đã đủ điểm trong kỳ, bao gồm điểm F. CPA lấy kết quả tốt nhất của mỗi mã môn trên toàn khóa theo giả định xử lý học lại. Tín chỉ tích lũy chỉ tính các môn đạt từ 4,0/10 và mỗi mã môn được tính một lần. Chưa có học phần đủ điểm thì giá trị tổng hợp hiển thị là 0.')

page();h('Câu 1 Ca sử dụng và kịch bản')
h('1 a Biểu đồ ca sử dụng',2)
image('cau1a_usecase','Hình 1.1  Hai ca sử dụng và tiền điều kiện đăng nhập',17)
p('Hai tác nhân chính lần lượt là Nhân viên và Sinh viên. Khung ghi chú nối nét đứt với hai ca sử dụng thể hiện điều kiện đã đăng nhập và đúng vai trò trước khi thực hiện chức năng.')
h('1 b Kịch bản hai ca sử dụng',2)
scenarios=[('Nhập điểm của sinh viên',[
('1','Tác nhân và mục tiêu','Nhân viên nhập hoặc cập nhật điểm cho sinh viên đã đăng ký lớp được phân công.'),
('2','Tiền điều kiện','Đã đăng nhập với vai trò nhân viên. Lớp học phần và đăng ký sinh viên đã tồn tại. Có trọng số môn học hợp lệ.'),
('3','Luồng chính','1. Nhân viên mở trang nhập điểm.\n2. Hệ thống tải các lớp được phân công.\n3. Nhân viên chọn lớp. Hệ thống kiểm tra quyền và lấy danh sách từ đăng ký, kèm điểm nếu có.\n4. Nhân viên nhập hoặc sửa điểm CC, KT, thi.\n5. Nhân viên chọn Lưu. Hệ thống kiểm tra điểm, mã lớp, trùng sinh viên và đăng ký.\n6. Hệ thống tính điểm tổng kết theo trọng số môn học và quy đổi khi đủ điểm.\n7. Lưu cả bảng trong một giao dịch.\n8. Thông báo kết quả và hiển thị dữ liệu đã lưu.'),
('4','Ngoại lệ','3a. Không được phân công lớp: từ chối truy cập.\n3b. Chưa có đăng ký: thông báo danh sách rỗng.\n5a. Sai định dạng, NaN, vô cực hoặc ngoài 0 đến 10: giữ form và yêu cầu sửa. Ô trống được hiểu là chưa có điểm.\n5b. Không có đăng ký tương ứng: khóa ngoại từ chối lưu.\n7a. Lỗi CSDL: rollback toàn bộ, khôi phục trạng thái kết nối, giữ dữ liệu form và thông báo lỗi.'),
('5','Hậu điều kiện','Lưu thành công thì mọi bản ghi trong yêu cầu được cập nhật. Lưu thất bại thì không ghi một phần bảng điểm.')]),
('Xem thông tin về kết quả học tập',[
('1','Tác nhân và mục tiêu','Sinh viên tra cứu bảng điểm cá nhân theo học kỳ hoặc toàn khóa và xem GPA, CPA, tín chỉ tích lũy.'),
('2','Tiền điều kiện','Đã đăng nhập với vai trò sinh viên. Máy chủ xác định mã sinh viên từ phiên xác thực.'),
('3','Luồng chính','1. Sinh viên mở trang xem kết quả.\n2. Hệ thống tải hồ sơ qua SinhVienDAO và danh mục kỳ qua HocKyDAO.\n3. Sinh viên chọn học kỳ hoặc toàn khóa.\n4. Hệ thống lấy các kết quả qua DiemDAO.\n5. Tính GPA từ dữ liệu kỳ đã chọn.\n6. Lấy dữ liệu toàn khóa để tính CPA và tín chỉ tích lũy, xử lý học lại theo giả định.\n7. Hiển thị môn học, tín chỉ, điểm thành phần, điểm tổng kết, điểm chữ, điểm hệ 4 và các giá trị tổng hợp.'),
('4','Ngoại lệ','4a. Chưa có kết quả: hiển thị bảng rỗng và thông báo chưa có dữ liệu.\n4b. Môn chưa đủ điểm: để trống tổng kết, không đưa vào GPA/CPA.\n4c. Lỗi CSDL: hiển thị thông báo lỗi, không thay bằng kết quả 0 giả tạo.'),
('5','Hậu điều kiện','Sinh viên xem được dữ liệu cá nhân; dữ liệu trong CSDL không thay đổi.')])]
for title,rows in scenarios:
    h(title,3);table(['STT','Hạng mục','Nội dung'],rows,[1,3.2,12.8])

page();h('Câu 2 Thực thể và lớp phân tích')
h('2 a Các lớp thực thể',2)
purpose={
'NhanVien':'Người được phân công phụ trách lớp và nhập điểm.',
'SinhVien':'Người đăng ký học và nhận kết quả học tập.',
'MonHoc':'Danh mục môn, tín chỉ và trọng số điểm.',
'HocKy':'Danh mục học kỳ và năm học.',
'LopHocPhan':'Lớp của một môn được mở trong một học kỳ.',
'DangKy':'Ghi nhận sinh viên đã đăng ký lớp trước khi có điểm.',
'Diem':'Kết quả của một đăng ký, có thể chưa đủ điểm thành phần.'}
p('Bảy thực thể sau phục vụ hai ca sử dụng. Ở mức phân tích, thuộc tính chỉ dùng kiểu dữ liệu cơ bản; liên kết giữa thực thể thể hiện bằng quan hệ kết hợp. Phương thức đọc thuộc tính được giữ trên thực thể, còn truy vấn và điều phối đặt tại DAO và Controller.')
for n in purpose:
    h(n,3);p(purpose[n])
    attrs=META[n]['fields']
    attrs=[f for f in attrs if f.split(': ')[-1] not in purpose]
    if n in ['Diem','DangKy']: attrs=[f for f in attrs if not f.startswith(('- maSV:','- maLHP:'))]
    p('Thuộc tính: '+'; '.join(a[2:] for a in attrs)+'.')
    if n=='Diem':p('Phương thức: kiemTraHopLe(): boolean; tinhDiemTB(): void; quyDoiDiemChuVaHe4(): void; các getter/setter. tinhDiemTB đọc trọng số thông qua quan hệ với lớp học phần và môn học.')
    elif n=='MonHoc':p('Phương thức: kiemTraHopLe(): boolean để kiểm tra tín chỉ và tổng trọng số; các getter/setter.')
    else:p('Phương thức cơ bản: các getter/setter để đọc và gán dữ liệu thực thể.')
page();h('2 b Biểu đồ lớp phân tích',2)
image('cau2b_class_analysis','Hình 2.1  Lớp phân tích và bội số quan hệ',23)
p('NhanVien, MonHoc và HocKy liên kết với LopHocPhan theo bội 1 đến 0..*. SinhVien và LopHocPhan đều liên kết với DangKy theo bội 1 đến 0..*. Mỗi DangKy có 0..1 Diem; mỗi Diem thuộc đúng một sinh viên và một lớp. Hai liên kết trực tiếp tới Diem phải nhất quán với cặp đăng ký tương ứng.')

page();h('Câu 3 Lớp thiết kế và giao tiếp')
h('3 a Biểu đồ lớp thiết kế',2)
p('Thiết kế dùng Boundary, Control, Entity và DAO cho ứng dụng web. NhapDiemUI và XemDiemUI là lớp biên Java chuẩn bị dữ liệu cho JSP; không dùng Swing. Thuộc tính private được ký hiệu bằng dấu trừ, phương thức public bằng dấu cộng. Để đọc rõ, mô hình được tách thành phần điều khiển và truy cập dữ liệu ở Hình 3.1a, phần thực thể ở Hình 3.1b.')
image('cau3a_class_design','Hình 3.1a  Các lớp biên điều khiển DAO và tiện ích',22)
page();h('Các lớp thực thể trong thiết kế',2)
image('cau3a_entities','Hình 3.1b  Các lớp thực thể trong mô hình thiết kế',23)
p('Trong mã Java, Diem có tham chiếu sinhVien và lopHocPhan; LopHocPhan có monHoc, hocKy và giangVien. Hình biểu diễn các tham chiếu này bằng quan hệ để tránh lặp. Diem và DangKy còn giữ maSV, maLHP để ánh xạ khóa ngoại. Getter/setter của mọi thuộc tính và chữ ký đầy đủ nằm trong Câu 4.b.')
p('DatabaseConnection là tiện ích mở kết nối JDBC riêng cho thao tác, không phải DAO và không chia sẻ một Connection giữa các request. HocKyDAO chịu trách nhiệm danh mục học kỳ. SinhVienDAO chỉ truy vấn hồ sơ; GPA, CPA và tín chỉ tích lũy đặt ở XemDiemController.')
page();h('3 b Biểu đồ giao tiếp',2)
image('cau3b_comm_nhap_diem','Hình 3.2  Giao tiếp cho ca sử dụng nhập điểm',22)
p('Các thông điệp 2.1.1 và 3.1 đều vào NhapDiemController. Trước khi đọc hoặc lưu, Controller kiểm tra phân công qua LopHocPhanDAO. Khi lưu, Controller kiểm tra điểm và gán lại môn học từ CSDL, sau đó DiemDAO thực hiện giao dịch. Thứ tự 3.1.1, 3.1.2, 3.1.3 và 3.2 liên tục theo phạm vi lời gọi.')
page();h('Giao tiếp cho ca sử dụng xem kết quả',2)
image('cau3b_comm_xem_diem','Hình 3.3  Giao tiếp cho ca sử dụng xem kết quả học tập',22)
p('Hồ sơ được lấy từ SinhVienDAO, học kỳ từ HocKyDAO, điểm từ DiemDAO. XemDiemController tự tính GPA, CPA và tín chỉ tích lũy; dữ liệu toàn khóa được truy vấn riêng cho CPA. UI trả model cho trang JSP, không gọi truy vấn trực tiếp lên thực thể SinhVien.')

page();h('Câu 4 Cơ sở dữ liệu và mã Java')
h('4 a Các bảng dữ liệu',2)
p('CSDL thống nhất tên qltc_db. Các bảng dùng InnoDB; các khóa ngoại dùng ON DELETE RESTRICT để bảo vệ lịch sử học tập. Không xóa nhân viên, môn, kỳ, lớp, sinh viên hoặc đăng ký khi đang có dữ liệu tham chiếu. Quy trình lưu trữ hoặc vô hiệu hóa hồ sơ thay thế việc xóa dây chuyền.')
p('tbl_dang_ky là nguồn danh sách lớp. DiemDAO dùng LEFT JOIN từ đăng ký sang điểm để trả về cả sinh viên chưa có điểm. Khóa ngoại ghép (ma_sv, ma_lhp) của tbl_diem trỏ tới tbl_dang_ky ngăn tạo điểm cho sinh viên chưa đăng ký.')
sql=(ROOT/'qltc_database.sql').read_text(encoding='utf-8')
for match in re.finditer(r'CREATE TABLE (\w+) \((.*?)\n\) ENGINE',sql,re.S):
    name,body=match.groups();h(name,3)
    rows=[];constraints=[]
    for line in body.strip().splitlines():
        line=line.strip().rstrip(',')
        m=re.match(r'(\w+)\s+(VARCHAR\(\d+\)|INT|FLOAT|DATE)\s*(.*)',line)
        if m and not line.startswith(('CONSTRAINT','PRIMARY','FOREIGN')):
            field,typ,rest=m.groups();key='PK' if 'PRIMARY KEY' in rest else ('UQ' if 'UNIQUE' in rest else '')
            rows.append((field,typ,'Không' if 'NOT NULL' in rest or key=='PK' else 'Có',key,rest or 'Cho phép chưa có dữ liệu'))
        else:constraints.append(line)
    if name=='tbl_dang_ky':
        rows=[(a,b,c,'PK, FK' if a in ['ma_sv','ma_lhp'] else d,e) for a,b,c,d,e in rows]
    if name=='tbl_diem':rows=[(a,b,c,'FK, UQ' if a in ['ma_sv','ma_lhp'] else d,e) for a,b,c,d,e in rows]
    if name=='tbl_lop_hoc_phan':rows=[(a,b,c,'FK' if a in ['ma_mh','ma_hoc_ky','ma_nv'] else d,e) for a,b,c,d,e in rows]
    table(['Trường','Kiểu','Null','Khóa','Ràng buộc'],rows,[3,3.1,1.6,1.8,7.5])
    if constraints:codes('\n'.join(constraints))
p('PK là khóa chính; FK là khóa ngoại; UQ là duy nhất. tbl_diem có UQ(ma_sv,ma_lhp); tbl_dang_ky có PK(ma_sv,ma_lhp). Điểm thành phần nằm trong [0,10], hệ 4 trong [0,4]. Trọng số không âm và tổng bằng 1. Tệp qltc_database.sql đi kèm chứa toàn bộ DDL, không tự xóa CSDL.')

h('4 b Sinh khung lớp Java từ thiết kế',2)
p('Phần này trình bày 16 lớp ở Câu 3.a với package, phạm vi private/public và giải thích phương thức bằng chú thích. Đây là khung lớp cùng phần xử lý cốt lõi; trang JSP, ánh xạ request, đăng nhập và cấu hình máy chủ là phần tích hợp triển khai. Các hàm JDBC khai báo throws SQLException để tầng web có thể thông báo lỗi và giữ form.')
p('Mã dùng Java SE và JDBC; khi chạy với MySQL cần bổ sung Connector/J và các biến môi trường QLTC_DB_URL, QLTC_DB_USER, QLTC_DB_PASSWORD. Luồng web chuyển ô trống thành null, kiểm tra chuỗi số trước khi tạo Float và chỉ lấy mã nhân viên/sinh viên từ session đã xác thực.')
for package in ['model','util','dao','controller','ui']:
    for name,info in META.items():
        if info['package']!=package:continue
        h('Lớp '+name,3)
        codes((ROOT/'src/com/qltc'/package/(name+'.java')).read_text(encoding='utf-8'))

page();h('Câu 5 Gói và triển khai')
h('5 a Biểu đồ gói từ các lớp ở Câu 3 a',2)
image('cau5a_package','Hình 5.1  Các package com.qltc và quan hệ phụ thuộc',21)
p('Các gói chứa đúng 16 lớp đã sinh ở Câu 4.b. UI phụ thuộc Controller và Model; Controller phụ thuộc DAO và Model; DAO phụ thuộc Model và Util. Không thêm các interface ngoài mô hình. DatabaseConnection nằm trong com.qltc.util.')
page();h('5 b Triển khai J2EE ba tầng',2)
image('cau5b_deployment_j2ee','Hình 5.2  Máy khách máy chủ ứng dụng và máy chủ CSDL',22)
p('Tầng 1 là trình duyệt nhận HTML qua HTTPS. Tầng 2 là máy chủ ứng dụng chạy servlet/JSP container và triển khai qltc.war. Tầng 3 là máy chủ CSDL MySQL độc lập, giao tiếp với ứng dụng qua JDBC. Các node máy dùng device, môi trường chạy dùng execution environment và tệp triển khai dùng artifact.')
p('Trong phương án đóng gói, qltc.war chứa nhap-diem.jsp, xem-diem.jsp, toàn bộ lớp Java dưới WEB-INF/classes/com/qltc và driver trong WEB-INF/lib. NhapDiemUI và XemDiemUI được triển khai trên máy chủ ứng dụng làm lớp biên cho JSP. NhapDiemController và XemDiemController giữ đúng tên ở biểu đồ và mã. Tệp qltc_database.sql tạo CSDL qltc_db trên máy chủ dữ liệu; các tệp class không nằm rời bên ngoài WAR.')

# Force explicit monochrome OOXML throughout, including all inherited styles.
for part in [doc.element,doc.styles.element]:
    for border in part.xpath('.//w:pBdr'):border.getparent().remove(border)
    for color in part.xpath('.//w:color'):
        color.set(qn('w:val'),'000000')
        for a in ['themeColor','themeTint','themeShade']:
            color.attrib.pop(qn('w:'+a),None)
    for shd in part.xpath('.//w:shd'):
        shd.set(qn('w:fill'),'FFFFFF');shd.set(qn('w:color'),'auto')
        for a in ['themeFill','themeFillTint','themeFillShade']:shd.attrib.pop(qn('w:'+a),None)
doc.core_properties.author='Lê Việt Hoàng'
doc.core_properties.title='Quản lý học tập theo tín chỉ'
doc.core_properties.subject='Bài kiểm tra phân tích và thiết kế hệ thống thông tin nhóm N13'
doc.save(DEST)
print('Corrected DOCX saved to ban_da_sua')
print(f'{len(doc.tables)} tables, {len(doc.inline_shapes)} figures, {len(META)} code classes')
