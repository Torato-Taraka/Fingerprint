import numpy as np
import os
import fcs
import time
#调库计算距离
from scipy.spatial.distance import cdist
import binascii
import hashlib
import donna25519 as curve25519

def to_bytes(x):
    return bytes(str(x), 'utf8')

def to_string(x):
    random_seed = 233
    result = ''
    while x > 0:
        result = chr(x % random_seed) + result
        x = x // random_seed
    return result

def int_to_2_string(x):
    x = str(bin(int(x))).replace('0b', '')
    return '0'*(3-len(x)) + x

def get_features(files):
    features_list = {}
    #print(files)
    for file in files:
        #file = files[0]
        #np.genfromtxt(file_path, delimiter, dtype)读取数据
        points = np.genfromtxt(file, delimiter = ',')
        #获取数据总量
        number = len(points)
        #print(number)
            
        #分别计算所有点之间相互的距离
        distance = cdist(points, points)
        #print(distance)
    
        #排序
        distance_sort = np.argsort(distance, axis = 1)
        #print(distance_sort)
            
        #选取距离最近的四个点
        nearest_distance_index = distance_sort[:, 1:5]
        #print(nearest_distance_index)
            
        #取出点坐标
        nearest_points = points[nearest_distance_index]
        #print(nearest_points)
            
        #计算中心点与周围四个点的向量
        vector = []
        for i in range(number):
            vector.append(nearest_points[i] - points[i])
        #print(vector)
                
        #计算距离，角度，并构建特征向量
        #features是最后的特征值
        features = []
        dist_list = []
        for i in range(number):
            #取出与最近四点的距离
            dist = distance[i][nearest_distance_index[i, :]]
            #print(dist)
            dist_list.append(dist)
        #print(dist_list)
        #模块化，相对距离八等份化，方便转为二进制串
        dist_list = np.round((dist_list / np.max(dist_list)) * 7.4)
        """
        #计算距离，角度，并构建特征向量
        #features是最后的特征值
        features = np.zeros(number, dtype = 'int64')
        dist_list = []
        for i in range(number):
            #取出与最近四点的距离
            dist = distance[i][nearest_distance_index[i, :]]
            #模块化，相对距离八等份化，方便转为二进制串
            dist = np.round((dist / np.max(dist)) * 7.4)
            #print(dist)
            dist_list.append(dist)
        #print(dist_list)
        """
        #融合四个距离到特征值
        for i in range(number):
            x = ''
            for j in range(4):
                x = x + int_to_2_string(dist_list[i][j])
            features.append(x)
        #print(features)
            
        #计算角度
        angle_list = []
        for i in range(number):
            angles = []
            #计算每个向量之间的夹角
            for j in range(4):
                for k in range(j+1, 4):
                    #计算点积
                    dot = np.dot(vector[i][j], vector[i][k])
                    #计算模长
                    norm = np.round(np.linalg.norm(vector[i][j]) * np.linalg.norm(vector[i][k]))
                    #求出角度并八等份化
                    angle = np.round(( np.arccos(dot / norm)/ np.pi )* 7.4)
                    angles.append(angle)
            angle_list.append(angles)
        #print(angle_list)
                        
        #六个角度融合到特征值里
        for i in range(number):
            for j in range(6):
                features[i] = features[i] + int_to_2_string(angle_list[i][j])
            features_list[features[i]] = hash(features[i])
        #print(features)
            
    print(len(features_list))
    return features_list

def get_commitment(features_list, k):
    #FCS第一个参数是commitment的长度，第二个参数是threshold阈值
    fuzzy_commitment = fcs.FCS(32 * 8, k)
    commitment_list = []
    for i in features_list:
        commitment_list.append(fuzzy_commitment.commit(binascii.unhexlify(i), to_bytes(features_list[i])))
        
    return fuzzy_commitment, commitment_list

def check(x, template, commitment_list):
    test = to_bytes(x)
    for i in commitment_list:
        if template.verify(i, test):
            return True
    
    return False

def compute_Gi(commitment_list):
    g_list = []
    for i in commitment_list:  
        x = hashlib.sha256(str(i.auxiliar).encode('utf-8')).hexdigest()       
        x = binascii.unhexlify(x)
        private = curve25519.PrivateKey(x)
        public = private.get_public()
        g_list.append(str(hex(int(binascii.hexlify(public.public), 16))).replace('0x',''))
    
    g_list = list(set(g_list))
    
    print(len(g_list))
    return g_list

if __name__ == '__main__':
    for root, dirs, files in os.walk('minutiaes'):
        print("root = ", root)
        print("\ndirs = ", dirs)
        print("\nfiles = \n", files)
        print("________________________________")
  
        x = files[0][:3]
        train_list = []
        temp_list = []
        for file in files:
            if x in file:
                temp_list.append(os.path.join(root, file))
            else:
                train_list.append(temp_list)
                temp_list = []
                x = file[:3]
                temp_list.append(os.path.join(root, file))
        train_list.append(temp_list)
    print("\ntrain files: ", len(train_list) * len(train_list[0]))
    print(train_list)
    print("________________________________")
    
    for k in range(len(train_list)):
        start = time.time()
        features_list = get_features(train_list[k])
        end = time.time()
        print("特征计算用时：{0}s".format(round(end - start, 2)))
    
        start = time.time()
        template, commitment_list = get_commitment(features_list, 5)
        end = time.time()
        print("fuzzy_commitment建立用时：{0}s".format(round(end - start, 3)))
        
        start = time.time()
        g_list = compute_Gi(commitment_list)
        end = time.time()
        print("加密用时：{0}s".format(round(end - start, 3)))
        print("________________________________")
        output_f = open('template{0}.txt'.format(k), 'w')
        for i in g_list:
            output_f.write(str(i) + '\n')
        output_f.close()
                        