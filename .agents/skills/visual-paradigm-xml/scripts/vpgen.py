#!/usr/bin/env python3
"""vpgen.py - sinh file XML (Visual Paradigm "Project" XML, ExporterVersion 16.1.1)
tu mot JSON spec don gian, de import bang  File > Import > ... XML  trong Visual Paradigm.

Dung:
    python3 vpgen.py spec.json -o out.xml
Xem references/spec-format.md de biet cau truc spec.

Nguyen tac cot loi (rut ra tu cac file export that):
  * Moi phan tu model co Id 16 ky tu; shape/connector tren diagram co Id RIENG va
    tro ve model bang  Model= / MetaModelElement=.
  * Model.<MasterView> liet ke Idref cua cac shape/connector (khong phai Id cua model).
  * Connector.From / To la Id cua SHAPE; relationship model.From / To la Id cua MODEL.
  * Thuoc tinh XML duoc sap xep theo ASCII (giong VP).
"""
import argparse, copy, datetime, html, json, math, os, random, string, sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')
T = json.load(open(os.path.join(ASSETS, 'attr_templates.json'), encoding='utf8'))
HEADER = open(os.path.join(ASSETS, 'project_header.tmpl'), encoding='utf8').read()

ID_CHARS = string.ascii_letters + string.digits + '_'
PRIO = {'Stereotypes': 0, 'ActionType': 1, 'CoveredLifeLines': 1, 'SubDiagrams': 1, 'ModelChildren': 2,
        'Activations': 2, 'Messages': 2, 'ForeignKeyConstraints': 2, 'Guard': 3, 'VerticalPartitions': 3,
        'FromSimpleRelationships': 4, 'ToSimpleRelationships': 5, 'FromEnd': 6, 'ToEnd': 7, 'MasterView': 9}
BLUE = 'rgb(122, 207, 245)'
ORANGE = 'rgb(245, 182, 122)'
INT_MIN = '-2147483648'


def tw(s, k=7, pad=14, mn=20):
    return max(int(len(s or '') * k + pad), mn)


class Diagram(ET.Element):
    pass


class Gen:
    def __init__(self, spec):
        self.spec = spec
        p = spec.get('project', {})
        self.pname = p.get('name', 'Project')
        self.author = p.get('author', 'SinhVien')
        n = datetime.datetime.now()
        self.now = n.strftime('%Y-%m-%dT%H:%M:%S.') + '%03d' % (n.microsecond // 1000)
        self.ids = set()
        self.z = 0
        self.models = ET.Element('Models')
        self.diagrams = ET.Element('Diagrams')
        self.reg = {}          # (kind, name) -> model Element
        self.rel_containers = {}
        self.rel_root = None
        self.stereo = {}
        self.uses_orm = False
        for n_ in ['boolean', 'byte', 'char', 'double', 'float', 'int', 'long', 'short', 'void', 'string']:
            self.models.append(self.mk('m:DataType', Name=n_))

    # ---------- primitives ----------
    def nid(self):
        while True:
            i = ''.join(random.choice(ID_CHARS) for _ in range(16))
            if i not in self.ids:
                self.ids.add(i)
                return i

    def mk(self, key, **over):
        tag = key.split(':')[-1]
        a = copy.deepcopy(T[key][0])
        a.pop('Documentation', None)
        if 'Documentation_plain' in a:
            a['Documentation_plain'] = ''
        known = set(a)
        for k, v in over.items():
            if v is not None and (k in known or k + '_IsNull' in known or k in ('Documentation',)):
                a.pop(k + '_IsNull', None)
                a[k] = str(v).lower() if isinstance(v, bool) else str(v)
        for k in ('FromActivation', 'ToActivation', 'ParentFrame', 'ForeignKey', 'RefColumn'):
            if k not in over:
                a.pop(k, None)
        if 'Id' in a:
            a['Id'] = over.get('Id') or self.nid()
        if 'PmAuthor' in a:
            a['PmAuthor'] = self.author
        if 'PmCreateDateTime' in a:
            a['PmCreateDateTime'] = self.now
        if 'PmLastModified' in a:
            a['PmLastModified'] = self.now
        return ET.Element(tag, a)

    def doc(self, el, text):
        if text:
            el.set('Documentation', '<HTML><BODY><p style="margin-top: 0">%s</p></BODY></HTML>' % html.escape(text))
            el.set('Documentation_plain', text)

    def sub(self, parent, tag, **a):
        return ET.SubElement(parent, tag, {k: str(v) for k, v in a.items()})

    def ref(self, parent, tag, el_or_id, name=''):
        i = el_or_id.get('Id') if isinstance(el_or_id, ET.Element) else el_or_id
        return self.sub(parent, tag, Idref=i, Name=name)

    def mv(self, model_el, tag, shape_id, name='', mvtag=None):
        tag = mvtag or tag
        m = model_el.find('MasterView')
        if m is None:
            m = ET.SubElement(model_el, 'MasterView')
        if tag in ('Generalization', 'Dependency', 'InteractionLifeLineLink', 'Realization'):
            self.sub(m, tag, Idref=shape_id)       # VP khong ghi Name cho cac loai nay
        else:
            self.ref(m, tag, shape_id, name or '')

    def children(self, el):
        c = el.find('ModelChildren')
        return c if c is not None else ET.SubElement(el, 'ModelChildren')

    def rel_container(self, kind):
        if self.rel_root is None:
            self.rel_root = self.mk('m:ModelRelationshipContainer', Name='relationships')
            self.sub(self.rel_root, 'ModelChildren')
            self.models.append(self.rel_root)
        if kind not in self.rel_containers:
            c = self.mk('m:ModelRelationshipContainer', Name=kind)
            self.sub(c, 'ModelChildren')
            self.rel_root.find('ModelChildren').append(c)
            self.rel_containers[kind] = c
        return self.rel_containers[kind].find('ModelChildren')

    def stereotype(self, name, base):
        k = (name, base)
        if k not in self.stereo:
            s = self.mk('m:Stereotype', Name=name, BaseType=base)
            self.models.append(s)
            self.stereo[k] = s
        return self.stereo[k]

    def nz(self):
        self.z += 2
        return self.z

    # ---------- diagram / shape / connector building ----------
    def new_diagram(self, dtag, name, **over):
        d0 = self.mk('d:' + dtag, Name=name, **over)
        d = Diagram(d0.tag, d0.attrib)
        d.set('PmAuthor', self.author)
        for k in ('PmCreateDateTime', 'PmLastModified'):
            d.set(k, self.now)
        self.diagrams.append(d)
        d.shapes = ET.SubElement(d, 'Shapes')
        d.conns = ET.SubElement(d, 'Connectors')
        d.sh = {}   # name -> dict(id,x,y,w,h)
        return d

    def deco(self, el, cap, fill=BLUE, transp=0, comp=False, stroke='1.0'):
        self.sub(el, 'ElementFont', Color='rgb(0, 0, 0)', Name='Dialog', Size='11', Style='0')
        ln = self.sub(el, 'Line', Cap='0', Color='rgb(0, 0, 0)', Transparency='0', Weight=stroke)
        ET.SubElement(ln, 'Stroke')
        self.sub(el, 'Caption', Height=cap['h'], InternalHeight=INT_MIN, InternalWidth=INT_MIN,
                 Side=cap.get('side', 'None'), Visible=cap.get('vis', 'true'), Width=cap['w'],
                 X=cap['x'], Y=cap['y'])
        if fill:
            self.sub(el, 'FillColor', Color=fill, Style='1', Transparency=transp, Type='1')
        if comp:
            self.sub(el, 'CompartmentFont', Value='none')

    def shape(self, d, key, model, name, x, y, w, h, parent=None, cap_side='FreeMove', fill=BLUE,
              transp=0, comp=False, cap_h=15, cap_pos=None, mvtag=None, **over):
        sid = self.nid()
        mid = model.get('Id') if model is not None else None
        a = dict(Id=sid, Name=name, X=int(x), Y=int(y), Width=int(w), Height=int(h), ZOrder=self.nz())
        if mid:
            a.update(MetaModelElement=mid, Model=mid)
        a.update(over)
        el = self.mk('s:%s:%s' % (d.tag, key), **a)
        for k in ('MetaModelElement', 'Model'):
            if k in el.attrib and not mid:
                del el.attrib[k]
        (parent if parent is not None else d.shapes).append(el)
        cx, cy = cap_pos if cap_pos else (x, y)
        self.deco(el, dict(h=cap_h, w=w, x=int(cx), y=int(cy), side=cap_side,
                           vis='false' if cap_side == 'Invisible' else 'true'), fill, transp, comp)
        d.sh[name if name not in d.sh else '%s#%s' % (name, sid)] = dict(id=sid, x=x, y=y, w=w, h=h, el=el)
        if model is not None:
            self.mv(model, key, sid, name, mvtag)
        return sid

    @staticmethod
    def edge(a, b):
        ax, ay = a['x'] + a['w'] / 2, a['y'] + a['h'] / 2
        bx, by = b['x'] + b['w'] / 2, b['y'] + b['h'] / 2
        dx, dy = bx - ax, by - ay
        if dx == 0 and dy == 0:
            return ax, ay
        sx = (a['w'] / 2) / abs(dx) if dx else 1e9
        sy = (a['h'] / 2) / abs(dy) if dy else 1e9
        t = min(sx, sy)
        return round(ax + dx * t), round(ay + dy * t)

    def connector(self, d, key, model, name, fs, ts, pts=None, extra=None, assoc_ends=None, **over):
        """fs/ts: dict shape (co 'id'). pts: list (x,y) hoac None -> tu tinh."""
        if pts is None:
            if fs is ts:
                x, y, w, h = fs['x'], fs['y'], fs['w'], fs['h']
                pts = [(x + 40, y), (x + 40, y - 40), (x + w + 50, y - 40), (x + w + 50, y + h / 2), (x + w, y + h / 2)]
            else:
                pts = [self.edge(fs, ts), self.edge(ts, fs)]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        cid = self.nid()
        a = dict(Id=cid, From=fs['id'], To=ts['id'], X=int(min(xs) - 50), Y=int(min(ys) - 50),
                 Width=int(max(xs) - min(xs) + 100), Height=int(max(ys) - min(ys) + 100), ZOrder=self.nz())
        if model is not None:
            a.update(MetaModelElement=model.get('Id'), Model=model.get('Id'))
        if name or name == '':
            a['Name'] = name
        a.update(over)
        if extra:
            a.update(extra)
        el = self.mk('c:%s:%s' % (d.tag, key), **a)
        if not name and 'Name' in el.attrib and key not in ('Association',):
            pass
        d.conns.append(el)
        mx, my = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        if assoc_ends:
            ma, mb = assoc_ends
            self.sub(el, 'MultiplicityBRectangle', Height=40, Width=40, X=int(pts[-1][0] - 20), Y=int(pts[-1][1] - 20))
            self.sub(el, 'MultiplicityARectangle', Height=40, Width=40, X=int(pts[0][0] - 20), Y=int(pts[0][1] - 20))
        cw = tw(name) if name else 20
        self.deco(el, dict(h=15 if name else 0, w=cw, x=int(mx - cw / 2), y=int(my - 21), side='None'), fill=None)
        if assoc_ends:
            ra = self.sub(el, 'RoleA')
            self.sub(ra, 'MultiplicityCaption', Height=40, Width=40, X=int(pts[0][0] - 20), Y=int(pts[0][1] - 20))
            rb = self.sub(el, 'RoleB')
            self.sub(rb, 'MultiplicityCaption', Height=40, Width=40, X=int(pts[-1][0] - 20), Y=int(pts[-1][1] - 20))
        pe = self.sub(el, 'Points')
        for (px, py) in pts:
            self.sub(pe, 'Point', X='%.1f' % px, Y='%.1f' % py)
        if model is not None:
            self.mv(model, key, cid, name or '')
        return cid, el

    @staticmethod
    def grid(i, n, cw=240, ch=170, x0=60, y0=60, cols=None):
        cols = cols or max(1, math.ceil(math.sqrt(n)))
        return x0 + (i % cols) * cw, y0 + (i // cols) * ch

    # ================= CLASS =================
    def class_el(self, c):
        k = ('class', c['name'])
        if k in self.reg:
            return self.reg[k]
        el = self.mk('m:Class', Name=c['name'], Visibility=c.get('visibility', 'public'),
                     Abstract=c.get('abstract', False))
        self.doc(el, c.get('documentation'))
        st = c.get('stereotype')
        if st:
            s = self.stereotype(st, 'Class')
            self.ref(self.sub(el, 'Stereotypes'), 'Stereotype', s, st)
        mc = self.sub(el, 'ModelChildren')
        for a in c.get('attributes', []):
            ae = self.mk('m:Attribute', Name=a['name'], Type=a.get('type', 'String'),
                         Visibility=a.get('visibility', 'private'), Scope='classifier' if a.get('static') else 'instance',
                         Multiplicity=a.get('multiplicity', 'Unspecified'))
            self.doc(ae, a.get('documentation'))
            mc.append(ae)
        for o in c.get('operations', []):
            oe = self.mk('m:Operation', Name=o['name'], ReturnType=o.get('returnType', 'void'),
                         Visibility=o.get('visibility', 'public'), Static=o.get('static', False),
                         Abstract=o.get('abstract', False), Scope='classifier' if o.get('static') else 'instance')
            self.doc(oe, o.get('documentation'))
            pc = self.sub(oe, 'ModelChildren')
            for p in o.get('params', []):
                pc.append(self.mk('m:Parameter', Name=p['name'], Type=p.get('type', 'String'),
                                  Direction=p.get('direction', 'in')))
            if not len(pc):
                oe.remove(pc)
            mc.append(oe)
        if not len(mc):
            el.remove(mc)
        self.models.append(el)
        self.reg[k] = el
        return el

    def class_size(self, c):
        st = c.get('stereotype')
        if st in ('boundary', 'control', 'entity'):
            return 80, 40
        na, no = len(c.get('attributes', [])), len(c.get('operations', []))
        texts = [c['name']] + ['- %s : %s' % (a['name'], a.get('type', '')) for a in c.get('attributes', [])] + \
                ['+ %s()' % o['name'] for o in c.get('operations', [])]
        w = max(80, max(len(t) for t in texts) * 7 + 20)
        h = max(38, 23 + 15 * (na + no) + (8 if na and no else 0)) + (11 if st else 0)
        return w, h

    def build_class(self, d):
        dg = self.new_diagram('ClassDiagram', d['name'])
        self.uses_orm = True
        classes = d.get('classes', [])
        for i, c in enumerate(classes):
            known = ('class', c['name']) in self.reg
            full = c if (not known or c.get('attributes') or c.get('operations') or c.get('stereotype')) else \
                {'name': c['name']}
            el = self.class_el(full)
            if known and not (c.get('attributes') or c.get('operations')):
                # lay lai thong tin kich thuoc tu model
                full = dict(c)
            w, h = self.class_size(c)
            x, y = (c['x'], c['y']) if 'x' in c else self.grid(i, len(classes), 260, 200)
            icon = c.get('stereotype') in ('boundary', 'control', 'entity')
            self.shape(dg, 'Class', el, c['name'], x, y, w, h, cap_side='South' if (icon or c.get('stereotype')) else 'FreeMove',
                       comp=True, cap_h=30 if c.get('stereotype') else 15,
                       cap_pos=(x - 4, y + h) if icon else None)
        for r in d.get('relationships', []):
            self.class_rel(dg, r)

    def class_rel(self, dg, r):
        kind = r.get('kind', 'association')
        fc, tc = self.reg[('class', r['from'])], self.reg[('class', r['to'])]
        fs, ts = dg.sh[r['from']], dg.sh[r['to']]
        name = r.get('name', '')
        k = (kind, r['from'], r['to'], name)
        if kind == 'generalization':
            el = self.reg.get(k)
            if el is None:
                el = self.mk('m:Generalization', From=fc.get('Id'), To=tc.get('Id'))   # From = con, To = cha
                self.rel_container('Generalization').append(el)
                self.ref(self.sub_once(fc, 'FromSimpleRelationships'), 'Generalization', el)
                self.ref(self.sub_once(tc, 'ToSimpleRelationships'), 'Generalization', el)
                self.reg[k] = el
            self.connector(dg, 'Generalization', el, None, fs, ts)
            return
        el = self.reg.get(k)
        if el is None:
            el = self.mk('m:Association', Name=name, EndRelationshipFromMetaModelElement=fc.get('Id'),
                         EndRelationshipToMetaModelElement=tc.get('Id'), Direction='From To')
            for side, cls, m, nav, agg in (
                    ('FromEnd', fc, r.get('fromMultiplicity', 'Unspecified'), r.get('fromNavigable', 'Unspecified'),
                     {'aggregation': 'Shared', 'composition': 'Composite'}.get(kind, 'None')),
                    ('ToEnd', tc, r.get('toMultiplicity', 'Unspecified'), r.get('toNavigable', 'Navigable'), 'None')):
                end = self.sub(el, side)
                ae = self.mk('m:AssociationEnd', EndModelElement=cls.get('Id'), Multiplicity=m, Navigable=nav,
                             AggregationKind=agg)
                if side == 'FromEnd' and r.get('fromRole'):
                    ae.set('Name', r['fromRole'])
                if side == 'ToEnd' and r.get('toRole'):
                    ae.set('Name', r['toRole'])
                end.append(ae)
                q = self.sub(ae, 'Qualifier')
                q.append(self.mk('m:Qualifier'))
                self.ref(self.sub(ae, 'Type'), 'Class', cls, cls.get('Name'))
            self.rel_container('Association').append(el)
            self.reg[k] = el
        has_m = any(r.get(x) for x in ('fromMultiplicity', 'toMultiplicity'))
        ex = dict(HasMultiplicityAShape='true', HasMultiplicityBShape='true') if has_m else {}
        # chon bien the connector co RoleA/RoleB khi co multiplicity
        self.connector(dg, 'Association', el, name, fs, ts, extra=ex, assoc_ends=(1, 1) if has_m else None)

    def sub_once(self, el, tag):
        e = el.find(tag)
        return e if e is not None else ET.SubElement(el, tag)

    # ================= STATE =================
    def build_state(self, d):
        dg = self.new_diagram('StateDiagram', d['name'])
        nodes = []
        if d.get('initial', True):
            nodes.append(('InitialPseudoState', 'initial', ''))
        for s in d.get('states', []):
            nodes.append(('State2', s['name'], s))
        for f in d.get('finals', []):
            nodes.append(('FinalState2', f if isinstance(f, str) else f['name'], {}))
        els = {}
        for i, (tag, name, s) in enumerate(nodes):
            nm = '' if tag == 'InitialPseudoState' else name
            el = self.mk('m:' + tag, Name=nm)
            if tag == 'State2':
                self.doc(el, s.get('documentation'))
            self.models.append(el)
            els[name] = el
            if 'x' in s if isinstance(s, dict) else False:
                x, y = s['x'], s['y']
            else:
                x, y = 50 + i * 250, 170
            if tag == 'State2':
                w, h = max(160, tw(name, 8, 40)), 50
                self.shape(dg, tag, el, nm, x, y, w, h, cap_side='None', cap_h=15)
            else:
                self.shape(dg, tag, el, nm, x, y, 20, 20, cap_side='None', cap_h=0 if tag == 'InitialPseudoState' else 15,
                           fill='rgb(0, 0, 0)')
            dg.sh['@' + name] = dg.sh[nm]
        for t in d.get('transitions', []):
            fn = 'initial' if t['from'] in ('initial', '[*]') else t['from']
            tn = t['to']
            fe, te = els[fn], els[tn]
            tr = self.mk('m:Transition2', From=fe.get('Id'), To=te.get('Id'), Name=t.get('name', ''), Kind='External')
            self.rel_container('Transition2').append(tr)
            self.ref(self.sub_once(fe, 'FromSimpleRelationships'), 'Transition2', tr, t.get('name', ''))
            self.ref(self.sub_once(te, 'ToSimpleRelationships'), 'Transition2', tr, t.get('name', ''))
            self.connector(dg, 'Transition2', tr, t.get('name', ''), dg.sh['@' + fn], dg.sh['@' + tn])

    # ================= SEQUENCE / COMMUNICATION =================
    def _seq_data(self, d):
        parts = {}
        for i, p in enumerate(d['participants']):
            kind = p.get('kind', 'lifeline')
            w = 60 if kind == 'actor' else max(90, tw(p['name'], 7, 24))
            parts[p['name']] = dict(spec=p, kind=kind, cx=120 + i * 230, w=w, acts=[], stack=[])
        ycur = 130
        rows = []
        msgs = d['messages']
        counter = 0

        def new_act(pt, y, caller=None):
            a = dict(mid=self.nid(), sid=self.nid(), part=pt, y0=y, y1=y, caller=caller)
            pt['acts'].append(a)
            pt['stack'].append(a)
            return a

        def touch(a, y):
            if a:
                a['y0'] = min(a['y0'], y)
                a['y1'] = max(a['y1'], y)
        for idx, m in enumerate(msgs):
            kind = m.get('kind', 'call')
            s, t = parts[m['from']], parts[m['to']]
            y = ycur
            ycur += 70 if kind == 'self' else 50
            counter += 1 if kind != 'self' or True else 0
            if kind == 'return':
                af = s['stack'][-1] if s['stack'] else None
                at = af['caller'] if af else None
                nxt = msgs[idx + 1] if idx + 1 < len(msgs) else None
                if af and not (nxt and nxt.get('kind') == 'return' and nxt['from'] == m['from']):
                    s['stack'].pop()
            elif kind == 'self':
                af = s['stack'][-1] if s['stack'] else (new_act(s, y) if s['kind'] == 'lifeline' else None)
                at = af
            else:
                af = s['stack'][-1] if s['stack'] else (new_act(s, y) if s['kind'] == 'lifeline' else None)
                at = new_act(t, y, af) if t['kind'] == 'lifeline' else None
            touch(af, y)
            touch(at, y + (26 if kind == 'self' else 0))
            rows.append(dict(m=m, kind=kind, y=y, af=af, at=at, s=s, t=t, seq=m.get('seq') or str(counter)))
        return parts, rows, ycur

    def build_sequence(self, d, comm=False):
        parts, rows, yend = self._seq_data(d)
        frame = self.mk('m:Frame', Name=d.get('frame', d['name']), Type='sd', BaseY='40')
        self.models.append(frame)
        fmc = self.sub(frame, 'ModelChildren')
        dg = self.new_diagram('CommunicationDiagram' if comm else 'InteractionDiagram', d['name'])
        height = yend + 60
        # ---- model: participants
        for nm, pt in parts.items():
            sp = pt['spec']
            if pt['kind'] == 'actor':
                pt['el'] = self.mk('m:InteractionActor', Name=nm)
            else:
                pt['el'] = self.mk('m:InteractionLifeLine', Name=nm)
                if sp.get('stereotype'):
                    s = self.stereotype(sp['stereotype'], 'InteractionLifeLine')
                    self.ref(self.sub(pt['el'], 'Stereotypes'), 'Stereotype', s, sp['stereotype'])
                if pt['acts']:
                    ac = self.sub(pt['el'], 'Activations')
                    for a in pt['acts']:
                        ae = self.mk('m:Activation', Id=a['mid'])
                        ac.append(ae)
                        a['el'] = ae
            fmc.append(pt['el'])
        # ---- model: messages
        links = {}
        for r in rows:
            m = r['m']
            s, t = r['s'], r['t']
            over = dict(Name=m['text'], SequenceNumber=r['seq'], EndRelationshipFromMetaModelElement=s['el'].get('Id'),
                        EndRelationshipToMetaModelElement=t['el'].get('Id'),
                        Type='Self Message' if r['kind'] == 'self' else 'Message',
                        Asynchronous=r['kind'] == 'async')
            if r['af']:
                over['FromActivation'] = r['af']['mid']
            if r['at']:
                over['ToActivation'] = r['at']['mid']
            me = self.mk('m:Message', **over)
            if r['kind'] == 'return':
                at_ = self.sub(me, 'ActionType')
                at_.append(self.mk('m:ActionTypeReturn'))
            fe, te = self.sub(me, 'FromEnd'), self.sub(me, 'ToEnd')
            fe.append(self.mk('m:MessageEnd', EndModelElement=s['el'].get('Id')))
            te.append(self.mk('m:MessageEnd', EndModelElement=t['el'].get('Id')))
            r['el'] = me
            if comm:
                key = tuple(sorted([m['from'], m['to']]))
                if key not in links:
                    f, t_ = (m['from'], m['to'])
                    le = self.mk('m:InteractionLifeLineLink', EndRelationshipFromMetaModelElement=parts[f]['el'].get('Id'),
                                 EndRelationshipToMetaModelElement=parts[t_]['el'].get('Id'))
                    for side, nme in (('FromEnd', f), ('ToEnd', t_)):
                        e = self.sub(le, side)
                        e.append(self.mk('m:InteractionLifeLineLinkEnd', EndModelElement=parts[nme]['el'].get('Id')))
                    self.sub(le, 'ModelChildren')
                    self.rel_container('InteractionLifeLineLink').append(le)
                    links[key] = dict(el=le, f=f, t=t_)
                links[key]['el'].find('ModelChildren').append(me)
                r['link'] = links[key]
            else:
                self.rel_container('Message').append(me)
        # ---- model: combined fragments
        frags = []
        for fg in d.get('fragments', []):
            covered = []
            for i in range(fg['from'], fg['to'] + 1):
                for nm in (rows[i]['m']['from'], rows[i]['m']['to']):
                    if parts[nm]['kind'] == 'lifeline' and nm not in covered:
                        covered.append(nm)
            fe = self.mk('m:CombinedFragment', Name='', OperatorKind=fg.get('operator', 'alt'))
            cl = self.sub(fe, 'CoveredLifeLines')
            for nm in covered:
                self.ref(cl, 'InteractionLifeLine', parts[nm]['el'], nm)
            fmc2 = self.sub(fe, 'ModelChildren')
            ops = []
            for k, op in enumerate(fg['operands']):
                oe = self.mk('m:InteractionOperand', Name='Operand' if k == 0 else 'Operand%d' % (k + 1))
                ms = self.sub(oe, 'Messages')
                for i in range(op['from'], op['to'] + 1):
                    self.ref(ms, 'Message', rows[i]['el'], rows[i]['m']['text'])
                g = self.sub(oe, 'Guard')
                if op.get('guard'):
                    g.append(self.mk('m:InteractionConstraint', Constraint=op['guard']))
                    g[-1].attrib.pop('Constraint_IsNull', None)
                else:
                    g.append(self.mk('m:InteractionConstraint'))
                fmc2.append(oe)
                ops.append((oe, op))
            fmc.append(fe)
            frags.append((fe, fg, covered, ops))
        # ---- diagram shapes
        sid = {}
        if comm:
            return self._comm_shapes(dg, parts, rows, links, frame)
        for fe, fg, covered, ops in frags:
            xs0 = min(parts[n]['cx'] - parts[n]['w'] / 2 for n in covered) - 20
            xs1 = max(parts[n]['cx'] + parts[n]['w'] / 2 for n in covered) + 20
            y0 = rows[fg['from']]['y'] - 30
            y1 = rows[fg['to']]['y'] + (70 if rows[fg['to']]['kind'] == 'self' else 40)
            starts = [rows[op['from']]['y'] - 30 for _, op in ops] + [y1]
            starts[0] = y0
            for k, (oe, op) in enumerate(ops):
                self.shape(dg, 'InteractionOperand', oe, oe.get('Name'), xs0, starts[k], xs1 - xs0, starts[k + 1] - starts[k],
                           cap_side='Invisible', cap_h=starts[k + 1] - starts[k])
                dg.sh['op:%s' % oe.get('Id')] = dg.sh[oe.get('Name')]
            fg['_box'] = (xs0, y0, xs1 - xs0, y1 - y0, fe)
        for pt in parts.values():
            for a in pt['acts']:
                self.shape(dg, 'Activation', a['el'], 'Activation', pt['cx'] - 4, a['y0'], 8, max(a['y1'] - a['y0'] + 30, 40),
                           cap_side='Invisible', fill=BLUE, cap_pos=(pt['cx'] - 4, a['y0'] + 4))
                a['shape'] = dg.sh['Activation'] if 'Activation' in dg.sh else None
                a['sdict'] = dict(id=dg.shapes[-1].get('Id'))
                dg.sh.pop('Activation', None)
        for fe, fg, covered, ops in frags:
            x, y, w, h, fe_ = fg['_box']
            self.shape(dg, 'CombinedFragment', fe_, '', x, y, w, h, cap_side='FreeMove', cap_h=18, transp=100,
                       fill='rgba(122, 207, 245, 0.0)', cap_pos=(0, 0))
        fid = frame.get('Id')
        for nm, pt in parts.items():
            if pt['kind'] == 'actor':
                sidv = self.shape(dg, 'InteractionActor', pt['el'], nm, pt['cx'] - 30, 40, 60, height - 40, cap_side='None',
                                  cap_pos=(pt['cx'] - 32, 75), ParentFrame=fid)
            else:
                sidv = self.shape(dg, 'InteractionLifeLine', pt['el'], nm, pt['cx'] - pt['w'] / 2, 40, pt['w'], height - 40,
                                  cap_side='South', cap_pos=(pt['cx'] - pt['w'] / 2, 75), ParentFrame=fid, ShowClassifier='true')
            pt['sid'] = sidv
        # ---- connectors (messages)
        for r in rows:
            s, t = r['s'], r['t']
            y = r['y']
            if r['kind'] == 'self':
                x = s['cx'] + 4
                pts = [(x, y), (x + 48, y), (x + 48, y + 26), (x, y + 26)]
            else:
                right = t['cx'] > s['cx']
                xs_ = s['cx'] + (4 if right else -4) if r['af'] else s['cx']
                xe_ = t['cx'] - (4 if right else -4) if r['at'] else t['cx']
                pts = [(xs_, y), (xe_, y)]
            fsd = dict(id=s['sid'])
            tsd = dict(id=t['sid'])
            self.connector(dg, 'Message', r['el'], r['m']['text'], fsd, tsd, pts=pts)

    def _comm_shapes(self, dg, parts, rows, links, frame):
        n = len(parts)
        for i, (nm, pt) in enumerate(parts.items()):
            x, y = (pt['spec']['x'], pt['spec']['y']) if 'x' in pt['spec'] else (80 + (i % 3) * 300, 80 + (i // 3) * 220)
            if pt['kind'] == 'actor':
                pt['sid'] = self.shape(dg, 'CommunicationActor', pt['el'], nm, x, y, 30, 60, cap_side='South', cap_pos=(x - 30, y + 60), mvtag='InteractionActor')
            else:
                w = max(79, tw(nm, 7, 24))
                pt['sid'] = self.shape(dg, 'CommunicationLifeLine', pt['el'], nm, x, y, w, 40, cap_side='South',
                                       cap_pos=(x, y + 40), mvtag='InteractionLifeLine')
            pt['box'] = dict(id=pt['sid'], x=x, y=y, w=30 if pt['kind'] == 'actor' else max(79, tw(nm, 7, 24)),
                             h=60 if pt['kind'] == 'actor' else 40)
        for key, lk in links.items():
            fb, tb = parts[lk['f']]['box'], parts[lk['t']]['box']
            cid, cel = self.connector(dg, 'InteractionLifeLineLink', lk['el'], None, fb, tb)
            cel.attrib.pop('Name', None)
            kids = self.sub(cel, 'DiagramElementChildren')
            cel.remove(kids)
            cel.insert(list(cel).index(cel.find('Points')), kids)
            pa, pb = self.edge(fb, tb), self.edge(tb, fb)
            msgs = [r for r in rows if r.get('link') is lk]
            for j, r in enumerate(msgs):
                fwd = r['m']['from'] == lk['f']
                key_ = 'CommunicationMessage' if fwd else 'CommunicationReverseMessage'
                mx = (pa[0] + pb[0]) / 2 - 30
                my = (pa[1] + pb[1]) / 2 + 20 * j - 30
                text = '%s: %s' % (r['seq'], r['m']['text'])
                a = dict(Id=self.nid(), MetaModelElement=r['el'].get('Id'), Model=r['el'].get('Id'), Name=r['m']['text'],
                         X=int(mx), Y=int(my), Width=60, Height=60, ZOrder=self.nz())
                me = self.mk('c:CommunicationDiagram:' + key_, **a)
                kids.append(me)
                self.deco(me, dict(h=15, w=tw(text), x=int(mx - 30), y=int(my - 8), side='None'), fill='rgb(0, 0, 0)')
                self.mv(r['el'], 'Message', a['Id'], r['m']['text'])

    # ================= PACKAGE =================
    def build_package(self, d):
        wrapper = self.mk('m:Model', Name=d['name'])
        self.models.append(wrapper)
        dg = self.new_diagram('PackageDiagram', d['name'])
        self.sub(self.sub(wrapper, 'SubDiagrams'), 'PackageDiagram', Idref=dg.get('Id'))
        mc = self.sub(wrapper, 'ModelChildren')
        pk = {}
        for p in d['packages']:
            el = self.mk('m:Package', Name=p['name'])
            pk[p['name']] = (el, p)
            parent = pk[p['parent']][0] if p.get('parent') else wrapper
            self.children(parent).append(el)
        tops = [n for n, (e, p) in pk.items() if not p.get('parent')]
        shape_parent = {}
        for i, n in enumerate(tops):
            el, p = pk[n]
            kids = [k for k, (e, q) in pk.items() if q.get('parent') == n]
            x, y = (p['x'], p['y']) if 'x' in p else self.grid(i, len(tops), 280, 220)
            w = max(140, tw(n, 8, 30)) if not kids else max(300, 140 * len(kids) + 40)
            h = 60 if not kids else 160
            sid = self.shape(dg, 'Package', el, n, x, y, w, h, cap_side='FreeMove')
            shape_parent[n] = dg.sh[n]
            if kids:
                dec = self.sub(dg.sh[n]['el'], 'DiagramElementChildren')
                dg.sh[n]['el'].remove(dec)
                dg.sh[n]['el'].insert(list(dg.sh[n]['el']).index(dg.sh[n]['el'].find('FillColor')), dec)
                for j, k in enumerate(kids):
                    kel, kp = pk[k]
                    self.shape(dg, 'Package', kel, k, x + 20 + j * 140, y + 50, 120, 60, parent=dec, cap_side='FreeMove')
        for dep in d.get('dependencies', []):
            fe, te = pk[dep['from']][0], pk[dep['to']][0]
            de = self.mk('m:Dependency', From=fe.get('Id'), To=te.get('Id'), Name=dep.get('name', ''))
            self.rel_container('Dependency').append(de)
            self.ref(self.sub_once(fe, 'FromSimpleRelationships'), 'Dependency', de)
            self.ref(self.sub_once(te, 'ToSimpleRelationships'), 'Dependency', de)
            self.connector(dg, 'Dependency', de, dep.get('name', ''), dg.sh[dep['from']], dg.sh[dep['to']])

    # ================= ER =================
    def build_er(self, d):
        dg = self.new_diagram('ERDiagram', d['name'])
        self.uses_orm = True
        tabs = {}
        for i, t in enumerate(d['tables']):
            el = self.mk('m:DBTable', Name=t['name'])
            mc = self.sub(el, 'ModelChildren')
            cols = {}
            for c in t.get('columns', []):
                ce = self.mk('m:DBColumn', Name=c['name'], Type=c.get('type', 'integer'),
                             PrimaryKey=bool(c.get('pk')), Nullable=bool(c.get('nullable', not c.get('pk'))),
                             Unique=bool(c.get('unique')), Length=c.get('length', 10))
                mc.append(ce)
                cols[c['name']] = ce
            self.models.append(el)
            x, y = (t['x'], t['y']) if 'x' in t else self.grid(i, len(d['tables']), 260, 220)
            w = max(110, max([len(c['name']) + len(c.get('type', 'integer')) for c in t.get('columns', [])] + [8]) * 8 + 40)
            h = 40 + 20 * max(len(t.get('columns', [])), 1)
            self.shape(dg, 'DBTable', el, t['name'], x, y, w, h, fill=ORANGE, comp=True)
            tabs[t['name']] = dict(el=el, cols=cols, spec=t)
        fk_proto = next((v for v in T['m:DBColumn'] if 'IdGenerator' in v), T['m:DBColumn'][0])
        for fk in d.get('foreignKeys', []):
            parent, child = tabs[fk['from']], tabs[fk['to']]   # from = bang tham chieu (PK), to = bang giu FK
            pkcol = fk.get('refColumn') or next((n for n, c in parent['cols'].items() if c.get('PrimaryKey') == 'true'), None)
            fe = self.mk('m:DBForeignKey', From=parent['el'].get('Id'), To=child['el'].get('Id'),
                         FromMultiplicity=fk.get('fromMultiplicity', '1'), ToMultiplicity=fk.get('toMultiplicity', '0..*'),
                         Identifying=bool(fk.get('identifying')), Name=fk.get('name', ''))
            self.rel_container('DBForeignKey').append(fe)
            colname = fk.get('column') or (fk['from'] + (pkcol[0].upper() + pkcol[1:] if pkcol else 'Id'))
            ce = self.mk('m:DBColumn', Name=colname, Type=parent['cols'][pkcol].get('Type', 'integer') if pkcol else 'integer',
                         Nullable=bool(fk.get('nullable', True)))
            for k, v in fk_proto.items():
                if k in ('ForeignKeyNamePattern', 'IdGenerator'):
                    ce.set(k, v)
            ce.attrib.pop('ForeignKeyNamePattern_IsNull', None)
            ce.attrib.pop('IdGenerator_IsNull', None)
            fc = self.sub(ce, 'ForeignKeyConstraints')
            fc.append(self.mk('m:DBForeignKeyConstraint', ForeignKey=fe.get('Id'),
                              RefColumn=parent['cols'][pkcol].get('Id') if pkcol else ''))
            self.children(child['el']).append(ce)
            self.ref(self.sub_once(parent['el'], 'FromSimpleRelationships'), 'DBForeignKey', fe)
            self.ref(self.sub_once(child['el'], 'ToSimpleRelationships'), 'DBForeignKey', fe)
            self.connector(dg, 'DBForeignKey', fe, '', dg.sh[fk['from']], dg.sh[fk['to']])

    # ================= DEPLOYMENT =================
    def build_deployment(self, d):
        wrapper = self.mk('m:Model', Name=d['name'])
        self.models.append(wrapper)
        dg = self.new_diagram('DeploymentDiagram', d['name'])
        self.sub(self.sub(wrapper, 'SubDiagrams'), 'DeploymentDiagram', Idref=dg.get('Id'))
        self.sub(wrapper, 'ModelChildren')
        els = {}
        for i, n in enumerate(d['nodes']):
            ne = self.mk('m:Node', Name=n['name'])
            self.children(wrapper).append(ne)
            els[n['name']] = ne
            kids = n.get('children', [])
            for k in kids:
                tag = 'Component' if k.get('kind', 'component') == 'component' else 'Artifact'
                ke = self.mk('m:' + tag, Name=k['name'])
                self.children(ne).append(ke)
                els[k['name']] = ke
            x, y = (n['x'], n['y']) if 'x' in n else self.grid(i, len(d['nodes']), 320, 260)
            w, h = max(220, 150 * len(kids) + 40), 200
            self.shape(dg, 'Node', ne, n['name'], x, y, w, h, comp=True)
            if kids:
                dec = self.sub(dg.sh[n['name']]['el'], 'DiagramElementChildren')
                nel = dg.sh[n['name']]['el']
                nel.remove(dec)
                nel.insert(list(nel).index(nel.find('FillColor')), dec)
                for j, k in enumerate(kids):
                    tag = 'Component' if k.get('kind', 'component') == 'component' else 'Artifact'
                    self.shape(dg, tag, els[k['name']], k['name'], x + 20 + j * 150, y + 60, 130, 70, parent=dec,
                               cap_side='InsideNorth' if tag == 'Component' else 'FreeMove', comp=(tag == 'Component'))
        for a in d.get('associations', []):
            fe, te = els[a['from']], els[a['to']]
            ae = self.mk('m:Association', Name=a.get('name', ''), EndRelationshipFromMetaModelElement=fe.get('Id'),
                         EndRelationshipToMetaModelElement=te.get('Id'), Direction='From To')
            for side, el_ in (('FromEnd', fe), ('ToEnd', te)):
                e = self.sub(ae, side)
                x_ = self.mk('m:AssociationEnd', EndModelElement=el_.get('Id'))
                e.append(x_)
                q = self.sub(x_, 'Qualifier')
                q.append(self.mk('m:Qualifier'))
                tag = el_.tag
                self.ref(self.sub(x_, 'Type'), tag, el_, el_.get('Name'))
            self.rel_container('Association').append(ae)
            self.connector(dg, 'Association', ae, a.get('name', ''), dg.sh[a['from']], dg.sh[a['to']])
        for a in d.get('dependencies', []):
            fe, te = els[a['from']], els[a['to']]
            de = self.mk('m:Dependency', From=fe.get('Id'), To=te.get('Id'), Name=a.get('name', ''))
            self.rel_container('Dependency').append(de)
            self.ref(self.sub_once(fe, 'FromSimpleRelationships'), 'Dependency', de)
            self.ref(self.sub_once(te, 'ToSimpleRelationships'), 'Dependency', de)
            self.connector(dg, 'Dependency', de, a.get('name', ''), dg.sh[a['from']], dg.sh[a['to']])

    # ================= ACTIVITY (chi cac node co mau that) =================
    def build_activity(self, d):
        dg = self.new_diagram('ActivityDiagram', d['name'])
        for i, a in enumerate(d.get('actions', [])):
            el = self.mk('m:ActivityAction', Name=a['name'])
            self.models.append(el)
            x, y = (a['x'], a['y']) if 'x' in a else (60 + i * 140, 60)
            self.shape(dg, 'ActivityAction', el, a['name'], x, y, max(60, tw(a['name'], 7, 20)), 40, cap_side='Center', cap_h=40,
                       cap_pos=(0, 0))
        for i, o in enumerate(d.get('objectNodes', [])):
            el = self.mk('m:ObjectNode', Name=o['name'])
            self.models.append(el)
            x, y = (o['x'], o['y']) if 'x' in o else (60 + i * 140, 200)
            self.shape(dg, 'ObjectNode', el, o['name'], x, y, 80, 40, cap_side='FreeMove', cap_pos=(0, 0))

    # ---------- finish ----------
    def build(self):
        fn = dict(class_=self.build_class, state=self.build_state, sequence=self.build_sequence,
                  communication=lambda d: self.build_sequence(d, comm=True), package=self.build_package,
                  er=self.build_er, deployment=self.build_deployment, activity=self.build_activity)
        for d in self.spec['diagrams']:
            t = d['type'].replace('class', 'class_') if d['type'] == 'class' else d['type']
            fn[t](d)

    @staticmethod
    def order(el):
        kids = list(el)
        if any(c.tag in PRIO for c in kids):
            kids.sort(key=lambda c: PRIO.get(c.tag, 5))
            for c in list(el):
                el.remove(c)
            for c in kids:
                el.append(c)
        for c in el:
            Gen.order(c)

    @staticmethod
    def sort_attrs(el):
        items = sorted(el.attrib.items())
        el.attrib.clear()
        el.attrib.update(items)
        for c in el:
            Gen.sort_attrs(c)

    def xml(self):
        self.build()
        self.order(self.models)
        for dg in self.diagrams:
            for sec in list(dg):
                if sec.tag in ('Shapes', 'Connectors') and not len(sec):
                    dg.remove(sec)
        for root in (self.models, self.diagrams):
            self.sort_attrs(root)
        orm = '<OrmInfo DefaultDatabase="1" SupportDatabases="0"/>\n\t\t' if self.uses_orm else ''
        head = (HEADER.replace('{NAME}', html.escape(self.pname, quote=True))
                .replace('{AUTHOR}', html.escape(self.author, quote=True)).replace('{ORMINFO}', orm))
        out = [head]
        for root in (self.models, self.diagrams):
            ET.indent(root, space='\t', level=1)
            out.append('\t' + ET.tostring(root, encoding='unicode') + '\n')
        out.append('</Project>\n')
        return ''.join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('spec')
    ap.add_argument('-o', '--out', default='project.xml')
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding='utf8'))
    xml = Gen(spec).xml()
    open(a.out, 'w', encoding='utf8', newline='\n').write(xml)
    print('Da ghi', a.out, '(%d bytes)' % len(xml.encode('utf8')))


if __name__ == '__main__':
    main()
