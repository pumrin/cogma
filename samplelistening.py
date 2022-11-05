import wave
import struct
import numpy as np
from collections import OrderedDict
import simpleaudio
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
    'ファ#_':739.989
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
Db = ['ド#','ファ','ソ＃']
D = ['レ','ファ＃','ラ']
Eb = ['レ#','ソ','ラ#']
E = ['ミ','ソ#','シ']
F = ['ファ','ラ','ド_']
Gb = ['ファ#','ラ#','ド#_']
G = ['ソ','シ','レ_']
Ab = ['ソ#','ド_','レ#_']
A = ['ラ','ド#_','ミ_']
Bb = ['ラ#','レ_','ファ_']
B = ['シ','レ#','ファ#_']
Cm = ['ド','レ#','ソ']
Dbm = ['ド#','ミ','ソ#']
Dm = ['レ','ファ','ラ']
Ebm = ['ド','ミ','ソ']
Em = ['ミ','ソ','シ']
Fm = ['ファ','ソ#','ド_']
Gbm = ['ファ#','ラ','ド#_']
Gm = ['ソ','ラ#','レ_']
Abm = ['ソ','シ','レ#_']
Am = ['ラ','ド_','ミ_']
Bbm =['ラ#','ド#_','ファ_']
Bm = ['シ','レ_','ファ#_']
C_ = ['ド_','ミ_','ソ_']


dct = {
    'C':C,
    'Db':Db,
    'D':D,
    'Eb':Eb,
    'E':E,
    'F':F,
    'Gb':Gb,
    'G':G,
    'Ab':Ab,
    'A':A,
    'Bb':Bb,
    'B':B,
    'Cm':Cm,
    'Dbm':Dbm,
    'Dm':Dm,
    'Ebm':Ebm,
    'Em':Em,
    'Fm':Fm,
    'Gbm':Gbm,
    'Gm':Gm,
    'Abm':Abm,
    'Am':Am,
    'Bbm':Bbm,
    'Bm':Bm,
    'C_':C_
}
c = input()
c_list = c.split('|')
input_chord = [0]*len(c_list)
for i in range(len(c_list)):
    input_chord[i] = [dct[c_list[i]], 1/3]


rec = Recorder(input_chord)
rec.save('sample.wav')

wav_obj = simpleaudio.WaveObject.from_wave_file("sample.wav")
play_obj = wav_obj.play()
play_obj.wait_done()

if not play_obj.is_playing():
    os.remove('sample.wav')