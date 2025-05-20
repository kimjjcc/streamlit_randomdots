import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io

# Streamlit 앱 제목
st.title("랜덤 도트 PDF 생성기")

# 사용자 입력 파라미터
num_dots = st.number_input("점 개수", min_value=5, max_value=100, value=30)
min_dist = st.number_input("점 간 최소 거리(인치)", min_value=0.1, max_value=3.0, value=1.5, step=0.1)
margin = st.number_input("가장자리 여백(인치)", min_value=0.1, max_value=3.0, value=0.5, step=0.1)
num_pdfs = st.number_input("PDF 개수", min_value=1, max_value=20, value=10)

a4_width, a4_height = 8.27, 11.69

def is_far_enough(new_dot, dots, min_dist):
    for dot in dots:
        if np.hypot(new_dot[0] - dot[0], new_dot[1] - dot[1]) < min_dist:
            return False
    return True

if st.button("PDF 생성 및 다운로드"):
    buffer = io.BytesIO()
    with PdfPages(buffer) as pdf:
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
            fig, ax = plt.subplots(figsize=(a4_width, a4_height))
            ax.scatter(*zip(*dots), color='black')
            ax.set_xlim(0, a4_width)
            ax.set_ylim(0, a4_height)
            ax.axis('off')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
    buffer.seek(0)
    st.download_button(
        label="PDF 다운로드",
        data=buffer,
        file_name="random_dots.pdf",
        mime="application/pdf"
    )
