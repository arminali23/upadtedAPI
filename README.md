# Model API (Integration Test)

This repository contains a lightweight API used to test the integration
between the Sokoban game telemetry system and an AI model for emotion
classification.

The goal of this project is to validate the **end-to-end pipeline**
between the game, the telemetry data format, and an AI inference service
before deploying the final production model.

------------------------------------------------------------------------

## Overview

The API receives Sokoban gameplay telemetry in JSON format, builds a
prompt from the game metrics, runs an AI model locally, and returns an
emotion prediction.

Pipeline:

Game telemetry JSON → Prompt builder → AI model → Emotion prediction
JSON → API response

This implementation is intended for **internal development and
integration testing only**.

------------------------------------------------------------------------

## Current Features

-   FastAPI based local API
-   Accepts Sokoban telemetry JSON
-   Converts telemetry metrics into a structured prompt
-   Runs a local LLM for emotion classification
-   Returns structured JSON output
-   Compatible with Apple Silicon (MPS acceleration)

------------------------------------------------------------------------

## API Endpoints

### Root

GET /

Returns service status.

Example response:

{ "ok": true, "service": "sohma_api" }

------------------------------------------------------------------------

### Health Check

GET /healthz

Used to verify that the API is running.

------------------------------------------------------------------------

## Running the API

1.  Create a virtual environment

python -m venv .venv\
source .venv/bin/activate

2.  Install dependencies

pip install -r requirements.txt

3.  Start the API

python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload

4.  Open the interactive API documentation

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

## Model

The API currently supports running a local instruction-tuned language
model for emotion classification.

Models being tested include:

-   Mistral-7B-Instruct
-   Qwen-2.5-Instruct (lighter alternative for local testing)

The model converts gameplay metrics into a structured emotion
classification response.

- According to the tests qwen-3b did not give the exact emotions that we wanted. On the other hand, mistral-7b performed much efficient in terms of our use cases.
- Hence, use "mistralai/Mistral-7B-Instruct-v0.2" in model_id (can be found in model_runtime.py)

------------------------------------------------------------------------

## Purpose

This API is designed to support the **initial integration test**
between:

-   Sokoban game telemetry
-   SDK communication
-   AI inference service

The goal is to validate:

-   JSON data flow
-   API communication
-   model response format
-   integration with the game engine

before deploying the final hosted model.

------------------------------------------------------------------------

## Future Work

-   Deploy model on shared server
-   Evaluate model latency and output consistency
-   Compare performance across different models
-   Integrate with the Unity SDK pipeline
-   Add logging for adaptation decisions

------------------------------------------------------------------------

## Author

Armin Ali\
SOHMA AI -- AI/ML Development
