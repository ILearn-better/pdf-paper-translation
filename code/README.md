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
   <img src="C:\Users\EDY\AppData\Roaming\Typora\typora-user-images\image-20230630180151486.png" alt="image-20230630180151486" style="zoom: 33%;" />
   - 思路2：利用block的x_0和x_1作为左横边界和右横边界，找满足筛选条件(span_x1 >  next span_x0 and span_y0 < next span_y1)的span，取其y_1作为上纵边界，利用下一个满足条件的span的y_0作为下纵边界，四角边界框出部分为段落。
3. 搭建pdf绘图测试模块，利用输出的span 可视化各模块文本模块提取情况。
>结果:可能是pdf比较复杂，正文提取结果可以接受，段落提取结果不理想
4.手动构建简单pdf。（Markdown内输入再转pdf）
5. 进行函数整理，.ipynb转为.py。



 
