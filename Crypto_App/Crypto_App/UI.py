
# Imported below Libs
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
 
# Imported below Libs for hash algos
import hashlib

# other libs
import sys

# creating main window class
class MainWindow(QTabWidget):

    def __init__(self):
        super().__init__()

        self.w_width = 750
        self.w_height = 500
        self.setGeometry(100, 100, self.w_width, self.w_height)

        self.listOfBlocks = []

        self.updateBlockchain = True

        self.UiComponents()
        self.show()

    def InitializeHashTab(self):
        
        layout = QVBoxLayout()
        self.hashTab.setLayout(layout)

        #input box
        self.inputEditor = QTextEdit()
        self.inputEditor.setStyleSheet("color: white;  background-color: black")
        layout.addWidget(self.inputEditor)
        
        #hash algo to choose
        self.hashAlgoCombo = QComboBox()
        self.hashAlgoCombo.addItem("sha256")
        self.hashAlgoCombo.addItem("sha384")
        self.hashAlgoCombo.addItem("sha224")
        self.hashAlgoCombo.addItem("sha512")
        layout.addWidget(self.hashAlgoCombo)
        
        #to show the output hash
        self.outputEditor = QTextEdit()
        self.outputEditor.setReadOnly(True)
        self.outputEditor.setStyleSheet("color: white;  background-color: black")
        layout.addWidget(self.outputEditor)

        # connect
        self.inputEditor.textChanged.connect(self.hash)
        self.hashAlgoCombo.currentIndexChanged.connect(self.hash)

    def CreateNewBlock(self):

        block = QWidget()
        block.setFixedWidth(300)
        block.setFixedHeight(300)
        block.setStyleSheet("background-color: lightblue")

        virtLayout = QVBoxLayout()
        block.setLayout(virtLayout)

        heightofBlockchain = len(self.listOfBlocks)

        #block number
        numberlabel = QLabel()
        numberlabel.setText("Block #" + str(heightofBlockchain + 1))
        virtLayout.addWidget(numberlabel)

        #data editor
        dataEditor = QTextEdit()
        dataEditor.setStyleSheet("color: white;  background-color: black")
        virtLayout.addWidget(dataEditor)

        #rpev block label
        prevBlockHashlabel = QLabel()
        prevBlockHashlabel.setText("Previous block hash")
        virtLayout.addWidget(prevBlockHashlabel)

        #previous block hash editor
        prevBlockHashEditor = QTextEdit()
        prevBlockHashEditor.setStyleSheet("color: white;  background-color: black")
        prevBlockHashEditor.setReadOnly(True)
        virtLayout.addWidget(prevBlockHashEditor)

        #nonce label
        nonceLabel = QLabel()
        nonceLabel.setText("Nonce")
        virtLayout.addWidget(nonceLabel)

        #nonce spin
        nonceSpin = QSpinBox()
        nonceSpin.setStyleSheet("color: white;  background-color: black")
        nonceSpin.setMinimum(0)
        nonceSpin.setMaximum(1e10)
        nonceSpin.setValue(0)
        nonceSpin.setSingleStep(1)
        nonceSpin.setWrapping(True)
        virtLayout.addWidget(nonceSpin)

        #target label
        targetLabel = QLabel()
        targetLabel.setText("Target Value")
        virtLayout.addWidget(targetLabel)

        #target spin
        targetSpin = QSpinBox()
        targetSpin.setStyleSheet("color: white;  background-color: black")
        targetSpin.setMinimum(0)
        targetSpin.setMaximum(10)
        targetSpin.setValue(1)
        targetSpin.setSingleStep(1)
        targetSpin.setWrapping(True)
        virtLayout.addWidget(targetSpin)
               
        mineButton = QPushButton("Mine")
        mineButton.setStyleSheet("color: black;  background-color: white")
        virtLayout.addWidget(mineButton)

        #curr block hash label
        currBlockHashlabel = QLabel()
        currBlockHashlabel.setText("Currrent block hash")
        virtLayout.addWidget(currBlockHashlabel)

        #current black hash editor
        currBlockHashEditor = QTextEdit()
        currBlockHashEditor.setStyleSheet("color: white;  background-color: black")
        currBlockHashEditor.setReadOnly(True)
        virtLayout.addWidget(currBlockHashEditor)

        self.listOfBlocks.append({"data":dataEditor, "prevBlockHashEditor":prevBlockHashEditor,  "nonceSpin":nonceSpin,
                                 "targetSpin":targetSpin, "currBlockHashEditor":currBlockHashEditor})

        if (heightofBlockchain == 0):

            strAlgoSelected = self.hashingAlgoForBC.currentText()

            if(strAlgoSelected == "sha256"):
                prevBlockHashEditor.setText("0" * 32)

            if(strAlgoSelected == "sha384"):
                prevBlockHashEditor.setText("0" * 48)

            if(strAlgoSelected == "sha224"):
                prevBlockHashEditor.setText("0" * 28)

            if(strAlgoSelected == "sha512"):
                prevBlockHashEditor.setText("0" * 64)
        else:
            strPrevHash = self.listOfBlocks[heightofBlockchain - 1]["currBlockHashEditor"].toPlainText()
            prevBlockHashEditor.setText(strPrevHash)

        #allocating the block number so that we can know who is the sender
        dataEditor.blockNum = heightofBlockchain + 1
        nonceSpin.blockNum = heightofBlockchain + 1
        prevBlockHashEditor.blockNum = heightofBlockchain + 1
        mineButton.blockNum = heightofBlockchain + 1

        #connect
        dataEditor.textChanged.connect(self.UpdateBlockchain)
        nonceSpin.valueChanged.connect(self.UpdateBlockchain)
        prevBlockHashEditor.textChanged.connect(self.UpdateBlockchain)
        mineButton.clicked.connect(self.Mine) 

        #return the created block
        return block

    def UpdateBlockchain(self):

        target = self.sender()
        blockNumber = target.blockNum

        dataEditor = self.listOfBlocks[blockNumber - 1]["data"]
        prevBlockHashEditor = self.listOfBlocks[blockNumber - 1]["prevBlockHashEditor"]
        nonceSpin = self.listOfBlocks[blockNumber - 1]["nonceSpin"]
        currBlockHashEditor = self.listOfBlocks[blockNumber - 1]["currBlockHashEditor"]

        strDataToHash = str(blockNumber) + dataEditor.toPlainText() + prevBlockHashEditor.toPlainText() + str(nonceSpin.value())

        if strDataToHash == "" or dataEditor.toPlainText() == "":
            currBlockHashEditor.setText("")
            return

        strSelectedAlgo = self.hashingAlgoForBC.currentText()

        if strSelectedAlgo == "sha256":
            result = hashlib.sha256(strDataToHash.encode())
        if strSelectedAlgo == "sha384":
            result = hashlib.sha384(strDataToHash.encode())
        if strSelectedAlgo == "sha224":
            result = hashlib.sha224(strDataToHash.encode())
        if strSelectedAlgo == "sha512":
            result = hashlib.sha512(strDataToHash.encode())

        strOutputHash = result.hexdigest()
        currBlockHashEditor.setText(strOutputHash)

        if(blockNumber < len(self.listOfBlocks) and self.updateBlockchain == True):
            nextBlocksPrevHashEditor = self.listOfBlocks[blockNumber]["prevBlockHashEditor"]
            nextBlocksPrevHashEditor.setText(strOutputHash)
            
    def AddANewBlock(self):

        block = self.CreateNewBlock()

        self.horizLayout.addWidget(block)

        separator = QSplitter()
        separator.setMinimumWidth(10)
        self.horizLayout.addWidget(separator)
               
    def Mine(self):
        target = self.sender()
        blockNumber = target.blockNum

        currBlockTargetSpin = self.listOfBlocks[blockNumber - 1]["targetSpin"]
        currBlockNonceSpin = self.listOfBlocks[blockNumber - 1]["nonceSpin"]
        currBlockHashEditor = self.listOfBlocks[blockNumber - 1]["currBlockHashEditor"]
                
        strTarget = '0' * (currBlockTargetSpin.value())

        nonce = 0
        self.updateBlockchain = False
        miningSuccesful = False

        while nonce < 1e10:

            currBlockNonceSpin.setValue(nonce)
            strBlockHash = currBlockHashEditor.toPlainText()

            if strBlockHash.startswith(strTarget) == True:
                miningSuccesful = True
                break                

            nonce = nonce + 1

        self.updateBlockchain = True
        self.UpdateBlockchain()

        if miningSuccesful == False:
            msg.setText("Mining failed. Suitable has not found")
        
    def InitializeBlockchainTab(self):

        virtLayout1 = QVBoxLayout()
        self.blockChainTab.setLayout(virtLayout1)

        #hash algo to choose from combo box
        self.hashingAlgoForBC = QComboBox()
        self.hashingAlgoForBC.addItem("sha256")
        self.hashingAlgoForBC.addItem("sha384")
        self.hashingAlgoForBC.addItem("sha224")
        self.hashingAlgoForBC.addItem("sha512")
        virtLayout1.addWidget(self.hashingAlgoForBC)

        # this will have blockchain
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        virtLayout1.addWidget(scroll)        

        blockchainContainer = QWidget()
        self.horizLayout = QHBoxLayout()
        blockchainContainer.setLayout(self.horizLayout)
        scroll.setWidget(blockchainContainer)        

        for x in range(1):
          block = self.CreateNewBlock()
          self.horizLayout.addWidget(block)

          separator = QSplitter()
          separator.setMinimumWidth(10)
          self.horizLayout.addWidget(separator)

        addBlockButton = QPushButton("Add new block")
        virtLayout1.addWidget(addBlockButton)

        #connect
        addBlockButton.clicked.connect(self.AddANewBlock) 

    # method for components
    def UiComponents(self):

        self.setWindowTitle("Crypto App")
        #self.setStyleSheet("background-color: black;")

        self.hashTab = QWidget()
        self.blockChainTab = QWidget()

        self.addTab(self.hashTab,"Hashing Algo")
        self.addTab(self.blockChainTab,"Blockchain")

        self.InitializeHashTab()
        self.InitializeBlockchainTab()
        
    def hash(self):

        strSelectedAlgo = self.hashAlgoCombo.currentText()
        strInputData = self.inputEditor.toPlainText()
        
        if strInputData == "":
            self.outputEditor.setText("")
            return

        if strSelectedAlgo == "sha256":
            result = hashlib.sha256(strInputData.encode())
        if strSelectedAlgo == "sha384":
            result = hashlib.sha384(strInputData.encode())
        if strSelectedAlgo == "sha224":
            result = hashlib.sha224(strInputData.encode())
        if strSelectedAlgo == "sha512":
            result = hashlib.sha512(strInputData.encode())

        strOutputHash = result.hexdigest()
        self.outputEditor.setText(strOutputHash)
