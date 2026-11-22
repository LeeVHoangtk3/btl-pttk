#!/usr/bin/env python3
"""validate_vp.py - kiem tra tinh toan ven tham chieu cua file XML Visual Paradigm.

Dung:  python3 validate_vp.py file.xml [file2.xml ...]
Thoat 0 neu khong co loi; 1 neu co loi. Chay lai tren file export that cung cho 0 loi.
"""
import sys
import xml.etree.ElementTree as ET

REF_ATTRS = ['From', 'To', 'Model', 'MetaModelElement', 'EndModelElement', 'EndRelationshipFromMetaModelElement',
             'EndRelationshipToMetaModelElement', 'ToActivation', 'FromActivation', 'ForeignKey', 'RefColumn',
             'ParentFrame', 'VerticalPartitionId']


def check(path):
    errs, warns = [], []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return ['XML khong hop le: %s' % e], []
    if root.tag != 'Project':
        errs.append('Root phai la <Project>, hien la <%s>' % root.tag)
    for need in ('ProjectInfo', 'Models', 'Diagrams'):
        if root.find(need) is None:
            errs.append('Thieu <%s>' % need)
    ids = {}
    for e in root.iter():
        i = e.get('Id')
        if i is not None:
            if i in ids:
                errs.append('Id trung: %s (<%s> va <%s>)' % (i, ids[i], e.tag))
            ids[i] = e.tag
    mv_children = set()
    for mv in root.iter('MasterView'):
        for c in mv:
            mv_children.add(id(c))
    for e in root.iter():
        i = e.get('Idref')
        if id(e) in mv_children:
            continue
        if i is not None and i not in ids and e.tag != 'EAViewpointProperty':
            errs.append('Idref khong ton tai: %s trong <%s Name="%s">' % (i, e.tag, e.get('Name')))
        for a in REF_ATTRS:
            v = e.get(a)
            if v and v not in ids:
                errs.append('Thuoc tinh %s="%s" tro toi Id khong ton tai (<%s Name="%s">)' % (a, v, e.tag, e.get('Name')))
    models, diagrams = root.find('Models'), root.find('Diagrams')
    if models is not None and diagrams is not None:
        shape_ids = set()
        for dg in diagrams:
            for sec in ('Shapes', 'Connectors'):
                s = dg.find(sec)
                if s is not None:
                    for e in s.iter():
                        if e.get('Id'):
                            shape_ids.add(e.get('Id'))
        # MasterView phai tro toi shape/connector
        for mv in models.iter('MasterView'):
            for c in mv:
                if c.get('Idref') not in shape_ids:
                    warns.append('MasterView <%s> Idref=%s khong phai shape/connector (VP van chap nhan neu diagram da bi xoa)' % (c.tag, c.get('Idref')))
        # shape.Model phai la model co MasterView tro nguoc lai
        back = {}
        for mv in models.iter('MasterView'):
            owner = None
        for el in models.iter():
            mv = el.find('MasterView')
            if mv is not None and el.get('Id'):
                for c in mv:
                    back.setdefault(c.get('Idref'), el.get('Id'))
        for dg in diagrams:
            for sec in ('Shapes', 'Connectors'):
                s = dg.find(sec)
                if s is None:
                    continue
                for e in s.iter():
                    m = e.get('Model')
                    if m and back.get(e.get('Id')) != m:
                        warns.append('Shape <%s Name="%s"> tro toi model %s nhung model khong co MasterView tro lai' %
                                     (e.tag, e.get('Name'), m))
                    if sec == 'Connectors' and e.get('From'):
                        for k in ('From', 'To'):
                            if e.get(k) not in shape_ids:
                                errs.append('Connector <%s> %s=%s khong phai Id cua shape' % (e.tag, k, e.get(k)))
    return errs, warns


def main():
    bad = 0
    for p in sys.argv[1:]:
        errs, warns = check(p)
        print('==', p, '->', 'OK' if not errs else '%d LOI' % len(errs), '(%d canh bao)' % len(warns))
        for e in errs[:40]:
            print('  LOI:', e)
        for w in warns[:10]:
            print('  canh bao:', w)
        bad += bool(errs)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
