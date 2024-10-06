from transformers import BlipProcessor, BlipForConditionalGeneration, AutoProcessor, MusicgenForConditionalGeneration
import scipy


def _save_audio_np_to_file(audio_values, sampling_rate, file_path):
    scipy.io.wavfile.write(file_path, rate=sampling_rate, data=audio_values[0, 0].numpy())


def img2textmusic(png='', audio_file_path='tmp.wav'):
    # Generate text using BLIP
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    # conditional image captioning
    text = "NASA space image:"
    inputs = processor(png, return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=256)
    out_str = text + processor.decode(out[0], skip_special_tokens=True)

    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

    inputs = processor(
        text=[out_str],
        padding=True,
        return_tensors="pt",
    )

    # Generate audio output (assumed to be a waveform tensor)
    audio_values = model.generate(**inputs, max_new_tokens=1024)

    # Get sampling rate
    sampling_rate = model.config.audio_encoder.sampling_rate
    
    _save_audio_np_to_file(audio_values, sampling_rate, audio_file_path)

    return out_str


if __name__ == '__main__':
    img2textmusic()
