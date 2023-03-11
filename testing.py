import pyttsx3
import fnutils
engine = pyttsx3.init()
engine.setProperty('volume',1.0)
print(fnutils.getcurrentshop())
engine.save_to_file(str(fnutils.getcurrentshop()), 'test.mp3')
engine.runAndWait()