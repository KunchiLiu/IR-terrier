# 现代信息检索大作业
## 环境
开发环境：Mac OS
软件版本：Java JRE 1.8.0、Python 3.7、Terrier5.0

## 数据文件
![image](https://github.com/KunchiLiu/IR-terrier/tree/master/images/datapath.png)

## 数据预处理成.xml格式

执行脚本：

```zsh
python modules/xml/clinicaltrials_xml.py
```
## 对预处理后的.xml文件执行去停用词和词形还原

执行脚本：

```zsh
python3 modules/xml/process.py
```
