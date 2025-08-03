from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from googletrans import Translator

def extract_video_id(url: str) -> str:
    import re
    
    # Handle various YouTube URL formats
    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([a-zA-Z0-9_-]{11})",
        r"youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be\/([a-zA-Z0-9_-]{11})",
        r"youtube\.com\/embed\/([a-zA-Z0-9_-]{11})",
        r"youtube\.com\/v\/([a-zA-Z0-9_-]{11})",
        r"m\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})",
        r"www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})",
        r"youtube\.com\/watch\?.*&v=([a-zA-Z0-9_-]{11})"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def list_available_transcripts(video_id: str) -> list:
    """List all available transcripts for a video (for debugging)"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        available_transcripts = []
        for transcript in transcript_list:
            available_transcripts.append({
                'language_code': transcript.language_code,
                'language': transcript.language,
                'is_generated': transcript.is_generated,
                'is_translatable': transcript.is_translatable
            })
        return available_transcripts
    except Exception as e:
        return []

def get_transcript(video_id: str, language: str = 'en') -> str:
    translator = Translator()
    try:
        # First, get the list of all available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to get the requested language first
        try:
            response = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
            return " ".join([entry['text'] for entry in response])
        except NoTranscriptFound:
            pass
        
        # If requested language not found, try to find any English variant
        for transcript in transcript_list:
            if transcript.language_code.startswith('en'):
                try:
                    response = transcript.fetch()
                    return " ".join([entry['text'] for entry in response])
                except Exception:
                    continue
        
        # If no English transcript found, get the first available transcript and translate it
        for transcript in transcript_list:
            try:
                response = transcript.fetch()
                transcript_text = " ".join([entry['text'] for entry in response])
                
                # If it's not English, translate it
                if not transcript.language_code.startswith('en'):
                    print(f"Found transcript in {transcript.language_code}, translating to English...")
                    translated = translator.translate(transcript_text, dest='en')
                    return translated.text
                else:
                    return transcript_text
            except Exception as e:
                print(f"Error processing transcript in {transcript.language_code}: {str(e)}")
                continue
        
        raise Exception("No transcript available in any language for this video.")
    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video.")
    except Exception as e:
        raise Exception(f"Error accessing transcripts: {str(e)}")