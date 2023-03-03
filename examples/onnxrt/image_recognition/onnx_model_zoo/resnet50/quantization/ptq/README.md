# Evaluate performance of ONNX Runtime(ResNet 50) 
>ONNX runtime quantization is under active development. please use 1.6.0+ to get more quantization support. 

This example load an image classification model from [ONNX Model Zoo](https://github.com/onnx/models) and confirm its accuracy and speed based on [ILSVR2012 validation Imagenet dataset](http://www.image-net.org/challenges/LSVRC/2012/downloads). You need to download this dataset yourself.

### Environment
onnx: 1.9.0
onnxruntime: 1.10.0

### Prepare model
Download model from [ONNX Model Zoo](https://github.com/onnx/models)

```shell
wget https://github.com/onnx/models/raw/main/vision/classification/resnet/model/resnet50-v1-12.onnx
```

### Quantization

Quantize model with QLinearOps:

```bash
bash run_tuning.sh --input_model=path/to/model \  # model path as *.onnx
                   --config=resnet50_v1_5.yaml \
                   --output_model=path/to/save
```

Quantize model with QDQ mode:

```bash
bash run_tuning.sh --input_model=path/to/model \  # model path as *.onnx
                   --config=resnet50_v1_5_qdq.yaml \
                   --output_model=path/to/save
```

### Benchmark 

```bash
bash run_benchmark.sh --input_model=path/to/model \  # model path as *.onnx
                      --config=resnet50_v1_5.yaml \
                      --mode=performance # or accuracy
```