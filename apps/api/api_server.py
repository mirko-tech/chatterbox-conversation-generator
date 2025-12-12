"""
FastAPI Backend for Chatterbox Dialogue Generator

Provides HTTP API endpoints for the web UI to generate conversations.
"""

import os
import tempfile
from pathlib import Path
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
import asyncio
import json

from apps.api.dialogue_generator import DialogueParser
from apps.api.voice_pipeline import create_dialogue_audio


# Initialize FastAPI app
app = FastAPI(
    title="Chatterbox Dialogue Generator API",
    description="Generate multi-speaker AI conversations with voice cloning",
    version="1.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class GenerateDialogueRequest(BaseModel):
    """Request model for dialogue generation."""
    dialogue_text: str = Field(
        ...,
        description="Dialogue text in the format: voice1_wav=\"path\" voice1=\"text\""
    )
    output_prefix: str = Field(
        default="conversation",
        description="Output file prefix (without extension)"
    )
    silence_ms: int = Field(
        default=500,
        ge=0,
        le=5000,
        description="Milliseconds of silence between lines"
    )
    language: str = Field(
        default="en",
        description="Language code (en, it, es, fr, de, zh, ja, ko)"
    )
    exaggeration: float = Field(
        default=1.5,
        ge=1.0,
        le=3.0,
        description="Expression intensity"
    )
    cfg_weight: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Configuration weight"
    )
    save_individual: bool = Field(
        default=True,
        description="Save individual line files"
    )
    process_audio: bool = Field(
        default=True,
        description="Enable audio processing (de-essing, normalization, fades)"
    )
    device: str = Field(
        default="cpu",
        description="Device to use for generation (cpu or cuda)"
    )


class GenerateDialogueResponse(BaseModel):
    """Response model for successful generation."""
    status: str
    output_file: str
    lines_dir: Optional[str]
    duration_seconds: float
    num_lines: int
    timestamp: str


class ErrorResponse(BaseModel):
    """Response model for errors."""
    status: str
    error: str
    details: Optional[str] = None


# Global progress tracking
progress_data = {
    "current_line": 0,
    "total_lines": 0,
    "status": "idle",  # idle, generating_line, merging, completed, error
    "message": ""
}

# API Endpoints

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.

    Returns:
        dict: Status information
    """
    return {
        "status": "healthy",
        "service": "Chatterbox Dialogue Generator API",
        "version": "1.0.0"
    }


@app.get("/api/progress-stream")
async def progress_stream():
    """
    Server-Sent Events endpoint for real-time progress updates.

    Returns:
        StreamingResponse: SSE stream of progress updates
    """
    async def event_generator():
        last_sent = {}
        while True:
            # Only send if data has changed
            current_data = progress_data.copy()
            if current_data != last_sent:
                yield f"data: {json.dumps(current_data)}\n\n"
                last_sent = current_data.copy()

            # Exit if completed or error
            if current_data.get("status") in ["completed", "error", "idle"]:
                break

            await asyncio.sleep(0.1)  # Check every 100ms

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post(
    "/api/generate-dialogue",
    response_model=GenerateDialogueResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
async def generate_dialogue(request: GenerateDialogueRequest):
    """
    Generate a multi-speaker dialogue audio file from text.

    Args:
        request: Generation parameters including dialogue text and settings

    Returns:
        GenerateDialogueResponse with output file path and metadata

    Raises:
        HTTPException: If generation fails
    """
    # Reset progress data
    progress_data["current_line"] = 0
    progress_data["total_lines"] = 0
    progress_data["status"] = "idle"
    progress_data["message"] = ""

    # Define progress callback
    def update_progress(data: dict):
        progress_data.update(data)

    try:
        # Create a temporary file to store the dialogue text
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False,
            encoding='utf-8'
        ) as tmp_file:
            tmp_file.write(request.dialogue_text)
            tmp_file_path = tmp_file.name

        try:
            # Parse the dialogue
            parser = DialogueParser()
            dialogue = parser.parse_dialogue_file(tmp_file_path)

            if not dialogue:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "status": "error",
                        "error": "No dialogue lines found",
                        "details": "Please check the dialogue format"
                    }
                )

            # Generate the audio with progress tracking
            output_path = create_dialogue_audio(
                dialogue=dialogue,
                output_prefix=request.output_prefix,
                silence_ms=request.silence_ms,
                language=request.language,
                exaggeration=request.exaggeration,
                cfg_weight=request.cfg_weight,
                save_individual=request.save_individual,
                process_audio=request.process_audio,
                device=request.device,
                progress_callback=update_progress
            )

            # Mark as completed
            progress_data["status"] = "completed"
            progress_data["message"] = "Generation complete!"

            # Calculate duration
            import torchaudio as ta
            waveform, sample_rate = ta.load(str(output_path))
            duration_seconds = waveform.shape[1] / sample_rate

            # Build response
            lines_dir = None
            if request.save_individual:
                lines_dir = str(output_path.parent / f"{request.output_prefix}_lines")

            return GenerateDialogueResponse(
                status="success",
                output_file=str(output_path),
                lines_dir=lines_dir,
                duration_seconds=float(duration_seconds),
                num_lines=len(dialogue),
                timestamp=datetime.now().isoformat()
            )

        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_file_path)
            except Exception:
                pass

    except FileNotFoundError as e:
        progress_data["status"] = "error"
        progress_data["message"] = str(e)
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "error": "Voice file not found",
                "details": str(e)
            }
        )

    except ValueError as e:
        progress_data["status"] = "error"
        progress_data["message"] = str(e)
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "error": "Invalid input",
                "details": str(e)
            }
        )

    except Exception as e:
        progress_data["status"] = "error"
        progress_data["message"] = str(e)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "error": "Generation failed",
                "details": str(e)
            }
        )


@app.get("/api/download")
async def download_file(path: str):
    """
    Download a generated audio file.

    Args:
        path: Path to the file (relative to project root)

    Returns:
        FileResponse with the audio file

    Raises:
        HTTPException: If file not found or path is invalid
    """
    try:
        file_path = Path(path)

        # Security: Only allow downloads from outputs directory
        if not str(file_path).startswith("outputs"):
            raise HTTPException(
                status_code=403,
                detail={
                    "status": "error",
                    "error": "Access denied",
                    "details": "Can only download files from outputs directory"
                }
            )

        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "error",
                    "error": "File not found",
                    "details": f"File does not exist: {path}"
                }
            )

        return FileResponse(
            path=str(file_path),
            media_type="audio/wav",
            filename=file_path.name
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "error": "Download failed",
                "details": str(e)
            }
        )


# Development server entry point
if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("Chatterbox Dialogue Generator - API Server")
    print("=" * 60)
    print("\n[*] Starting server...")
    print("[*] API documentation available at: http://localhost:8000/docs")
    print("[*] Health check: http://localhost:8000/health")
    print("\n[!] Press Ctrl+C to stop the server\n")

    uvicorn.run(
        "app.api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
