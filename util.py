
import cv2
import numpy


mousePos = (0, 0)
zoomIn = 0
zoomOut = 0
def onMouse(event, x, y, flags, params):
    global mousePos
    global zoomIn
    global zoomOut
    if event == cv2.EVENT_LBUTTONDBLCLK:
        zoomIn = 1
        mousePos = (x, y)
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        zoomOut = 1
        mousePos = (x, y)
    else: 
        zoomOut=0
        zoomIn = 0


def showImg(img, winName, destroy=1):
    global mousePos
    global zoomIn
    global zoomOut
    zoomWin = 1
    zoom = 1
    h, w = img.shape[:2]
    y1,y2,x1,x2=0,0,0,0
    imgPrev = numpy.copy(img)
    imgZoom = numpy.copy(img)
    cv2.namedWindow(winName)
    cv2.imshow(winName, imgPrev)
    cv2.setMouseCallback(winName, onMouse)
    op = 71
    needUpdate = 1
    countUpdate=0
    while op==71 or op==103 or op==45 or op==43 or op==9 or op==-1:
    #while op != 27:
        if needUpdate or countUpdate==30:
            cv2.imshow(winName, imgPrev)
            needUpdate=0
            countUpdate=0
        else:
            countUpdate+=1

        op=cv2.waitKey(50)
        if op == 71 or op == 103:
            cv2.imwrite(winName+".jpg", imgPrev)

        elif op == 43:
            if zoomWin < 1.4:
                zoomWin += 0.2
                h, w = int(img.shape[0]*zoomWin),int(img.shape[1]*zoomWin)
                imgZoom = cv2.resize(img, (int(img.shape[1] * zoom), int(img.shape[0] * zoom)))
                mousePos2 = int((w/2)+x1), int((h/2)+y1)
                y2 = int(mousePos2[1] + h / 2)
                y1 = int(mousePos2[1] - h / 2)
                x2 = int(mousePos2[0] + w / 2)
                x1 = int(mousePos2[0] - w / 2)
                imgPrev = imgZoom[y1:y2, x1:x2]
                needUpdate = 1
                #print "WinZoomIn " + str(zoomWin)
        elif op == 45:
            if zoomWin > 0.6:
                zoomWin -= 0.2
                h, w = int(img.shape[0]*zoomWin),int(img.shape[1]*zoomWin)
                imgZoom = cv2.resize(img, (int(img.shape[1] * zoom), int(img.shape[0] * zoom)))
                mousePos2 = int((w/2)+x1), int((h/2)+y1)
                y2 = int(mousePos2[1] + h / 2)
                y1 = int(mousePos2[1] - h / 2)
                x2 = int(mousePos2[0] + w / 2)
                x1 = int(mousePos2[0] - w / 2)
                imgPrev = imgZoom[y1:y2, x1:x2]
                needUpdate = 1
        if zoomIn == 1:
            if zoom < 9:
                zoom *= 1.5
                imgZoom = cv2.resize(img, (int(imgZoom.shape[1] * 1.5), int(imgZoom.shape[0] * 1.5)))
                mousePos2 = int((mousePos[0]+x1)*1.5), int((mousePos[1]+y1)*1.5)
                y2 = int(mousePos2[1] + h / 2)
                y1 = int(mousePos2[1] - h / 2)
                x2 = int(mousePos2[0] + w / 2)
                x1 = int(mousePos2[0] - w / 2)
                if y1 < 0:
                    y1, y2 = 0, h
                elif y2 > imgZoom.shape[0]:
                    y1, y2 = (imgZoom.shape[0] - h), imgZoom.shape[0]
                if x1 < 0:
                    x1, x2 = 0, w
                elif x2 > imgZoom.shape[1]:
                    x1, x2 = imgZoom.shape[1] - w, imgZoom.shape[1]
                imgPrev = imgZoom[y1:y2, x1:x2]
                needUpdate = 1
            #print "ZoomIn " + str(zoom)
            zoomIn = 0
        elif zoomOut == 1:
            if zoom >= 1.5:
                zoom /= 1.5
                imgZoom = cv2.resize(img, (int(imgZoom.shape[1] / 1.5), int(imgZoom.shape[0] / 1.5)))
                mousePos2 = int((mousePos[0]+x1)/1.5), int((mousePos[1]+y1)/1.5)
                y2 = int(mousePos2[1] + h / 2)
                y1 = int(mousePos2[1] - h / 2)
                x2 = int(mousePos2[0] + w / 2)
                x1 = int(mousePos2[0] - w / 2)
                if y1 < 0:
                    y1, y2 = 0, h
                elif y2 > imgZoom.shape[0]:
                    y1, y2 = (imgZoom.shape[0] - h), imgZoom.shape[0]
                if x1 < 0:
                    x1, x2 = 0, w
                elif x2 > imgZoom.shape[1]:
                    x1, x2 = imgZoom.shape[1] - w, imgZoom.shape[1]
                imgPrev = imgZoom[y1:y2, x1:x2]
                needUpdate = 1
            #print "ZoomOut " + str(zoom)
            zoomOut = 0
    if destroy:
        cv2.destroyWindow(winName)
    #TODO:
    #         flaoting window com notificacoes temporarias e permanentes de utilizacao da janela

def resize(img, w=1000, h=0):
    if h == 0:
        h = (float(img.shape[0])/float(img.shape[1])) * w
        return cv2.resize(img, dsize=(int(w),int(h)))
    elif w == 0:
        return cv2.resize(img, dsize=(int(w),int(h)))
    else:
        return img