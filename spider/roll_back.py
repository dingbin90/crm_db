#!/usr/bin/env python
#coding=utf-8
import os,time
modulename = 'purchase_portal_web'


def old_war():
    war = []
    dir = '/jenkins/warversion/'
    patten = "purchase_purchase_web"
    list = os.listdir(dir)
    for i in list:
        if i.startswith(patten):
            war.append(i)
    war = sorted(war)
    # return war[-1].split("_2")[0]
    return war[-1]







def roll_back():
    # war_dir = "/jenkins/warversion"
    # group_name = "twebapp"
    # filename = '%s/%s-0.0.1-SNAPSHOT.war' % (war_dir,modulename)
    # rm_cmd = '''ansible %s -m file -a "path=/home/admin/taobao-tomcat-production-7.0.59.3/deploy/ROOT state=absent" '''  %(
    #     group_name)
    #
    # rm_war_cmd='''ansible %s -m file -a "path=/home/admin/taobao-tomcat-production-7.0.59.3/deploy/ROOT.war state=absent" ''' %(group_name)
    #
    # copy_cmd='''ansible %s -m copy -a "src=%s dest=/home/admin/taobao-tomcat-production-7.0.59.3/deploy/ROOT.war owner=admin group=admin mode=0644"''' %(group_name,filename)
    # print ("开始删除远程主机文件")
    # os.system(rm_cmd)
    # time.sleep(1)
    # print ("开始删除远程的war包")
    # os.system(rm_war_cmd)
    # time.sleep(1)
    # print ("开始拷贝war包")
    # os.system(copy_cmd)
    war =old_war()
    cmd = "cp war /root/"
    os.system(cmd)


if __name__ == "__main__":
    roll_back()



