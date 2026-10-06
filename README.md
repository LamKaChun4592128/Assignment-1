- 书名：西游记
- 作者：吴承恩
- 来源：https://ctext.org/xiyouji
- `data/`：语料纯文本
- `output/`：CSV 与 HTML 结果
- `scripts/`：Python 脚本
- 使用 qhchina `find_collocates`
- opencc 繁转简
- jieba 分词
- 停用词过滤
```bash
python scripts/analyze.py
