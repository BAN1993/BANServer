#coding: utf-8
import sys
import os

def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
     #�ض����׼�ļ���������Ĭ������¶���/dev/null��
    try: 
        pid = os.fork() 
          #������(�Ự��ͷ�����)�˳�������ζ��һ���ǻỰ��ͷ�������Զ�������»�ÿ����նˡ�
        if pid > 0:
            sys.exit(0)   #�������˳�
    except OSError, e: 
        sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

     #��ĸ�廷������
    os.chdir("./")  #chdirȷ�Ͻ��̲������κ�Ŀ¼��ʹ��״̬��������umountһ���ļ�ϵͳ��Ҳ���Ըı䵽�����ػ�����������Ҫ���ļ�����Ŀ¼
    os.umask(0)    #����umask(0)�Ա�ӵ�ж���д���κζ�������ȫ���ƣ���Ϊ��ʱ��֪���̳���ʲô����umask��
    os.setsid()    #setsid���óɹ��󣬽��̳�Ϊ�µĻỰ�鳤���µĽ����鳤������ԭ���ĵ�¼�Ự�ͽ��������롣

     #ִ�еڶ���fork
    try: 
        pid = os.fork() 
        if pid > 0:
            sys.exit(0)   #�ڶ����������˳�
    except OSError, e: 
        sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

     #�����Ѿ����ػ������ˣ��ض����׼�ļ�������

    for f in sys.stdout, sys.stderr: f.flush()
    #si = open(stdin, 'r')
    #so = open(stdout, 'a+')
    #se = open(stderr, 'a+', 0)
    #os.dup2(si.fileno(), sys.stdin.fileno())    #dup2����ԭ�ӻ��رպ͸����ļ�������
    #os.dup2(so.fileno(), sys.stdout.fileno())
    #os.dup2(se.fileno(), sys.stderr.fileno())
