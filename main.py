from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import torch
import os

# ─── PATCH: Disable weights_only for torch.load ─────────────────────────────────
original_torch_load = torch.load

def patched_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return original_torch_load(*args, **kwargs)

torch.load = patched_load

# ─── PATCH: Allow XTTS config class ─────────────────────────────────────────────
from TTS.tts.configs.xtts_config import XttsConfig
from torch.serialization import add_safe_globals

add_safe_globals({ "TTS.tts.configs.xtts_config.XttsConfig": XttsConfig })

# ─── Load XTTS Model ────────────────────────────────────────────────────────────
from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")

# ─── FastAPI Setup ──────────────────────────────────────────────────────────────
app = FastAPI()

@app.post("/generate")
async def generate_tts(text: str = Form(...), speaker_wav: UploadFile = File(...)):
    input_path = f"temp_{speaker_wav.filename}"
    output_path = "output.wav"

    # Save uploaded audio
    with open(input_path, "wb") as f:
        f.write(await speaker_wav.read())

    # Run XTTS
    tts.tts_to_file(
        text=text,
        speaker_wav=input_path,
        language="en",
        file_path=output_path
    )

    os.remove(input_path)
    return FileResponse(output_path, media_type="audio/wav", filename="output.wav")


