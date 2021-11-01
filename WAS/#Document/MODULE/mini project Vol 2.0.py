from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
import math
import cv2
import numpy
import tkinter
from tkinter import filedialog
import os
from datetime import datetime
import xlwt
import xlrd
import xlsxwriter
import numpy as np
import time
# import Admin_main
# import Admin_Input
import tempfile
import os
# import pymysql
import random

## 메뉴 ##
def malloc(h, w, value=0) :
    retMemory = [ [ value for _ in range(w)]  for _ in range(h) ]
    return retMemory

def mallocNumpy(t, h, w) :
    retMemory = np.zeros((t,h,w), dtype=np.int16)
    return retMemory

def allocateOutMemory():
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage

    outImage = mallocNumpy(RGB,outH,outW)

def openFile() :
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    global boolImageDown

    ## 파일 선택하기
    filename = askopenfilename(parent=window,
           filetypes=(('Color 파일', '*.jpg;*.png;*.bmp;*.tif'), ('All File', '*.*')))

    ## (중요!) 입력이미지의 높이와 폭 알아내기

    cvInImage = cv2.imread(filename)
    inH = cvInImage.shape[0]
    inW = cvInImage.shape[1]

    ## 입력이미지용 메모리 할당

    # inImage = []
    # for _ in range(RGB) :
    #     inImage.append(malloc(inH, inW))
    inImage = mallocNumpy(RGB, inH, inW)
    ## 파일 --> 메모리 로딩

    for i in range(inH):
        for k in range(inW):
            inImage[R][i][k] = cvInImage.item(i, k ,B)
            inImage[G][i][k] = cvInImage.item(i, k, G)
            inImage[B][i][k] = cvInImage.item(i, k, R)

    boolImageDown = False
    equalColor()

def saveImage() :

    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == None or filename == '' :
        return

    saveCvPhoto = np.zeros((outH, outW, 3), np.uint8)

    for i in range(outH) :
        for k in range(outW) :
            tup = tuple(([outImage[B][i][k],outImage[G][i][k],outImage[R][i][k]]))
            saveCvPhoto[i,k] = tup

    saveFp = asksaveasfile(parent=window, mode='wb',defaultextension='.', filetypes=(("그림 파일", "*.png;*.jpg;*.bmp;*.tif"), ("모든 파일", "*.*")))

    if saveFp == '' or saveFp == None:

        return

    cv2.imwrite(saveFp.name, saveCvPhoto)
    if boolImageDown == True:
        saveWork("파일저장")

def displayImageColor() :

    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, windowImage


    if canvas != None :
        canvas.destroy()

    VX, VY = 512,512 #최대화면 크기
    # 크기가 512보다 크면, 최대 512로 보이기
    if outH <= VY or outW <= VX :
        VX = outW
        VY = outH
        step = 1
    else:
        if outH > outW :
            step = outH / VY  # 1021/512 = 2
            VX = int(VY*outW/outH)
        else:
            step = outW / VX # 1021/512 = 2
            VY = int(VX*outH/outW)

    window.geometry(str(int(VX*1.2)) + 'x' + str(int(VY*1.2)) )
    # 기존 이미지 삭제
    if canvas != None:
        canvas.destroy()

    canvas = Canvas(window, height=VY, width=VX)
    paper = PhotoImage(height=VY, width=VX)
    canvas.create_image((VX // 2, VY // 2), image=paper, state='normal')

    # 메모리에서 처리한 후, 한방에 화면에 보이기 --> 완전 빠름

    rgbString =""

    for i in numpy.arange(0,outH,step) :
        tmpString = "" # 각 줄
        for k in numpy.arange(0,outW,step) :
            i=int(i); k=int(k)
            r = outImage[R][i][k]
            g = outImage[G][i][k]
            b = outImage[B][i][k]
            tmpString += "#%02x%02x%02x " % (r, g, b)
        rgbString += '{' + tmpString + '} '

    paper.put(rgbString)
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지정보:' + str(outH) + 'x' + str(outW)+'      '+filename)


###### 영상 처리 함수 ##########
## 화소점 처리 ##
def equalColor() :

    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return

    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존

    outH = inH;    outW = inW

    ## 출력이미지 메모리 할당

    # outImage = []

    # for _ in range(RGB) :
    #     outImage.append(malloc(outH, outW))
    #
    #outImage = allocateOutMemory()

    ### 진짜 영상처리 알고리즘 ###
    # for rgb in range(RGB):
    #     for i in range(inH):
    #         for k in range(inW):
    #             outImage[rgb][i][k] = inImage[rgb][i][k]
    outImage = inImage.copy()
    ########################

    displayImageColor()
    if boolImageDown == True:
        saveWork("복구되었습니다")

def reverseColor() :

    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    start = time.time()
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존

    outH = inH;    outW = inW

    ## 출력이미지 메모리 할당
    outImage = mallocNumpy(RGB, outH, outW)
    # outImage = []
    # for _ in range(RGB) :
    #     outImage.append(malloc(outH, outW))

    ### 진짜 영상처리 알고리즘 ###
    #
    # value = askinteger("밝게하기", "값")
    # if value == None :
    #
    #     return

    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                outImage[rgb][i][k] = 255 - inImage[rgb][i][k]


    ########################

    displayImageColor()
    saveWork('영상반전')

    end = time.time
    second = end - start
    status.configure(text="{0:.2f}".format(second) + "초  " + status.cget("text") )

def reverseColor_NP():
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    start = time.time()
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존

    outH = inH;    outW = inW

    ## 출력이미지 메모리 할당
    outImage = mallocNumpy(RGB, outH, outW)
    # outImage = []
    # for _ in range(RGB) :
    #     outImage.append(malloc(outH, outW))

    ### 진짜 영상처리 알고리즘 ###

    # value = askinteger("밝게하기", "값")
    # if value == None :
    #
    #     return

    outImage = 255 - inImage

    ########################

    displayImageColor()
    saveWork('영상반전_NP')

    end = time.time
    second = end - start
    status.configure(text="{0:.2f}".format(second) + "초  " + status.cget("text") )

def grayColor() :

    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:

        return

    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존

    outH = inH;    outW = inW

    ## 출력이미지 메모리 할당

    outImage = []

    for _ in range(RGB) :
        outImage.append(malloc(outH, outW))

    ### 진짜 영상처리 알고리즘 ###

    for i in range(inH):
        for k in range(inW):
            c = inImage[R][i][k] + inImage[G][i][k] + inImage[B][i][k]
            c = int(c/3)
            outImage[R][i][k] = outImage[G][i][k] = outImage[B][i][k] = c

    ########################

    displayImageColor()
    saveWork('그레이 스케일')

def grayColor_NP() :

    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:

        return

    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존

    outH = inH;    outW = inW

    ## 출력이미지 메모리 할당
    outImage = mallocNumpy(RGB, outH, outW)


    ### 진짜 영상처리 알고리즘 ###

    inImage[0] = (inImage[0] + inImage[1] + inImage[2]) // 3
    outImage = np.array([inImage[0],inImage[0],inImage[0]])

    ########################

    displayImageColor()
    saveWork('그레이 스케일_NP')

def addColor() :
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB) :
        outImage.append(malloc(outH, outW))
    ### 진짜 영상처리 알고리즘 ###
    value = askinteger("밝게하기", "값")
    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                out = inImage[rgb][i][k] + value
                if out > 255 :
                    outImage[rgb][i][k] = 255
                else :
                    outImage[rgb][i][k] = out
    ########################

    displayImageColor()
    saveWork('밝게하기')

def addColor_NP() :
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = mallocNumpy(RGB, outH, outW)
    # outImage = []
    # for _ in range(RGB) :
    #     outImage.append(malloc(outH, outW))
    ### 진짜 영상처리 알고리즘 ###
    value = askinteger("밝게하기", "값")
    if value == None :
        return
    inImage = inImage.astype(np.int16)
    outImage = inImage + value

    # 조건으로 범위 지정
    outImage = np.where(outImage > 255, 255, outImage)
    outImage = np.where(outImage < 0, 0, outImage)
    ########################

    displayImageColor()
    saveWork('밝게하기_NP')

def bw1Color():  #이진화
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))

    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                c = inImage[R][i][k] + inImage[G][i][k] + inImage[B][i][k]
                c = int(c / 3)
                if c > 127:
                    outImage[rgb][i][k] = 255
                else:
                    outImage[rgb][i][k] = 0
    displayImageColor()
    saveWork('이진화')

def bw1Color_NP():  #이진화_NP
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    ## 출력이미지 메모리 할당
    outImage = mallocNumpy(RGB, outH, outW)

    outImage[0] = (inImage[0] + inImage[1] + inImage[2]) // 3
    outImage = np.array([outImage[0], outImage[0], outImage[0]])

    outImage[outImage > 127] = 255
    outImage[outImage <= 127] = 0

    displayImageColor()
    saveWork('이진화_NP')

def bw2Color(): #이진화 (평균값)
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
    sum = 0
    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                c = inImage[R][i][k] + inImage[G][i][k] + inImage[B][i][k]
                sum += c
    avr = sum/(RGB*inW*inW)
    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                c = inImage[R][i][k] + inImage[G][i][k] + inImage[B][i][k]
                if c > avr:
                    outImage[rgb][i][k] = 255
                else:
                    outImage[rgb][i][k] = 0

    displayImageColor()
    saveWork('이진화 평균값')

def bw2Color_NP(): #이진화 (평균값)
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = mallocNumpy(RGB, outH, outW)

    outImage[0] = (inImage[0] + inImage[1] + inImage[2]) // 3
    outImage = np.array([outImage[0], outImage[0], outImage[0]])

    outImage[outImage > inImage.mean()] = 255
    outImage[outImage <= inImage.mean()] = 0

    displayImageColor()
    saveWork('이진화 평균값_NP')

def bw3Color(): #이진화 (중위값)
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))

    temp =[]
    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                temp.append(inImage[rgb][i][k])
    temp.sort()
    mid = temp[int((RGB*inH*inW)/2)]
    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                c = inImage[R][i][k] + inImage[G][i][k] + inImage[B][i][k]
                if c >= mid:
                    outImage[rgb][i][k]= 255
                else:
                    outImage[rgb][i][k] = 0

    displayImageColor()
    saveWork('이진화 중위수')

def addpColor(): #포스터라이징
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))

    value = askinteger("경계값","값을 입력하시오", minvalue=1, maxvalue=255)
    temp = int(256 / value)
    for rgb in range(RGB):
        for i in range(outH):
            for k in range(outW):
                for j in range(temp, 257, temp):
                    c = inImage[R][i][k] + inImage[G][i][k] + inImage[B][i][k]
                    c = int(c / 3)
                    if c < j:
                        outImage[rgb][i][k] = j
                        break

    displayImageColor()
    saveWork('포스터 라이징')

def gammaColor(): #감마
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))

    value = askinteger("감마값", "값을 입력하시오", minvalue=1, maxvalue=255)
    # temp = 256 / value
    for rgb in range(RGB):
        for i in range(outH):
            for j in range(outW):
                outImage[rgb][i][j] = int(math.pow(inImage[rgb][i][j] / 255.0, 1.0 / value) * 255.0)
    displayImageColor()
    saveWork('감마')

def gammaColor_NP(): #감마_NP
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = mallocNumpy(RGB, outH, outW)


    value = askfloat("감마", "값")
    if value == None:
        return
    inImage = inImage.astype(np.int16)

    outImage = inImage ** (1/value)
    outImage = outImage.astype(np.int16)
    outImage = np.where(outImage > 255, 255, outImage)
    outImage = np.where(outImage < 0, 0, outImage)


    displayImageColor()
    saveWork('감마_NP')

def paraCupColor() : # 파라볼라 컵 알고리즘
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))

    ### 진짜 영상처리 알고리즘 ###
    # Out = 255.0 * ( (In / 128.0 - 1.0) ** 2 )
    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                v =  255.0 * ( (inImage[rgb][i][k] /128.0 - 1.0) ** 2)
                if v > 255 :
                    outImage[rgb][i][k] = 255
                elif v < 0 :
                    outImage[rgb][i][k] = 0
                else :
                    outImage[rgb][i][k] = int(v)

    displayImageColor()
    saveWork('파라볼라 컵')

def paraCapColor() : # 파라볼라 캡 알고리즘
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))

    ### 진짜 영상처리 알고리즘 ###
    # Out = 255.0 * ( (In / 128.0 - 1.0) ** 2 )
    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                v = 255 - 255.0 * ( (inImage[rgb][i][k] /128.0 - 1.0) ** 2)
                if v > 255 :
                    outImage[rgb][i][k] = 255
                elif v < 0 :
                    outImage[rgb][i][k] = 0
                else :
                    outImage[rgb][i][k] = int(v)

    displayImageColor()
    saveWork('파라볼라 캡')

def point2Color() : #범위 강조 변환
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))

    ### 진짜 영상처리 알고리즘 ###
    p1 = askinteger("","값:")
    p2 = askinteger("", "값:")
    if p1 > p2 :
        p1, p2 = p2, p1
    #     tmp = p1
    #     p1 = p2
    #     p2 = tmp
    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                #if p1 < inImage[i][k] and inImage[i][k] < p2 :
                if p1 < inImage[rgb][i][k] < p2 :
                    outImage[rgb][i][k] = 255
                else :
                    outImage[rgb][i][k] = inImage[rgb][i][k]

    displayImageColor()
    saveWork('범위 강조 변환')

## 화소영역 처리 ##
def embossColor() : # 엠보싱 효과
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
    ### 진짜 영상처리 알고리즘 ###
    # (중요!) 마스크
    mSize = 3
    mask = [ [-1, 0, 0],
             [ 0, 0, 0],
             [ 0, 0, 1] ]
    tmpInImage, tmpOutImage = [],[]
    for _ in range(RGB):
        tmpInImage.append(malloc(inH+2, inW+2, 127))
        tmpOutImage.append(malloc(outH, outW))
    # inImage --> 임시input
    for rgb in range(RGB):
        for i in range(inH) :
            for k in range(inW) :
                tmpInImage[rgb][i+1][k+1] = float(inImage[rgb][i][k])
    # 회선 연산 : 마스크로 긁어가면서 처리하기
    for rgb in range(RGB):
        for i in range(1, inH+1) :
            for k in range(1, inW+1) :
                # 각 점을 처리
                S = 0.0
                for m in range(mSize) :
                    for n in range(mSize) :
                        S += mask[m][n] * tmpInImage[rgb][m+i-1][n+k-1]
                tmpOutImage[rgb][i-1][k-1] = S
    ## 마무리.. 마스크에 따라서 127 더할지 결정
    for rgb in range(RGB):
        for i in range(outH) :
            for k in range(outW) :
                tmpOutImage[rgb][i][k] += 127.0
    ## 임시Output --> outImage .... 오버플로 체크
    for rgb in range(RGB):
        for i in range(outH):
            for k in range(outW):
                if tmpOutImage[rgb][i][k] > 255 :
                    outImage[rgb][i][k] = 255
                elif tmpOutImage[rgb][i][k] < 0:
                    outImage[rgb][i][k] = 0
                else :
                    outImage[rgb][i][k] = int(tmpOutImage[rgb][i][k])
    ########################
    displayImageColor()
    saveWork('엠보싱')

def blurr5Color() : # 블러링 효과
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;
    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
    ### 진짜 영상처리 알고리즘 ###
    # (중요!) 마스크
    mSize = 5
    mask = [ [ 1/25.0, 1/25.0, 1/25.0, 1/25.0, 1/25.0],
             [ 1/25.0, 1/25.0, 1/25.0, 1/25.0, 1/25.0],
             [ 1/25.0, 1/25.0, 1/25.0, 1/25.0, 1/25.0],
             [ 1/25.0, 1/25.0, 1/25.0, 1/25.0, 1/25.0],
             [ 1/25.0, 1/25.0, 1/25.0, 1/25.0, 1/25.0] ]
    tmpInImage, tmpOutImage = [],[]
    for _ in range(RGB):
        tmpInImage.append(malloc(inH+4, inW+4, 127))
        tmpOutImage.append(malloc(outH, outW))
    # inImage --> 임시input
    for rgb in range(RGB):
        for i in range(inH) :
            for k in range(inW) :
                tmpInImage[rgb][i+2][k+2] = float(inImage[rgb][i][k])
    # 회선 연산 : 마스크로 긁어가면서 처리하기
    for rgb in range(RGB):
        for i in range(2, inH+2) :
            for k in range(2, inW+2) :
                # 각 점을 처리
                S = 0.0
                for m in range(mSize) :
                    for n in range(mSize) :
                        S += mask[m][n] * tmpInImage[rgb][m+i-2][n+k-2]
                tmpOutImage[rgb][i-2][k-2] = S
    ## 마무리.. 마스크에 따라서 127 더할지 결정
    # for i in range(outH) :
    #     for k in range(outW) :
    #         tmpOutImage[i][k] += 127.0
    ## 임시Output --> outImage .... 오버플로 체크
    for rgb in range(RGB):
        for i in range(outH):
            for k in range(outW):
                if tmpOutImage[rgb][i][k] > 255 :
                    outImage[rgb][i][k] = 255
                elif tmpOutImage[rgb][i][k] < 0:
                    outImage[rgb][i][k] = 0
                else :
                    outImage[rgb][i][k] = int(tmpOutImage[rgb][i][k])
    ########################
    displayImageColor()
    saveWork('블러링')

def sharpColor(): #샤프닝
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))

    mSize = 3
    mask = [[-1.0, -1.0, -1.0],
            [-1.0, 9.0, -1.0],
            [-1.0, -1.0, -1.0]]
    tmpInImage, tmpOutImage = [],[]
    for _ in range(RGB):
        tmpInImage.append(malloc(inH+4, inW+4, 127))
        tmpOutImage.append(malloc(outH, outW))

    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                tmpInImage[rgb][i+1][k+1] = float(inImage[rgb][i][k])
    for rgb in range(RGB):
        for i in range(1, inH+1):
            for k in range(1, inW+1):
                S =0.0
                for m in range(mSize):
                    for n in range(mSize):
                        S += mask[m][n]*tmpInImage[rgb][i-1+m][k-1+n]
                tmpOutImage[rgb][i-1][k-1] = S
    for rgb in range(RGB):
        for i in range(outH):
            for k in range(outW):
                if tmpOutImage[rgb][i][k] > 255:
                    outImage[rgb][i][k] = 255
                elif tmpOutImage[rgb][i][k] < 0:
                    outImage[rgb][i][k] = 0
                else: outImage[rgb][i][k] = int(tmpOutImage[rgb][i][k])

    displayImageColor()
    saveWork('샤프닝')

def laplacColor():  # 라플라시안
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))

    mSize = 3
    mask = [[0.0, -1.0, 0.0],
            [-1.0, 4.0, -1.0],
            [0.0, -1.0, 0.0]]
    tmpInImage, tmpOutImage = [],[]
    for _ in range(RGB):
        tmpInImage.append(malloc(inH+4, inW+4, 127))
        tmpOutImage.append(malloc(outH, outW))
    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                tmpInImage[rgb][i + 1][k + 1] = float(inImage[rgb][i][k])

    for rgb in range(RGB):
        for i in range(1, inH + 1):
            for k in range(1, inW + 1):
                S = 0.0
                for m in range(mSize):
                    for n in range(mSize):
                        S += mask[m][n] * tmpInImage[rgb][i - 1 + m][k - 1 + n]
                tmpOutImage[rgb][i - 1][k - 1] = S
    for rgb in range(RGB):
        for i in range(outH):
            for k in range(outW):
                if tmpOutImage[rgb][i][k] > 255:
                    outImage[rgb][i][k] = 255
                elif tmpOutImage[rgb][i][k] < 0:
                    outImage[rgb][i][k] = 0
                else:
                    outImage[rgb][i][k] = int(tmpOutImage[rgb][i][k])

    displayImageColor()
    saveWork('라플라시안')

## 기하학 처리 ##
def moveColor() : #영상 이동
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))

    ### 진짜 영상처리 알고리즘 ###
    dy = askinteger("", "x변위:")
    dx = askinteger("", "y변위:")
    for rgb in range(RGB):
        for i in range(inH):
            for k in range(inW):
                if 0<= i+dx < outH and 0<= k+dy < outW :
                    outImage[rgb][i+dx][k+dy] = int(inImage[rgb][i][k])

    displayImageColor()
    saveWork('영상 이동')

def zoomOutColor():  # 영상 축소 알고리즘
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    scale = askinteger("축소", "배율")  # 짝수
    outH = int(inH / scale);
    outW = int(inW / scale)
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))

    ### 진짜 영상처리 알고리즘 ###
    for rgb in range(RGB):
        for i in range(outH):
            for k in range(outW):
                outImage[rgb][i][k] = inImage[rgb][i*scale][k*scale]

    displayImageColor()
    saveWork('영상 축소')

def zoomInColor():  # 영상 확대
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    scale = askinteger("확대", "배율")  # 짝수
    outH = int(inH*scale);
    outW = int(inW*scale)
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))

    ### 진짜 영상처리 알고리즘 ###
    for rgb in range(RGB):
        for i in range(outH):
            for k in range(outW):
                outImage[rgb][i][k] = inImage[rgb][int(i/scale)][int(k/scale)]

    displayImageColor()
    saveWork('영상 확대')

def rotateColorImage() : # 회전 - 중심, 백워딩
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return
    ## (중요!) 출력이미지의 높이, 폭을 결정 ---> 알고리즘에 의존
    outH = inH;    outW = inW
    ## 출력이미지 메모리 할당
    outImage = []
    for _ in range(RGB):
        outImage.append(malloc(outH, outW))
    ### 진짜 영상처리 알고리즘 ###
    # xd = cos * xs - sin * ys
    # yd = sin * xs + cos * ys
    angle = askinteger("회전", "각도", minvalue=0, maxvalue=360)
    r = angle * math.pi / 180
    cx = inH // 2
    cy = inW // 2
    for rgb in range(RGB):
        for i in range(outH):
            for k in range(outW):
                xs = i ; ys = k
                xd = int(math.cos(r) * (xs -cx) - math.sin(r) * (ys-cy) + cx)
                yd = int(math.sin(r) * (xs -cx) + math.cos(r) * (ys-cy) + cy)
                if 0<= xd < outH and 0<= yd < outW :
                    outImage[rgb][xs][ys] = inImage[rgb][xd][yd]

    ########################
    displayImageColor()
    saveWork('영상 회전')

## MySQL 관련 함수 ##
def saveMySQL():
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    global userID

    if filename == None or filename == '':
        return
    saveCvPhoto = np.zeros((outH, outW, 3), np.uint8)
    for i in range(outH):
        for k in range(outW):
            tup = tuple(([outImage[B][i][k], outImage[G][i][k], outImage[R][i][k]]))
            saveCvPhoto[i, k] = tup
    saveFname = tempfile.gettempdir() + '/' + os.path.basename(filename)
    cv2.imwrite(saveFname, saveCvPhoto)
    ##############
    '''
    DROP DATABASE IF exists photo_db;
    CREATE DATABASE photo_db;
    USE photo_db;
    CREATE TABLE photo_table (
      p_id INT PRIMARY KEY,
      p_fname VARCHAR(255),
      p_ext   CHAR(5),
      p_size  BIGINT,
      p_height INT,
      p_width  INT,
      p_photo LONGBLOB,
      p_upDate DATE,
      p_upUser CHAR(10) -- Foreign Key
    )
    '''
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()  # 빈 트럭 준비
    p_id = random.randint(-2100000000, 2100000000)
    tmpName = os.path.basename(os.path.basename(saveFname))
    p_fname, p_ext = tmpName.split('.')
    p_size = os.path.getsize(saveFname)
    tmpImage = cv2.imread(saveFname)
    p_height = tmpImage.shape[0]
    p_width = tmpImage.shape[1]
    p_upDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 구글링
    p_upUser = userID  # 로그인한 사용자
    # 파일을 읽기
    fp = open(saveFname, 'rb')
    blobData = fp.read()
    fp.close()
    # 파일 정보 입력
    sql = "INSERT INTO photo_table(p_id, p_fname, p_ext, p_size, p_height, p_width, "
    sql += "p_upDate, p_UpUser, p_photo) VALUES (" + str(p_id) + ", '" + p_fname + "', '" + p_ext
    sql += "', " + str(p_size) + "," + str(p_height) + "," + str(p_width) + ", '" + p_upDate
    sql += "', '" + p_upUser + "', %s )"
    tupleData = (blobData,)
    cur.execute(sql, tupleData)
    conn.commit()
    cur.close()
    conn.close()
    messagebox.showinfo('성공', filename + ' 잘 입력됨.')
    #############

def openMySQL():  # 파일 열기 개념....
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList
    global userID
    global work_photoid, work_what, work_fname, work_ext, boolImageDown

    ###################
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()  # 빈 트럭 준비
    sql = "SELECT p_id, p_fname, p_ext, p_size FROM photo_table"
    cur.execute(sql)
    fileList = cur.fetchall()
    cur.close()
    conn.close()

    ##################
    # 서브 윈도창 나오기.
    def downLoad():
        global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
        global cvInImage, cvOutImage, fileList
        global work_photoid, work_what, work_fname, work_ext, boolImageDown

        selectIndex = listData.curselection()[0]
        conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cur = conn.cursor()  # 빈 트럭 준비
        sql = "SELECT  p_fname, p_ext, p_photo FROM photo_table WHERE p_id= "
        sql += str(fileList[selectIndex][0])
        cur.execute(sql)
        p_fname, p_ext, p_photo = cur.fetchone()
        fullPath = tempfile.gettempdir() + '/' + p_fname + '.' + p_ext
        fp = open(fullPath, 'wb')
        fp.write(p_photo)
        print(fullPath)
        fp.close()
        cur.close()
        conn.close()
        filename = fullPath

        subWindow.destroy()
        ####
        cvInImage = cv2.imread(filename)
        inH = cvInImage.shape[0]
        inW = cvInImage.shape[1]
        ## 입력이미지용 메모리 할당
        inImage = []
        for _ in range(RGB):
            inImage.append(malloc(inH, inW))
        ## 파일 --> 메모리 로딩
        for i in range(inH):
            for k in range(inW):
                inImage[R][i][k] = cvInImage.item(i, k, B)
                inImage[G][i][k] = cvInImage.item(i, k, G)
                inImage[B][i][k] = cvInImage.item(i, k, R)
        equalColor()

        ### 작업기록 저장
        work_photoid = fileList[selectIndex][0]
        work_fname = p_fname
        work_ext = p_ext
        saveWork("SQL 다운로드")
        boolImageDown = True
        messagebox.showinfo('성공', userID + '님의 ' + work_fname + ' 작업기록이 MySQL에 저장됩니다.')
        ####

    subWindow = Toplevel(windowImage)
    subWindow.geometry('300x400')
    ## 스크롤바 나타내기
    frame = Frame(subWindow)
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side='right', fill='y')
    listData = Listbox(frame, yscrollcommand=scrollbar.set);
    listData.pack()
    scrollbar['command'] = listData.yview
    frame.pack()
    for fileTup in fileList:
        listData.insert(END, fileTup[1:])
    btnDownLoad = Button(subWindow, text='!!다운로드!!', command=downLoad)
    btnDownLoad.pack(padx=10, pady=10)

def upAllMySQL():
    global userID
    dir_path = askdirectory(parent=None, initialdir="/", title='Please select a directory')

    print("dir_path : ", dir_path)

    file_list = os.listdir(dir_path)

    print("file_list: {}".format(file_list))

    for item in file_list:
        if item == None or item == '':
            break

        path = dir_path + '/' + item
        # 입력이미지의 높이와 폭 알아내기
        cvInImage = cv2.imread(path)
        inH = cvInImage.shape[0]
        inW = cvInImage.shape[1]

        # 입력이미지용 메모리 할당
        bufImage = []
        for _ in range(RGB):
            bufImage.append(malloc(inH, inW))

        # 파일 -> 메모리 로딩
        for i in range(inH):
            for j in range(inW):
                bufImage[R][i][j] = cvInImage.item(i, j, B)
                bufImage[G][i][j] = cvInImage.item(i, j, G)
                bufImage[B][i][j] = cvInImage.item(i, j, R)

        saveCvPhoto = np.zeros((inH, inW, 3), np.uint8)
        for i in range(inH):
            for k in range(inW):
                tup = tuple(([bufImage[B][i][k], bufImage[G][i][k], bufImage[R][i][k]]))
                saveCvPhoto[i, k] = tup
        saveFname = tempfile.gettempdir() + '/' + os.path.basename(item)
        cv2.imwrite(saveFname, saveCvPhoto)

        conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cur = conn.cursor()  # 빈 트럭 준비
        p_id = random.randint(-2100000000, 2100000000)
        tmpName = os.path.basename(os.path.basename(saveFname))
        p_fname, p_ext = tmpName.split('.')
        p_size = os.path.getsize(saveFname)
        tmpImage = cv2.imread(saveFname)
        p_height = tmpImage.shape[0]
        p_width = tmpImage.shape[1]
        p_upDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 구글링
        p_upUser = userID  # 로그인한 사용자
        # 파일을 읽기
        fp = open(saveFname, 'rb')
        blobData = fp.read()
        fp.close()
        # 파일 정보 입력
        sql = "INSERT INTO photo_table(p_id, p_fname, p_ext, p_size, p_height, p_width, "
        sql += "p_upDate, p_UpUser, p_photo) VALUES (" + str(p_id) + ", '" + p_fname + "', '" + p_ext
        sql += "', " + str(p_size) + "," + str(p_height) + "," + str(p_width) + ", '" + p_upDate
        sql += "', '" + p_upUser + "', %s )"
        tupleData = (blobData,)
        cur.execute(sql, tupleData)
        conn.commit()
        cur.close()
        conn.close()
        print(item)
        #############

def showWorkList():
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList
    global userID
    global work_photoid, work_what, work_fname, work_ext, boolImageDown

    ###################
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()  # 빈 트럭 준비
    sql = "SELECT work_id, work_userid, work_date, work_fname, work_ext, work_what FROM work_table "
    sql += "WHERE work_userid='" + userID + "'"
    print(sql)
    cur.execute(sql)
    fileList = cur.fetchall()
    cur.close()
    conn.close()

    ##################
    # 서브 윈도창 나오기.
    def downLoad():
        global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
        global cvInImage, cvOutImage, fileList
        global work_photoid, work_what, work_fname, work_ext, boolImageDown

        selectIndex = listData.curselection()[0]
        conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cur = conn.cursor()  # 빈 트럭 준비
        sql = "SELECT  work_photoid, work_fname, work_ext, work_photo FROM work_table WHERE work_id= "
        sql += str(fileList[selectIndex][0])
        cur.execute(sql)
        work_photoid, work_fname, work_ext, work_photo = cur.fetchone()
        fullPath = tempfile.gettempdir() + '/' + work_fname + '.' + work_ext
        fp = open(fullPath, 'wb')
        fp.write(work_photo)
        print(fullPath)
        fp.close()
        cur.close()
        conn.close()
        filename = fullPath

        subWindow.destroy()
        ####
        cvInImage = cv2.imread(filename)
        inH = cvInImage.shape[0]
        inW = cvInImage.shape[1]
        ## 입력이미지용 메모리 할당
        inImage = []
        for _ in range(RGB):
            inImage.append(malloc(inH, inW))
        ## 파일 --> 메모리 로딩
        for i in range(inH):
            for k in range(inW):
                inImage[R][i][k] = cvInImage.item(i, k, B)
                inImage[G][i][k] = cvInImage.item(i, k, G)
                inImage[B][i][k] = cvInImage.item(i, k, R)
        equalColor()

        ### 작업기록 저장
        saveWork("SQL 다운로드")
        boolImageDown = True
        messagebox.showinfo('성공', userID + '님의 ' + work_fname + ' 작업기록이 MySQL에 저장됩니다.')
        ####

    subWindow = Toplevel(windowImage)
    subWindow.geometry('400x400')
    ## 스크롤바 나타내기
    frame = Frame(subWindow)
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side='right', fill='y')
    listData = Listbox(frame, yscrollcommand=scrollbar.set, width=200);
    listData.pack()
    scrollbar['command'] = listData.yview
    frame.pack()
    for fileTup in fileList:
        listData.insert(END, fileTup[2:])
    btnDownLoad = Button(subWindow, text='!!불러오기!!', command=downLoad)
    btnDownLoad.pack(padx=10, pady=10)


## 엑셀 ##

def openExcel():
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList
    filename = askopenfilename(parent=window,
           filetypes=(('엑셀 파일', '*.xls'), ('All File', '*.*')))

    workbook = xlrd.open_workbook(filename)
    wsList = workbook.sheets()
    inH = wsList[0].nrows
    inW = wsList[0].ncols
    ## 입력이미지용 메모리 할당

    inImage = []
    for _ in range(RGB) :
        inImage.append(malloc(inH, inW))

    ## 파일 --> 메모리 로딩
    for i in range(inH):
        for k in range(inW):
            inImage[R][i][k] = int(wsList[R].cell_value(i, k))
            inImage[G][i][k] = int(wsList[G].cell_value(i, k))
            inImage[B][i][k] = int(wsList[B].cell_value(i, k))

    equalColor()

def saveExcel():
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList
    saveFp = asksaveasfile(parent=window, mode='wb',defaultextension='xls', filetypes=(("엑셀 파일", "*.xls"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    xlsName = saveFp.name
    #sheetName = os.path.basename(filename)
    wb = xlwt.Workbook()
    ws_R = wb.add_sheet("RED")
    ws_G = wb.add_sheet("GREEN")
    ws_B = wb.add_sheet("BLUE")
    for i in range(outH):
        for k in range(outW):
            ws_R.write(i, k, int(outImage[R][i][k]))
            ws_G.write(i, k, int(outImage[G][i][k]))
            ws_B.write(i, k, int(outImage[B][i][k]))


    wb.save(xlsName)
    print('엑셀. 저장')


def drawExcel():

    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList
    saveFp = asksaveasfile(parent=window, mode='wb',defaultextension='xls', filetypes=(("엑셀 파일", "*.xls"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    xlsName = saveFp.name

    wb = xlsxwriter.Workbook(xlsName)
    ws_R = wb.add_worksheet("RED")
    ws_G = wb.add_worksheet("GREEN")
    ws_B = wb.add_worksheet("BLUE")
    ws = wb.add_worksheet("COLOR")

    #셀 크기 조절
    ws_R.set_column(0, outW-1, 1.0) #엑셀에서 0.34
    for i in range(outH):
        ws_R.set_row(i, 9.5) #엑셀에서 약 0.35
    ws_G.set_column(0, outW-1, 1.0) #엑셀에서 0.34
    for i in range(outH):
        ws_G.set_row(i, 9.5)
    ws_B.set_column(0, outW-1, 1.0) #엑셀에서 0.34
    for i in range(outH):
        ws_B.set_row(i, 9.5)
    ws.set_column(0, outW - 1, 1.0)  # 엑셀에서 0.34쯤
    for i in range(outH):
        ws.set_row(i, 9.5)  # 엑셀에서 0.35쯤

    #메모리 --> 엑셀파일
    for i in range(outH):
        for k in range(outW):
            ## red시트
            data = outImage[R][i][k]
            if data <= 15 :
                hexStr = '#' +('0'+ hex(data)[2:]) + '0000'
            else:
                hexStr = '#' + hex(data)[2:] + '0000'
            # 셀 속성 변경
            cell_format = wb.add_format()
            cell_format.set_bg_color(hexStr)
            ws_R.write(i,k,'',cell_format)

            #green 시트
            data = outImage[G][i][k]
            if data <= 15 :
                hexStr = '#00' + ('0' + hex(data)[2:]) + '00'
            else :
                hexStr = '#00' + hex(data)[2:] + '00'

            cell_format = wb.add_format()
            cell_format.set_bg_color(hexStr)
            ws_G.write(i, k, '', cell_format)


            # Blue 시트
            data = outImage[B][i][k]
            if data <= 15 :
                hexStr = '#0000' + ('0' + hex(data)[2:])
            else :
                hexStr = '#0000' + hex(data)[2:]

            cell_format = wb.add_format()
            cell_format.set_bg_color(hexStr)
            ws_B.write(i, k, '', cell_format)

            # COLOR 시트
            dataR = outImage[R][i][k]
            dataG = outImage[G][i][k]
            dataB = outImage[B][i][k]
            if dataR <= 15 :
                hexStr = '#' + ('0' + hex(dataR)[2:])
            else :
                hexStr = '#' + hex(dataR)[2:]

            if dataG <= 15 :
                hexStr += ('0' + hex(dataG)[2:])
            else :
                hexStr += hex(dataG)[2:]

            if dataB <= 15 :
                hexStr += ('0' + hex(dataB)[2:])
            else :
                hexStr += hex(dataB)[2:]

            cell_format = wb.add_format()
            cell_format.set_bg_color(hexStr)
            ws.write(i, k, '', cell_format)


    wb.close()
    print('엑셀아트. 저장')


## openCV용 함수 모음
def cvOut2outImage() : # OpenCV의 결과 --> OutImage 메모리에 넣기
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList
    ## 결과 메모리의 크기
    outH = cvOutImage.shape[0]
    outW = cvOutImage.shape[1]
    ## 입력이미지용 메모리 할당
    outImage = []
    for _ in range(RGB) :
        outImage.append(malloc(outH, outW))
    ## cvOut --> 메모리
    for i in range(outH):
        for k in range(outW):
            if (cvOutImage.ndim == 2) : # 그레이, 흑백
                outImage[R][i][k] = cvOutImage.item(i, k)
                outImage[G][i][k] = cvOutImage.item(i, k)
                outImage[B][i][k] = cvOutImage.item(i, k)
            else :
                outImage[R][i][k] = cvOutImage.item(i, k, B)
                outImage[G][i][k] = cvOutImage.item(i, k, G)
                outImage[B][i][k] = cvOutImage.item(i, k, R)

def grayscale_CV() :
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList
    if filename == None :
        return
    ##### OpenCV 용 영상처리 ###
    cvOutImage = cv2.cvtColor(cvInImage, cv2.COLOR_BGR2GRAY)
    ########################
    cvOut2outImage()
    displayImageColor()
    saveWork('그레이 스케일_CV')

def cartoon_CV() :
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList
    if filename == None :
        return
    ##### OpenCV 용 영상처리 ###
    cvOutImage = cv2.cvtColor(cvInImage, cv2.COLOR_RGB2GRAY)
    cvOutImage = cv2.medianBlur(cvOutImage, 7)

    edges = cv2.Laplacian(cvOutImage, cv2.CV_8U, ksize=5)
    ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
    cvOutImage = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    ########################
    cvOut2outImage()
    displayImageColor()
    saveWork('카툰_CV')

def emboss_CV() : # 엠보싱 효과
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return

    cvOutImage = cv2.imread(filename)

    mask = np.zeros((3,3), np.float32)
    mask[0][0] = -1.0; mask[2][2] = 1.0
    cvOutImage = cv2.filter2D(cvInImage,-1,mask)
    cvOutImage += 127

    cvOut2outImage()
    displayImageColor()
    saveWork('엠보싱_CV')

def blurrColor_CV() : # 블러링_CV 효과
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return

    cvOutImage = cv2.imread(filename)
    cvOutImage = cv2.blur(cvInImage, (5,5))


    cvOut2outImage()
    displayImageColor()
    saveWork('블러링_CV')

def sharpColor_CV(): #샤프닝_CV
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return

    cvOutImage = cv2.imread(filename)
    mask = np.array([[-1, -1, -1],
                     [-1, 9, -1],
                     [-1, -1, -1]])

    cvOutImage = cv2.filter2D(cvInImage, -1, mask)

    cvOut2outImage()
    displayImageColor()
    saveWork('샤프닝_CV')

def laplacColor_CV():  # 라플라시안_CV 수정해야댐
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage
    if filename == '' or filename == None:
        return

    cvOutImage = cv2.imread(filename)

    mask = np.array([[0.0, -1.0, 0.0],
                     [-1.0, 4.0, -1.0],
                     [0.0, -1.0, 0.0]])

    cvOutImage = cv2.filter2D(cvInImage, -1, mask)

    cvOut2outImage()
    displayImageColor()
    saveWork('라플라시안_CV')

def face_CV():
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList


    ##### OpenCV 용 영상처리 ###
    face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_alt.xml')
    grey = cv2.cvtColor(cvInImage[:], cv2.COLOR_BGR2GRAY)
    # 얼굴찾기
    cvOutImage = cvInImage
    fact_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(fact_rects)
    for x, y, w, h in fact_rects:
        cv2.rectangle(cvOutImage, (x, y), (x + h, y + w), (0, 255, 0), 3)

    cvOut2outImage()
    displayImageColor()

    # ########################

def nose_CV():
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList


    ##### OpenCV 용 영상처리 ###
    face_cascade = cv2.CascadeClassifier('haar/haarcascade_mcs_nose.xml')
    grey = cv2.cvtColor(cvInImage[:], cv2.COLOR_BGR2GRAY)
    # 코찾기
    cvOutImage = cvInImage
    fact_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(fact_rects)
    for x, y, w, h in fact_rects:
        cv2.rectangle(cvOutImage, (x, y), (x + h, y + w), (0, 255, 0), 3)

    cvOut2outImage()
    displayImageColor()

def ear_CV():

    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList


    ##### OpenCV 용 영상처리 ###
    face_cascade = cv2.CascadeClassifier('haar/haarcascade_mcs_leftear.xml')
    grey = cv2.cvtColor(cvInImage[:], cv2.COLOR_BGR2GRAY)
    # 코찾기
    cvOutImage = cvInImage
    fact_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(fact_rects)
    for x, y, w, h in fact_rects:
        cv2.rectangle(cvOutImage, (x, y), (x + h, y + w), (0, 255, 0), 3)

    cvOut2outImage()
    displayImageColor()

def mouth_CV():
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList


    ##### OpenCV 용 영상처리 ###
    face_cascade = cv2.CascadeClassifier('haar/haarcascade_mcs_mouth.xml')
    grey = cv2.cvtColor(cvInImage[:], cv2.COLOR_BGR2GRAY)
    # 코찾기
    cvOutImage = cvInImage
    fact_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(fact_rects)
    for x, y, w, h in fact_rects:
        cv2.rectangle(cvOutImage, (x, y), (x + h, y + w), (0, 255, 0), 3)

    cvOut2outImage()
    displayImageColor()

def catface_CV():
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList


    ##### OpenCV 용 영상처리 ###
    face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalcatface.xml')
    grey = cv2.cvtColor(cvInImage[:], cv2.COLOR_BGR2GRAY)
    # 고영희씨 찾기
    cvOutImage = cvInImage
    fact_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(fact_rects)
    for x, y, w, h in fact_rects:
        cv2.rectangle(cvOutImage, (x, y), (x + h, y + w), (0, 255, 0), 3)

    cvOut2outImage()
    displayImageColor()


## 딥러닝 ##
def deepStopImage_CV():

    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList


    ##### OpenCV 용 영상처리 ###
    # face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface.xml')
    # grey = cv2.cvtColor(cvInImage[:], cv2.COLOR_BGR2GRAY)
    cvOutImage = ssdNet(cvInImage)



    cvOut2outImage()
    displayImageColor()

def snapshot(f):
    cv2.imwrite('traffic.png',f)
    capture = cv2.VideoCapture('c:/images/traffic.mp4')

def deepMoveImage_CV():
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList

    movieName = askopenfilename(parent=window,
           filetypes=(('동영상 파일', '*.mp4;*.avi'), ('All File', '*.*')))
    s_factor = 0.8 ##화면 크기 비율(조절 가능)
    capture = cv2.VideoCapture(movieName)
    frameCount = 0 #처리할 프레임의 숫자


    ##### OpenCV 용 영상처리 ###
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        frameCount += 1
        if frameCount % 10 == 0: ##숫자 조절가능 (속도문제)
            frame = cv2.resize(frame, None, fx=s_factor, fy=s_factor, interpolation=cv2.INTER_AREA)
            ## 한장 짜리 ssd딥러닝
            retImage = ssdNet(frame)
            ##########################
            cv2.imshow('Video', retImage)


        key = cv2.waitKey(20)
        if key == 27:  # esc 키
            break
        if key == ord('c') or key == ord('C'):
            cvInImage = cvOutImage = retImage

            filename = movieName
            cvOut2outImage()
            displayImageColor()

    cv2.destroyWindow('Video')
    cvOut2outImage()

def ssdNet(image) :
    CONF_VALUE = 0.2 # 20% 인정한다는 의미
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    net = cv2.dnn.readNetFromCaffe("MibileNetSSD/MobileNetSSD_deploy.prototxt.txt", "MibileNetSSD/MobileNetSSD_deploy.caffemodel")
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > CONF_VALUE:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            cv2.rectangle(image, (startX, startY), (endX, endY),
                          COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    return image

def deepfire_CV():
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList

    movieName = askopenfilename(parent=window,
           filetypes=(('동영상 파일', '*.mp4;*.avi'), ('All File', '*.*')))
    s_factor = 0.8 ##화면 크기 비율(조절 가능)
    fire_cascade = cv2.CascadeClassifier('fire_detection.xml')

    cap = cv2.VideoCapture(movieName)

    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

        for (x, y, w, h) in fire:
            cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            print("불 감지")

        cv2.imshow('fire', frame)

        frameCount = 0
        if not ret:
            break
        frameCount += 1
        if frameCount % 10 == 0:  ##숫자 조절가능 (속도문제)
            frame = cv2.resize(frame, None, fx=s_factor, fy=s_factor, interpolation=cv2.INTER_AREA)
            ## 한장 짜리 ssd딥러닝
            # retImage = fire(frame)
            ##########################


        key = cv2.waitKey(20)
        if key == 27:  # esc 키
            break
        if key == ord('c') or key == ord('C'):
            cvInImage = cvOutImage = frame
            cv2.imshow('fire', frame)
            filename = movieName
            cvOut2outImage()
            displayImageColor()

    cv2.destroyWindow('fire')
    cvOut2outImage()



## 로그인, 레이아웃 ##
def showLogin():
    global entryID_login, entryPW_login, windowLogin
    ## 로그인 화면
    windowLogin = Tk()
    windowLogin.title("미니 프로젝트 Vol 2")
    windowLogin.geometry('290x200')

    ## ID 입력란
    frameID = Frame(windowLogin)
    frameID.pack(fill=X, pady=10)

    labelID = Label(frameID, text="ID", width=2)
    labelID.pack(side=LEFT, padx=10)

    entryID_login = Entry(frameID, width=10)
    entryID_login.pack(fill=X, expand=True, padx=10)

    ## PW 입력란
    framePW = Frame(windowLogin)
    framePW.pack(fill=X)

    labelPW = Label(framePW, text="PW", width=2)
    labelPW.pack(side=LEFT, padx=10)

    entryPW_login = Entry(framePW, width=10)
    entryPW_login.pack(fill=X, expand=True, padx=10)


    ## 버튼 란
    frameBTN = Frame(windowLogin)
    frameBTN.pack(fill=X, pady=5)

    btnLogin = Button(frameBTN, text='로그인', command=clickBtnLogin, width=10)
    btnLogin.pack(side=RIGHT, fill=X, padx=10)

    btnJoin = Button(frameBTN, text='회원가입', command=Admin_Input.Input, width=10)
    btnJoin.pack(side=RIGHT, fill=X, padx=10)

##################### (로그인 할때 귀찮으면 쓰는용) ####################################################################################

    # entryID_login.insert(0, 'test')
    # entryPW_login.insert(0, 'test')
    # btnLogin.invoke()

###################################################################################################################################################


    windowLogin.mainloop()

def clickBtnLogin():
    global windowLogin, boolUserLogin, entryID_login, entryPW_login, userID, boolRootLogin
    global conn, cur

    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()  # 빈 트럭 준비

    # 계정 정보 입력
    mem_id = entryID_login.get()
    mem_pw = entryPW_login.get()
    sql = "SELECT * FROM member_table WHERE member_table.mem_id = "
    sql += "'" + mem_id + "'"
    cur.execute(sql)
    mem_info = cur.fetchall()
    if mem_info[0][1] == mem_pw:
        userID = mem_info[0][0]
        messagebox.showinfo('성공', mem_id + ' 로그인 성공.')
        if userID == 'root':
            boolRootLogin = True
        else:
            boolUserLogin = True
        windowLogin.destroy()
    else:
        messagebox.showinfo('실패', mem_id + ' 암호 불일치.')

    cur.close()
    conn.close()

def saveWork(work):
    global windowImage, canvas, paper, inImage, outImage, inH, inW, outH, outW, filename
    global cvInImage, cvOutImage, fileList
    global userID
    global work_photoid, work_what, work_fname, work_ext

    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()  # 빈 트럭 준비

    saveCvPhoto = np.zeros((outH, outW, 3), np.uint8)
    for i in range(outH):
        for k in range(outW):
            tup = tuple(([outImage[B][i][k], outImage[G][i][k], outImage[R][i][k]]))
            saveCvPhoto[i, k] = tup
    saveFname = tempfile.gettempdir() + '/' + os.path.basename(filename)
    cv2.imwrite(saveFname, saveCvPhoto)
    # 파일을 읽기
    fp = open(saveFname, 'rb')
    blobData = fp.read()
    fp.close()

    work_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    sql = "INSERT INTO work_table(work_id, work_userid, work_photoid, work_what, work_fname, "
    sql += "work_ext, work_date, work_photo) "
    sql += "VALUES (" + "NULL, '" + userID + "', " + str(work_photoid) + ", '" + work
    sql += "', '" + work_fname + "', '" + work_ext + "', '" + work_date + "', %s )"
    tupleData = (blobData,)
    print(sql)


    cur.execute(sql, tupleData)
    conn.commit()
    cur.close()
    conn.close()


## 전역 변수부
windowImage, canvas, paper = None, None, None
# frame1, frame2 = None, None
inImage, outImage = [], [];
outImageBuf = []
inH, inW, outH, outW = [0] * 4
cvInImage, cvOutImage = None, None
filename = ''
RGB,R, G, B= 3, 0, 1, 2

# DB 관련
conn, cur = None, None  # 교량과 트럭
IP = '127.0.0.1'
USER = 'root'
PASSWORD = '1234'
DB = 'photo_db'
fileList = None
windowLogin = Tk
boolUserLogin, boolRootLogin = False, False
entryID_login, entryPW_login = Entry, Entry


boolImageDown = False
userID = None
work_photoid = None
work_what = None
work_fname = None
work_ext = None


## 메인 코드부
if __name__ == '__main__':
    showLogin()

    window = Tk()
    window.title('미니 프로젝트 Vol 2')
    window.geometry('512x512')

    #window.resizable(height=False, width=False)
    status = Label(window, text='이미지정보:', bd=1, relief=SUNKEN, anchor=W)
    status.pack(side=BOTTOM, fill=X)

    ### 메뉴 만들기 ###
    mainMenu = Menu(window)
    window.configure(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="파일", menu=fileMenu)
    fileMenu.add_command(label="열기(Open)", command=openFile)
    fileMenu.add_command(label="저장(Save)", command=saveImage)
    fileMenu.add_separator()
    fileMenu.add_command(label="닫기(Close)")

    pixelMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="화소점 처리(+_NP)", menu=pixelMenu)
    pixelMenu.add_command(label="동일영상", command=equalColor)
    pixelMenu.add_command(label="반전영상", command=reverseColor)
    pixelMenu.add_command(label="반전영상(NumPy)", command=reverseColor_NP)
    pixelMenu.add_command(label="그레이스케일", command=grayColor)
    pixelMenu.add_command(label="그레이스케일(NumPy)", command=grayColor_NP)
    pixelMenu.add_command(label="밝게하기", command=addColor)
    pixelMenu.add_command(label="밝게하기(NumPy)", command=addColor_NP)
    pixelMenu.add_command(label="이진화", command=bw1Color)
    pixelMenu.add_command(label="이진화(NumPy)", command=bw1Color_NP)
    pixelMenu.add_command(label="이진화(평균값)", command=bw2Color)
    pixelMenu.add_command(label="이진화(평균값/NumPy)", command=bw2Color_NP)
    pixelMenu.add_command(label="이진화(중위수)", command=bw3Color)
    pixelMenu.add_command(label="포스터라이징", command=addpColor)
    pixelMenu.add_command(label="감마연산(정수)", command=gammaColor)
    pixelMenu.add_command(label="감마연산(실수, NumPy)", command=gammaColor_NP)
    pixelMenu.add_command(label="파라볼라(Cup)", command=paraCupColor)
    pixelMenu.add_command(label="파라볼라(Cap)", command=paraCapColor)
    pixelMenu.add_command(label="범위강조 변환", command=point2Color)

    areaMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="화소영역 처리", menu=areaMenu)
    areaMenu.add_command(label="엠보싱", command=embossColor)
    areaMenu.add_command(label="블러링5x5", command=blurr5Color)
    areaMenu.add_command(label="샤프닝", command=sharpColor)
    areaMenu.add_command(label="라플라시안", command=laplacColor)

    geometryMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="기하학 처리", menu=geometryMenu)
    geometryMenu.add_command(label="영상 이동", command=moveColor)
    geometryMenu.add_command(label="영상 축소", command=zoomOutColor)
    geometryMenu.add_command(label="영상 확대", command=zoomInColor)
    geometryMenu.add_command(label="영상 회전", command=rotateColorImage)

    MySQLMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="MySQL", menu=MySQLMenu)
    MySQLMenu.add_command(label="MySQL에 저장", command=saveMySQL)
    MySQLMenu.add_command(label="MySQL에서 열기", command=openMySQL)
    MySQLMenu.add_command(label="MySQL에서 폴더 열기", command=upAllMySQL)
    MySQLMenu.add_command(label="작업기록", command=showWorkList)

    excelMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="Excel", menu=excelMenu)
    excelMenu.add_command(label="Excel에서 열기", command=openExcel)
    excelMenu.add_command(label="Excel에 저장", command=saveExcel)
    excelMenu.add_separator()
    excelMenu.add_command(label="Excel 아트", command=drawExcel)

    openCVMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="OpenCV", menu=openCVMenu)
    openCVMenu.add_command(label="그레이 스케일", command=grayscale_CV)
    openCVMenu.add_command(label="카툰 이미지", command=cartoon_CV)
    openCVMenu.add_command(label="엠보싱", command=emboss_CV)
    openCVMenu.add_command(label="블러링", command=blurrColor_CV)
    openCVMenu.add_command(label="샤프닝", command=sharpColor_CV)
    openCVMenu.add_command(label="라플라시안", command=laplacColor_CV)

    ## Machine Learning ##
    haarMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="하르케스케이드", menu=haarMenu)
    haarMenu.add_command(label="얼굴 인식", command=face_CV)
    haarMenu.add_command(label="코 인식", command=nose_CV)
    haarMenu.add_command(label="귀 인식", command=ear_CV)
    haarMenu.add_command(label="입 인식", command=mouth_CV)
    haarMenu.add_command(label="고양이 얼굴 인식", command=catface_CV)

    deepCVMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="딥러닝", menu=deepCVMenu)
    deepCVMenu.add_command(label="사물 인식(정지영상)", command=deepStopImage_CV)
    deepCVMenu.add_command(label="사람, 사물 인식(동영상)", command=deepMoveImage_CV)
    deepCVMenu.add_command(label="불 인식(동영상)", command=deepfire_CV)
    ######################
    window.mainloop()

    # elif boolRootLogin == True:
        # Admin_main.admin()

    # else:
        # messagebox.showinfo("오류","로그인을 하세요.")