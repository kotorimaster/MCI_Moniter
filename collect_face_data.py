import cv2
import Face_Distance_Mosaic
import numpy as np


if __name__ == '__main__':
    cv2.namedWindow('frame', 0)
    cv2.moveWindow("frame", 0, 0)
    cv2.resizeWindow('frame', 960, 540)

    cap = cv2.VideoCapture(1)
    ret = cap.set(3, 3840)
    # print(ret)
    ret = cap.set(4, 2160)
    # print(ret)
    while(1):
        ret, frame = cap.read()
        # print(ret)
        bboxs, frame = Face_Distance_Mosaic.face_detect(frame)
        bboxs = np.array(bboxs)
        if(bboxs.shape[0] > 0):
            cv2.rectangle(frame, (bboxs[0][0], bboxs[0][1]), (bboxs[0][2], bboxs[0][3]), (0, 0, 255), 5)
            print('Width: ', bboxs[0][2] - bboxs[0][0])
            print('Height: ', bboxs[0][3] - bboxs[0][1])
            print('Area: ', (bboxs[0][2] - bboxs[0][0]) * (bboxs[0][3] - bboxs[0][1]))
        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break