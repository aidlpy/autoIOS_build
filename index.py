#!/usr/bin/env python

import requests
import os
import webbrowser
import time
import subprocess


# 打包后的ipa文件路径
backupIPA = '/Users/admin/Desktop/CityPartner/IPA'
# 应用对应蒲公英路径
openUrlPath = 'https://www.pgyer.com/manager/dashboard/app/6e1b29900417dbf7d5e435cdcc8e2edf'
# 应用下载页
openDownLoadUrlPath = 'https://www.pgyer.com/eoO4'
# 项目scheme
schemeName = 'CityPartner'
# 蒲公英账号USER_KEY、API_KEY及App_Key

USER_KEY = '6e70fde3a4dddb27279e48120d44c983'
API_KEY = '662dbe1bf471f5c2de9452c7ed6b0105'
App_Key = '6e1b29900417dbf7d5e435cdcc8e2edf'

# clean工程
def cleanPro():

    start = time.time()
    if desDev == 1:
        desDvStr = 'Release'
    else:
        desDvStr = 'Debug'

    # cleanProRun = 'xcodebuild clean -project %s.xcodeproj -scheme %s ' \
                  #'-configuration %s'%(schemeName,schemeName,desDvStr)
    # workspace工程
    cleanProRun = 'xcodebuild clean -workspace %s.xcworkspace -scheme %s ' \
                  '-configuration %s'%(schemeName,schemeName,desDvStr)
    print('%s' % cleanProRun)
    cleanProRun = subprocess.Popen(cleanProRun, shell=True)
    cleanProRun.wait()
    end = time.time()
    cleanReturnCode = cleanProRun.returncode
    print('%s' % cleanReturnCode)

    if  cleanReturnCode != 0:
        print("\n***************clean失败******耗时:%s秒***************\n" % (end - start))
    else:
        print("\n***************clean成功*********耗时:%s秒************\n" % (end - start))

    archive()


# archive工程
def archive():


    # 删除之前打包的ProgramIpa文件夹
    subprocess.call(["rm","-rf", backupIPA])
    time.sleep(1)

    #在桌面上创建ProgramIpa文件夹
    mkdir(backupIPA)
    # subprocess.call(["mkdir","-p",backupIPA])
    time.sleep(1)
    start = time.time()
    # xcodeproj工程
    # archiveRun = 'xcodebuild archive -project %s.xcodeproj -scheme %s -archivePath ./build/%s.xcarchive'%(schemeName,schemeName,schemeName)
    # archiveRun = 'xcodebuild archive -project %s.xcodeproj -scheme %s -archivePath %s/%s.xcarchive' % (
    # schemeName, schemeName, backupIPA, schemeName)
    # workspace工程
    archiveRun = 'xcodebuild archive -workspace %s.xcworkspace -scheme %s' \
                 ' -archivePath %s/%s.xcarchive'%(schemeName,schemeName,backupIPA,schemeName)
    print("%s" % archiveRun)
    archiveProcessRun = subprocess.Popen(archiveRun, shell=True)
    archiveProcessRun.wait()

    end = time.time()
    # 获取Code码
    archiveReturnCode = archiveProcessRun.returncode
    print('%s' % archiveReturnCode)
    if archiveReturnCode != 0:

        print("\n***************archive失败******耗时:%s秒***************\n" % (end - start))

    else:

        print("\n***************archive成功*********耗时:%s秒************\n" % (end - start))

    exportIPA()



def exportIPA():

    start = time.time()

    exportRun = 'xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s/%s -exportOptionsPlist ./ExportOptions.plist' % (
    backupIPA, schemeName, backupIPA, schemeName)

    print('++++++%s' % exportRun)

    exportProcessRun = subprocess.Popen(exportRun, shell=True)

    exportProcessRun.wait()

    # 结束时间

    end = time.time()

    # 获取Code码

    exportReturnCode = exportProcessRun.returncode

    if exportReturnCode != 0:

        print("\n***************导出IPA失败*********耗时:%s秒************\n" % (end - start))

    else:

        print("\n***************导出IPA成功*********耗时:%s秒************\n" % (end - start))

    os.chdir(backupIPA)
    # 移除xcarchive
    subprocess.getoutput('rm -rf ./*.xcarchive')
    time.sleep(1)
    uploadIPA('%s/%s/%s.ipa' % (backupIPA, schemeName, schemeName))

# 上传蒲公英

def uploadIPA(IPAPath):

    if (IPAPath == ""):

        print("\n***********************************没有找到关联IPA包******************************************\n")
        return
    else:

        print("\n***********************************IPA包开始上传到蒲公英**************************\n")
        url = 'http://www.pgyer.com/apiv1/app/upload'
        data = {
            'uKey':USER_KEY,
            '_api_key':API_KEY,
            'installType':'2',
            'password':'123456',
            'updateDescription':'des'
        }

        files = {'file':open(IPAPath, 'rb')}
        r = requests.post(url, data=data, files=files)


def openDownloadUrl():

    webbrowser.open('%s%s' % (openUrlPath, App_Key), new=1,autoraise=True)
    time.sleep(3)
    webbrowser.open(openDownLoadUrlPath,new=1,autoraise=True)
    print("\n*************** IPA上传更新成功 *********************\n")



def mkdir(backupIPA):

    isExists = os.path.exists(backupIPA)

    if not isExists:
        os.makedirs(backupIPA)
        print(backupIPA+'创建成功')
        return True
    else:
        print(backupIPA + '目录已经存在')
        return False


if __name__ == '__main__':

    des = input("请输入更新的日志描述:")
    desDev = input('请输入编译环境 1、Release 2、Debug:')
    cleanPro()
