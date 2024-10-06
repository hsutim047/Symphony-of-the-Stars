from PIL import Image
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration, AutoProcessor, MusicgenForConditionalGeneration

from pydub import AudioSegment
import io
import base64
import numpy as np

import warnings
warnings.filterwarnings("ignore")


def test_func(d):
    return "TEST" + str(d)


def _numpy_to_base64_mp3(audio_data, sample_rate):
    # Create a BytesIO object to hold WAV data in memory
    wav_io = io.BytesIO()
    wav_io.write(audio_data.tobytes())
    wav_io.seek(0)

    # Convert WAV (from BytesIO) to MP3 using pydub
    audio_segment = AudioSegment(
        data=wav_io.read(),
        sample_width=2,  # 16 bits = 2 bytes
        frame_rate=sample_rate,
        channels=1  # mono audio, adjust as necessary
    )
    
    mp3_io = io.BytesIO()
    audio_segment.export(mp3_io, format="mp3")
    
    # Base64 encode the MP3
    mp3_io.seek(0)
    mp3_base64 = base64.b64encode(mp3_io.read()).decode('utf-8')
    
    return f"audio/mp3;base64,{mp3_base64}"



def img2textmusic(png):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    # conditional image captioning
    text = "NASA space image:"
    inputs = processor(png, return_tensors="pt")

    out = model.generate(**inputs)
    out_str = text + processor.decode(out[0], skip_special_tokens=True)

    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

    inputs = processor(
        text=[out_str],
        padding=True,
        return_tensors="pt",
    )

    audio_values = model.generate(**inputs, max_new_tokens=16)

    sampling_rate = model.config.audio_encoder.sampling_rate

    music = _numpy_to_base64_mp3(np.repeat(audio_values[0].numpy(), 50), sampling_rate)

    return out_str, png, music

if __name__ == '__main__':
  print(img2textmusic(Image.open(requests.get("https://stsci-opo.org/STScI-01J748X0ZXT252FZ802FWB5608.png", stream=True).raw).convert('RGB')))
