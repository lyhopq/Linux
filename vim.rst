vim 技巧
==========


记忆
-------

* ``K`` 查看man手册
* ``:Man xxx`` 在新窗口中查看man手册
* ``ga`` 查看ascii值
* ``g CTRL-G`` 统计字数，使用Visual模式选取统计部分
* ``q:`` 打开历史记录窗口
* ``:marks`` 打开编辑标记窗口， ```0`` 准确回到上一次退出vim的位置
* ``gf`` 打开光标下的指定文件， ``CTRL-W f`` 在新窗口中打开
* 格式转换： ``:set fileformat=unix``
* 断行： ``:set textwidth=70``
* 重新格式化： ``gq`` 如： ``gqap`` 格式化一段， ``gggqG`` 格式化整个文档
* 增加/减少缩进： ``>>/<<``
* 块编辑： ``:set virtualedit=all`` ， 退出 ``:set virtualedit=`` 。特别适用于表格编辑
* ``gv`` 再次选定上次选择的Visual区域
* ``CTRL-A`` ， ``CTRL-X`` 对数字加/减
* ``ls | vim -`` 从标准输入读取要编辑的内容
* ``\c, \C`` 忽略/不忽略大小写匹配
* ``/`` 重复前一次搜索
* ``zM`` 关闭所有折行， ``zR`` 打开所有折行， ``zo, zc`` 打开，关闭某个折行
* 剪切版： ``"xy`` 复制到x缓冲区， ``"xp`` 粘贴x缓冲区

替换
------

* ``:20,100s/bc/a&d/g``
  
  .. note::
  
       - ``&`` 是一个特殊字符，表示被替换的内容。结果为把bc替换成abcd
       - 如果要替换成"a&d"的话，需要用 ``\&`` 将&转义

* ``:%s/(\(\d+\))/\="(".(submatch(1)+1).")"/g``
  
  .. note::

       * 作用： ::

            将“(1), ...., (2), ....,(100)”替换成“
            (2), ...., (3), ...., (101)”。 
            即括号里的序号数字都加一。

       * 解释如下： ::

           %       全文（“%”是“1，$”范围的缩写）
           s       替换
           /       搜索字符串开始
           (       左括号
           \(      开始记录匹配
           \d+     一个或多个数字
           \)      结束记录匹配
           )       右括号
           /       搜索字符串结束
           \=      把后面的表达式计算出来作为替换字符串
           "("     左括号
           .       字符串连接运算符
           (submatch(1)+1)       把第一个匹配的结果加一作为一个整体返回
           .")"    添上右括号
           /g      替换字符串结束，g表示替换每一行的所有匹配结果。

* 消除多余空格 ::

    :%s/\s\+$//  # "\s\+$"位于行尾的一个或多个空白字符

替换多个文件中的目标
---------------------

案例：将所有cpp文件中的"aaaa"替换为"bbb"。 ::

    vim *.cpp          # 启动vim，同时指定了要编辑的文件列表
    qa                 # 开始宏记录
    :%s/\<aaa\>/bbb/ge # 在第一个文件中执行替换操作。使用‘e’在没有匹配目标时也不会报错
    :wnext             # 保存该文件并转到下一个文件进行编辑
    q                  # 停止宏记录
    @a                 # 执行名为a的宏。看看整个过程有没有错
    999@a              # 对其余文件执行同样操作

部分交换
-----------

案例： ::

    Doe, John       ====>        John Doe
    Smith, Peter                 Peter Smith

    在vim中只需一条命令：
    ``:%s/\([^,]*\), \(.*\)/\2 \1/``  # 可以使用的反向引用为9个，"\0"特指整个匹配到的内容

排序
------

通过外部程序 ``sort`` 对行排序 ::

    :.,/^$/-1!sort

.. note::

    ``.,/^$/-1``  选取的范围是自改行直至下一个空行。也可以在Visual模式下选取要排序的行

反转行序
---------

* 将所有行移到第0行后面 ::

    :g/^/m 0

* 将连续行移到某一行的后面 ::

    mt                  # 标记“某一行”
    [n]j                # 移到“连续行”的最后一行
    :`t+1,.g/^/m `t

.. note::

    - "g"  对范围内的所有行进行操作
    - "^"  匹配一行的开头
    - "m 0" 或 "m \`t" 移到第0（\`t）行之后 


项目管理
----------

* 会话：session

  * 保存当前会话： ``:wa`` 后 ``:mks``
  
    - 会在当前目录下生成"Session.vim"脚本文件
    - ``:mks filename`` 产生"filename"脚本文件
  * 恢复会话： ``:so Session.vim`` 或 ``vim -S Session.vim``
  * 切换会话： ::
     
      :wall
      :mks! ~/.vim/secret.vim
      :so ~/.vim/boring.vim
  
* 记住编辑信息：viminfo

  - 保存信息： ``:wviminfo ~/tmp/test.viminfo``   
  - 读取信息： ``:rviminfo ~/tmp/test.viminfo``  
* 视图：view

  - 保存视图： ``:mkview 1`` 或 ``:mkview ~/.vim/main.vim``
  - 恢复视图： ``:loadview 1`` 或 ``:so ~/.vim/main.vim``

* 缓冲区：buffer
  
  - 显示缓冲区列表： ``:buffer`` 或 ``:ls`` , ``:ls!``

    | 输出为： 
    
    ::

      :ls
         1  h   "[未命名]"                     第 1 行
         2 %a + "Proj/Uliweb/mysite/apps/Notes/files/Ubuntu/vim.rst" 第 145 行
         3 #h   "Proj/Uliweb/mysite/apps/Notes/files/Ubuntu/imagemagick.rst" 第 23 行
         4  h   "im"                           第 0 行

  - 编辑一个缓冲区： 
    
    - ``:buffer 2``  
    - ``:buffer im``
    - ``:sbuffer 3``  # 新窗口
  - 遍历缓冲区：

    - ``：bnext``      下一个缓冲区
    - ``：bprevious``  前一个缓冲区
    - ``：bfirst``     第一个缓冲区
    - ``：blast``      最后一个缓冲区
  - 删除缓冲区： ``:bdelete 3``

查找一个word在何处被引用
-------------------------

案例：希望编辑所有包含了"frame_counter"的c文件 ::

    vim `grep -1 frame_counter *.c`
    或
    :grep frame_counter *.c

.. note::

    - "-1" 使grep的输出只包含文件名而不显示匹配的行
    - “`”  反向引用符号，运行其中的命令，并将命令的结果作为当前命令的一部分
    - "grep" vim中的一个内部命令。
    - ``:next`` 和 ``:first`` 来遍历文件列表
    - 结合 ``:cnext, :cprev, :clist``  遍历所有匹配

加密
-----

* 加密：

  - 方法一： ``vim -x test.txt``
  - 方法二： ``:X``
* 解密： ``:set key=``

二进制文件
----------

* ``vim -b datafile``

  | ``:set display=uhex`` 以十六进制格式显示
* 使用xxd程序 ::

    vim -b datafile
    :%!xxd

自动补全
--------

* 补全单词： ``CTRL-P`` ， ``CTRL-N``
* 补全特殊的文档元素： ::

    CTRL-X CTRL-F 文件名
    CTRL-X CTRL-L 整行内容
    CTRL-X CTRL-D 宏定义(也包括那些在include文件里定义的宏)
    CTRL-X CTRL-I 当前文件和被当前文件include的文件
    CTRL-X CTRL-K 来自一个字典文件的word
    CTRL-X CTRL-T 来自一个thesaurus的word
    CTRL-X CTRL-] tags
    CTRL-X CTRL-V Vim的命令行

* 智能补全： ``CTRL-X CTRL-O``  常用在c源码中:w

缩写
----

* 定义缩写： ``:iabbrev lyh lyhopq@gmail.com``
* 列出以定义缩写： ``abbreviate``
* 删除缩写： ``unabbreviate lyh``
* 更正打字错误： ``abbreviate teh the``
* 移除所有缩写： ``:abclear``

文本对齐
---------

* 居中对齐： ``:{range}center [width]`` 例： ``:1,5center 40``
* 左/右对齐： ``:left/right``
* 左右对齐： 

  - 使用宏： ``:runtime macros/justify.vim``

    | 在Visual模式下选定格式化文本，然后执行 ``_j``
  - 使用外部程序： ``:%!fmt``


对多个文件做同样的改动
-----------------------

* 案例1：把多个C文件中名为"x_cnt"的变量都改为"X_counter"  ::

    :args *.c
    :argdo %s/\<x_cnt\>/x_counter/ge | update
  
  .. note::
  
    * ``args *.c`` 把所有要改的文件放到参数列表上
    * ``:argdo`` 以另一个命令为参数，该命令将对所有待编辑的文件都执行一次
    * ``|`` 用来分割两个命令
    * ``update`` 在文件有所改变时进行保存
    * 类似于 ``:argdo`` 
  
      - ``:windo`` 对所有窗口执行同样的操作
      - ``:bufdo`` 对所有缓冲区进行操作， ``这个要小心使用`` ，最好用 ``:ls`` 看一下有哪些缓冲区会被改动
  
* 案例二：将多个文件中的"-person-"都改为"Jones"其后打印出来

  #. 将要执行的vim命令（Ex模式）放入"change.vim"中  ::

      %s/-person-/Jones/g
      write tempfile
      quit

  #. 以批处理模式运行vim

     .. code:: bash

        for file in *.txt; do
          vim -e -s $file < change.vim # "-e"Ex模式， “-s”告诉vim安静地运行
          lpr -r tempfile              # 打印"tempfile"的内容，然后删除它("-r")
        done

搜索
------

* 偏移

  - ``/default/2`` 将光标停留在目标行向下的第二行
  - ``/const/e-1`` "e"使光标在找到目标串后以它的结尾作为移动的起始处
  - ``/const/b+2`` "b"目标串开头为起始处
  - ``//e`` 重复前一次搜索使用不同的偏移
  - ``?const?e-2`` 反向搜索必须以"?"来分割命令的不同部分

* 多次匹配

  - ``/ab*`` "*"匹配任意个（零个或多个）b
  - ``/\(ab\)*`` "ab"作为整体
  - ``/ab\+`` "\+"至少一次
  - ``/folders\=`` "\="一次或零次
  - ``/ab\{m,n}`` 匹配至少m次，至多n次
  - ``/foo\|bar`` "\|"模式中的或操作
* 字符范围： 
  
  - ``/[a-z]`` ，使用"^"指定补集
  - 预定义字符集 ::

      \d 数字 [0-9] 
      \D 非数字 [^0-9] 
      \x 十六进制数 [0-9a-fA-F] 
      \X 非十六进制数 [^0-9a-fA-F] 
      \s 空白字符 [ ] (<Tab> 和<Space>)
      \S 非空白字符 [^ ] (除 <Tab> 和 <Space>之外)
      \l 小写字母 [a-z] 
      \L 非小写字母 [^a-z] 
      \u 大写字母 [A-Z] 
      \U 非大写字母 [^A-Z] 
* 匹配一个断行：通过前缀"\_"来同时包括断行，例： ``/the\_s\+word`` 匹配断行或多个空白字符


之于程序
----------

* tags

  * 跳转： ``CTRL-W ]`` 分割当前窗口并跳转到光标下的tag， ``:tnext`` 下一个符合条件的地方， ``:tselect tagname`` 列出所有符合条件的地方
  * 搜索： ``:tag /xxx`` ，然后按<Tab>
  * 预览窗口： ``ptag tagname`` ，关闭窗口 ``:pclose`` ， ``:pedit defs.h`` 在预览窗口中编辑一个文件， ``:psearch popen`` 在预览窗口中显示搜索内容
  
* 程序中的移动

  * ``[#,]#`` ``#if`` 内的移动
  * ``[[,]]`` ``{}`` 内的移动
  * ``[(,])`` ``()`` 内的移动
  * ``[/,]/``  注释内的移动

* 查找标识符

  - ``[I`` 查找全局标识符，光标放在要查找的标识符上
  - ``[<tab>`` 同 ``[I`` ，但它跳转到第一个匹配项
  - ``[D`` 只查找以"#define"定义的
  - ``gD`` 搜索限制在当前文件， ``gd`` 当前函数

* 编译

  - 编译： ``:make {arguments}``
  - 错误： ``:cnext``, ``:cc``, ``:clist``, ``:clist!``, ``:cprevious``, ``:cfirst``, ``:clast``, ``:cc [n]``
  - 错误列表： ``:colder``, ``:cnewer``

* 缩进： ``==`` ， ``=a{`` ， ``gg=G``
