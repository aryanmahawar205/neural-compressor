
Validated Models
======
Intel® Neural Compressor validated examples with multiple compression techniques. The typical examples link can be found in [example tables](https://github.com/intel/neural-compressor/blob/master/examples/README.md), and the performance/accuracy results is available here.

1. [Validated Quantization Examples](#Validated-Quantization-Examples)

    1.1. [TensorFlow Models with Intel TensorFlow 2.13.0](#tensorflow-models-with-Intel-tensorflow-2130)

    1.2. [PyTorch Models with Torch 2.0.1+cpu in PTQ Mode](#pytorch-models-with-torch-201cpu-in-ptq-mode)

    1.3. [PyTorch Models with Torch 2.0.1+cpu in QAT Mode](#pytorch-models-with-torch-201cpu-in-qat-mode)

    1.4. [PyTorch Models with Intel® Extension for PyTorch* 2.0.1+cpu](#pytorch-models-with-intel-extension-for-pytorch-201cpu)

    1.5. [PyTorch Models with Torch 2.0.1+cpu in WOQ Mode](#pytorch-models-with-torch-201cpu-in-woq-mode)

    1.6. [ONNX Models with ONNX Runtime 1.15.1](#onnx-models-with-onnx-runtime-1151)

    1.7. [ONNX Models with ONNX Runtime 1.15.0 in WOQ Mode](#onnx-models-with-onnx-runtime-1150-in-woq-mode)

2. [Validated Pruning Examples](#Validated-Pruning-Examples)

3. [Validated Knowledge Distillation Examples](#Validated-Knowledge-Distillation-Examples)

4. [Validated ONNX QDQ INT8 Models on Multiple Hardware through ONNX Runtime](#validated-onnx-qdq-int8-models-on-multiple-hardware-through-onnx-runtime)

## Validated Quantization Examples

System summary: Test by Intel on 09/01/2023. 1-node, 1x Intel(R) Xeon(R) Platinum 8480+ @3.8GHz, 56 cores/socket, HT On, Turbo On, Total Memory 256GB (16x16GB DDR5 4800 MT/s [4800 MT/s]), BIOS 3A14.TEL2P1, microcode 0x2b0001b0,   
CentOS Stream 8, gcc (GCC) 8.5.0 20210514 (Red Hat 8.5.0-10), DL Models, Frameworks: TensorFlow/ONNXRT/PyTorch, Datatype: FP32/INT8/BF16.  
Using 1 socket, 4 cores/instance, 14 instances and batch size 1 to benchmark most of the model.  
Using 1 socket, 56 cores/instance, 1 instance and batch size 1 for some large models performance measurement.   

Performance varies by use, configuration and other factors.  
For more complete information about performance and benchmark results, visit www.intel.com/benchmarks

### TensorFlow Models with Intel TensorFlow 2.13.0

<table>
<thead>
  <tr>
    <th rowspan="2">Model</th>
    <th rowspan="2">Example</th>
    <th colspan="3">Accuracy</th>
    <th colspan="3">Performance 1s4c14ins1bs<br>Throughput(samples/sec)</th>
  </tr>
  <tr>
    <th>INT8</th>
    <th>FP32</th>
    <th>Accuracy Ratio<br>[(INT8-FP32)/FP32]</th>
    <th>INT8</th>
    <th>FP32</th>
    <th>Performance Ratio<br>[INT8/FP32]</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>ResNet50 v1.0</td>
    <td>pb</td>
    <td>74.12%</td>
    <td>74.27%</td>
    <td>-0.21%</td>
    <td>2914.42</td>
    <td>621.91</td>
    <td>4.69x</td>
  </tr>
  <tr>
    <td>ResNet50 v1.5</td>
    <td>pb</td>
    <td>76.23%</td>
    <td>76.46%</td>
    <td>-0.31%</td>
    <td>2160.07</td>
    <td>545.47</td>
    <td>3.96x</td>
  </tr>
  <tr>
    <td>ResNet101</td>
    <td>pb</td>
    <td>77.50%</td>
    <td>76.45%</td>
    <td>1.37%</td>
    <td>1508.97</td>
    <td>428.02</td>
    <td>3.53x</td>
  </tr>
  <tr>
    <td>Inception V1</td>
    <td>pb</td>
    <td>70.44%</td>
    <td>69.74%</td>
    <td>1.01%</td>
    <td>3290.75</td>
    <td>1229.78</td>
    <td>2.68x</td>
  </tr>
  <tr>
    <td>Inception V2</td>
    <td>pb</td>
    <td>74.38%</td>
    <td>73.97%</td>
    <td>0.57%</td>
    <td>2404.57</td>
    <td>1048.49</td>
    <td>2.29x</td>
  </tr>
  <tr>
    <td>Inception V3</td>
    <td>pb</td>
    <td>76.71%</td>
    <td>76.75%</td>
    <td>-0.05%</td>
    <td>1669.09</td>
    <td>500.95</td>
    <td>3.33x</td>
  </tr>
  <tr>
    <td>Inception V4</td>
    <td>pb</td>
    <td>80.18%</td>
    <td>80.27%</td>
    <td>-0.11%</td>
    <td>1073.14</td>
    <td>245.13</td>
    <td>4.38x</td>
  </tr>
  <tr>
    <td>Inception ResNet V2</td>
    <td>pb</td>
    <td>80.34%</td>
    <td>80.40%</td>
    <td>-0.07%</td>
    <td>374.52</td>
    <td>172.06</td>
    <td>2.18x</td>
  </tr>
  <tr>
    <td>MobileNet V1</td>
    <td>pb</td>
    <td>71.78%</td>
    <td>70.96%</td>
    <td>1.16%</td>
    <td>5478.88</td>
    <td>1756.33</td>
    <td>3.12x</td>
  </tr>
  <tr>
    <td>MobileNet V2</td>
    <td>pb</td>
    <td>72.52%</td>
    <td>71.76%</td>
    <td>1.07%</td>
    <td>4133.01</td>
    <td>1748.06</td>
    <td>2.36x</td>
  </tr>
  <tr>
    <td>VGG16</td>
    <td>pb</td>
    <td>72.64%</td>
    <td>70.89%</td>
    <td>2.47%</td>
    <td>1534.50</td>
    <td>236.62</td>
    <td>6.49x</td>
  </tr>
  <tr>
    <td>VGG19</td>
    <td>pb</td>
    <td>72.69%</td>
    <td>71.01%</td>
    <td>2.37%</td>
    <td>1377.40</td>
    <td>197.77</td>
    <td>6.96x</td>
  </tr>
  <tr>
    <td>ResNetV2 50</td>
    <td>pb</td>
    <td>70.39%</td>
    <td>69.64%</td>
    <td>1.07%</td>
    <td>1125.32</td>
    <td>656.38</td>
    <td>1.71x</td>
  </tr>
  <tr>
    <td>ResNetV2 101</td>
    <td>pb</td>
    <td>72.62%</td>
    <td>71.87%</td>
    <td>1.04%</td>
    <td>709.50</td>
    <td>367.00</td>
    <td>1.93x</td>
  </tr>
  <tr>
    <td>ResNetV2 152</td>
    <td>pb</td>
    <td>73.11%</td>
    <td>72.37%</td>
    <td>1.03%</td>
    <td>497.24</td>
    <td>265.34</td>
    <td>1.87x</td>
  </tr>
  <tr>
    <td>Densenet 121</td>
    <td>pb</td>
    <td>73.59%</td>
    <td>72.89%</td>
    <td>0.97%</td>
    <td>557.67</td>
    <td>456.61</td>
    <td>1.22x</td>
  </tr>
  <tr>
    <td>Densenet 161</td>
    <td>pb</td>
    <td>76.35%</td>
    <td>76.29%</td>
    <td>0.08%</td>
    <td>353.18</td>
    <td>235.35</td>
    <td>1.50x</td>
  </tr>
  <tr>
    <td>Densenet 169</td>
    <td>pb</td>
    <td>74.34%</td>
    <td>74.65%</td>
    <td>-0.41%</td>
    <td>435.44</td>
    <td>385.73</td>
    <td>1.13x</td>
  </tr>
  <tr>
    <td>EfficientNet B0</td>
    <td>ckpt</td>
    <td>76.15%</td>
    <td>76.76%</td>
    <td>-0.79%</td>
    <td>786.55</td>
    <td>723.69</td>
    <td>1.09x</td>
  </tr>
  <tr>
    <td>SSD ResNet50 V1</td>
    <td>pb</td>
    <td>37.88%</td>
    <td>38.00%</td>
    <td>-0.31%</td>
    <td>130.09</td>
    <td>30.78</td>
    <td>4.23x</td>
  </tr>
  <tr>
    <td>SSD MobileNet V1</td>
    <td>pb</td>
    <td>22.98%</td>
    <td>23.13%</td>
    <td>-0.64%</td>
    <td>1291.02</td>
    <td>683.50</td>
    <td>1.89x</td>
  </tr>
  <tr>
    <td>SSD ResNet50 v1</td>
    <td>ckpt</td>
    <td>37.89%</td>
    <td>38.00%</td>
    <td>-0.30%</td>
    <td>127.30</td>
    <td>27.63</td>
    <td>4.61x</td>
  </tr>
  <tr>
    <td>SSD MobileNet v1</td>
    <td>ckpt</td>
    <td>22.96%</td>
    <td>23.13%</td>
    <td>-0.72%</td>
    <td>1295.23</td>
    <td>453.76</td>
    <td>2.85x</td>
  </tr>
  <tr>
    <td>SSD ResNet34</td>
    <td>pb</td>
    <td>21.70%</td>
    <td>22.09%</td>
    <td>-1.76%</td>
    <td>242.91</td>
    <td>14.03</td>
    <td>17.31x</td>
  </tr>
  <tr>
    <td>Faster R-CNN Inception ResNet V2</td>
    <td>pb</td>
    <td>37.47%</td>
    <td>38.31%</td>
    <td>-2.18%</td>
    <td>5.44</td>
    <td>3.02</td>
    <td>1.80x</td>
  </tr>
  <tr>
    <td>Faster R-CNN Inception ResNet V2</td>
    <td>SavedModel</td>
    <td>37.79%</td>
    <td>38.31%</td>
    <td>-1.34%</td>
    <td>5.43</td>
    <td>3.00</td>
    <td>1.81x</td>
  </tr>
  <tr>
    <td>Faster R-CNN ResNet101</td>
    <td>pb</td>
    <td>30.32%</td>
    <td>30.39%</td>
    <td>-0.23%</td>
    <td>166.37</td>
    <td>23.54</td>
    <td>7.07x</td>
  </tr>
  <tr>
    <td>Faster R-CNN ResNet101</td>
    <td>SavedModel</td>
    <td>30.33%</td>
    <td>30.39%</td>
    <td>-0.20%</td>
    <td>151.54</td>
    <td>18.58</td>
    <td>8.16x</td>
  </tr>
  <tr>
    <td>Faster R-CNN ResNet50</td>
    <td>pb</td>
    <td>26.64%</td>
    <td>26.59%</td>
    <td>0.21%</td>
    <td>173.33</td>
    <td>28.58</td>
    <td>6.07x</td>
  </tr>
  <tr>
    <td>YOLOv3</td>
    <td>pb</td>
    <td>82.13%</td>
    <td>82.35%</td>
    <td>-0.28%</td>
    <td>230.69</td>
    <td>88.35</td>
    <td>2.61x</td>
  </tr>
  <tr>
    <td>BERT large SQuAD</td>
    <td>pb</td>
    <td>92.36</td>
    <td>92.99</td>
    <td>-0.67%</td>
    <td>59.76</td>
    <td>17.71</td>
    <td>3.37x</td>
  </tr>
  <tr>
    <td>BERT large SQuAD (ONNX Model Zoo)</td>
    <td>pb</td>
    <td>92.26</td>
    <td>92.98</td>
    <td>-0.78%</td>
    <td>41.65</td>
    <td>16.14</td>
    <td>2.58x</td>
  </tr>
  <tr>
    <td>BERT base MRPC</td>
    <td>ckpt</td>
    <td>87.01%</td>
    <td>86.52%</td>
    <td>0.57%</td>
    <td>416.57</td>
    <td>177.06</td>
    <td>2.35x</td>
  </tr>
  <tr>
    <td>Transformer LT</td>
    <td>pb</td>
    <td>25.68</td>
    <td>25.86</td>
    <td>-0.67%</td>
    <td>41.19</td>
    <td>21.94</td>
    <td>1.88x</td>
  </tr>
  <tr>
    <td>Transformer lt MLPerf</td>
    <td>pb</td>
    <td>27.27</td>
    <td>27.17</td>
    <td>0.39%</td>
    <td>9.77</td>
    <td>4.51</td>
    <td>2.17x</td>
  </tr>
  <tr>
    <td>Wide Deep large DS</td>
    <td>pb</td>
    <td>77.75%</td>
    <td>77.67%</td>
    <td>0.10%</td>
    <td>75552.26</td>
    <td>50803.82</td>
    <td>1.49x</td>
  </tr>
</tbody>
</table>

<table>
<thead>
  <tr>
    <th rowspan="2">Model</th>
    <th rowspan="2">Example</th>
    <th colspan="3">Accuracy</th>
    <th colspan="3">Performance 1s56c1ins1bs<br>Throughput(samples/sec)</th>
  </tr>
  <tr>
    <th>INT8</th>
    <th>FP32</th>
    <th>Accuracy Ratio<br>[(INT8-FP32)/FP32]</th>
    <th>INT8</th>
    <th>FP32</th>
    <th>Performance Ratio<br>[INT8/FP32]</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Mask R-CNN Inception V2</td>
    <td>pb</td>
    <td>28.60%</td>
    <td>28.73%</td>
    <td>-0.44%</td>
    <td>41.96</td>
    <td>25.66</td>
    <td>1.64x</td>
  </tr>
  <tr>
    <td>Mask R-CNN Inception V2</td>
    <td>ckpt</td>
    <td>28.60%</td>
    <td>28.73%</td>
    <td>-0.44%</td>
    <td>41.56</td>
    <td>24.35</td>
    <td>1.71x</td>
  </tr>
</tbody>
</table>

### PyTorch Models with Torch 2.0.1+cpu in PTQ Mode

<table>
<thead>
  <tr>
    <th rowspan="2">Model</th>
    <th rowspan="2">Example</th>
    <th colspan="3">Accuracy</th>
    <th colspan="3">Performance 1s4c14ins1bs<br>Throughput(samples/sec)</th>
  </tr>
  <tr>
    <th>INT8</th>
    <th>FP32</th>
    <th>Accuracy Ratio<br>[(INT8-FP32)/FP32]</th>
    <th>INT8</th>
    <th>FP32</th>
    <th>Performance Ratio<br>[INT8/FP32]</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>ResNet18</td>
    <td>static</td>
    <td>69.61%</td>
    <td>69.76%</td>
    <td>-0.22%</td>
    <td>1673.05</td>
    <td>653.13</td>
    <td>2.56x</td>
  </tr>
  <tr>
    <td>ResNet50</td>
    <td>static</td>
    <td>75.92%</td>
    <td>76.15%</td>
    <td>-0.30%</td>
    <td>1170.62</td>
    <td>329.70</td>
    <td>3.55x</td>
  </tr>
  <tr>
    <td>Inception V3</td>
    <td>static</td>
    <td>69.47%</td>
    <td>69.52%</td>
    <td>-0.07%</td>
    <td>977.08</td>
    <td>335.55</td>
    <td>2.91x</td>
  </tr>
  <tr>
    <td>ResNeSt50</td>
    <td>static</td>
    <td>80.80%</td>
    <td>81.04%</td>
    <td>-0.30%</td>
    <td>404.51</td>
    <td>40.04</td>
    <td>10.10x</td>
  </tr>
  <tr>
    <td>ResNeXt101_32x8d</td>
    <td>static</td>
    <td>78.94%</td>
    <td>79.31%</td>
    <td>-0.46%</td>
    <td>562.16</td>
    <td>109.77</td>
    <td>5.12x</td>
  </tr>
  <tr>
    <td>Efficientnet_b0</td>
    <td>static</td>
    <td>76.89%</td>
    <td>77.67%</td>
    <td>-1.01%</td>
    <td>696.79</td>
    <td>667.27</td>
    <td>1.04x</td>
  </tr>
  <tr>
    <td>Efficientnet_b3</td>
    <td>static</td>
    <td>77.82%</td>
    <td>78.54%</td>
    <td>-0.93%</td>
    <td>508.85</td>
    <td>397.32</td>
    <td>1.28x</td>
  </tr>
  <tr>
    <td>Efficientnet_b7</td>
    <td>static</td>
    <td>73.55%</td>
    <td>73.92%</td>
    <td>-0.50%</td>
    <td>234.87</td>
    <td>149.65</td>
    <td>1.57x</td>
  </tr>
  <tr>
    <td>Peleenet</td>
    <td>static</td>
    <td>71.85%</td>
    <td>72.10%</td>
    <td>-0.35%</td>
    <td>858.18</td>
    <td>588.33</td>
    <td>1.46x</td>
  </tr>
  <tr>
    <td>SE_ResNeXt50_32x4d</td>
    <td>static</td>
    <td>79.03%</td>
    <td>79.08%</td>
    <td>-0.07%</td>
    <td>739.61</td>
    <td>283.60</td>
    <td>2.61x</td>
  </tr>
  <tr>
    <td>YOLO V3</td>
    <td>static</td>
    <td>55.09%</td>
    <td>54.93%</td>
    <td>0.31%</td>
    <td>161.92</td>
    <td>60.48</td>
    <td>2.68x</td>
  </tr>
  <tr>
    <td>SSD ResNet34</td>
    <td>static</td>
    <td>19.52</td>
    <td>19.63</td>
    <td>-0.58%</td>
    <td>141.26</td>
    <td>11.78</td>
    <td>11.99x</td>
  </tr>
  <tr>
    <td>Roberta base MRPC</td>
    <td>static</td>
    <td>92.69%</td>
    <td>93.59%</td>
    <td>-0.96%</td>
    <td>404.62</td>
    <td>174.02</td>
    <td>2.33x</td>
  </tr>
  <tr>
    <td>CamemBERT base MRPC</td>
    <td>static</td>
    <td>88.93%</td>
    <td>89.28%</td>
    <td>-0.39%</td>
    <td>395.08</td>
    <td>171.78</td>
    <td>2.30x</td>
  </tr>
  <tr>
    <td>DistilBERT base MRPC</td>
    <td>static</td>
    <td>89.53%</td>
    <td>90.27%</td>
    <td>-0.82%</td>
    <td>795.98</td>
    <td>341.60</td>
    <td>2.33x</td>
  </tr>
  <tr>
    <td>DistilBERT base MRPC</td>
    <td>dynamic</td>
    <td>90.20%</td>
    <td>90.27%</td>
    <td>-0.07%</td>
    <td>744.78</td>
    <td>343.36</td>
    <td>2.17x</td>
  </tr>
  <tr>
    <td>ALBERT base MRPC</td>
    <td>static</td>
    <td>92.63%</td>
    <td>92.63%</td>
    <td>0.00%</td>
    <td>374.41</td>
    <td>163.39</td>
    <td>2.29x</td>
  </tr>
  <tr>
    <td>Funnel MRPC</td>
    <td>static</td>
    <td>91.60%</td>
    <td>92.25%</td>
    <td>-0.71%</td>
    <td>300.02</td>
    <td>182.21</td>
    <td>1.65x</td>
  </tr>
  <tr>
    <td>Xlm Roberta MRPC</td>
    <td>static</td>
    <td>88.36%</td>
    <td>88.62%</td>
    <td>-0.29%</td>
    <td>399.27</td>
    <td>173.62</td>
    <td>2.30x</td>
  </tr>
  <tr>
    <td>Xlm Roberta MRPC</td>
    <td>dynamic</td>
    <td>88.24%</td>
    <td>88.24%</td>
    <td>0.00%</td>
    <td>385.00</td>
    <td>174.37</td>
    <td>2.21x</td>
  </tr>
  <tr>
    <td>BERT base MRPC</td>
    <td>static</td>
    <td>89.63%</td>
    <td>90.42%</td>
    <td>-0.87%</td>
    <td>407.79</td>
    <td>173.24</td>
    <td>2.35x</td>
  </tr>
  <tr>
    <td>BERT base COLA</td>
    <td>static</td>
    <td>54.51%</td>
    <td>53.39%</td>
    <td>2.10%</td>
    <td>412.12</td>
    <td>172.97</td>
    <td>2.38x</td>
  </tr>
  <tr>
    <td>BERT base STSB</td>
    <td>static</td>
    <td>87.55%</td>
    <td>88.05%</td>
    <td>-0.57%</td>
    <td>413.19</td>
    <td>173.17</td>
    <td>2.39x</td>
  </tr>
  <tr>
    <td>BERT base SST-2</td>
    <td>static</td>
    <td>91.51%</td>
    <td>92.32%</td>
    <td>-0.87%</td>
    <td>409.94</td>
    <td>172.77</td>
    <td>2.37x</td>
  </tr>
  <tr>
    <td>BERT large COLA</td>
    <td>static</td>
    <td>62.84%</td>
    <td>63.35%</td>
    <td>-0.80%</td>
    <td>141.90</td>
    <td>51.55</td>
    <td>2.75x</td>
  </tr>
  <tr>
    <td>BERT base RTE</td>
    <td>static</td>
    <td>72.56%</td>
    <td>72.56%</td>
    <td>0.00%</td>
    <td>401.42</td>
    <td>174.02</td>
    <td>2.31x</td>
  </tr>
  <tr>
    <td>BERT large MRPC</td>
    <td>static</td>
    <td>90.22%</td>
    <td>90.38%</td>
    <td>-0.17%</td>
    <td>139.59</td>
    <td>51.66</td>
    <td>2.70x</td>
  </tr>
  <tr>
    <td>BERT large QNLI</td>
    <td>static</td>
    <td>90.87%</td>
    <td>91.54%</td>
    <td>-0.74%</td>
    <td>406.48</td>
    <td>172.94</td>
    <td>2.35x</td>
  </tr>
  <tr>
    <td>BERT large RTE</td>
    <td>static</td>
    <td>73.29%</td>
    <td>74.01%</td>
    <td>-0.98%</td>
    <td>141.92</td>
    <td>51.41</td>
    <td>2.76x</td>
  </tr>
  <tr>
    <td>BERT large RTE</td>
    <td>dynamic</td>
    <td>71.48%</td>
    <td>74.01%</td>
    <td>-3.41%</td>
    <td>128.46</td>
    <td>51.61</td>
    <td>2.49x</td>
  </tr>
  <tr>
    <td>BERT large SQuAD</td>
    <td>static</td>
    <td>92.27</td>
    <td>93.16</td>
    <td>-0.95%</td>
    <td>37.59</td>
    <td>16.48</td>
    <td>2.28x</td>
  </tr>
  <tr>
    <td>Reformer Crime and Punishment</td>
    <td>static</td>
    <td>1.88</td>
    <td>1.87</td>
    <td>0.23%</td>
    <td>446.29</td>
    <td>398.25</td>
    <td>1.12x</td>
  </tr>
  <tr>
    <td>lvwerra/pegasus-samsum</td>
    <td>static</td>
    <td>42.50</td>
    <td>42.67</td>
    <td>-0.39%</td>
    <td>102.63</td>
    <td>37.94</td>
    <td>2.71x</td>
  </tr>
  <tr>
    <td>T5 Small </td>
    <td>dynamic</td>
    <td>2.65</td>
    <td>3.16</td>
    <td>-16.25%</td>
    <td>770.18</td>
    <td>450.79</td>
    <td>1.71x</td>
  </tr>
</tbody>
</table>

<table>
<thead>
  <tr>
    <th rowspan="2">Model</th>
    <th rowspan="2">Example</th>
    <th colspan="3">Accuracy</th>
    <th colspan="3">Performance 1s56c1ins1bs<br>Throughput(samples/sec)</th>
  </tr>
  <tr>
    <th>INT8</th>
    <th>FP32</th>
    <th>Accuracy Ratio<br>[(INT8-FP32)/FP32]</th>
    <th>INT8</th>
    <th>FP32</th>
    <th>Performance Ratio<br>[INT8/FP32]</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>EleutherAI/gpt-j-6B</td>
    <td>static</td>
    <td>3.36</td>
    <td>2.34</td>
    <td>43.85%</td>
    <td>0.88</td>
    <td>0.28</td>
    <td>3.14x</td>
  </tr>
  <tr>
    <td>openai/whisper-large</td>
    <td>dynamic</td>
    <td>97.07%</td>
    <td>96.96%</td>
    <td>0.12%</td>
    <td>0.59</td>
    <td>0.47</td>
    <td>1.25x</td>
  </tr>
  <tr>
    <td>abeja/gpt-neox-japanese-2.7b</td>
    <td>static</td>
    <td>4.30</td>
    <td>3.52</td>
    <td>22.06%</td>
    <td>1.04</td>
    <td>0.55</td>
    <td>1.90x</td>
  </tr>
</tbody>
</table>

### PyTorch Models with Torch 2.0.1+cpu in QAT Mode

<table>
<thead>
  <tr>
    <th rowspan="2">Model</th>
    <th rowspan="2">Example</th>
    <th colspan="3">Accuracy</th>
    <th colspan="3">Performance 1s4c14ins1bs<br>Throughput(samples/sec)</th>
  </tr>
  <tr>
    <th>INT8</th>
    <th>FP32</th>
    <th>Accuracy Ratio<br>[(INT8-FP32)/FP32]</th>
    <th>INT8</th>
    <th>FP32</th>
    <th>Performance Ratio<br>[INT8/FP32]</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>ResNet18</td>
    <td>static</td>
    <td>69.74%</td>
    <td>69.76%</td>
    <td>-0.03%</td>
    <td>1646.74</td>
    <td>657.43</td>
    <td>2.50x</td>
  </tr>
  <tr>
    <td>ResNet50</td>
    <td>static</td>
    <td>76.05%</td>
    <td>76.15%</td>
    <td>-0.12%</td>
    <td>1098.80</td>
    <td>322.34</td>
    <td>3.41x</td>
  </tr>
  <tr>
    <td>ResNeXt101_32x8d</td>
    <td>static</td>
    <td>79.28%</td>
    <td>79.31%</td>
    <td>-0.04%</td>
    <td>568.02</td>
    <td>109.50</td>
    <td>5.19x</td>
  </tr>
  <tr>
    <td>MobileNet V2</td>
    <td>static</td>
    <td>69.73%</td>
    <td>71.84%</td>
    <td>-2.93%</td>
    <td>1383.77</td>
    <td>761.35</td>
    <td>1.82x</td>
  </tr>
  <tr>
    <td>BERT base MRPC</td>
    <td>static</td>
    <td>89.50%</td>
    <td>90.40%</td>
    <td>-1.00%</td>
    <td>401.83</td>
    <td>173.17</td>
    <td>2.32x</td>
  </tr>
</tbody>
</table>

### PyTorch Models with Intel® Extension for PyTorch* 2.0.1+cpu

<table>
<thead>
  <tr>
    <th rowspan="2">Model</th>
    <th rowspan="2">Example</th>
    <th colspan="3">Accuracy</th>
    <th colspan="3">Performance 1s4c14ins1bs<br>Throughput(samples/sec)</th>
  </tr>
  <tr>
    <th>INT8</th>
    <th>FP32</th>
    <th>Accuracy Ratio<br>[(INT8-FP32)/FP32]</th>
    <th>INT8</th>
    <th>FP32</th>
    <th>Performance Ratio<br>[INT8/FP32]</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>ResNet18</td>
    <td>static</td>
    <td>69.56%</td>
    <td>69.76%</td>
    <td>-0.29%</td>
    <td>5701.04</td>
    <td>1593.88</td>
    <td>3.58x</td>
  </tr>
  <tr>
    <td>ResNet50</td>
    <td>static</td>
    <td>75.98%</td>
    <td>76.15%</td>
    <td>-0.22%</td>
    <td>2090.03</td>
    <td>685.29</td>
    <td>3.05x</td>
  </tr>
  <tr>
    <td>ResNeXt101_32x16d_wsl</td>
    <td>static</td>
    <td>84.04%</td>
    <td>84.17%</td>
    <td>-0.15%</td>
    <td>556.86</td>
    <td>79.42</td>
    <td>7.01x</td>
  </tr>
  <tr>
    <td>SSD ResNet34</td>
    <td>static</td>
    <td>19.93%</td>
    <td>20.00%</td>
    <td>-0.38%</td>
    <td>91.53</td>
    <td>15.62</td>
    <td>5.86x</td>
  </tr>
  <tr>
    <td>bert-large-uncased-whole-word-masking-finetuned-squad</td>
    <td>static</td>
    <td>92.93</td>
    <td>93.16</td>
    <td>-0.25%</td>
    <td>162.94</td>
    <td>22.37</td>
    <td>7.29x</td>
  </tr>
  <tr>
    <td>distilbert-base-uncased-distilled-squad</td>
    <td>static</td>
    <td>86.09</td>
    <td>86.84</td>
    <td>-0.86%</td>
    <td>558.66</td>
    <td>151.25</td>
    <td>3.69x</td>
  </tr>
</tbody>
</table>

<table>
<thead>
  <tr>
    <th rowspan="2">Model</th>
    <th rowspan="2">Example</th>
    <th colspan="3">Accuracy</th>
    <th colspan="3">Performance 1s56c1ins1bs<br>Throughput(samples/sec)</th>
  </tr>
  <tr>
    <th>INT8</th>
    <th>FP32</th>
    <th>Accuracy Ratio<br>[(INT8-FP32)/FP32]</th>
    <th>INT8</th>
    <th>FP32</th>
    <th>Performance Ratio<br>[INT8/FP32]</th>
  </tr>
</thead>
<tbody align="center">
  <tr>
    <td>EleutherAI/gpt-j-6B</td>
    <td>static</td>
    <td>78.70%</td>
    <td>79.20%</td>
    <td>-0.63%</td>
    <td>4.88</td>
    <td>1.57</td>
    <td>3.11x</td>
  </tr>
</tbody>
</table>


### PyTorch Models with Torch 2.0.1+cpu in WOQ Mode

<table class="tg">
<thead>
  <tr>
    <th class="tg-rq3n" rowspan="2">Model name</th>
    <th class="tg-rq3n" rowspan="2">Configuration</th>
    <th class="tg-rq5v">Lambada_openai</th>
    <th class="tg-oo9c">Hellaswag</th>
    <th class="tg-oo9c">Winogrande</th>
    <th class="tg-oo9c">Piqa</th>
    <th class="tg-oo9c" colspan="2">Average<br>[Mean accuracy of previous four tasks]</th>
    <th class="tg-oo9c">Wikitext</th>
  </tr>
  <tr>
    <th class="tg-71nf">Accuracy</th>
    <th class="tg-im72">Accuracy</th>
    <th class="tg-im72">Accuracy</th>
    <th class="tg-im72">Accuracy</th>
    <th class="tg-im72">Accuracy</th>
    <th class="tg-iire">Accuracy Ratio<br>[INT4/FP32]</th>
    <th class="tg-haiz">Word_perplexity</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-rq3n" rowspan="5">EleutherAI/gpt-j-6b</td>
    <td class="tg-rq3n">FP32</td>
    <td class="tg-rq3n">0.6831</td>
    <td class="tg-vxga">0.4954</td>
    <td class="tg-vxga">0.6409</td>
    <td class="tg-vxga">0.7541</td>
    <td class="tg-vxga">0.6434</td>
    <td class="tg-iire">/</td>
    <td class="tg-vxga">10.8816</td>
  </tr>
  <tr>
    <td class="tg-rq3n">GPTQ<br>W4G128Asym</td>
    <td class="tg-rq3n">0.679</td>
    <td class="tg-vxga">0.4895</td>
    <td class="tg-vxga">0.6433</td>
    <td class="tg-vxga">0.7476</td>
    <td class="tg-vxga">0.6399</td>
    <td class="tg-p7cy">0.9945</td>
    <td class="tg-vxga">11.0999</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-vxga">0.6829</td>
    <td class="tg-vxga">0.4923</td>
    <td class="tg-vxga">0.6401</td>
    <td class="tg-vxga">0.7486</td>
    <td class="tg-vxga">0.6410</td>
    <td class="tg-p7cy">0.9963</td>
    <td class="tg-vxga">11.0141</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Sym</td>
    <td class="tg-vxga">0.685</td>
    <td class="tg-vxga">0.4907</td>
    <td class="tg-vxga">0.6361</td>
    <td class="tg-vxga">0.7443</td>
    <td class="tg-vxga">0.6390</td>
    <td class="tg-p7cy">0.9932</td>
    <td class="tg-vxga">11.1498</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Sym</td>
    <td class="tg-vxga">0.6911</td>
    <td class="tg-vxga">0.4899</td>
    <td class="tg-vxga">0.6448</td>
    <td class="tg-vxga">0.7497</td>
    <td class="tg-vxga">0.6439</td>
    <td class="tg-p7cy">1.0008</td>
    <td class="tg-vxga">11.0927</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="3">facebook/opt-6.7b</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.6769</td>
    <td class="tg-vxga">0.5049</td>
    <td class="tg-im72">0.6543</td>
    <td class="tg-im72">0.7628</td>
    <td class="tg-vxga">0.6497</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">12.2862</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.6804</td>
    <td class="tg-folj">0.4984</td>
    <td class="tg-im72">0.6535</td>
    <td class="tg-im72">0.7568</td>
    <td class="tg-vxga">0.6473</td>
    <td class="tg-p7cy">0.9962</td>
    <td class="tg-im72">12.4193</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Sym</td>
    <td class="tg-im72">0.6885</td>
    <td class="tg-vxga">0.4973</td>
    <td class="tg-im72">0.6433</td>
    <td class="tg-im72">0.753</td>
    <td class="tg-vxga">0.6455</td>
    <td class="tg-p7cy">0.9935</td>
    <td class="tg-im72">12.4607</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="2">decapoda-research/llama-7b-hf</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.7361</td>
    <td class="tg-vxga">0.5642</td>
    <td class="tg-im72">0.6709</td>
    <td class="tg-im72">0.7835</td>
    <td class="tg-vxga">0.6887</td>
    <td class="tg-p7cy">/</td>
    <td class="tg-im72">9.4202</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.7244</td>
    <td class="tg-folj">0.5603</td>
    <td class="tg-im72">0.6614</td>
    <td class="tg-im72">0.7835</td>
    <td class="tg-vxga">0.6824</td>
    <td class="tg-p7cy">0.9909</td>
    <td class="tg-im72">9.5881</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="4">decapoda-research/llama-13b-hf</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.7627</td>
    <td class="tg-vxga">0.5911</td>
    <td class="tg-im72">0.7009</td>
    <td class="tg-im72">0.7878</td>
    <td class="tg-vxga">0.7106</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">8.212</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.7518</td>
    <td class="tg-vxga">0.5843</td>
    <td class="tg-im72">0.6961</td>
    <td class="tg-im72">0.7911</td>
    <td class="tg-vxga">0.7058</td>
    <td class="tg-p7cy">0.9932</td>
    <td class="tg-im72">8.4319</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.7572</td>
    <td class="tg-im72">0.5898</td>
    <td class="tg-im72">0.7056</td>
    <td class="tg-im72">0.7894</td>
    <td class="tg-vxga">0.7105</td>
    <td class="tg-p7cy">0.9998</td>
    <td class="tg-im72">8.3429</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Sym</td>
    <td class="tg-im72">0.7596</td>
    <td class="tg-im72">0.5841</td>
    <td class="tg-im72">0.6977</td>
    <td class="tg-im72">0.7905</td>
    <td class="tg-vxga">0.7080</td>
    <td class="tg-p7cy">0.9963</td>
    <td class="tg-im72">8.4916</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="4">decapoda-research/llama-30b-hf</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.7759</td>
    <td class="tg-im72">0.6266</td>
    <td class="tg-im72">0.7277</td>
    <td class="tg-im72">0.8096</td>
    <td class="tg-vxga">0.7350</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">6.2384</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.778</td>
    <td class="tg-im72">0.624</td>
    <td class="tg-im72">0.7269</td>
    <td class="tg-im72">0.8047</td>
    <td class="tg-vxga">0.7334</td>
    <td class="tg-p7cy">0.9979</td>
    <td class="tg-im72">6.4237</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.7706</td>
    <td class="tg-im72">0.6239</td>
    <td class="tg-im72">0.7285</td>
    <td class="tg-im72">0.8058</td>
    <td class="tg-vxga">0.7322</td>
    <td class="tg-p7cy">0.9963</td>
    <td class="tg-im72">6.4697</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Sym</td>
    <td class="tg-im72">0.7836</td>
    <td class="tg-im72">0.6195</td>
    <td class="tg-im72">0.7269</td>
    <td class="tg-im72">0.8047</td>
    <td class="tg-vxga">0.7337</td>
    <td class="tg-p7cy">0.9983</td>
    <td class="tg-im72">6.5604</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="3">meta-llama/Llama-2-7b-chat-hf</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.7058</td>
    <td class="tg-im72">0.5732</td>
    <td class="tg-im72">0.648</td>
    <td class="tg-im72">0.7715</td>
    <td class="tg-vxga">0.6746</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">11.7107</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.6982</td>
    <td class="tg-im72">0.5637</td>
    <td class="tg-im72">0.6527</td>
    <td class="tg-im72">0.7704</td>
    <td class="tg-vxga">0.6713</td>
    <td class="tg-p7cy">0.9950</td>
    <td class="tg-im72">11.9702</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.6953</td>
    <td class="tg-im72">0.5682</td>
    <td class="tg-im72">0.6575</td>
    <td class="tg-im72">0.7758</td>
    <td class="tg-vxga">0.6742</td>
    <td class="tg-p7cy">0.9994</td>
    <td class="tg-im72">11.9317</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="3">meta-llama/Llama-2-7b-hf</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.7392</td>
    <td class="tg-im72">0.567</td>
    <td class="tg-im72">0.6709</td>
    <td class="tg-im72">0.7835</td>
    <td class="tg-vxga">0.6902</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">8.7911</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.7353</td>
    <td class="tg-im72">0.5642</td>
    <td class="tg-im72">0.6622</td>
    <td class="tg-im72">0.7829</td>
    <td class="tg-vxga">0.6862</td>
    <td class="tg-p7cy">0.9942</td>
    <td class="tg-im72">8.9635</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Sym</td>
    <td class="tg-im72">0.7246</td>
    <td class="tg-im72">0.5617</td>
    <td class="tg-im72">0.6756</td>
    <td class="tg-im72">0.7797</td>
    <td class="tg-vxga">0.6854</td>
    <td class="tg-p7cy">0.9931</td>
    <td class="tg-im72">9.2799</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="4">meta-llama/Llama-2-13b-chat-hf</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.7312</td>
    <td class="tg-im72">0.6059</td>
    <td class="tg-im72">0.7103</td>
    <td class="tg-im72">0.7835</td>
    <td class="tg-vxga">0.7077</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">10.2213</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.7273</td>
    <td class="tg-im72">0.6018</td>
    <td class="tg-im72">0.7088</td>
    <td class="tg-im72">0.7742</td>
    <td class="tg-vxga">0.7030</td>
    <td class="tg-p7cy">0.9934</td>
    <td class="tg-im72">2538.083</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.7283</td>
    <td class="tg-im72">0.6053</td>
    <td class="tg-im72">0.7024</td>
    <td class="tg-im72">0.7764</td>
    <td class="tg-vxga">0.7031</td>
    <td class="tg-p7cy">0.9935</td>
    <td class="tg-im72">1889.374</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Sym</td>
    <td class="tg-im72">0.727</td>
    <td class="tg-im72">0.5997</td>
    <td class="tg-im72">0.7024</td>
    <td class="tg-im72">0.778</td>
    <td class="tg-vxga">0.7018</td>
    <td class="tg-p7cy">0.9916</td>
    <td class="tg-im72">2504.497</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="4">meta-llama/Llama-2-13b-hf</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.7677</td>
    <td class="tg-im72">0.5972</td>
    <td class="tg-im72">0.6961</td>
    <td class="tg-im72">0.7878</td>
    <td class="tg-vxga">0.7122</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">7.8984</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.7627</td>
    <td class="tg-im72">0.5933</td>
    <td class="tg-im72">0.689</td>
    <td class="tg-im72">0.7851</td>
    <td class="tg-vxga">0.7075</td>
    <td class="tg-p7cy">0.9934</td>
    <td class="tg-im72">1556.448</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.7675</td>
    <td class="tg-im72">0.5934</td>
    <td class="tg-im72">0.6977</td>
    <td class="tg-im72">0.7856</td>
    <td class="tg-vxga">0.7111</td>
    <td class="tg-p7cy">0.9984</td>
    <td class="tg-im72">1514.927</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Sym</td>
    <td class="tg-im72">0.7566</td>
    <td class="tg-im72">0.5899</td>
    <td class="tg-im72">0.7032</td>
    <td class="tg-im72">0.7856</td>
    <td class="tg-vxga">0.7088</td>
    <td class="tg-p7cy">0.9953</td>
    <td class="tg-im72">1374.728</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="2">bigscience/bloom-7b1</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.5764</td>
    <td class="tg-im72">0.4628</td>
    <td class="tg-im72">0.6456</td>
    <td class="tg-im72">0.7269</td>
    <td class="tg-vxga">0.6029</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">30.6438</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Sym</td>
    <td class="tg-im72">0.5799</td>
    <td class="tg-im72">0.4542</td>
    <td class="tg-im72">0.6361</td>
    <td class="tg-im72">0.7312</td>
    <td class="tg-vxga">0.6004</td>
    <td class="tg-p7cy">0.9957</td>
    <td class="tg-im72">32.0626</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="2">bigscience/bloomz-7b1</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.5593</td>
    <td class="tg-im72">0.4789</td>
    <td class="tg-im72">0.6527</td>
    <td class="tg-im72">0.7628</td>
    <td class="tg-vxga">0.6134</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">51.7432</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.5525</td>
    <td class="tg-im72">0.4731</td>
    <td class="tg-im72">0.6504</td>
    <td class="tg-im72">0.7617</td>
    <td class="tg-vxga">0.6094</td>
    <td class="tg-p7cy">0.9935</td>
    <td class="tg-im72">52.7828</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="4">databricks/dolly-v1-6b</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.6866</td>
    <td class="tg-im72">0.5098</td>
    <td class="tg-im72">0.6433</td>
    <td class="tg-im72">0.7622</td>
    <td class="tg-im72">0.6505</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">11.3242</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.6878</td>
    <td class="tg-im72">0.5058</td>
    <td class="tg-im72">0.6393</td>
    <td class="tg-im72">0.7633</td>
    <td class="tg-im72">0.6491</td>
    <td class="tg-iire">0.9978</td>
    <td class="tg-im72">11.5514</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.6864</td>
    <td class="tg-im72">0.5084</td>
    <td class="tg-im72">0.6519</td>
    <td class="tg-im72">0.7568</td>
    <td class="tg-im72">0.6509</td>
    <td class="tg-iire">1.0006</td>
    <td class="tg-im72">11.4728</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Sym</td>
    <td class="tg-im72">0.6876</td>
    <td class="tg-im72">0.5045</td>
    <td class="tg-im72">0.6433</td>
    <td class="tg-im72">0.7541</td>
    <td class="tg-im72">0.6474</td>
    <td class="tg-iire">0.9952</td>
    <td class="tg-im72">11.6474</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="2">databricks/dolly-v2-7b</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.6379</td>
    <td class="tg-im72">0.5282</td>
    <td class="tg-im72">0.614</td>
    <td class="tg-im72">0.7448</td>
    <td class="tg-im72">0.6312</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">16.161</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.6377</td>
    <td class="tg-im72">0.5228</td>
    <td class="tg-im72">0.5991</td>
    <td class="tg-im72">0.7448</td>
    <td class="tg-im72">0.6261</td>
    <td class="tg-iire">0.9919</td>
    <td class="tg-im72">16.4096</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="4">EleutherAI/gpt-neo-2.7b</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.6224</td>
    <td class="tg-im72">0.4271</td>
    <td class="tg-im72">0.577</td>
    <td class="tg-im72">0.722</td>
    <td class="tg-im72">0.5871</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">13.9359</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.6123</td>
    <td class="tg-im72">0.4227</td>
    <td class="tg-im72">0.5738</td>
    <td class="tg-im72">0.7203</td>
    <td class="tg-im72">0.5823</td>
    <td class="tg-iire">0.9917</td>
    <td class="tg-im72">14.3377</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.615</td>
    <td class="tg-im72">0.4259</td>
    <td class="tg-im72">0.5714</td>
    <td class="tg-im72">0.7247</td>
    <td class="tg-im72">0.5843</td>
    <td class="tg-iire">0.9951</td>
    <td class="tg-im72">14.2083</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Sym</td>
    <td class="tg-im72">0.6154</td>
    <td class="tg-im72">0.4208</td>
    <td class="tg-im72">0.5777</td>
    <td class="tg-im72">0.7198</td>
    <td class="tg-im72">0.5834</td>
    <td class="tg-iire">0.9937</td>
    <td class="tg-im72">14.3121</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="3">EleutherAI/gpt-neox-20b</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.7233</td>
    <td class="tg-im72">0.5359</td>
    <td class="tg-im72">0.6614</td>
    <td class="tg-im72">0.7753</td>
    <td class="tg-im72">0.6740</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">9.195</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.7186</td>
    <td class="tg-im72">0.5328</td>
    <td class="tg-im72">0.6535</td>
    <td class="tg-im72">0.7699</td>
    <td class="tg-im72">0.6687</td>
    <td class="tg-iire">0.9922</td>
    <td class="tg-im72">9.3463</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.7268</td>
    <td class="tg-im72">0.533</td>
    <td class="tg-im72">0.659</td>
    <td class="tg-im72">0.7715</td>
    <td class="tg-im72">0.6726</td>
    <td class="tg-iire">0.9979</td>
    <td class="tg-im72">9.2897</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="2">mosaicml/mpt-7b</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.7056</td>
    <td class="tg-im72">0.5718</td>
    <td class="tg-im72">0.6859</td>
    <td class="tg-im72">0.7927</td>
    <td class="tg-im72">0.6890</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">9.9324</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.7006</td>
    <td class="tg-im72">0.5655</td>
    <td class="tg-im72">0.6803</td>
    <td class="tg-im72">0.7965</td>
    <td class="tg-im72">0.6857</td>
    <td class="tg-iire">0.9952</td>
    <td class="tg-im72">10.1515</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="2">mosaicml/mpt-7b-chat</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.655</td>
    <td class="tg-im72">0.5752</td>
    <td class="tg-im72">0.6748</td>
    <td class="tg-im72">0.7845</td>
    <td class="tg-im72">0.6724</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">13.5951</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.6472</td>
    <td class="tg-im72">0.5716</td>
    <td class="tg-im72">0.6685</td>
    <td class="tg-im72">0.784</td>
    <td class="tg-im72">0.6678</td>
    <td class="tg-iire">0.9932</td>
    <td class="tg-im72">13.8539</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="2">mosaicml/mpt-7b-instruct</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.6918</td>
    <td class="tg-im72">0.5819</td>
    <td class="tg-im72">0.678</td>
    <td class="tg-im72">0.7927</td>
    <td class="tg-im72">0.6861</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">10.8863</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.6864</td>
    <td class="tg-im72">0.5765</td>
    <td class="tg-im72">0.6827</td>
    <td class="tg-im72">0.7873</td>
    <td class="tg-im72">0.6832</td>
    <td class="tg-iire">0.9958</td>
    <td class="tg-im72">11.1451</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="2">mosaicml/mpt-7b-storywriter</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.693</td>
    <td class="tg-im72">0.5477</td>
    <td class="tg-im72">0.663</td>
    <td class="tg-im72">0.784</td>
    <td class="tg-im72">0.6719</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">9.9125</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.6854</td>
    <td class="tg-im72">0.5443</td>
    <td class="tg-im72">0.6661</td>
    <td class="tg-im72">0.7813</td>
    <td class="tg-im72">0.6693</td>
    <td class="tg-iire">0.9961</td>
    <td class="tg-im72">10.1137</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="4">tiiuae/falcon-rw-7b</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.6604</td>
    <td class="tg-im72">0.5419</td>
    <td class="tg-im72">0.6598</td>
    <td class="tg-im72">0.7753</td>
    <td class="tg-im72">0.6594</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">11.7616</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.6484</td>
    <td class="tg-im72">0.5369</td>
    <td class="tg-im72">0.6575</td>
    <td class="tg-im72">0.7807</td>
    <td class="tg-im72">0.6559</td>
    <td class="tg-iire">0.9947</td>
    <td class="tg-im72">11.9411</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.6571</td>
    <td class="tg-im72">0.5398</td>
    <td class="tg-im72">0.6582</td>
    <td class="tg-im72">0.7764</td>
    <td class="tg-im72">0.6579</td>
    <td class="tg-iire">0.9978</td>
    <td class="tg-im72">11.8809</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Sym</td>
    <td class="tg-im72">0.652</td>
    <td class="tg-im72">0.535</td>
    <td class="tg-im72">0.6575</td>
    <td class="tg-im72">0.7682</td>
    <td class="tg-im72">0.6532</td>
    <td class="tg-iire">0.9906</td>
    <td class="tg-im72">12.0048</td>
  </tr>
  <tr>
    <td class="tg-vxga" rowspan="3">tiiuae/falcon-7b-instruct</td>
    <td class="tg-vxga">FP32</td>
    <td class="tg-im72">0.6437</td>
    <td class="tg-im72">0.5177</td>
    <td class="tg-im72">0.6669</td>
    <td class="tg-im72">0.7824</td>
    <td class="tg-im72">0.6527</td>
    <td class="tg-iire">/</td>
    <td class="tg-im72">14.5053</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G128Asym</td>
    <td class="tg-im72">0.6301</td>
    <td class="tg-im72">0.5142</td>
    <td class="tg-im72">0.6654</td>
    <td class="tg-im72">0.7835</td>
    <td class="tg-im72">0.6483</td>
    <td class="tg-iire">0.9933</td>
    <td class="tg-im72">14.8146</td>
  </tr>
  <tr>
    <td class="tg-vxga">GPTQ<br>W4G32Asym</td>
    <td class="tg-im72">0.6377</td>
    <td class="tg-im72">0.517</td>
    <td class="tg-im72">0.6598</td>
    <td class="tg-im72">0.7807</td>
    <td class="tg-im72">0.6488</td>
    <td class="tg-iire">0.9941</td>
    <td class="tg-im72">14.6953</td>
  </tr>
</tbody>
</table>


### ONNX Models with ONNX Runtime 1.15.1

<table>
<thead>
  <tr>
    <th rowspan="2">Model</th>
    <th rowspan="2">Example</th>
    <th colspan="3">Accuracy</th>
    <th colspan="3">Performance 1s4c14ins1bs<br>Throughput(samples/sec)</th>
  </tr>
  <tr>
    <th>INT8</th>
    <th>FP32</th>
    <th>Accuracy Ratio<br>[(INT8-FP32)/FP32]</th>
    <th>INT8</th>
    <th>FP32</th>
    <th>Performance Ratio<br>[INT8/FP32]</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>ResNet50 V1.5</td>
    <td>qlinearops</td>
    <td>72.16%</td>
    <td>72.29%</td>
    <td>-0.19%</td>
    <td>1566.70</td>
    <td>724.89</td>
    <td>2.16x</td>
  </tr>
  <tr>
    <td>ResNet50 V1.5</td>
    <td>qdq</td>
    <td>72.14%</td>
    <td>72.29%</td>
    <td>-0.22%</td>
    <td>1567.15</td>
    <td>716.57</td>
    <td>2.19x</td>
  </tr>
  <tr>
    <td>ResNet50 V1.5 MLPerf</td>
    <td>qlinearops</td>
    <td>76.11%</td>
    <td>76.46%</td>
    <td>-0.46%</td>
    <td>1414.92</td>
    <td>718.25</td>
    <td>1.97x</td>
  </tr>
  <tr>
    <td>ResNet50 V1.5 MLPerf</td>
    <td>qdq</td>
    <td>76.13%</td>
    <td>76.46%</td>
    <td>-0.44%</td>
    <td>1459.45</td>
    <td>721.54</td>
    <td>2.02x</td>
  </tr>
  <tr>
    <td>ResNet50 V1.5 (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>74.82%</td>
    <td>74.99%</td>
    <td>-0.22%</td>
    <td>1593.71</td>
    <td>753.89</td>
    <td>2.11x</td>
  </tr>
  <tr>
    <td>ResNet50 V1.5 (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>74.82%</td>
    <td>74.99%</td>
    <td>-0.23%</td>
    <td>1582.24</td>
    <td>752.38</td>
    <td>2.10x</td>
  </tr>
  <tr>
    <td>MobileNet V2</td>
    <td>qlinearops</td>
    <td>65.49%</td>
    <td>66.89%</td>
    <td>-2.09%</td>
    <td>7139.93</td>
    <td>4289.29</td>
    <td>1.66x</td>
  </tr>
  <tr>
    <td>MobileNet V2</td>
    <td>qdq</td>
    <td>65.49%</td>
    <td>66.89%</td>
    <td>-2.10%</td>
    <td>7335.80</td>
    <td>4080.31</td>
    <td>1.80x</td>
  </tr>
  <tr>
    <td>MobileNet V2 (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>68.38%</td>
    <td>69.48%</td>
    <td>-1.59%</td>
    <td>7236.84</td>
    <td>4299.29</td>
    <td>1.68x</td>
  </tr>
  <tr>
    <td>MobileNet V2 (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>68.38%</td>
    <td>69.48%</td>
    <td>-1.59%</td>
    <td>6842.58</td>
    <td>4496.44</td>
    <td>1.52x</td>
  </tr>
  <tr>
    <td>VGG16</td>
    <td>qlinearops</td>
    <td>66.56%</td>
    <td>66.69%</td>
    <td>-0.19%</td>
    <td>591.43</td>
    <td>178.91</td>
    <td>3.31x</td>
  </tr>
  <tr>
    <td>VGG16</td>
    <td>qdq</td>
    <td>66.59%</td>
    <td>66.69%</td>
    <td>-0.15%</td>
    <td>614.91</td>
    <td>183.79</td>
    <td>3.35x</td>
  </tr>
  <tr>
    <td>VGG16 (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>72.33%</td>
    <td>72.40%</td>
    <td>-0.09%</td>
    <td>590.04</td>
    <td>182.90</td>
    <td>3.23x</td>
  </tr>
  <tr>
    <td>VGG16 (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>72.33%</td>
    <td>72.40%</td>
    <td>-0.09%</td>
    <td>614.75</td>
    <td>179.93</td>
    <td>3.42x</td>
  </tr>
  <tr>
    <td>MobileNet V3 MLPerf</td>
    <td>qlinearops</td>
    <td>75.56%</td>
    <td>75.74%</td>
    <td>-0.24%</td>
    <td>5703.81</td>
    <td>2578.80</td>
    <td>2.21x</td>
  </tr>
  <tr>
    <td>MobileNet V3 MLPerf</td>
    <td>qdq</td>
    <td>75.56%</td>
    <td>75.74%</td>
    <td>-0.24%</td>
    <td>5610.37</td>
    <td>2603.41</td>
    <td>2.16x</td>
  </tr>
  <tr>
    <td>ShuffleNet V2 (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>66.09%</td>
    <td>66.36%</td>
    <td>-0.41%</td>
    <td>6689.57</td>
    <td>3690.63</td>
    <td>1.81x</td>
  </tr>
  <tr>
    <td>ShuffleNet V2 (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>66.09%</td>
    <td>66.36%</td>
    <td>-0.41%</td>
    <td>5692.38</td>
    <td>3758.23</td>
    <td>1.51x</td>
  </tr>
  <tr>
    <td>GoogleNet (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>67.71%</td>
    <td>67.79%</td>
    <td>-0.12%</td>
    <td>1792.52</td>
    <td>1111.26</td>
    <td>1.61x</td>
  </tr>
  <tr>
    <td>GoogleNet (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>67.73%</td>
    <td>67.79%</td>
    <td>-0.09%</td>
    <td>1821.10</td>
    <td>1104.52</td>
    <td>1.65x</td>
  </tr>
  <tr>
    <td>SqueezeNet (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>56.54%</td>
    <td>56.87%</td>
    <td>-0.57%</td>
    <td>9472.72</td>
    <td>5582.40</td>
    <td>1.70x</td>
  </tr>
  <tr>
    <td>SqueezeNet (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>56.54%</td>
    <td>56.87%</td>
    <td>-0.57%</td>
    <td>9861.50</td>
    <td>5566.72</td>
    <td>1.77x</td>
  </tr>
  <tr>
    <td>CaffeNet (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>56.21%</td>
    <td>56.30%</td>
    <td>-0.16%</td>
    <td>3348.37</td>
    <td>1141.01</td>
    <td>2.93x</td>
  </tr>
  <tr>
    <td>CaffeNet (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>56.25%</td>
    <td>56.30%</td>
    <td>-0.09%</td>
    <td>3509.70</td>
    <td>1142.19</td>
    <td>3.07x</td>
  </tr>
  <tr>
    <td>AlexNet (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>54.73%</td>
    <td>54.79%</td>
    <td>-0.10%</td>
    <td>2426.58</td>
    <td>987.34</td>
    <td>2.46x</td>
  </tr>
  <tr>
    <td>AlexNet (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>54.71%</td>
    <td>54.79%</td>
    <td>-0.14%</td>
    <td>2208.63</td>
    <td>1016.53</td>
    <td>2.17x</td>
  </tr>
  <tr>
    <td>ZFNet (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>55.84%</td>
    <td>55.96%</td>
    <td>-0.21%</td>
    <td>930.06</td>
    <td>532.61</td>
    <td>1.75x</td>
  </tr>
  <tr>
    <td>ZFNet (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>55.86%</td>
    <td>55.96%</td>
    <td>-0.18%</td>
    <td>919.83</td>
    <td>417.00</td>
    <td>2.21x</td>
  </tr>
  <tr>
    <td>Inception V1 (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>67.21%</td>
    <td>67.24%</td>
    <td>-0.05%</td>
    <td>1880.94</td>
    <td>1159.97</td>
    <td>1.62x</td>
  </tr>
  <tr>
    <td>Inception V1 (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>67.21%</td>
    <td>67.24%</td>
    <td>-0.05%</td>
    <td>1798.96</td>
    <td>1151.37</td>
    <td>1.56x</td>
  </tr>
  <tr>
    <td>EfficientNet (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>76.98%</td>
    <td>77.11%</td>
    <td>-0.17%</td>
    <td>2890.97</td>
    <td>1380.23</td>
    <td>2.09x</td>
  </tr>
  <tr>
    <td>EfficientNet (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>76.99%</td>
    <td>77.11%</td>
    <td>-0.16%</td>
    <td>2548.20</td>
    <td>1362.69</td>
    <td>1.87x</td>
  </tr>
  <tr>
    <td>DenseNet (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>60.53%</td>
    <td>60.96%</td>
    <td>-0.70%</td>
    <td>657.12</td>
    <td>507.94</td>
    <td>1.29x</td>
  </tr>
  <tr>
    <td>SSD (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>18.47%</td>
    <td>18.98%</td>
    <td>-2.69%</td>
    <td>57.63</td>
    <td>14.64</td>
    <td>3.94x</td>
  </tr>
  <tr>
    <td>SSD (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>18.62%</td>
    <td>18.98%</td>
    <td>-1.89%</td>
    <td>56.96</td>
    <td>14.58</td>
    <td>3.91x</td>
  </tr>
  <tr>
    <td>SSD MobileNet V1</td>
    <td>qlinearops</td>
    <td>22.44%</td>
    <td>23.10%</td>
    <td>-2.86%</td>
    <td>1286.79</td>
    <td>904.83</td>
    <td>1.42x</td>
  </tr>
  <tr>
    <td>SSD MobileNet V1</td>
    <td>qdq</td>
    <td>22.44%</td>
    <td>23.10%</td>
    <td>-2.86%</td>
    <td>1121.02</td>
    <td>856.82</td>
    <td>1.31x</td>
  </tr>
  <tr>
    <td>SSD MobileNet V1 (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>22.96%</td>
    <td>23.02%</td>
    <td>-0.27%</td>
    <td>1098.80</td>
    <td>829.55</td>
    <td>1.32x</td>
  </tr>
  <tr>
    <td>SSD MobileNet V1 (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>22.96%</td>
    <td>23.02%</td>
    <td>-0.27%</td>
    <td>1044.34</td>
    <td>790.39</td>
    <td>1.32x</td>
  </tr>
  <tr>
    <td>SSD MobileNet V2</td>
    <td>qlinearops</td>
    <td>23.87%</td>
    <td>24.67%</td>
    <td>-3.25%</td>
    <td>849.89</td>
    <td>627.62</td>
    <td>1.35x</td>
  </tr>
  <tr>
    <td>YOLOv3 (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>27.01%</td>
    <td>28.73%</td>
    <td>-5.99%</td>
    <td>66.22</td>
    <td>83.98</td>
    <td>0.79x</td>
  </tr>
  <tr>
    <td>YOLOv4 (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>32.30%</td>
    <td>33.71%</td>
    <td>-4.19%</td>
    <td>70.87</td>
    <td>66.16</td>
    <td>1.07x</td>
  </tr>
  <tr>
    <td>DUC (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>81.63%</td>
    <td>81.92%</td>
    <td>-0.36%</td>
    <td>9.15</td>
    <td>4.90</td>
    <td>1.87x</td>
  </tr>
  <tr>
    <td>Tiny YOLOv3 (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>11.74%</td>
    <td>12.42%</td>
    <td>-5.48%</td>
    <td>1119.16</td>
    <td>161.90</td>
    <td>6.91x</td>
  </tr>
  <tr>
    <td>Ultra Face (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>83.17%</td>
    <td>83.65%</td>
    <td>-0.57%</td>
    <td>8537.50</td>
    <td>1934.53</td>
    <td>4.41x</td>
  </tr>
  <tr>
    <td>Emotion FERPlus (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>7.97%</td>
    <td>8.00%</td>
    <td>-0.35%</td>
    <td>3568.69</td>
    <td>3121.38</td>
    <td>1.14x</td>
  </tr>
  <tr>
    <td>ArcFace (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>99.80%</td>
    <td>99.80%</td>
    <td>0.00%</td>
    <td>494.07</td>
    <td>244.21</td>
    <td>2.02x</td>
  </tr>
  <tr>
    <td>BERT base MRPC</td>
    <td>qlinearops</td>
    <td>85.54%</td>
    <td>86.03%</td>
    <td>-0.57%</td>
    <td>398.76</td>
    <td>226.09</td>
    <td>1.76x</td>
  </tr>
  <tr>
    <td>BERT base MRPC</td>
    <td>qdq</td>
    <td>85.54%</td>
    <td>86.03%</td>
    <td>-0.57%</td>
    <td>392.94</td>
    <td>223.06</td>
    <td>1.76x</td>
  </tr>
  <tr>
    <td>BERT base MRPC</td>
    <td>integerops</td>
    <td>85.29%</td>
    <td>86.03%</td>
    <td>-0.85%</td>
    <td>473.72</td>
    <td>223.12</td>
    <td>2.12x</td>
  </tr>
  <tr>
    <td>DistilBERT base MRPC</td>
    <td>qdq</td>
    <td>84.07%</td>
    <td>84.56%</td>
    <td>-0.58%</td>
    <td>548.57</td>
    <td>400.62</td>
    <td>1.37x</td>
  </tr>
  <tr>
    <td>DistilBERT base MRPC</td>
    <td>integerops</td>
    <td>85.54%</td>
    <td>84.56%</td>
    <td>1.16%</td>
    <td>964.62</td>
    <td>400.86</td>
    <td>2.41x</td>
  </tr>
  <tr>
    <td>Mobile bert MRPC</td>
    <td>qdq</td>
    <td>85.54%</td>
    <td>86.28%</td>
    <td>-0.85%</td>
    <td>540.59</td>
    <td>394.98</td>
    <td>1.37x</td>
  </tr>
  <tr>
    <td>Mobile bert MRPC</td>
    <td>integerops</td>
    <td>85.54%</td>
    <td>86.28%</td>
    <td>-0.85%</td>
    <td>602.34</td>
    <td>397.35</td>
    <td>1.52x</td>
  </tr>
  <tr>
    <td>Roberta base MRPC</td>
    <td>integerops</td>
    <td>90.93%</td>
    <td>89.95%</td>
    <td>1.09%</td>
    <td>487.62</td>
    <td>222.08</td>
    <td>2.20x</td>
  </tr>
  <tr>
    <td>BERT SQuAD (ONNX Model Zoo)</td>
    <td>integerops</td>
    <td>80.29</td>
    <td>80.67</td>
    <td>-0.47%</td>
    <td>189.27</td>
    <td>97.40</td>
    <td>1.94x</td>
  </tr>
  <tr>
    <td>MobileBERT SQuAD MLPerf (ONNX Model Zoo)</td>
    <td>integerops</td>
    <td>89.87</td>
    <td>90.03</td>
    <td>-0.17%</td>
    <td>146.72</td>
    <td>125.33</td>
    <td>1.17x</td>
  </tr>
  <tr>
    <td>BiDAF (ONNX Model Zoo)</td>
    <td>integerops</td>
    <td>65.93%</td>
    <td>66.08%</td>
    <td>-0.23%</td>
    <td>2757.59</td>
    <td>2277.14</td>
    <td>1.21x</td>
  </tr>
  <tr>
    <td>GPT2 lm head WikiText (ONNX Model Zoo)</td>
    <td>integerops</td>
    <td>31.98</td>
    <td>29.00</td>
    <td>10.31%</td>
    <td>15.47</td>
    <td>9.78</td>
    <td>1.58x</td>
  </tr>
  <tr>
    <td>BERT base cased MRPC (HuggingFace)</td>
    <td>qlinearops</td>
    <td>90.21%</td>
    <td>90.42%</td>
    <td>-0.23%</td>
    <td>360.90</td>
    <td>212.41</td>
    <td>1.70x</td>
  </tr>
  <tr>
    <td>BERT base uncased MRPC (HuggingFace)</td>
    <td>integerops</td>
    <td>89.58%</td>
    <td>90.42%</td>
    <td>-0.93%</td>
    <td>484.68</td>
    <td>212.34</td>
    <td>2.28x</td>
  </tr>
  <tr>
    <td>Roberta base MRPC (HuggingFace)</td>
    <td>qlinearops</td>
    <td>91.00%</td>
    <td>91.38%</td>
    <td>-0.41%</td>
    <td>353.24</td>
    <td>213.83</td>
    <td>1.65x</td>
  </tr>
  <tr>
    <td>Roberta base MRPC (HuggingFace)</td>
    <td>integerops</td>
    <td>90.85%</td>
    <td>91.38%</td>
    <td>-0.58%</td>
    <td>490.42</td>
    <td>212.57</td>
    <td>2.31x</td>
  </tr>
  <tr>
    <td>XLM Roberta base MRPC (HuggingFace)</td>
    <td>qlinearops</td>
    <td>89.37%</td>
    <td>90.10%</td>
    <td>-0.81%</td>
    <td>304.10</td>
    <td>214.51</td>
    <td>1.42x</td>
  </tr>
  <tr>
    <td>XLM Roberta base MRPC (HuggingFace)</td>
    <td>integerops</td>
    <td>89.66%</td>
    <td>90.10%</td>
    <td>-0.50%</td>
    <td>347.25</td>
    <td>214.13</td>
    <td>1.62x</td>
  </tr>
  <tr>
    <td>Camembert base MRPC (HuggingFace)</td>
    <td>qlinearops</td>
    <td>89.28%</td>
    <td>89.28%</td>
    <td>0.00%</td>
    <td>272.62</td>
    <td>216.98</td>
    <td>1.26x</td>
  </tr>
  <tr>
    <td>Camembert base MRPC (HuggingFace)</td>
    <td>integerops</td>
    <td>89.19%</td>
    <td>89.28%</td>
    <td>-0.10%</td>
    <td>489.58</td>
    <td>216.06</td>
    <td>2.27x</td>
  </tr>
  <tr>
    <td>MiniLM L12 H384 uncased MRPC (HuggingFace)</td>
    <td>qlinearops</td>
    <td>90.13%</td>
    <td>90.97%</td>
    <td>-0.93%</td>
    <td>1054.31</td>
    <td>585.78</td>
    <td>1.80x</td>
  </tr>
  <tr>
    <td>MiniLM L12 H384 uncased MRPC (HuggingFace)</td>
    <td>integerops</td>
    <td>91.07%</td>
    <td>90.97%</td>
    <td>0.10%</td>
    <td>1072.47</td>
    <td>590.03</td>
    <td>1.82x</td>
  </tr>
  <tr>
    <td>DistilBERT base uncased SST-2 (HuggingFace)</td>
    <td>qlinearops</td>
    <td>90.71%</td>
    <td>91.06%</td>
    <td>-0.38%</td>
    <td>890.23</td>
    <td>398.72</td>
    <td>2.23x</td>
  </tr>
  <tr>
    <td>DistilBERT base uncased SST-2 (HuggingFace)</td>
    <td>integerops</td>
    <td>90.25%</td>
    <td>91.06%</td>
    <td>-0.88%</td>
    <td>746.66</td>
    <td>397.78</td>
    <td>1.88x</td>
  </tr>
  <tr>
    <td>Albert base v2 SST-2 (HuggingFace)</td>
    <td>qlinearops</td>
    <td>92.09%</td>
    <td>92.32%</td>
    <td>-0.25%</td>
    <td>268.37</td>
    <td>211.96</td>
    <td>1.27x</td>
  </tr>
  <tr>
    <td>Albert base v2 SST-2 (HuggingFace)</td>
    <td>integerops</td>
    <td>91.74%</td>
    <td>92.32%</td>
    <td>-0.62%</td>
    <td>265.65</td>
    <td>212.21</td>
    <td>1.25x</td>
  </tr>
  <tr>
    <td>MiniLM L6 H384 uncased SST-2 (HuggingFace)</td>
    <td>qlinearops</td>
    <td>89.45%</td>
    <td>90.14%</td>
    <td>-0.76%</td>
    <td>1958.82</td>
    <td>1130.40</td>
    <td>1.73x</td>
  </tr>
  <tr>
    <td>MiniLM L6 H384 uncased SST-2 (HuggingFace)</td>
    <td>integerops</td>
    <td>89.91%</td>
    <td>90.14%</td>
    <td>-0.26%</td>
    <td>2022.09</td>
    <td>1130.14</td>
    <td>1.79x</td>
  </tr>
  <tr>
    <td>MiniLM L6 H384 uncased SST-2 (HuggingFace)</td>
    <td>qlinearops</td>
    <td>87.70%</td>
    <td>88.29%</td>
    <td>-0.67%</td>
    <td>397.45</td>
    <td>212.84</td>
    <td>1.87x</td>
  </tr>
  <tr>
    <td>MiniLM L6 H384 uncased SST-2 (HuggingFace)</td>
    <td>integerops</td>
    <td>88.19%</td>
    <td>88.29%</td>
    <td>-0.12%</td>
    <td>489.19</td>
    <td>213.14</td>
    <td>2.30x</td>
  </tr>
  <tr>
    <td>Electra small discriminator MRPC (HuggingFace)</td>
    <td>qlinearops</td>
    <td>89.92%</td>
    <td>89.83%</td>
    <td>0.09%</td>
    <td>1797.98</td>
    <td>1077.51</td>
    <td>1.67x</td>
  </tr>
  <tr>
    <td>Electra small discriminator MRPC (HuggingFace)</td>
    <td>integerops</td>
    <td>89.27%</td>
    <td>89.83%</td>
    <td>-0.63%</td>
    <td>1930.55</td>
    <td>1139.74</td>
    <td>1.69x</td>
  </tr>
  <tr>
    <td>BERT mini MRPC (HuggingFace)</td>
    <td>qlinearops</td>
    <td>86.21%</td>
    <td>86.52%</td>
    <td>-0.35%</td>
    <td>5510.81</td>
    <td>3334.89</td>
    <td>1.65x</td>
  </tr>
  <tr>
    <td>BERT mini MRPC (HuggingFace)</td>
    <td>integerops</td>
    <td>86.16%</td>
    <td>86.52%</td>
    <td>-0.41%</td>
    <td>5627.19</td>
    <td>3365.08</td>
    <td>1.67x</td>
  </tr>
  <tr>
    <td>Xlnet base cased MRPC (HuggingFace)</td>
    <td>qlinearops</td>
    <td>90.05%</td>
    <td>89.86%</td>
    <td>0.21%</td>
    <td>108.83</td>
    <td>92.24</td>
    <td>1.18x</td>
  </tr>
  <tr>
    <td>Xlnet base cased MRPC (HuggingFace)</td>
    <td>integerops</td>
    <td>89.58%</td>
    <td>89.86%</td>
    <td>-0.31%</td>
    <td>110.83</td>
    <td>90.80</td>
    <td>1.22x</td>
  </tr>
  <tr>
    <td>BART large MRPC (HuggingFace)</td>
    <td>qlinearops</td>
    <td>91.77%</td>
    <td>91.20%</td>
    <td>0.63%</td>
    <td>59.18</td>
    <td>51.49</td>
    <td>1.15x</td>
  </tr>
  <tr>
    <td>BART large MRPC (HuggingFace)</td>
    <td>integerops</td>
    <td>92.36%</td>
    <td>91.20%</td>
    <td>1.28%</td>
    <td>96.38</td>
    <td>51.47</td>
    <td>1.87x</td>
  </tr>
  <tr>
    <td>DeBERTa v3 base MRPC (HuggingFace)</td>
    <td>qlinearops</td>
    <td>91.85%</td>
    <td>92.23%</td>
    <td>-0.40%</td>
    <td>163.17</td>
    <td>146.13</td>
    <td>1.12x</td>
  </tr>
  <tr>
    <td>DeBERTa v3 base MRPC (HuggingFace)</td>
    <td>integerops</td>
    <td>92.39%</td>
    <td>92.23%</td>
    <td>0.17%</td>
    <td>168.41</td>
    <td>145.58</td>
    <td>1.16x</td>
  </tr>
  <tr>
    <td>Spanbert SQuAD (HuggingFace)</td>
    <td>qlinearops</td>
    <td>91.14</td>
    <td>91.98</td>
    <td>-0.91%</td>
    <td>69.53</td>
    <td>42.72</td>
    <td>1.63x</td>
  </tr>
  <tr>
    <td>Spanbert SQuAD (HuggingFace)</td>
    <td>integerops</td>
    <td>91.40</td>
    <td>91.98</td>
    <td>-0.63%</td>
    <td>79.82</td>
    <td>42.58</td>
    <td>1.87x</td>
  </tr>
  <tr>
    <td>Bert base multilingual cased SQuAD (HuggingFace)</td>
    <td>qlinearops</td>
    <td>88.42</td>
    <td>89.13</td>
    <td>-0.79%</td>
    <td>70.47</td>
    <td>42.73</td>
    <td>1.65x</td>
  </tr>
  <tr>
    <td>Bert base multilingual cased SQuAD (HuggingFace)</td>
    <td>integerops</td>
    <td>88.70</td>
    <td>89.13</td>
    <td>-0.48%</td>
    <td>79.35</td>
    <td>42.46</td>
    <td>1.87x</td>
  </tr>
  <tr>
    <td>DistilBert base uncased SQuAD (HuggingFace)</td>
    <td>qlinearops</td>
    <td>86.33</td>
    <td>86.86</td>
    <td>-0.62%</td>
    <td>113.00</td>
    <td>67.85</td>
    <td>1.67x</td>
  </tr>
  <tr>
    <td>DistilBert base uncased SQuAD (HuggingFace)</td>
    <td>integerops</td>
    <td>86.05</td>
    <td>86.86</td>
    <td>-0.94%</td>
    <td>159.51</td>
    <td>67.90</td>
    <td>2.35x</td>
  </tr>
  <tr>
    <td>BERT large uncased whole word masking SQuAD (HuggingFace)</td>
    <td>qlinearops</td>
    <td>92.34</td>
    <td>93.16</td>
    <td>-0.88%</td>
    <td>24.64</td>
    <td>12.75</td>
    <td>1.93x</td>
  </tr>
  <tr>
    <td>BERT large uncased whole word masking SQuAD (HuggingFace)</td>
    <td>integerops</td>
    <td>92.99</td>
    <td>93.16</td>
    <td>-0.18%</td>
    <td>26.79</td>
    <td>12.76</td>
    <td>2.10x</td>
  </tr>
  <tr>
    <td>Roberta large SQuAD v2 (HuggingFace)</td>
    <td>qlinearops</td>
    <td>89.03</td>
    <td>89.02</td>
    <td>0.02%</td>
    <td>16.91</td>
    <td>12.98</td>
    <td>1.30x</td>
  </tr>
  <tr>
    <td>Roberta large SQuAD v2 (HuggingFace)</td>
    <td>integerops</td>
    <td>89.04</td>
    <td>89.02</td>
    <td>0.02%</td>
    <td>26.80</td>
    <td>12.95</td>
    <td>2.07x</td>
  </tr>
  <tr>
    <td>GPT2 WikiText (HuggingFace)</td>
    <td>qlinearops</td>
    <td>30.25</td>
    <td>29.00</td>
    <td>4.33%</td>
    <td>12.82</td>
    <td>9.80</td>
    <td>1.31x</td>
  </tr>
  <tr>
    <td>GPT2 WikiText (HuggingFace)</td>
    <td>integerops</td>
    <td>29.68</td>
    <td>29.00</td>
    <td>2.36%</td>
    <td>13.68</td>
    <td>9.76</td>
    <td>1.40x</td>
  </tr>
  <tr>
    <td>DistilGPT2 WikiText (HuggingFace)</td>
    <td>qlinearops</td>
    <td>44.93</td>
    <td>43.43</td>
    <td>3.46%</td>
    <td>20.66</td>
    <td>16.78</td>
    <td>1.23x</td>
  </tr>
  <tr>
    <td>DistilGPT2 WikiText (HuggingFace)</td>
    <td>integerops</td>
    <td>44.62</td>
    <td>43.43</td>
    <td>2.74%</td>
    <td>21.97</td>
    <td>16.77</td>
    <td>1.31x</td>
  </tr>
  <tr>
    <td>LayoutLM FUNSD (HuggingFace)</td>
    <td>qlinearops</td>
    <td>78.15%</td>
    <td>78.35%</td>
    <td>-0.25%</td>
    <td>59.50</td>
    <td>42.98</td>
    <td>1.38x</td>
  </tr>
  <tr>
    <td>LayoutLM FUNSD (HuggingFace)</td>
    <td>integerops</td>
    <td>77.58%</td>
    <td>78.35%</td>
    <td>-0.98%</td>
    <td>64.93</td>
    <td>43.20</td>
    <td>1.50x</td>
  </tr>
  <tr>
    <td>LayoutLMv3 FUNSD (HuggingFace)</td>
    <td>qlinearops</td>
    <td>90.00%</td>
    <td>90.49%</td>
    <td>-0.54%</td>
    <td>30.97</td>
    <td>27.97</td>
    <td>1.11x</td>
  </tr>
  <tr>
    <td>LayoutLMv3 FUNSD (HuggingFace)</td>
    <td>integerops</td>
    <td>90.07%</td>
    <td>90.49%</td>
    <td>-0.46%</td>
    <td>35.15</td>
    <td>27.72</td>
    <td>1.27x</td>
  </tr>
  <tr>
    <td>LayoutLMv2 (HuggingFace)</td>
    <td>qlinearops</td>
    <td>81.36%</td>
    <td>81.17%</td>
    <td>0.23%</td>
    <td>48.61</td>
    <td>38.93</td>
    <td>1.25x</td>
  </tr>
  <tr>
    <td>LayoutLMv2 (HuggingFace)</td>
    <td>integerops</td>
    <td>80.86%</td>
    <td>81.17%</td>
    <td>-0.39%</td>
    <td>45.52</td>
    <td>36.10</td>
    <td>1.26x</td>
  </tr>
  <tr>
    <td>CodeBert  (HuggingFace)</td>
    <td>qlinearops</td>
    <td>64.97%</td>
    <td>65.41%</td>
    <td>-0.67%</td>
    <td>64.99</td>
    <td>44.20</td>
    <td>1.47x</td>
  </tr>
  <tr>
    <td>CodeBert  (HuggingFace)</td>
    <td>integerops</td>
    <td>64.93%</td>
    <td>65.41%</td>
    <td>-0.73%</td>
    <td>77.99</td>
    <td>43.63</td>
    <td>1.79x</td>
  </tr>
</tbody>
</table>

<table>
<thead>
  <tr>
    <th rowspan="2">Model</th>
    <th rowspan="2">Example</th>
    <th colspan="3">Accuracy</th>
    <th colspan="3">Performance 1s56c1ins1bs<br>Throughput(samples/sec)</th>
  </tr>
  <tr>
    <th>INT8</th>
    <th>FP32</th>
    <th>Accuracy Ratio<br>[(INT8-FP32)/FP32]</th>
    <th>INT8</th>
    <th>FP32</th>
    <th>Performance Ratio<br>[INT8/FP32]</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Faster R-CNN (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>34.06%</td>
    <td>34.37%</td>
    <td>-0.88%</td>
    <td>4.15</td>
    <td>3.47</td>
    <td>1.20x</td>
  </tr>
  <tr>
    <td>Faster R-CNN (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>33.98%</td>
    <td>34.37%</td>
    <td>-1.12%</td>
    <td>4.19</td>
    <td>3.49</td>
    <td>1.20x</td>
  </tr>
  <tr>
    <td>Mask R-CNN (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>33.13%</td>
    <td>33.72%</td>
    <td>-1.74%</td>
    <td>3.46</td>
    <td>3.02</td>
    <td>1.15x</td>
  </tr>
  <tr>
    <td>Mask R-CNN (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>33.29%</td>
    <td>33.72%</td>
    <td>-1.28%</td>
    <td>3.46</td>
    <td>3.02</td>
    <td>1.15x</td>
  </tr>
  <tr>
    <td>FCN (ONNX Model Zoo)</td>
    <td>qlinearops</td>
    <td>64.54%</td>
    <td>64.98%</td>
    <td>-0.67%</td>
    <td>28.04</td>
    <td>12.59</td>
    <td>2.23x</td>
  </tr>
  <tr>
    <td>FCN (ONNX Model Zoo)</td>
    <td>qdq</td>
    <td>64.54%</td>
    <td>64.98%</td>
    <td>-0.67%</td>
    <td>28.22</td>
    <td>12.67</td>
    <td>2.23x</td>
  </tr>
  <tr>
    <td>GPT-J-6B (HuggingFace)</td>
    <td>qlinearops</td>
    <td>78.46%</td>
    <td>79.17%</td>
    <td>-0.91%</td>
    <td>1.74</td>
    <td>0.66</td>
    <td>2.62x</td>
  </tr>
  <tr>
    <td>GPT-J-6B (HuggingFace)</td>
    <td>integerops</td>
    <td>78.93%</td>
    <td>79.17%</td>
    <td>-0.31%</td>
    <td>1.68</td>
    <td>0.67</td>
    <td>2.52x</td>
  </tr>
</tbody>
</table>

### ONNX Models with ONNX Runtime 1.15.0 in WOQ Mode

<table class="tg">
<thead>
  <tr>
    <th rowspan="2">Model name</th>
    <th rowspan="2">Configuration</th>
    <th colspan="2">Lambada_openai</th>
    <th rowspan="2">Accuracy Ratio<br>[INT4/FP32]</th>
  </tr>
  <tr>
    <th>Accuracy</th>
    <th>Perplexity</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="2">meta-llama/Llama-2-7b-chat-hf</td>
    <td>FP32</td>
    <td>0.7058</td>
    <td>3.2788</td>
    <td>/</td>
  </tr>
  <tr>
    <td>GPTQ<br>W4G32Asym</td>
    <td>0.7002</td>
    <td>3.4124</td>
    <td>0.9921</td>
  </tr>
  <tr>
    <td rowspan="2">meta-llama/Llama-2-7b-hf</td>
    <td>FP32</td>
    <td>0.7392</td>
    <td>3.3950</td>
    <td>/</td>
  </tr>
  <tr>
    <td>GPTQ<br>W4G32Asym</td>
    <td>0.7312</td>
    <td>3.5711</td>
    <td>0.9892</td>
  </tr>
  <tr>
    <td rowspan="2">meta-llama/Llama-2-13b-chat-hf</td>
    <td>FP32</td>
    <td>0.7312</td>
    <td>2.9163</td>
    <td>/</td>
  </tr>
  <tr>
    <td>GPTQ<br>W4G128Asym</td>
    <td>0.7240</td>
    <td>2.9945</td>
    <td>0.9902</td>
  <tr>
    <td rowspan="3">meta-llama/Llama-2-13b-hf</td>
    <td>FP32</td>
    <td>0.7677</td>
    <td>3.0438</td>
    <td>/</td>
  </tr>
  <tr>
    <td>GPTQ<br>W4G128Asym</td>
    <td>0.7634</td>
    <td>3.1186</td>
    <td>0.9944</td>
  <tr>
    <td>GPTQ<br>W4G32Asym</td>
    <td>0.7615</td>
    <td>3.1276</td>
    <td>0.9919</td>
  </tr>
  <tr>
    <td rowspan="2">meta-llama/Llama-2-70b-chat-hf</td>
    <td>FP32</td>
    <td>0.7543</td>
    <td>2.6181</td>
    <td>/</td>
  </tr>
  <tr>
    <td>RTN<br>W4G32Asym</td>
    <td>0.7518</td>
    <td>2.6496</td>
    <td>0.9967</td>
  </tr>
  <tr>
    <td rowspan="2">meta-llama/Llama-2-70b-hf</td>
    <td>FP32</td>
    <td>0.7964</td>
    <td>2.6612</td>
    <td>/</td>
  </tr>
  <tr>
    <td>RTN<br>W4G32Sym</td>
    <td>0.7941</td>
    <td>2.7243</td>
    <td>0.9971</td>
  </tr>
</tbody>
</table>


## Validated Pruning Examples

<table class="docutils">
<thead>
  <tr>
    <th rowspan="2">Model</th>
    <th rowspan="2">Task</br>Dataset</th>
    <th rowspan="2">Dense Accuracy<br>Sparse Accuracy</th>
    <th rowspan="2">Relative Drop</th>
    <th rowspan="2">Sparsity ratio<br>Sparsity Pattern</th>
    <th rowspan="2">Comments<br>Balanced<br>or unbalanced ratio</th>
  </tr>
  <tr>
  </tr>
</thead>
<tbody>  
  <tr>
    <td>Bert-Mini</td>
    <td>question answering</br>SQuAD-v1.1</td>
    <td>f1=76.87</br>f1=76.2</td>
    <td>-0.80%</td>
    <td>80%</br>structured 4x1</td>
    <td>snip momentum</br>unbalanced</td>
  </tr>
  <tr>
  </tr>  
  <tr>
    <td>Bert-Mini</td>
    <td>question answering</br>SQuAD-v1.1</td>
    <td>f1=76.87</br>f1=76.2</td>
    <td>-0.80%</td>
    <td>80%</br>structured 4x1</td>
    <td>snip momentum</br>unbalanced</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-Mini</td>
    <td>question answering</br>SQuAD-v1.1</td>
    <td>f1=76.87</br>f1=77.62</td>
    <td>+0.98%</td>
    <td>50%</br>structured 2:4</td>
    <td>snip momentum</br>balanced</td>  
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Distilbert-base-uncased</td>
    <td>question answering</br>SQuAD-v1.1</td>
    <td>f1=86.90</br>f1=86.15</td>
    <td>-0.86%</td>
    <td>80%</br>structured 4x1</td>
    <td>snip momentum</br>unbalanced</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Distilbert-base-uncased</td>
    <td>question answering</br>SQuAD-v1.1</td>
    <td>f1=86.90</br>f1=87.50</td>
    <td>+0.69%</td>
    <td>50%</br>structured 2:4</td>
    <td>snip momentum</br>balanced</td>  
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-base-uncased</td>
    <td>question answering</br>SQuAD-v1.1</td>
    <td>f1=88.59</br>f1=87.78</td>
    <td>-0.92%</td>
    <td>80%</br>structured 4x1</td>
    <td>snip momentum</br>unbalanced</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-base-uncased</td>
    <td>question answering</br>SQuAD-v1.1</td>
    <td>f1=88.59</br>f1=89.40</td>
    <td>+0.91%</td>
    <td>50%</br>structured 2:4</td>
    <td>snip momentum</br>balanced</td>  
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-large</td>
    <td>question answering</br>SQuAD-v1.1</td>
    <td>f1=91.23</br>f1=90.91</td>
    <td>-0.35%</td>
    <td>80%</br>structured 4x1</td>
    <td>snip momentum</br>unbalanced</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-large</td>
    <td>question answering</br>SQuAD-v1.1</td>
    <td>f1=91.23</br>f1=91.67</td>
    <td>+0.48%</td>
    <td>50%</br>structured 2:4</td>
    <td>snip momentum</br>balanced</td>  
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-Mini</td>
    <td>text classification</br>MRPC</td>
    <td>f1=87.52</br>f1=87.22</td>
    <td>-0.34%</td>
    <td>90%</br>structured 4x1</td>
    <td>snip momentum</br>unbalanced</td>  
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-Mini</td>
    <td>text classification</br>MRPC</td>
    <td>f1=87.52</br>f1=87.33</td>
    <td>-0.22%</td>
    <td>90%</br>structured 4x1</td>
    <td>snip momentum</br>balanced</td>  
  </tr>
  <tr>
  </tr>  
  <tr>
    <td>Bert-Mini</td>
    <td>text classification</br>MRPC</td>
    <td>f1=87.52</br>f1=86.89</td>
    <td>-0.72%</td>
    <td>50%</br>structured 2:4</td>
    <td>snip momentum</br>balanced</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-Mini</td>
    <td>text classification</br>MRPC</td>
    <td>f1=87.52</br>f1=86.8</td>
    <td>-0.83%</td>
    <td>60%</br>structured per channel</td>
    <td>snip momentum</br>unbalanced</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Distilbert-base-uncased</td>
    <td>text classification</br>MRPC</td>
    <td>f1=90.26</br>f1=89.85</td>
    <td>-0.46%</td>
    <td>90%</br>structured 4x1</td>
    <td>snip momentum</br>unbalanced</td>  
  </tr>
  <tr>
  </tr>  
  <tr>
    <td>Distilbert-base-uncased</td>
    <td>text classification</br>MRPC</td>
    <td>f1=90.26</br>f1=90.88</td>
    <td>+0.69%</td>
    <td>50%</br>structured 2:4</td>
    <td>snip momentum</br>balanced</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-Mini</td>
    <td>text classification</br>SST-2</td>
    <td>accuracy=87.61</br>accuracy=86.92</td>
    <td>-0.79%</td>
    <td>90%</br>structured 4x1</td>
    <td>snip momentum</br>unbalanced</td>  
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-Mini</td>
    <td>text classification</br>SST-2</td>
    <td>accuracy=87.61</br>accuracy=87.73</td>
    <td>+0.14%</td>
    <td>50%</br>structured 2:4</td>
    <td>snip momentum</br>balanced</td>
  </tr>
  <tr>
  </tr>  
  <tr>
    <td>Bert-Mini</td>
    <td>text classification</br>SST-2</td>
    <td>accuracy=87.61</br>accuracy=86.92</td>
    <td>-0.79%</td>
    <td>50%</br>structured per channel</td>
    <td>snip momentum</br>unbalanced</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td>ResNet50</td>
    <td>image recognition</br>ImageNet</td>
    <td>top1 acc = 78.95</br>top1 acc = 80.10</td>
    <td>-1.43%</td>
    <td>75%</br>structured 2x1</td>
    <td>snip momentum</br>unbalanced</td>
  </tr>
  <tr>
  <tr>
    <td>YOLO-v5s6</td>
    <td>object detection</br>COCO</td>
    <td>AP0.50:0.95/AP0.50=0.404/0.6</br>AP0.50:0.95/AP0.50=0.393/0.584</td>
    <td>-2.72%</td>
    <td>80%</br>unstructured</td>
    <td>snip momentum</br>unbalanced</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-Large</td>
    <td>question answering</br>SQuAD-v1.1</td>
    <td>f1=91.34</br>f1=90.7</td>
    <td>-0.07%</td>
    <td>80%</br>structured 2x1</td>
    <td>group lasso</br>unbalanced</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-Base</td>
    <td>text classification</br>MNLI</td>
    <td>[m, mm] = [84.57, 84.79]</br>[m, mm] = [82.45, 83.27]</td>
    <td>[-2.51%, -1.80%]</td>
    <td>70%</br>unstructured</td>
    <td>Prune once for all</br>balanced</td>    
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-Base</td>
    <td>text classification</br>MNLI</td>
    <td>[m, mm] = [84.57, 84.79]</br>[m, mm] = [83.20, 84.11]</td>
    <td>[-1.62%, -0.80%]</td>
    <td>50%</br>structured 1:2</td>
    <td>Prune once for all</br>balanced</td>    
  </tr>
  <tr>
  </tr>  
  <tr>
    <td>Bert-Base</td>
    <td>text classification</br>SST-2</td>
    <td>accuracy = 92.32</br>accuracy = 91.51</td>
    <td>-0.88%</td>
    <td>70%</br>unstructured</td>
    <td>Prune once for all</br>balanced</td>    
  </tr>
  <tr>
  <tr>
    <td>Bert-Base</td>
    <td>text classification</br>SST-2</td>
    <td>accuracy = 92.32</br>accuracy = 92.20</td>
    <td>-0.13%</td>
    <td>50%</br>structured 1:2</td>
    <td>Prune once for all</br>balanced</td>       
  </tr>
  <tr>  
  </tr>
  <tr>
    <td>Bert-Base</td>
    <td>text classification</br>SST-2</td>
    <td>accuracy = 92.32</br>accuracy = 91.97</td>
    <td>-0.38%</td>
    <td>20%</br>unstructured</td>
    <td>gradient sensitivity</br>balanced</td>       
  </tr>
  <tr>  
  </tr>  
  <tr>
    <td>Bert-Base</td>
    <td>text classification</br>QQP</td>
    <td>[accuracy, f1] = [91.10, 88.05]</br>[accuracy, f1] = [90.48, 87.06]</td>
    <td>[-0.68%, -1.12%]</td>
    <td>70%</br>unstructured</td>
    <td>Prune once for all</br>balanced</td>        
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-Base</td>
    <td>text classification</br>QQP</td>
    <td>[accuracy, f1] = [91.10, 88.05]</br>[accuracy, f1] = [90.92, 87.78]</td>
    <td>[-0.20%, -0.31%]</td>
    <td>50%</br>structured 1:2</td>
    <td>Prune once for all</br>balanced</td>        
  </tr>
  <tr>
  </tr>   
  <tr>
    <td>Bert-Base</td>
    <td>text classification</br>QNLI</td>
    <td>accuracy = 91.54</br>accuracy = 90.39</td>
    <td>-1.26%</td>
    <td>70%</br>unstructured</td>
    <td>Prune once for all</br>balanced</td>        
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Bert-Base</td>
    <td>text classification</br>QNLI</td>
    <td>accuracy = 91.54</br>accuracy = 90.87</td>
    <td>-0.73%</td>
    <td>50%</br>structured 1:2</td>
    <td>Prune once for all</br>balanced</td>      
  </tr>
  <tr>
  </tr>   
  <tr>
    <td>Bert-Base</td>
    <td>question answering</td>
    <td>[em, f1] = [79.34, 87.10]</br>[em, f1] = [77.27, 85.75]</td>
    <td>[-2.61%, -1.54%]</td>
    <td>70%</br>unstructured</td>
    <td>Prune once for all</br>balanced</td>   
  </tr>  
  <tr>
  </tr>
  <tr>
    <td>Bert-Base</td>
    <td>question answering</td>
    <td>[em, f1] = [79.34, 87.10]</br>[em, f1] = [78.03, 86.50]</td>
    <td>[-1.65%, -0.69%]</td>
    <td>50%</br>structured 1:2</td>
    <td>Prune once for all</br>balanced</td>       
  </tr>  
  <tr>
  </tr>  
</tbody>
</table>

## Validated Knowledge Distillation Examples

|  Example Name       | Dataset   | Student<br>(Metrics)                 | Teacher<br>(Metrics)               | Student With Distillation<br>(Metrics Improvement)  | Student With <br>Distributed Distillation<br>(Metrics Improvement)  |
|---------------------|-----------|--------------------------------------|------------------------------------|-----------------------------------------------------|-----------------------------------------------------|
| MobileNet example   | CIFAR-10  | MobileNetV2-0.35<br>(0.7965 ACC)     | WideResNet40-2<br>(0.9522 ACC)     |   0.8178 ACC<br>(0.0213 ACC)                        |   0.8235 ACC<br>(0.027 ACC)                        |
| CNN example         | CIFAR-100 | CNN-2<br>(0.5494 ACC)                | CNN-10<br>(0.7153 ACC)             |   0.5540 ACC<br>(0.0046 ACC)                        |   0.5523 ACC<br>(0.0029 ACC)                        |
| VGG example         | CIFAR-100 | VGG-8-BN<br>(0.7022 ACC)             | VGG-13-BN<br>(0.7415 ACC)          |   0.7025 ACC<br>(0.0003 ACC)                        |   NA                        |
| ResNet example      | ImageNet  | ResNet18<br>(0.6739 ACC)             | ResNet50<br>(0.7399 ACC)           |   0.6845 ACC<br>(0.0106 ACC)                        |   NA                        |
| BlendCnn example    |   MRPC    | BlendCnn<br>(0.7034 ACC)             | BERT-Base<br>(0.8382 ACC)          |   0.7034 ACC<br>(0 ACC)                             |   NA                        |
| BiLSTM example      |  SST-2    | BiLSTM<br>(0.8314 ACC)               | RoBERTa-Base<br>(0.9403 ACC)       |   0.9048 ACC<br>(0.0734 ACC)                        |   NA                        |
|DistilBERT example   |  SQuAD    | DistilBERT<br>(0.7323/0.8256 EM/F1)  | BERT-Base<br>(0.8084/0.8814 EM/F1) |   0.7442/0.8371 EM/F1<br>(0.0119/0.0115 EM/F1)      |   NA                        |
|TinyBERT example     |  MNLI     | TinyBERT<br>(0.8018/0.8044 m/mm)     | BERT-Base<br>(0.8363/0.8411 m/mm)  |   0.8025/0.8074 m/mm<br>(0.0007/0.0030 m/mm)        |   NA                        |
|BERT-3 example       |  QQP      | BERT-3<br>(0.8626/0.8213 EM/F1)      | BERT-Base<br>(0.9091/0.8782 EM/F1) |   0.8684/0.8259 EM/F1<br>(0.0058/0.0046 EM/F1)      |   NA                        |
|DistilRoBERTa example|  COLA     | DistilRoBERTa<br>(0.6057 ACC)        | RoBERTa-Large<br>(0.6455 ACC)      |   0.6187 ACC<br>(0.0130 ACC)                        |   NA                        |

## Validated ONNX QDQ INT8 Models on Multiple Hardware through ONNX Runtime

<table class="docutils">
<thead>
  <tr>
    <th class="tg-y3we">Model (ONNX QDQ)</th>
    <th class="tg-pm1l">AWS c6i.2xlarge (Intel)<br>CPU Execution Provider</th>
    <th class="tg-pm1l">AWS c6a.2xlarge (AMD)<br>CPU Execution Provider</th>
    <th class="tg-pm1l">AWS c6g.2xlarge (ARM)<br>CPU Execution Provider</th>
    <th class="tg-8d8j">NVidia A100<br>CUDA Execution<br>Provider</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-cwad">ResNet50</td>
    <td class="tg-pm1l">74.76%</td>
    <td class="tg-pm1l">68.95%</td>
    <td class="tg-pm1l">74.76%</td>
    <td class="tg-6q5x">74.75%</td>
  </tr>
  <tr>
    <td class="tg-cwad">BERT-base</td>
    <td class="tg-pm1l">85.54%</td>
    <td class="tg-pm1l">84.56%</td>
    <td class="tg-pm1l">85.54%</td>
    <td class="tg-6q5x">84.31%</td>
  </tr>
  <tr>
    <td class="tg-cwad">ResNet50 V1.5</td>
    <td class="tg-pm1l">72.20%</td>
    <td class="tg-pm1l">67.70%</td>
    <td class="tg-pm1l">72.20%</td>
    <td class="tg-6q5x">72.29%</td>
  </tr>
  <tr>
    <td class="tg-cwad">MobileNet V2</td>
    <td class="tg-pm1l">65.82%</td>
    <td class="tg-pm1l">58.56%</td>
    <td class="tg-pm1l">65.83%</td>
    <td class="tg-pm1l">65.63%</td>
  </tr>
  <tr>
    <td class="tg-cwad">SSD MobileNet V1</td>
    <td class="tg-pm1l">22.45%</td>
    <td class="tg-pm1l">16.53%</td>
    <td class="tg-pm1l">22.45%</td>
    <td class="tg-pm1l">22.35%</td>
  </tr>
  <tr>
    <td class="tg-cwad">DistilBERT base MRPC</td>
    <td class="tg-pm1l">84.56%</td>
    <td class="tg-pm1l">83.82%</td>
    <td class="tg-pm1l">84.56%</td>
    <td class="tg-6q5x">84.56%</td>
  </tr>
  <tr>
    <td class="tg-cwad">SqueezeNet</td>
    <td class="tg-pm1l">56.54%</td>
    <td class="tg-pm1l">53.52%</td>
    <td class="tg-pm1l">56.54%</td>
    <td class="tg-6q5x">56.55%</td>
  </tr>
  <tr>
    <td class="tg-cwad">SSD</td>
    <td class="tg-pm1l">18.63%</td>
    <td class="tg-pm1l">18.54%</td>
    <td class="tg-pm1l">18.63%</td>
    <td class="tg-6q5x">18.61%</td>
  </tr>
  <tr>
    <td class="tg-cwad">AlexNet</td>
    <td class="tg-pm1l">54.71%</td>
    <td class="tg-pm1l">47.06%</td>
    <td class="tg-pm1l">54.71%</td>
    <td class="tg-pm1l">54.79%</td>
  </tr>
  <tr>
    <td class="tg-cwad">CaffeNet</td>
    <td class="tg-pm1l">56.25%</td>
    <td class="tg-pm1l">52.35%</td>
    <td class="tg-pm1l">56.27%</td>
    <td class="tg-pm1l">56.24%</td>
  </tr>
  <tr>
    <td class="tg-cwad">GoogleNet</td>
    <td class="tg-pm1l">67.73%</td>
    <td class="tg-pm1l">63.56%</td>
    <td class="tg-pm1l">67.72%</td>
    <td class="tg-6q5x">67.76%</td>
  </tr>
  <tr>
    <td class="tg-cwad">ZFNet</td>
    <td class="tg-pm1l">55.86%</td>
    <td class="tg-pm1l">45.09%</td>
    <td class="tg-pm1l">55.86%</td>
    <td class="tg-pm1l">55.89%</td>
  </tr>
  <tr>
    <td class="tg-cwad">Inception V1</td>
    <td class="tg-pm1l">67.21%</td>
    <td class="tg-pm1l">63.03%</td>
    <td class="tg-pm1l">67.20%</td>
    <td class="tg-6q5x">67.21%</td>
  </tr>
  <tr>
    <td class="tg-cwad">SSD MobileNet V1 (ONNX Model Zoo)</td>
    <td class="tg-pm1l">22.86%</td>
    <td class="tg-pm1l">16.94%</td>
    <td class="tg-pm1l">22.80%</td>
    <td class="tg-pm1l">22.87%</td>
  </tr>
  <tr>
    <td class="tg-cwad">Mobile bert MRPC</td>
    <td class="tg-pm1l">85.54%</td>
    <td class="tg-pm1l">84.56%</td>
    <td class="tg-pm1l">85.54%</td>
    <td class="tg-pm1l">85.54%</td>
  </tr>
  <tr>
    <td class="tg-cwad">Roberta base MRPC</td>
    <td class="tg-pm1l">89.46%</td>
    <td class="tg-pm1l">90.44%</td>
    <td class="tg-pm1l">89.71%</td>
    <td class="tg-pm1l">89.71%</td>
  </tr>
  <tr>
    <td class="tg-cwad">ResNet50 V1.5 MLPerf</td>
    <td class="tg-pm1l">76.14%</td>
    <td class="tg-pm1l">72.80%</td>
    <td class="tg-pm1l">76.14%</td>
    <td class="tg-6q5x">76.17%</td>
  </tr>
  <tr>
    <td class="tg-cwad">VGG16</td>
    <td class="tg-pm1l">66.69%</td>
    <td class="tg-pm1l">64.25%</td>
    <td class="tg-pm1l">66.69%</td>
    <td class="tg-pm1l">66.64%</td>
  </tr>
  <tr>
    <td class="tg-cwad">VGG16 (ONNX Model Zoo)</td>
    <td class="tg-pm1l">72.31%</td>
    <td class="tg-pm1l">69.35%</td>
    <td class="tg-pm1l">72.32%</td>
    <td class="tg-pm1l">72.34%</td>
  </tr>
  <tr>
    <td class="tg-cwad">MobileNet V3 MLPerf</td>
    <td class="tg-pm1l">75.57%</td>
    <td class="tg-pm1l">70.78%</td>
    <td class="tg-pm1l">75.56%</td>
    <td class="tg-6q5x">75.52%</td>
  </tr>
  <tr>
    <td class="tg-cwad">EfficientNet</td>
    <td class="tg-pm1l">77.61%</td>
    <td class="tg-pm1l">76.52%</td>
    <td class="tg-pm1l">77.56%</td>
    <td class="tg-pm1l">77.60%</td>
  </tr>
  <tr>
    <td class="tg-cwad">MobileNet V2 (ONNX Model Zoo)</td>
    <td class="tg-pm1l">68.51%</td>
    <td class="tg-pm1l">62.48%</td>
    <td class="tg-pm1l">68.58%</td>
    <td class="tg-pm1l">68.48%</td>
  </tr>
  <tr>
    <td class="tg-413a">ShuffleNet V2</td>
    <td class="tg-pm1l">66.12%</td>
    <td class="tg-pm1l">58.41%</td>
    <td class="tg-pm1l">66.11%</td>
    <td class="tg-pm1l">66.11%</td>
  </tr>
</tbody>
</table>
