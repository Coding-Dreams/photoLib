import PySide6 as pyS
import fullScreenWin as FSW

class VideoPlayer(pyS.QtMultimediaWidgets.QVideoWidget):
    
    def __init__(self, file):

        #get file for media
        self.file = file

        #create media player widget (which will be added to the grid on main gui)
        self.homeWidget = pyS.QtWidgets.QWidget()
        self.homeWidget.setMinimumSize(pyS.QtCore.QSize(400,400))
        self.homeWidget.setMaximumSize(pyS.QtCore.QSize(400,400))

        self.gridLayout = pyS.QtWidgets.QBoxLayout(pyS.QtWidgets.QBoxLayout.TopToBottom, self.homeWidget)


        #define and initialize Player
        self.player = pyS.QtMultimedia.QMediaPlayer()
        #self.player.setNotifyInterval(100)
        self.player.setSource(pyS.QtCore.QUrl.fromLocalFile(file.replace("\\","/")))

        #for le Audio
        self.audioOutput = pyS.QtMultimedia.QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(100)

        #create movie object and pass to player
        self.movieWidgetObj = pyS.QtMultimediaWidgets.QVideoWidget(self.homeWidget)
        self.movieWidgetObj.setMinimumSize(pyS.QtCore.QSize(400,380))
        self.movieWidgetObj.setMaximumSize(pyS.QtCore.QSize(400,380))
        self.player.setVideoOutput(self.movieWidgetObj)

        #add movie object to widget
        self.gridLayout.addWidget(self.movieWidgetObj)

        self.gridForButtons = pyS.QtWidgets.QBoxLayout(pyS.QtWidgets.QBoxLayout.LeftToRight)
        self.gridLayout.addLayout(self.gridForButtons)

        #define play button
        self.playButton = pyS.QtWidgets.QPushButton("Play")
        self.playButton.clicked.connect(self.execPlay)
        self.gridForButtons.addWidget(self.playButton, stretch=1)

        #define Seek bar
        self.seekBar = pyS.QtWidgets.QSlider(pyS.QtCore.Qt.Horizontal)
        self.seekBar.sliderMoved.connect(self.set_position)
        self.gridForButtons.addWidget(self.seekBar, stretch=5)

        #make infrastructure for slider (stolen from StuDig on SO)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)

        #define fullscreen button
        self.fullScreenButton = pyS.QtWidgets.QPushButton("Full")
        self.fullScreenButton.clicked.connect(self.fullScreen)
        self.gridForButtons.addWidget(self.fullScreenButton, stretch=1)

        #fullscreen window
        

    def execPlay(self):
        if self.player.isPlaying():
            self.player.pause()
        else:
            self.player.play()

    def getWidget(self):
        return self.homeWidget
    
    def fullScreen(self):
        return
        # self.fullScreenWindow = FSW.fullscreen(self.movieWidgetObj)
        # if self.fullScreenWindow.isVisible():
        #     self.fullScreenWindow.hide()
        # else:
        #     self.fullScreenWindow.show()
    
    def set_position(self, position):
        self.player.setPosition(position)

    def position_changed(self, position):
        self.seekBar.setValue(position)

    def duration_changed(self, duration):
        self.seekBar.setRange(0, duration)
