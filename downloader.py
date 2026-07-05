#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║         GORDON DOWNLOADER               ║
║     محمّل الفيديوهات من كل المواقع      ║
╚══════════════════════════════════════════╝
يدعم: YouTube, Instagram, Facebook, TikTok,
      Snapchat, Twitter/X, Vimeo, وأكثر من 1000 موقع
"""

import sys
import os
import subprocess

# ألوان
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def banner():
    print(f"""
{CYAN}{BOLD}
 ██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ 
 ██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗
 ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║
 ██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║
 ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝
 ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
{RESET}
{YELLOW}   محمّل الفيديوهات - يدعم أكثر من 1000 موقع{RESET}
    """)

def check_ytdlp():
    """التحقق من تثبيت yt-dlp"""
    try:
        subprocess.run(["yt-dlp", "--version"],
                       capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_ytdlp():
    """تثبيت yt-dlp تلقائياً"""
    print(f"{YELLOW}[*] جاري تثبيت yt-dlp...{RESET}")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"],
                       check=True)
        print(f"{GREEN}[✓] تم تثبيت yt-dlp بنجاح{RESET}")
        return True
    except subprocess.CalledProcessError:
        print(f"{RED}[!] فشل التثبيت. جرب: pip install yt-dlp{RESET}")
        return False

def get_video_info(url: str) -> dict:
    """جلب معلومات الفيديو"""
    try:
        import yt_dlp
        ydl_opts = {"quiet": True, "no_warnings": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title":    info.get("title", "Unknown"),
                "uploader": info.get("uploader", "Unknown"),
                "duration": info.get("duration", 0),
                "views":    info.get("view_count", 0),
                "platform": info.get("extractor_key", "Unknown"),
            }
    except Exception as e:
        return {"error": str(e)}

def download_video(url: str, quality: str, output_dir: str, audio_only: bool = False):
    """تحميل الفيديو"""
    import yt_dlp

    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    if audio_only:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    else:
        fmt_map = {
            "1": "bestvideo[height<=1080]+bestaudio/best",
            "2": "bestvideo[height<=720]+bestaudio/best",
            "3": "bestvideo[height<=480]+bestaudio/best",
            "4": "best",
        }
        fmt = fmt_map.get(quality, "best")
        ydl_opts = {
            "format": fmt,
            "outtmpl": output_template,
            "merge_output_format": "mp4",
        }

    print(f"\n{CYAN}[*] جاري التحميل...{RESET}\n")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n{GREEN}[✓] تم التحميل بنجاح في مجلد: {output_dir}{RESET}")
    except Exception as e:
        print(f"\n{RED}[!] فشل التحميل: {e}{RESET}")

def format_duration(seconds):
    if not seconds:
        return "غير معروف"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

def format_views(n):
    if not n:
        return "غير معروف"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)

def main():
    banner()

    # التحقق من yt-dlp
    if not check_ytdlp():
        if not install_ytdlp():
            sys.exit(1)

    while True:
        print(f"\n{CYAN}{'═'*55}{RESET}")
        url = input(f"{WHITE}[؟] أدخل رابط الفيديو (أو 'خروج' للإنهاء): {RESET}").strip()

        if url.lower() in ("خروج", "exit", "quit", "q"):
            print(f"\n{YELLOW}وداعاً!{RESET}\n")
            break

        if not url:
            continue

        # جلب معلومات الفيديو
        print(f"\n{CYAN}[*] جاري جلب معلومات الفيديو...{RESET}")
        info = get_video_info(url)

        if "error" in info:
            print(f"{RED}[!] خطأ: {info['error']}{RESET}")
            continue

        # عرض المعلومات
        print(f"\n{YELLOW}{'─'*45}{RESET}")
        print(f"  {BOLD}📹 العنوان  :{RESET} {info['title'][:60]}")
        print(f"  {BOLD}👤 الناشر  :{RESET} {info['uploader']}")
        print(f"  {BOLD}⏱ المدة    :{RESET} {format_duration(info['duration'])}")
        print(f"  {BOLD}👁 المشاهدات:{RESET} {format_views(info['views'])}")
        print(f"  {BOLD}🌐 المنصة  :{RESET} {info['platform']}")
        print(f"{YELLOW}{'─'*45}{RESET}")

        # خيار الصوت أو الفيديو
        print(f"\n{YELLOW}نوع التحميل:{RESET}")
        print("  1) فيديو 🎬")
        print("  2) صوت فقط MP3 🎵")
        type_choice = input(f"{WHITE}[؟] اختر (1/2): {RESET}").strip() or "1"
        audio_only = type_choice == "2"

        quality = "4"
        if not audio_only:
            print(f"\n{YELLOW}الجودة:{RESET}")
            print("  1) 1080p عالية جداً")
            print("  2) 720p  عالية")
            print("  3) 480p  متوسطة")
            print("  4) أفضل جودة متاحة (افتراضي)")
            quality = input(f"{WHITE}[؟] اختر (1/2/3/4): {RESET}").strip() or "4"

        # مجلد الحفظ
        default_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Gordon")
        out = input(f"{WHITE}[؟] مجلد الحفظ (افتراضي: {default_dir}): {RESET}").strip()
        output_dir = out if out else default_dir

        download_video(url, quality, output_dir, audio_only)

        again = input(f"\n{WHITE}[؟] هل تريد تحميل فيديو آخر؟ (y/n): {RESET}").strip().lower()
        if again != "y":
            print(f"\n{YELLOW}وداعاً!{RESET}\n")
            break

if __name__ == "__main__":
    main()
