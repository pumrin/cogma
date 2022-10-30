#coding:utf-8
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import librosa #インストールしてください!
import librosa.display
import functions as fn
import soundfile as sf
import sys

def beatstest(file_name):
    #######################################
    wave, fs = librosa.load(file_name)
    hop_length = 512
    onset_env = librosa.onset.onset_strength(y=wave, sr=fs, hop_length=hop_length, aggregate=np.median)
    times = librosa.times_like(onset_env, sr=fs, hop_length=hop_length)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=fs)

    #######################################3

    # クロマグラムを求めます
    chroma = fn.librosa_chroma(file_name)

    TONES = 12 # ピッチクラス,音の種類の数
    sampling_rate = 44100 #音源依存

    # "この設定では",こんな感じで時間軸設定を求められます
    # (詳しくはドキュメントを読んで下さい)
    time_unit = 512.0 / 44100 # 1フレームのクロマグラムの長さ
    stop = time_unit * (chroma.shape[1])
    time_ruler = np.arange(0, stop, time_unit)

    ###コードのテンプレートベクトル
    #順番を保ちたいのでOrderdDictを使います
    one_third = 1.0/3
    one_fourth = 1.0/4
    chord_dic = OrderedDict()
    chord_dic["C"] = [one_third, 0,0,0, one_third, 0,0, one_third, 0,0,0,0]
    chord_dic["Db"] = [0, one_third, 0,0,0, one_third, 0,0, one_third, 0,0,0]
    chord_dic["D"] = [0,0, one_third, 0,0,0, one_third, 0,0, one_third, 0,0]
    chord_dic["Eb"] = [0,0,0, one_third, 0,0,0, one_third, 0,0, one_third, 0]
    chord_dic["E"] = [0,0,0,0, one_third, 0,0,0, one_third, 0,0, one_third]
    chord_dic["F"] = [one_third, 0,0,0,0, one_third, 0,0,0, one_third, 0,0]
    chord_dic["Gb"] = [0, one_third, 0,0,0,0, one_third, 0,0,0, one_third, 0]
    chord_dic["G"] = [0,0, one_third, 0,0,0,0, one_third, 0,0,0, one_third]
    chord_dic["Ab"] = [one_third, 0,0, one_third, 0,0,0,0, one_third, 0,0,0]
    chord_dic["A"] = [0, one_third, 0,0, one_third, 0,0,0,0, one_third, 0,0]
    chord_dic["Bb"] = [0,0, one_third, 0,0, one_third, 0,0,0,0, one_third, 0]
    chord_dic["B"] = [0,0,0, one_third, 0,0, one_third, 0,0,0,0, one_third]
    chord_dic["Cm"] = [one_third, 0,0, one_third, 0,0,0, one_third, 0,0,0,0]
    chord_dic["Dbm"] = [0, one_third, 0,0, one_third, 0,0,0, one_third, 0,0,0]
    chord_dic["Dm"] = [0,0, one_third, 0,0, one_third, 0,0,0, one_third, 0,0]
    chord_dic["Ebm"] = [0,0,0, one_third, 0,0, one_third, 0,0,0, one_third, 0]
    chord_dic["Em"] = [0,0,0,0, one_third, 0,0, one_third, 0,0,0, one_third]
    chord_dic["Fm"] = [one_third, 0,0,0,0, one_third, 0,0, one_third, 0,0,0]
    chord_dic["Gbm"] = [0, one_third, 0,0,0,0, one_third, 0,0, one_third, 0,0]
    chord_dic["Gm"] = [0,0, one_third, 0,0,0,0, one_third, 0,0, one_third, 0]
    chord_dic["Abm"] = [0,0,0, one_third, 0,0,0,0, one_third, 0,0, one_third]
    chord_dic["Am"] = [one_third, 0,0,0, one_third, 0,0,0,0, one_third, 0,0]
    chord_dic["Bbm"] = [0, one_third, 0,0,0, one_third, 0,0,0,0, one_third, 0]
    chord_dic["Bm"] = [0,0, one_third, 0,0,0, one_third, 0,0,0,0, one_third]
    chord_dic["C7"] = [one_fourth,0,0,0,one_fourth,0,0,one_fourth,0,0,one_fourth,0]
    chord_dic["Cm7"] = [one_fourth,0,0,one_fourth,0,0,0,one_fourth,0,0,one_fourth,0]
    chord_dic["CM7"] = [one_fourth,0,0,0,one_fourth,0,0,one_fourth,0,0,0,one_fourth]
    chord_dic["E7"] = [0,0,one_fourth,0,one_fourth,0,0,0,one_fourth,0,0,one_fourth]


    prev_chord = 0
    sum_chroma = np.zeros(TONES)
    estimate_chords = []

    result = np.zeros((28, len(beats)))

    nth_chord = 0
    j = 0
    for time_index, time in enumerate(time_ruler):
        # 今は何番目のコードを解析しているのか
        #nth_chord = int(time) // 2
        if(j<len(beats)):
            if(time>=times[beats[j]]):
                nth_chord = nth_chord + 1
                j = j+1

        # 次の2秒間に移る時に,前の2秒間のコードを推定します
        if nth_chord != prev_chord:
            maximum = -100000
            this_chord = ""
            # コサイン類似度が最大になるコードを調べます
            for chord_index, (name, vector) in enumerate(chord_dic.items()):
                similarity = fn.cos_sim(sum_chroma, vector)
                result[chord_index][nth_chord - 1] = similarity
                if similarity > maximum:
                    maximum = similarity
                    this_chord = name
            # 初期化、推定したコードを格納します
            sum_chroma = np.zeros(TONES)
            estimate_chords.append(this_chord)

        else:
            # chromaのshapeに注意しながら足していきます
            if(time_index<chroma.shape[1]):
                for i in range(TONES):
                    sum_chroma[i] += chroma[i][time_index]


        # 更新
        prev_chord = nth_chord

    # 最終結果です
    chordResult = '|'.join(estimate_chords)
    return chordResult
    # print(chordResult)

if __name__ == '__main__':
    print(beatstest(filename))