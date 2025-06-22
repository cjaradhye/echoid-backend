import torch
from TTS.tts.configs.xtts_config import XttsConfig
from torch.serialization import add_safe_globals

# PATCH: Allow XTTS config
add_safe_globals({"TTS.tts.configs.xtts_config.XttsConfig": XttsConfig})

# PATCH: Force weights_only=False
original_torch_load = torch.load
def patched_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return original_torch_load(*args, **kwargs)
torch.load = patched_load

# ─── Run TTS ─────────────────────────────────────────────
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
tts.tts_to_file(
    text="Please let it work.",
    speaker_wav="your_speaker.wav",  # change this
    language="en",
    file_path="test.wav"
)
