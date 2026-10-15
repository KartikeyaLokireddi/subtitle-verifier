import yt_dlp
import os


def download_audio(url, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    output_template = os.path.join(
        output_folder,
        "audio.%(ext)s"
    )

    options = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
    }

    try:

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)

        downloaded_file = ydl.prepare_filename(info)

        return downloaded_file

    except Exception as e:

        print("Audio download failed:")
        print(e)

        return None