import cv2
import numpy as np
from dface.core.detect import create_mtcnn_net, MtcnnDetector
import time
from image_match.goldberg import ImageSignature
import matlab.engine
import os
# import camera_configs


"""
    .   Binocular Camera and Thermal Camera parameters
    .   
    .   @param thermal_fx focus distance of thermal camera / sensor width
    .   @param thermal_fy focus distance of thermal camera / sensor height
    .   @param fx focus distance of binocular camera / sensor width
    .   @param fy focus distance of binocular camera / sensor height
    .   note that the former four parameters can be measured by experiments
    .   @param dy distance between optical centers of thermal camera and binocular camera(the left one) Unit: mm
    .   @param b distance between binocular cameras Unit: mm
    """
thermal_fx = 1050
thermal_fy = 1050
fx = 744
fy = 744
dy = -60
dx = 0
b = 58.7


# Left button click callback on thermal image
# def mouse_callback(event, x, y, flags, param):
#     global TempArray
#     if event == cv2.EVENT_LBUTTONDBLCLK & (TempArray is not None):
#         print(TempArray[y, x])


# Presentation UI
cv2.namedWindow('Thermal_frame', 0)
cv2.resizeWindow('Thermal_frame', 640, 480)
cv2.moveWindow('Thermal_frame', 650, 0)
# cv2.setMouseCallback('Thermal_frame', mouse_callback)
cv2.namedWindow('Left_frame', 0)
cv2.moveWindow("Left_frame", 0, 0)
cv2.resizeWindow('Left_frame', 640, 480)
cv2.namedWindow('Right_frame', 0)
cv2.moveWindow("Right_frame", 0, 490)
cv2.resizeWindow('Right_frame', 640, 480)

# Initiate MatLab engine for Thermal Camera
matlab_engine = matlab.engine.start_matlab()
matlab_engine.addpath(os.path.dirname(os.path.realpath(__file__)))
matlab_engine.addpath('.\\Fluke\\MATLAB Toolkit\\Source Code\\FlukeStreamingGUI\\')
isReadingThermal = matlab_engine.StartStream(nargout=1)

# Initiate Binocular Camera & Face Detection
cap = cv2.VideoCapture(1)
pnet, rnet, onet = create_mtcnn_net(p_model_path="./model_store/pnet_epoch.pt",
                                    r_model_path="./model_store/rnet_epoch.pt",
                                    o_model_path="./model_store/onet_epoch.pt", use_cuda=True)
mtcnn_detector = MtcnnDetector(pnet=pnet, rnet=rnet, onet=onet, min_face_size=24)

ColorPool = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]


def pHash(image):
    return ImageSignature().generate_signature(image)


def similarity_distance(image1, image2):
    return ImageSignature.normalized_distance(image1, image2)


def find_min(matrix):
    mini = 0
    minj = 0
    minr = 1
    for i in matrix.keys():
        if len(matrix[i].keys()) == 0:
            return None, None, None
        for j in matrix[i].keys():
            if matrix[i][j] <= minr:
                mini = i
                minj = j
                minr = matrix[i][j]
    return minr, mini, minj


# Binocular Ranging Algorithm
def binocular_distance_measurement(frame_left, frame_right):
    bboxs_left, landmarks_left = mtcnn_detector.detect_face(frame_left)
    if bboxs_left.shape[0] == 0:
        return bboxs_left, landmarks_left, None, None, None
    bboxs_left, landmarks_left = sort_by_position(bboxs_left, landmarks_left)
    bboxs_left[bboxs_left < 0] = 0
    bboxs_right, landmarks_right = mtcnn_detector.detect_face(frame_right)
    bboxs_right, landmarks_right = sort_by_position(bboxs_right, landmarks_right)
    bboxs_right[bboxs_right < 0] = 0
    faces_left = []
    faces_right = []

    couple = []

    similarity_matrix = {}

    # calculate the correlations and significance level
    for i in range(bboxs_left.shape[0]):
        similarity_matrix[i] = {}
        faces_left.append(
            frame_left[int(bboxs_left[i][1]):int(bboxs_left[i][3]), int(bboxs_left[i][0]):int(bboxs_left[i][2])])
        # cv2.imwrite('face_l.jpg', faces_left[i])
        for j in range(bboxs_right.shape[0]):
            if i == 0:
                faces_right.append(frame_right[int(bboxs_right[j][1]):int(bboxs_right[j][3]),
                                   int(bboxs_right[j][0]):int(bboxs_right[j][2])])
            # cv2.matchTemplate
            # r, p = stats.pearsonr(landmarks_left[i], landmarks_right[j])
            # cv2.imwrite('face_r.jpg', faces_right[j])
            similarity_matrix[i][j] = similarity_distance(pHash(faces_left[i]), pHash(faces_right[j]))
            # print(i, j, Rs[j])

    while len(similarity_matrix.keys()) > 0:
        r, i, j = find_min(similarity_matrix)
        if i is None or j is None or r is None:
            break
        # left = (landmarks_left[i][0] + landmarks_left[i][2] + landmarks_left[i][4] + landmarks_left[i][6] +
        #         landmarks_left[i][8]) / 5
        # right = (landmarks_right[j][0] + landmarks_right[j][2] + landmarks_right[j][4] + landmarks_right[j][6] +
        #          landmarks_right[j][8]) / 5
        # print('1:', abs(landmarks_right[j][0] - landmarks_left[i][0]), '2:', abs(landmarks_right[j][2] - landmarks_left[i][2]), '3:', abs(landmarks_right[j][4] - landmarks_left[i][4]), '4:', abs(landmarks_right[j][6] - landmarks_left[i][6]), '5:', abs(landmarks_right[j][8] - landmarks_left[i][8]))
        left = (bboxs_left[i][0] + bboxs_left[i][2]) / 2
        right = (bboxs_right[j][0] + bboxs_right[j][2]) / 2
        d = abs(right - left)
        # distance = b * fx / d
        # distance = 92284.619 / d - 562.8836
        distance = 6877.0412 / d
        variance = (-0.003530762 * distance + 10.110305) * (-0.003530762 * distance + 10.110305)
        if variance < 0:
            variance = 0

        couple.append([i, j, distance, r, variance])

        del similarity_matrix[i]
        for key in similarity_matrix.keys():
            del similarity_matrix[key][j]

    bboxs_left, landmarks_left = np.round(bboxs_left).astype(int), np.round(landmarks_left).astype(int)
    bboxs_right, landmarks_right = np.round(bboxs_right).astype(int), np.round(landmarks_right).astype(int)
    couple = np.array(couple)
    return bboxs_left, landmarks_left, bboxs_right, landmarks_right, couple


# sort face by position(left->right, up->down)
def sort_by_position(bboxs, landmarks):
    if bboxs.shape[0] == 0:
        return bboxs, landmarks
    new_bboxs = []
    new_landmarks = []
    new_bboxs.append(bboxs[0])
    new_landmarks.append(landmarks[0])

    # priority from left to right, up to down
    for i in range(bboxs.shape[0] - 1):
        for j in range(len(new_bboxs)):
            if bboxs[i + 1][0] < new_bboxs[j][0]:
                new_bboxs.insert(j, bboxs[i + 1])
                new_landmarks.insert(j, landmarks[i + 1])
                break
            elif bboxs[i + 1][0] == new_bboxs[j][0]:
                if bboxs[i + 1][1] < new_bboxs[j][1]:
                    new_bboxs.insert(j, bboxs[i + 1])
                    new_landmarks.insert(j, landmarks[i + 1])
                    break
        else:
            new_bboxs.append(bboxs[i + 1])
            new_landmarks.append(landmarks[i + 1])

    # convert to ndarray
    new_bboxs = np.array(new_bboxs)
    new_landmarks = np.array(new_landmarks)
    return new_bboxs, new_landmarks


# Binocular Camera & Thermal Camera
def camera():
    start = time.asctime(time.localtime(time.time()))
    former_bboxs_left, former_landmarks_left, former_bboxs_right, former_landmarks_right, former_couple = np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
    history_variance = []

    # while count < 1000:
    while True:
        # Capture frame-by-frame
        ret, Dual_frame = cap.read()
        Dual_height = Dual_frame.shape[0]
        Dual_width = Dual_frame.shape[1]
        # print(Dual_height, Dual_width)
        Left_frame, Right_frame = Dual_frame[:, :int(Dual_width / 2)], Dual_frame[:, int(Dual_width / 2):Dual_width]
        # Left_frame = cv2.remap(Left_frame, camera_config.left_map1, camera_config.left_map2, cv2.INTER_LINEAR)
        # Right_frame = cv2.remap(Right_frame, camera_config.right_map1, camera_config.right_map2, cv2.INTER_LINEAR)

        bboxs_left, landmarks_left, bboxs_right, landmarks_right, couple = binocular_distance_measurement(Left_frame,
                                                                                                          Right_frame)

        TempArray, MatImage = matlab_engine.GetThermalData(nargout=2)
        if not (MatImage is None):
            TempArray = np.array(TempArray._data).reshape(TempArray.size, order='F')
            MatImage = np.array(MatImage._data, dtype='uint8').reshape(MatImage.size, order='F')
            MatImage = cv2.UMat(MatImage)

        # if bboxs_left.shape[0] > 0:
        #     count += 1

        matched = 0
        for i in range(bboxs_left.shape[0]):
            width = bboxs_left[i][2] - bboxs_left[i][0]
            height = bboxs_left[i][3] - bboxs_left[i][1]

            # distance = 500.0
            for j in range(couple.shape[0]):
                if i == couple[j][0]:
                    matched += 1
                    coupledRight = int(couple[j][1])
                    # print(coupledRight)
                    distance = couple[j][2]
                    variance = couple[j][4]
                    # print(distance)
                    r = couple[j][3]
                    # p = couple[j][4]

                    # Kalman filtering
                    if former_couple is not None and former_couple.shape[0] >= matched:
                        # print('未通过卡尔曼滤波：', distance)
                        former_distance = former_couple[j][2]
                        former_variance = former_couple[j][4]
                        distance = former_distance + (former_variance / (former_variance + variance)) * (distance - former_distance)
                        # update variance and distance
                        couple[j][4] = (variance / (former_variance + variance) * former_variance) ** 0.5
                        couple[j][2] = distance
                        # print('通过卡尔曼滤波后：', distance)
                    # else:
                    #     history_variance = variance

                    cv2.putText(Left_frame, str(format(distance * 0.001, '0.3f')) + 'm',
                                (bboxs_left[i][0], bboxs_left[i][1] - 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

                    cv2.rectangle(Right_frame, (bboxs_right[coupledRight][0], bboxs_right[coupledRight][1]),
                                  (bboxs_right[coupledRight][2], bboxs_right[coupledRight][3]), ColorPool[int(i % 3)],
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

                    # Get Thermal data and image
                    # distance = 200
                    if not (MatImage is None):
                        # thermal_height = int(height * thermal_f / f * 0.7)
                        # thermal_width = int(width * thermal_f / f * 0.7)
                        left = bboxs_left[i][0]
                        up = bboxs_left[i][1]
                        right = bboxs_left[i][2]
                        down = bboxs_left[i][3]
                        thermal_left = int(
                            thermal_fx / fx * left + Dual_width / 4 - Dual_width / 4 * thermal_fx / fx + thermal_fx * dx / distance)
                        thermal_up = int(
                            thermal_fy / fy * up + Dual_height / 2 + dy * thermal_fy / distance - Dual_height / 2 * thermal_fy / fy)
                        thermal_right = int(
                            thermal_fx / fx * right + Dual_width / 4 - Dual_width / 4 * thermal_fx / fx + thermal_fx * dx / distance)
                        thermal_down = int(
                            thermal_fy / fy * down + Dual_height / 2 + dy * thermal_fy / distance - Dual_height / 2 * thermal_fy / fy)
                        # print('(', thermal_left, ',', thermal_up, ')', '(', thermal_right, ',', thermal_down, ')')
                        if thermal_left < 0:
                            thermal_left = int(0)
                        if thermal_up < 0:
                            thermal_up = int(0)
                        if thermal_down < 0:
                            thermal_down = int(0)
                        if thermal_right < 0:
                            thermal_right = int(0)
                        if thermal_left != thermal_right and thermal_up != thermal_down and thermal_down < Dual_height and thermal_right < Dual_width / 2:
                            # face_thermal = TempArray[thermal_up:thermal_up + thermal_height,
                            #                thermal_left:thermal_left + thermal_width]
                            face_thermal = TempArray[thermal_up:thermal_down,
                                           thermal_left:thermal_right]
                            temperature = np.max(face_thermal)
                            cv2.rectangle(MatImage, (thermal_left, thermal_up),
                                          (thermal_right, thermal_down),
                                          ColorPool[int(i % 3)], 2)
                            cv2.putText(Left_frame, str(format(temperature, '.1f')) + '摄氏度',
                                        (bboxs_left[i][0], bboxs_left[i][1] + 10),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
                            print(i, 'temperature:', str(format(temperature, '.1f')) + '摄氏度', 'distance:',
                                  str(format(distance * 0.001, '.3f')) + 'm')

            cv2.rectangle(Left_frame, (bboxs_left[i][0], bboxs_left[i][1]), (bboxs_left[i][2], bboxs_left[i][3]),
                          ColorPool[int(i % 3)], 2)
            cv2.circle(Left_frame, (landmarks_left[i][0], landmarks_left[i][1]), 1, (0, 0, 255), 4)
            cv2.circle(Left_frame, (landmarks_left[i][2], landmarks_left[i][3]), 1, (0, 0, 255), 4)
            cv2.circle(Left_frame, (landmarks_left[i][4], landmarks_left[i][5]), 1, (0, 0, 255), 4)
            cv2.circle(Left_frame, (landmarks_left[i][6], landmarks_left[i][7]), 1, (0, 0, 255), 4)
            cv2.circle(Left_frame, (landmarks_left[i][8], landmarks_left[i][9]), 1, (0, 0, 255), 4)

            ll = time.localtime(time.time())
            timestamp = ll.tm_hour * 10000 + ll.tm_min * 100 + ll.tm_sec
            # print('width:', str(width), 'height:', str(height), 'area:', str(area), timestamp)
            # save2[count, i*3], save2[count, i*3 + 1], save2[count, i*3 + 2] = width, height, area

        former_bboxs_left, former_landmarks_left, former_bboxs_right, former_landmarks_right, former_couple = bboxs_left, landmarks_left, bboxs_right, landmarks_right, couple

        cv2.imshow('Left_frame', Left_frame)
        cv2.imshow('Right_frame', Right_frame)
        cv2.imshow('Thermal_frame', MatImage)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # ll = time.localtime(time.time())
        # timestamp = ll.tm_hour * 10000 + ll.tm_min * 100 + ll.tm_sec
        # save2[count, 9] = timestamp
        # count += 1

    # sio.savemat('save2.mat', {'A': save2})
    # When everything done, release the capture
    matlab_engine.StopStream(nargout=0)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    camera()
