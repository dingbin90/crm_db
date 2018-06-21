#!/usr/bin/env python
# coding=utf-8

import datetime, os, sys, shutil, time

from util import *

def stopapp(group_name):
    stop_cmd = '''ansible %s -m shell -a "/bin/bash /usr/local/apache-tomcat/bin/shutdown.sh"''' %(group_name)
    os.system(stop_cmd)
    time.sleep(5)


def startapp(group_name):
    start_cmd = '''ansible %s -m shell -a "nohup /usr/local/apache-tomcat/bin/startup.sh &"''' %(group_name)
    os.system(start_cmd)


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

if __name__ == '__main__':
    # if you want to change module,you must change two variables

    # 发版的模块
    modulename = 'purchase-web'

    # 存放war的目录
    war_dir = "/jenkins/warversion"

    # ansible 推的主机组
    group_name = 'neiwang'

    # this is a dir
    logname = './log/deploy_%s_info.log' % group_name

    # 具体war的文件位置
    filename = '%s/%s-1.0.0.war' % (war_dir, modulename)
    # if you want to change project,you must modify this variable

    # Jenkins打包的war包位置
    source_file = "/root/.jenkins/jobs/neiwang-test/workspace/%s/target/%s-1.0.0.war" % (
    modulename, modulename)

    # war包存放的位置
    remote_dir = "/jenkins/warversion"
    jarpath = "/jenkins/warversion"
    # -------rename war--------------

 #   发版前war包备份，加时间格式
    fileRename(filename)
# -----copy war------

#拷贝Jenkins打包的文件到war包存放的位置
    shutil.copy(source_file, remote_dir)
# ------scp war to dest dir cmd----------

# 删除目录命令
    rm_cmd = '''ansible %s -m file -a "path=/usr/local/apache-tomcat/webapps/purchase-web-1.0.0 state=absent" ''' % (
    group_name)

# 删除远程的war包的命令
    rm_war_cmd = '''ansible %s -m file -a "path=/usr/local/apache-tomcat/webapps/purchase-web-1.0.0.war state=absent" ''' % (
    group_name)

# 拷贝war包到远程机器的命令
     copy_cmd = '''ansible %s -m copy -a "src=%s dest=/usr/local/apache-tomcat/webapps/purchase-web-1.0.0.war owner=admin group=admin mode=0644"''' % (
     group_name, filename)

# ---stop app-----
     stopapp(group_name)
     time.sleep(3)
     res_dic = checkApp(group_name)
     for k in res_dic.keys():
         if int(res_dic[k]) == 0:
             msg = 'host %s stop app successfully' % k
             dealMsg(logname, msg)
         else:
             msg = 'host %s stop app failed' % k
             dealMsg(logname, msg)
             sys.exit()
# ---scp app to dest---
msg = 'start delete app'
dealMsg(logname, msg)
os.system(rm_cmd)
os.system(rm_war_cmd)
msg = 'start copy app'
dealMsg(logname, msg)
os.system(copy_cmd)
# ---start app---------
startapp(group_name)
time.sleep(3)
res_dic = checkApp(group_name)
for k in res_dic.keys():
    if int(res_dic[k]) == 1:
        msg = 'host %s start app successfully' % k
        dealMsg(logname, msg)
    else:
        msg = 'host %s start app failed' % k
        dealMsg(logname, msg)
