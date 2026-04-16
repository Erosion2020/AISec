"""
从 PDF 中提取指定页码范围的文字内容。
用法：python extract_pdf_pages.py <pdf_path> <start_page> <end_page>
页码从 1 开始（调用方负责在用户页码基础上加封面偏移量）。

提取策略：
1. 用 pdfplumber 提取文字层
2. 提取结果做乱码检测：若可读字符比例过低，标注"建议手动复制"
3. 完全空页（公式截图等）直接标注"建议手动复制"
"""

import sys
import re


# 乱码判断：可读字符（中文、英文字母、数字、常见标点）占比低于此阈值时视为乱码
READABLE_RATIO_THRESHOLD = 0.4


def is_garbled(text: str) -> bool:
    """
    判断提取的文字是否为乱码。
    策略：统计中文字符、ASCII 可读字符的比例，低于阈值则认为乱码。
    """
    if not text:
        return False
    total = len(text)
    # 中文、英文字母、数字、常见标点、空白
    readable = len(re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef'
                              r'a-zA-Z0-9\s\.,!?;:，。！？；：、""''（）【】《》]', text))
    return (readable / total) < READABLE_RATIO_THRESHOLD


def extract(pdf_path: str, start_page: int, end_page: int):
    try:
        import pdfplumber
    except ImportError:
        print("ERROR: pdfplumber 未安装，请先运行：pip install pdfplumber "
              "--index-url https://pypi.tuna.tsinghua.edu.cn/simple")
        sys.exit(1)

    results = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        if start_page < 1 or end_page > total:
            print(f"ERROR: 页码超出范围，该 PDF 共 {total} 页（含封面等）")
            sys.exit(1)

        for i in range(start_page - 1, end_page):
            page_num = i + 1
            text = pdf.pages[i].extract_text() or ""
            text = text.strip()

            if not text:
                # 完全空页，通常是整页图片或公式截图
                results.append(
                    f"=== 第 {page_num} 页 ===\n"
                    f"【此页无可提取文字，建议手动复制该页内容后粘贴给我】"
                )
            elif is_garbled(text):
                # 有内容但可读字符比例低，疑似公式乱码
                results.append(
                    f"=== 第 {page_num} 页 ===\n"
                    f"【提取内容疑似乱码（可能含大量公式图片），建议手动复制该页文字】\n"
                    f"--- 原始提取内容（供参考）---\n{text}"
                )
            else:
                results.append(f"=== 第 {page_num} 页 ===\n{text}")

    print("\n\n".join(results))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法：python extract_pdf_pages.py <pdf_path> <start_page> <end_page>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    start    = int(sys.argv[2])
    end      = int(sys.argv[3])
    extract(pdf_path, start, end)
