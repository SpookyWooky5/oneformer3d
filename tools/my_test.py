import os
import sys
import os.path as osp
import argparse

from mmengine.config import Config, ConfigDict, DictAction
from mmengine.registry import RUNNERS
from mmengine.runner import Runner

from mmdet3d.utils import replace_ceph_backend

sys.path.insert(0, './')
