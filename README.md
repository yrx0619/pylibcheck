# pylibcheck
检查一个项目中使用但是还未安装的python库。

# 使用方法
```shell
[root@host pylibcheck]# python gen_requirement.py -h
usage: gen_requirement.py [-h] [-d DIR] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     The path of source code
  -o OUTPUT, --output OUTPUT
                        output path for requirement.txt

```

-d 参数 代表工程或者源码所在的目录，默认是当前目录
-o 参数 代表输出requirement.txt文件的目录，默认是当前目录

# 实现 
多线程分析每一个py脚本中使用到的库，查找本机是否安装了。
