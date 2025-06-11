import logging
from xml.etree.ElementTree import ParseError
import time

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def get_transcript(
    video_id: str,
    languages: list[str] = ['en'],
    fallback_language: str = 'en'
) -> str | None:
    """
    Estrae e restituisce il transcript completo di un video YouTube.

    Args:
        video_id: ID del video YouTube
        languages: lista di lingue preferite (es. ['en', 'it'])
        fallback_language: lingua di fallback se le preferite non sono disponibili

    Returns:
        Una singola stringa con tutto il testo del transcript,
        oppure None se non è disponibile o si verifica un errore.
    """
    try_for_max = 3
    for i in range(try_for_max):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            testo = ' '.join([x['text'] for x in transcript])
            return testo

            # # Lista tutte le trascrizioni disponibili per quel video
            # transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # # Provo a prendere la prima trascrizione in una delle lingue preferite
            # for lang in languages:
            #     try:
            #         transcript = transcript_list.find_transcript([lang])
            #         break
            #     except Exception:
            #         continue
            # else:
            #     # Se non trovo alcuna preferita, uso la lingua di fallback
            #     transcript = transcript_list.find_transcript([fallback_language])

            # # Scarico le singole porzioni di testo
            # entries = transcript.fetch()
            # # Concatena tutto in un'unica stringa
            # full_text = " ".join([entry['text'] for entry in entries])
            # return full_text
        except ParseError:
            print(f"Attempt {i+1}: ParseError, i'll try again in few seconds...")
            time.sleep(10)
        except TranscriptsDisabled:
            logging.warning(f"Transcripts are disabled for video {video_id}")
            return None
        except NoTranscriptFound:
            logging.warning(f"No transcript found for video {video_id} in {languages + [fallback_language]}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error fetching transcript for {video_id}: {e}")
            return None
