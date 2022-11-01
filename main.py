import sys
from PyQt5.QtCore import Qt, QUrl, QDir
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, \
    QFrame, QGraphicsDropShadowEffect, QGraphicsView, QGraphicsScene, QLabel, \
    QPushButton, QHBoxLayout, QListWidget, QFileDialog
from PyQt5.QtGui import QGradient, QFont, QColor, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist, \
    QMediaMetaData

class Pencere(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Müzik Çalar")

        # Konteyner Oluşturma

        btn_box = QHBoxLayout()
        btn_box2 = QHBoxLayout()
        konteyner = QGridLayout()
        bilgi_konteyner = QGridLayout()
        cerceve = QFrame()
        cerceve.setFrameShape(QFrame.Box)
        cerceve.setFrameShadow(QFrame.Sunken)
        cerceve.setLayout(bilgi_konteyner)

        # Kelime Oluşturma

        self.dir = f"{QDir.currentPath()}"
        self.url = QUrl()
        self.player = QMediaPlayer()
        self.content = QMediaContent()
        self.playlist = QMediaPlaylist(self.player)
        self.player.setPlaylist(self.playlist)

        # Çalma Listesini Otomatik Güncellenmesi


        self.playlist.currentIndexChanged.connect(self._guncelleme)



        self.player.metaDataChanged.connect(self.meta_data)

        # Etiket için bilgiler

        self.sanatci = QLabel("Sanatçı: ")
        self.album_ismi = QLabel("Albüm İsmi: ")
        self.parca_ismi = QLabel("Parça İsmi: ")
        self.piyasaya_cikis_tarihi = QLabel("Piyasa Çıkış Tarihi: ")
        self.tur = QLabel("Tür: ")
        self.art = QLabel()

        # Bilgi Konteynerine  Bilgileri Ekleme

        bilgi_konteyner.addWidget(self.sanatci, 0, 0, 1, 1)
        bilgi_konteyner.addWidget(self.album_ismi, 1, 0, 1, 1)
        bilgi_konteyner.addWidget(self.parca_ismi, 2, 0, 1, 1)
        bilgi_konteyner.addWidget(self.piyasaya_cikis_tarihi, 3, 0, 1, 1)
        bilgi_konteyner.addWidget(self.tur, 4, 0, 1, 1)
        bilgi_konteyner.addWidget(self.art, 5, 0, 1, 1)
        # Durum oluşturma ve Etiket Takip Etme

        self.status = QLabel("Durum: ")
        self.status.setFrameShape(QFrame.Box)
        self.status.setFrameShadow(QFrame.Sunken)

        self.track =QLabel("İzlemek: ")
        self.track.setFrameShadow(QFrame.Sunken)
        self.track.setFrameShape(QFrame.Box)

        # Liste kutusunu tanımlama ve oluşturma

        self.muzik_listesi = QListWidget()
        self.muzik_listesi.setFrameShape(QFrame.Box)
        self.muzik_listesi.setFrameShadow(QFrame.Sunken)
        self.muzik_listesi.setStyleSheet("background-color: snow;")

        # İki kere tıklandığında parça oynatma

        self.muzik_listesi.itemDoubleClicked.connect(self._cifttiklama)

        # Kontrol Düğmesinin Stilini Ayarlama

        btn_style = '''QPushButton{background-color: snow;}
                       QPushButton:hover{background-color: lightskyblue; color: dodgerblue; \
                       font-weight: bold;}'''
        # Ses dosyalarını ekleme ve Çalma listesini temizleme

        dosya_btn = QPushButton("Dosya Ekle ")
        dosya_btn.released.connect(self._dosya)
        dosya_btn.setCursor(Qt.PointingHandCursor)
        dosya_btn.setStyleSheet(btn_style)
        dosya_btn.setMaximumWidth(100)

        temizleme_btn = QPushButton("Temizle ")
        temizleme_btn.released.connect(self._temizleme)
        temizleme_btn.setCursor(Qt.PointingHandCursor)
        temizleme_btn.setStyleSheet(btn_style)
        temizleme_btn.setMaximumWidth(100)

        # Kontrol Düğmelerini oluşturma

        self.oynat_btn = QPushButton("Oynat")
        self.oynat_btn.released.connect(self._belirti)
        self.oynat_btn.setCursor(Qt.PointingHandCursor)
        self.oynat_btn.setStyleSheet(btn_style)

        self.onceki_btn = QPushButton("Geri")
        self.onceki_btn.released.connect(self._Stackgeri)
        self.onceki_btn.setCursor(Qt.PointingHandCursor)
        self.onceki_btn.setStyleSheet(btn_style)

        self.ileri_btn = QPushButton("İleri")
        self.ileri_btn.released.connect(self._Queueileri)
        self.ileri_btn.setCursor(Qt.PointingHandCursor)
        self.ileri_btn.setStyleSheet(btn_style)

        self.dur_btn = QPushButton("Dur")
        self.dur_btn.released.connect(self._dur)
        self.dur_btn.setCursor(Qt.PointingHandCursor)
        self.dur_btn.setStyleSheet(btn_style)

        self.cikis_btn = QPushButton("Çıkış")
        self.cikis_btn.released.connect(sys.exit)
        self.cikis_btn.setCursor(Qt.PointingHandCursor)
        self.cikis_btn.setStyleSheet("QPushButton{background-color: firebrick;} \
                                    QPushButton:hover{background-color: red; color: white; \
                                    font-weight: bold;}")

        # Butonlar için Düzenleme

        btn_box.addWidget(dosya_btn)
        btn_box.addWidget(temizleme_btn)
        btn_box2.addWidget(self.oynat_btn)
        btn_box2.addWidget(self.onceki_btn)
        btn_box2.addWidget(self.ileri_btn)
        btn_box2.addWidget(self.dur_btn)
        btn_box2.addWidget(self.cikis_btn)

        # Konteynerlar için Düzenleme

        konteyner.addWidget(self._baslik_olusturma(100, 100, 40, "MÜZİK ÇALAR"), 0, 0, 1, 3)
        konteyner.addWidget(self.status, 1, 0, 1, 1)
        konteyner.addWidget(self.track, 1, 1, 1, 1)
        konteyner.addLayout(btn_box, 1, 2, 1, 1)
        konteyner.addWidget(cerceve, 2, 0, 2, 1)
        konteyner.addWidget(self.muzik_listesi, 2, 1, 1, 2)
        konteyner.addLayout(btn_box2, 3, 1, 1, 2)
        konteyner.addWidget(self._baslik_olusturma(40, 40, 10, ""), 4, 0, 1, 3)

        # Widget Düğme Ekleme

        widget = QWidget()
        widget.setLayout(konteyner)
        self.setCentralWidget(widget)

        # Müzikleri Çekme Fonksiyonu

    def meta_data(self):
        if self.player.isMetaDataAvailable():
            self.sanatci.setText(f"Sanatçı: {self.player.metaData(QMediaMetaData.AlbumArtist)}")
            self.album_ismi.setText(f"Albüm İsmi: {self.player.metaData(QMediaMetaData.AlbumTitle)}")
            self.parca_ismi.setText(f"Parça İsmi: {self.player.metaData(QMediaMetaData.Title)}")
            self.piyasaya_cikis_tarihi.setText(f"Çıkış Tarihi: {self.player.metaData(QMediaMetaData.Year)}")
            self.tur.setText(f"Tür: {self.player.metaData(QMediaMetaData.Genre)}")
            self.track.setText(f"İzlemek: {self.player.metaData(QMediaMetaData.Title)}")
            pixmap = QPixmap(self.player.metaData(QMediaMetaData.CoverArtImage))
            pixmap = pixmap.scaled(int(pixmap.width() / 3), int(pixmap.height() / 3))
            self.art.setPixmap(pixmap)

        # Başlık Oluşturma Fonksiyonu

    def _baslik_olusturma(self, minyuksek, maxyuksek, yaziboyutu, metin):
        golge = QGraphicsDropShadowEffect()
        golge.setBlurRadius(3)
        golge.setOffset(3, 3)

        ekran = QGraphicsScene()

        gorus = QGraphicsView()
        gorus.setMinimumSize(800, minyuksek)
        gorus.setMaximumHeight(maxyuksek)
        gorus.setScene(ekran)

        egim = QGradient(QGradient.RichMetal)

        ekran.setBackgroundBrush(egim)

        yazi = QFont("Consolas", yaziboyutu, QFont.Bold)

        metin = ekran.addText(metin)
        metin.setDefaultTextColor(QColor(250, 250, 250))
        metin.setFont(yazi)

        metin.setGraphicsEffect(golge)

        return gorus

    # Parçaya Çift Tıklama Ve Oynatma Fonksiyonu

    def _cifttiklama(self):
        self.playlist.setCurrentIndex(self.muzik_listesi.currentRow())
        self.player.play()

    # Müzik Listesini Temizleme Fonksiyonu

    def _temizleme(self):
        self.player.stop()
        self.muzik_listesi.clear()
        self.playlist.clear()
        self.oynat_btn.setText("Oynat")
        self.status.setText("Durum: ")
        self.track.setText("İzle: ")
        self.sanatci.setText("Sanatçı: ")
        self.album_ismi.setText("Albüm: ")
        self.parca_ismi.setText("Parça ")
        self.piyasaya_cikis_tarihi.setText("Tarih: ")
        self.tur.setText("Tür: ")
        pixmap = QPixmap()
        self.art.setPixmap(pixmap)

    # Müzik Listesine Dosya Ekleme Fonksiyonu

    def _dosya(self):
        dosya = QFileDialog.getOpenFileNames(None, "Dosya Ekle",
                                             filter="Audio Files (*.mp3 *.amr *.ogg *.wav)")
        for file in dosya[0]:
            self.playlist.addMedia(QMediaContent(self.url.fromLocalFile(file)))
            file = file.split("/")
            self.muzik_listesi.addItem(f"{file[-1][:-4]}")


        self.muzik_listesi.setCurrentRow(0)
        self.playlist.setCurrentIndex(0)

    # Kontrol Butonların Fonksiyonları

    def _Stackgeri(self):
        if self.playlist.previousIndex == -1:
            self.playlist.setCurrentIndex(self.playlist.mediaCount() - 1)
        else:
            self.playlist.previous()

    def _Queueileri(self):
        self.playlist.next()
        if self.playlist.currentIndex() == -1:
            self.playlist.setCurrentIndex(0)
            self.player.play()

    def _dur(self):
        self.player.stop()
        self.oynat_btn.setText("Oynat")
        self.playlist.setCurrentIndex(0)
        self.muzik_listesi.setCurrentRow(0)
        self.status.setText("Durum: Durduruldu")

    def _belirti(self):
        if self.playlist.mediaCount() > 0:
            if self.player.state() != QMediaPlayer.PlayingState:
                self.oynat_btn.setText("Dur")
                self.status.setText("Durum: Oynatılıyor")
                self.player.play()
            else:
                self.oynat_btn.setText("Oynat")
                self.player.pause()
                self.status.setText("Durum: Durduruldu")
        else:
            pass

    # Liste Kutusu Güncelleme Fonksiyonu

    def _guncelleme(self):
        self.muzik_listesi.setCurrentRow(self.playlist.currentIndex())
        if self.playlist.currentIndex() < 0:
            self.muzik_listesi.setCurrentRow(0)
            self.playlist.setCurrentIndex(0)
# Uygulamaya Dönüştürme Ve Obje Oluşturma Fonksiyonu

def main():
    app = QApplication(sys.argv)
    pencere = Pencere()
    pencere.show()
    sys.exit(app.exec()) 


# Uygulamayı Çalıştırma

if __name__ == '__main__':
    main()










