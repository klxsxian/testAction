
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

    5.3 在workflows目录新建testCosUpload.yml,测试通过
        saltbo/uptoc这个组件只能上传，支持oss,cos,s3等，如果需要下载就需要替换成另一个

    5.4 一个支持腾讯cos上传和下载的组件 参考：https://github.com/marketplace/actions/tencent-cos-action
        在workflows目录新建coscmd.yml,测试通过
        使用需要参考腾讯coscmd相关的命令 参考：https://cloud.tencent.com/document/product/436/10976

#### 6、sqlfluff DBT SQL语法格式正确性的校验
    6.1 安装依赖包
        pip install sqlfluff
        pip install sqlfluff-templater-dbt

    6.2 配置sqlfluff：
        创建.sqlfluff和.sqlfluffingnore文件
        更多配置使用参考：https://docs.sqlfluff.com/en/stable/configuration.html

    6.3 使用sqlfluff：
        示例：检查某个目录下的所以sql文件
        执行命令：sqlfluff lint path/to/my/sqlfiles
        
        step1、执行sqlfluff lint ./models
        L:  36 | P:   3 | L003 | Indentation not hanging or a multiple of 4 spaces
        == [models/stg/stg_members.sql] FAIL =========》发现有语法错误
    
        step2、修复sql,执行如下命令：
        sqlfluff fix ./models/stg/stg_members.sql

        step3、再次执行：执行sqlfluff lint ./models   
        结果：校验通过，说明sqlfluff根据配置的规则，进行了修复

### 7、sqlfluff github cicd校验
    7.1 在workflows目录新建sqlfluff_lint_models.yml
 
### dbt安装
    pip install dbt-postgres