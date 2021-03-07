import sys
from PyQt5.QtCore import Qt,QTime,QTimer,QDate,pyqtSignal, pyqtSlot,QThread
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QLabel, QSpacerItem, QSizePolicy,
                             QHBoxLayout,)
import os
from PyQt5.QtGui import QPixmap
import requests
import json
import copy
import numpy as np
import cv2
import face_recognition as fr
import scripts


class InfomirrorGUI(QWidget):
    def __init__(self, input,parent=None):
        super(InfomirrorGUI, self).__init__(parent)
        self.a = App(input['names'],input['encodings'])
        self.currentuser = 'None'
        self.grid = QGridLayout()
        self.setWindowTitle("Infomirror")
        self.showFullScreen()
        self.weather = InfomirrorWeather(input['cid'])
        self.news = InfomirrorNews(input['country'],input['category'])
        self.traffic = InfomirrorTraffic(input['quadkey'])
        self.rona = InfomirrorCorona(input['city'])

        spacer = QSpacerItem(300,200,QSizePolicy.Minimum)
        #self.grid.addItem(spacer,0,1)
        self.grid.addWidget(self.a,0,1)
        self.setLayout(self.grid)
        self.setWindowTitle("PyQt5 Group Box")

        self.lbl = QLabel()
        self.lbl.setFont(QtGui.QFont('Arial', 60))
        # setting centre alignment to the label
        self.lbl.setAlignment(Qt.AlignCenter)

        # adding label to the layout
        self.weather.layout.addWidget(self.lbl,0,0,Qt.AlignLeft)

        # creating a timer object
        timer = QTimer(self)

        # adding action to timer
        timer.timeout.connect(self.showTime)

        # update the timer every second
        timer.start(1000)
        #######################################################
        #######################################################
        #self.resize(1920, 1080)

    def startui(self,user):
        if self.currentuser in user:
            pass
        else:
            #config = scripts.get_user_config(user.replace('_','.'),'87afe80878b563e915db28911b8a2cd018e6e0e5')
            self.grid.addWidget(self.weather.getbox(), 0, 0)
            self.grid.addWidget(self.news.getbox(), 0, 2)
            self.grid.addWidget(self.traffic.getbox(),1,2)
            self.grid.addWidget(self.rona.getbox(), 1, 0)
            self.currentuser = user

    def closeui(self):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)
        self.grid.addWidget(self.a,0,1)
        self.currentuser = 'None'


    def showTime(self):

        # getting current time
        current_time = QTime.currentTime()

        # converting QTime object to string
        self.label_time = current_time.toString('hh:mm')

        # showing it to the label
        self.lbl.setText(self.label_time)


class InfomirrorGroupbox(QGroupBox):
    def __init__(self, parent=None):
        super(InfomirrorGroupbox, self).__init__(parent)
        self.groupBox = QGroupBox()

    def getbox(self):
        return self.groupBox


class InfomirrorWeather(InfomirrorGroupbox):
    def __init__(self, cid,parent=None):
        super(InfomirrorWeather, self).__init__(parent)
        self.icon = 45
        self.setweather(cid)

    def getweather(self,cid):
        api_key = "2f1b54024d7d3798e4d2956b19f496ce"

        url = "http://api.openweathermap.org/data/2.5/group?id=%s&units=metric&appid=%s" % (cid, api_key)
        response = requests.get(url)
        data = json.loads(response.text)
        return data

    def geticon(self):
        if 200 <= self.weather <= 232:
            self.icon = 27
        elif 300 <= self.weather <= 321:
            self.icon = 17
        elif 500 <= self.weather <= 531:
            self.icon = 18
        elif 600 <= self.weather <= 622:
            self.icon = 7
        elif 700 <= self.weather <= 781:
            self.icon = 5
        elif self.weather == 800:
            self.icon = 2
        elif self.weather == 801:
            self.icon = 8
        elif 802 <= self.weather <= 804:
            self.icon = 14

    def setweather(self,cid):
        self.data = self.getweather(cid)
        # Extracting all relevant info from the dict data
        self.current = self.data['list'][0]['main']
        self.mintemp = round(self.current['temp_min'])
        self.maxtemp = round(self.current['temp_max'])
        self.MinMaxlabel = QLabel(str(self.mintemp) + '°C to ' + str(self.maxtemp) + '°C')
        self.temp = QLabel(str(round(self.current['temp'],1)) + '°C')
        self.current = self.data['list'][0]['weather']
        self.weather = self.current[0]['id']
        # Set text sizes for the labels
        self.temp.setFont(QtGui.QFont('Arial', 60))
        self.MinMaxlabel.setFont(QtGui.QFont('Arial', 20))
        # Determine icon based on the data
        self.icon = 45
        self.geticon()
        self.weathericonlabel = QLabel('icon')
        self.weathericon = QtGui.QPixmap("assets/png/%s.png" % self.icon)
        self.weathericon = self.weathericon.scaled(115, 115)
        # Layout bullshit mostly trial and error lmao
        now = QDate.currentDate()
        self.datelabel = QLabel(now.toString(Qt.DefaultLocaleLongDate))
        self.datelabel.setFont(QtGui.QFont('Arial', 40))
        self.layout = QGridLayout()
        #######################################################
        #######################################################
        # creating a label object
        sublayout = QVBoxLayout()
        sublayout.setSpacing(0)
        sublayout.addWidget(self.temp, 0, Qt.AlignTop)
        sublayout.addWidget(self.MinMaxlabel, 1, Qt.AlignTop)
        self.layout.setSpacing(0)
        self.layout.addLayout(sublayout, 2, 0, Qt.AlignTop)
        self.layout.addWidget(self.datelabel,1,0,Qt.AlignTop)
        self.weathericonlabel.setPixmap(self.weathericon)
        self.layout.addWidget(self.weathericonlabel, 2, 1, Qt.AlignTop)
        self.groupBox.setLayout(self.layout)


class InfomirrorNews(InfomirrorGroupbox):
    def __init__(self,country,category, Parent=None):
        super(InfomirrorNews, self).__init__(Parent)

        self.data = self.getnews(country,category)
        self.setnews()

    def getnews(self,country,category):
        url = ('http://newsapi.org/v2/'+ category +'?'
                                                   'country=' + country + '&'
                                                                          'apiKey=bb1da63b525442119c597abc2275a5fa')
        response = requests.get(url)
        return response.json()['articles']

    def setnews(self):
        self.layout = QVBoxLayout()
        self.title1 = QLabel(self.data[0]['title'])
        self.title1.setFont(QtGui.QFont('Arial', 22, weight=QtGui.QFont.Bold))
        self.desc1 = QLabel(self.data[0]['description'])
        self.desc1.setFont(QtGui.QFont('Arial', 16))
        self.title1.setWordWrap(True)
        self.desc1.setWordWrap(True)

        self.title2 = QLabel(self.data[1]['title'])
        self.title2.setFont(QtGui.QFont('Arial', 22, weight=QtGui.QFont.Bold))
        self.desc2 = QLabel(self.data[1]['description'])
        self.desc2.setFont(QtGui.QFont('Arial', 16))
        self.title2.setWordWrap(True)
        self.desc2.setWordWrap(True)

        self.title3 = QLabel(self.data[2]['title'])
        self.title3.setFont(QtGui.QFont('Arial', 22, weight=QtGui.QFont.Bold))
        self.desc3 = QLabel(self.data[2]['description'])
        self.desc3.setFont(QtGui.QFont('Arial', 16))

        self.title3.setWordWrap(True)
        self.desc3.setWordWrap(True)
        self.layout.addWidget(self.title1, 0, Qt.AlignTop)
        self.layout.addWidget(self.desc1, 1, Qt.AlignTop)
        self.layout.addWidget(self.title2, 0, Qt.AlignTop)
        self.layout.addWidget(self.desc2, 1, Qt.AlignTop)
        self.layout.addWidget(self.title3, 0, Qt.AlignTop)
        self.layout.addWidget(self.desc3, 1, Qt.AlignTop)
        self.groupBox.setLayout(self.layout)

class InfomirrorTraffic(InfomirrorGroupbox):
    def __init__(self, quadkey,Parent=None):
        super(InfomirrorTraffic, self).__init__(Parent)
        self.settraffic(quadkey)

    def settraffic(self,quadkey):
        url = ('https://traffic.ls.hereapi.com/traffic/6.2/flow/json' + quadkey +
               '?apiKey=upuAQnHO45ru_gRpscpQniwppnbIc5XBY5wuS-1Zh3M'
               '&minjamfactor=8.0'
               '&maxjamfactor=10.0')
        response = requests.get(url)
        data = response.json()
        data = data['RWS'][0]['RW']
        rows, cols = (5, 3)
        biglist = [[0 for i in range(cols)] for j in range(rows)]

        for i in range(0, 5):
            biglist[i][0] = 0
            biglist[i][1] = -1
            biglist[i][2] = -1

        for i in data:
            for j in range(0, 5):
                if i['FIS'][0]['FI'][0]['TMC']['LE'] > biglist[j][0]:
                    copylist = copy.deepcopy(biglist)
                    for k in range(j + 1, 5):
                        biglist[k][0] = copylist[k - 1][0]
                        biglist[k][1] = copylist[k - 1][1]
                        biglist[k][2] = copylist[k - 1][2]
                    biglist[j][0] = round(i['FIS'][0]['FI'][0]['TMC']['LE'], 1)
                    biglist[j][1] = i['FIS'][0]['FI'][0]['TMC']['DE']
                    biglist[j][2] = i['DE']
                    break

        self.layout = QVBoxLayout()
        self.title1 = QLabel(
            'On ' + str(biglist[0][2]) + ' by ' + str(biglist[0][1]) + ' ' + str(biglist[0][0]) + ' km')
        self.title1.setFont(QtGui.QFont('Arial', 27, weight=QtGui.QFont.Bold))
        self.title2 = QLabel(
            'On ' + str(biglist[1][2]) + ' by ' + str(biglist[1][1]) + ' ' + str(biglist[1][0]) + ' km')
        self.title2.setFont(QtGui.QFont('Arial', 27, weight=QtGui.QFont.Bold))
        self.title3 = QLabel(
            'On ' + str(biglist[2][2]) + ' by ' + str(biglist[2][1]) + ' ' + str(biglist[2][0]) + ' km')
        self.title3.setFont(QtGui.QFont('Arial', 27, weight=QtGui.QFont.Bold))
        self.title4 = QLabel(
            'On ' + str(biglist[3][2]) + ' by ' + str(biglist[3][1]) + ' ' + str(biglist[3][0]) + ' km')
        self.title4.setFont(QtGui.QFont('Arial', 27, weight=QtGui.QFont.Bold))
        self.title5 = QLabel(
            'On ' + str(biglist[4][2]) + ' by ' + str(biglist[4][1]) + ' ' + str(biglist[4][0]) + ' km')
        self.title5.setFont(QtGui.QFont('Arial', 27, weight=QtGui.QFont.Bold))

        self.layout.addWidget(self.title1, 1, Qt.AlignTop)
        self.layout.addWidget(self.title2, 1, Qt.AlignTop)
        self.layout.addWidget(self.title3, 1, Qt.AlignTop)
        self.layout.addWidget(self.title4, 1, Qt.AlignTop)
        self.layout.addWidget(self.title5, 1, Qt.AlignTop)
        self.groupBox.setLayout(self.layout)


class InfomirrorCorona(InfomirrorGroupbox):
    def __init__(self,city, Parent = None):
        super(InfomirrorCorona, self).__init__(Parent)
        self.setrona(city)

    def setrona(self,city):
        url = (
                'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/'
                'arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/'
                'query?where=GEN%20%3D%20%27'+city+'%27'
                                                   '&outFields=county,last_update,cases7_per_100k,cases7_bl_per_100k,GEN,cases,deaths&outSR=4326&f=json')
        response = requests.get(url)
        data = response.json()
        data = data['features'][0]['attributes']
        self.Title = QLabel('COVID19 \n' + data['GEN'])
        self.Title.setFont(QtGui.QFont('Arial', 35, weight=QtGui.QFont.Bold))
        self.lastupdate = QLabel('Last update: ' + data['last_update'])
        self.lastupdate.setFont(QtGui.QFont('Arial', 20))
        self.cases7city = QLabel('Incidence: ' + str(round(data['cases7_per_100k'])))
        self.cases7city.setFont(QtGui.QFont('Arial', 25))
        self.cases7county = QLabel('Incidence for the county: ' + str(round(data['cases7_bl_per_100k'])))
        self.cases7county.setFont(QtGui.QFont('Arial', 25))
        self.ceasetoexist = QLabel('Total cases: ' + str(data['cases']) + ' Total deaths: ' + str(data['deaths']))
        self.ceasetoexist.setFont(QtGui.QFont('Arial', 25))
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.Title,0,Qt.AlignTop)
        self.layout.addWidget(self.lastupdate,1,Qt.AlignTop)
        self.layout.addWidget(self.cases7city,0,Qt.AlignTop)
        self.layout.addWidget(self.ceasetoexist,1,Qt.AlignTop)
        self.layout.addWidget(self.cases7county,0,Qt.AlignTop)
        self.groupBox.setLayout(self.layout)


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while True:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)

class FaceThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while True:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)

class App(QWidget):
    def __init__(self,names,encodings):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 1280
        self.display_height = 960
        self.faceupdater = 0
        self.facetimer = 0
        self.timeout = 0
        self.known_face_names = names
        self.known_face_encodings = encodings
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.image_label)
        self.vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(self.vbox)

        # create the video capture thread
        self.thread = VideoThread()
        self.facer = FaceThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.facer.change_pixmap_signal.connect(self.update_face)
        # start the thread
        self.thread.start()
        self.facer.start()

    def updatename(self):
        self.known_face_names, self.known_face_encodings = loaduserimages()


    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def update_face(self, cv_img):
        rgb_frame = cv_img[:, :, ::-1]
        self.facetimer += 1
        if self.faceupdater == 10:
            self.updatename()
            self.faceupdater = 0
        if self.timeout == 3:
            if window.currentuser != 'None':
                window.closeui()
        if self.facetimer % 30 == 0:
            self.faceupdater+=1
            self.facetimer = 0
            self.timeout+=1
            face_locations = fr.face_locations(rgb_frame)
            face_encodings = fr.face_encodings(rgb_frame, face_locations)
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = fr.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = fr.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    if name in self.known_face_names:
                        window.startui(name)
                        self.timeout = 0



    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

def loaduserimages():
    known_face_names = []
    known_face_encodings = []
    for filename in os.listdir('user_images/'):
        os.remove('user_images/' + filename)
    scripts.get_all_user_images('87afe80878b563e915db28911b8a2cd018e6e0e5')
    for filename in os.listdir('user_images/'):
        known_face_encodings.append(fr.face_encodings(fr.load_image_file('user_images/' + filename))[0])
        known_face_names.append(filename.removesuffix('.png'))
    return known_face_names, known_face_encodings




if __name__ == '__main__':
    known_face_names, known_face_encodings = loaduserimages()
    input = {'city': 'FRANKFURT%20AM%20MAIN', 'category': 'top-headlines', 'country' : 'de', 'cid' : "2925533",'quadkey':'/9/268/173','names': known_face_names,'encodings': known_face_encodings}
    app = QApplication(sys.argv)
    window = InfomirrorGUI(input)
    window.show()
    app.exit(app.exec_())

