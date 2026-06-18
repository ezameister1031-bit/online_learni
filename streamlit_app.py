import streamlit as st
import time
import requests

# =========================
# Ollama
# =========================
def get_hint(problem, code):
    prompt = f"""
あなたはプログラミング学習支援AIです。

【問題】
{problem}

【ユーザーのコード】
{code}

このユーザーの詰まりを分析し、短くヒントだけ出してください。
解答は禁止です。
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

# =========================
# UI
# =========================
st.title("学習支援AI（入力停止検知版）")

problem = st.text_area("問題")

code = st.text_area("コード", height=300)

# =========================
# state初期化
# =========================
if "last_edit" not in st.session_state:
    st.session_state.last_edit = time.time()

if "hint" not in st.session_state:
    st.session_state.hint = ""

if "last_code" not in st.session_state:
    st.session_state.last_code = ""

if "last_call" not in st.session_state:
    st.session_state.last_call = 0

# =========================
# 入力変化検知
# =========================
if code != st.session_state.last_code:
    st.session_state.last_code = code
    st.session_state.last_edit = time.time()

# =========================
# アイドル判定
# =========================
IDLE_LIMIT = 5  # 秒（テスト用。本番は60〜300）

now = time.time()

if now - st.session_state.last_edit > IDLE_LIMIT:
    if code and problem:
        # API連打防止
        if now - st.session_state.last_call > 10:
            st.session_state.hint = get_hint(problem, code)
            st.session_state.last_call = now

# =========================
# 表示
# =========================
st.subheader("AIヒント")
st.write(st.session_state.hint)

st.caption("コード入力が止まると自動でヒントが出ます")
