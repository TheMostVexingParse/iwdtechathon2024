from datetime import timedelta
import os
import numpy as np
import requests
import json
from glob import glob

from moviepy.editor import VideoFileClip
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

SAVING_FRAMES_PER_SECOND = 0.3  # Define the desired frames per second for saving frames

def extract_frames(video_file):
    video_clip = VideoFileClip(video_file)
    filename, _ = os.path.splitext(video_file)
    filename = "scrshots_" + filename
    filename = filename.replace(".", "_")
    os.makedirs(filename, exist_ok=True)
    saving_frames_per_second = min(video_clip.fps, SAVING_FRAMES_PER_SECOND)
    step = 1 / video_clip.fps if saving_frames_per_second == 0 else 1 / saving_frames_per_second
    for current_duration in np.arange(0, video_clip.duration, step):
        frame_duration_formatted = str(timedelta(seconds=current_duration)).replace(":", "_")
        frame_filename = os.path.join(filename, f"frame_{frame_duration_formatted}.jpg")
        video_clip.save_frame(frame_filename, current_duration)

def ocr_space_file(filename, overlay=False, api_key='K88606795188957', language='eng'):
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()

def run_sentiment_on_video(video_file):
    extract_frames(video_file)
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    
    filename, _ = os.path.splitext(video_file)
    filename = filename.replace(".", "_")
    
    screenshot_dir = "scrshots_" + filename
    os.chdir(screenshot_dir)
    emotions = []
    sentiment_analyzer = SentimentIntensityAnalyzer()
    translator = Translator()
    ocr_text_final = ""
    for image_file in glob("*.jpg"):
        ocr_text = ocr_space_file(image_file, language='tur')
        ocr_result = json.loads(ocr_text)
        parsed_text = ocr_result.get("ParsedResults", [{}])[0].get("ParsedText", "")
        cleaned_text = " ".join("".join(filter(str.isalnum, word)) for word in parsed_text.split())
        translated_text = translator.translate(cleaned_text).text
        ocr_text_final += translated_text + " "
        print(translated_text)
        # print("="*os.get_terminal_size())
        sentiment_scores = sentiment_analyzer.polarity_scores(translated_text)
        emotions.append(-1 * sentiment_scores['compound'])
        print(f"Negativity: {sentiment_scores['neg']}, Neutral: {sentiment_scores['neu']}, Positivity: {sentiment_scores['pos']}, Compound: {sentiment_scores['compound']}")
        # print("="*os.get_terminal_size())
    avg_emotion = sum(emotions) / len(emotions)
    print("Average Emotion:", avg_emotion)
    # print("="*os.get_terminal_size())
    return avg_emotion, ocr_text_final


def run_sentiment_on_text(text):
    sentiment_analyzer = SentimentIntensityAnalyzer()
    translator = Translator()
    translated_text = translator.translate(text).text
    sentiment_score = sentiment_analyzer.polarity_scores(translated_text)
    return sentiment_score


if __name__ == "__main__":
    video_file = "videos/example.mp4"
    run_sentiment_on_video(video_file)
# Example usage


# runSentimentOnVideo("aHR0cHM6Ly93d3cuaW5zdGFncmFtLmNvbS9yZWVscy9DM1BVVEJlTDE5SS8=.mp4")