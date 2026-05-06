import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("サンプルアプリ①：自作LLMアプリ")

st.write("##### LLMのモデルはOpenAIのgpt-4o-miniを使用しています。")
st.write("##### 以下に質問を入力して、「実行」ボタンを押すと、LLMが回答します。")

input_message = st.text_input(label="質問を入力してください。")
if st.button("実行"):
    if not input_message:
        st.warning("質問を入力してください。")
    else:
        st.write(f"質問: **{input_message}**")
        try:
            first_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "あなたは、生成AIに詳しいAIです。"},{"role": "user", "content": input_message}],
                temperature=0.5
            )
            answer = first_completion.choices[0].message.content
            st.write(f"回答: **{answer}**")
        except Exception as e:
            st.error(f"回答の取得中にエラーが発生しました: {e}")


