import requests

def get_hint_from_ollama(problem, code):
    prompt = f"""
あなたは優秀なプログラミング学習支援AIです。

【問題】
{problem}

【ユーザーのコード】
{code}

ユーザーは詰まっている可能性があります。
短くヒントだけ日本語で返してください。
※絶対に解答は出さないでください。
"""

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return res.json()["response"]
