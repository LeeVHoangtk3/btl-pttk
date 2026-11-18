"""
gen_all_diagrams.py - Master Script to generate all UML diagrams for the assignment
Produces all diagrams matching Visual Paradigm Community Edition styling into ../diagrams/
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))

from gen_usecase import generate_usecase_diagram
from gen_class_analysis import generate_analysis_class_diagram
from gen_class_design import generate_design_class_diagram
from gen_communication_lanes import generate_all_swimlane_comm
from gen_package_spec import generate_spec_package_diagram
from gen_deployment_spec import generate_spec_deployment_diagram

def generate_all():
    diagrams_dir = os.path.join(os.path.dirname(__file__), '..', 'diagrams')
    os.makedirs(diagrams_dir, exist_ok=True)
    
    print("=" * 60)
    print("BẮT ĐẦU TẠO TẤT CẢ BIỂU ĐỒ UML (CHUẨN VISUAL PARADIGM)...")
    print("=" * 60)
    
    print("\n[1/6] Tạo Biểu đồ Ca sử dụng (Câu 1.a)...")
    generate_usecase_diagram(os.path.join(diagrams_dir, 'cau1a_usecase.png'))
    
    print("\n[2/6] Tạo Biểu đồ Lớp phân tích (Câu 2.b)...")
    generate_analysis_class_diagram(os.path.join(diagrams_dir, 'cau2b_class_analysis.png'))
    
    print("\n[3/6] Tạo Biểu đồ Lớp thiết kế BCE (Câu 3.a)...")
    generate_design_class_diagram(os.path.join(diagrams_dir, 'cau3a_class_design.png'))
    
    print("\n[4/6] Tạo Biểu đồ Giao tiếp Communication Diagrams 4-lane (Câu 3.b)...")
    generate_all_swimlane_comm()
    
    print("\n[5/6] Tạo Biểu đồ Gói Package Diagram Specification & Realization (Câu 5.a)...")
    generate_spec_package_diagram(os.path.join(diagrams_dir, 'cau5a_package.png'))
    
    print("\n[6/6] Tạo Biểu đồ Triển khai Deployment Diagram 3D + Artifacts (Câu 5.b)...")
    generate_spec_deployment_diagram(os.path.join(diagrams_dir, 'cau5b_deployment_j2ee.png'))
    
    print("\n" + "=" * 60)
    print("HOÀN TẤT TẠO TOÀN BỘ BIỂU ĐỒ UML CHUẨN VISUAL PARADIGM!")
    print(f"Toàn bộ ảnh lưu tại: {diagrams_dir}")
    print("=" * 60)

if __name__ == '__main__':
    generate_all()
