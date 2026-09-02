import streamlit as st
from google import genai
from PIL import Image
from dotenv import load_dotenv
import os
import tempfile
import ollama

st.title ("🌟ゴール可視化アプリ🌟")

#１．ユーザーからの入力
category = st.selectbox(
    "どの目標を管理する？",
    ["📚 勉強", "💪 ダイエット・健康", "💻 スキルアップ", "✨ その他・自由"]
    )
user_input=st.text_input("欲しいものやこうなりたいという理想を書いてね")
days_limit=st.number_input("何日以内に達成したい？",min_value=1,max_value=180)
uploaded_file=st.file_uploader("なりたい姿や参考の画像をアップロード",type=["jpg","png","jpeg"])

#画像がある場合に表示するための条件分岐
if uploaded_file:
    image=Image.open(uploaded_file)
    st.image(image,caption='アップロードされた画像',use_container_width=True)

    if st.button("理想を言語化して目標を作る"):
        if user_input:
            with st.spinner("ローカルAI（LLaVA）が画像を分析中‥‥（少し時間がかかります）"):
                #アップロードされた画像を一時ファイルとして保存
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                # AIへのプロンプトを作る
                prompt = f"""
                [ジャンル]:{category}
                [理想]:{user_input}
                [目標期間]:{days_limit}日以内

                この画像と上記の情報をもとに、期間内に達成するための具体的な理想像を言語化し、
                今日取り組むべき目標を1~2個、簡潔に提案してください。
                """

                try:
                    #ollamaに画像とテキストを投げる
                    response = ollama.chat(
                        model="llava",
                        messages=[{"role": "user", "content": prompt,
                        "images":[tmp_file_path]
                        }]
                    )
                    #結果を表示する
                    st.success("AIからの目標提案")
                    st.write(response["message"]["content"])

                finally:
                    #使い終わった一時ファイルを掃除する
                    if os.path.exists(tmp_file_path):
                        os.remove(tmp_file_path)
        else:
            st.warning("理想や希望の文章を入力してください。")