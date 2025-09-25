# synthesizer/synthesize.py
import os
import logging
from .prompts import SYNTH_PROMPT

logger = logging.getLogger(__name__)

# ---------------------------
# OpenAI (primary route)
# ---------------------------
def call_openai_chat(prompt, model="gpt-3.5-turbo", temperature=0.2):
    import openai
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = key
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful synthesizer & fact-checker."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=1000,
    )
    return resp['choices'][0]['message']['content']


# ---------------------------
# HuggingFace fallback (safe)
# ---------------------------
def local_summarize(prompt, max_chunk=400):
    from transformers import pipeline

    # Lighter summarizer model than flan-t5-large (safer on CPU)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    words = prompt.split()
    chunks = [" ".join(words[i:i + max_chunk]) for i in range(0, len(words), max_chunk)]

    outputs = []
    for c in chunks:
        out = summarizer(c, max_length=200, min_length=50, do_sample=False)[0]['summary_text']
        outputs.append(out)

    return "\n".join(outputs)


# ---------------------------
# Synthesizer main logic
# ---------------------------
def synthesize(sources_dict):
    """
    sources_dict: {url: text}
    """
    # Create numbered source list and short extracts for prompt
    sources = []
    extracts = []
    for i, (url, txt) in enumerate(sources_dict.items(), start=1):
        sources.append(f"[{i}] {url}")
        # take top 3 paragraphs as extract
        paras = [p.strip() for p in txt.split("\n\n") if len(p.strip()) > 50]
        sample = "\n\n".join(paras[:3])
        extracts.append(f"[{i}] {sample}")

    prompt = SYNTH_PROMPT.format(
        sources="\n".join(sources),
        extracts="\n\n".join(extracts)
    )
    logger.info("Prompt built; length=%d", len(prompt))

    # Choose LLM route
    try:
        answer = call_openai_chat(prompt)
    except Exception as e:
        logger.warning("OpenAI not available, using local summarizer: %s", e)
        answer = local_summarize(prompt)

    return answer
