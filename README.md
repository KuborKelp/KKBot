## 安装mcl

    使用 iTX Technologies Mirai Console Loader(简称mcl)
    地址:https://github.com/iTXTech/mcl-installer
      ·安装 Java 运行时（版本必须 >= 11）
      ·从 Releases 下载最新版本的MCL
      ·解压到某处

### 设置Qsign签名服务

    详见https://github.com/MrXiaoM/qsign

## 需要的python库的安装

    笔者使用的是py3.11
    pip install graia-ariadne[full]
    pip install pillow
    pip install requests
    pip install creart
    
    <!-- ::
    python3.11 -m pip graia-ariadne[full]
    python3.11 -m pip pillow
    python3.11 -m pip request -->

## 运行方法(以windows为例)

    先打开mcl文件夹下的mcl.cmd,加载完毕后登录QQ
       格式:login <qq> <password>
    运行 main.py

