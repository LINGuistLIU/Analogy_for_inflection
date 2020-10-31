'''
This script picks out the models with the first five highest accuracies on the dev set,
and deletes all other models.
'''

import os
import sys

def file2dict(fname):
    id2gold = {}
    id2pred = {}
    with open(fname) as f:
        for line in f:
            if 'T-' == line[:2]:
                id, gold = line.strip().split('\t')
                id = int(id.strip().split('-')[1])
                id2gold[id] = gold.strip()
            if 'H-' == line[:2]:
                id, score, pred = line.strip('\n').split('\t')
                id = int(id.strip().split('-')[1])
                id2pred[id] = pred.strip()
    return id2gold, id2pred

def first5accurate(pred_dir):
    file_acc_list = []
    for item in os.listdir(pred_dir):
        if 'dev-' in item:
            if 'last' in item:
                id = 99999999
            elif 'best' in item:
                id = 9999999999999999
            else:
                idpart = item.split('-')[1]
                id = int(idpart.split('.')[0][10:])
            fname = pred_dir + item
            id2gold, id2pred = file2dict(fname)
            correct = 0
            guess = 0
            for k, v in id2gold.items():
                guess += 1
                if v == id2pred[k]:
                    correct += 1
            file_acc_list.append((item, id, round(100*correct/guess, 4)))
    file_acc_list = sorted(file_acc_list, key=lambda x:x[1])
    if len(file_acc_list) <= 5:
        sorted_file_acc_list = sorted(file_acc_list, key=lambda x: x[-1], reverse=True)
        final_list = sorted_file_acc_list
        print('The saved models and acc on dev set:')
    else:
        sorted_file_acc_list = sorted(file_acc_list, key=lambda x:x[-1], reverse=True)
        final_list = sorted_file_acc_list[:5]
        # final_list = []
        # for i in range(0, 5):
        #     candidate = (0, -1)
        #     for j in range(len(file_acc_list)):
        #         if file_acc_list[j][1] > candidate[1]:
        #             candidate = file_acc_list[j]
        #     file_acc_list.remove(candidate)
        #     final_list.append(candidate)
        print('The first five best model and acc on dev set:')
    print(final_list)
    print(final_list[0][-1])
    return final_list

def deletefiles(final_list):
    modelset = set([item[0][4:-4] for item in final_list])
    predset = set([item[0] for item in final_list])
    for item in os.listdir(model_dir):
        if item not in modelset and 'best' not in item and 'last' not in item:
            os.remove(model_dir+item)
    for item in os.listdir(pred_dir):
        if item not in predset and 'best' not in item and 'last' not in item:
            os.remove(pred_dir+item)

if __name__ == '__main__':
    lang = sys.argv[1]
    dirnow=sys.argv[2]

    model_dir = dirnow + '/checkpoints/' + lang + '-models/'
    pred_dir = dirnow + '/checkpoints/' + lang + '-predictions/'

    final_list = first5accurate(pred_dir)
    deletefiles(final_list)

