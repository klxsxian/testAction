
###1、创建python 虚拟运行环境
python3 -m venv ./

###2、启动运行虚拟环境
source ./bin/activate

###3、安装腾讯cos的pythonSDK
pip install -U cos-python-sdk-v5

###4、测试cos上传

    4.1 设置好IDEA对应python环境的SDK

    4.2 新建local.txt和cosUpload.py文件

    4.3 idea运行cosUpload.py文件--已测试通过

###5、github action 验证cos上传 ，主要是替换s3
    5.1 GitHub Actions了解  参考：https://docs.github.com/cn/actions/quickstart
    
    5.2 选择saltbo/uptoc这个action组件  参考：https://github.com/marketplace/actions/uptoc-action

    5.3 在workflows目录新建testCosUpload.yml
    

