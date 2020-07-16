import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import cv2
import pytesseract
# import matplotlib.pyplot as plt


def rm_regression(img, border):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoise = cv2.fastNlMeansDenoising(gray, h=50)
    ret, thres = cv2.threshold(denoise, 127, 255, cv2.THRESH_BINARY_INV)
    ori = thres.copy()
    height = thres.shape[0]
    width = thres.shape[1]
    thres[:, border:width - border] = 0
    border_data = np.where(thres == 255)
    Y_label = border_data[0]
    samples = Y_label.shape[0]
    X_ori = border_data[1].reshape(samples, 1)
    reg = LinearRegression()
    feature = PolynomialFeatures(degree=2)
    X_input = feature.fit_transform(X_ori)

    reg.fit(X_input, Y_label)
    # print('二項函數係數: ', reg.coef_)
    # print('二項函數截距: ', reg.intercept_)

    newX_ori = np.array([i for i in range(width)])
    newX_ori = newX_ori.reshape(newX_ori.shape[0], 1)
    newX_input = feature.fit_transform(newX_ori)
    newY = reg.predict(newX_input)

    # plt.ylim(bottom=0, top=height)
    # plt.scatter(X_ori, height - Y_label, color='blue', s=1)
    # plt.scatter(newX_ori, height - newY, color='red', s=1)
    # plt.show()

    img_cuv = np.zeros_like(ori)
    newY = newY.round(0)
    for point in np.column_stack([newY, newX_ori]):
        py = int(point[0])
        px = int(point[1])
        w = 3
        img_cuv[py - w:py + w, px] = 255
    diff = cv2.absdiff(ori, img_cuv)
    denoise = cv2.fastNlMeansDenoising(diff, h=80)
    return denoise


if __name__ == '__main__':
    img = cv2.imread('RPHF.png')
    result_img = rm_regression(img, border=9)
    ocr_txt = pytesseract.image_to_string(result_img)
    print('ocr結果', ocr_txt)
    cv2.imshow('2', result_img)
    cv2.imshow('1', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
