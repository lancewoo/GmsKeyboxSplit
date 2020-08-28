# -*- coding: utf-8 -*-
"""
解析谷歌提供的GMS密钥文件，并将其拆分，按IMEI逐个保存文件。

运行时命令行第一个参数是待拆解密钥文件名，第二个参数是标记调试停留的文件次序，
例如：
    GmsKeyboxSplit.py gmskeyboxes.xml 2
将在拆分gmskeyboxes.xml文件时写完第二个设备密钥文件后停止继续执行。

author: WU Liang
"""

import xml.etree.ElementTree as ET
import copy
import sys

if sys.version_info < (3,7,6):
    sys.stderr.write("You need Python 3.7.6 or later to run this script\n")
    sys.exit(1)

# 标记调试停留的文件次序，不做调试时可将其设置为0
DEBUG_STOP = 0 if len(sys.argv) != 2 else int(sys.argv[2] - 1)

def main(keyboxesxml):
    tree = ET.parse(keyboxesxml)
    root = tree.getroot()

    index = 0
    deviceId = ''

    # 修改keybox数量为1
    for child in root:
        # print(child.tag, child.attrib)
        # if child.attrib:
        #     index += 1
            
        #     deviceId = child.attrib["DeviceID"]
        #     # print('deviceId = ', deviceId)
        #     if index > 1:
        #         pass
        #         #root.remove(child)
        #         #print('index = ', index)
        #     else:
        #         continue
        if child.tag == 'NumberOfKeyboxes':
            print(child.tag, child.text)
            child.text = '1'
            break
            # print(child.tag, child.text)

    # 备份，方便后面直接复制
    treebackup = copy.deepcopy(tree)

    print('==================================<<<<')

    for keyboxIndex in range(len(treebackup.getroot().findall('Keybox'))):
        tree = copy.deepcopy(treebackup)
        root = tree.getroot()
        # 当前正在循环到的节点是第keyboxIndex+1个
        index = 0
        # 删除其他节点
        for child in root.findall('Keybox'):
            if child.attrib:
                index += 1
                if index != (keyboxIndex + 1):
                    root.remove(child)
                    # print('index = ', index)
                else:
                    deviceId = child.attrib["DeviceID"]

        # 写文件，
        # 先将原xml文件中的-----BEGIN CERTIFICATE-----开始没有换行的换行
        # 同时将没有换行黏连的标签换行，类似这种：<Key algorithm="rsa"><PrivateKey format="pem">
        keyboxxml = 'keymaster_keybox_' + str(deviceId) + '.xml'
        # with open(keyboxxml, 'wb') as outputfile:
        #     tree.write(outputfile, encoding = "utf-8", xml_declaration = True)
        with open(keyboxxml, 'wb') as outputfile:
            xmlText = ET.tostring(root)
            xmlText = xmlText.replace(b">-----BEGIN", b">\n-----BEGIN").replace(b"><", b">\n<")
            # 主动写入整个xml树
            outputfile.write(b'<?xml version="1.0"?>\n')
            outputfile.write(xmlText)
            # 使用ElementTree.write()写入文件，缺点是xml头文件声明必然会带encoding选项
            # tree._setroot(ET.fromstring(xmlText))
            # tree.write(outputfile)
        print('写入文件：' + keyboxxml + '，序号：' + str(keyboxIndex + 1))
        # ET.dump(root)
        # 调试
        if DEBUG_STOP > 0 and keyboxIndex == DEBUG_STOP:
            print('调试值：', str(DEBUG_STOP))
            break

    print('==================================>>>>')

if __name__ == '__main__':
    # print(sys.argv)
    if len(sys.argv) == 1:
        main('2020-08-12_06-30-21.255_UTC.attest_keyboxes.xml')
    else:
        main(sys.argv[1])
