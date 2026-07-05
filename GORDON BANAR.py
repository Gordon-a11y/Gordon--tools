#!/usr/bin/env python3
"""
==========================================
   GORDON BANNER TOOL
==========================================
أداة متطورة لتوليد بانرات/شعارات ASCII
بخطوط وأشكال وألوان متعددة

تثبيت المتطلبات (مرة وحدة فقط):
    pip install pyfiglet

تشغيل:
    python banner.py
"""

import os
import sys
import random

try:
    import pyfiglet
except ImportError:
    print("المكتبة pyfiglet غير مثبتة.")
    print("نزّلها بهذا الأمر:  pip install pyfiglet")
    sys.exit(1)


# ---------------------------------------------------------------------------
# الألوان (ANSI escape codes) - تعمل على ترموكس ولينكس وماك
# ---------------------------------------------------------------------------
COLORS = {
    "1": ("أحمر",      "\033[91m"),
    "2": ("أخضر",      "\033[92m"),
    "3": ("أصفر",      "\033[93m"),
    "4": ("أزرق",      "\033[94m"),
    "5": ("بنفسجي",    "\033[95m"),
    "6": ("سماوي",     "\033[96m"),
    "7": ("أبيض",      "\033[97m"),
    "8": ("بدون لون",  ""),
}
RESET = "\033[0m"
RAINBOW = ["\033[91m", "\033[93m", "\033[92m", "\033[96m", "\033[94m", "\033[95m"]


# ---------------------------------------------------------------------------
# الخطوط (Fonts) - مجموعة كبيرة ومتنوعة من الأشكال
# ---------------------------------------------------------------------------
FONTS = [
    "ansi_shadow", "standard", "slant", "big", "block", "bubble", "digital",
    "doom", "shadow", "small", "smslant", "starwars", "banner3-D", "alphabet",
    "avatar", "basic", "bell", "bigfig", "binary", "bulbhead", "chunky",
    "colossal", "computer", "cosmic", "cricket", "cyberlarge", "diamond",
    "doh", "dotmatrix", "drpepper", "epic", "fender", "fuzzy", "goofy",
    "gothic", "graffiti", "hollywood", "isometric1", "larry3d", "lean",
    "letters", "lineblocks", "madrid", "marquee", "maxfour", "mini",
    "mirror", "nancyj", "ntgreek", "ogre", "pawp", "peaks", "pebbles",
    "puffy", "rectangles", "relief", "rev", "roman", "rounded", "script",
    "short", "slscript", "smkeyboard", "speed", "stacey", "stampatello",
    "straight", "tanja", "thick", "thin", "threepoint", "tinker-toy",
    "tombstone", "trek", "twopoint", "wavy", "weird",
]


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def colorize(text: str, color_code: str, rainbow: bool = False) -> str:
    if rainbow:
        lines = text.split("\n")
        out = []
        for i, line in enumerate(lines):
            c = RAINBOW[i % len(RAINBOW)]
            out.append(f"{c}{line}{RESET}")
        return "\n".join(out)
    if color_code:
        return f"{color_code}{text}{RESET}"
    return text


def render(text: str, font: str) -> str:
    try:
        fig = pyfiglet.Figlet(font=font)
        return fig.renderText(text)
    except pyfiglet.FontNotFound:
        return None


def show_logo():
    """شعار الأداة نفسها GORDON عند بدء التشغيل"""
    banner = render("GORDON", "ansi_shadow") or render("GORDON", "standard")
    print(colorize(banner, "", rainbow=True))
    print("        أداة توليد بانرات ASCII - تطوير Gordon Tool\n")
    print("=" * 60)


def pick_font() -> str:
    print("\nاختر شكل الخط (اكتب رقم) أو 0 لخط عشوائي:")
    for i, f in enumerate(FONTS, start=1):
        print(f"{i:>2}. {f}")
    choice = input("\nرقمك: ").strip()
    if choice == "0" or not choice.isdigit():
        return random.choice(FONTS)
    idx = int(choice)
    if 1 <= idx <= len(FONTS):
        return FONTS[idx - 1]
    return random.choice(FONTS)


def pick_color() -> tuple:
    print("\nاختر اللون:")
    for k, (name, _) in COLORS.items():
        print(f"{k}. {name}")
    print("9. قوس قزح (rainbow)")
    choice = input("\nرقمك: ").strip()
    if choice == "9":
        return ("", True)
    if choice in COLORS:
        return (COLORS[choice][1], False)
    return ("", False)


def generate_one():
    text = input("\nاكتب الاسم/النص: ").strip()
    if not text:
        print("لازم تكتب نص!")
        return

    font = pick_font()
    color_code, rainbow = pick_color()

    banner = render(text, font)
    if banner is None:
        print(f"\nالخط '{font}' غير متوفر، رجاءً جرب خط تاني.")
        return

    print()
    print(colorize(banner, color_code, rainbow))
    print(f"الخط المستخدم: {font}")

    save = input("\nبدك تحفظه بملف؟ (y/n): ").strip().lower()
    if save == "y":
        filename = f"{text}_{font}.txt".replace(" ", "_")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(banner)
        print(f"تم الحفظ: {filename}")


def generate_all_shapes():
    """يطبع نفس النص بكل الخطوط المتوفرة دفعة واحدة - أشكال كتيرة بضغطة واحدة"""
    text = input("\nاكتب الاسم/النص: ").strip()
    if not text:
        print("لازم تكتب نص!")
        return

    for font in FONTS:
        banner = render(text, font)
        if banner is None:
            continue
        print(f"\n--- {font} ---")
        print(colorize(banner, random.choice(RAINBOW)))


def main():
    clear()
    show_logo()

    while True:
        print("\nالقائمة:")
        print("1. توليد بانر (اختيار خط ولون)")
        print("2. عرض نفس النص بكل الأشكال دفعة واحدة")
        print("3. خروج")

        choice = input("\nاختيارك: ").strip()

        if choice == "1":
            generate_one()
        elif choice == "2":
            generate_all_shapes()
        elif choice == "3":
            print("\nتم الإغلاق. سلام!")
            break
        else:
            print("اختيار غير صحيح.")


if __name__ == "__main__":
    main()