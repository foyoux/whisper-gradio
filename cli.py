import argparse
from pathlib import Path

import whisper
from pygtrans import TARGET_LANGUAGES
from pygtrans import Translate
from tqdm import tqdm
from whisper.tokenizer import TO_LANGUAGE_CODE

MODELS = [
    "tiny.en",
    "tiny",
    "base.en",
    "base",
    "small.en",
    "small",
    "medium.en",
    "medium",
    "large-v1",
    "large-v2",
    "large-v3",
    "large",
    "large-v3-turbo",
    "turbo",
]
SOURCES = [i for i in TO_LANGUAGE_CODE]
# fmt: off
AUDIO_SUFFIXS = {
    ".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm", ".3gp", ".mpeg", ".mpg", ".m4v",
    ".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma",  # '.aiff', '.alac'
}
# fmt: on


def print_models():
    print("Available models:")
    for model in MODELS:
        print(f"  - {model}")


def print_sources():
    print("Available source languages:")
    for source in SOURCES:
        print(f"  - {TO_LANGUAGE_CODE[source]}({source})")


def print_targets():
    print("Available target languages:")
    for code, name in TARGET_LANGUAGES.items():
        print(f"  - {code} ({name})")


def parse_args(parser):
    parser.add_argument("--model", nargs="?", const=None, default="turbo", help="Model to use for whisper")
    parser.add_argument("--source", nargs="?", const=False, default=None, help="Source language of the audio")
    parser.add_argument(
        "--target", nargs="?", const=None, default="zh-CN", help="Target language for the translated subtitles"
    )
    parser.add_argument("--proxy", help="Proxy for translate subtitles")
    parser.add_argument("files", nargs="*", help="Audio/video file or folder")
    return parser.parse_args()


def seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def generate_srt(results):
    srts = []
    for i in results["segments"]:
        srts.append(f'{i["id"] + 1}')
        srts.append(f"{seconds_to_srt_time(i['start'])} --> {seconds_to_srt_time(i['end'])}")
        srts.append(i["text"])
        srts.append("")
    return "\n".join(srts)


def save_srt(file: Path, lang, srt):
    file.with_name(f"{file.stem}-{lang}.srt").write_text(srt, encoding="utf8")


def process(model, file, source, target, at: Translate):
    results = model.transcribe(str(file), language=source)
    source_srt = generate_srt(results)
    save_srt(file, results["language"], source_srt)
    texts = [i["text"] for i in results["segments"]]
    target_texts = at.translate(texts)
    for k, v in zip(results["segments"], target_texts):
        k["text"] = v.translatedText
    target_srt = generate_srt(results)
    save_srt(file, target, target_srt)


def main():
    parser = argparse.ArgumentParser()
    args = parse_args(parser)
    if args.model is None:
        print_models()
        return
    if args.source is False:
        print_sources()
        return
    if args.target is None:
        print_targets()
        return

    if not args.files:
        parser.print_help()
        return

    all_files = set()
    for i in tqdm(args.files, desc="收集文件"):
        j = Path(i)
        if j.is_file():
            all_files.add(j)
        else:
            for k in j.rglob("*"):
                if k.suffix.lower() in AUDIO_SUFFIXS:
                    all_files.add(k)

    at = Translate(target=args.target, fmt="text", proxies={"https": args.proxy} if args.proxy else None)
    model = whisper.load_model(args.model)
    with tqdm(total=len(all_files), desc="转录字幕") as pbar:
        for i in all_files:
            pbar.set_postfix_str(i)
            process(model, i, source=args.source, target=args.target, at=at)
            pbar.update(1)


if __name__ == "__main__":
    main()
