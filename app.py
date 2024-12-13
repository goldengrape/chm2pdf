import os
import subprocess
import tempfile
import streamlit as st
import pdfkit
from PyPDF2 import PdfMerger

def chm_to_pdf(chm_file_path, output_pdf_path):
    with tempfile.TemporaryDirectory() as output_dir:
        # 解压CHM文件
        subprocess.run(["extract_chmLib", chm_file_path, output_dir], check=True)

        # 列出所有解压文件（调试）
        extracted_files = []
        for root, dirs, files in os.walk(output_dir):
            for f in files:
                extracted_files.append(os.path.join(root, f))
        st.write("解压出的文件列表：")
        st.write(extracted_files)

        # 找到所有的HTML文件(包括.html和.htm)
        html_candidates = []
        for f in extracted_files:
            if f.lower().endswith(".html") or f.lower().endswith(".htm"):
                html_candidates.append(f)

        st.write("找到的HTML候选文件：", html_candidates)

        # 如果没有任何HTML候选文件，则说明无法转换
        if not html_candidates:
            raise RuntimeError("未在CHM文件中找到任何HTML/HTM文件。")

        # 配置wkhtmltopdf
        options = {
            "enable-local-file-access": "",
            "load-error-handling": "ignore"
        }

        temp_pdfs = []
        total = len(html_candidates)
        for i, html_file in enumerate(html_candidates):
            st.progress(i / total)
            html_file_path = f"file://{os.path.abspath(html_file)}"
            
            # 再次检查文件是否存在
            if not os.path.exists(html_file):
                st.warning(f"文件不存在: {html_file}, 跳过。")
                continue
            
            pdf_file = html_file + ".pdf"
            try:
                pdfkit.from_file(html_file_path, pdf_file, options=options)
                temp_pdfs.append(pdf_file)
            except Exception as e:
                st.warning(f"转换 {html_file} 时发生错误，已跳过：{e}")
                continue

        if not temp_pdfs:
            raise RuntimeError("没有成功转换任何HTML文件，请检查CHM内容是否正常。")

        # 合并PDF
        merger = PdfMerger()
        for pdf in temp_pdfs:
            merger.append(pdf)
        merger.write(output_pdf_path)
        merger.close()

st.title("CHM转PDF工具")

uploaded_file = st.file_uploader("上传CHM文件", type=["chm"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".chm") as tmp_chm:
        tmp_chm.write(uploaded_file.read())
        tmp_chm_path = tmp_chm.name

    output_pdf = "output.pdf"
    try:
        st.write("正在转换，请稍候...")
        chm_to_pdf(tmp_chm_path, output_pdf)
        st.success("转换完成!")
        with open(output_pdf, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(label="下载PDF文件", data=pdf_bytes, file_name=output_pdf)
    except Exception as e:
        st.error(f"转换失败: {e}")
    finally:
        if os.path.exists(tmp_chm_path):
            os.remove(tmp_chm_path)
