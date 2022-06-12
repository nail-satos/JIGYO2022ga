# 追加インストールしたライブラリ
import numpy as np
import pandas as pd 
import streamlit as st

def main():
    """ メインモジュール
    """

    # セッションステートを初期化する
    if 'ini_flg' not in st.session_state:

        st.session_state.ini_flg = True

        # パラーメータの初期設定（CO2排出量）
        temp = []
        # temp.append([10,10,10,10])   # マシンA（製造時、交換時、整備時、遊休時）
        # temp.append([ 3, 3, 3, 3])   # マシンB（製造時、交換時、整備時、遊休時）
        # temp.append([ 1, 1, 1, 1])   # マシンC（製造時、交換時、整備時、遊休時）
        temp.append([10, 7, 5, 3])   # マシンA（製造時、交換時、整備時、遊休時）
        temp.append([ 5, 4, 3, 2])   # マシンB（製造時、交換時、整備時、遊休時）
        temp.append([ 3, 2, 1, 1])   # マシンC（製造時、交換時、整備時、遊休時）
        st.session_state.co2_params_list = temp

        # パラーメータの初期設定（製造能力:キャパシティ）
        temp = []
        temp.append([10, 10,  5])   # マシンA（部品α、部品β、部品γ）
        temp.append([ 7,  5,  3])   # マシンB（部品α、部品β、部品γ）
        temp.append([ 5,  4,  2])   # マシンC（部品α、部品β、部品γ）
        st.session_state.cap_params_list = temp

        # パラメータの初期設定（稼働率）
        st.session_state.operating_rate = 75

        # # パラメータの初期設定（未生産分のペナルティ）
        # st.session_state.incomplete_loss = 100

        # # パラメータの初期設定（作りすぎのペナルティ）
        # st.session_state.complete_loss = 20


    # stのタイトル表示
    st.title("遺伝的アルゴリズム\n（製造機器の稼働におけるCO2排出量の最適化問題)")

    # ファイルのアップローダー
    uploaded_file = st.sidebar.file_uploader("データのアップロード", type='csv') 

if __name__ == "__main__":
    main()


