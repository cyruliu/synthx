# SynthX: An AI agent for X Chatbot
## Background

A prototype started from [Weekend AI Agent Hack](https://lu.ma/fjs446ye?tk=WePHyw) (06/14/2025), by General Machine Intelligent (GMI) Cloud.

## Features
- Configurable for different X account.
- Live chat on X.
- Stock analysis.

## Setting Up

Create a `credentials.py` file with the following credential configurations:

- X account keys: it can be generated from https://developer.x.com/.
``` 
API_KEY = $your_key
API_KEY_SECRET = $your_key
BEARER_TOKEN = $your_token
ACCESS_TOKEN_SECRET = $your_secret
```
- LLM API Key: LLMs provider API keys.
```
LLM_API_Key = $your_key
```


## Run the Test

On the root directory, run the following:
```
python3 -m venv synthx
source synthx/bin/activate
pip install -r requirements.txt
```

## Extension 