import re
from difflib import SequenceMatcher


def normalize_text(text):

    text = text.lower()

    text = re.sub(
        r"[^\w\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

def compare_text(subtitle_file, transcript_file):

    with open(
        subtitle_file,
        "r",
        encoding="utf-8"
    ) as file:

        subtitle = file.read()


    with open(
        transcript_file,
        "r",
        encoding="utf-8"
    ) as file:

        transcript = file.read()


    subtitle = normalize_text(subtitle)
    transcript = normalize_text(transcript)


    subtitle_words = subtitle.split()
    transcript_words = transcript.split()


    matcher = SequenceMatcher(
        None,
        subtitle_words,
        transcript_words
    )


    differences = []


    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        if tag == "equal":
            continue


        subtitle_part = " ".join(
            subtitle_words[i1:i2]
        )

        transcript_part = " ".join(
            transcript_words[j1:j2]
        )


        differences.append({

            "type": tag,

            "subtitle": subtitle_part,

            "audio": transcript_part

        })


    return differences