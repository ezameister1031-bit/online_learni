import streamlit as st
import time

from monitor import ActivityMonitor
from ollama_client import get_hint_from_ollama

st.title("学習支援AI（アイドル検知版）")

# ======================
# 入力
# ======================
problem = st.text_area("問題")
code = st.text_area("コード")

# ======================
# 初期化（1回だけ）
# ======================
if "monitor" not in st.session_state:
    monitor = ActivityMonitor()
    monitor.start()
    st.session_state.monitor = monitor

if "hint" not in st.session_state:
    st.session_state.hint = ""

if "last_call" not in st.session_state:
    st.session_state.last_call = 0

# ======================
# 自動再実行（超重要）
# ======================
st.autorefresh = st.experimental_rerun  # 互換用（なくてもOK）

# 画面更新トリガー（1秒ごと）
time.sleep(1)
st.rerun()

# ======================
# アイドル判定
# ======================
monitor = st.session_state.monitor

if monitor.is_idle():
    now = time.time()

    # 連続API呼び出し防止（10秒に1回）
    if now - st.session_state.last_call > 10:
        if problem and code:
            st.session_state.hint = get_hint_from_ollama(problem, code)
            st.session_state.last_call = now

# ======================
# 表示
# ======================
st.subheader("ヒント")
st.write(st.session_state.hint)

st.caption("※一定時間操作がないとヒントが自動生成されます")
