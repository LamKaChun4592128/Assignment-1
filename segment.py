import re
import unicodedata

import jieba
import opencc

INPUT_FILE = "data/novel.txt"
OUTPUT_FILE = "sentences.txt"
MIN_WORDS = 5


def is_word(token):
    return token and all(
        unicodedata.category(ch)[0] in ("L", "N") for ch in token
    )


def main():
    with open(INPUT_FILE, encoding="utf-8-sig") as f:
        text = f.read()

    converter = opencc.OpenCC("t2s")
    text = converter.convert(text)

    sentences = re.split(r"[。！？]", text)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        kept = 0
        for sentence in sentences:
            words = [w for w in jieba.lcut(sentence) if is_word(w)]
            if len(words) >= MIN_WORDS:
                f.write(" ".join(words) + "\n")
                kept += 1

    print(f"Wrote {kept} sentences (>= {MIN_WORDS} words) to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()