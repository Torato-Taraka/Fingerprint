import os
import minutiae
import processminutiae
import time
import numpy as np

#minutiae.minutiae_extract("imgs\\", "minutiaes\\")

true_list = []
false_list = []
for root, dirs, files in os.walk('minutiaes'):
    print("root = ", root)
    print("\ndirs = ", dirs)
    print("\nfiles = \n", files)
    print("________________________________")
    
    test_true_list = []
    for file in files:
        if file[4] == '8' :
            test_true_list.append([os.path.join(root, file)])
            files.remove(file)
    print("\ntest true files: ", len(test_true_list))
    print("________________________________")
    
    test_false_list = []
    for file in files:
        if file[4] == '9' :
            test_false_list.append([os.path.join(root, file)])
            files.remove(file)
    print("\ntest false files: ", len(test_false_list))
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
    print("________________________________")
    
    all_time = []
    
    for i in range(len(train_list)):
        print("\n这是第{0}组数据：\n".format(i))
        time_cost = 0
        
        start = time.time()
        train_features_list = processminutiae.get_features(train_list[i])
        test_true_features_list = processminutiae.get_features(test_true_list[i])
        test_false_features_list = processminutiae.get_features(test_false_list[i])
        end = time.time()
        time_cost += round(end - start, 2)
        print("特征计算用时：{0}s".format(round(end - start, 2)))
    
        start = time.time()
        template, commitment_list = processminutiae.get_commitment(train_features_list, 1)
        end = time.time()
        time_cost += round(end - start, 3)
        print("fuzzy_commitment建立用时：{0}s".format(round(end - start, 3)))
        
        all_time.append(time_cost)
        
        true = 0
        for i, j in test_true_features_list.items():
            if processminutiae.check(i, template, commitment_list):
                true += 1
                continue
        print("真样本匹配率：", true / len(test_true_features_list))
        true_list.append(true / len(test_true_features_list))
        
        false = 0
        for i, j in test_false_features_list.items():
            if processminutiae.check(i, template, commitment_list):
                false += 1
                continue
        print("假样本匹配率", false / len(test_false_features_list))
        false_list.append(false / len(test_false_features_list))
        
        print("________________________________")
        
        
    print("\n平均用时：{0}(+/-{1}) s\n".format(np.mean(all_time), np.std(all_time)))
    print("\n正确率为： \n", true_list)
    print("\n错误率为： \n", false_list)
    
    total_sample = len(true_list) + len(false_list)
    
    FAR = 0
    FRR = 0
    for i in true_list:
        if i < 0.5:
            FRR+=1
    for i in false_list:
        if i > 0.5:
            FAR+=1
    FAR = FAR / total_sample
    FRR = FRR / total_sample
    print("\nFAR = {0}%".format(FAR * 100))
    print("\nFRR = {0}%".format(FRR * 100))
    