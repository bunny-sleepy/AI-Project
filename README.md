# AI-Project
为了能够运行这个项目, 请先确保电脑上拥有python3.7或更高版本和tensorflow
如果没有tensorflow, 请先使用命令`pip install tensorflow` 或者使用 `pip install --upgrade tensorflow`

之后, 请运行命令`pip install magenta`

请先在云盘上下载coconet已经训练好的节点, 可以在清华云盘上查看.

为了使用coconet, 请先安装**git bash**

之后, 在coconet所在目录下运行git bash, 输入以下命令

`sh my_bazel.sh $model_path(folder) $file_to_harmonize_path(file)`



*2020.11.29更新*

在使用bert之前, 先安装包**transformers**, 在cmd运行如下命令:

`pip3 install transformers`

或`pip install transformers`

注意不要装到python2里面了



## 中期总结

### 问题分析

1. **数据集爬取 (已完成)**
2. 数据集处理 (未完成)
3. NLP模型现在使用maxpooling, 但需要修改 (未完成)
4. **coconet 的 harmonize 函数 (未完成)**
5. midi 主旋律提取 (未完成)
6. midi 标题处理 (未完成)
7. **midi 合法性 (未完成)**
8. **模型整合 (未完成)**