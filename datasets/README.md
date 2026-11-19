# 数据制作与评价材料

本目录保存数据规格、制作配方、合成样例与检查代码。原始媒体、模型输出和大型标注数据外置，通过来源清单与校验信息引用。

- [多镜头与主体参考配方](recipes/multishot-reference/README.md)
- [场景记录 Schema](schemas/scene-record.schema.json)
- [纯文字合成样例](examples/synthetic-scenes.jsonl)：只用于演示记录格式，不是训练集。

划分应按场景、原始视频或主体来源成组，避免同一来源的相邻镜头进入不同集合。素材的可访问性、训练权利与再分发权利分别登记。
