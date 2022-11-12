
def yes_no_input():
    while True:
        choice = input(" 'yes'か'no'で答えてください [y/N]: ").lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False

print("実行したい処理を選んで、番号を入力してください")
print("楽曲のパラメータを設定しますか？")
input_number = input("設定する場合は1、設定しない場合は2を入力してください：")
number = int(input_number)

paramata = []

if number == 1:
    print("パラメータを設定しますか？")
    if yes_no_input():
        print("既存曲を入力する場合はファイル名を記入してください")
        input_song = input()
        if not input_song:
            song = ''
            print("指定されませんでした")
        else:
            song = " --input "+input_song

        print("コード進行を'|'で区切って記入してください")
        input_chord = input()
        if not input_chord:
            chord = ''
            print("指定されませんでした")
        else:
            chord = " --chord "+"'"+input_chord+"'"

        print("出力ファイル名を設定する場合は記入してください")
        input_output = input()
        if not input_output:
            output = ''
            print("指定されませんでした")
        else:
            output = " --output "+input_output

        
        print("さらに詳細のパラメータを設定しますか？")
        if yes_no_input():
            print("1小節ごとのコード進行を指定してください<デフォルト2>")
            input_chordbeat = input()
            if not input_chordbeat:
                chordbeat = ''
                print("指定されませんでした")
            else:
                chordbeat = " --chordbeat "+input_chordbeat

            print("生成される曲の小節数を記入してください<デフォルト8>")
            input_numbars = input()

            if not input_numbars:
                numbars = ''
                print("指定されませんでした")
            else:
                numbars = " --num_bars "+input_numbars


            print("テンポを指定してください<デフォルト120>")
            input_tempo = input()
            if not input_tempo:
                tempo = ''
                print("指定されませんでした")
            else:
                tempo = " --tempo "+input_tempo

            print("↓これをコマンドに入力してください")
            print("!python cogmacreater.py "+song+chord+output+chordbeat+numbars+tempo)

        else:
            print("↓これをコマンドに入力してください")
            print("!python cogmacreater.py "+song+chord+output)
    else:
        print("↓これをコマンドに入力してください")
        print("!python cogmacreater.py")

if number == 2:
    print("↓これをコマンドに入力してください")
    print("!python cogmacreater.py")
    # print("!python samplelistening.py\nimport IPython.display\nIPython.display.Audio('sample.wav')")
