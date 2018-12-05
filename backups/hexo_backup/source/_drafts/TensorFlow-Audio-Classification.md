---
title: TensorFlow Audio Classification
categories:
  - Project
tags:
  - TensorFlow
  - Audio
  - Deep Learning
  - VGGish
  - AudioSet
  - Python
date: 2018-09-05 22:46:43
---

此项目源自4个月前(即2018年5月)公司的一个实际项目: **检测主播是否在唱歌**, 即通过直播间的声音信号判定主播当前时间段是否在唱歌. 该项目已于 2018-06-20 上线, 准确率为 `~93%`.

在此之前, 我没有语音相关的经验, 不仅如此, 公司内部也没有相关技术储备. 只能凭借经验和 sense 去查找解决方案, 经过 1 星期的调研, 确定了使用深度学习, 并选定 **特征提取 + 分类** 这种比较传统但成熟的方案. 最后, 我与一个实习生经过一个月的努力, 在 deadline 之前完成上线. 具体地

- **特征提取** 阶段选用 [VGGish][vggish] 网络结构, 这是由 Google 开源并在 [YouTube8M][ytb8m] 中实际应用的技术;
- **分类** 阶段采用非常简单的结构: `2个全连接层 + 1个Softmax层` , 因为 VGGish 提取的特征(embedding)够紧凑, 包含的信息足够多, 可以应对一个二分类问题(唱歌和非唱歌);

在这篇文章中, 我将介绍关于这个项目涉及的主要问题和解决办法, 以及怎样通过一些 trick 将准确率从 **70% 提升至 93%**. 并以一个公开数据集 [UrbanSound][data-urban] 作为例子进行讲解.

开源地址: [https://github.com/luuil/tensorflow-audio-classification][tf-ac]

<!-- more -->

## 前言

在"星秀"类型的直播中, 主播的直播内容可能包括聊天, 跳舞, 唱歌等内容. 在整场直播过程中, 聊天(闲聊, 互动)所占时间比重是最大的, 大约80%, 其余20%包括唱歌, 跳舞, 其他等. 所以, 对于比较喜欢听主播唱歌的观众来讲, 怎样迅速找到 **正在唱歌** 的直播间是一个比较痛点的需求.

针对该问题, 本文提出了利用深度学习对直播间声音信号进行分类的方案, 下面进行详细介绍.


## 摘要

在解决 **是否在唱歌** 的问题之前, 优先解决如下问题

- 这是一个语音项目, 公司没相关技术储备, 可选择的方法不详.
- 获取语音数据, 及其处理.

为了解决上述两个问题, 我们(我与实习生)进行了分工, 我调研了语音项目相关的技术, 实习生负责数据的采集的处理. 最后选定

- [VGGish][vggish] + 简单分类器 作为语音解决办法.
- 抽取直播间音频作为数据来源, 标注唱歌部分(区间), 训练时会将这些区间进一步拆分为等长的片段.

## 概述

### 使用场景

本文提出的算法, 使用场景如下

- 识别声音片段是否为唱歌状态
- 识别声音片段是否为其他状态

### 算法流程

使用深度学习(机器学习)开发时一般分为 **训练** 和 **预测** 两个阶段. 训练是指利用算法在已有数据上拟合(学习)出一些规律或法则(模型), 预测是指使用训练生成的模型对新数据进行预测.

训练分为三步:

- 基于梅尔倒频谱算法, 提取声音片段的特征, 并将其转换成频谱图片.
- 将频谱图片输入至 VGGish 网络(直接加载已有 [checkpoint][vggish-ckpt])进一步提取图形特征(embedding)
- 将 embedding 输入 **简单分类网络** 进行训练, 得到分类模型

预测与训练除第三步外完全一致: 先提取声音特征, 然后加载训练好的模型即可获得预测结果.



[vggish]: https://github.com/tensorflow/models/tree/master/research/audioset
[vggish-ckpt]: https://storage.googleapis.com/audioset/vggish_model.ckpt
[ytb8m]: https://research.google.com/youtube8m
[data-urban]: https://serv.cusp.nyu.edu/projects/urbansounddataset/
[tf-ac]: https://github.com/luuil/tensorflow-audio-classification
