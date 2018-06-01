import os,time,shutil
#python 2的脚本
modulename = 'purchase_portal_web'
group_name = "twebapp"
#提取上一个版本的war包
def old_war():
    war_list = []
    dir = '/jenkins/warversion/'
    list = os.listdir(dir)
    for i in list:
        if i.startswith(modulename):
            war_list.append(i)
    war = sorted(war_list)
    # return war[-1].split("_2")[0]
    #print war[-1]
    return war[-1]

def roll_back():
    war_dir = "/jenkins/warversion/"
    war = old_war()
    new_name = war.split("_2")[0]
    new_path = '/jenkins/war_backup/' + new_name
    war_dir = war_dir + war
    shutil.copy(war_dir, new_path)
    # filename = '%s/%s-0.0.1-SNAPSHOT.war' % (war_dir,modulename)
    rm_cmd = '''ansible %s -m file -a "path=/home/admin/taobao-tomcat-production-7.0.59.3/deploy/ROOT state=absent" '''  %(
        group_name)
    #
    rm_war_cmd='''ansible %s -m file -a "path=/home/admin/taobao-tomcat-production-7.0.59.3/deploy/ROOT.war state=absent" ''' %(group_name)
    #
    copy_cmd='''ansible %s -m copy -a "src=%s dest=/home/admin/taobao-tomcat-production-7.0.59.3/deploy/ROOT.war owner=admin group=admin mode=0644"''' %(group_name,new_path)
    print ("开始删除远程主机文件")
    os.system(rm_cmd)
    time.sleep(1)
    print ("开始删除远程的war包")
    os.system(rm_war_cmd)
    time.sleep(1)
    print ("开始拷贝war包")
    os.system(copy_cmd)
if __name__ == "__main__":
    roll_back()

