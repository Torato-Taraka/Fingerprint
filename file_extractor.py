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
    train_features_list = []
    
    for i in range(len(train_list)):
        print("\n这是第{0}组数据:".format(i))
        time_cost = 0
        
        start = time.time()
        temp_list = []
        for j in range(len(train_list[i])):
            temp_list.append(processminutiae.get_features([train_list[i][j]]))
        train_features_list.append(temp_list)
        end = time.time()
        time_cost += round(end - start, 2)
        print("特征计算用时：{0}s".format(round(end - start, 2)))
        print("________________________________")
    
    
    true_false = 0
    false_true = 0
    for i in range(len(train_list)):
        start = time.time()
        temp_dict = {}
        for j in range(6):
            
            temp_dict.update(train_features_list[i][j])

        template, commitment_list = processminutiae.get_commitment(temp_dict, 7)
        #end = time.time()
        #time_cost += round(end - start, 3)
        #print("fuzzy_commitment建立用时：{0}s".format(round(end - start, 3)))
        
        all_time.append(time_cost)
        
        for j in range(len(train_list[i])):
            true = 0
            for k, v in train_features_list[i][j].items():
                if processminutiae.check(k, template, commitment_list):
                    true += 1
            print(true, len(train_features_list[i][j]))
            if true / len(train_features_list[i][j]) < 0.5:
                true_false += 1
            print("\n第{0}个正确指纹检验完毕".format(j))
        
        for j in range(len(train_list)):
            if i != j:
                true = 0
                for k, v in train_features_list[j][(i+j) % len(train_list[j])].items():
                    if processminutiae.check(k, template, commitment_list):
                        true += 1
                print(true, len(train_features_list[j][(i+j) % len(train_list[j])]))
                if true / len(train_features_list[j][(i+j) % len(train_list[j])]) >= 0.5:
                    false_true += 1
            print("\n第{0}个错误指纹检验完毕".format(j))
        print("________________________________")
    
    total_compare = len(train_list) * (len(train_list) - 1 + len(train_list[0]))
    should_true = len(train_list) * len(train_list[0])
    should_false = total_compare - should_true
    print("\nFRR = {0}".format(true_false / should_true) )
    print("\nFAR = {0}".format(false_true / should_false) )
        
    #print("\n平均用时：{0}(+/-{1}) s\n".format(np.mean(all_time), np.std(all_time)))