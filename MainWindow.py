# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import binascii

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from dbUtility import iud_db, select_data

import nfc

# 待ち受けの1サイクル秒
TIME_cycle = 5.0
# 待ち受けの反応インターバル秒
TIME_interval = 0.2
# タッチされてから次の待ち受けを開始するまで無効化する秒
TIME_wait = 3
# NFC接続リクエストのための準備106A(NFC type A)で設定
target_req_nfc = nfc.clf.RemoteTarget("106A")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(490, 324)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(56, 34, 50, 12))
        self.ShainCD = QLineEdit(self.centralwidget)
        self.ShainCD.setObjectName(u"ShainCD")
        self.ShainCD.setGeometry(QRect(110, 30, 61, 20))
        self.ShainCD.setMaxLength(4)
        self.ShainCD.textChanged.connect(self.cdChanged)
        self.ShainNM = QLineEdit(self.centralwidget)
        self.ShainNM.setObjectName(u"ShainNM")
        self.ShainNM.setGeometry(QRect(171, 30, 231, 20))
        self.ShainNM.setReadOnly(True)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(90, 80, 81, 16))
        self.preCard = QLineEdit(self.centralwidget)
        self.preCard.setObjectName(u"preCard")
        self.preCard.setGeometry(QRect(173, 77, 230, 20))
        self.preCard.setReadOnly(True)
        self.btnRead = QPushButton(self.centralwidget)
        self.btnRead.clicked.connect(self.btnReadClick)
        self.btnRead.setObjectName(u"btnRead")
        self.btnRead.setGeometry(QRect(140, 120, 221, 51))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(90, 200, 81, 16))
        self.NewCard = QLineEdit(self.centralwidget)
        self.NewCard.setObjectName(u"NewCard")
        self.NewCard.setGeometry(QRect(170, 200, 221, 20))
        self.NewCard.setReadOnly(True)
        self.btnRecord = QPushButton(self.centralwidget)
        self.btnRecord.clicked.connect(self.btnRecordClick)
        self.btnRecord.setObjectName(u"btnRecord")
        self.btnRecord.setGeometry(QRect(140, 240, 221, 51))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"\u793e\u54e1\u30ab\u30fc\u30c9\u7ba1\u7406", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6c0f\u540d\u30b3\u30fc\u30c9", None))
        self.btnRead.setText(
            QCoreApplication.translate("MainWindow", u"\u30ab\u30fc\u30c9\u8aad\u307f\u8fbc\u307f", None))
        self.btnRecord.setText(QCoreApplication.translate("MainWindow", u"\u30ab\u30fc\u30c9\u767b\u9332", None))
        self.label_2.setText(
            QCoreApplication.translate("MainWindow", u"\u767b\u9332\u6e08\u307f\u30ab\u30fc\u30c9", None))
        self.label_3.setText(
            QCoreApplication.translate("MainWindow", u"\u8aad\u307f\u8fbc\u307f\u30ab\u30fc\u30c9", None))

    # retranslateUi

    #
    def cdChanged(self):
        # 社員IDが4桁入力されたらその値から社員情報を検索する
        if len(self.ShainCD.text()) == 4:
            sql = f"SELECT shainnm, cardid FROM shain WHERE shainid = '{self.ShainCD.text()}';"
            rec = select_data(sql)
            if len(rec) > 0:
                dd = rec[0]
                self.ShainNM.setText(dd[0])
                self.preCard.setText(dd[1])
                self.NewCard.setText("")
        else:
            self.ShainNM.setText("")
            self.preCard.setText("")
            self.NewCard.setText("")

    def btnReadClick(self):
        # self.ShainNM.setText("Hello World")
        # USBに接続されたNFCリーダに接続してインスタンス化
        clf = nfc.ContactlessFrontend('usb')
        target_res = clf.sense(target_req_nfc, iterations=int(TIME_cycle // TIME_interval) + 1, interval=TIME_interval)
        if not target_res is None:
            tag = nfc.tag.activate(clf, target_res)
            print('TAG type: ' + tag.type)

            # Type1,Type2:NFCタグ、Type4:Android端末でのNFCなど
            if tag.type == "Type2Tag":
                idm = binascii.hexlify(tag.identifier).upper().decode('utf-8')
                self.NewCard.setText(idm)

        clf.close()


    def btnRecordClick(self):
        # 社員IDが未入力なら処理しない
        if self.ShainCD.text() == "":
            return

        # 社員名を返却していなければ処理しない
        if self.ShainNM.text() == "":
            return

        # 読み込みカード情報がない場合には処理しない
        if self.NewCard.text() == "":
            return

        # 確認用のメッセージボックスを表示し、OKボタンがクリックされたら以下を実行
        ret = QMessageBox.question(None, "確認", "カード情報を更新します。よろしいですか？", QMessageBox.Ok, QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            # 更新SQL文を作成する
            sql = f"UPDATE shain SET cardid = '{self.NewCard.text()}' WHERE shainid = '{self.ShainCD.text()}';"
            # SQL文を実行する
            iud_db(sql)

            # 完了したら後始末
            self.ShainCD.setText("")
            self.ShainNM.setText("")
            self.preCard.setText("")
            self.NewCard.setText("")

