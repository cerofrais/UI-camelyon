from flask import Flask,request,render_template
import os
import cv2
import numpy as np

app = Flask(__name__,template_folder='templates')

App_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(App_path,'data')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/upload', methods=["POST","GET"])
def upload():

    static_path = os.path.join(App_path,'static')
    # if not os.path.exists(data_path):
    #     os.mkdir(data_path)

    for upload in request.files.getlist("file"):
        print(upload.filename)
        filename = upload.filename
        if not allowedfile(filename):
            return render_template('home.html')
        dest = os.path.join(static_path,filename)

        upload.save(dest)
        try :
            height, width,crops = make_crops(dest)
        except :
            crops = 0
        if crops:

            for each in os.listdir('CROP'):
                crop_img = cv2.imread(os.path.join('CROP',each))
                c_image = cv2.Canny(crop_img,100,200)
                cv2.imwrite("canny_crop/c_"+each,c_image)
            stich_back(height, width)

    return render_template('uploaded.html',img_name = filename,img_2 ='c_download.jpg')

def allowedfile(name):
    #print(name[-3:])
    return name[-3:] in ['jpg','jpeg','png']

def make_crops(filename):
    img = cv2.imread(filename)
    #img2 = img
    cv2.imshow('raw',img)
    height, width, channels = img.shape
    # Number of pieces Horizontally
    CROP_W_SIZE = 3
    # Number of pieces Vertically to each Horizontal
    CROP_H_SIZE = 2

    for ih in range(CROP_H_SIZE):
        for iw in range(CROP_W_SIZE):
            x = width / CROP_W_SIZE * iw
            y = height / CROP_H_SIZE * ih
            h = (height / CROP_H_SIZE)
            w = (width / CROP_W_SIZE)
            #print(x, y, h, w)
            crop_img = img[int(y):int(y + h), int(x):int(x + w)]

            NAME = 'crop_'+str(ih)+'_'+str(iw)
            cv2.imwrite("CROP/" + NAME + ".png", crop_img)

    return height, width,1

def stich_back(height, width):
    c_full_img=np.zeros((height, width,3))
    each = os.listdir('canny_crop')
    CROP_W_SIZE = 3
    # Number of pieces Vertically to each Horizontal
    CROP_H_SIZE = 2
    count=0
    for ih in range(CROP_H_SIZE):
        for iw in range(CROP_W_SIZE):

            x = width / CROP_W_SIZE * iw
            y = height / CROP_H_SIZE * ih
            h = (height / CROP_H_SIZE)
            w = (width / CROP_W_SIZE)
            # print(x, y, h, w)
            c_full_img[int(y):int(y + h), int(x):int(x + w),:3] = cv2.imread(os.path.join('canny_crop',each[count]))
            count=count+1
    cv2.imwrite('static/c_download.jpg',c_full_img)
    return 'static/c_download.jpg'





if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port= 8888 )

