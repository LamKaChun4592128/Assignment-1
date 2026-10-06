import re

import jieba
import opencc

CONVERTER = opencc.OpenCC("t2s")
SENTENCE_DELIMS = "。！？"
MIN_WORDS = 5
PUNCT_RE = re.compile(r"[\u4e00-\u9fffA-Za-z0-9]")


def main():
    with open("data/novel.txt", encoding="utf-8-sig") as f:
        text = CONVERTER.convert(f.read())

    sentences = []
    for part in re.split(f"[{SENTENCE_DELIMS}]", text):
        words = [
            w for w in (t.strip() for t in jieba.lcut(part))
            if w and PUNCT_RE.search(w)
        ]
        if len(words) >= MIN_WORDS:
            sentences.append(" ".join(words))

    with open("sentences.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sentences) + "\n")

    print(f"{len(sentences)} sentences written to sentences.txt")


if __name__ == "__main__":
    main()
