import os
import pandas as pd

from get_subtitles import get_subtitle
from download_audio import download_audio
from transcribe_audio import transcribe_audio
from compare_text import compare_text


INPUT_FILE = "videos.xlsx"


def main():

    df = pd.read_excel(INPUT_FILE)

    summary = []
    errors = []
    failed = []

    print("Total videos:", len(df))

    for index, row in df.iterrows():

        video_no = index + 1
        url = row["YouTube_URL"]

        print("\n" + "=" * 50)
        print(f"Processing {video_no}/{len(df)}")
        print(url)
        print("=" * 50)

        folder = os.path.join("data", str(video_no))
        os.makedirs(folder, exist_ok=True)

        subtitle_file = os.path.join(folder, "subtitle.txt")
        transcript_file = os.path.join(folder, "transcript.txt")

        try:

            print("[1/4] Getting subtitles...")
            get_subtitle(url, subtitle_file)

            print("[2/4] Downloading audio...")
            audio_file = download_audio(url, folder)

            if not audio_file:
                raise Exception("Audio download failed")

            print("[3/4] Transcribing...")
            transcribe_audio(audio_file, transcript_file)

            print("[4/4] Comparing...")
            differences = compare_text(
                subtitle_file,
                transcript_file
            )

            summary.append({
                "Video No": video_no,
                "YouTube URL": url,
                "Status": "Success",
                "Total Differences": len(differences)
            })

            for number, diff in enumerate(differences, 1):

                errors.append({
                    "Video No": video_no,
                    "Error No": number,
                    "Type": diff["type"],
                    "Subtitle": diff["subtitle"],
                    "Audio / Transcript": diff["audio"]
                })

            print("Differences:", len(differences))

        except Exception as e:

            print("FAILED:", e)

            summary.append({
                "Video No": video_no,
                "YouTube URL": url,
                "Status": "Failed",
                "Total Differences": ""
            })

            failed.append({
                "Video No": video_no,
                "YouTube URL": url,
                "Error": str(e)
            })

    os.makedirs("reports", exist_ok=True)

    output = "reports/verification_results.xlsx"

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        pd.DataFrame(summary).to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        pd.DataFrame(errors).to_excel(
            writer,
            sheet_name="Error Details",
            index=False
        )

        pd.DataFrame(failed).to_excel(
            writer,
            sheet_name="Failed Videos",
            index=False
        )


    print("\n" + "=" * 50)
    print("PROCESSING COMPLETED")
    print("Report:", output)
    print("=" * 50)


if __name__ == "__main__":
    main()