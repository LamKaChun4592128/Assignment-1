import re
from collections import Counter

import jieba
import matplotlib.pyplot as plt

with open("沉沦.txt", encoding="utf-8-sig") as f:
    text = f.read()

words = [
    w for w in (t.strip() for t in jieba.lcut(text))
    if w and re.search(r"[\u4e00-\u9fffA-Za-z0-9]", w)
]

counts = Counter(words)

for word, freq in counts.most_common(10):
    print(f"{word}\t{freq}")

top100 = counts.most_common(100)
fig, ax = plt.subplots(figsize=(15, 5))
ax.bar(range(len(top100)), [freq for _, freq in top100], width=1.0)
ax.set_axis_off()
fig.tight_layout()
fig.savefig("top100_words.png", dpi=150)
