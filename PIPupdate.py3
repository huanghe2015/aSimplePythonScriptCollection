#!/usr/bin/python
 
import os
 
package = input("Please input the package which you want to update!\n")
command = "pip3 install %s -U -i http://pypi.mirrors.ustc.edu.cn/simple --trusted-host pypi.mirrors.ustc.edu.cn" % package
os.system(command)