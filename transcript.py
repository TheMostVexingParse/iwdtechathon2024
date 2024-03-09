import moviepy.editor as mp 
import speech_recognition as sr


def getTranscipt(filename):

    fname_split = ".".join(filename.split(".")[:-1])
  
    video = mp.VideoFileClip(fname_split + ".mp4") 
    
    audio_file = video.audio 
    audio_file.write_audiofile(fname_split + ".wav") 
    
    r = sr.Recognizer() 
    
    with sr.AudioFile(fname_split + ".wav") as source: 
        data = r.record(source) 
    
    text = r.recognize_google(data, language = 'tr') 
    
    return text
