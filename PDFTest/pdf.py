from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter


def parser_pdf_file(pdf_file_path):
    read_pdf = open(pdf_file_path, 'rb')  # 打开PDF文件。
    parser_pdf = PDFParser(read_pdf)  # 用文件对象创建一个PDF文档分析器。
    pdf_document = PDFDocument(parser_pdf)  # 创建一个PDF文档。

    parser_pdf.set_document(pdf_document)
    pdf_document.set_parser(parser_pdf)  # 连接分析器 与文档对象。
    pdf_document.initialize()  # 如果没有密码，就创建一个空的字符串。

    if not pdf_document.is_extractable:  # 检测文档是否提供txt转换，不提供就忽略。
        raise PDFTextExtractionNotAllowed
    else:
        pdf_manager = PDFResourceManager()  # 创建PDF资源管理器 来管理共享资源。
        pdf_laparams = LAParams()  # 创建一个PDF参数分析器。
        pdf_device = PDFPageAggregator(pdf_manager, laparams=pdf_laparams)  # 创建一个聚合器
        pdf_interpreter = PDFPageInterpreter(pdf_manager, pdf_device)  # 创建一个PDF页面解释器对象
        # 循环遍历列表，每次处理一页的内容，pdf_document.get_pages()获取page列表
        for each_page in pdf_document.get_pages():
            pdf_interpreter.process_page(each_page)  # 使用页面解释器来读取
            layout = pdf_device.get_result()  # 这里layout是一个LTPage对象 里面存放着这个page解析出的各种对象 一般包括LTTexBox,LTFigure,LTImage,
            # LTTexBoxHorizontal等等 想要获取文本就获得对象的text属性。
            # print(layout)
            for each_info in layout:
                if isinstance(each_info, LTTextBoxHorizontal):
                    results = each_info.get_text().strip()
                    print(results)
                    print("======")
                    print(len(results))


if __name__ == '__main__':
    # pdf_file_path = get_pdf_file()
    parser_pdf_file(r'D:\code\python\spider\ArticleSpider\pdfs\full\6b196eca27c90e60f8b1c4ef36d8066f4d2d7bcd.pdf')

