# YouTube Subtitle Verification System

## About the Project

The **YouTube Subtitle Verification System** is a prototype developed to explore automated subtitle extraction and verification for YouTube videos. The goal is to obtain English subtitles and, in the planned verification workflow, compare subtitle text with the spoken content to identify possible differences.

## Objectives

- Extract English subtitles from YouTube videos.
- Clean and process subtitle text for further analysis.
- Explore audio transcription and text-comparison techniques.
- Identify potential differences between subtitles and spoken words.

## Technologies Used

- **Python** — core programming language
- **yt-dlp** — explored for YouTube subtitle and media retrieval
- **OpenAI Whisper** — explored for speech-to-text transcription
- **Pandas and OpenPyXL** — data processing and Excel file handling
- **SequenceMatcher** — text comparison

## Project Files

| File | Purpose |
|---|---|
| `app.py` | Application entry point |
| `main.py` | Main processing workflow |
| `subtitle_dataset.py` | Subtitle dataset extraction |
| `get_subtitles.py` | Subtitle retrieval |
| `download_audio.py` | Audio download workflow |
| `transcribe_audio.py` | Audio transcription |
| `compare_text.py` | Text comparison |
| `test_subtitle.py` | Subtitle-related testing |
| `requirements.txt` | Python dependencies |

*File responsibilities are based on their names and intended roles; the scripts may contain different or evolving implementations.*

## Current Progress

- Tested the subtitle extraction workflow using five YouTube videos.
- Successfully extracted English subtitles from three videos in the test.
- Two videos could not be processed because of YouTube access restrictions.
- Identified rate limits and automated-access checks as challenges affecting reliable extraction.

## Limitations

Subtitle extraction may fail because of YouTube rate limits, automated-access restrictions, unavailable subtitles, or video access settings. Results may vary depending on the video and the environment.

This repository represents work completed during the prototype stage. The project is currently paused, and the full workflow has not been validated as a complete, reliable system.

## Future Improvements

- Improve subtitle retrieval reliability and error handling.
- Build a more consistent dataset of English-language videos.
- Validate audio transcription and subtitle comparison end to end.
- Generate structured reports showing the number and details of text differences.

## Disclaimer

This is an educational project created to explore subtitle extraction, speech transcription, and text comparison. It is not a production-ready verification tool.
