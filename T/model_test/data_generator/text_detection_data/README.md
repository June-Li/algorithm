本文件夹中所有文件均用于生成文本检测(ctpn)用数据，运行的顺序以及各个文件的作用如下所示：

1.pdf_anaylse.py 运行程序可以将pdf/original中的pdf文件转成100-200分辨率之间的图片，并生成每幅图片对应的文本行的bounding box信息。图片和bounding box都存于pdf/pdf_text文件夹中。  
2.combine.py 运行可以将标准的pdf图片制作成伪扫描件形式，主要变化为增加背景，旋转文本角度，调节对比度和亮度。输入图片来源于pdf/pdf_text，输出结果存放于pdf/new。  
3.split_label.py 将伪扫描件的bounding box制作成ctpn所需的形式，即一行的bounding box会被分成多个宽度为16像素的多个小bounding box共同构成。输出结果分为图片和标签，图片保存在pdf/re_image中，标签保存在pdf/label_tmp中。  
4.ToVoc.py 将第3步得到的结果制作成VOC2007形式的文件，存在VOC2007文件夹中，可用于ctpn的训练


其他：  
1.fun_code.py主要用于可视化结果，运行结果保存于vision。其中xml_vision函数用于解析xml文件，可用将xml的可视化结果保存，txt_vision函数可用于解析txt文件，并保存期可视化结果。  
2.使用pdfplumber前建议修改pdfplumber/display.py的第18行"DEFAULT_RESOLUTION = 144"，非必须，建议修改。
