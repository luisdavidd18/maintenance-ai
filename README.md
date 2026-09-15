# Maintenance AI Copilot

A local AI assistant for industrial maintenance and reliability troubleshooting.

## What it does

The application accepts a maintenance failure description and returns:

- Probable causes
- Immediate troubleshooting checks
- Safety considerations
- Data to collect
- Root-cause-analysis questions

## Why I built it

This project combines industrial maintenance and reliability engineering experience with applied AI.

The goal is to explore how local language models can support technicians and engineers during troubleshooting without relying on paid cloud APIs.

## Tech Stack

- Python
- Ollama
- Qwen 2.5
- Requests
- uv
- Git / GitHub

## Run locally

Start Ollama:

```bash
brew services start ollama