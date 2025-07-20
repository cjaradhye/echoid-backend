# Echoid Backend

This project is a FastAPI-based backend for a Text-to-Speech (TTS) service. It uses the Coqui TTS library to generate speech that mimics a voice from an input audio file.

## How it Works

The application provides a single API endpoint, `/generate`, which accepts a text string and an audio file (WAV format). It uses the pre-trained XTTS v2 model from Coqui TTS to generate a new audio file where the provided text is spoken in the voice from the input audio file.

The core logic is in `main.py`:

1.  A FastAPI application is initialized.
2.  A pre-trained Coqui XTTS v2 model is loaded.
3.  The `/generate` endpoint is defined:
    *   It receives a text string and an uploaded audio file.
    *   The uploaded audio file is saved temporarily.
    *   The `tts.tts_to_file()` function is called with the text and the path to the temporary audio file.
    *   The generated audio file (`output.wav`) is returned as a response.
    *   The temporary audio file is deleted.

## Getting Started

### Prerequisites

*   Python 3.11
*   ffmpeg (for audio conversion)
*   The Python dependencies listed in `requirements.txt`

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/echoid-backend.git
    cd echoid-backend
    ```
2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

You can run the application using uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

This will start the server, and you can access the API at `http://localhost:8000`.

## API Endpoint

### `POST /generate`

*   **Description:** Generates speech from text in the voice of the provided audio file.
*   **Request:**
    *   `text` (form data): The text to be converted to speech.
    *   `speaker_wav` (file upload): The audio file containing the voice to be mimicked.
*   **Response:**
    *   An audio file (`output.wav`) in WAV format.

### Example Usage (with curl)

```bash
curl -X POST -F "text=Hello, this is a test." -F "speaker_wav=@/path/to/your/speaker.wav" http://localhost:8000/generate -o output.wav
```

## Docker

A `Dockerfile` is provided to build and run the application in a container.

1.  Build the Docker image:
    ```bash
    docker build -t echoid-backend .
    ```
2.  Run the Docker container:
    ```bash
    docker run -p 8000:8000 echoid-backend
    ```

## Other Files

*   `please.py`: A script for testing the TTS model locally.
*   `convert`: A shell script to convert an M4A audio file to WAV format using ffmpeg.
*   `connect`: A shell script for connecting to an AWS EC2 instance.
