from datetime import datetime
import streamlit as st
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt


st.sidebar.title("メニュー")

page = st.sidebar.radio(
    "選んでください",
    ["ホーム", "貯金状況", "貯金履歴", "グラフ"]
)

st.title("推し貯金サイト")

if "total" not in st.session_state:
    
    total = 0

    if os.path.exists("saving_data.csv"):

        with open("saving_data.csv", "r") as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) >= 3:
                    total += int(row[2])
                

    st.session_state["total"] = total

if "goal" not in st.session_state:
    st.session_state["goal"] = 50000

if page == "ホーム":
    st.divider()

    st.subheader("貯金理由")
    reason = st.text_input("貯金する理由")

    goal = st.number_input(
        "目標金額",
        min_value=0,
        step=1000,
        value=st.session_state["goal"]
    )

    st.session_state["goal"] = goal

    st.subheader("今日の貯金")
    saving = st.number_input("今日の貯金額", min_value=0, step=100)

    memo = st.text_area("メモ")

    if st.button("記録する"):

        st.session_state["total"] += saving

        with open("saving_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            today = datetime.now().strftime("%Y-%m-%d")
            writer.writerow([today, reason, saving, memo])

        total = st.session_state["total"]
        remaining = goal - total

        if goal > 0:
            percent = (total / goal) * 100
        else:
            percent = 0

        st.success("記録しました！")

    if st.button("データをリセット"):

        st.session_state["total"] = 0

        with open("saving_data.csv", "w") as file:
            pass

        st.success("リセットしました！")

if page == "貯金状況":
    st.divider()

    st.subheader("貯金状況")

    total = st.session_state["total"]
    goal = st.session_state["goal"]
    remaining = goal - total

    if goal > 0:
        percent = (total / goal) * 100
    else:
        percent = 0    

    st.write("現在の貯金額:", total, "円")
    st.write("目標まであと:", remaining, "円")
    st.write("達成率:", round(percent,1), "%")
    st.progress(percent / 100)

    if percent >= 100:
        st.success("目標達成！")
        st.balloons()

if page == "貯金履歴":
    st.divider()

    st.subheader("貯金履歴")

    if os.path.exists("saving_data.csv"):
        with open("saving_data.csv", "r") as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) >= 4:
                    st.write("日付:", row[0])
                    st.write("理由:", row[1])
                    st.write("貯金額:", row[2], "円")
                    st.write("メモ:", row[3])

                st.divider()
    else:
        st.write("まだ記録がありません")

if page == "グラフ":
    st.divider()
    st.subheader("貯金グラフ")

    if os.path.exists("saving_data.csv"):

        df = pd.read_csv(
            "saving_data.csv",
            header=None,
            names=["日付", "理由", "貯金額", "メモ"]
        )

        df = df.groupby("理由")["貯金額"].sum()
        
        fig, ax = plt.subplots()

        ax.pie(
            df,
            labels=df.index,
            autopct="%1.1f%%"
        )

        st.pyplot(fig)

    else:
        st.write("まだグラフにする記録がありません")