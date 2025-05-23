import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io
import zipfile

st.title("처리의 랜덤 도트 PDF 생성기 (ZIP)")

# 사용자 입력 파라미터
num_dots = st.number_input("점 개수", min_value=5, max_value=100, value=30)
min_dist = st.number_input("점 간 최소 거리(인치)", min_value=0.1, max_value=3.0, value=1.5, step=0.1)
margin = st.number_input("가장자리 여백(인치)", min_value=0.1, max_value=3.0, value=0.5, step=0.1)
num_pdfs = st.number_input("PDF 개수 (최대 10개)", min_value=1, max_value=10, value=10)

a4_width, a4_height = 8.27, 11.69

def is_far_enough(new_dot, dots, min_dist):
    for dot in dots:
        if np.hypot(new_dot[0] - dot[0], new_dot[1] - dot[1]) < min_dist:
            return False
    return True

if st.button("PDF 생성 및 ZIP 다운로드"):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for i in range(num_pdfs):
            dots = []
            attempts = 0
            max_attempts = num_dots * 100
            while len(dots) < num_dots and attempts < max_attempts:
                x = np.random.uniform(margin, a4_width - margin)
                y = np.random.uniform(margin, a4_height - margin)
                if is_far_enough((x, y), dots, min_dist):
                    dots.append((x, y))
                attempts += 1
            if len(dots) < num_dots:
                st.warning(f"{i+1}번째 PDF: {num_dots}개 점을 모두 배치하지 못했습니다. 실제 배치: {len(dots)}개")
            
            # PDF를 메모리 내에 저장
            pdf_buffer = io.BytesIO()
            fig, ax = plt.subplots(figsize=(a4_width, a4_height))
            ax.scatter(*zip(*dots), color='black')
            ax.set_xlim(0, a4_width)
            ax.set_ylim(0, a4_height)
            ax.axis('off')
            with PdfPages(pdf_buffer) as pdf:
                pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
            pdf_buffer.seek(0)
            
            # ZIP 파일에 PDF 추가
            zip_file.writestr(f'random_dots_a4_spaced_{i+1}.pdf', pdf_buffer.read())
    
    zip_buffer.seek(0)
    st.download_button(
        label="ZIP 파일 다운로드",
        data=zip_buffer,
        file_name="random_dots_pdfs.zip",
        mime="application/zip"
    )
