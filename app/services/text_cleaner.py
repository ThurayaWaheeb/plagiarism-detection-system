import re


def optimal_arabic_cleaner(text: str) -> str:

    tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = re.sub(tashkeel, '', text)

    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ـ', '', text)

    text = re.sub(r'[^\u0600-\u06FF0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text


ignore_sections = [
    "الشكر والتقدير",
    "صفحة الغلاف",
    "الفهرس",
    "المراجع",
    "قائمة المراجع",
    "الملخص",
    "Abstract"
]

def remove_unwanted_sections(text):

    ignore_sections = [
        "الشكر والتقدير",
        "صفحة الغلاف",
        "الفهرس",
        "المراجع",
        "قائمة المراجع",
        "Abstract"
    ]

    lines = text.split("\n")

    filtered_lines = []

    for line in lines:

        if any(section in line for section in ignore_sections):
            continue

        filtered_lines.append(line)

    return "\n".join(filtered_lines)