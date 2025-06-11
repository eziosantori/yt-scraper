import logging
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from xml.etree.ElementTree import ParseError
import time

def get_full_transcript(
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
    tentativi = 3
    for i in range(tentativi):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            testo = ' '.join([x['text'] for x in transcript])
            print(testo)
            break
        except ParseError:
            print(f"Tentativo {i+1}: ParseError, riprovo tra qualche secondo...")
            time.sleep(10)
        except Exception as e:
            print(f"Errore: {e}")
            break


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Estrai il transcript completo da un video YouTube"
    )
    parser.add_argument("video_id", help="ID del video YouTube")
    parser.add_argument(
        "-l", "--languages",
        nargs="+",
        default=["en"],
        help="Lingue preferite (es: en it)"
    )
    parser.add_argument(
        "-f", "--fallback",
        default="en",
        help="Lingua di fallback"
    )
    args = parser.parse_args()
    text = get_full_transcript(
        args.video_id,
        languages=args.languages,
        fallback_language=args.fallback
    )
    if text:
        print(text)
    else:
        print("Transcript non disponibile")