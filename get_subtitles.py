import yt_dlp
import os


def get_subtitle(url, output_file):

    folder = os.path.dirname(output_file)

    if folder:
        os.makedirs(folder, exist_ok=True)

    options = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "outtmpl": os.path.join(
            folder if folder else ".",
            "subtitle"
        ),
        "noplaylist": True
    }

    try:

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        vtt_file = os.path.join(
            folder if folder else ".",
            "subtitle.en.vtt"
        )

        if not os.path.exists(vtt_file):
            raise Exception(
                "English subtitles were not found."
            )

        with open(
            vtt_file,
            "r",
            encoding="utf-8"
        ) as file:

            lines = file.readlines()

        text_lines = []

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if line == "WEBVTT":
                continue

            if "-->" in line:
                continue

            if line.isdigit():
                continue

            text_lines.append(line)

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(" ".join(text_lines))

        print("English subtitles saved.")

        return output_file

    except Exception as e:

        print("Subtitle extraction failed:")
        print(e)

        return None