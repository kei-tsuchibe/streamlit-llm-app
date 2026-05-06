import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from typing import Dict, Any, List, Union, Sequence
from langchain.schema import BaseMessage, LLMResult, AgentAction, AgentFinish, Document
load_dotenv()

class StreamlitCallbackHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)  # 徐々に更新

st.title("サンプルアプリ①：自作LLMアプリ")
st.write("##### LLMのモデルはOpenAIのgpt-4o-miniを使用しています。")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["生成AIに関する専門家に質問", "政治に関する専門家に質問","経済に関する専門家に質問","スポーツに関する専門家に質問"])

st.divider()

if selected_item == "生成AIに関する専門家に質問":
    genre="生成AIに関する専門家"

elif selected_item == "政治に関する専門家に質問":
    genre="政治に関する専門家"

elif selected_item == "経済に関する専門家に質問":
    genre="経済に関する専門家"

elif selected_item == "スポーツに関する専門家に質問":
    genre="スポーツに関する専門家"

st.write("##### 以下に質問を入力して、「実行」ボタンを押すと、LLMが回答します。")
input_message = st.text_input(label=f"あなたは今から{genre}に質問します")
if st.button("実行"):
    if not input_message:
        st.warning("質問を入力してください。")
    else:
        st.write(f"質問: **{input_message}**")
        try:
            llm = ChatOpenAI(
                model_name="gpt-4o-mini",
                temperature=0.5,
                streaming=True,
                callbacks=[StreamlitCallbackHandler(st.empty())])
            messages = [SystemMessage(content=f"あなたは{genre}です。"),HumanMessage(content=input_message)]
            answer = llm(messages)
            st.write(f"回答: **{answer.content}**")
        except Exception as e:
            st.error(f"回答の取得中にエラーが発生しました: {e}")


