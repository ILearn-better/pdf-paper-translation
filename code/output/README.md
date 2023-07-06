# 论文分析翻译工具开发

**2023.06.28**

1.配置环境:

```
pycharm community
python 3.8.7 
```
2.选择下载文献

3.熟悉pymupdf使用，实现font size的获取

**2023.06.29**

1.完成正文识别模块，输入整体pdf对象，整合输出正文的所有span的span size，span text，span bbox

2.目录查找部分，还差检测筛选出的font size是否满足一颗完备树。

**2023.06.30**

1. 完成目录查找模块
2. 继续开发段落提取模块，遇到若干问题
   - 思路1：找key span(需满足span_x1 >  next span_x0 and span_y0 < next span_y1),再通过key span进行正文span list切分
   - 思路2：利用block的x_0和x_1作为左横边界和右横边界，找满足筛选条件(span_x1 >  next span_x0 and span_y0 < next span_y1)的span，取其y_1作为上纵边界，利用下一个满足条件的span的y_0作为下纵边界，四角边界框出部分为段落。
3. 搭建pdf绘图测试模块，利用输出的span 可视化各模块文本模块提取情况。
>结果:可能是pdf比较复杂，正文提取结果可以接受，段落提取结果不理想

4. 手动构建简单pdf。（Markdown内输入再转pdf）

5. 进行函数整理，.ipynb转为.py。

**2023.07.01**
1. 优化目录提取模块和段落提取模块
2. 完成图片和其他font提取模块
3. 尝试简单pdf转json

**2023.07.03**

1. 完成other font提取模块并测试。  
    问题:  

  	对三个pdf文档进行提取other font进行对比：
  		绘制复杂pdf的other font的效果并不太好,对于复杂文本的公式,表格等提取的很乱,失去了其关联性，甚至可以说该部分信息已失效。所以一般的，之后尝试将含有公式和表格的block作为图片保存，通过OCR技术进行提取或仅存为图片。

2. 改善markdown生成的格式问题  

   ​	利用<span>标签的style属性，将font-size与span size对应，增强生成后的markdown可读性  
   ​	问题:表格和图片没有对应插入  

3. 配置githunb上同类型的开源项目环境。  

  对比一下效果，调整下一步思路。  

  >[pdf-to-markdown](https://github.com/lxulxu/pdf-to-markdown)

4. 阅读其他项目文档  
    表格提取  
    公式提取  

    > [聊聊Python模块导入机制与大型项目规范：](https://juejin.cn/post/6876310603942920200)

**2023.07.05**

完成json to chart：

- 完成功能：
  - 利用模板Json（三层）变量生成图片（三种），并保留Json和图片对应路径
  - 自定义Json变量生成图片
  - 完成含有5个主题的复杂叠加图片的提取内容提取与绘图
- 测试与修改

  - 手动改json内部key words和values都为英文
  
  - 美化和添加chart的细节

**2023.07.06**

协助简历提取

讨论json结构搭建，完成json生成
