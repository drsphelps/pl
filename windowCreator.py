import sys
from utils.dbManager import getDBConnector
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QLabel, QHeaderView
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItemModel

from datetime import datetime

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Playlist Generator'
        self.getSongList()
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout(self)
        central_widget.setLayout(grid_layout)

        self.createSongTable()
        self.createPlaylistTable()

        self.songTableWidget.resizeColumnsToContents()
        grid_layout.addWidget(self.songTableWidget, 0, 0)
        self.playlistTableWidget.resizeColumnsToContents()
        grid_layout.addWidget(self.playlistTableWidget, 0, 1)

        self.playlistTableWidget.resizeColumnsToContents()
        self.songTableWidget.resizeColumnsToContents()
        # Show widget
        self.show()

    def createPlaylistTable(self):
        # Create table
        self.playlistTableWidget = QTableWidget()
        self.playlistTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.playlistTableWidget.horizontalHeader().setStretchLastSection(True)
        self.playlistTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.playlistTableWidget.horizontalHeader().hide()
        self.playlistTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.playlistTableWidget.setRowCount(1)
        self.playlistTableWidget.setColumnCount(4)
        self.playlistTableWidget.setItem(0, 0,  QTableWidgetItem(""))
        self.playlistTableWidget.setItem(0, 1,  QTableWidgetItem(""))
        self.playlistTableWidget.setItem(0, 2,  QTableWidgetItem("Total:  "))
        self.playlistTableWidget.setItem(0, 3,  QTableWidgetItem("00:00:00"))
        self.playlistTableWidget.move(0,0)

        self.playlistTableWidget.doubleClicked.connect(self.onClickSub)

    @pyqtSlot()
    def onClickSub(self):
        sel = self.playlistTableWidget.selectedItems()

        print(sel)

        rowPosition = self.playlistTableWidget.rowCount() - 1
        currentLength = datetime.strptime(self.playlistTableWidget.item(rowPosition, 3).text(), "%H:%M:%S")
        toAdd = datetime.strptime(sel[3].text(), "%H:%M:%S")
        time_zero = datetime.strptime('00:00:00', '%H:%M:%S')
        newTotal = str((time_zero + (currentLength - toAdd)).time())
        self.playlistTableWidget.setItem(rowPosition, 3, QTableWidgetItem(newTotal))

        if sel[0].row() != self.playlistTableWidget.rowCount() - 1:
            self.playlistTableWidget.removeRow(sel[0].row())

    def getSongList(self):
        conn = getDBConnector('SRDB.sqlite')
        cursor = conn.cursor()

        query = """ SELECT Song.SongTitle, Artist.ArtistName, Album.AlbumName, Song.Length, Song.PlayCount, Song.Playable, Song.Link
                    FROM Song, Artist, Album
                    WHERE Song.Artist = Artist.ArtistID
                    AND Song.Album = Album.AlbumID;"""

        cursor.execute(query)
        songs = cursor.fetchall()
        self.songs = songs

    def createSongTable(self):
        # Create table
        self.songTableWidget = QTableWidget()
        self.songTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.songTableWidget.setHorizontalHeaderLabels(('Song', 'Artist', 'Album', 'Length', 'Play Count', 'Playable', "Link"))
        self.songTableWidget.verticalHeader().hide()

        self.songTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.songTableWidget.setRowCount(len(self.songs))
        self.songTableWidget.setColumnCount(7)
        row = 0
        for song in self.songs:
            for col in range(0, 7):
                item = song[col]
                if col == 4:
                    item = str(item)
                if col == 5:
                    if item == 0:
                        item = "No"
                    else:
                        item = "Yes"
                if col == 6:
                    if item is None:
                        item = "No link found"
                    else:
                        item = item.split('"')[1]
                self.songTableWidget.setItem(row, col, QTableWidgetItem(item))
            row+=1
        self.songTableWidget.move(0,0)

        self.songTableWidget.doubleClicked.connect(self.onClickAdd)

    @pyqtSlot()
    def onClickAdd(self):
        row = self.songTableWidget.selectedItems()

        rowPosition = self.playlistTableWidget.rowCount() - 1
        currentLength = datetime.strptime(self.playlistTableWidget.item(rowPosition, 3).text(), "%H:%M:%S")
        toAdd = datetime.strptime(row[3].text(), "%H:%M:%S")
        time_zero = datetime.strptime('00:00:00', '%H:%M:%S')
        newTotal = str((currentLength - time_zero + toAdd).time())
        self.playlistTableWidget.setItem(rowPosition, 3, QTableWidgetItem(newTotal))
        self.playlistTableWidget.insertRow(rowPosition)
        self.playlistTableWidget.setItem(rowPosition , 0,  QTableWidgetItem(row[0].text()))
        self.playlistTableWidget.setItem(rowPosition , 1,  QTableWidgetItem(row[1].text()))
        self.playlistTableWidget.setItem(rowPosition , 2,  QTableWidgetItem(row[2].text()))
        self.playlistTableWidget.setItem(rowPosition , 3,  QTableWidgetItem(row[3].text()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
