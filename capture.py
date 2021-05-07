import cv2
import matlab.engine
import os
import numpy as np
from image_match.goldberg import ImageSignature
from dface.core.detect import create_mtcnn_net, MtcnnDetector
from binocular_distance_measurement import binocular_distance_measurement

true_distance = 400  # mm
count = 300
cap = cv2.VideoCapture(1)
pnet, rnet, onet = create_mtcnn_net(p_model_path="./model_store/pnet_epoch.pt",
                                    r_model_path="./model_store/rnet_epoch.pt",
                                    o_model_path="./model_store/onet_epoch.pt", use_cuda=True)
mtcnn_detector = MtcnnDetector(pnet=pnet, rnet=rnet, onet=onet, min_face_size=24)
# matlab_engine = matlab.engine.start_matlab()
# matlab_engine.addpath(os.path.dirname(os.path.realpath(__file__)))
# matlab_engine.addpath('D:\\matlabWork\\Fluke\\MATLAB Toolkit\\Source Code\\FlukeStreamingGUI\\')
# isReadingThermal = matlab_engine.StartStream(nargout=1)

cv2.namedWindow("Thermal_frame", 0)
cv2.moveWindow("Thermal_frame", 0, 490)
cv2.resizeWindow("Thermal_frame", 640, 480)
# cv2.setMouseCallback('Thermal_frame', mouse_callback)
cv2.namedWindow('Left_frame', 0)
cv2.moveWindow("Left_frame", 0, 0)
cv2.resizeWindow("Left_frame", 640, 480)
cv2.namedWindow('Right_frame', 0)
cv2.moveWindow("Right_frame", 650, 0)
cv2.resizeWindow("Right_frame", 640, 480)

file_handler = open(str(true_distance) + '.txt', mode='w')

while True:
    ret, Dual_frame = cap.read()
    # cv2.imshow('frame', Dual_frame)
    Dual_height = Dual_frame.shape[0]
    Dual_width = Dual_frame.shape[1]
    Left_frame, Right_frame = Dual_frame[:, :int(Dual_width / 2)], Dual_frame[:, int(Dual_width / 2):Dual_width]
    # TempArray, MatImage = matlab_engine.GetThermalData(nargout=2)
    # if not (MatImage is None):
    #     TempArray = np.array(TempArray._data).reshape(TempArray.size, order='F')
    #     MatImage = np.array(MatImage._data, dtype='uint8').reshape(MatImage.size, order='F')
    #     MatImage = cv2.UMat(MatImage)
    #     cv2.imshow('Thermal_frame', MatImage)

    bboxs_left, landmarks_left, bboxs_right, landmarks_right, couple = binocular_distance_measurement(Left_frame,
                                                                                                      Right_frame)
    for i in range(bboxs_left.shape[0]):
        width = bboxs_left[i][2] - bboxs_left[i][0]
        height = bboxs_left[i][3] - bboxs_left[i][1]

        hasCoupled = False
        distance = 0.0
        for j in range(couple.shape[0]):
            if i == couple[j][0]:
                hasCoupled = True
                coupledRight = int(couple[j][1])
                # print(coupledRight)
                distance = couple[j][2]
                # print(distance)
                r = couple[j][3]
                # p = couple[j][4]

                # cv2.putText(Left_frame, 'Distance: ' + str(int(distance)) + 'mm',
                #             (bboxs_left[i][0], bboxs_left[i][1] + int(round(30 * width / 400))),
                #             cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

                cv2.putText(Left_frame, str(format(distance * 0.001, '0.3f')) + 'm',
                            (bboxs_left[i][0], bboxs_left[i][1] - 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

                cv2.rectangle(Right_frame, (bboxs_right[coupledRight][0], bboxs_right[coupledRight][1]),
                              (bboxs_right[coupledRight][2], bboxs_right[coupledRight][3]), (0, 0, 255),
                              2)
                cv2.circle(Right_frame, (landmarks_right[coupledRight][0], landmarks_right[coupledRight][1]), 1,
                           (0, 0, 255), 4)
                cv2.circle(Right_frame, (landmarks_right[coupledRight][2], landmarks_right[coupledRight][3]), 1,
                           (0, 0, 255), 4)
                cv2.circle(Right_frame, (landmarks_right[coupledRight][4], landmarks_right[coupledRight][5]), 1,
                           (0, 0, 255), 4)
                cv2.circle(Right_frame, (landmarks_right[coupledRight][6], landmarks_right[coupledRight][7]), 1,
                           (0, 0, 255), 4)
                cv2.circle(Right_frame, (landmarks_right[coupledRight][8], landmarks_right[coupledRight][9]), 1,
                           (0, 0, 255), 4)
                file_handler.write(str(format(bboxs_left[i][0], '0.3f')) + ' ' + str(format(bboxs_left[i][1], '0.3f')) + ' ' + str(format(bboxs_left[i][2], '0.3f')) + ' ' + str(format(bboxs_left[i][3], '0.3f')) + ' ' + str(format(bboxs_right[coupledRight][0], '0.3f')) + ' ' + str(format(bboxs_right[coupledRight][1], '0.3f')) + ' ' + str(format(bboxs_right[coupledRight][2], '0.3f')) + ' ' + str(format(bboxs_right[coupledRight][3], '0.3f')) + '\n')
                count = count - 1

        cv2.rectangle(Left_frame, (bboxs_left[i][0], bboxs_left[i][1]), (bboxs_left[i][2], bboxs_left[i][3]),
                      (0, 0, 255), 2)

    if count <= 0:
        break
    cv2.imshow('Left_frame', Left_frame)
    cv2.imshow('Right_frame', Right_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# matlab_engine.StopStream(nargout=0)
file_handler.close()
cap.release()
cv2.destroyAllWindows()