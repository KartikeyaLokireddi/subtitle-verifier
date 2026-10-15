
import os
import re
import pandas as pd
import yt_dlp


INPUT_FILE = "videos.xlsx"
OUTPUT_FILE = "subtitle_dataset.xlsx"


def clean_vtt(file_path):
    """Extract only subtitle text from a VTT file."""

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    subtitles = []

    for line in lines:
        line = line.strip()

        
        if not line:
            continue

        if line == "WEBVTT":
            continue

        
        if "-->" in line:
            continue

        # Skip VTT numbering
        if line.isdigit():
            continue

        line = re.sub(r"<[^>]+>", "", line)

        line = line.replace("&nbsp;", " ")
        line = line.replace("&amp;", "&")
        line = line.replace("&lt;", "<")
        line = line.replace("&gt;", ">")

        line = line.strip()

        if line:
            subtitles.append(line)

    # Remove consecutive duplicate subtitle lines
    cleaned = []

    for line in subtitles:
        if not cleaned or line != cleaned[-1]:
            cleaned.append(line)

    return " ".join(cleaned)


def download_subtitle(url, folder):
    """Download English subtitle from YouTube."""

    os.makedirs(folder, exist_ok=True)

    output_template = os.path.join(folder, "subtitle.%(ext)s")

    options = {
        "skip_download": True,
        "writesubtitles": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "outtmpl": output_template,
        "quiet": False,
        "no_warnings": False,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        vtt_file = os.path.join(folder, "subtitle.en.vtt")

        if not os.path.exists(vtt_file):
            return None

        return vtt_file

    except Exception as e:
        print("Error:", e)
        return None


def main():

    df = pd.read_excel(INPUT_FILE)

    print("Columns found:", list(df.columns))

    if "YouTube_URL" not in df.columns:
        print("ERROR: 'YouTube_URL' column not found.")
        return

    results = []

    total = len(df)

    print("Total videos:", total)

    for index, row in df.iterrows():

        url = str(row["YouTube_URL"]).strip()

        if not url or url.lower() == "nan":
            continue

        print("\n" + "=" * 50)
        print(f"Processing {index + 1}/{total}")
        print(url)
        print("=" * 50)

        folder = os.path.join("data", str(index + 1))

        vtt_file = download_subtitle(url, folder)

        if vtt_file:

            subtitle_text = clean_vtt(vtt_file)

            if subtitle_text:
                status = "Success"
                print("Status: Success")
            else:
                subtitle_text = ""
                status = "Failed"
                print("Status: Subtitle empty")

        else:
            subtitle_text = ""
            status = "Failed"
            print("Status: Failed")

        results.append({
            "yt_link": url,
            "subtitles": subtitle_text,
            "status": status
        })

    output_df = pd.DataFrame(results)


    MAX_CHARS = 32000

    final_rows = []

    for _, row in output_df.iterrows():

        text = row["subtitles"]

        if len(text) <= MAX_CHARS:

            final_rows.append({
                "yt_link": row["yt_link"],
                "subtitles": text,
                "status": row["status"]
            })

        else:

            parts = [
                text[i:i + MAX_CHARS]
                for i in range(0, len(text), MAX_CHARS)
            ]

            new_row = {
                "yt_link": row["yt_link"],
                "status": row["status"]
            }

            for i, part in enumerate(parts, start=1):
                new_row[f"subtitles_part_{i}"] = part

            final_rows.append(new_row)

    final_df = pd.DataFrame(final_rows)

    final_df.to_excel(OUTPUT_FILE, index=False)

    print("\n" + "=" * 50)
    print("PROCESSING COMPLETED")
    print("=" * 50)
    print("Output file:", OUTPUT_FILE)


if __name__ == "__main__":
    main()