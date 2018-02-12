#coding: utf-8
import sys
import os
import platform
import logging

def daemonize ():
    sysstr = platform.system()
    if sysstr != "Linux" :
        logging.warn("can not deamonize,platform="+sysstr)
        return

    try:
        pid = os.fork()
          # 父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
        if pid > 0:
            # 父进程退出
            sys.exit(0)
    except OSError, e:
        sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

    # 从母体环境脱离
    os.chdir("./") # chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
    os.umask(0)    # 调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.setsid()    # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。

    # 执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            # 第二个父进程退出
            sys.exit(0)
    except OSError, e:
        sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

     # 进程已经是守护进程了，重定向标准文件描述符
    for f in sys.stdout, sys.stderr: f.flush()
