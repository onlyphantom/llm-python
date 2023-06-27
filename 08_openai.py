from dotenv import load_dotenv
load_dotenv()

import openai
import webbrowser


# list all models
models = openai.Model.list()
print(models.data[0].root)

# create our completion
completion = openai.Completion.create(model="ada", prompt="Bill Gates is a")
print(completion.choices[0].text)

image_gen = openai.Image.create(prompt="Zwei Hunde spielen unter einem Baum, cartoon",
                                n=2,
                                size="512x512"
                            )
# imgurl1 = image_gen.data[0].url
# imgurl2 = image_gen.data[1].url
# webbrowser.open(imgurl)
for img in image_gen.data:
    webbrowser.open_new_tab(img.url)


# Gwendolyn Brooks Writers' Conference - Keynote Address: Dr. Donda West
audio = open("audio/donda.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio)
print(transcript)