import os
import random
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
<<<<<<< HEAD
from tools.colorize_mask import cityscapes_colorize_mask, camvid_colorize_mask, paris_colorize_mask, austin_colorize_mask, road_colorize_mask
=======
from tools.colorize_mask import cityscapes_colorize_mask, camvid_colorize_mask, paris_colorize_mask, austin_colorize_mask
>>>>>>> 60b121b66c11a06ff5e6ff160b220c96fd746bde


def __init_weight(feature, conv_init, norm_layer, bn_eps, bn_momentum,
                  **kwargs):
    for name, m in feature.named_modules():
        # print('name is',name)
        # print('m is',m)
        if isinstance(m, (nn.Conv2d, nn.Conv3d)):
            conv_init(m.weight, **kwargs)
        elif isinstance(m, norm_layer):
            m.eps = bn_eps
            m.momentum = bn_momentum
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)


def init_weight(module_list, conv_init, norm_layer, bn_eps, bn_momentum,
                **kwargs):
    if isinstance(module_list, list):
        for feature in module_list:
            __init_weight(feature, conv_init, norm_layer, bn_eps, bn_momentum,
                          **kwargs)
    else:
        __init_weight(module_list, conv_init, norm_layer, bn_eps, bn_momentum,
                      **kwargs)


def setup_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True


def save_predict(output, gt, img_name, dataset, save_path, output_grey=False, output_color=True, gt_color=False):
    if output_grey:
        output_grey = Image.fromarray(output)
        output_grey.save(os.path.join(save_path, img_name + '.png'))

    if output_color:
        if dataset == 'cityscapes':
            output_color = cityscapes_colorize_mask(output)
        elif dataset == 'camvid':
            output_color = camvid_colorize_mask(output)
        elif dataset == 'paris':
            output_color = paris_colorize_mask(output)
        elif dataset == 'austin':
            output_color = austin_colorize_mask(output)
<<<<<<< HEAD
        elif dataset == 'road':
            output_color = road_colorize_mask(output)
=======
>>>>>>> 60b121b66c11a06ff5e6ff160b220c96fd746bde
        output_color.save(os.path.join(save_path, str(img_name) + '_colour.png'))

    if gt_color:
        if dataset == 'cityscapes':
            gt_color = cityscapes_colorize_mask(gt)
        elif dataset == 'camvid':
            gt_color = camvid_colorize_mask(gt)
        elif dataset == 'paris':
            gt_color = paris_colorize_mask(gt)
        elif dataset == 'austin':
            gt_color = austin_colorize_mask(gt)
<<<<<<< HEAD
        elif dataset == 'road':
            gt_color = road_colorize_mask(gt)

        gt_color.save(os.path.join(save_path, str(img_name) + '_gt.png'))
=======

        gt_color.save(os.path.join(save_path, img_name + '_gt.png'))
>>>>>>> 60b121b66c11a06ff5e6ff160b220c96fd746bde


def netParams(model):
    """
    computing total network parameters
    args:
       model: model
    return: the number of parameters
    """
    total_paramters = 0
    for parameter in model.parameters():
        i = len(parameter.size())
        p = 1
        for j in range(i):
            p *= parameter.size(j)
        total_paramters += p

    return total_paramters
