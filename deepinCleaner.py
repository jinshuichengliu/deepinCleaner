#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018年10月12日

@author: marks
"""

"""
"""
import os
import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets


def userask(askstring: str, isanswer: bool = True, yesno: bool = True) -> bool:
    '''
    :param askstring: 给用户的提示
    :param isanswer:  是否需要用户回答
    :param yesno:  默认选择Y或N
    :return: True or False
    '''
    needanswer = ""
    if isanswer:
        if yesno:
            needanswer = "Y/n"
        else:
            needanswer = "y/N"

    while True:
        print(askstring, needanswer, "? ", end="")
        userin = input()
        if isanswer == False:
            return True

        if userin not in ["", "y", "Y", "n", "N"]:
            continue
        if userin == "y" or userin == "Y":
            return True
        elif userin == "n" or userin == "N":
            return False
        elif yesno:
            return True
        else:
            return False

def getHomePath():
    # os.path.expandvars('$HOME')
    # os.path.expanduser('~')
    return os.environ['HOME']


def getDeepinVersion():
    # /home/marks/.config/deepin/dde-welcome.conf
    with open(os.path.join(getHomePath(), ".config/deepin/dde-welcome.conf"), "r") as rfile:
        # Version=15.8
        for line in rfile:
            if line.startswith("Version") == True:
                version = line.split("=")
                return version[1].strip()
    return None


def setWindowSize():
    homepath = getHomePath()
    ret = ""
    # 设置窗口大小
    # window_height = 864
    # window_width = 1440
    height = 4000
    width = 4000
    with open(os.path.join(homepath, ".config/deepin/deepin-system-monitor/config.conf"), "r") as rfile:
        for line in rfile.readlines():
            if line.startswith("window_height"):
                theight = line.split("=")
                height = theight[1].strip()
                # print("新的窗口高： %s" % height)
            if line.startswith("window_width"):
                twidth = line.split("=")
                width = twidth[1].strip()
                # print("窗口宽： %s" % width)

    ddefmjson = None
    with open(os.path.join(homepath, ".config/deepin/dde-file-manager/dde-file-manager.obtusely.json"),
              "r") as rfile:
        ddefmjson = json.load(rfile)
        # print("窗口原分辨率为：%d x %d"%(ddefmjson["WindowManager"]["WindowState"]["width"], ddefmjson["WindowManager"]["WindowState"]["height"]))
        ret += "原窗口大小为：%s × %s\n" % (ddefmjson["WindowManager"]["WindowState"]["width"], ddefmjson["WindowManager"]["WindowState"]["height"]) + "新窗口大小为：%s × %s" % (width, height)
        ddefmjson["WindowManager"]["WindowState"]["height"] = height
        ddefmjson["WindowManager"]["WindowState"]["width"] = width

    with open(os.path.join(homepath, ".config/deepin/dde-file-manager/dde-file-manager.obtusely.json"),
              "w") as wfile:
        wfile.write(json.dumps(ddefmjson, sort_keys=True, indent=4, separators=(',', ': ')))
    return ret


def cleanSearchAndViewHistory():
    homepath = getHomePath()
    ret = ""
    # 清除搜索记录和浏览记录
    ddefmjson = None
    with open(os.path.join(homepath, ".config/deepin/dde-file-manager/dde-file-manager.obtusely.json"),
              "r") as rfile:
        ddefmjson = json.load(rfile)
        # print("共删除搜索记录：%d 条"%len(ddefmjson["Cache"]["SearchHistroy"]))
        # print("共删除窗口设置记录：%d 条"%len(ddefmjson["FileViewState"]))
        ret += "共删除搜索记录：%d 条\n"%len(ddefmjson["Cache"]["SearchHistroy"])
        ret += "共删除窗口设置记录：%d 条"%len(ddefmjson["FileViewState"])
        ddefmjson["Cache"]["SearchHistroy"] = []
        ddefmjson["FileViewState"] = {}

    with open(os.path.join(homepath, ".config/deepin/dde-file-manager/dde-file-manager.obtusely.json"),
              "w") as wfile:
        wfile.write(json.dumps(ddefmjson, sort_keys=True, indent=4, separators=(',', ': ')))
    return ret


def cleanLogFiles():
    homepath = getHomePath()
    ret = ""
    # 清除deepin日志文件
    delcount = 0
    getspace = 0
    for root, dirs, files in os.walk(os.path.join(homepath, ".cache/deepin")):
        for file in files:
            if (file.endswith(".log") == True) or (file.find(".log.") != -1 and file[-1].isalnum() == True):
                newpath = os.path.join(root, file)
                delcount += 1
                getspace += os.path.getsize(newpath)
                os.remove(newpath)

    # print("共删除日志文件： %d 个" % delcount)
    # print("共释放空间： %.3f M" % (getspace / 1024 / 1024))
    ret += "共删除日志文件： %d 个\n" % delcount
    ret += "共释放空间： %.3f M" % (getspace / 1024 / 1024)
    return ret


def cleanThumbnailFiles():
    homepath = getHomePath()
    ret = ""
    # 清除deepin缩略图
    delcount = 0
    getspace = 0
    for root, dirs, files in os.walk(os.path.join(homepath, ".cache/thumbnails")):
        for file in files:
            if file.endswith(".png") == True:
                newpath = os.path.join(root, file)
                delcount += 1
                getspace += os.path.getsize(newpath)
                os.remove(newpath)

    # print("共删除缩略图文件： %d 个" % delcount)
    # print("共释放空间： %.3f M" % (getspace / 1024 / 1024))
    ret += "共删除缩略图文件： %d 个\n" % delcount
    ret += "共释放空间： %.3f M" % (getspace / 1024 / 1024)
    return ret


def cleanRecentOpen():
    homepath = getHomePath()
    ret = ""
    # 清除最近打开
    # ~/.local/share/recently-used.xbel
    os.remove(os.path.join(homepath, ".local/share/recently-used.xbel"))
    ret += "尽量关闭所有打开的文件，否则清除最近打开记录会失败！！！\n如发现清除失败，请继续关闭打开的文件，并重试！！！"
    return ret


def cleanAptCache():
    homepath = getHomePath()
    ret = ""
    # /var/lib/apt/lists
    # /var/cache/apt
    # /var/lib/lastore/safecache
    # 以上目录下所有文件，除了名字为lock的
    # 清除apt缓存
    delcount = 0
    getspace = 0
    varpathlist = ["/var/lib/apt/lists", "/var/cache/apt", "/var/lib/lastore/safecache"]
    for varpath in varpathlist:
        for root, dirs, files in os.walk(varpath):
            for file in files:
                if file != "lock":
                    newpath = os.path.join(root, file)
                    delcount += 1
                    getspace += os.path.getsize(newpath)

                    try:
                        os.remove(newpath)
                    except:
                        return "清除深度商店缓存失败，请以管理员权限重新运行本工具！！！"

    ret += "共删除深度商店缓存文件： %d 个\n" % delcount
    ret += "共释放空间： %.3f M" % (getspace / 1024 / 1024)
    return ret


class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)

        # 设置窗口大小
        # window_height = 864
        # window_width = 1440
        self.pbtnSetWindowSize = QtWidgets.QPushButton(Form)
        self.pbtnSetWindowSize.setGeometry(QtCore.QRect(10, 10, 120, 30))
        self.pbtnSetWindowSize.setObjectName("pbtnSetWindowSize")

        # 清除搜索记录和浏览记录
        self.pbtnCleanSearchAndViewHistory = QtWidgets.QPushButton(Form)
        self.pbtnCleanSearchAndViewHistory.setGeometry(QtCore.QRect(140, 10, 120, 30))
        self.pbtnCleanSearchAndViewHistory.setObjectName("pbtnCleanSearchAndViewHistory")

        # 清除deepin日志文件
        self.pbtnCleanLogFiles = QtWidgets.QPushButton(Form)
        self.pbtnCleanLogFiles.setGeometry(QtCore.QRect(270, 10, 120, 30))
        self.pbtnCleanLogFiles.setObjectName("pbtnCleanLogFiles")

        # 清除deepin缩略图
        self.pbtnCleanThumbnailFiles = QtWidgets.QPushButton(Form)
        self.pbtnCleanThumbnailFiles.setGeometry(QtCore.QRect(10, 50, 120, 30))
        self.pbtnCleanThumbnailFiles.setObjectName("pbtnCleanThumbnailFiles")

        # 清除最近打开
        self.pbtnCleanRecentOpen = QtWidgets.QPushButton(Form)
        self.pbtnCleanRecentOpen.setGeometry(QtCore.QRect(140, 50, 120, 30))
        self.pbtnCleanRecentOpen.setObjectName("pbtnCleanRecentOpen")

        # 清除Apt缓存
        self.pbtnCleanAptCache = QtWidgets.QPushButton(Form)
        self.pbtnCleanAptCache.setGeometry(QtCore.QRect(270, 50, 120, 30))
        self.pbtnCleanAptCache.setObjectName("pbtnCleanAptCache")

        # 清除以上所有
        self.pbtnCleanAboveAll = QtWidgets.QPushButton(Form)
        self.pbtnCleanAboveAll.setGeometry(QtCore.QRect(10, 90, 120, 30))
        self.pbtnCleanAboveAll.setObjectName("pbtnCleanAboveAll")

        # 显示反馈信息
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(10, 130, 380, 160))
        self.textBrowser.setObjectName("textBrowser")

        self.pbtnSetWindowSize.clicked.connect(self.btnclkSetWindowSize)
        self.pbtnCleanSearchAndViewHistory.clicked.connect(self.btnclkCleanSearchAndViewHistory)
        self.pbtnCleanLogFiles.clicked.connect(self.btnclkCleanLogFiles)
        self.pbtnCleanThumbnailFiles.clicked.connect(self.btnclkCleanThumbnailFiles)
        self.pbtnCleanRecentOpen.clicked.connect(self.btnclkCleanRecentOpen)
        self.pbtnCleanAptCache.clicked.connect(self.btnclkCleanAptCache)
        self.pbtnCleanAboveAll.clicked.connect(self.btnclkCleanAboveAll)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Deepin垃圾清理工具"))
        self.pbtnSetWindowSize.setText(_translate("Form", "文管窗口最大化"))
        self.pbtnCleanSearchAndViewHistory.setText(_translate("Form", "清除搜索和浏览历史"))
        self.pbtnCleanLogFiles.setText(_translate("Form", "清除深度系列日志"))
        self.pbtnCleanThumbnailFiles.setText(_translate("Form", "清除所有深度缩略图"))
        self.pbtnCleanRecentOpen.setText(_translate("Form", "清除最近打开记录"))
        self.pbtnCleanAptCache.setText(_translate("Form", "清除深度商店缓存"))
        self.pbtnCleanAboveAll.setText(_translate("Form", "清除以上所有内容"))
        self.textBrowser.setText(_translate("Form", "所有操作都需要关闭文管或重启文管才能生效！！！\n清除深度商店缓存需要管理权限，请以管理权限启动本工具！！！\n本清理工具目前只适用于15.7和15.8版本。"))

    def btnclkSetWindowSize(self):
        ret = setWindowSize()
        self.textBrowser.setText(ret)

    def btnclkCleanSearchAndViewHistory(self):
        ret = cleanSearchAndViewHistory()
        self.textBrowser.setText(ret)

    def btnclkCleanLogFiles(self):
        ret = cleanLogFiles()
        self.textBrowser.setText(ret)

    def btnclkCleanThumbnailFiles(self):
        ret = cleanThumbnailFiles()
        self.textBrowser.setText(ret)

    def btnclkCleanRecentOpen(self):
        ret = cleanRecentOpen()
        self.textBrowser.setText(ret)

    def btnclkCleanAptCache(self):
        ret = cleanAptCache()
        self.textBrowser.setText(ret)

    def btnclkCleanAboveAll(self):
        ret = cleanSearchAndViewHistory()
        ret += cleanLogFiles()
        ret += cleanThumbnailFiles()
        ret += cleanRecentOpen()
        ret += cleanAptCache()
        self.textBrowser.setText(ret)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())

