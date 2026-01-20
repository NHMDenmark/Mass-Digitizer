# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'specimendataentry.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_SpecimenDataEntry(object):
    def setupUi(self, SpecimenDataEntry):
        if not SpecimenDataEntry.objectName():
            SpecimenDataEntry.setObjectName(u"SpecimenDataEntry")
        SpecimenDataEntry.resize(1080, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SpecimenDataEntry.sizePolicy().hasHeightForWidth())
        SpecimenDataEntry.setSizePolicy(sizePolicy)
        SpecimenDataEntry.setMinimumSize(QSize(1080, 720))
        SpecimenDataEntry.setMaximumSize(QSize(1080, 720))
        font = QFont()
        font.setFamilies([u"Arial"])
        SpecimenDataEntry.setFont(font)
        self.verticalLayout = QVBoxLayout(SpecimenDataEntry)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayoutHeader = QHBoxLayout()
        self.horizontalLayoutHeader.setObjectName(u"horizontalLayoutHeader")
        self.appTitle = QLabel(SpecimenDataEntry)
        self.appTitle.setObjectName(u"appTitle")
        self.appTitle.setMinimumSize(QSize(0, 0))
        self.appTitle.setMaximumSize(QSize(480, 4096))
        font1 = QFont()
        font1.setFamilies([u"Bahnschrift"])
        font1.setPointSize(20)
        font1.setKerning(False)
        self.appTitle.setFont(font1)

        self.horizontalLayoutHeader.addWidget(self.appTitle)

        self.verticalLayoutMeta = QVBoxLayout()
        self.verticalLayoutMeta.setObjectName(u"verticalLayoutMeta")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lblUserName = QLabel(SpecimenDataEntry)
        self.lblUserName.setObjectName(u"lblUserName")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblUserName)

        self.lblInstitution = QLabel(SpecimenDataEntry)
        self.lblInstitution.setObjectName(u"lblInstitution")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblInstitution)

        self.lblCollection = QLabel(SpecimenDataEntry)
        self.lblCollection.setObjectName(u"lblCollection")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblCollection)

        self.lblVersion = QLabel(SpecimenDataEntry)
        self.lblVersion.setObjectName(u"lblVersion")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lblVersion)

        self.txtUserName = QLabel(SpecimenDataEntry)
        self.txtUserName.setObjectName(u"txtUserName")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.txtUserName)

        self.txtInstitution = QLabel(SpecimenDataEntry)
        self.txtInstitution.setObjectName(u"txtInstitution")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.txtInstitution)

        self.txtCollection = QLabel(SpecimenDataEntry)
        self.txtCollection.setObjectName(u"txtCollection")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.txtCollection)

        self.txtVersionNr = QLabel(SpecimenDataEntry)
        self.txtVersionNr.setObjectName(u"txtVersionNr")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.txtVersionNr)


        self.verticalLayoutMeta.addLayout(self.formLayout)


        self.horizontalLayoutHeader.addLayout(self.verticalLayoutMeta)


        self.verticalLayout.addLayout(self.horizontalLayoutHeader)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)

        self.radModeDefault = QRadioButton(SpecimenDataEntry)
        self.radModeDefault.setObjectName(u"radModeDefault")
        self.radModeDefault.setChecked(True)

        self.horizontalLayout.addWidget(self.radModeDefault)

        self.radModeFastEntry = QRadioButton(SpecimenDataEntry)
        self.radModeFastEntry.setObjectName(u"radModeFastEntry")

        self.horizontalLayout.addWidget(self.radModeFastEntry)

        self.horizontalSpacer = QSpacerItem(600, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.frmGreenArea = QFrame(SpecimenDataEntry)
        self.frmGreenArea.setObjectName(u"frmGreenArea")
        self.frmGreenArea.setFrameShape(QFrame.Shape.StyledPanel)
        self.frmGreenArea.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayoutGreenArea = QHBoxLayout(self.frmGreenArea)
        self.horizontalLayoutGreenArea.setObjectName(u"horizontalLayoutGreenArea")
        self.verticalLayoutGreenAreaLeft = QVBoxLayout()
        self.verticalLayoutGreenAreaLeft.setObjectName(u"verticalLayoutGreenAreaLeft")
        self.formLayoutGreenAreaLeft = QFormLayout()
        self.formLayoutGreenAreaLeft.setObjectName(u"formLayoutGreenAreaLeft")
        self.lblStorage = QLabel(self.frmGreenArea)
        self.lblStorage.setObjectName(u"lblStorage")

        self.formLayoutGreenAreaLeft.setWidget(0, QFormLayout.LabelRole, self.lblStorage)

        self.inpStorage = QLineEdit(self.frmGreenArea)
        self.inpStorage.setObjectName(u"inpStorage")
        self.inpStorage.setMinimumSize(QSize(600, 0))

        self.formLayoutGreenAreaLeft.setWidget(0, QFormLayout.FieldRole, self.inpStorage)

        self.lblPreparation = QLabel(self.frmGreenArea)
        self.lblPreparation.setObjectName(u"lblPreparation")

        self.formLayoutGreenAreaLeft.setWidget(1, QFormLayout.LabelRole, self.lblPreparation)

        self.cbxPrepType = QComboBox(self.frmGreenArea)
        self.cbxPrepType.setObjectName(u"cbxPrepType")

        self.formLayoutGreenAreaLeft.setWidget(1, QFormLayout.FieldRole, self.cbxPrepType)

        self.lblTypeStatus = QLabel(self.frmGreenArea)
        self.lblTypeStatus.setObjectName(u"lblTypeStatus")

        self.formLayoutGreenAreaLeft.setWidget(2, QFormLayout.LabelRole, self.lblTypeStatus)

        self.cbxTypeStatus = QComboBox(self.frmGreenArea)
        self.cbxTypeStatus.setObjectName(u"cbxTypeStatus")

        self.formLayoutGreenAreaLeft.setWidget(2, QFormLayout.FieldRole, self.cbxTypeStatus)

        self.lblGeoRegion = QLabel(self.frmGreenArea)
        self.lblGeoRegion.setObjectName(u"lblGeoRegion")

        self.formLayoutGreenAreaLeft.setWidget(3, QFormLayout.LabelRole, self.lblGeoRegion)

        self.cbxGeoRegion = QComboBox(self.frmGreenArea)
        self.cbxGeoRegion.setObjectName(u"cbxGeoRegion")

        self.formLayoutGreenAreaLeft.setWidget(3, QFormLayout.FieldRole, self.cbxGeoRegion)

        self.lblTaxonName = QLabel(self.frmGreenArea)
        self.lblTaxonName.setObjectName(u"lblTaxonName")

        self.formLayoutGreenAreaLeft.setWidget(4, QFormLayout.LabelRole, self.lblTaxonName)

        self.inpTaxonName = QLineEdit(self.frmGreenArea)
        self.inpTaxonName.setObjectName(u"inpTaxonName")

        self.formLayoutGreenAreaLeft.setWidget(4, QFormLayout.FieldRole, self.inpTaxonName)


        self.verticalLayoutGreenAreaLeft.addLayout(self.formLayoutGreenAreaLeft)


        self.horizontalLayoutGreenArea.addLayout(self.verticalLayoutGreenAreaLeft)

        self.verticalLayoutGreenAreaRight = QVBoxLayout()
        self.verticalLayoutGreenAreaRight.setObjectName(u"verticalLayoutGreenAreaRight")
        self.txtStorageFullname = QLabel(self.frmGreenArea)
        self.txtStorageFullname.setObjectName(u"txtStorageFullname")
        self.txtStorageFullname.setMinimumSize(QSize(0, 80))
        self.txtStorageFullname.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.txtStorageFullname.setWordWrap(True)

        self.verticalLayoutGreenAreaRight.addWidget(self.txtStorageFullname)

        self.horizontalSpacer_7 = QSpacerItem(200, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayoutGreenAreaRight.addItem(self.horizontalSpacer_7)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setLabelAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)
        self.formLayout_2.setFormAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)
        self.lblTaxonNumber = QLabel(self.frmGreenArea)
        self.lblTaxonNumber.setObjectName(u"lblTaxonNumber")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.lblTaxonNumber)

        self.inpTaxonNumber = QLineEdit(self.frmGreenArea)
        self.inpTaxonNumber.setObjectName(u"inpTaxonNumber")
        self.inpTaxonNumber.setMaximumSize(QSize(100, 4096))

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.inpTaxonNumber)


        self.verticalLayoutGreenAreaRight.addLayout(self.formLayout_2)


        self.horizontalLayoutGreenArea.addLayout(self.verticalLayoutGreenAreaRight)


        self.verticalLayout.addWidget(self.frmGreenArea)

        self.frmBlueArea = QFrame(SpecimenDataEntry)
        self.frmBlueArea.setObjectName(u"frmBlueArea")
        self.frmBlueArea.setFrameShape(QFrame.Shape.StyledPanel)
        self.frmBlueArea.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayoutBlueArea = QHBoxLayout(self.frmBlueArea)
        self.horizontalLayoutBlueArea.setObjectName(u"horizontalLayoutBlueArea")
        self.verticalLayoutBlueAreaLeft = QVBoxLayout()
        self.verticalLayoutBlueAreaLeft.setObjectName(u"verticalLayoutBlueAreaLeft")
        self.horizontalLayoutWarning = QHBoxLayout()
        self.horizontalLayoutWarning.setObjectName(u"horizontalLayoutWarning")
        self.formLayoutInputFieldsBlue = QFormLayout()
        self.formLayoutInputFieldsBlue.setObjectName(u"formLayoutInputFieldsBlue")
        self.lblSpecimenFlags = QLabel(self.frmBlueArea)
        self.lblSpecimenFlags.setObjectName(u"lblSpecimenFlags")

        self.formLayoutInputFieldsBlue.setWidget(0, QFormLayout.LabelRole, self.lblSpecimenFlags)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.chkDamage = QCheckBox(self.frmBlueArea)
        self.chkDamage.setObjectName(u"chkDamage")
        sizePolicy.setHeightForWidth(self.chkDamage.sizePolicy().hasHeightForWidth())
        self.chkDamage.setSizePolicy(sizePolicy)
        self.chkDamage.setMinimumSize(QSize(142, 0))

        self.horizontalLayout_2.addWidget(self.chkDamage)

        self.chkSpecimenObscured = QCheckBox(self.frmBlueArea)
        self.chkSpecimenObscured.setObjectName(u"chkSpecimenObscured")
        sizePolicy.setHeightForWidth(self.chkSpecimenObscured.sizePolicy().hasHeightForWidth())
        self.chkSpecimenObscured.setSizePolicy(sizePolicy)
        self.chkSpecimenObscured.setMinimumSize(QSize(141, 0))

        self.horizontalLayout_2.addWidget(self.chkSpecimenObscured)

        self.chkLabelObscured = QCheckBox(self.frmBlueArea)
        self.chkLabelObscured.setObjectName(u"chkLabelObscured")

        self.horizontalLayout_2.addWidget(self.chkLabelObscured)

        self.horizontalSpacer_2 = QSpacerItem(100, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.formLayoutInputFieldsBlue.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.lblContainerType = QLabel(self.frmBlueArea)
        self.lblContainerType.setObjectName(u"lblContainerType")

        self.formLayoutInputFieldsBlue.setWidget(2, QFormLayout.LabelRole, self.lblContainerType)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radRadioSSO = QRadioButton(self.frmBlueArea)
        self.radRadioSSO.setObjectName(u"radRadioSSO")
        self.radRadioSSO.setChecked(True)

        self.horizontalLayout_3.addWidget(self.radRadioSSO)

        self.radRadioMOS = QRadioButton(self.frmBlueArea)
        self.radRadioMOS.setObjectName(u"radRadioMOS")
        self.radRadioMOS.setToolTipDuration(3)

        self.horizontalLayout_3.addWidget(self.radRadioMOS)

        self.radRadioMSO = QRadioButton(self.frmBlueArea)
        self.radRadioMSO.setObjectName(u"radRadioMSO")
        self.radRadioMSO.setToolTipDuration(3)

        self.horizontalLayout_3.addWidget(self.radRadioMSO)

        self.horizontalSpacer_3 = QSpacerItem(500, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.formLayoutInputFieldsBlue.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.lblContainerID = QLabel(self.frmBlueArea)
        self.lblContainerID.setObjectName(u"lblContainerID")

        self.formLayoutInputFieldsBlue.setWidget(3, QFormLayout.LabelRole, self.lblContainerID)

        self.inpContainerName = QLineEdit(self.frmBlueArea)
        self.inpContainerName.setObjectName(u"inpContainerName")
        self.inpContainerName.setEnabled(False)
        self.inpContainerName.setMaximumSize(QSize(380, 4096))

        self.formLayoutInputFieldsBlue.setWidget(3, QFormLayout.FieldRole, self.inpContainerName)

        self.lblNotes = QLabel(self.frmBlueArea)
        self.lblNotes.setObjectName(u"lblNotes")

        self.formLayoutInputFieldsBlue.setWidget(4, QFormLayout.LabelRole, self.lblNotes)

        self.inpNotes = QLineEdit(self.frmBlueArea)
        self.inpNotes.setObjectName(u"inpNotes")

        self.formLayoutInputFieldsBlue.setWidget(4, QFormLayout.FieldRole, self.inpNotes)

        self.lblBarcode = QLabel(self.frmBlueArea)
        self.lblBarcode.setObjectName(u"lblBarcode")

        self.formLayoutInputFieldsBlue.setWidget(5, QFormLayout.LabelRole, self.lblBarcode)

        self.inpCatalogNumber = QLineEdit(self.frmBlueArea)
        self.inpCatalogNumber.setObjectName(u"inpCatalogNumber")
        self.inpCatalogNumber.setMaximumSize(QSize(380, 4096))

        self.formLayoutInputFieldsBlue.setWidget(5, QFormLayout.FieldRole, self.inpCatalogNumber)


        self.horizontalLayoutWarning.addLayout(self.formLayoutInputFieldsBlue)

        self.imgWarningLinkedRecord = QLabel(self.frmBlueArea)
        self.imgWarningLinkedRecord.setObjectName(u"imgWarningLinkedRecord")
        self.imgWarningLinkedRecord.setVisible(False)
        self.imgWarningLinkedRecord.setLocale(QLocale(QLocale.English, QLocale.Denmark))
        self.imgWarningLinkedRecord.setPixmap(QPixmap(u"img/Warning_LinkedRecord.png"))

        self.horizontalLayoutWarning.addWidget(self.imgWarningLinkedRecord)


        self.verticalLayoutBlueAreaLeft.addLayout(self.horizontalLayoutWarning)

        self.lblError = QLabel(self.frmBlueArea)
        self.lblError.setObjectName(u"lblError")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lblError.sizePolicy().hasHeightForWidth())
        self.lblError.setSizePolicy(sizePolicy1)
        self.lblError.setMaximumSize(QSize(1000, 20))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(11)
        self.lblError.setFont(font2)
        self.lblError.setVisible(False)
        self.lblError.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayoutBlueAreaLeft.addWidget(self.lblError)

        self.horizontalLayoutControlArea = QHBoxLayout()
        self.horizontalLayoutControlArea.setObjectName(u"horizontalLayoutControlArea")
        self.lblRecordID = QLabel(self.frmBlueArea)
        self.lblRecordID.setObjectName(u"lblRecordID")
        self.lblRecordID.setMaximumSize(QSize(80, 30))

        self.horizontalLayoutControlArea.addWidget(self.lblRecordID)

        self.txtRecordID = QLabel(self.frmBlueArea)
        self.txtRecordID.setObjectName(u"txtRecordID")
        self.txtRecordID.setMaximumSize(QSize(80, 30))
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setPointSize(11)
        font3.setItalic(True)
        self.txtRecordID.setFont(font3)

        self.horizontalLayoutControlArea.addWidget(self.txtRecordID)

        self.horizontalSpacer_4 = QSpacerItem(80, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutControlArea.addItem(self.horizontalSpacer_4)

        self.btnSave = QPushButton(self.frmBlueArea)
        self.btnSave.setObjectName(u"btnSave")
        self.btnSave.setMaximumSize(QSize(150, 50))
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(10)
        font4.setUnderline(False)
        font4.setStrikeOut(False)
        self.btnSave.setFont(font4)

        self.horizontalLayoutControlArea.addWidget(self.btnSave)

        self.horizontalSpacer_5 = QSpacerItem(80, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutControlArea.addItem(self.horizontalSpacer_5)

        self.btnBack = QPushButton(self.frmBlueArea)
        self.btnBack.setObjectName(u"btnBack")
        self.btnBack.setMaximumSize(QSize(150, 50))
        self.btnBack.setFont(font4)

        self.horizontalLayoutControlArea.addWidget(self.btnBack)

        self.btnForward = QPushButton(self.frmBlueArea)
        self.btnForward.setObjectName(u"btnForward")
        self.btnForward.setMaximumSize(QSize(150, 50))
        self.btnForward.setFont(font4)

        self.horizontalLayoutControlArea.addWidget(self.btnForward)

        self.btnClear = QPushButton(self.frmBlueArea)
        self.btnClear.setObjectName(u"btnClear")
        self.btnClear.setMaximumSize(QSize(150, 50))
        self.btnClear.setFont(font4)

        self.horizontalLayoutControlArea.addWidget(self.btnClear)


        self.verticalLayoutBlueAreaLeft.addLayout(self.horizontalLayoutControlArea)

        self.tblPrevious = QTableWidget(self.frmBlueArea)
        if (self.tblPrevious.columnCount() < 6):
            self.tblPrevious.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tblPrevious.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tblPrevious.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tblPrevious.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tblPrevious.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tblPrevious.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tblPrevious.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tblPrevious.setObjectName(u"tblPrevious")
        self.tblPrevious.setMaximumSize(QSize(4096, 120))
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        font5.setPointSize(10)
        self.tblPrevious.setFont(font5)
        self.tblPrevious.setStyleSheet(u"\n"
"          QHeaderView::section {\n"
"              font-family: Arial;\n"
"              font-size: 12pt;\n"
"              background-color: #D3D3D3;\n"
"              color: black;\n"
"              border: 1px solid grey;\n"
"              padding: 1px;\n"
"          }\n"
"            QTableWidget::item {\n"
"                height: 20px;\n"
"            }\n"
"          ")
        self.tblPrevious.horizontalHeader().setDefaultSectionSize(100)
        self.tblPrevious.horizontalHeader().setStretchLastSection(True)

        self.verticalLayoutBlueAreaLeft.addWidget(self.tblPrevious)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lblNumberCounter = QLabel(self.frmBlueArea)
        self.lblNumberCounter.setObjectName(u"lblNumberCounter")
        self.lblNumberCounter.setMaximumSize(QSize(120, 30))

        self.horizontalLayout_4.addWidget(self.lblNumberCounter)

        self.txtNumberCounter = QLabel(self.frmBlueArea)
        self.txtNumberCounter.setObjectName(u"txtNumberCounter")
        self.txtNumberCounter.setMaximumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.txtNumberCounter)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayoutBlueAreaLeft.addLayout(self.horizontalLayout_5)


        self.horizontalLayoutBlueArea.addLayout(self.verticalLayoutBlueAreaLeft)


        self.verticalLayout.addWidget(self.frmBlueArea)


        self.retranslateUi(SpecimenDataEntry)

        QMetaObject.connectSlotsByName(SpecimenDataEntry)
    # setupUi

    def retranslateUi(self, SpecimenDataEntry):
        SpecimenDataEntry.setWindowTitle(QCoreApplication.translate("SpecimenDataEntry", u"DaSSCo Mass Digitization App", None))
        SpecimenDataEntry.setStyleSheet(QCoreApplication.translate("SpecimenDataEntry", u"\n"
"    QWidget#SpecimenDataEntry {\n"
"        background-color: #BFD1DF;\n"
"    }\n"
"    QLineEdit {\n"
"        background-color: white;\n"
"        color: black;\n"
"    }    \n"
"    QComboBox{\n"
"        background-color: white;\n"
"        color: black;\n"
"    }\n"
"    QLineEdit:focus {\n"
"    background-color: yellow; /* Background color when focused */\n"
"    }\n"
"    QLineEdit:disabled {\n"
"        background-color: #E1E1E1;\n"
"        border: 1px solid rgb(128, 128, 128);\n"
"    }\n"
"    QLabel {\n"
"        font-family: Bahnschrift;\n"
"        font-size: 13pt;\n"
"    }\n"
"    QLabel#appTitle {\n"
"        font-size: 20pt;\n"
"    }\n"
"    .QLabelMetaInfo {\n"
"        font-family: Arial;\n"
"        font-size: 11pt;\n"
"        font-style: italic;\n"
"    }\n"
"    .QLabelError {\n"
"        font-family: Arial;\n"
"        font-size: 11pt;\n"
"        color: red;\n"
"    }\n"
"    .QLabelPlain{\n"
"        font-family: Arial;\n"
"        font-size: 11pt;\n"
"        color: black;\n"
""
                        "    }\n"
"    QPushButton {\n"
"        border: 1px solid rgb(128, 128, 128);\n"
"        padding: 5px;\n"
"        text-align: center;\n"
"        text-decoration: none;\n"
"        font-size: 10pt;\n"
"        margin: 4px 2px;\n"
"    }\n"
"    QPushButton#btnSave {\n"
"        color: white;\n"
"        background-color: #2E8B57\n"
"    }\n"
"    QPushButton#btnBack {\n"
"        color: white;\n"
"        background-color: #8B0000\n"
"    }\n"
"    QPushButton#btnForward {\n"
"        color: black;\n"
"        background-color: #EEE9BF\n"
"    }\n"
"    QPushButton#btnClear {\n"
"        color: black;\n"
"        background-color:white\n"
"    }\n"
"    QPushButton:focus {\n"
"    border: 2px solid yellow; \n"
"    }\n"
"   QFrame#frmGreenArea {\n"
"       background-color: #E8F4EA;    \n"
"       border: 1px solid rgb(128, 128, 128);\n"
"       padding: 10px;\n"
"   }\n"
"   QFrame#frmBlueArea {\n"
"       background-color: #99CDFF;    \n"
"       border: 1px solid rgb(128, 128, 128);\n"
"       padding: 10"
                        "px;\n"
"   }\n"
"   QCheckBox:focus {\n"
"    border: 2px solid yellow; \n"
"    }\n"
"   QComboBox:focus {\n"
"    border: 2px solid yellow; \n"
"    }\n"
"   QRadioButton:focus {\n"
"    border: 2px solid yellow; \n"
"    }\n"
"   ", None))
        self.appTitle.setText(QCoreApplication.translate("SpecimenDataEntry", u"DaSSCo Mass Digitization App", None))
        self.lblUserName.setText(QCoreApplication.translate("SpecimenDataEntry", u"Logged in as:", None))
        self.lblInstitution.setText(QCoreApplication.translate("SpecimenDataEntry", u"Institution:", None))
        self.lblCollection.setText(QCoreApplication.translate("SpecimenDataEntry", u"Collection:", None))
        self.lblVersion.setText(QCoreApplication.translate("SpecimenDataEntry", u"Version number:", None))
        self.txtUserName.setText(QCoreApplication.translate("SpecimenDataEntry", u"-not set-", None))
        self.txtUserName.setProperty(u"class", QCoreApplication.translate("SpecimenDataEntry", u"QLabelMetaInfo", None))
        self.txtInstitution.setText(QCoreApplication.translate("SpecimenDataEntry", u"-not set-", None))
        self.txtInstitution.setProperty(u"class", QCoreApplication.translate("SpecimenDataEntry", u"QLabelMetaInfo", None))
        self.txtCollection.setText(QCoreApplication.translate("SpecimenDataEntry", u"-not set-", None))
        self.txtCollection.setProperty(u"class", QCoreApplication.translate("SpecimenDataEntry", u"QLabelMetaInfo", None))
        self.txtVersionNr.setText(QCoreApplication.translate("SpecimenDataEntry", u"-not set-", None))
        self.txtVersionNr.setProperty(u"class", QCoreApplication.translate("SpecimenDataEntry", u"QLabelMetaInfo", None))
        self.radModeDefault.setText(QCoreApplication.translate("SpecimenDataEntry", u"Default entry mode", None))
        self.radModeFastEntry.setText(QCoreApplication.translate("SpecimenDataEntry", u"Fast entry mode", None))
        self.lblStorage.setText(QCoreApplication.translate("SpecimenDataEntry", u"Storage location:", None))
        self.lblPreparation.setText(QCoreApplication.translate("SpecimenDataEntry", u"Preparation type:", None))
        self.lblTypeStatus.setText(QCoreApplication.translate("SpecimenDataEntry", u"Type status:", None))
        self.lblGeoRegion.setText(QCoreApplication.translate("SpecimenDataEntry", u"Geographic region:", None))
        self.lblTaxonName.setText(QCoreApplication.translate("SpecimenDataEntry", u"Taxonomic name:", None))
        self.txtStorageFullname.setText(QCoreApplication.translate("SpecimenDataEntry", u"-no storage selected-", None))
        self.txtStorageFullname.setProperty(u"class", QCoreApplication.translate("SpecimenDataEntry", u"QLabelMetaInfo", None))
        self.lblTaxonNumber.setText(QCoreApplication.translate("SpecimenDataEntry", u"Taxon Number:", None))
        self.lblSpecimenFlags.setText(QCoreApplication.translate("SpecimenDataEntry", u"Specimen flags", None))
        self.chkDamage.setText(QCoreApplication.translate("SpecimenDataEntry", u"Needs Repair", None))
        self.chkSpecimenObscured.setText(QCoreApplication.translate("SpecimenDataEntry", u"Specimen obscured", None))
        self.chkLabelObscured.setText(QCoreApplication.translate("SpecimenDataEntry", u"Label obscured", None))
        self.lblContainerType.setText(QCoreApplication.translate("SpecimenDataEntry", u"Container type", None))
        self.radRadioSSO.setText(QCoreApplication.translate("SpecimenDataEntry", u"Single specimen object", None))
#if QT_CONFIG(tooltip)
        self.radRadioMOS.setToolTip(QCoreApplication.translate("SpecimenDataEntry", u"One specimen on multiple objects", None))
#endif // QT_CONFIG(tooltip)
        self.radRadioMOS.setText(QCoreApplication.translate("SpecimenDataEntry", u"Multi object specimen", None))
#if QT_CONFIG(tooltip)
        self.radRadioMSO.setToolTip(QCoreApplication.translate("SpecimenDataEntry", u"Multiple specimens on one object", None))
#endif // QT_CONFIG(tooltip)
        self.radRadioMSO.setText(QCoreApplication.translate("SpecimenDataEntry", u"Multi specimen object", None))
        self.lblContainerID.setText(QCoreApplication.translate("SpecimenDataEntry", u"Container ID", None))
        self.lblNotes.setText(QCoreApplication.translate("SpecimenDataEntry", u"Notes", None))
        self.lblBarcode.setText(QCoreApplication.translate("SpecimenDataEntry", u"Barcode:", None))
        self.imgWarningLinkedRecord.setText("")
        self.lblError.setText(QCoreApplication.translate("SpecimenDataEntry", u"Validation Error", None))
        self.lblError.setProperty(u"class", QCoreApplication.translate("SpecimenDataEntry", u"QLabelError", None))
        self.lblRecordID.setText(QCoreApplication.translate("SpecimenDataEntry", u"Record ID:", None))
        self.txtRecordID.setText(QCoreApplication.translate("SpecimenDataEntry", u"-no record-", None))
        self.txtRecordID.setProperty(u"class", QCoreApplication.translate("SpecimenDataEntry", u"QLabelPlain", None))
        self.btnSave.setText(QCoreApplication.translate("SpecimenDataEntry", u"SAVE", None))
        self.btnBack.setText(QCoreApplication.translate("SpecimenDataEntry", u"GO BACK", None))
        self.btnForward.setText(QCoreApplication.translate("SpecimenDataEntry", u"GO FORWARDS", None))
        self.btnClear.setText(QCoreApplication.translate("SpecimenDataEntry", u"CLEAR FORM", None))
        ___qtablewidgetitem = self.tblPrevious.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("SpecimenDataEntry", u"id", None));
        ___qtablewidgetitem1 = self.tblPrevious.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("SpecimenDataEntry", u"catalognumber", None));
        ___qtablewidgetitem2 = self.tblPrevious.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("SpecimenDataEntry", u"taxonfullname", None));
        ___qtablewidgetitem3 = self.tblPrevious.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("SpecimenDataEntry", u"containertype", None));
        ___qtablewidgetitem4 = self.tblPrevious.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("SpecimenDataEntry", u"georegionname", None));
        ___qtablewidgetitem5 = self.tblPrevious.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("SpecimenDataEntry", u"storagename", None));
        self.lblNumberCounter.setText(QCoreApplication.translate("SpecimenDataEntry", u"Records added:", None))
        self.txtNumberCounter.setText(QCoreApplication.translate("SpecimenDataEntry", u"-not set-", None))
        self.txtNumberCounter.setProperty(u"class", QCoreApplication.translate("SpecimenDataEntry", u"QLabelPlain", None))
    # retranslateUi

