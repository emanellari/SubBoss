import sys
import os
from PyQt5.QtCore import Qt, QUrl, QTimer, pyqtSignal
from PyQt5.QtGui import QPalette, QColor, QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QShortcut, \
   QLabel, QToolBar, QTextEdit, QComboBox, QDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from TransciptionReady import timestamps_to_milisekonds,miliseconds_to_timestamps,create_transcribe
from translate import Translator

def create_language_dialog(parent=None):
   dialog = QDialog(parent)
   dialog.setWindowTitle("Zgjedhja e Gjuhës")


   layout = QVBoxLayout(dialog)


   label = QLabel("Select language:")
   languageComboBox = QComboBox()
   languages = ['French', 'English', 'Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Azerbaijani', 'Basque', 'Belarusian',
                          'Bengali', 'Bosnian', 'Bulgarian', 'Catalan', 'Cebuano', 'Chichewa', 'Chinese (Simplified)', 'Chinese (Traditional)', 'Corsican', 'Croatian',
                          'Czech', 'Danish', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Filipino', 'Finnish', 'French', 'Frisian', 'Galician', 'Georgian',
                          'German', 'Greek', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic',
                          'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Korean', 'Kurdish (Kurmanji)', 'Kyrgyz',
                          'Lao', 'Latin', 'Latvian', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Maori', 'Marathi',
                          'Mongolian', 'Myanmar (Burmese)', 'Nepali', 'Norwegian', 'Odia', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Romanian', 'Russian',
                          'Samoan', 'Scots Gaelic', 'Serbian', 'Sesotho', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Spanish', 'Sundanese', 'Swahili',
                          'Swedish', 'Tajik', 'Tamil', 'Telugu', 'Thai', 'Turkish', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Xhosa', 'Yiddish',
                          'Yoruba', 'Zulu']
   language_codes = ['fr', 'en', 'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'ny',
                     'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl',
                     'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga',
                     'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg',
                     'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro',
                     'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg',
                     'ta', 'te', 'th', 'tr', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']


   print(language_codes)
   languageComboBox.addItems(languages)


   selectButton = QPushButton("Select")
   selectButton.clicked.connect(dialog.accept)


   layout.addWidget(label)
   layout.addWidget(languageComboBox)
   layout.addWidget(selectButton)
   lang=languageComboBox.currentText()






   return dialog, languageComboBox


   def get_selected_language(self):
       selected_language = self.languageComboBox.currentText()
       print("Gjuha e zgjedhur: {}".format(selected_language))
       self.accept()


def find_seg(self, current_time):
   all=0
   i=0
   for s in self.segments:
       if current_time >= s[0] and current_time<= s[1]:
           return s,i
           all=all+1
       i=i+1
   if all==0:
       return s,i




class ClickableTextEdit(QTextEdit):
   clicked = pyqtSignal()


   def mousePressEvent(self, event):
       self.clicked.emit()
       super().mousePressEvent(event)


class VideoPlayer(QWidget):
   def __init__(self):
       super().__init__()


       self.initUI()


   def initUI(self):
       self.setWindowTitle('Video Player')
       self.setGeometry(100, 100, 1000, 600)


       self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
       self.videoWidget = QVideoWidget()


       self.mediaPlayer.setVideoOutput(self.videoWidget)


       openButton = QPushButton('Open Video')
       openButton.clicked.connect(self.openFile)


       trancsribe_button=QPushButton('Transcribe')
       trancsribe_button.clicked.connect(self.Transcribe)


       trancslate_button = QPushButton('Translate')
       trancslate_button.clicked.connect(self.Translate)


       save_button = QPushButton('Save')
       save_button.clicked.connect(self.Save)


       import_srt_button = QPushButton('Import .srt')
       import_srt_button.clicked.connect(self.ImportSrt)






       toolbar = QToolBar()
       toolbar.addWidget(openButton)
       toolbar.addWidget(trancsribe_button)
       toolbar.addWidget(trancslate_button)
       toolbar.addWidget(save_button)
       toolbar.addWidget(import_srt_button)






       self.timeLabel = QLabel('Bottom')
       self.timeLabel.setFixedSize(200,30)


       toolbar.addWidget(self.timeLabel)
       layout = QVBoxLayout()
       sub_textbox = QHBoxLayout()
       left_sub_toolbox=QVBoxLayout()
       right_sub_toolbox=QVBoxLayout()


       self.textbox=ClickableTextEdit()
       self.textbox.setLineWidth(500)
       self.textbox.setFixedHeight(100)
       self.textbox.insertPlainText(' ')
       self.textbox.setStyleSheet(
           'background-color: black; color: white;')  # Vendos background-in zi dhe tekst të bardhë
       font = self.textbox.font()
       font.setPointSize(20)  # Rrit madhësinë e tekstit (ndryshoni vlerën sipas dëshirës)
       self.textbox.setFont(font)
       self.textbox.setAlignment(Qt.AlignCenter)
       self.segments=''
       self.smaller_start=QPushButton('⬱')
       self.bigger_start = QPushButton('⇶')
       self.smaller_end = QPushButton('⬱')
       self.bigger_end = QPushButton('⇶')
       left_sub_toolbox.addWidget(self.smaller_start)
       left_sub_toolbox.addWidget(self.bigger_start)
       right_sub_toolbox.addWidget(self.bigger_end)
       right_sub_toolbox.addWidget(self.smaller_end)
       sub_textbox.addLayout(left_sub_toolbox)
       sub_textbox.addWidget(self.textbox)
       sub_textbox.addLayout(right_sub_toolbox)
       layout.addWidget(toolbar)
       layout.addWidget(self.videoWidget)
       layout.addLayout(sub_textbox)




       self.setLayout(layout)


       self.defaultPath = os.path.expanduser("~/Downloads")


       self.videoWidget.mousePressEvent = self.playPauseVideo


       # Shto shkurtesat e tastierës për shkëmbimin 5 sekondave prapa dhe përpara
       self.shortcut_left = QShortcut(QKeySequence(Qt.CTRL+Qt.Key_K), self)
       self.shortcut_left.activated.connect(lambda :self.skipBackward(5000))


       self.shortcut_right = QShortcut(QKeySequence(Qt.CTRL+Qt.Key_L), self)
       self.shortcut_right.activated.connect(lambda :self.skipForward(5000))
       self.textbox.clicked.connect(self.while_textbox_is_clicked)


       self.smaller_start.clicked.connect(self.SmallerStart)
       self.bigger_start.clicked.connect(self.BiggerStart)
       self.smaller_end.clicked.connect(self.SmallerEnd)
       self.bigger_end.clicked.connect(self.BiggerEnd)


       # Nis një timer për të përditësuar kohën çdo 500 milisekonda (0.5 sekondë)


       self.timer = QTimer(self)
       self.timer.timeout.connect(self.updateTime)
       self.timer.start(500)
       self.focused_i=[0]


   def SmallerStart(self):
       current_time = self.mediaPlayer.position()
       lim1, limi = find_seg(self, current_time)
       key = lim1[0] - 500
       if limi==0:
           self.mediaPlayer.setPosition(0)
       elif limi==1:
           print('elif')
           if key>=500:
               self.segments[1][0]=key
               self.segments[0][1]=key
               self.lim1 = self.segments[limi]
               self.mediaPlayer.setPosition(key+1)
               print(lim1)
       else:
           print('else')
           if key >= self.segments[limi-1][0]+500:
               self.segments[limi][0]=key
               self.segments[limi-1][1]=key
               self.lim1 = self.segments[limi]
               self.mediaPlayer.setPosition(key+1)
               print(lim1)
           elif key >= self.segments[limi-2][0]+1000:
               self.segments[limi - 2][1] = key - 500
               self.segments[limi - 1][0] = key - 500
               self.segments[limi - 1][1] = key
               self.segments[limi][0]=key+1
               self.lim1 = self.segments[limi]
               self.mediaPlayer.setPosition(key+1)
               print(lim1)










   def SmallerEnd(self):
       current_time = self.mediaPlayer.position()
       lim1, limi = find_seg(self, current_time)
       key=lim1[1]-500
       if key>lim1[0] and limi!=len(self.segments):
           print(f'range={len(self.segments)},index1={self.limi},sg={self.segments[self.limi]}')
           self.segments[limi][1]=key
           self.segments[limi + 1][0] = key
           self.lim1 = self.segments[limi]
           self.mediaPlayer.setPosition(max(key, 0)-500)


       print(self.segments[limi])


   def BiggerStart(self):
       print('bigger start')
       current_time = self.mediaPlayer.position()
       lim1, limi = find_seg(self, current_time)
       key = lim1[0] + 500
       p=key
       if limi!=0 and key<lim1[1]:
           print('plotesohet')
           self.segments[limi][0]=key
           self.segments[limi-1][1]=key
           self.lim1 = self.segments[limi]


           self.mediaPlayer.setPosition(p+1)


           print(self.lim1)


   def BiggerEnd(self):
       current_time = self.mediaPlayer.position()
       lim1, limi = find_seg(self, current_time)
       key = lim1[1] + 500
       n=len(self.segments)
       duration=self.mediaPlayer.duration()
       if limi == n-1:
           self.mediaPlayer.setPosition(self.segments[n-1][1]-500)
       elif limi == n-2:
           print('elif')
           if key >= duration-500:
               self.segments[n-2][1] = key
               self.segments[n-1][0] = key
               self.lim1 = self.segments[limi]
               self.mediaPlayer.setPosition(key -500)
               print(lim1)
       else:
           print('else')
           if key <= self.segments[limi + 1][1] - 500:
               self.segments[limi][1] = key
               self.segments[limi + 1][0] = key
               self.lim1 = self.segments[limi]
               self.mediaPlayer.setPosition(key-500)
               print(lim1)
           elif key <= self.segments[limi + 2][1] - 1000:
               self.segments[limi + 2][0] = key + 500
               self.segments[limi + 1][1] = key + 500
               self.segments[limi + 1][0] = key
               self.segments[limi][1] = key
               self.lim1 = self.segments[limi]
               self.mediaPlayer.setPosition(key -500)
               print(lim1)




   def ImportSrt(self):
       pass
   def Transcribe(self):
       try:
           dialog, languageComboBox = create_language_dialog()
           result = dialog.exec_()
           lang=languageComboBox.currentText()
           print('lang=', lang)
           languages = ['French', 'English', 'Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Azerbaijani',
                        'Basque', 'Belarusian',
                        'Bengali', 'Bosnian', 'Bulgarian', 'Catalan', 'Cebuano', 'Chichewa', 'Chinese (Simplified)',
                        'Chinese (Traditional)', 'Corsican', 'Croatian',
                        'Czech', 'Danish', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Filipino', 'Finnish',
                        'French', 'Frisian', 'Galician', 'Georgian',
                        'German', 'Greek', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hebrew',
                        'Hindi', 'Hmong', 'Hungarian', 'Icelandic',
                        'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer',
                        'Korean', 'Kurdish (Kurmanji)', 'Kyrgyz',
                        'Lao', 'Latin', 'Latvian', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay',
                        'Malayalam', 'Maltese', 'Maori', 'Marathi',
                        'Mongolian', 'Myanmar (Burmese)', 'Nepali', 'Norwegian', 'Odia', 'Pashto', 'Persian', 'Polish',
                        'Portuguese', 'Punjabi', 'Romanian', 'Russian',
                        'Samoan', 'Scots Gaelic', 'Serbian', 'Sesotho', 'Shona', 'Sindhi', 'Sinhala', 'Slovak',
                        'Slovenian', 'Somali', 'Spanish', 'Sundanese', 'Swahili',
                        'Swedish', 'Tajik', 'Tamil', 'Telugu', 'Thai', 'Turkish', 'Ukrainian', 'Urdu', 'Uyghur',
                        'Uzbek', 'Vietnamese', 'Welsh', 'Xhosa', 'Yiddish',
                        'Yoruba', 'Zulu']
           language_codes = ['fr', 'en', 'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb',
                             'ny',
                             'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy',
                             'gl',
                             'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig',
                             'id', 'ga',
                             'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk',
                             'mg',
                             'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt', 'pa',
                             'ro',
                             'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv',
                             'tg',
                             'ta', 'te', 'th', 'tr', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']
           for i in range(len(languages)):
               if lang == languages[i]:
                   fixedi = i
           code = language_codes[fixedi]
           self.default_original_language=code
       except Exception as e:
           print(f"Gabim: {e}")
       starts, ends, sentences = create_transcribe(self.fileurl, self.mediaPlayer.duration(),self.default_original_language)
       self.data = [starts, ends, sentences]
       segments = [[0, self.data[0][0], ''], [self.data[0][0], self.data[1][0], self.data[2][0]]]
       for i in range(len(self.data[2])):
           if i != 0:
               segments.append([self.data[1][i - 1], self.data[0][i], ''])
               segments.append([self.data[0][i], self.data[1][i], self.data[2][i]])
       self.duration = self.mediaPlayer.duration()
       segments.append([self.data[1][i], self.duration, ''])
       print(segments)
       self.lim1 = segments[0]
       self.limi = 0
       self.ilim = 0
       self.segments = segments
   def Translate(self):


       dialog, languageComboBox = create_language_dialog()
       result = dialog.exec_()
       lang = languageComboBox.currentText()
       print('lang=', lang)
       languages = ['French', 'English', 'Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Azerbaijani',
                    'Basque', 'Belarusian',
                    'Bengali', 'Bosnian', 'Bulgarian', 'Catalan', 'Cebuano', 'Chichewa', 'Chinese (Simplified)',
                    'Chinese (Traditional)', 'Corsican', 'Croatian',
                    'Czech', 'Danish', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Filipino', 'Finnish',
                    'French', 'Frisian', 'Galician', 'Georgian',
                    'German', 'Greek', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hebrew',
                    'Hindi', 'Hmong', 'Hungarian', 'Icelandic',
                    'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer',
                    'Korean', 'Kurdish (Kurmanji)', 'Kyrgyz',
                    'Lao', 'Latin', 'Latvian', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay',
                    'Malayalam', 'Maltese', 'Maori', 'Marathi',
                    'Mongolian', 'Myanmar (Burmese)', 'Nepali', 'Norwegian', 'Odia', 'Pashto', 'Persian', 'Polish',
                    'Portuguese', 'Punjabi', 'Romanian', 'Russian',
                    'Samoan', 'Scots Gaelic', 'Serbian', 'Sesotho', 'Shona', 'Sindhi', 'Sinhala', 'Slovak',
                    'Slovenian', 'Somali', 'Spanish', 'Sundanese', 'Swahili',
                    'Swedish', 'Tajik', 'Tamil', 'Telugu', 'Thai', 'Turkish', 'Ukrainian', 'Urdu', 'Uyghur',
                    'Uzbek', 'Vietnamese', 'Welsh', 'Xhosa', 'Yiddish',
                    'Yoruba', 'Zulu']
       language_codes = ['fr', 'en', 'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb',
                         'ny',
                         'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy',
                         'gl',
                         'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig',
                         'id', 'ga',
                         'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk',
                         'mg',
                         'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt', 'pa',
                         'ro',
                         'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv',
                         'tg',
                         'ta', 'te', 'th', 'tr', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']
       for i in range(len(languages)):
           if lang == languages[i]:
               fixedi = i
       code = language_codes[fixedi]
       self.default_final_language=code
       print(code)
       print(self.default_original_language)
       print(self.default_final_language)


       translator = Translator(from_lang=self.default_original_language, to_lang=self.default_final_language)
       print(self.segments)
       for x in self.segments:
          tra_line=translator.translate(x[2])
          print(tra_line)
          x[2]=tra_line.replace(" '","'").replace("- A gjete një kamion?",'').replace('- Baltimore? - Ku bie?','Çfarë')
       self.default_original_language=self.default_final_language
   def Save(self):
       options = QFileDialog.Options()
       options |= QFileDialog.DontUseNativeDialog
       fileName, _ = QFileDialog.getSaveFileName(self, "Save Subtitles", "", "Subtitles Files (*.srt);;All Files (*)",
                                                 options=options)


       if fileName:
           subtitles_text = ""
           with open(fileName, "w", encoding='utf-16') as file:
               j=0
               prev_end=0
               for i in range(len(self.segments)):
                   if self.segments[i][2]!='':
                       j=j+1
                       file.write(f'{j}\n')
                       if self.segments[i][0]>=prev_end:
                           st=miliseconds_to_timestamps(self.segments[i][0])
                       else:
                           st=miliseconds_to_timestamps(prev_end)


                       timstamp=st+' --> '+miliseconds_to_timestamps(self.segments[i][1])
                       file.write(f'{timstamp}\n')
                       file.write(f'{self.segments[i][2]}\n\n')
                       prev_end = self.segments[i][1]
   def while_textbox_is_clicked(self):
       self.mediaPlayer.pause()
       self.shortcut_left.activated.connect(lambda:self.skipBackward(5000))
       self.shortcut_right.activated.connect(lambda:self.skipForward(5000))
   def openFile(self):
       options = QFileDialog.Options()
       options |= QFileDialog.DontUseNativeDialog
       fileName, _ = QFileDialog.getOpenFileName(self, "Open Video", self.defaultPath, "Video Files (*.mp4 *.avi *.mkv);;All Files (*)", options=options)
       self.fileurl=fileName
       if fileName:
           mediaContent = QMediaContent(QUrl.fromLocalFile(fileName))
           self.mediaPlayer.setMedia(mediaContent)


   def playPauseVideo(self, event):
       if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
           self.mediaPlayer.pause()
       else:
           self.mediaPlayer.play()


   def onButtonClick(self, index):
       print(f'Button {index + 1} clicked')  # Përdoroni funksionin e përshtatur sipas nevojës


   def skipBackward(self,milisek):
       position = self.current_time - 5000  # 5000 milliseconds (5 seconds)
       self.mediaPlayer.setPosition(max(position, 0))


   def skipForward(self,milisek):
       position = self.current_time + 5000  # 5000 milliseconds (5 seconds)
       self.mediaPlayer.setPosition(min(position, self.mediaPlayer.duration()))








   def updateTime(self):
       self.current_time = self.mediaPlayer.position()
       self.timeLabel.setText(f"{miliseconds_to_timestamps(self.current_time)}")
       if len(self.segments)!=0:
           if self.current_time<self.lim1[0] or self.current_time> self.lim1[1]:
                   self.segments[self.limi][2]=self.textbox.toPlainText()
                   print(self.current_time)
                   self.lim1,self.limi=find_seg(self,self.current_time)
                   self.textbox.clear()
                   self.textbox.insertPlainText(self.lim1[2])
                   self.textbox.setAlignment(Qt.AlignCenter)










if __name__ == '__main__':
   app = QApplication(sys.argv)
   app.setApplicationName('Video Player')


   player = VideoPlayer()
   player.show()


   sys.exit(app.exec_())

