# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint:disable=redefined-outer-name,logging-format-interpolation

import cv2
import onnx
import logging
import argparse
import numpy as np
from PIL import Image
from scipy import special

logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt = '%m/%d/%Y %H:%M:%S',
                    level = logging.WARN)
logger.info("Evaluating ONNXRuntime full precision accuracy and performance:")
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    '--data_path',
    type=str,
    help="Path of COCO dataset, it contains val2017 and annotations subfolder"
)
parser.add_argument(
    '--model_path',
    type=str,
    help="Pre-trained model on onnx file"
)
parser.add_argument(
    '--benchmark',
    action='store_true', \
    default=False
)
parser.add_argument(
    '--tune',
    action='store_true', \
    default=False,
    help="whether quantize the model"
)
parser.add_argument(
    '--config',
    type=str,
    help="config yaml path"
)
parser.add_argument(
    '--output_model',
    type=str,
    help="output model path"
)
parser.add_argument(
    '--mode',
    type=str,
    help="benchmark mode of performance or accuracy"
)
args = parser.parse_args()

def get_anchors(anchors_path, tiny=False):
    '''loads the anchors from a file'''
    with open(anchors_path) as f:
        anchors = f.readline()
    anchors = np.array(anchors.split(','), dtype=np.float32)
    return anchors.reshape(3, 3, 2)

IMAGE_INPUT_SZIE = 416
ANCHORS = get_anchors("./yolov4_anchors.txt")
STRIDES = np.array([8, 16, 32])
XYSCALE = [1.2, 1.1, 1.05]

class Dataloader:
    def __init__(self, root, img_dir='val2017', \
            anno_dir='annotations/instances_val2017.json'):
        import json
        import os
        import numpy as np
        from pycocotools.coco import COCO
        from neural_compressor.experimental.metric.coco_label_map import category_map
        self.batch_size = 1
        self.image_list = []
        img_path = os.path.join(root, img_dir)
        anno_path = os.path.join(root, anno_dir)
        coco = COCO(anno_path)
        img_ids = coco.getImgIds()
        cat_ids = coco.getCatIds()
        for idx, img_id in enumerate(img_ids):
            img_info = {}
            bboxes = []
            labels = []
            ids = []
            img_detail = coco.loadImgs(img_id)[0]
            ids.append(img_detail['file_name'].encode('utf-8'))
            pic_height = img_detail['height']
            pic_width = img_detail['width']

            ann_ids = coco.getAnnIds(imgIds=img_id,catIds=cat_ids)
            anns = coco.loadAnns(ann_ids)
            for ann in anns:
                bbox = ann['bbox']
                if len(bbox) == 0:
                    continue
                bboxes.append([bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1]+bbox[3]])
                labels.append(category_map[ann['category_id']].encode('utf8'))
            img_file = os.path.join(img_path, img_detail['file_name'])
            if not os.path.exists(img_file) or len(bboxes) == 0:
                continue

            if filter and not filter(None, bboxes):
                continue
            label = [np.array([bboxes]), np.array([labels]), np.zeros((1,0)), np.array([img_detail['file_name'].encode('utf-8')])]
            with Image.open(img_file) as image:
                image = image.convert('RGB')
                image, label = self.preprocess((image, label))
            self.image_list.append((image, label))

    def __iter__(self):
        for item in self.image_list:
            yield item

    def preprocess(self, sample):
        image, label = sample
        image = np.array(image)
        ih = iw = IMAGE_INPUT_SZIE
        h, w, _ = image.shape

        scale = min(iw/w, ih/h)
        nw, nh = int(scale * w), int(scale * h)
        image_resized = cv2.resize(image, (nw, nh))

        image_padded = np.full(shape=[ih, iw, 3], fill_value=128.0)
        dw, dh = (iw - nw) // 2, (ih-nh) // 2
        image_padded[dh:nh+dh, dw:nw+dw, :] = image_resized
        image_padded = image_padded / 255.

        gt_boxes, str_labels, int_labels, image_ids = label
        return image_padded[np.newaxis, ...].astype(np.float32), \
            (gt_boxes, str_labels, int_labels, image_ids, (h, w))

class Post:
    def __init__(self) -> None:
        self.ANCHORS = ANCHORS
        self.STRIDES = STRIDES
        self.XYSCALE = XYSCALE
        self.input_size = IMAGE_INPUT_SZIE

    def __call__(self, sample):
        preds, labels = sample
        labels = labels[0]

        pred_bbox = postprocess_bbbox(preds, self.ANCHORS, self.STRIDES, self.XYSCALE)
        bboxes = postprocess_boxes(pred_bbox, labels[4], self.input_size, 0.25)
        if len(bboxes) == 0:
            return (np.zeros((1,0,4)), np.zeros((1,0)), np.zeros((1,0))), labels[:4]
        bboxes_ = np.array(nms(bboxes, 0.213, method='nms'))
        bboxes, scores, classes = bboxes_[:, :4], bboxes_[:, 4], bboxes_[:, 5]

        bboxes = np.reshape(bboxes, (1, -1, 4))
        classes = np.reshape(classes, (1, -1)).astype('int64') + 1
        scores = np.reshape(scores, (1, -1))
        return (bboxes, classes, scores), labels[:4]

def postprocess_bbbox(pred_bbox, ANCHORS, STRIDES, XYSCALE=[1,1,1]):
    '''define anchor boxes'''
    for i, pred in enumerate(pred_bbox):
        conv_shape = pred.shape
        output_size = conv_shape[1]
        conv_raw_dxdy = pred[:, :, :, :, 0:2]
        conv_raw_dwdh = pred[:, :, :, :, 2:4]
        xy_grid = np.meshgrid(np.arange(output_size), np.arange(output_size))
        xy_grid = np.expand_dims(np.stack(xy_grid, axis=-1), axis=2)

        xy_grid = np.tile(np.expand_dims(xy_grid, axis=0), [1, 1, 1, 3, 1])
        xy_grid = xy_grid.astype(np.float)

        pred_xy = ((special.expit(conv_raw_dxdy) * XYSCALE[i]) - 0.5 * (XYSCALE[i] - 1) + xy_grid) * STRIDES[i]
        pred_wh = (np.exp(conv_raw_dwdh) * ANCHORS[i])
        pred[:, :, :, :, 0:4] = np.concatenate([pred_xy, pred_wh], axis=-1)

    pred_bbox = [np.reshape(x, (-1, np.shape(x)[-1])) for x in pred_bbox]
    pred_bbox = np.concatenate(pred_bbox, axis=0)
    return pred_bbox

def postprocess_boxes(pred_bbox, org_img_shape, input_size, score_threshold):
    '''remove boundary boxs with a low detection probability'''
    valid_scale=[0, np.inf]
    pred_bbox = np.array(pred_bbox)

    pred_xywh = pred_bbox[:, 0:4]
    pred_conf = pred_bbox[:, 4]
    pred_prob = pred_bbox[:, 5:]

    # # (1) (x, y, w, h) --> (xmin, ymin, xmax, ymax)
    pred_coor = np.concatenate([pred_xywh[:, :2] - pred_xywh[:, 2:] * 0.5,
                                pred_xywh[:, :2] + pred_xywh[:, 2:] * 0.5], axis=-1)
    # # (2) (xmin, ymin, xmax, ymax) -> (xmin_org, ymin_org, xmax_org, ymax_org)
    org_h, org_w = org_img_shape
    resize_ratio = min(input_size / org_w, input_size / org_h)

    dw = (input_size - resize_ratio * org_w) / 2
    dh = (input_size - resize_ratio * org_h) / 2

    pred_coor[:, 0::2] = 1.0 * (pred_coor[:, 0::2] - dw) / resize_ratio
    pred_coor[:, 1::2] = 1.0 * (pred_coor[:, 1::2] - dh) / resize_ratio

    # # (3) clip some boxes that are out of range
    pred_coor = np.concatenate([np.maximum(pred_coor[:, :2], [0, 0]),
                                np.minimum(pred_coor[:, 2:], [org_w - 1, org_h - 1])], axis=-1)
    invalid_mask = np.logical_or((pred_coor[:, 0] > pred_coor[:, 2]), (pred_coor[:, 1] > pred_coor[:, 3]))
    pred_coor[invalid_mask] = 0

    # # (4) discard some invalid boxes
    bboxes_scale = np.sqrt(np.multiply.reduce(pred_coor[:, 2:4] - pred_coor[:, 0:2], axis=-1))
    scale_mask = np.logical_and((valid_scale[0] < bboxes_scale), (bboxes_scale < valid_scale[1]))

    # # (5) discard some boxes with low scores
    classes = np.argmax(pred_prob, axis=-1)
    scores = pred_conf * pred_prob[np.arange(len(pred_coor)), classes]
    score_mask = scores > score_threshold
    mask = np.logical_and(scale_mask, score_mask)
    coors, scores, classes = pred_coor[mask], scores[mask], classes[mask]
    return np.concatenate([coors, scores[:, np.newaxis], classes[:, np.newaxis]], axis=-1)

def bboxes_iou(boxes1, boxes2):
    '''calculate the Intersection Over Union value'''
    boxes1 = np.array(boxes1)
    boxes2 = np.array(boxes2)

    boxes1_area = (boxes1[..., 2] - boxes1[..., 0]) * (boxes1[..., 3] - boxes1[..., 1])
    boxes2_area = (boxes2[..., 2] - boxes2[..., 0]) * (boxes2[..., 3] - boxes2[..., 1])

    left_up       = np.maximum(boxes1[..., :2], boxes2[..., :2])
    right_down    = np.minimum(boxes1[..., 2:], boxes2[..., 2:])

    inter_section = np.maximum(right_down - left_up, 0.0)
    inter_area    = inter_section[..., 0] * inter_section[..., 1]
    union_area    = boxes1_area + boxes2_area - inter_area
    ious          = np.maximum(1.0 * inter_area / union_area, np.finfo(np.float32).eps)

    return ious

def nms(bboxes, iou_threshold, sigma=0.3, method='nms'):
    """
    :param bboxes: (xmin, ymin, xmax, ymax, score, class)

    Note: soft-nms, https://arxiv.org/pdf/1704.04503.pdf
          https://github.com/bharatsingh430/soft-nms
    """
    classes_in_img = list(set(bboxes[:, 5]))
    best_bboxes = []

    for cls in classes_in_img:
        cls_mask = (bboxes[:, 5] == cls)
        cls_bboxes = bboxes[cls_mask]

        while len(cls_bboxes) > 0:
            max_ind = np.argmax(cls_bboxes[:, 4])
            best_bbox = cls_bboxes[max_ind]
            best_bboxes.append(best_bbox)
            cls_bboxes = np.concatenate([cls_bboxes[: max_ind], cls_bboxes[max_ind + 1:]])
            iou = bboxes_iou(best_bbox[np.newaxis, :4], cls_bboxes[:, :4])
            weight = np.ones((len(iou),), dtype=np.float32)

            assert method in ['nms', 'soft-nms']

            if method == 'nms':
                iou_mask = iou > iou_threshold
                weight[iou_mask] = 0.0

            if method == 'soft-nms':
                weight = np.exp(-(1.0 * iou ** 2 / sigma))

            cls_bboxes[:, 4] = cls_bboxes[:, 4] * weight
            score_mask = cls_bboxes[:, 4] > 0.
            cls_bboxes = cls_bboxes[score_mask]

    return best_bboxes

if __name__ == "__main__":
    model = onnx.load(args.model_path)
    dataloader = Dataloader(args.data_path)
    if args.benchmark:
        from neural_compressor.experimental import Benchmark, common
        evaluator = Benchmark(args.config)
        evaluator.model = common.Model(model)
        evaluator.b_dataloader = dataloader
        evaluator.postprocess = common.Postprocess(Post)
        evaluator(args.mode)

    if args.tune:
        from neural_compressor import options
        from neural_compressor.experimental import Quantization, common
        options.onnxrt.graph_optimization.level = 'ENABLE_BASIC'

        quantize = Quantization(args.config)
        quantize.model = common.Model(model)
        quantize.eval_dataloader = dataloader
        quantize.calib_dataloader = dataloader
        quantize.postprocess = common.Postprocess(Post)
        q_model = quantize()
        q_model.save(args.output_model)
        
