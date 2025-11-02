# Supermemory — Ollama inference quickstart

This repository contains inference helpers that call an Ollama server. The instructions below show how to load Ollama on the cluster, pull a model (example: Claude Sonnet 3.5), and make the model available to other clients on the network.

## Start Ollama (example)

Load the provided module and start the Ollama service on the host that will serve models:

```bash
module load ollama/0.12.3
ollama-start

# Check list of models loaded
ollama list
```

```bash
export OLLAMA_HOST='http://<server_ip>:11437'
```

Then your client scripts or tools that respect `OLLAMA_HOST` (for example, the included `run_inference_ollama.py`) will send requests to the server-hosted model.

## Quick test using the included script

The repository includes `run_inference_ollama.py`, which reads `OLLAMA_HOST` from the environment and runs `ollama run` against models. To test from a client after setting `OLLAMA_HOST`:

```bash
# make sure OLLAMA_HOST points at the server
export OLLAMA_HOST='http://<server_ip>:11437'

# run the provided inference script
python run_inference_ollama.py
```
 
