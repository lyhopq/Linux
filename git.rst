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
#. ``git commit``
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

撤销一个合并
----------------

1. 如果你觉得你合并后的状态是一团乱麻,想把当前的修改都放弃,你可以用下面的命令回到合并之前的状态： ::
    
     $ git reset --hard HEAD    # 撤销上一次提交
     $ git reset --hard HEAD^   # 撤销上上次提交

#. 或者你已经把合并后的代码提交,但还是想把它们撒销： ::

     $ git reset --hard ORIG_HEAD

  .. ttip::

     但是这条命令在某些情况会很危险,如果你把一个已经被另一个分支合并的分支给删了,那么 以后在合并相关的分支时会出错。

#. 或者你只要回复一个文件，如"hello.c"： ::

     $ git checkout -- hello.c



rebase
---------

1. 在rebase的过程中,也许会出现冲突(conflict)。 在这种情况，Git会停止rebase并会让你去解决冲突；在解决完冲突后，使用一下命令完成rebase：  ::

    git add
    git rebase --continue

#. 在任何时候，你可以用--abort参数来终止rebase的行动，并且"mywork" 分支会回到rebase开始前的状态： ::

    $ git rebase --abort

跟踪分支
----------

  * $ git checkout --track origin/serverfix  或

  * $ git checkout -b sf origin/serverfix   # 分支重命名为sf

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

   .. ttip::

      上面命令中带了 ``--global`` 参数，这就意味是在进行全局配置，它会影响本机上的每个一个Git项目。如果没有 ``--global`` 表示本项目的配置。

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

#. 从svn更新： ::

   $ git checkout master
   $ git svn rebase


