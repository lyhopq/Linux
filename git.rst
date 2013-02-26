==============
Git使用记录
==============

Git基本使用
===============

详细手册： `Git Book`_

.. _`Git Book`: http://gitbook.liuhui998.com/index.html

去跟踪以commit的文件
----------------------

1. ``git rm -f source/*.pyc``
#. ``git cvommit``
#. 在将不要跟踪的文件在 ``.gitignore`` 中设定好


merge的冲突解决
------------------

1. 编辑冲突
#. ``git commit``

    .. note:: 冲突说明
    
        ::
    
          a123
          <<<<<<< HEAD
          b789
          =======
          b45678910
          >>>>>>> 6853e5ff961e684d3a6c02d4d06183b5ff330dcc
          c
       
        其中：冲突标记<<<<<<< （7个<）与=======之间的内容是本地修改，=======与>>>>>>>之间的内容是合入的修改。

        可以使用图形界面工具解决冲突： ::

          git mergetool

github
=========

配置Git
---------

1. 在本地创建ssh key： ::

     $ ssh-keygen -t rsa -C "youremail@youremail.com"

#. 回到github，进入Account Settings，左边选择SSH Keys，Add SSH Key,title随便填，粘贴key。为了验证是否成功，在终端输入： ::

     $ ssh -T git@github.com

#. 设置username和email： ::

     $ git config --global user.name "your name"
     $ git config --global user.email "youremail@youremail.com"

#. 进入要上传的仓库，右键git bash，添加远程地址： ::

     $ git remote add origin git@github.com:yourName/yourRepo.git
     

git-svn
===========

工作流
-------------

1. 从svn clone出项目： ::

   $ git svn clone -s https://svn.xxx.com/svn/xxx  # 加上-s参数以标记识别svn标准的目录分支结构
   $ git svn show-ignore >> .git/info/exclude      # 通过show-ignore设置git库的exclude属性

#. 建立本地工作分支，开始工作： ::

   $ git checkout -b work
   $ git commit -a

#. 提交回svn： ::

   $ git checkout master
   $ git merge work
   $ git svn rebase
   $ git svn dcommit
