pip install streamlit pynput requests
import requests

def get_hint_from_ollama(problem, code):
    prompt = f"""
あなたはプログラミング学習支援AIです。

問題:
{problem}

ユーザーのコード:
{code}

このユーザーが詰まっている可能性があります。
短くヒントだけを日本語で返してください。
解答は出さないでください。
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
import streamlit as st
import threading
import time

from monitor import ActivityMonitor
from ollama_client import get_hint_from_ollama

st.title("学習支援AI")

problem = st.text_area("問題")
code = st.text_area("コード")

if "monitor" not in st.session_state:
    st.session_state.monitor = ActivityMonitor()
    st.session_state.monitor.start()

if "hint" not in st.session_state:
    st.session_state.hint = ""

def background_loop():
    while True:
        time.sleep(1)

        if st.session_state.monitor.is_idle():
            st.session_state.hint = get_hint_from_ollama(problem, code)

threading.Thread(target=background_loop, daemon=True).start()

st.subheader("ヒント")
st.write(st.session_state.hint)
