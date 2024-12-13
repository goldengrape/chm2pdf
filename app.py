import os
import subprocess
import tempfile
import shutil
import streamlit as st
import pdfkit
from PyPDF2 import PdfMerger

def chm_to_pdf(chm_file_path, output_pdf_path):
    with tempfile.TemporaryDirectory() as output_dir:
        # 解压CHM文件
        subprocess.run(["extract_chmLib", chm_file_path, output_dir], check=True)

        # 找到所有HTML文件
        html_files = []
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.lower().endswith(".html") or file.lower().endswith(".htm"):
                    html_files.append(os.path.join(root, file))

        if not html_files:
            raise RuntimeError("未能在CHM文件中找到HTML文档，无法转换。")

        # 转换为PDF时，加入options启用本地文件访问
        options = {
            "enable-local-file-access": ""
        }

        temp_pdfs = []
        total = len(html_files)
        for i, html_file in enumerate(html_files):
            # 在streamlit中显示进度
            st.progress(i / total)
            # 给html_file加上file://协议前缀（如果需要）
            html_file_path = f"file://{os.path.abspath(html_file)}"
            pdf_file = html_file + ".pdf"
            pdfkit.from_file(html_file_path, pdf_file, options=options)
            temp_pdfs.append(pdf_file)

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
