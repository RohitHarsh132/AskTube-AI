from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from googletrans import Translator

def extract_video_id(url: str) -> str:
    import re
    match = re.search(r"v=([\w-]+)", url)
    return match.group(1) if match else None

def get_transcript(video_id: str, language: str = 'en') -> str:
    translator = Translator()
    try:
        # Try to get English transcript first
        response = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return " ".join([entry['text'] for entry in response])
    except NoTranscriptFound:
        # Get the list of available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        # Try to find any English variant (en-US, en-GB, etc.)
        for transcript in transcript_list:
            if transcript.language_code.startswith('en'):
                try:
                    response = transcript.fetch()
                    return " ".join([entry['text'] for entry in response])
                except Exception:
                    continue
        # Fallback: Try the first available transcript in any language
        for transcript in transcript_list:
            try:
                response = transcript.fetch()
                transcript_text = " ".join([entry['text'] for entry in response])
                # Translate to English if not already English
                if not transcript.language_code.startswith('en'):
                    translated = translator.translate(transcript_text, dest='en')
                    return translated.text
                else:
                    return transcript_text
            except Exception:
                continue
        raise Exception("No transcript available in any language for this video.")
    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video.")