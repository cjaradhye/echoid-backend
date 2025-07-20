from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
import os
import uuid

# ─── PATCH: Disable weights_only for torch.load ─────────────────────────────────
original_torch_load = torch.load

def patched_load(*args, **kwargs):
    kwargs["weights_only"] = False  # Required for XTTS full model load
    return original_torch_load(*args, **kwargs)

torch.load = patched_load

# ─── PATCH: Let XTTS call .generate() ───────────────────────────────────────────
from transformers import PreTrainedModel
from transformers.generation.utils import GenerationMixin

if not issubclass(PreTrainedModel, GenerationMixin):
    PreTrainedModel.__bases__ += (GenerationMixin,)

# ─── Load XTTS Model ────────────────────────────────────────────────────────────
from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")

# ─── FastAPI Setup ──────────────────────────────────────────────────────────────
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_tts(
    background_tasks: BackgroundTasks,
    text: str = Form(...),
    speaker_wav: UploadFile = File(...)
):
    # Generate unique filenames to avoid conflicts
    unique_id = str(uuid.uuid4())
    input_path = f"temp_{unique_id}_{speaker_wav.filename}"
    output_path = f"output_{unique_id}.wav"

    try:
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

        # Schedule file cleanup after response is sent
        background_tasks.add_task(os.remove, input_path)
        background_tasks.add_task(os.remove, output_path)

        # Return the generated audio file
        return FileResponse(output_path, media_type="audio/wav", filename="output.wav")
    
    except Exception as e:
        # Clean up input file if error occurs before scheduling background task
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
