# shenji_sum

## 会议纪要关系抽取

- pdf、docx文件解析成txt

```
python file2txt/file2txt.py --file_dir ./data/file --result_file_dir ./data/txt
```

其中 `--file_dir` 为要总结的原文件所在的目录， `--result_file_dir` 为解析结果 txt 输出目录

- 大模型总结文件中的时间、事件和金额

```
python llm/run.py --file_dir ./data/txt --result_file_dir ./data/llm_output
```

其中 `--file_dir` 为上一步解析结果 txt 输出目录， `--result_file_dir` 大模型对会议纪要进行抽取之后的结果输出目录

- 画图

```
python merge_and_draw/draw_graph.py --file_dir ./data/llm_output --d_threshold 5
```

其中 `--file_dir` 为大模型抽取结果的 txt 所在目录， `--d_threshold` 判断两个节点是否融合编辑距离的阈值

## 会议纪要总结

```
python summary/summary.py --file_dir ./data/txt --result_file_dir ./data/summary
```

其中 `--file_dir` 为文件解析结果 txt 输出目录， `--result_file_dir` 会议纪要总结输出目录

----------------------------

## ps: 关键技术方案简要说明

### 会议纪要关系抽取

1. 大模型分别抽取会议纪要中的三种信息（时间、事件、金额）
2. 解析大模型的输出得到 nodes，links 的二元组格式，然后将相似的 node 进行合并，判断相似性的方法为编辑距离，如果两个 node
   的编辑距离小于某个阈值，则判定为同一个 node， 进而将这两个 node 合并

### 会议纪要总结

1. 直接利用大模型总结会议纪要文本