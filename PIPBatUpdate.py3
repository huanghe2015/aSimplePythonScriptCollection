import pip
from subprocess import call
 
for dist in pip.get_installed_distributions():
    call("pip3 install -U -i https://pypi.tuna.tsinghua.edu.cn/simple " + dist.project_name, shell=True)