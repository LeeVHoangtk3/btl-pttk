"""Build a reviewable report revision using the supplied native VP diagrams.

Source fix1 is read only. Vector class diagrams are generated from transcribed
labels; native sequence/activity/use-case exports retain their original pixels.
Run: python redesign_report_from_fix1.py assets|assemble|verify|finalize
After assets, run render_vp_svg.cjs with the bundled Node runtime.
"""
from pathlib import Path
from io import BytesIO
from copy import deepcopy
import hashlib,json,re,shutil,sys
import numpy as np
from PIL import Image,ImageChops
from docx import Document
from docx.oxml import OxmlElement,parse_xml
from docx.oxml.ns import qn
from docx.shared import Cm,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.part import Part
from docx.opc.packuri import PackURI
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from vp_diagram_canvas import Canvas,graph,VP_BLUE
from vp_report_models import build_graphs

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'build/vp_redesign'
OUT=ROOT/'code_pttk/diagrams/vp_fix1'
SOURCE=ROOT/'code_pttk/docs/N13 Nhóm 10_fix1.docx'
TARGET=ROOT/'code_pttk/docs/doi_chieu_datn24/N13 Nhóm 10 cấu trúc tham khảo ĐATN24.docx'
SEQUENCES={18,19,20,21,35,36,37,38}
ACTIVITIES={25,26,27,28}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def doc_images(doc):return [doc.part.related_parts[s._inline.xpath('.//a:blip/@r:embed')[0]].blob for s in doc.inline_shapes]
def snapshot(doc):
    return {'paragraphs':[p.text for p in doc.paragraphs if p.text and not p.style.name.lower().startswith('toc')],
            'tables':[[[c.text for c in r.cells] for r in t.rows] for t in doc.tables]}
def source_caption(doc,shape):
    p=shape._inline.getparent()
    while p.tag!=qn('w:p'):p=p.getparent()
    for el in p.itersiblings():
        if el.tag==qn('w:p'):
            text=''.join(el.itertext())
            # python-docx paragraph provides the correct text without XML duplicates.
            from docx.text.paragraph import Paragraph
            text=Paragraph(el,doc._body).text
            if text.startswith('Hình '):return text
    raise ValueError('Missing source caption')

def compact_native(blob,index):
    rgba=Image.open(BytesIO(blob)).convert('RGBA')
    bg=Image.new('RGBA',rgba.size,'white');bg.alpha_composite(rgba)
    image=bg.convert('RGB')
    bbox=ImageChops.difference(image,Image.new('RGB',image.size,'white')).getbbox()
    image=image.crop(bbox)
    removed=0
    if index in SEQUENCES|ACTIVITIES:
        a=np.asarray(image);dark=(a[:,:,:3].max(axis=2)<160)
        blue=(a[:,:,2]>170)&(a[:,:,0]<180)&(a[:,:,1]>120)
        def longest(mask):
            padded=np.pad(mask.astype(np.int8),(1,1));changes=np.diff(padded)
            starts=np.flatnonzero(changes==1);ends=np.flatnonzero(changes==-1)
            return int(max(ends-starts,default=0))
        content=np.array([longest(d)>4 or longest(b)>17 for d,b in zip(dark,blue)])
        # Protect all glyph, arrowhead and symbol rows with a 4-pixel halo.
        content=np.convolve(content.astype(int),np.ones(9,dtype=int),mode='same')>0
        keep=np.ones(len(content),dtype=bool);start=0
        while start<len(content):
            if content[start]:start+=1;continue
            end=start+1
            while end<len(content) and not content[end]:end+=1
            length=end-start
            if length>18:
                # Remove only rows occupied by straight lifelines or empty lanes.
                keep[start+6:end-6]=False
            start=end
        removed=int((~keep).sum())
        image=Image.fromarray(a[keep])
    padded=Image.new('RGB',(image.width+32,image.height+32),'white');padded.paste(image,(16,16))
    return padded,removed

def states():
    def box(c,x,y,label):
        c.rect(x,y,220,62,rx=9);c.text(x+110,y+37,label,18)
    c=Canvas(1000,380);c.initial(35,150);box(c,180,119,'DANG_PHUC_VU');box(c,570,119,'CHO_THANH_TOAN');c.initial(950,150,True)
    c.line([(43,150),(180,150)],True);c.text(110,133,'Tạo đơn',17)
    c.line([(400,150),(570,150)],True);c.text(485,131,'Yêu cầu thanh toán',17)
    c.line([(790,150),(940,150)],True);c.text(865,131,'Thanh toán xong',17)
    c.line([(290,119),(290,55),(365,55),(365,119)],True);c.text(328,36,'Thêm / sửa món',17)
    c.initial(290,320,True);c.initial(680,320,True)
    c.line([(240,181),(240,240),(290,240),(290,310)],True);c.text(145,244,'Gộp đơn',17)
    c.line([(350,181),(350,274),(680,274),(680,310)],True);c.text(492,260,'Hủy đơn',17)
    c.line([(680,181),(680,310)],True);c.text(744,244,'Hủy đơn',17)
    c.save(OUT/'figure-22.svg')
    c=Canvas(940,360);c.initial(35,110);box(c,170,79,'TRONG');box(c,620,79,'DANG_PHUC_VU')
    c.line([(43,110),(170,110)],True);c.line([(390,110),(620,110)],True);c.text(505,91,'Tạo đơn mới',18)
    for j,label in enumerate(['Thanh toán xong','Gộp đơn giải phóng bàn nguồn','Hủy đơn cuối cùng']):
        yy=205+j*55
        c.line([(700+j*35,141),(700+j*35,yy),(240+j*40,yy),(240+j*40,141)],True)
        c.text(490,yy-10,label,17,back=True)
    c.save(OUT/'figure-23.svg')
    c=Canvas(1080,380);c.initial(30,140);box(c,225,109,'DANG_KINH_DOANH');box(c,660,109,'TAM_NGUNG');c.initial(1035,140,True)
    c.line([(38,140),(225,140)],True);c.text(130,121,'Quản lý tạo món / combo',17)
    c.line([(445,140),(660,140)],True);c.text(552,120,'Tạm ngừng (hết nguyên liệu)',16)
    c.line([(775,171),(775,260),(335,260),(335,171)],True);c.text(552,245,'Kinh doanh lại',17)
    c.line([(880,140),(1025,140)],True);c.text(954,120,'Xóa khỏi thực đơn',16)
    c.line([(275,171),(275,325),(1035,325),(1035,150)],True);c.text(655,312,'Xóa khỏi thực đơn',17)
    for x in [335,770]:
        c.line([(x-30,109),(x-30,48),(x+30,48),(x+30,109)],True);c.text(x,30,'Sửa thông tin',16)
    c.save(OUT/'figure-24.svg')

def usecases():
    def boundary(c,w,h):
        c.rect(280,40,w-310,h-70,'white');c.text((w+250)/2,73,'Hệ thống quản lý nhà hàng Thanh Hoa',20)
    def uc(c,x,y,label,w=250,h=78,extensions=None):
        c.ellipse(x,y,w/2,h/2)
        if extensions:
            c.text(x,y-27,label,20)
            c.line([(x-w/2+8,y-15),(x+w/2-8,y-15)])
            c.text(x,y+5,'extension points',15,True)
            c.text(x,y+27,extensions,15)
        else:c.text(x,y+7,label,20)
    c=Canvas(1360,700);boundary(c,1360,700)
    c.actor(100,127,'Quản lý');c.actor(100,332,'Nhân viên order');c.actor(100,552,'Thu ngân')
    for x,y,label,ext in [(460,170,'Quản lý món ăn',None),(790,170,'Quản lý combo',None),(1120,170,'Tạo đơn hàng','Đơn tại chỗ'),(460,360,'Gộp đơn',None),(790,360,'Tách đơn',None),(1120,360,'Hủy đơn',None),(460,550,'Chuyển bàn',None),(790,550,'Thanh toán','Tiền mặt / Thẻ')]:uc(c,x,y,label,h=118 if ext else 78,extensions=ext)
    for x in (460,790):c.line([(118,150),(220,150),(220,108),(x,108),(x,131)])
    c.line([(118,355),(245,355),(245,92),(1285,92),(1285,170),(1245,170)])
    for x in (460,790,1120):
        c.line([(118,355),(220,355),(220,275),(x,275),(x,321)])
        c.line([(118,575),(240,575),(240,440),(x,440),(x,399)])
    c.line([(118,355),(205,355),(205,550),(335,550)])
    for x,y in [(460,589),(790,609)]:c.line([(118,575),(220,575),(220,640),(x,640),(x,y)])
    c.save(OUT/'figure-8.svg')
    c=Canvas(1400,810);boundary(c,1400,810);c.actor(100,325,'Quản lý')
    for x,y,label in [(460,210,'Thêm món ăn'),(800,210,'Sửa món ăn'),(1140,210,'Xóa món ăn'),(460,450,'Tạo combo'),(800,450,'Sửa combo'),(1140,450,'Xóa combo'),(800,690,'Chọn món cho combo')]:uc(c,x,y,label)
    for x in (460,800,1140):
        c.line([(118,348),(220,348),(220,130),(x,130),(x,171)])
        c.line([(118,348),(240,348),(240,540),(x,540),(x,489)])
    c.line([(460,489),(460,610),(800,610),(800,651)],True,True);c.text(560,596,'«include»',18,back=True)
    c.line([(800,489),(800,651)],True,True);c.text(850,575,'«include»',18,back=True)
    c.save(OUT/'figure-9.svg')
    c=Canvas(1250,650);boundary(c,1250,650);c.actor(100,210,'Nhân viên order')
    uc(c,520,240,'Tạo đơn hàng',w=310,h=138,extensions='Đơn tại chỗ')
    uc(c,1010,240,'Chọn bàn',w=260)
    uc(c,520,500,'Chọn món',w=260);uc(c,1010,500,'Lưu đơn & in phiếu bếp',w=350)
    c.line([(118,233),(365,233)])
    c.line([(880,240),(675,240)],True,True);c.text(780,222,'«extend»',18,back=True)
    c.line([(520,309),(520,461)],True,True);c.text(570,390,'«include»',18,back=True)
    c.line([(630,288),(730,288),(730,500),(835,500)],True,True);c.text(750,400,'«include»',18,back=True)
    c.save(OUT/'figure-10.svg')
    # A single aligned case column lets both actors connect without crossing cases.
    c=Canvas(1180,790);c.rect(280,40,620,720,'white')
    c.text(590,77,'Hệ thống quản lý nhà hàng Thanh Hoa',20)
    c.actor(100,340,'Thu ngân');c.actor(1080,340,'Nhân viên order')
    for y,label in [(180,'Gộp đơn'),(350,'Tách đơn'),(520,'Hủy đơn'),(690,'Chuyển bàn')]:
        uc(c,590,y,label,w=280)
        c.line([(118,363),(450,y)])
        c.line([(1062,363),(730,y)])
    c.save(OUT/'figure-11.svg')
    c=Canvas(1320,680);boundary(c,1320,680);c.actor(100,210,'Thu ngân')
    uc(c,520,240,'Thanh toán',w=300,h=138,extensions='Tiền mặt / Thẻ')
    uc(c,1025,240,'Thanh toán tiền mặt',w=340)
    uc(c,520,520,'Thanh toán bằng thẻ',w=340);uc(c,1025,520,'In hóa đơn',w=270)
    c.line([(118,233),(370,233)])
    c.line([(855,240),(670,240)],True,True);c.text(760,221,'«extend»',18,back=True)
    c.line([(520,481),(520,309)],True,True);c.text(570,409,'«extend»',18,back=True)
    c.line([(630,290),(750,290),(750,520),(890,520)],True,True);c.text(800,411,'«include»',18,back=True)
    c.save(OUT/'figure-12.svg')

def package(c,x,y,w,h,title):
    c.rect(x,y-24,110,24);c.rect(x,y,w,h);c.text(x+w/2,y+27,title,20,True)
def component(c,x,y,w,h,label):
    c.rect(x,y,w,h);c.rect(x+w-26,y+9,15,18,'white');c.rect(x+w-30,y+12,7,4,'white');c.rect(x+w-30,y+20,7,4,'white')
    c.text(x+w/2,y+28,'«component»',13);c.text(x+w/2,y+55,label,16)
def structural():
    c=Canvas(1160,900)
    for y,title,labels in [(60,'Giao diện người dùng',['Giao diện quản lý thực đơn','Giao diện chọn bàn và đặt món','Giao diện gộp đơn','Giao diện thanh toán']),(320,'Dịch vụ nghiệp vụ',['Dịch vụ thực đơn - combo','Dịch vụ đơn hàng','Dịch vụ gộp đơn','Dịch vụ thanh toán'])]:
        package(c,60,y,1040,160,title)
        for j,label in enumerate(labels):package(c,80+j*255,y+67,235,70,'');c.text(197+j*255,y+108,label,14)
    for x,y,w,h,title in [(230,590,340,95,'Truy cập dữ liệu (DAO)'),(710,590,290,95,'Tiện ích (Util)'),(230,790,340,70,'Thực thể (Entity)'),(710,790,290,70,'CSDL MySQL')]:package(c,x,y,w,h,title)
    c.line([(580,220),(580,320)],True,True)
    c.line([(480,480),(480,540),(400,540),(400,566)],True,True)
    c.line([(740,480),(740,540),(855,540),(855,566)],True,True)
    c.line([(400,685),(400,766)],True,True)
    c.line([(530,685),(530,730),(855,730),(855,766)],True,True)
    c.line([(60,140),(22,140),(22,825),(230,825)],True,True)
    c.line([(60,400),(40,400),(40,810),(230,810)],True,True)
    c.save(OUT/'figure-39.svg')
    c=Canvas(1260,920)
    def device(x,y,w,h,title):
        c.items.append(f'<polygon points="{x},{y} {x+10},{y-10} {x+w+10},{y-10} {x+w+10},{y+h-10} {x+w},{y+h} {x},{y+h}" fill="{VP_BLUE}" stroke="black" stroke-width="1.25"/>')
        c.rect(x,y,w,h);c.line([(x+w,y),(x+w+10,y-10)])
        title_size=18
        from PIL import ImageFont
        while ImageFont.truetype('C:/Windows/Fonts/arial.ttf',title_size).getlength(title)>w-16:title_size-=1
        c.text(x+w/2,y+28,title,title_size,True)
    for x,w,title,label in [(50,260,'Máy trạm quản lý','Giao diện quản lý thực đơn'),(430,400,'Thiết bị nhân viên order (POS/Tablet)','Giao diện chọn bàn và đặt món'),(950,260,'Máy thu ngân','Giao diện thanh toán')]:
        device(x,50,w,140,title)
        if x==430:
            component(c,x+12,95,184,75,'Chọn bàn và đặt món')
            component(c,x+204,95,184,75,'Giao diện gộp đơn')
        else:component(c,x+15,95,w-30,75,label)
    device(170,320,920,350,'Máy chủ ứng dụng')
    for j,label in enumerate(['Dịch vụ thực đơn - combo','Dịch vụ đơn hàng','Dịch vụ gộp đơn','Dịch vụ thanh toán']):component(c,190+j*225,380,205,85,label)
    component(c,480,495,300,75,'Lớp truy cập dữ liệu (DAO)')
    c.rect(480,598,300,48);c.text(630,617,'«artifact»',13);c.text(630,637,'RestaurantPOS.war',17)
    for x,w,title in [(40,270,'Máy chủ CSDL MySQL'),(390,230,'Máy in bếp'),(710,230,'Máy in hóa đơn'),(1010,220,'Dịch vụ thanh toán bên ngoài')]:device(x,790,w,95,title)
    c.rect(55,832,240,35);c.text(175,855,'CSDL nhà hàng (16 bảng)',16)
    for a,b,mid,label in [(180,320,250,'HTTP/HTTPS'),(630,630,250,'HTTP/HTTPS'),(1080,960,250,'HTTP/HTTPS')]:
        c.line([(a,190),(a,mid),(b,mid),(b,320)]);c.text((a+b)/2,mid-12,label,16,back=True)
    for j,(x,label) in enumerate([(175,'JDBC'),(505,'In phiếu bếp'),(825,'In hóa đơn'),(1120,'API thanh toán')]):
        sx=315+j*205;c.line([(sx,670),(sx,720),(x,720),(x,780)]);c.text((sx+x)/2,708,label,16,back=True)
    for j in range(4):
        sx=292+j*225;c.line([(sx,465),(sx,480),(540+j*55,480),(540+j*55,495)],True,True)
    c.line([(630,570),(630,598)],True,True)
    c.save(OUT/'figure-40.svg')

def assets():
    WORK.mkdir(exist_ok=True,parents=True);OUT.mkdir(exist_ok=True,parents=True)
    statefile=WORK/'state.json'
    if statefile.exists():state=json.loads(statefile.read_text('utf-8'));assert sha(SOURCE)==state['source_sha256']
    else:
        state={'source_sha256':sha(SOURCE),'target_sha256_before':sha(TARGET)}
        shutil.copy2(TARGET,WORK/'original-target.docx')
        statefile.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
    s=Document(SOURCE);blobs=doc_images(s)
    manifest=[]
    graphs=build_graphs()
    for index in range(8,41):
        info={'index':index,'caption':source_caption(s,s.inline_shapes[index]),'source_image_sha256':hashlib.sha256(blobs[index]).hexdigest()}
        if index in graphs:
            spec=graphs[index]
            if index in (31,32,33,34):
                # Keep large operation lists readable: two coordinated panels.
                services=[n for n in spec['nodes'] if n['name'] not in __import__('vp_report_models').FIELDS]
                entities=[n for n in spec['nodes'] if n not in services]
                service_names={n['name'] for n in services};entity_names={n['name'] for n in entities}
                links=[e for e in spec['edges'] if e[0] in service_names and e[1] in entity_names]
                stubs=[{'name':n['name'],'kind':'class'} for n in entities if any(e[1]==n['name'] for e in links)]
                a=graph(OUT/f'figure-{index}-a.svg',services+stubs,[e for e in spec['edges'] if e[0] in service_names],cols=3,box_w=290,font=18)
                b=graph(OUT/f'figure-{index}-b.svg',entities,[e for e in spec['edges'] if e[0] in entity_names and e[1] in entity_names],cols=3,box_w=290,font=18)
                info.update(method='vector_relayout',panels=[f'figure-{index}-a',f'figure-{index}-b'],geometry=[a,b])
            else:
                compact_rows=index in (16,17)
                meta=graph(OUT/f'figure-{index}.svg',spec['nodes'],spec['edges'],cols=spec['cols'],box_w=300,font=18,row_gap=50 if compact_rows else 90,clearance=20 if compact_rows else 30)
                info.update(method='vector_relayout',panels=[f'figure-{index}'],geometry=[meta])
        elif index in (8,9,10,11,12,22,23,24,39,40):
            info.update(method='vector_relayout',panels=[f'figure-{index}'])
        else:
            im,removed=compact_native(blobs[index],index);im.save(OUT/f'figure-{index}.png',dpi=(260,260))
            info.update(method='native_vp_export',panels=[f'figure-{index}'],removed_straight_rows=removed,size=im.size)
        manifest.append(info)
    usecases();states();structural()
    (OUT/'manifest.json').write_text(json.dumps({'source':str(SOURCE.relative_to(ROOT)),'source_sha256':state['source_sha256'],'figures':manifest},ensure_ascii=False,indent=2),encoding='utf-8')
    assert sha(SOURCE)==state['source_sha256']
    print('33 source figures prepared. fix1 unchanged.')

def image_para(shape):
    p=shape._inline.getparent()
    while p.tag!=qn('w:p'):p=p.getparent()
    return p
def attach_svg(doc,shape,path,serial):
    part=Part(PackURI(f'/word/media/vp_diagram_{serial}.svg'),'image/svg+xml',path.read_bytes(),doc.part.package)
    rid=doc.part.relate_to(part,RT.IMAGE)
    blip=shape._inline.xpath('.//a:blip')[0]
    for child in list(blip):
        if child.tag==qn('a:extLst'):blip.remove(child)
    ext=OxmlElement('a:extLst')
    ext.append(parse_xml(f'<a:ext xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" uri="{{96DAC541-7B7A-43D3-8B79-37D633B846F1}}"><asvg:svgBlip xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="{rid}"/></a:ext>'))
    blip.append(ext)

def section_break(doc,after,landscape):
    p=OxmlElement('w:p');after.addnext(p)
    pp=OxmlElement('w:pPr');p.append(pp)
    sect=deepcopy(doc.sections[-1]._sectPr)
    typ=sect.find(qn('w:type'))
    if typ is None:typ=OxmlElement('w:type');sect.insert(0,typ)
    typ.set(qn('w:val'),'nextPage')
    pg=sect.find(qn('w:pgSz'))
    pg.set(qn('w:w'),'16838' if landscape else '11906');pg.set(qn('w:h'),'11906' if landscape else '16838')
    if landscape:pg.set(qn('w:orient'),'landscape')
    else:pg.attrib.pop(qn('w:orient'),None)
    margins=sect.find(qn('w:pgMar'))
    for side in ('top','bottom','left','right'):margins.set(qn('w:'+side),'1134' if landscape else ('1701' if side=='left' else '1134'))
    pp.append(sect)
    return p

def assemble():
    from docx.text.paragraph import Paragraph
    state=json.loads((WORK/'state.json').read_text('utf-8'));assert sha(SOURCE)==state['source_sha256'];assert sha(TARGET)==state['target_sha256_before']
    d=Document(TARGET);before=snapshot(d)
    manifest=json.loads((OUT/'manifest.json').read_text('utf-8'))['figures']
    shapes=list(d.inline_shapes);changed_captions={};added_text=[];placements=[]
    for item in manifest:
        index=item['index'];shape=shapes[index];p=image_para(shape)
        caption=None
        for el in p.itersiblings():
            if el.tag==qn('w:p'):
                pp=Paragraph(el,d._body)
                if pp.text.startswith('Hình '):caption=pp;break
        assert caption is not None
        old_caption=caption.text
        desired_caption=item['caption']+(' (a)' if len(item['panels'])>1 else '')
        if old_caption!=desired_caption:
            changed_captions[old_caption]=desired_caption;caption.runs[0].text=desired_caption
            for run in caption.runs[1:]:run.text=''
        panel_shapes=[shape]
        if len(item['panels'])>1:
            extra=OxmlElement('w:p');caption._p.addnext(extra);extra_p=Paragraph(extra,d._body)
            extra_p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            new_shape=extra_p.add_run().add_picture(str(OUT/(item['panels'][1]+'.png')))
            panel_shapes.append(new_shape)
            cp=OxmlElement('w:p');extra.addnext(cp);continued=Paragraph(cp,d._body)
            continued.style=caption.style
            continued.add_run(item['caption']+' (b) Các lớp thực thể và kiểu liệt kê')
            added_text.append(continued.text)
            extra_p.paragraph_format.page_break_before=True
            extra_p.paragraph_format.keep_with_next=True
            continued.paragraph_format.keep_with_next=False
        wide=index in (13,29,30,40)
        for j,(panel,sh) in enumerate(zip(item['panels'],panel_shapes)):
            png=OUT/(panel+'.png');im=Image.open(png)
            rid,_=d.part.get_or_add_image(str(png));sh._inline.xpath('.//a:blip')[0].set(qn('r:embed'),rid)
            ratio=im.width/im.height
            max_w=25.2 if wide else 15.8
            max_h=13.3 if wide else (21.3 if index in SEQUENCES|ACTIVITIES or len(panel_shapes)>1 else 18.5)
            if index==28:max_h=20.0
            width=min(max_w,max_h*ratio);sh.width=Cm(width);sh.height=Cm(width/ratio)
            if (OUT/(panel+'.svg')).exists():attach_svg(d,sh,OUT/(panel+'.svg'),f'{index}_{j}')
            ip=Paragraph(image_para(sh),d._body)
            ip.alignment=WD_ALIGN_PARAGRAPH.CENTER;ip.paragraph_format.keep_with_next=True
            ip.paragraph_format.space_before=Pt(3);ip.paragraph_format.space_after=Pt(5)
            placements.append({'index':index,'panel':panel,'width_cm':width,'height_cm':width/ratio})
        caption.paragraph_format.keep_with_next=False
        block_start=p
        cursor=p.getprevious()
        while cursor is not None and cursor.tag==qn('w:p'):
            prior=Paragraph(cursor,d._body)
            if prior.style.name.startswith('Heading') or (not prior.text and not cursor.xpath('.//w:drawing') and not cursor.xpath('.//w:sectPr')):
                block_start=cursor;cursor=cursor.getprevious()
            else:break
        if wide:
            # Section properties describe the block preceding the break paragraph.
            prev=block_start.getprevious()
            if prev is not None:section_break(d,prev,False)
            section_break(d,caption._p,True)
        elif index in SEQUENCES|ACTIVITIES or len(panel_shapes)>1:
            Paragraph(block_start,d._body).paragraph_format.page_break_before=True
    for i,paragraph in enumerate(d.paragraphs[:-1]):
        if paragraph.text.startswith(('2.5 Biểu đồ trình tự pha phân tích','2.8 Kết luận chương')) and paragraph.style.name.startswith('Heading'):
            d.paragraphs[i+1].paragraph_format.keep_together=True
    after=snapshot(d)
    expected=[changed_captions.get(t,t) for t in before['paragraphs']]
    actual=[t for t in after['paragraphs'] if t not in added_text]
    assert actual==expected,'Unexpected prose changes'
    assert after['tables']==before['tables'],'Unexpected table changes'
    assert doc_images(d)[:8]==doc_images(Document(TARGET))[:8]
    d.save(WORK/'candidate.docx')
    state.update(changed_captions=changed_captions,added_continuation_captions=added_text,placements=placements,before_content=before,expected_content=after,output_images=len(d.inline_shapes))
    (WORK/'state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Candidate assembled: {len(manifest)} figures; {len(d.inline_shapes)} inline pictures; prose and {len(d.tables)} tables preserved.')

def verify(finalize=False):
    from pypdf import PdfReader
    import pdfplumber
    state=json.loads((WORK/'state.json').read_text('utf-8'))
    assert sha(SOURCE)==state['source_sha256'],'fix1 was modified'
    final=WORK/'render/corrected.docx';d=Document(final)
    assert snapshot(d)==state['expected_content'],'Rendered text/table drift'
    assert len(d.inline_shapes)==state['output_images']
    assert doc_images(d)[:8]==doc_images(Document(WORK/'original-target.docx'))[:8]
    with pdfplumber.open(WORK/'render/corrected.pdf') as pdf:
        blank=[]
        for n,page in enumerate(pdf.pages,1):
            if len((page.extract_text() or '').split())<3:blank.append(n)
            for im in page.images:
                assert im['x0']>=-1 and im['x1']<=page.width+1 and im['top']>=-1 and im['bottom']<=page.height+1,('Image out of page',n)
        state['pages']=len(pdf.pages);state['sparse_pages']=blank
    if finalize:
        assert not state['sparse_pages'],state['sparse_pages']
        assert sha(TARGET)==state['target_sha256_before'],'Target edited concurrently'
        shutil.copy2(final,TARGET)
        assert sha(TARGET)==sha(final)
        state['target_sha256_final']=sha(TARGET);state['finalized']=True
    (WORK/'state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'fix1_unchanged':True,'prose_tables_preserved':True,'figures':33,'pictures':len(d.inline_shapes),'pages':state['pages'],'sparse_pages':state['sparse_pages'],'finalized':state.get('finalized',False)},ensure_ascii=False))

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='assets':assets()
    elif mode=='assemble':assemble()
    elif mode=='verify':verify()
    elif mode=='finalize':verify(True)
