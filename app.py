import os
import subprocess
import tempfile
import shutil
import streamlit as st
import pdfkit
from PyPDF2 import PdfMerger

def chm_to_pdf(chm_file_path, output_pdf_path):
    # 创建一个临时输出目录
    base_name = os.path.splitext(os.path.basename(chm_file_path))[0]
    with tempfile.TemporaryDirectory() as output_dir:
        # 使用extract_chmLib解压CHM文件（Linux环境）
        # 如果在Windows上，则使用:
        # subprocess.run(["hh.exe", "-decompile", output_dir, chm_file_path], check=True)
        subprocess.run(["extract_chmLib", chm_file_path, output_dir], check=True)

        # 遍历解包目录，找到所有的HTML文件
        html_files = []
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.lower().endswith(".html") or file.lower().endswith(".htm"):
                    html_files.append(os.path.join(root, file))

        if not html_files:
            raise RuntimeError("未能在CHM文件中找到HTML文档，无法转换。")

        # 将每个HTML文件转换为单独的PDF文件
        temp_pdfs = []
        for i, html_file in enumerate(html_files):
            # 在Streamlit中显示进度
            st.progress(i / len(html_files))
            pdf_file = html_file + ".pdf"
            pdfkit.from_file(html_file, pdf_file)
            temp_pdfs.append(pdf_file)

        # 合并所有PDF为一个完整的PDF
        merger = PdfMerger()
        for pdf in temp_pdfs:
            merger.append(pdf)
        merger.write(output_pdf_path)
        merger.close()


st.title("CHM转PDF工具")

uploaded_file = st.file_uploader("上传CHM文件", type=["chm"])

if uploaded_file is not None:
    # 将上传文件保存到临时目录
    with tempfile.NamedTemporaryFile(delete=False, suffix=".chm") as tmp_chm:
        tmp_chm.write(uploaded_file.read())
        tmp_chm_path = tmp_chm.name

    output_pdf = "output.pdf"  # 输出PDF文件名，可自行修改
    try:
        st.write("正在转换，请稍候...")
        chm_to_pdf(tmp_chm_path, output_pdf)
        st.success("转换完成!")
        
        # 提供PDF下载链接
        with open(output_pdf, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(label="下载PDF文件", data=pdf_bytes, file_name=output_pdf)
        
    except Exception as e:
        st.error(f"转换失败: {e}")
    finally:
        # 清理临时CHM文件
        if os.path.exists(tmp_chm_path):
            os.remove(tmp_chm_path)
        # 如有必要，清理其它临时文件
        if os.path.exists(output_pdf):
            # 这里保留输出文件到当前目录，亦可自行删除
            pass
