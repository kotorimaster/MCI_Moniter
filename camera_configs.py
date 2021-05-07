import cv2
import numpy as np



# 左摄像头参数
left_camera_matrix = np.array([[651.0429, 0, 0],
                               [-0.4629, 652.3253, 0],
                               [343.568, 277.2594, 1]])
left_distortion = np.array([[-0.0345, 0.0432, 0.0048, -0.0047, 0]])

# 右摄像头参数
right_camera_matrix = np.array([[649.845853186629, 0, 0],
                                [-1.62285663751384, 650.864752239762, 0],
                                [315.102623472331, 272.461552630242, 1]])
right_distortion = np.array([[-0.0766, 0.2705, 0.0045, -0.0033, 0]])

R = np.array([[0.9999, 0.0105, 0.0025], [-0.0105, 0.9999, 0.0104], [-0.0024, -0.0105, 0.9999]])  # 旋转关系矩阵
T = np.array([59.2444, 0.0442, -0.8184])  # 平移关系向量

size = (640, 480)  # 图像尺寸

# 进行立体更正
R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(left_camera_matrix, left_distortion,
                                                                  right_camera_matrix, right_distortion, size, R,
                                                                  T)
# 计算更正map
left_map1, left_map2 = cv2.initUndistortRectifyMap(left_camera_matrix, left_distortion, R1, P1, size, cv2.CV_16SC2)
right_map1, right_map2 = cv2.initUndistortRectifyMap(right_camera_matrix, right_distortion, R2, P2, size, cv2.CV_16SC2)