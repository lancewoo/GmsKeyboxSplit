# GmsKeyboxSplit

解析谷歌提供的GMS密钥文件，并将其拆分，按IMEI逐个保存文件。

运行时命令行第一个参数是待拆解密钥文件名，第二个参数是标记调试停留的文件次序，

例如：
    GmsKeyboxSplit.py gmskeyboxes.xml
拆分gmskeyboxes.xml。
    GmsKeyboxSplit.py gmskeyboxes.xml 2
将在拆分gmskeyboxes.xml文件时写完第二个设备密钥文件后停止继续执行。
