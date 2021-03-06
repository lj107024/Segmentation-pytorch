import os
import pickle
from torch.utils import data
from dataset.cityscapes import CityscapesDataSet, CityscapesTrainInform, CityscapesValDataSet, CityscapesTestDataSet
from dataset.camvid import CamVidDataSet, CamVidValDataSet, CamVidTrainInform, CamVidTestDataSet
from dataset.paris import ParisDataSet, ParisValDataSet, ParisTrainInform, ParisTestDataSet
from dataset.austin import AustinDataSet, AustinValDataSet, AustinTrainInform, AustinTestDataSet
from dataset.road import RoadDataSet, RoadValDataSet, RoadTrainInform, RoadTestDataSet


def build_dataset_train(dataset, input_size, batch_size, train_type, random_scale, random_mirror, num_workers):
    # data_dir = '/media/ding/Data/datasets/camvid/camvid/'
    # data_dir = '/media/ding/Data/datasets/cityscapes/'
    data_dir = os.path.join('/media/ding/Data/datasets', dataset)
    dataset_list = os.path.join(dataset + '_train_list.txt')
    train_data_list = os.path.join(data_dir, dataset + '_' + train_type + '_list.txt')
    val_data_list = os.path.join(data_dir, dataset + '_val' + '_list.txt')
    inform_data_file = os.path.join('./dataset/inform/', dataset + '_inform.pkl')

    # inform_data_file collect the information of mean, std and weigth_class
    if not os.path.isfile(inform_data_file):
        print("%s is not found" % (inform_data_file))
        if dataset == "cityscapes":
            dataCollect = CityscapesTrainInform(data_dir, 19, train_set_file=dataset_list,
                                                inform_data_file=inform_data_file)
        elif dataset == 'camvid':
            dataCollect = CamVidTrainInform(data_dir, 11, train_set_file=dataset_list,
                                            inform_data_file=inform_data_file)
        elif dataset == 'paris':
            dataCollect = ParisTrainInform(data_dir, 3, train_set_file=dataset_list,
                                            inform_data_file=inform_data_file)
        elif dataset == 'austin':
            dataCollect = AustinTrainInform(data_dir, 2, train_set_file=dataset_list,
                                           inform_data_file=inform_data_file)
        elif dataset == 'road':
            dataCollect = RoadTrainInform(data_dir, 2, train_set_file=dataset_list,
                                            inform_data_file=inform_data_file)
        else:
            raise NotImplementedError(
                "This repository now supports two datasets: cityscapes and camvid, %s is not included" % dataset)

        datas = dataCollect.collectDataAndSave()
        if datas is None:
            print("error while pickling data. Please check.")
            exit(-1)
    else:
        print("find file: ", str(inform_data_file))
        datas = pickle.load(open(inform_data_file, "rb"))

    if dataset == "cityscapes":

        trainLoader = data.DataLoader(
            CityscapesDataSet(data_dir, train_data_list, crop_size=input_size, scale=random_scale,
                              mirror=random_mirror, mean=datas['mean']),
            batch_size=batch_size, shuffle=True, num_workers=num_workers,
            pin_memory=True, drop_last=True)

        valLoader = data.DataLoader(
            CityscapesValDataSet(data_dir, val_data_list, f_scale=0.5, mean=datas['mean']),
            batch_size=1, shuffle=True, num_workers=num_workers, pin_memory=True,
            drop_last=True)

        return datas, trainLoader, valLoader

    elif dataset == "camvid":

        trainLoader = data.DataLoader(
            CamVidDataSet(data_dir, train_data_list, crop_size=input_size, scale=random_scale,
                          mirror=random_mirror, mean=datas['mean']),
            batch_size=batch_size, shuffle=True, num_workers=num_workers,
            pin_memory=True, drop_last=True)

        valLoader = data.DataLoader(
            CamVidValDataSet(data_dir, val_data_list, f_scale=1, mean=datas['mean']),
            batch_size=1, shuffle=True, num_workers=num_workers, pin_memory=True)

        return datas, trainLoader, valLoader

    elif dataset == "paris":

        trainLoader = data.DataLoader(
            ParisDataSet(data_dir, train_data_list, crop_size=input_size, scale=random_scale,
                          mirror=random_mirror, mean=datas['mean'], std=datas['std']),
            batch_size=batch_size, shuffle=True, num_workers=num_workers,
            pin_memory=True, drop_last=True)

        valLoader = data.DataLoader(
            ParisValDataSet(data_dir, val_data_list, f_scale=1, mean=datas['mean'], std=datas['std']),
            batch_size=1, shuffle=True, num_workers=num_workers, pin_memory=True)

        return datas, trainLoader, valLoader

    elif dataset == "austin":

        trainLoader = data.DataLoader(
            AustinDataSet(data_dir, train_data_list, crop_size=input_size, scale=random_scale,
                         mirror=random_mirror, mean=datas['mean']),
            batch_size=batch_size, shuffle=True, num_workers=num_workers,
            pin_memory=True, drop_last=True)

        valLoader = data.DataLoader(
            AustinValDataSet(data_dir, val_data_list, f_scale=1, mean=datas['mean']),
            batch_size=1, shuffle=True, num_workers=num_workers, pin_memory=True)

        return datas, trainLoader, valLoader

    elif dataset == "road":

        trainLoader = data.DataLoader(
            RoadDataSet(data_dir, train_data_list, crop_size=input_size, scale=random_scale,
                          mirror=random_mirror, mean=datas['mean']),
            batch_size=batch_size, shuffle=True, num_workers=num_workers,
            pin_memory=True, drop_last=True)

        valLoader = data.DataLoader(
            RoadValDataSet(data_dir, val_data_list, f_scale=1, mean=datas['mean']),
            batch_size=1, shuffle=True, num_workers=num_workers, pin_memory=True)

        return datas, trainLoader, valLoader


def build_dataset_test(dataset, num_workers, none_gt=False):
    data_dir = os.path.join('/media/ding/Data/datasets', dataset)
    dataset_list = os.path.join(dataset, '_train_list.txt')
    if(dataset == 'cityscapes'):
        test_data_list = os.path.join(data_dir, dataset + '_val' + '_list.txt')
    else:
        test_data_list = os.path.join(data_dir, dataset + '_test' + '_list.txt')
    inform_data_file = os.path.join('./dataset/inform/', dataset + '_inform.pkl')

    # inform_data_file collect the information of mean, std and weigth_class
    if not os.path.isfile(inform_data_file):
        print("%s is not found" % (inform_data_file))
        if dataset == "cityscapes":
            dataCollect = CityscapesTrainInform(data_dir, 19, train_set_file=dataset_list,
                                                inform_data_file=inform_data_file)
        elif dataset == 'camvid':
            dataCollect = CamVidTrainInform(data_dir, 11, train_set_file=dataset_list,
                                            inform_data_file=inform_data_file)
        elif dataset == 'paris':
            dataCollect = ParisTrainInform(data_dir, 3, train_set_file=dataset_list,
                                           inform_data_file=inform_data_file)
        elif dataset == 'austin':
            dataCollect = AustinTrainInform(data_dir, 2, train_set_file=dataset_list,
                                           inform_data_file=inform_data_file)
        elif dataset == 'road':
            dataCollect = RoadTrainInform(data_dir, 2, train_set_file=dataset_list,
                                            inform_data_file=inform_data_file)
        else:
            raise NotImplementedError(
                "This repository now supports two datasets: cityscapes and camvid, %s is not included" % dataset)
        
        datas = dataCollect.collectDataAndSave()
        if datas is None:
            print("error while pickling data. Please check.")
            exit(-1)
    else:
        print("find file: ", str(inform_data_file))
        datas = pickle.load(open(inform_data_file, "rb"))

    if dataset == "cityscapes":
        # for cityscapes, if test on validation set, set none_gt to False
        # if test on the test set, set none_gt to True
        if not none_gt:
            testLoader = data.DataLoader(
                CityscapesTestDataSet(data_dir, test_data_list, mean=datas['mean']),
                batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)
        else:
            test_data_list = os.path.join(data_dir, dataset + '_val' + '_list.txt')
            testLoader = data.DataLoader(
                CityscapesValDataSet(data_dir, test_data_list, mean=datas['mean']),
                batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)

        return datas, testLoader

    elif dataset == "camvid":

        testLoader = data.DataLoader(
            CamVidValDataSet(data_dir, test_data_list, mean=datas['mean']),
            batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)

        return datas, testLoader

    elif dataset == "paris":

        testLoader = data.DataLoader(
            ParisTestDataSet(data_dir, test_data_list, mean=datas['mean']),
            batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)

        return datas, testLoader

    elif dataset == "austin":

        testLoader = data.DataLoader(
            AustinTestDataSet(data_dir, test_data_list, mean=datas['mean']),
            batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)

        return datas, testLoader

    elif dataset == "road":

        testLoader = data.DataLoader(
            RoadTestDataSet(data_dir, test_data_list, mean=datas['mean']),
            batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)

        return datas, testLoader


def build_dataset_sliding_test(dataset, num_workers, none_gt=False):
    data_dir = os.path.join('/media/ding/Data/datasets', dataset)
    dataset_list = os.path.join(dataset, '_train_list.txt')
    if (dataset == 'cityscapes'):
        test_data_list = os.path.join(data_dir, dataset + '_val' + '_list.txt')
    else:
        test_data_list = os.path.join(data_dir, dataset + '_sliding_test' + '_list.txt')
    inform_data_file = os.path.join('./dataset/inform/', dataset + '_inform.pkl')

    # inform_data_file collect the information of mean, std and weigth_class
    if not os.path.isfile(inform_data_file):
        print("%s is not found" % (inform_data_file))
        if dataset == "cityscapes":
            dataCollect = CityscapesTrainInform(data_dir, 19, train_set_file=dataset_list,
                                                inform_data_file=inform_data_file)
        elif dataset == 'camvid':
            dataCollect = CamVidTrainInform(data_dir, 11, train_set_file=dataset_list,
                                            inform_data_file=inform_data_file)
        elif dataset == 'paris':
            dataCollect = ParisTrainInform(data_dir, 3, train_set_file=dataset_list,
                                           inform_data_file=inform_data_file)
        elif dataset == 'austin':
            dataCollect = AustinTrainInform(data_dir, 2, train_set_file=dataset_list,
                                            inform_data_file=inform_data_file)
        elif dataset == 'road':
            dataCollect = RoadTrainInform(data_dir, 2, train_set_file=dataset_list,
                                          inform_data_file=inform_data_file)
        else:
            raise NotImplementedError(
                "This repository now supports two datasets: cityscapes and camvid, %s is not included" % dataset)

        datas = dataCollect.collectDataAndSave()
        if datas is None:
            print("error while pickling data. Please check.")
            exit(-1)
    else:
        print("find file: ", str(inform_data_file))
        datas = pickle.load(open(inform_data_file, "rb"))

    if dataset == "cityscapes":
        # for cityscapes, if test on validation set, set none_gt to False
        # if test on the test set, set none_gt to True
        if not none_gt:
            testLoader = data.DataLoader(
                CityscapesTestDataSet(data_dir, test_data_list, mean=datas['mean']),
                batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)
        else:
            test_data_list = os.path.join(data_dir, dataset + '_val' + '_list.txt')
            testLoader = data.DataLoader(
                CityscapesValDataSet(data_dir, test_data_list, mean=datas['mean']),
                batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)

        return datas, testLoader

    elif dataset == "camvid":

        testLoader = data.DataLoader(
            CamVidValDataSet(data_dir, test_data_list, mean=datas['mean']),
            batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)

        return datas, testLoader

    elif dataset == "paris":

        testLoader = data.DataLoader(
            ParisTestDataSet(data_dir, test_data_list, mean=datas['mean']),
            batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)

        return datas, testLoader

    elif dataset == "austin":

        testLoader = data.DataLoader(
            AustinTestDataSet(data_dir, test_data_list, mean=datas['mean']),
            batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)

        return datas, testLoader

    elif dataset == "road":

        testLoader = data.DataLoader(
            RoadTestDataSet(data_dir, test_data_list, mean=datas['mean']),
            batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)

        return datas, testLoader


