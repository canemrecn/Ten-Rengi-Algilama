import cv2
import numpy as np
import sys
#Gerekli kütüpaneleri import et
if sys.platform == 'win32':
    deltax=0
    deltay=0
else:
    deltax=50
    deltay=105
# Platforma göre deltax ve deltay değerlerini ayarla
kamera = cv2.VideoCapture(0)
# Kamerayı başlat
kamera.set(3,640) #genişlik
kamera.set(4,480) #yükseklik
kamera.set(10, 0.8) #parlaklık
# Kamera ayarlarını yap
while True:
    _, kare = kamera.read()
# Kameradan bir kare oku
    ycrcb = cv2.cvtColor(kare , cv2.COLOR_BGR2YCrCb)
# Kareyi YCrCb renk uzayına dönüştür
    ycrcb = cv2.inRange(ycrcb, (0, 137, 85), (255, 180, 135))
# YCrCb renk uzayında belirli bir aralıktaki renkleri maskeleyerek elde edilen maskeyi al
    ycrcb = cv2.morphologyEx(ycrcb, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
# Morfolojik açma işlemi ile gürültüyü azalt
    ycrcb = cv2.dilate(ycrcb,(11,11), iterations=1)
# Maskeyi genişlet
    ycrcb = cv2.erode(ycrcb, (11,11), iterations=1)
# Maskeyi erozyon işlemine tabi tut
    ycrcb = cv2.medianBlur(ycrcb, 5)
# Maskeyi median bulanıklaştırma ile yumuşat
    sonuc = cv2.bitwise_and(kare,kare,mask=ycrcb)
# Maskeyi orijinal kare üzerine uygula
    cv2.imshow('kare',kare)
    cv2.imshow('maske',ycrcb)
    cv2.imshow('sonuc',sonuc)
    cv2.moveWindow('kare',10,10)
    cv2.moveWindow('maske',10,kare.shape[0]+deltay)
    cv2.moveWindow('sonuc', kare.shape[1]+deltax,kare.shape[0] + deltay)
# Pencereleri göster ve konumlandır
    k = cv2.waitKey(10)
    if k == 27 or k == ord('q'):
        break
# Klavyeden ESC veya q tuşuna basıldığında döngüyü sonlandır
kamera.release()
cv2.destroyAllWindows()
# Kamerayı serbest bırak ve pencereleri kapat
