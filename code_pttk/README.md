# CẤU TRÚC THƯ MỤC DỰ ÁN PTTKHTTT - NHÓM 10 (`code_pttk`)

Thư mục này chứa toàn bộ tài liệu báo cáo, mã nguồn sơ đồ (Mermaid, PlantUML), hình ảnh kết xuất và các script tự động hóa cho bài tập lớn học phần **Phân tích và Thiết kế Hệ thống Thông tin** (Đề tài: *Hệ thống quản lý nhà hàng Thanh Hoa*).

---

## Sơ đồ tổ chức thư mục

```text
code_pttk/
├── docs/                               # Tài liệu báo cáo Word, văn bản trích xuất & đề bài
│   ├── PTTKHTTT N10.docx               # Báo cáo chính thức Nhóm 10
│   ├── N13_Nhom10.docx                 # Báo cáo tổng hợp Nhóm 10
│   ├── Dat_ban_bao_cao_wireframe_table.docx
│   ├── extracted_doc.txt               # Nội dung text trích xuất từ báo cáo
│   └── de_bai_4-11.jpg                 # Ảnh đề bài
│
├── chucnang/                           # Tài liệu & sơ đồ chi tiết theo từng module chức năng
│   ├── menu/                           # Chức năng Quản lý thực đơn & Tạo combo (Lê Việt Hoàng)
│   │   ├── phantich/                   # Sơ đồ lớp & tuần tự pha Phân tích (.mermaid)
│   │   ├── thietke/                    # Sơ đồ lớp & tuần tự pha Thiết kế (.mermaid)
│   │   ├── images/                     # Ảnh chụp màn hình giao diện thực đơn & combo
│   │   ├── KICH_BAN_TAO_COMBO.md       # Đặc tả kịch bản tạo combo
│   │   └── README.md
│   ├── chon_ban_va_dat_mon/            # Chức năng Chọn bàn & Đặt món (Phan Việt Bảo)
│   │   ├── Activity Diagram1.jpg
│   │   ├── Class Diagram - Pha thiết kế_ Chọn bàn và đặt món.jpg
│   │   ├── ERD Nha hang Thanh Hoa.jpg
│   │   └── Sequence Diagram - Chọn bàn và đặt món.jpg
│   └── gop_don/                        # Chức năng Gộp đơn hàng (Ngô Văn Phương)
│       ├── diagram/                    # Mã nguồn sơ đồ lớp Phân tích & Thiết kế (.mermaid, .puml)
│       └── README.md
│
├── src/                                # Mã nguồn sơ đồ cấp hệ thống & phân hệ (Menu, Order, Thanh toán)
│   ├── mermaid/                        # Mã nguồn Mermaid (.mermaid)
│   └── puml/                           # Mã nguồn PlantUML (.puml) chuẩn style Visual Paradigm
│
├── diagrams/                           # Toàn bộ hình ảnh sơ đồ đã kết xuất & tài nguyên ảnh
│   ├── generated/                      # Ảnh sơ đồ sinh tự động từ Python script (Sequence, Component, Deployment, ERD)
│   ├── puml_out/                       # Ảnh PNG xuất ra từ PlantUML (src/puml & chucnang/gop_don)
│   ├── system/                         # Ảnh sơ đồ kiến trúc hệ thống (Thành phần & Triển khai)
│   └── extracted_media/                # Tài nguyên ảnh trích xuất từ báo cáo phục vụ tạo file Word
│
└── scripts/                            # Các công cụ Python tự động hóa vẽ sơ đồ và xuất báo cáo
    ├── generate_diagrams.py            # Vẽ các biểu đồ trình tự (Sequence Diagram) chuẩn Visual Paradigm
    ├── gen_component_vp.py             # Vẽ biểu đồ thành phần (Component Diagram) chuẩn Visual Paradigm
    └── build_thiet_ke_docx.py          # Tự động đóng gói báo cáo Phần III: Tài liệu thiết kế (.docx)
```
