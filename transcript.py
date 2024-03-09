import moviepy.editor as mp 
import speech_recognition as sr


def getTranscipt(filename, output):

    fname_split = ".".join(filename.split(".")[:-1])
  
    video = mp.VideoFileClip(fname_split + ".mp4") 
    
    audio_file = video.audio 
    audio_file.write_audiofile(output + ".wav") 
    
    r = sr.Recognizer() 
    
    with sr.AudioFile(output + ".wav") as source: 
        data = r.record(source) 
    
    text = r.recognize_google(data, language = 'en') 
    
    return text
