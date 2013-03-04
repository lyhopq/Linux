Linux 实用集
================


Linux下实现合并PDF文件
-------------------------

    ::
    
        使用Gost Script和 PDFtk运行如下命令：
        #gs -q -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=Linuxidc.pdf -dBATCH *.pdf
        合并结果：把当前目录下所有的 pdf 文件全部合并到 Linuxidc.pdf 中。
    

杀掉僵尸
---------------------

     .. code-block:: bash
     
         $top  # 看有没有僵尸进程
         $ps -ef | grep defunct    # 列出僵尸(defunct)进程
         $kill -9 ppid     # 杀掉僵尸进程的父进程(ppid)
     
     
查看 TCP/IP 链接状况
---------------------
    
    .. code-block:: bash
    
    
        netstat -n | awk '/^tcp/{++S[$NF]} END {for(a in S) print a, S[a]}'
    

系统备份与还原
---------------------

- 备份

    .. code-block:: bash

        #cd /
        #tar -cvpzf /home/lyh/Backup/xxx.tgz / 
            --exclude=/media --exclude=/proc --exclude=/mnt 
            --exclude=/lost+found --exclude=/tmp 
            --exclude=/sys --exclude=/home

- 还原

    .. code-block:: bash

        #tar -xvzf /home/lyh/xxx.tgz -C / }}}g


合并文本行
-------------

* 合并相邻两行（奇偶合并）

    .. code-block:: bash

        awk '{if(NR%2==0) {print $0} else {printf $0 "   "}}' filename 
        或
        sed '{N;s/\n/   /}' filename


smplayer双字幕制作
---------------------
    
    .. code-block:: bash
    
        ls -1 *.srt > tmpg
        while read l1 && read l2;dog
            file=${l1%.*.*}.srt  # 模式匹配g
            echo $fileg
            cat $l1 $l2 > $fileg
        done < tmpg
    
    .. note::
    
        模式匹配运算符号：g
         * ${var#pattern}最短匹配开头处，并删除该部分。
         * ${var##pattern}最长匹配开头处，并删除该部分。
         * ${var%pattern}最短匹配结尾处，并删除该部分。
         * ${var%%pattern}最长匹配结尾处，并删除该部分。
    
cron 服务
-----------

 :: 

    /etc/init.d/cron start //启动服务
    
    建立新任务：
    方式1：用配置文件/etc/crontab
    vim /etc/crontab
    # m h dom mon dow user  command
    */2 * * * * root echo "hello"
    解释：
    m - month
    h - hour
    dom - day of the month
    mon - month
    dow - day of the week (0 星期天)
    
    方式2： 用 -e 选项
    # crontab -e
     m h  dom mon dow   command
    */2 * * * * echo "hello"
    
    实例：
    $crontab -e
    */2 * * * * notify-send "Hehe" "I'm running"

Desktop 文件示例
-----------------
  .. code-block:: bash

        $ cat xvidcap.desktop
        [Desktop Entry]
        Encoding=UTF-8
        Name=Xvidcap
        Name[zh_CN]=屏幕录像机
        Exec=xvidcap
        Icon=/usr/share/xvidcap/glade/xvidcap_logo.png
        Terminal=false
        Type=Application
        Categories=GNOME;GTK;Application;AudioVideo;

制作ISO文件，并刻录
--------------------

  .. code-block:: bash

        $mkisofs -r -o myISOFile.ISO folderOrFilename
        $cdrecord --devic=cdwriter-device -tao -eject myISOFile.ISO


远程登录
----------

* rdesktop

  .. code-block:: bash

    rdesktop -f -r sound:local -r clipboard:PRIMARYCLIPBOARD -r disk:MyDisk=/home/lyh/Downloads -a 24 -u administrator -p 203 192.168.0.1

* X ::

    X :1.0 -query 192.168.0.1

查看系统中文字体
-------------------

  .. code-block:: bash

    $fc-list :lang=zh-cn

Ubuntu 系统备份
-----------------

* 备份

  .. code-block:: bash

    cd /
    sudo tar -cvpzf /home/lyh/Backup/Ubuntu_2009.3.7.tgz / 
    --exclude=/media --exclude=/proc --exclude=/mnt 
    --exclude=/lost+found --exclude=/tmp 
    --exclude=/sys --exclude=/home

* 恢复

  .. code-block:: bash

    tar -xvzf /home/lyh/Backup/Ubuntu_2009.3.7.tgz -C /

* 得到已安装软件列表文件 
  
  ::

    dpkg -–get-selections | grep -v deinstall > ubuntu.files

* 从备份的安装包的列表文件恢复所有包 
  
  ::
  
    dpkg --set-selections < ubuntu.files;sudo dselect



* 将列表文件发到邮箱中

  ::

    dpkg -–get-selections | grep -v deinstall > ubuntu-files; cat ubuntu-files | mailx -s “ubuntu-files” 自己的email地址

文件分割
---------

* 分割 ::

    $ split –b500m myBigFile mySmallFIles.

* 合并 ::

    $ cat mySmallFiles.* > myBigFile


快速重装Ubuntu
---------------

    ::

        # 重装前
        cp /etc/apt/sources.list ~/home/sources.list # home分区单独，且不格式化
        dpkg --get-selections | grep -v deinstall > Ubuntu.files #得到已安装软件列表文件
        
        # 重装时
        cp ~/home/sources.list /etc/apt/sources.list
        dpkg --set-selections


转换jpg图片为pdf
-------------------

    ::

        $ find *.jpg -exec convert {} {}.pdf \;

vim去掉 `^M`
-------------------

在vim中显示的 `^M`` 其实是 ``\r`` ，因此使用如下命令去掉： 

    ::

        :%s/\r/g


Windows远程访问Unbuntu
------------------------

1. 在Ubuntu中打开 ``桌面共享首选项`` 软件（Ubuntu12.04中按 ``windows`` 键，输入 ``桌面共享首选项`` ）。进行下图所示的设置：

     .. image:: _static/gongxiang.png

#. 在Windows中安装vnc软件，安装完后打开 `Run VNC Viewer` ，并输入要登录的Ubuntu系统IP即可。 

Ubuntu 差异比较工具
------------------------------

Meld，一个可视化的文件及目录比较工具。为了方便使用，写了几个脚本添加右键功能（模仿 Beyond Compare 的右键快捷菜单）。下载\ `脚本`_\ ，解压后执行：

    .. code-block:: bash

        chmod +x meld.sh
        ./meld.sh  

下图是使用方法及其结果： 

    .. figure:: _static/meld1.png

       使用方法，与 `Beyond Compare` 相似 

    .. figure:: _static/meld2.png

       可视化比较界面

.. _脚本: _static/meld.zip

改变终端大小
---------------

  ::
    
    sudo vim /usr/share/vte/termcap/xterm

找到下面设置，修改为想要的值（80为高，24为宽）： ::

    co#80:it#8:li#24:\





