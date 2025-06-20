import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка

from PIL import ImageEnhance

# 2) Перейди к полю настройки контраста объекта ImageEnhance (команда: pic_contrast = ImageEnhance.Contrast(pic_original)).

# 3) Увеличь контраст на 50% (команда: pic_contrast = pic_contrast.enhance(1.5)).
from PIL import Image
# from PIL.ImageQt import ImageQt # для перевода графики из Pillow в Qt 
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)


class ImageProcessor() :
    def __init__(self) :
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'new_image'
    
    def loadImage(self, dir, filename) :
        self.filename = filename
        self.dir = dir
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    
    def showImage(self, path) :
        pikcher.hide()
        pixmapimage = QPixmap(path)
        w, h = pikcher.width(), pikcher.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        pikcher.setPixmap(pixmapimage)
        pikcher.show()

    def saveImage(self) :
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)) :
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    
    def do_dw(self) :
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_flip(self) :
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_blur(self) :
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_left(self) :
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self) :
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_contrast(self) :
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)



workimage = ImageProcessor()

def showChosenImage() :
    if pikchers.currentRow() >= 0 :
        filename = pikchers.currentItem().text()
        workimage.loadImage(workdir, filename)
        print(workimage.dir, workimage.filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)


app = QApplication([])

main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(700,500)

btn_papc = QPushButton('Папка')
pikchers = QListWidget()
pikcher = QLabel('Картинка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_contrast = QPushButton('Резкость')
btn_dw = QPushButton('Ч/Б')
btn_zercalo = QPushButton('Зеркало')

main_outline = QHBoxLayout()
cub_leyout_left = QVBoxLayout()
cub_leyout_right = QVBoxLayout()
leyout = QHBoxLayout()

leyout.addWidget(btn_left)
leyout.addWidget(btn_right)
leyout.addWidget(btn_zercalo)
leyout.addWidget(btn_contrast)
leyout.addWidget(btn_dw)

cub_leyout_left.addWidget(btn_papc)
cub_leyout_left.addWidget(pikchers)

cub_leyout_right.addWidget(pikcher)
cub_leyout_right.addLayout(leyout)

main_outline.addLayout(cub_leyout_left)
main_outline.addLayout(cub_leyout_right)

main_win.setLayout(main_outline)


workdir = ''
def chooseWorkdir() :
    global workdir
    workdir = QFileDialog.getExistingDirectory()

#extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
def filter(files, extensions) :
    results = []
    for filename in files :
        for ext in extensions :
            if filename.endswith(ext) :
                results.append(filename)
    return results

def showFilenamesList() :
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    files = os.listdir(workdir)
    list_image = filter(files,extensions)
    pikchers.clear()
    for i in list_image :
        pikchers.addItem(i)

btn_papc.clicked.connect(showFilenamesList)
pikchers.currentRowChanged.connect(showChosenImage)
btn_dw.clicked.connect(workimage.do_dw)
btn_zercalo.clicked.connect(workimage.do_flip)
# btn_filter.clicked.connect(workimage.do_blur)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_contrast.clicked.connect(workimage.do_contrast)








main_win.show()
app.exec_()