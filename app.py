import os.path
import time
import warnings

import gradio as gr
import whisper
from pygtrans import Translate
from whisper.tokenizer import LANGUAGES, TO_LANGUAGE_CODE

warnings.simplefilter(action="ignore", category=UserWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)

# https://github.com/openai/whisper
MODELS = {
    # "tiny": whisper.load_model("tiny"),
    # "tiny.en": whisper.load_model("tiny.en"),
    # "base": whisper.load_model("base"),
    # "base.en": whisper.load_model("base.en"),
    # "small": whisper.load_model("small"),
    # "small.en": whisper.load_model("small.en"),
    # "medium": whisper.load_model("medium"),
    # "medium.en": whisper.load_model("medium.en"),
    # "large": whisper.load_model("large"),
    "turbo": whisper.load_model("turbo"),
}
MODEL_LANG_CODES = {"Auto Detect": "None"}
MODEL_LANG_CODES.update(TO_LANGUAGE_CODE)
MODEL_CODE_LANGS = {v: k for k, v in MODEL_LANG_CODES.items()}

# https://github.com/foyoux/pygtrans
AT = Translate(target="zh-CN", fmt="text")
SRTS_DIR = "assets/srts"
SRT_LANGUAGES = {
    "Chinese (Simplified)": "zh-CN",
    "Abkhaz": "ab",
    "Acehnese": "ace",
    "Acholi": "ach",
    "Afar": "aa",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Alur": "alz",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Assamese": "as",
    "Avar": "av",
    "Awadhi": "awa",
    "Aymara": "ay",
    "Azerbaijani": "az",
    "Balinese": "ban",
    "Baluchi": "bal",
    "Bambara": "bm",
    "Baoulé": "bci",
    "Bashkir": "ba",
    "Basque": "eu",
    "Batak Karo": "btx",
    "Batak Simalungun": "bts",
    "Batak Toba": "bbc",
    "Belarusian": "be",
    "Bemba": "bem",
    "Bengali": "bn",
    "Betawi": "bew",
    "Bhojpuri": "bho",
    "Bikol": "bik",
    "Bosnian": "bs",
    "Breton": "br",
    "Bulgarian": "bg",
    "Buryat": "bua",
    "Cantonese": "yue",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chamorro": "ch",
    "Chechen": "ce",
    "Chichewa": "ny",
    # "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Chuukese": "chk",
    "Chuvash": "cv",
    "Corsican": "co",
    "Crimean Tatar": "crh",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dari": "fa-AF",
    "Dhivehi": "dv",
    "Dinka": "din",
    "Dogri": "doi",
    "Dombe": "dov",
    "Dutch": "nl",
    "Dyula": "dyu",
    "Dzongkha": "dz",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Ewe": "ee",
    "Faroese": "fo",
    "Fijian": "fj",
    "Filipino": "tl",
    "Finnish": "fi",
    "Fon": "fon",
    "French": "fr",
    "Frisian": "fy",
    "Friulian": "fur",
    "Fulani": "ff",
    "Ga": "gaa",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Guarani": "gn",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hakha Chin": "cnh",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "iw",
    "Hiligaynon": "hil",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Hunsrik": "hrx",
    "Iban": "iba",
    "Icelandic": "is",
    "Igbo": "ig",
    "Ilocano": "ilo",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Jamaican Patois": "jam",
    "Japanese": "ja",
    "Javanese": "jw",
    "Jingpo": "kac",
    "Kalaallisut": "kl",
    "Kannada": "kn",
    "Kanuri": "kr",
    "Kapampangan": "pam",
    "Kazakh": "kk",
    "Khasi": "kha",
    "Khmer": "km",
    "Kiga": "cgg",
    "Kikongo": "kg",
    "Kinyarwanda": "rw",
    "Kituba": "ktu",
    "Kokborok": "trp",
    "Komi": "kv",
    "Konkani": "gom",
    "Korean": "ko",
    "Krio": "kri",
    "Kurdish (Kurmanji)": "ku",
    "Kurdish (Sorani)": "ckb",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latgalian": "ltg",
    "Latin": "la",
    "Latvian": "lv",
    "Ligurian": "lij",
    "Limburgish": "li",
    "Lingala": "ln",
    "Lithuanian": "lt",
    "Lombard": "lmo",
    "Luganda": "lg",
    "Luo": "luo",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Madurese": "mad",
    "Maithili": "mai",
    "Makassar": "mak",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malay (Jawi)": "ms-Arab",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Mam": "mam",
    "Manx": "gv",
    "Maori": "mi",
    "Marathi": "mr",
    "Marshallese": "mh",
    "Marwadi": "mwr",
    "Mauritian Creole": "mfe",
    "Meadow Mari": "chm",
    "Meiteilon (Manipuri)": "mni-Mtei",
    "Minang": "min",
    "Mizo": "lus",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nahuatl (Eastern Huasteca)": "nhe",
    "Ndau": "ndc-ZW",
    "Ndebele (South)": "nr",
    "Nepalbhasa (Newari)": "new",
    "Nepali": "ne",
    "NKo": "bm-Nkoo",
    "Norwegian": "no",
    "Nuer": "nus",
    "Occitan": "oc",
    "Odia (Oriya)": "or",
    "Oromo": "om",
    "Ossetian": "os",
    "Pangasinan": "pag",
    "Papiamento": "pap",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese (Brazil)": "pt",
    "Portuguese (Portugal)": "pt-PT",
    "Punjabi (Gurmukhi)": "pa",
    "Punjabi (Shahmukhi)": "pa-Arab",
    "Quechua": "qu",
    "Qʼeqchiʼ": "kek",
    "Romani": "rom",
    "Romanian": "ro",
    "Rundi": "rn",
    "Russian": "ru",
    "Sami (North)": "se",
    "Samoan": "sm",
    "Sango": "sg",
    "Sanskrit": "sa",
    "Santali": "sat-Latn",
    "Scots Gaelic": "gd",
    "Sepedi": "nso",
    "Serbian": "sr",
    "Sesotho": "st",
    "Seychellois Creole": "crs",
    "Shan": "shn",
    "Shona": "sn",
    "Sicilian": "scn",
    "Silesian": "szl",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Susu": "sus",
    "Swahili": "sw",
    "Swati": "ss",
    "Swedish": "sv",
    "Tahitian": "ty",
    "Tajik": "tg",
    "Tamazight": "ber-Latn",
    "Tamazight (Tifinagh)": "ber",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Tetum": "tet",
    "Thai": "th",
    "Tibetan": "bo",
    "Tigrinya": "ti",
    "Tiv": "tiv",
    "Tok Pisin": "tpi",
    "Tongan": "to",
    "Tsonga": "ts",
    "Tswana": "tn",
    "Tulu": "tcy",
    "Tumbuka": "tum",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Tuvan": "tyv",
    "Twi": "ak",
    "Udmurt": "udm",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Venda": "ve",
    "Venetian": "vec",
    "Vietnamese": "vi",
    "Waray": "war",
    "Welsh": "cy",
    "Wolof": "wo",
    "Xhosa": "xh",
    "Yakut": "sah",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Yucatec Maya": "yua",
    "Zapotec": "zap",
    "Zulu": "zu",
}


def translate(text: str, srt_lang, srt_file, audio):
    if not srt_file:
        gr.Warning("Please transcribe the audio first")
        return gr.skip()
    start_time = time.time()
    srts = []
    for i in text.strip().split('\n\n'):
        i = i.strip().split('\n')
        a = i[0]
        b = i[1]
        c = '\n'.join(i[2:])
        srts.append((a, b, c))
    trans = AT.translate([i[2] for i in srts], target=srt_lang)
    srt_trans = []
    for i, j in zip(srts, trans):
        srt_trans.append(i[0])
        srt_trans.append(i[1])
        srt_trans.append(j.translatedText)
        srt_trans.append("")
    translation = '\n'.join(srt_trans)
    file_name = os.path.splitext(os.path.basename(audio))[0]
    end_time = time.time()
    return generate_file(file_name, translation, srt_lang), gr.Text(
        translation, info=f"Time: {end_time - start_time:.2f} seconds"
    )


def generate_srt(results):
    srts = []
    for i in results["segments"]:
        srts.append(f'{i["id"] + 1}')
        srts.append(
            f"{seconds_to_srt_time(i['start'])} --> {seconds_to_srt_time(i['end'])}"
        )
        srts.append(i["text"])
        srts.append("")
    return "\n".join(srts)


def seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def generate_file(file_name, srt, code):
    os.makedirs(SRTS_DIR, exist_ok=True)
    file_path = os.path.join(SRTS_DIR, f"{file_name}-{code}.srt")
    with open(file_path, "w") as f:
        f.write(srt)
    return file_path


def transcribe(model, model_lang, audio):
    if not audio:
        gr.Warning("Please upload an audio file")
        return gr.skip()
    if model_lang == "None":
        model_lang = None
    start_time = time.time()
    file_name = os.path.splitext(os.path.basename(audio))[0]
    results = MODELS[model].transcribe(audio, language=model_lang)
    code = results["language"]
    language = LANGUAGES.get(code, MODEL_CODE_LANGS.get(code, "Unknown"))
    srt = generate_srt(results)
    end_time = time.time()
    return generate_file(file_name, srt, code), gr.Text(
        srt,
        info=f"Language: {language}, Time: {end_time - start_time:.2f} seconds",
    )


def main():
    with gr.Blocks(analytics_enabled=False) as demo:
        with gr.Row():
            with gr.Column():
                choices = list(MODELS.keys())
                model = gr.Radio(choices=choices, value=choices[0], label="Model")
                model_lang = gr.Dropdown(
                    [(k, v) for k, v in MODEL_LANG_CODES.items()],
                    value="None",
                    label="Audio Language",
                )
                audio = gr.File(label="Audio/Video")
                transcribe_btn = gr.Button("Transcribe")
            with gr.Column():
                srt_file1 = gr.File(label="Transcription SRT File")
                transcribe_text = gr.Text(
                    label="Transcription",
                    lines=10,
                    max_lines=20,
                    autoscroll=False,
                    interactive=False,
                )
                srt_lang = gr.Dropdown(
                    [(k, v) for k, v in SRT_LANGUAGES.items()],
                    value="zh-CN",
                    label="SRT Language",
                )
                translate_btn = gr.Button("Translate")
            with gr.Column():
                srt_file2 = gr.File(label="Translation SRT File")
                translate_text = gr.Text(
                    label="Translation", lines=10, max_lines=20, autoscroll=False
                )
        audio.clear(
            lambda: (
                gr.Text(None, info=None),
                gr.Text(None, info=None),
                None,
                None,
            ),
            outputs=[transcribe_text, translate_text, srt_file1, srt_file2],
        )
        transcribe_btn.click(
            transcribe,
            inputs=[model, model_lang, audio],
            outputs=[srt_file1, transcribe_text],
        )
        translate_btn.click(
            translate,
            inputs=[transcribe_text, srt_lang, srt_file1, audio],
            outputs=[srt_file2, translate_text],
        )
    demo.launch(allowed_paths=["assets/srts"])


if __name__ == "__main__":
    main()
