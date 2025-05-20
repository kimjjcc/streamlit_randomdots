import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# A4 크기 (인치)
a4_width, a4_height = 8.27, 11.69

# 파라미터
num_dots = 30         # 점 개수
min_dist = 1.5         # 점 사이 최소 거리 (인치)
margin = 0.5           # 가장자리 여백 (인치)
num_pdfs = 10          # 생성할 PDF 개수

def is_far_enough(new_dot, dots, min_dist):
    for dot in dots:
        if np.hypot(new_dot[0] - dot[0], new_dot[1] - dot[1]) < min_dist:
            return False
    return True

for i in range(num_pdfs):
    dots = []
    attempts = 0
    max_attempts = num_dots * 100  # 무한루프 방지

    while len(dots) < num_dots and attempts < max_attempts:
        x = np.random.uniform(margin, a4_width - margin)
        y = np.random.uniform(margin, a4_height - margin)
        if is_far_enough((x, y), dots, min_dist):
            dots.append((x, y))
        attempts += 1

    if len(dots) < num_dots:
        print(f"Warning: {num_dots}개 점을 배치할 수 없습니다. 실제 배치된 점 개수: {len(dots)}")

    # PDF로 저장
    fig, ax = plt.subplots(figsize=(a4_width, a4_height))
    ax.scatter(*zip(*dots), color='black')
    ax.set_xlim(0, a4_width)
    ax.set_ylim(0, a4_height)
    ax.axis('off')

    pdf_filename = f'random_dots_a4_spaced_{i+1}.pdf'
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig(fig, bbox_inches='tight')

    plt.close(fig)

print(f"{num_pdfs}개의 PDF 파일이 생성되었습니다.")
