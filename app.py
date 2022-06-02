""" streamlit_demo
streamlitでIrisデータセットの分析結果を Web アプリ化するモジュール

【Streamlit 入門 1】Streamlit で機械学習のデモアプリ作成 – DogsCox's tech. blog
https://dogscox-trivial-tech-blog.com/posts/streamlit_demo_iris_decisiontree/
"""

# 追加インストールしたライブラリ
import numpy as np
import pandas as pd 
import streamlit as st
import matplotlib.pyplot as plt 
import japanize_matplotlib
import seaborn as sns 

# ロゴの表示用
from PIL import Image

# 標準ライブラリ
import random
import copy

sns.set()
japanize_matplotlib.japanize()  # 日本語フォントの設定

# matplotlib / seaborn の日本語の文字化けを直す、汎用的かつ一番簡単な設定方法 | BOUL
# https://boul.tech/mplsns-ja/

def st_display_table(title, df: pd.DataFrame):

    # データフレームを表示
    st.subheader(title)
    st.table(df)

    # Streamlitでdataframeを表示させる | ITブログ
    # https://kajiblo.com/streamlit-dataframe/


def create_1st_generation(df: pd.DataFrame):

    i = 0
    while i < 30:

        # ランダム：稼働させる機器の番号(0～2)
        maschine = random.randint(0,2)

        # ランダム：稼働させる時間帯(0～23)
        hour = random.randint(0,23)

        status = df.iloc[maschine, hour]

        # 稼働状況が0=停止、または 1=遊休の場合
        if status == '停止' or status == '遊休':
            # print('この機械は空いています')
            df.iloc[maschine, hour] = '製造'
            i = i + 1
        else:
            print('この機械は使われています')

    return(df)


def main():
    """ メインモジュール
    """

    # セッションステートを初期化する
    if 'ini_flg' not in st.session_state:

        st.session_state.ini_flg = True

        st.session_state.ma_co2 = 10
        st.session_state.ma_chg = 7
        st.session_state.ma_mnt = 5
        st.session_state.ma_idl = 3


    # stのタイトル表示
    st.title("遺伝的アルゴリズム\n（製造機器の稼働におけるCO2排出量の最適化問題)")

    # ファイルのアップローダー
    uploaded_file = st.sidebar.file_uploader("データのアップロード", type='csv') 

    # サイドメニューの設定
    activities = ["製造指示確認", "ＣＯ２排出量", "部品製造能力", "最適化の実行", "About"]
    choice = st.sidebar.selectbox("Select Activity", activities)

    if choice == '製造指示確認':
        # アップロードの有無を確認
        if uploaded_file is not None:

            # データフレームの読み込み（一番左端の列をインデックスに設定）
            df = pd.read_csv(uploaded_file, index_col=0)

            # 表示する件数
            cnt = st.sidebar.slider('表示する件数', 1, len(df), 3)

            # テーブルの表示
            st_display_table('製造指示データ', df.head(int(cnt)))

        else:
            st.subheader('製造指示データをアップロードしてください')

    if choice == 'ＣＯ２排出量':

        # 高評価ボタン＆低評価ボタン
        col1, col2, col3 = st.columns(3)

        with col1:

            st.text('マシンＡの性能')
            st.session_state.ma_co2 = st.number_input('製造時のCO2排出量(/h)', value=10)
            st.session_state.ma_chg = st.number_input('交換時のCO2排出量(/h)', value=7)
            st.session_state.ma_mnt = st.number_input('整備時のCO2排出量(/h)', value=5)
            st.session_state.ma_idl = st.number_input('遊休時のCO2排出量(/h)', value=3)

        with col2:

            st.text('マシンＢの性能')
            mb_co2 = st.number_input('製造時のCO2排出量(/h)', value=5)
            mb_chg = st.number_input('交換時のCO2排出量(/h)', value=4)
            mb_mnt = st.number_input('整備時のCO2排出量(/h)', value=3)
            mb_idl = st.number_input('遊休時のCO2排出量(/h)', value=2)

        with col3:

            st.text('マシンＣの性能')
            mc_co2 = st.number_input('製造時のCO2排出量(/h)', value=3)
            mc_chg = st.number_input('交換時のCO2排出量(/h)', value=2)
            mc_mnt = st.number_input('整備時のCO2排出量(/h)', value=1)
            mc_idl = st.number_input('遊休時のCO2排出量(/h)', value=1)

    if choice == '部品製造能力':

        # 高評価ボタン＆低評価ボタン
        col1, col2, col3 = st.columns(3)

        with col1:

            st.text('マシンＡの性能')
            ma_a = st.number_input('部品αの製造能力(/h)', value=10)
            ma_b = st.number_input('部品βの製造能力(/h)', value=10)
            ma_g = st.number_input('部品γの製造能力(/h)', value=5)

        with col2:

            st.text('マシンＢの性能')
            mb_a = st.number_input('部品αの製造能力(/h)', value=5)
            mb_b = st.number_input('部品βの製造能力(/h)', value=5)
            mb_g = st.number_input('部品γの製造能力(/h)', value=3)

        with col3:

            st.text('マシンＣの性能')
            mc_a = st.number_input('部品αの製造能力(/h)', value=3)
            mc_b = st.number_input('部品βの製造能力(/h)', value=3)
            mc_g = st.number_input('部品γの製造能力(/h)', value=1)


    if choice == '最適化の実行':

        # 表示する世代
        max_generation = st.sidebar.number_input('世代の最大値', value=1)
        prt_generation = st.sidebar.number_input('表示する世代', value=1)
        choice_graph = st.sidebar.selectbox("評価値の遷移グラフ", ['表示しない','表示する'])


        # データフレームの読み込み
        df_norma = pd.read_csv(uploaded_file)

        # テーブルの表示
        st_display_table('製造指示データ', df_norma)


        # 第0世代の生成
        # データフレームの読み込み（一番左端の列をインデックスに設定）
        df_shift = pd.read_csv('稼働状況.csv', index_col=0)
        st_display_table('第0世代', df_shift)

        # zero = np.zeros((3,24))
        # df_shift = pd.DataFrame(zero)

        # 第1世代の生成
        df_shift = create_1st_generation(df_shift)
        st_display_table('第1世代', df_shift)

        if choice_graph == '表示する':

            chart_data = pd.DataFrame(
                np.random.randn(20, 3),
                columns=['a', 'b', 'c'])

            st.line_chart(chart_data)


    if choice == 'About':

        image = Image.open('logo_nail.png')
        st.image(image)

        st.markdown("Built by [Nail Team]")
        st.text("Version 0.1")
        st.markdown("For More Information check out   (https://nai-lab.com/)")
        

if __name__ == "__main__":
    main()


