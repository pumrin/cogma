import wave
import struct
import numpy as np
from collections import OrderedDict
# import simpleaudio
import os
### 各種定数
VOLUME = 1
SAMPLE_RATE = 44100
TONES = {
    'ド': 261.626,
    'ド#':277.183,
    'レ': 293.665,
    'レ#':311.127,
    'ミ': 329.628,
    'ファ': 349.228,
    'ファ#':369.994,
    'ソ': 391.995,
    'ソ#':415.305,
    'ラ': 440.000,
    'ラ#':466.164,
    'シ': 493.883,
    'ド_':523.251,
    'ド#_':554.365,
    'レ_':587.330,
    'レ#_':622.254,
    'ミ_':659.255,
    'ファ_':698.456,
    'ファ#_':739.989,
    'ソ_':783.991,
    'ソ#_':830.609,
    'ラ_':880.000,
    'ラ#_':932.328,


}
#参考：https://www.petitmonte.com/javascript/musical_scale_frequency.html
### レコーダークラス
class Recorder:
    melody = []
    def __init__(self, melody):
        # 楽譜格納
        self.melody = melody
    def generate_tone(self, tones, beat, bpm=120):
        """周波数の配列を生成して返却
        Args:
            tones (list): 生成する音の周波数
            beat (float): 再生時間
        Returns:
            list: 生成された波形配列
        """
        sec = bpm / 60 * beat
        t = np.arange(0, SAMPLE_RATE * sec)
        y = None
        for tone in tones:
            # 和音対応（各音の配列を足し合わせると和音になる）
            f = TONES[tone] if tone in TONES else 0
            if y is None:
                y = VOLUME * np.sin(2 * np.pi * f * t / SAMPLE_RATE)
            else:
                y += VOLUME * np.sin(2 * np.pi * f * t / SAMPLE_RATE).tolist()
        return y.tolist()
    def save_as_wave(self, y, filename):
        """waveファイル出力
        Args:
            y (ndarray): wavファイルに出力する波形配列
            filename (str): 出力ファイル名
        Returns:
            None
        """
        max_num = 32767.0 / max(y)
        bit = [int(x * max_num) for x in y]
        waves = struct.pack("i" * len(bit), *bit)
        w = wave.Wave_write(filename)
        w.setparams((1, 2, SAMPLE_RATE, len(waves), 'NONE', 'not compressed'))
        w.writeframes(waves)
        w.close()
    def save(self, filename):
        """セットした楽譜から配列を作成し音声ファイルを出力
        Args:
            filename (str): 出力ファイル名
        """
        song = []
        for note in self.melody:
            song += self.generate_tone(*note)
        self.save_as_wave(np.array(song), filename)

C = ['ド','ミ','ソ']
Cm = ['ド','レ#','ソ']
C7 =['ド','ミ','ソ','ラ#']
Cm7=['ド','レ#','ソ','ラ#']
CM7=['ド','ミ','ソ','シ']
Cm7_5 =['ド','レ#','ファ#','ラ#']
# Cdim=[]
# Csus4=[]
# C7sus4=[]
# Caug=[]
# Cm6=[]
# C7_9=[]
# Cm7_9=[]
# Cadd9=[]
# C6=[]
# CmM7=[]
# C7_5=[]

Db = ['ド#','ファ','ソ#']
Dbm = ['ド#','ミ','ソ#']
D = ['レ','ファ#','ラ']
Dm = ['レ','ファ','ラ']
D7 =['レ','ファ#','ラ','ド_']
Dm7=['レ','ファ','ラ','ド_']
DM7=['レ','ファ#','ラ','ド#_']
Dm7_5 =['レ','ファ','ソ#','ド_']


Eb = ['レ#','ソ','ラ#']
Ebm = ['ド','ミ','ソ']
E = ['ミ','ソ#','シ']
Em = ['ミ','ソ','シ']
E7 =['ミ','ソ#','シ','レ_']
Em7=['ミ','ソ','シ','レ_']
EM7=['ミ','ソ#','シ','レ#_']
Em7_5 =['ミ','ソ','ラ#','レ_']


F = ['ファ','ラ','ド_']
Fm = ['ファ','ソ#','ド_']
F7 =['ファ','ラ','ド_','レ#_']
Fm7=['ファ','ソ#','ド','レ#_']
FM7=['ファ','ラ','ド_','ミ_']
Fm7_5 =['ファ','ソ#','シ','レ#_']

Gb = ['ファ#','ラ#','ド#_']
Gbm = ['ファ#','ラ','ド#_']

G = ['ソ','シ','レ_']
Gm = ['ソ','ラ#','レ_']
G7 =['ソ','シ','レ_','ファ_']
Gm7=['ソ','ラ#','レ_','ファ_']
GM7=['ソ','シ','レ_','ファ#_']
Gm7_5 =['ソ','ラ#','ド#_','ファ_']

Ab = ['ソ#','ド_','レ#_']
Abm = ['ソ','シ','レ#_']
A = ['ラ','ド#_','ミ_']
Am = ['ラ','ド_','ミ_']
A7 =['ラ','ド#_','ミ_','ソ_']
Am7=['ラ','ド_','ミ_','ソ_']
AM7=['ラ','ド#_','ミ_','ソ#_']
Am7_5 =['ラ','ド#_','レ#_','ソ_'] 

Bb = ['ラ#','レ_','ファ_']
Bbm =['ラ#','ド#_','ファ_']
B = ['シ','レ#','ファ#_']
Bm = ['シ','レ_','ファ#_']
B7 =['シ','レ#','ファ#_','ラ_']
Bm7=['シ','レ_','ファ#_','ラ_']
BM7=['シ','レ_','ファ#_','ラ#_']
Bm7_5 =['シ','レ_','ファ_','ラ_'] 

C_ = ['ド_','ミ_','ソ_']

dct = {
    'C':C,
    'Cm':Cm,
    'C7':C7,
    'Cm7':Cm7,
    'CM7':CM7,
    'Cm7-5':Cm7_5,
    # 'Cdim':Cdim,
    # 'Csus4':Csus4,
    # 'C7sus4':C7sus4,
    # 'Caug':Caug,
    # 'Cm6':Cm6,
    # 'C7(9)':C7_9,
    # 'Cm7(9)':Cm7_9,
    # 'Cadd9':Cadd9,
    # 'C6':C6,
    # 'CmM7':CmM7,
    # 'C7-5':C7_5,

    'Db':Db,
    'Dbm':Dbm,
    'D':D,
    'Dm':Dm,
    'D7':D7,
    'Dm7':Dm7,
    'DM7':DM7,
    'Dm7-5':Dm7_5,


    'Eb':Eb,
    'Ebm':Ebm,
    'E':E,
    'Em':Em,
    'E7':E7,
    'Em7':Em7,
    'EM7':EM7,
    'Em7-5':Em7_5,

    'F':F,
    'Fm':Fm,
    'E7':E7,
    'Em7':Em7,
    'EM7':EM7,
    'Em7-5':Em7_5,

    'Gb':Gb,
    'Gbm':Gbm,
    'Gm':Gm,
    'G':G,
    'G7':G7,
    'Gm7':Gm7,
    'GM7':GM7,
    'Gm7-5':Gm7_5,

    'Ab':Ab,
    'A':A,
    'Abm':Abm,
    'Am':Am,
    'A7':A7,
    'Am7':Am7,
    'AM7':AM7,
    'Am7-5':Am7_5,

    'Bb':Bb,
    'B':B,
    'Bbm':Bbm,
    'Bm':Bm,
    'B7':B7,
    'Bm7':Bm7,
    'BM7':BM7,
    'Bm7-5':Bm7_5,
    
    'C_':C_
}

print("試し聞きしたいコード進行を「|」で区切って入力してください")
c = input()
c_list = c.split('|')
input_chord = [0]*len(c_list)
for i in range(len(c_list)):
    input_chord[i] = [dct[c_list[i]], 1/3]


rec = Recorder(input_chord)
rec.save('sample.wav')

# wav_obj = simpleaudio.WaveObject.from_wave_file("sample.wav")
# play_obj = wav_obj.play()
# play_obj.wait_done()

# if not play_obj.is_playing():
#     os.remove('sample.wav')
