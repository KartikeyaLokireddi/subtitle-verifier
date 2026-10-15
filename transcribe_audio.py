import whisper
import os


print("Loading Whisper model...")

model = whisper.load_model("base")

print("Whisper model loaded!")


def transcribe_audio(audio_file, output_file):

    print("\nTranscribing:")
    print(audio_file)

    result = model.transcribe(
        audio_file,
        language="en"
    )

    transcript = result["text"]

    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(transcript)

    return transcript