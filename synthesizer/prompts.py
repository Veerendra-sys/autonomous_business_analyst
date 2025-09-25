# synthesizer/prompts.py

SYNTH_PROMPT = """
You are an expert product manager and fact-checker. You will be given short extracts from multiple sources, each with a link.
1) Synthesize a concise, accurate definition of the RICE scoring model.
2) Synthesize a concise, accurate definition of the Kano model.
3) Explain, with bullets, the core differences between them and practical guidance on when to use each.
4) For each factual claim, include square-bracket citations like [1], [2], ... matching the numbered source list below.
Do not hallucinate — if a claim is unsupported across sources, mark it "UNVERIFIED".
Sources:
{sources}
Extracts:
{extracts}
Produce the final answer in plain text, aiming for ~300-600 words.
"""
