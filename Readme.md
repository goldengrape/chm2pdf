# CHM转PDF转换工具

本项目提供了一个基于Streamlit的Web界面，用于将CHM文件转换为PDF文件。用户可以通过上传CHM文件，在线完成转换并下载生成的PDF。

## 功能特色

- **简易操作**：通过简单的文件上传操作，实现CHM到PDF的一键转换。  
- **可视化进度**：在转换过程中提供进度提示。  
- **跨平台支持**：  
  - 在Linux环境下使用`extract_chmLib`进行CHM解包  
  - 在Windows环境下可使用`hh.exe -decompile`进行CHM解包（请根据实际情况调整代码）  
- **PDF合并**：自动将CHM内部的多个HTML文件转换为多个PDF后再合并为一个完整的PDF文档。

## 文件结构

```
project/
│
├─ app.py               # Streamlit 主程序代码
├─ requirements.txt      # Python依赖文件
└─ packages.txt          # 系统依赖文件（用于安装系统级别工具）
```

## 部署和运行

### 安装依赖

在部署环境中（例如本地、云服务器或 Streamlit Cloud）安装所需依赖。

**Python依赖**（通过 `requirements.txt` 安装）：  
```bash
pip install -r requirements.txt
```

`requirements.txt`中包括：
- `streamlit`  
- `pdfkit`  
- `PyPDF2`

**系统依赖**（通过 `packages.txt` 安装）：  
```txt
wkhtmltopdf
libchm-bin
```

在Linux环境中，您也可以直接通过命令行安装：  
```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf libchm-bin
```

若在Windows下使用，请安装 `HTML Help Workshop` 以获取 `hh.exe`，并修改代码中调用 `extract_chmLib` 的部分。

### 运行

安装完毕后，运行Streamlit应用：  
```bash
streamlit run app.py
```

运行后将在本地服务器（默认 `http://localhost:8501`）打开Web界面，您可以通过浏览器访问。

### 使用步骤

1. 打开浏览器访问 `http://localhost:8501`。  
2. 在页面中上传需要转换的 `.chm` 文件。  
3. 点击确认后，等待转换完成。  
4. 转换成功后，可直接下载生成的 `output.pdf` 文件。

## 注意事项

- 确保在部署环境中安装了 `wkhtmltopdf` 和 `extract_chmLib` (Linux) 或 `HTML Help Workshop` (Windows)。  
- `wkhtmltopdf` 在某些平台需要通过配置指定其可执行文件路径，如有需要可在 `app.py` 中通过 `pdfkit.configuration()` 设置。  
- 若CHM文件体积较大或包含大量HTML文档，转换过程可能较为耗时。请耐心等待。

## 致谢

此程序的撰写由 **ChatGPT o1 pro** 完成，该模型提供了从CHM到PDF的转换逻辑示例代码及部署配置说明。  
如有问题或改进建议，欢迎提出Issue或Pull Request！
