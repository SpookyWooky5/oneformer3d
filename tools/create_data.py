# Copyright (c) OpenMMLab. All rights reserved.
import argparse
from os import path as osp

# from indoor_converter import create_indoor_info_file
# from update_infos_to_v2 import update_pkl_infos

import indoor_converter as indoor
from update_infos_to_v2 import update_pkl_infos


def scannet_data_prep(root_path, info_prefix, out_dir, workers):
    """Prepare the info file for scannet dataset.

    Args:
        root_path (str): Path of dataset root.
        info_prefix (str): The prefix of info filenames.
        out_dir (str): Output directory of the generated info file.
        workers (int): Number of threads to be used.
    """
    indoor.create_indoor_info_file(
        root_path, info_prefix, out_dir, workers=workers)
    info_train_path = osp.join(out_dir, f'{info_prefix}_infos_train.pkl')
    info_val_path = osp.join(out_dir, f'{info_prefix}_infos_val.pkl')
    info_test_path = osp.join(out_dir, f'{info_prefix}_infos_test.pkl')
    update_pkl_infos('scannet', out_dir=out_dir, pkl_path=info_train_path)
    update_pkl_infos('scannet', out_dir=out_dir, pkl_path=info_val_path)
    update_pkl_infos('scannet', out_dir=out_dir, pkl_path=info_test_path)


def s3dis_data_prep(root_path, info_prefix, out_dir, workers):
    """Prepare the info file for s3dis dataset.

    Args:
        root_path (str): Path of dataset root.
        info_prefix (str): The prefix of info filenames.
        out_dir (str): Output directory of the generated info file.
        workers (int): Number of threads to be used.
    """
    indoor.create_indoor_info_file(
        root_path, info_prefix, out_dir, workers=workers)
    splits = [f'Area_{i}' for i in [1, 2, 3, 4, 5, 6]]
    for split in splits:
        filename = osp.join(out_dir, f'{info_prefix}_infos_{split}.pkl')
        update_pkl_infos('s3dis', out_dir=out_dir, pkl_path=filename)


parser = argparse.ArgumentParser(description='Data converter arg parser')
parser.add_argument('dataset', metavar='kitti', help='name of the dataset')
parser.add_argument(
    '--root-path',
    type=str,
    default='./data/kitti',
    help='specify the root path of dataset')
parser.add_argument(
    '--out-dir',
    type=str,
    default='./data/kitti',
    required=False,
    help='name of info pkl')
parser.add_argument('--extra-tag', type=str, default='kitti')
parser.add_argument(
    '--workers', type=int, default=4, help='number of threads to be used')
args = parser.parse_args()

if __name__ == '__main__':
    from mmdet3d.utils import register_all_modules
    register_all_modules()

    if args.dataset in ('scannet', 'scannet200'):
        scannet_data_prep(
            root_path=args.root_path,
            info_prefix=args.extra_tag,
            out_dir=args.out_dir,
            workers=args.workers)
    elif args.dataset == 's3dis':
        s3dis_data_prep(
            root_path=args.root_path,
            info_prefix=args.extra_tag,
            out_dir=args.out_dir,
            workers=args.workers)
    else:
        raise NotImplementedError(f'Don\'t support {args.dataset} dataset.')
