from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).parent/'render'
pdf=pdfium.PdfDocument(root/'report.pdf')
for i,page in enumerate(pdf):
    im=page.render(scale=1.5).to_pil().convert('RGB')
    im.save(root/f'page-{i+1}.png')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
for start in range(0,len(pdf),6):
    sheet=Image.new('RGB',(1350,1920),'#dddddd')
    d=ImageDraw.Draw(sheet)
    for j in range(start,min(start+6,len(pdf))):
        im=Image.open(root/f'page-{j+1}.png');im.thumbnail((440,600))
        x=((j-start)%3)*450;y=((j-start)//3)*960
        sheet.paste(im,(x,y+35));d.text((x+10,y+5),str(j+1),font=font,fill='black')
    sheet.save(root/f'contact-{start//6+1}.png')
print(f'{len(pdf)} pages rendered')
