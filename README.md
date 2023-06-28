# 论文翻译工具

## 需求

1. 将PDF格式的英文论文翻译为中文，输出为Markdown格式文本

## 方案

1. 解析PDF
    1. 将PDF分为 Page, Block, Line, Span 获取 span 中文字的 font size
    1. 按照以下步骤处理，各步骤都需要记录对应的坐标
        1. 找正文
            1. 统计 font size 出现频率最高的，认为是正文
        1. 找目录
            1. 有TOC，通过meta data找
            1. 没有TOC
                1. 所有 font size > 正文的 font size，并且出现次数 >= 2 的认为是目录
                1. 按照 font size 从大到小排序，是否能形成一颗完备的树
        1. 找段落
            1. 根据 Block, Line, Span 找到 Page 的左右边界
            1. 根据 连续 Span xxbox 位置关系和 Block 边界的关系，判断段落的结束和下一段开始
        1. 特殊情况
            1. 其他 font size 的Span，我们认为是文章中的强调，可以使用 Markdown 中的强调格式（加粗、斜体、下划线、删除线、高亮、下标/上标、。。。）
        1. PDF中的图片导出为PNG文件，记录好其在PDF中的坐标
        1. 将内容汇总后，记录到json文件中，标记其类型，坐标，内容
1. 将内容按照Markdown格式输出
1. 使用ChatGLM将内容翻译为中文

## 资源

1. [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
1. [Oliver Wyman](https://www.oliverwyman.com/our-expertise/industries/financial-services.html)
1. [JLI](https://www.us.jll.com/)
1. [Google Finance](https://www.google.com/finance)
1. [Yahoo Finance](https://finance.yahoo.com)
1. [Open Access Library](https://www.oalib.com/)
1. [SCI-Hub](https://tool.yovisun.com/scihub/) [SCI-hub](https://sci-hub.ru/)
1. [Science.gov](https://www.science.gov/)
