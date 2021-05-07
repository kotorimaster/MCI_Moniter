# created by Xikang Jiang
import cv2
import torch
from dface.core.detect import create_mtcnn_net, MtcnnDetector
import time
from image_match.goldberg import ImageSignature
import numpy as np
import Face_Distance_Mosaic


def __init__():
    pass


class binocular_camera:
    """A class for binocular camera

    Description:

    Attributes:

    Methods:

    """
    cap = None  # instance for binocular camera
    fx = None  # focus distance of binocular camera / sensor width
    fy = None  # focus distance of binocular camera / sensor height
    b = None  # distance between binocular cameras Unit: mm
    width = None
    height = None

    # face detection module
    pnet, rnet, onet = None, None, None
    mtcnn_detector = None

    binocular_frame, left_frame, right_frame = None, None, None
    faces = {'Left': None, 'Right': None}  # faces in left and right frames
    landmarks = {'Left': None, 'Right': None}  # landmarks of faces in left and right frames
    couples = None  # couples for faces in left and right frames
    former_bboxs_left, former_bboxs_right, former_couples = None, None, None  # former faces, landmarks and couples for Kalman smoother

    timestamp = None
    face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')

    def __init__(self, camera_index=[0], fx=2300, fy=2300, b=58.7):
        if len(camera_index) == 1:
            self.cap = [cv2.VideoCapture(camera_index[0])]
            if self.cap is None:
                raise Exception('No Camera Found!')
            ret = self.cap[0].set(3, 2000)
            ret = self.cap[0].set(4, 1000)
            ret, dual_frame = self.cap[0].read()
            # print('ret', ret)
            self.height = dual_frame.shape[0]
            self.width = dual_frame.shape[1]
            # print(self.height, self.width)
            # fx, fy = 1400, 1400
        elif len(camera_index) == 2:
            self.cap = [cv2.VideoCapture(camera_index[0]), cv2.VideoCapture(camera_index[1])]
            if self.cap is None:
                raise Exception('No Camera Found!')
            ret = self.cap[0].set(3, 3840)
            ret = self.cap[0].set(4, 2160)
            ret = self.cap[1].set(3, 3840)
            ret = self.cap[1].set(4, 2160)
            ret, dual_frame = self.cap[0].read()
            
            # print('ret', ret)
            self.height = dual_frame.shape[0]
            self.width = dual_frame.shape[1] * 2
            # print(self.height, self.width)
        self.fx = fx
        self.fy = fy
        self.b = b
        # self.pnet, self.rnet, self.onet = create_mtcnn_net(p_model_path="./model_store/pnet_epoch.pt",
        #                                                    r_model_path="./model_store/rnet_epoch.pt",
        #                                                    o_model_path="./model_store/onet_epoch.pt",
        #                                                    use_cuda=torch.cuda.is_available())
        # self.mtcnn_detector = MtcnnDetector(pnet=self.pnet, rnet=self.rnet, onet=self.onet, min_face_size=24)

    def pHash(self, image):
        return ImageSignature().generate_signature(image)

    def similarity_distance(self, image1, image2):
        return ImageSignature.normalized_distance(image1, image2)

    def find_min(self, matrix):
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
        return minr, int(mini), int(minj)

    def sort_by_position(self, bboxs):
        if bboxs.shape[0] == 0:
            return bboxs
        new_bboxs = []
        new_bboxs.append(bboxs[0])

        # priority from left to right, up to down
        for i in range(bboxs.shape[0] - 1):
            for j in range(len(new_bboxs)):
                if bboxs[i + 1][0] < new_bboxs[j][0]:
                    new_bboxs.insert(j, bboxs[i + 1])
                    break
                elif bboxs[i + 1][0] == new_bboxs[j][0]:
                    if bboxs[i + 1][1] < new_bboxs[j][1]:
                        new_bboxs.insert(j, bboxs[i + 1])
                        break
            else:
                new_bboxs.append(bboxs[i + 1])

        # convert to ndarray
        new_bboxs = np.array(new_bboxs)
        return new_bboxs

    def binocular_distance_measurement(self, frame_left, frame_right):
        # bboxs_left, landmarks_left = self.mtcnn_detector.detect_face(frame_left)
        # bboxs_left = self.face_cascade.detectMultiScale(
        #     cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY),
        #     scaleFactor=1.15,
        #     minNeighbors=5,
        #     minSize=(5, 5)
        # )
        bboxs_left, frame_left = Face_Distance_Mosaic.face_detect(frame_left)
        # for i in range(len(bboxs_left)):
        #     bboxs_left[i] = [bboxs_left[i][0], bboxs_left[i][1], bboxs_left[i][0] + bboxs_left[i][2],
        #                      bboxs_left[i][1] + bboxs_left[i][3]]
        bboxs_left = np.array(bboxs_left)
        if bboxs_left.shape[0] == 0:
            return bboxs_left, None, None
        bboxs_left = self.sort_by_position(bboxs_left)
        bboxs_left[bboxs_left < 0] = 0
        # print(bboxs_left)
        # print(frame_left.shape)
        # bboxs_right, landmarks_right = self.mtcnn_detector.detect_face(frame_right)
        # bboxs_right = self.face_cascade.detectMultiScale(
        #     cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY),
        #     scaleFactor=1.15,
        #     minNeighbors=5,
        #     minSize=(5, 5)
        # )
        bboxs_right, frame_right = Face_Distance_Mosaic.face_detect(frame_right)
        # for i in range(len(bboxs_right)):
        #     bboxs_right[i] = [bboxs_right[i][0], bboxs_right[i][1], bboxs_right[i][0] + bboxs_right[i][2],
        #                       bboxs_right[i][1] + bboxs_right[i][3]]
        bboxs_right = np.array(bboxs_right)
        bboxs_right = self.sort_by_position(bboxs_right)
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
                similarity_matrix[i][j] = self.similarity_distance(self.pHash(faces_left[i]),
                                                                   self.pHash(faces_right[j]))
                # print(i, j, Rs[j])

        while len(similarity_matrix.keys()) > 0:
            r, i, j = self.find_min(similarity_matrix)
            if i is None or j is None or r is None:
                break
            # left = (landmarks_left[i][0] + landmarks_left[i][2] + landmarks_left[i][4] + landmarks_left[i][6] +
            #         landmarks_left[i][8]) / 5
            # right = (landmarks_right[j][0] + landmarks_right[j][2] + landmarks_right[j][4] + landmarks_right[j][6] +
            #          landmarks_right[j][8]) / 5
            # print('1:', abs(landmarks_right[j][0] - landmarks_left[i][0]), '2:', abs(landmarks_right[j][2] - landmarks_left[i][2]), '3:', abs(landmarks_right[j][4] - landmarks_left[i][4]), '4:', abs(landmarks_right[j][6] - landmarks_left[i][6]), '5:', abs(landmarks_right[j][8] - landmarks_left[i][8]))
            left = (bboxs_left[i][0] + bboxs_left[i][2]) / 2
            right = (bboxs_right[j][0] + bboxs_right[j][2]) / 2
            face_width = bboxs_left[i][2] - bboxs_left[i][0]
            d = abs(right - left)
            # distance = self.b * self.fx / d
            # # print(d)
            distance = 99086.186 / d
            # distance = 68758.58 / d
            # distance = self.fy * 150 / face_width

            # variance = (-0.003530762 * distance + 10.110305) * (-0.003530762 * distance + 10.110305)
            variance = 27562.877 / d
            if variance < 0:
                variance = 0

            couple.append([i, j, distance, r, variance])

            del similarity_matrix[i]
            for key in similarity_matrix.keys():
                del similarity_matrix[key][j]

        bboxs_left = np.round(bboxs_left).astype(int)
        bboxs_right = np.round(bboxs_right).astype(int)
        couple = np.array(couple)
        return bboxs_left, bboxs_right, couple

    def camera(self):
        # Capture frame
        if len(self.cap) == 1:
            ret, dual_frame = self.cap[0].read()
            ll = time.localtime(time.time())
            timestamp = ll.tm_hour * 10000 + ll.tm_min * 100 + ll.tm_sec
            dual_height = dual_frame.shape[0]
            dual_width = dual_frame.shape[1]
            left_frame, right_frame = dual_frame[:, :int(dual_width / 2)], dual_frame[:, int(dual_width / 2):dual_width]
        elif len(self.cap) == 2:
            ret, left_frame = self.cap[0].read()
            ret, right_frame = self.cap[1].read()
            ll = time.localtime(time.time())
            timestamp = ll.tm_hour * 10000 + ll.tm_min * 100 + ll.tm_sec
            dual_height = left_frame.shape[0]
            dual_width = left_frame.shape[1] * 2
            dual_frame = np.zeros((dual_height, dual_width, 3), np.uint8)
            dual_frame[:, :int(dual_width / 2)] = left_frame[:, :]
            dual_frame[:, int(dual_width / 2):] = right_frame[:, :]
            dual_frame = cv2.UMat(dual_frame)

        bboxs_left, bboxs_right, couple = self.binocular_distance_measurement(left_frame, right_frame)

        matched = 0
        for i in range(bboxs_left.shape[0]):
            for j in range(couple.shape[0]):
                if i == couple[j][0]:
                    matched += 1
                    coupled_right = int(couple[j][1])
                    # print(coupledRight)
                    distance = couple[j][2]
                    variance = couple[j][4]
                    # print(distance)
                    r = couple[j][3]
                    # p = couple[j][4]

                    # # Kalman filtering
                    # if self.former_couples is not None and self.former_couples.shape[0] >= matched:
                    #     # print('未通过卡尔曼滤波：', distance)
                    #     former_distance = self.former_couples[j][2]
                    #     former_variance = self.former_couples[j][4]
                    #     distance = former_distance + (former_variance / (former_variance + variance)) * (
                    #             distance - former_distance)
                    #     # update variance and distance
                    #     couple[j][4] = (variance / (former_variance + variance) * former_variance) ** 0.5
                    #     couple[j][2] = distance
                    #     # print('通过卡尔曼滤波后：', distance)
                    # # else:
                    # #     history_variance = variance

        self.former_bboxs_left, self.former_bboxs_right, self.former_couple = bboxs_left, bboxs_right, couple
        self.couples = couple
        self.faces['Left'], self.faces['Right'] = bboxs_left, bboxs_right
        self.binocular_frame = dual_frame
        self.left_frame = left_frame
        self.right_frame = right_frame
        self.timestamp = timestamp

        return self.faces, self.couples, self.left_frame, self.right_frame, self.timestamp

    def __del__(self):
        if len(self.cap) == 1:
            self.cap[0].release()
        elif len(self.cap) == 2:
            self.cap[0].release()
            self.cap[1].release()


if __name__ == '__main__':
    # Presentation UI
    cv2.namedWindow('Left_frame', 0)
    cv2.moveWindow("Left_frame", 0, 0)
    cv2.resizeWindow('Left_frame', 500, 500)
    cv2.namedWindow('Right_frame', 0)
    cv2.moveWindow("Right_frame", 520, 0)
    cv2.resizeWindow('Right_frame', 500, 500)

    # cam = binocular_camera([0, 2])
    cam = binocular_camera([1])

    f = open('.\\binocular_data_1520_1520\\1400.txt', mode='w')
    x = 0
    while x <= 300:
        faces, couples, left_frame, right_frame, timestamp = cam.camera()
        x += 1
        print(x)
        # print(timestamp)
        for i in range(faces['Left'].shape[0]):
            cv2.rectangle(left_frame, (faces['Left'][i][0], faces['Left'][i][1]),
                          (faces['Left'][i][2], faces['Left'][i][3]),
                          (0, 0, 255), 2)
            for j in range(couples.shape[0]):
                if couples[j][0] == i:
                    distance = couples[j][2]
                    d = 0
                    # f.write(str(d) + '\n')
                    jj = int(couples[j][1])
                    cv2.putText(left_frame, str(format(distance * 0.001, '0.3f')) + 'm',
                                (faces['Left'][i][0], faces['Left'][i][1] - 30),
                                cv2.FONT_HERSHEY_COMPLEX, 5, (0, 0, 255), 5)
                    f.write(str(d) + ' ' + str(faces['Left'][i][0]) + ' ' + str(faces['Left'][i][2]) + ' ' + str(faces['Right'][jj][0]) + ' ' + str(faces['Right'][jj][2]) +'\n')
                    cv2.rectangle(right_frame, (faces['Right'][jj][0], faces['Right'][jj][1]),
                                  (faces['Right'][jj][2], faces['Right'][jj][3]),
                                  (0, 0, 255), 5)

        cv2.imshow('Left_frame', left_frame)
        cv2.imshow('Right_frame', right_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    f.close()
