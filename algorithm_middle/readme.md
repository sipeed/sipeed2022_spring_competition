# 算法中级题
免训练的目标检测

## 题目描述
我们已经见惯了各种trick的目标检测，比如各种yolo。  
但是这些模型无一例外都需要采集大量的数据集图片，进行繁重的标注，并进行长时间的训练。  
你是否设想过免训练的目标检测？只需要提供一张目标物体的图片，即可自动学习到物体特征，实现自动追踪，或者自动标注？  
（知道这个问题名词的老鸟可以先保密 ^_^）

操作步骤：  
1. 提供一张目标物体的128x128的小图作为模型初始参考（实际模型可以自行使用缩放的尺寸，如64x64）
2. 提供一段几十秒的 224x224 的小视频，其中有目标物体的影像，包含了旋转，尺度缩放，角度变化，移出视野等情况（参考视频在本目录下）
3. 模型仅通过步骤1的数据进行“学习”，在步骤2的视频中将目标物体框出来  

模型要求：
1. 必须使用深度学习模型，不能使用传统视觉方法（特征点），不可以使用在线学习的方式  
2. 只能使用普通卷积为主的结构，不能使用transformer结构，其它算子以NCNN默认支持为准  
3. 模型输入：视频输入224x224，初始目标图片输入可任意自定
4. 模型输出：不限，但最终后处理后需要输出目标物体的位置框和概率
5. 模型尺寸：1MB以内
6. 模型速率：以树莓派4为基准，在树莓派4上达到单核20帧以上，或者R329纯CPU计算单核达到10帧以上速度。

部署要求
1. 最终使用NCNN进行部署，目标平台为ARMv8，NCNN不支持的算子需要自行手写实现  
2. 部署硬件平台可选 树莓派4（A72），Sipeed MaixSense（R329 A53）  
   1. 购买链接（https://item.taobao.com/item.htm?id=652879327858）

测试程序要求：
1. 输入参数为待测物体图片路径，待测视频路径，输出视频路径
   1. 如 ./autodet dest.jpg dest.mp4 output.mp4
2. 输出视频文件里需要用红框标注目标物体，运行帧率

对于合格的中级算法工程师，本赛题的参考用时为3～5天。

## 提交内容
参赛者请在2022.3.31前提交结果  
提交邮箱： support@sipeed.com  
邮件标题：[矽速挑战赛] 算法中级组 参赛者名（可以是昵称）  
邮件内容：参赛者的基本信息（姓名，学校/公司，联系方式等），阐述基本的工作流程，优化点等  
附件内容：训练工程文件，预训练模型，及对应的测试程序  

## 评比方法
1. 在测试视频中，不出现明显的误检测，未检测情况，目标物体移出视野后重新进入可以快速检测回来  
2. 帧率需要在 在树莓派4上达到单核20帧以上，或者R329达到纯CPU单核10帧以上速度
3. 未完成以上要求的没有评奖资格
4. 本赛题最终解释权归矽速科技所有。

## 成绩天梯
参赛者的测试结果会在比赛期间及时更新到本节

