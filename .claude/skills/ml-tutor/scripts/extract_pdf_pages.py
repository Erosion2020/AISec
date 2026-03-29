"""
从 PDF 中提取指定页码范围的文字内容。
用法：python extract_pdf_pages.py <pdf_path> <start_page> <end_page>
页码从 1 开始（与用户说的页码一致）。

提取策略：
1. 优先用 pdfplumber 提取文字层
2. 如果某页提取为空（图片/扫描页），自动降级用 OCR（pytesseract）识别
3. OCR 也不可用时，标注该页需要用户手动复制
"""

import sys


def try_ocr_page(pdf_path, page_index):
    """对单页尝试 OCR，返回识别文字或 None。"""
    try:
        from pdf2image import convert_from_path
        import pytesseract
    except ImportError:
        return None

    try:
        images = convert_from_path(
            pdf_path,
            first_page=page_index + 1,
            last_page=page_index + 1,
            dpi=200,
        )
        if not images:
            return None
        text = pytesseract.image_to_string(images[0], lang="chi_sim+eng")
        return text.strip() or None
    except Exception:
        return None


def extract(pdf_path, start_page, end_page):
    try:
        import pdfplumber
    except ImportError:
        print("ERROR: pdfplumber 未安装，请先运行：pip install pdfplumber")
        sys.exit(1)

    ocr_available = None   # 延迟检测，第一次遇到空页才判断

    results = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        if start_page < 1 or end_page > total:
            print(f"ERROR: 页码超出范围，该 PDF 共 {total} 页")
            sys.exit(1)

        for i in range(start_page - 1, end_page):
            page_num = i + 1
            text = pdf.pages[i].extract_text()

            if text and text.strip():
                # 正常提取到文字
                results.append(f"=== 第 {page_num} 页 ===\n{text.strip()}")
            else:
                # 空页，尝试 OCR
                if ocr_available is None:
                    # 首次遇到空页时检测 OCR 依赖
                    try:
                        import pdf2image  # noqa: F401
                        import pytesseract  # noqa: F401
                        ocr_available = True
                    except ImportError:
                        ocr_available = False

                if ocr_available:
                    print(f"第 {page_num} 页无文字层，正在 OCR 识别...", file=sys.stderr)
                    ocr_text = try_ocr_page(pdf_path, i)
                    if ocr_text:
                        results.append(
                            f"=== 第 {page_num} 页（OCR 识别）===\n{ocr_text}"
                        )
                    else:
                        results.append(
                            f"=== 第 {page_num} 页 ===\n"
                            f"（OCR 未能识别内容，建议手动复制该页文字）"
                        )
                else:
                    results.append(
                        f"=== 第 {page_num} 页 ===\n"
                        f"（此页无文字层，且 OCR 未安装。"
                        f"如需识别请运行：pip install pdf2image pytesseract，"
                        f"并安装 Tesseract-OCR 程序）"
                    )

    print("\n\n".join(results))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法：python extract_pdf_pages.py <pdf_path> <start_page> <end_page>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    start    = int(sys.argv[2])
    end      = int(sys.argv[3])
    extract(pdf_path, start, end)
