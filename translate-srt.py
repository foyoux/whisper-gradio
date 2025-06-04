import argparse
from pathlib import Path

from pygtrans import Translate
from tqdm import tqdm


def parse_args(parser):
    parser.add_argument("--source", nargs="?", const=None, default="auto", help="Source language of the subtitles")
    parser.add_argument(
        "--target", nargs="?", const=None, default="zh-CN", help="Target language for the translated subtitles"
    )
    parser.add_argument("--proxy", help="Proxy for translate subtitles")
    parser.add_argument("srts", nargs="*", help="subtitles file or folder")
    return parser.parse_args()


def process(file: Path, target, at: Translate):
    text = file.read_text(encoding="utf8")
    srts = []
    for i in text.strip().split("\n\n"):
        i = i.strip().split("\n")
        a = i[0]
        b = i[1]
        c = "\n".join(i[2:])
        srts.append((a, b, c))
    trans = at.translate([i[2] for i in srts], target=target)
    srt_trans = []
    for i, j in zip(srts, trans):
        srt_trans.append(i[0])
        srt_trans.append(i[1])
        srt_trans.append(j.translatedText)
        srt_trans.append("")
    translation = "\n".join(srt_trans)
    file.with_name(f"{file.stem}-{target}.srt").write_text(translation, encoding="utf8")


def main():
    parser = argparse.ArgumentParser()
    args = parse_args(parser)

    if not args.srts:
        parser.print_help()
        return

    all_srts = set()
    for i in tqdm(args.srts, desc="收集文件"):
        j = Path(i)
        if j.is_file():
            all_srts.add(j)
        else:
            for k in j.rglob("*.srt"):
                all_srts.add(k)

    at = Translate(
        source=args.source, target=args.target, fmt="text", proxies={"https": args.proxy} if args.proxy else None
    )
    with tqdm(total=len(all_srts), desc="转录字幕") as pbar:
        for i in all_srts:
            pbar.set_postfix_str(i)
            process(i, target=args.target, at=at)
            pbar.update(1)


if __name__ == "__main__":
    main()
