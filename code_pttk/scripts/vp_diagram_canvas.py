"""Deterministic SVG drawing primitives matched to the supplied VP screenshots.

This module does not use the former XML skill or add vendor export branding.
"""
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import ImageFont
import heapq, math, textwrap

VP_BLUE='#7ACFF5'
VP_BORDER='#000000'
VP_TEXT='#000000'
VP_BG_WHITE='#FFFFFF'
FONT='C:/Windows/Fonts/arial.ttf'

class Canvas:
    def __init__(self,w,h):
        self.w,self.h=w,h
        self.items=[]
        self.boxes=[]
    def rect(self,x,y,w,h,fill=VP_BLUE,rx=0,stroke=VP_BORDER):
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.25"/>')
    def ellipse(self,x,y,rx,ry,fill=VP_BLUE):
        self.items.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="black" stroke-width="1.25"/>')
    def text(self,x,y,value,size=18,bold=False,anchor='middle',back=False,italic=False):
        lines=str(value).split('\n')
        for i,line in enumerate(lines):
            yy=y+i*(size+5)
            if back:
                width=ImageFont.truetype(FONT,size).getlength(line)+10
                self.rect(x-width/2,yy-size,width,size+5,'white',stroke='none')
            self.items.append(f'<text x="{x}" y="{yy}" text-anchor="{anchor}" font-family="Arial" font-size="{size}" font-weight="{"bold" if bold else "normal"}" font-style="{"italic" if italic else "normal"}" fill="black">{escape(line)}</text>')
    def line(self,pts,arrow=False,dash=False,kind=None):
        p=' '.join(f'{x},{y}' for x,y in pts)
        self.items.append(f'<polyline points="{p}" fill="none" stroke="black" stroke-width="1.25"'+(' stroke-dasharray="6 4"' if dash else '')+'/>')
        if arrow or kind:
            a,b=pts[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0]); length=15 if kind=='generalization' else 10
            left=(b[0]-length*math.cos(ang-.43),b[1]-length*math.sin(ang-.43));right=(b[0]-length*math.cos(ang+.43),b[1]-length*math.sin(ang+.43))
            if kind=='generalization':
                self.items.append(f'<polygon points="{b[0]},{b[1]} {left[0]},{left[1]} {right[0]},{right[1]}" fill="white" stroke="black" stroke-width="1.25"/>')
            else:self.line([left,b,right])
    def actor(self,x,y,label):
        self.ellipse(x,y,10,10)
        self.line([(x,y+10),(x,y+38)])
        self.line([(x-18,y+23),(x+18,y+23)])
        self.line([(x-16,y+61),(x,y+38),(x+16,y+61)])
        self.text(x,y+85,label,18)
    def initial(self,x,y,final=False):
        if final:self.ellipse(x,y,10,10,'white')
        self.ellipse(x,y,6,6,'black')
    def diamond(self,x,y,r=15):
        self.items.append(f'<polygon points="{x},{y-r} {x+r},{y} {x},{y+r} {x-r},{y}" fill="{VP_BLUE}" stroke="black" stroke-width="1.25"/>')
    def node(self,x,y,w,title,fields=(),methods=(),kind='class',size=18):
        font=ImageFont.truetype(FONT,size)
        def wrap(value):
            words=str(value).replace('(', '( ').split();result=[];line=''
            if len(words)>1 and words[0] in ('+','-','#'):words=[words[0]+' '+words[1]]+words[2:]
            for word in words:
                trial=(line+' '+word).strip()
                if line and font.getlength(trial)>w-20:result.append(line);line='  '+word
                else:line=trial
            result.append(line)
            return result
        ff=[l for f in fields for l in wrap(f)]
        mm=[l for m in methods for l in wrap(m)]
        if kind in ('boundary','control'):
            # Native VP uses robustness icons with operations below the icon.
            h=math.ceil((95+(len(ff)+len(mm))*(size+5))/10)*10
            cx=x+w/2;cy=y+19
            self.ellipse(cx,cy,16,16)
            if kind=='boundary':
                self.line([(cx-31,cy-18),(cx-31,cy+18)])
                self.line([(cx-31,cy),(cx-16,cy)])
            else:self.line([(cx+5,cy-21),(cx-6,cy-16),(cx+3,cy-11)])
            self.text(cx,y+63,title,size,True)
            yy=y+92
            for value in ff+mm:self.text(x+6,yy,value,size,anchor='start');yy+=size+5
            box=(x,y,w,h);self.boxes.append(box);return box
        if kind=='erd':
            # The reference ERD uses an orange header and white row separators.
            h=math.ceil((32+len(fields)*24+8)/10)*10
            self.rect(x,y,w,h,'#F4B777',rx=7)
            self.text(x+w/2,y+23,title,17)
            for j,value in enumerate(fields):
                yy=y+32+j*24
                self.line([(x,yy),(x+w,yy)])
                # Use a white row rule, as in the native export.
                self.items[-1]=self.items[-1].replace('stroke="black"','stroke="white"')
                field,datatype=value.split(' : ',1)
                pk=field.startswith('PK');fk='FK ' in field
                field=field.replace('PK/FK ','').replace('PK ','').replace('FK ','')
                fs=16
                while ImageFont.truetype(FONT,fs).getlength(field)>w*.56-27:fs-=1
                if pk:
                    self.ellipse(x+11,yy+8,3,3,'#FFD21A')
                    self.line([(x+11,yy+11),(x+11,yy+20),(x+15,yy+20)])
                if fk:
                    self.items.append(f'<path d="M {x+4},{yy+5} L {x+15},{yy+5} L {x+15},{yy+15}" stroke="#479b40" stroke-width="2" fill="none"/><polygon points="{x+12},{yy+12} {x+18},{yy+12} {x+15},{yy+18}" fill="#479b40"/>')
                if not pk and not fk:
                    self.rect(x+5,yy+5,10,15,'#e7f5ff')
                    self.line([(x+8,yy+9),(x+13,yy+9)]);self.line([(x+8,yy+13),(x+13,yy+13)])
                self.text(x+21,yy+18,field,fs,pk,anchor='start',italic=fk)
                self.text(x+w*.58,yy+18,datatype,14,pk,anchor='start',italic=fk)
            box=(x,y,w,h);self.boxes.append(box);return box
        hh=34+(len(ff)+len(mm))*(size+5)+(12 if ff else 0)+(12 if mm else 0)
        if kind=='enum':hh+=24
        if kind in ('boundary','control'):hh+=40
        h=math.ceil(max(60,hh)/10)*10
        fill='#F4B777' if kind=='erd' else VP_BLUE
        self.rect(x,y,w,h,fill,rx=7 if kind=='erd' else 0)
        yy=y+24
        if kind=='enum':self.text(x+w/2,yy,'«enumeration»',size-2);yy+=24
        if kind in ('boundary','control'):
            self.text(x+w/2,yy,'«'+kind+'»',size-2);yy+=24
        self.text(x+w/2,yy,title,size,True,italic=title in ('MenuItem','Order','Payment'))
        yy+=10;self.line([(x,yy),(x+w,yy)])
        yy+=size+5
        for value in ff:self.text(x+10,yy,value,size,anchor='start');yy+=size+5
        if mm:
            self.line([(x,yy-size+3),(x+w,yy-size+3)])
            yy+=6
            for value in mm:self.text(x+10,yy,value,size,anchor='start');yy+=size+5
        box=(x,y,w,h)
        self.boxes.append(box)
        return box
    def save(self,path):
        Path(path).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}"><rect width="100%" height="100%" fill="white"/>'+''.join(self.items)+'</svg>',encoding='utf-8')

def graph(path, specs, edges, cols=3, box_w=300, font=18, row_gap=90, clearance=30):
    """Route all relations in gutters using A*, never across a class body."""
    gap=90;left=70;top=60
    nodes={};kinds={s['name']:s.get('kind','class') for s in specs};rows=[];y=top
    c=Canvas(1,1)
    for first in range(0,len(specs),cols):
        batch=specs[first:first+cols];heights=[]
        for j,s in enumerate(batch):
            box=c.node(left+j*(box_w+gap),y,box_w,s['name'],s.get('fields',[]),s.get('methods',[]),s.get('kind','class'),font)
            nodes[s['name']]=box;heights.append(box[3])
        y+=max(heights)+row_gap
    c.w=left*2+cols*box_w+(cols-1)*gap;c.h=y-row_gap+top
    shape_items=c.items;c.items=[]
    # Reserve distinct connector ports when many relations touch a class.
    requirements={}
    planned=[]
    for edge in edges:
        a,b=edge[:2];kind=edge[2] if len(edge)>2 else 'association'
        if a not in nodes or b not in nodes:continue
        aa,bb=nodes[a],nodes[b]
        dx=bb[0]-aa[0];dy=bb[1]-aa[1]
        if abs(dx)>abs(dy):sa,sb=('r','l') if dx>0 else ('l','r')
        else:sa,sb=('b','t') if dy>0 else ('t','b')
        if len(edge)>3 and edge[3]:sa,sb=edge[3]
        if kinds[a] in ('boundary','control'):sa='r'
        if kinds[b] in ('boundary','control'):sb='l'
        for key in [(a,sa),(b,sb)]:requirements[key]=requirements.get(key,0)+1
        planned.append((a,b,kind,sa,sb,edge[4:] if len(edge)>4 else []))
    used={};occupied={}
    step=10
    nx,ny=math.ceil(c.w/step),math.ceil(c.h/step)
    blocked=set()
    for name,(x,y,w,h) in nodes.items():
        obstacles=[(x,y,w,h)]
        if kinds[name] in ('boundary','control'):obstacles=[(x,y+48,w,h-48),(x+w/2-20,y,40,36)]
        for bx,by,bw,bh in obstacles:
            for xx in range(max(0,int((bx-12)//step)),min(nx,int((bx+bw+12)//step)+1)):
                for yy in range(max(0,int((by-12)//step)),min(ny,int((by+bh+12)//step)+1)):blocked.add((xx,yy))
    def port(name,side):
        key=(name,side);n=used.get(key,0)+1;used[key]=n
        x,y,w,h=nodes[name];t=n/(requirements[key]+1)
        if kinds[name] in ('boundary','control'):
            p=(x+w/2+(-16 if side=='l' else 16),y+19)
            q=(round((p[0]+(-35 if side=='l' else 35))/step)*step,round(p[1]/step)*step)
            return p,q
        if side in ('l','r'):t=(round((y+h*t)/step)*step-y)/h
        else:t=(round((x+w*t)/step)*step-x)/w
        if side in ('l','r'):p=(x if side=='l' else x+w,y+h*t);q=(p[0]+(-clearance if side=='l' else clearance),p[1])
        else:p=(x+w*t,y if side=='t' else y+h);q=(p[0],p[1]+(-clearance if side=='t' else clearance))
        q=(round(q[0]/step)*step,round(q[1]/step)*step)
        return p,q
    def route(a,b):
        start=tuple(round(v/step) for v in a);end=tuple(round(v/step) for v in b)
        queue=[(0,0,start,None)];best={(start,None):0};prev={};final=None
        while queue:
            _,cost,p,direction=heapq.heappop(queue)
            if p==end:final=(p,direction);break
            if cost!=best.get((p,direction)):continue
            for di,(dx,dy) in enumerate(((1,0),(0,1),(-1,0),(0,-1))):
                q=(p[0]+dx,p[1]+dy)
                if not(1<=q[0]<nx and 1<=q[1]<ny):continue
                if q in blocked and q not in (start,end):continue
                nc=cost+1+(4 if direction is not None and direction!=di else 0)+occupied.get(q,0)*4
                key=(q,di)
                if nc<best.get(key,1e12):
                    best[key]=nc;prev[key]=(p,direction)
                    heapq.heappush(queue,(nc+abs(end[0]-q[0])+abs(end[1]-q[1]),nc,q,di))
        if final is None:raise ValueError(f'No clear route: {a} -> {b}')
        path=[];state=final
        while state in prev:path.append(state[0]);state=prev[state]
        path.append(start);path.reverse()
        for p in path:occupied[p]=occupied.get(p,0)+1
        result=[]
        for p in path:
            pt=(p[0]*step,p[1]*step)
            if len(result)>1 and (result[-2][0]==result[-1][0]==pt[0] or result[-2][1]==result[-1][1]==pt[1]):result[-1]=pt
            else:result.append(pt)
        return result
    for a,b,kind,sa,sb,labels in planned:
        pa,qa=port(a,sa);pb,qb=port(b,sb)
        middle=route(qa,qb)
        # Bridge exact ports to the grid with orthogonal segments.
        bend_a=(qa[0],pa[1]) if sa in 'lr' else (pa[0],qa[1])
        bend_b=(qb[0],pb[1]) if sb in 'lr' else (pb[0],qb[1])
        pts=[pa,bend_a,qa]+middle[1:-1]+[qb,bend_b,pb]
        pts=[p for j,p in enumerate(pts) if j==0 or p!=pts[j-1]]
        c.line(pts,arrow=kind in ('dependency','arrow'),dash=kind in ('dependency','erd'),kind='generalization' if kind=='generalization' else None)
        if kind=='erd':
            end_labels=labels or ['1','0..*']
            for p,q,label in [(pa,qa,end_labels[0]),(pb,qb,end_labels[1])]:
                c.text((p[0]+q[0])/2+8,(p[1]+q[1])/2-7,label,14)
        elif labels:
            for text,p,q in zip(labels,(pa,pb),(qa,qb)):c.text((p[0]+q[0])/2+8,(p[1]+q[1])/2-8,text,14)
    c.items+=shape_items
    c.save(path)
    return {'width':c.w,'height':c.h,'nodes':len(nodes),'edges':len(planned)}
