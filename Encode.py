import wave
import random


def read_audio_file(file_path):
    # Открываем WAV файл и извлекаем из него необработанные данные
    with wave.open(file_path, 'rb') as wf:
        return wf.readframes(wf.getnframes())


def audio_info(file_path):
    with wave.open(file_path, 'rb') as wf:
        info = wf.getparams()
    return info


def frame_to_bin(frames):
    bits = []
    for i in range(len(frames)):
        bits.append("0" * (8 - len(str(bin(frames[i]))[2:])) + str(bin(frames[i]))[2:])
    return bits


def bin_to_frame(bits):
    frames = bytearray(len(bits))
    for i in range(0, len(bits)):
        frames[i] = int(bits[i], 2)
    return frames


def write_audio_file(data, file_path, info):
    # Записываем зашифрованные данные в новый WAV файл
    with wave.open(file_path, 'wb') as wf:
        wf.setparams(info)
        wf.writeframesraw(data)


def randseed():
    seed = ''
    seed = ''.join(str(random.randint(0, 1)) for i in range(64))
    return seed


def encode(seed, audio_data):
    # Инициализируем три РСЛОС заданным значением seed
    r1 = seed[0:19]
    r2 = seed[19:41]
    r3 = seed[41:64]
    key_stream = []
    k = 0
    l = len(audio_data)
    strarr = ''
    strCount = 0
    strout = ''
    for i in range(l * 8):  # Индикаторная
        if k == 0 and 0.25 <= i / (l * 8 - 1) < 0.5:
            print("25%", end='')
            k = 1
        if k == 1 and 0.5 <= i / (l * 8- 1) < 0.75:
            print("..50%", end='')
            k = 2
        if k == 2 and 0.75 <= i / (l * 8 - 1) < 1:
            print("..75%", end='')
            k = 3
        if k == 3 and i / (l * 8 - 1) == 1:
            print("..100%", end=' ')
            k = 0

        x = r1[8]  # Снятие бит синхронизации
        y = r2[10]
        z = r3[10]
        F = x and y or x and z or y and z
        if x == F:  # Сдвиг r1
            r1 = str(int(r1[13]) ^ int(r1[16]) ^ int(r1[17]) ^ int(r1[18]) ^ 1) + r1
            t1 = r1[19]
        else:
            t1 = 0
        if y == F:  # Сдвиг r2
            r2 = str(int(r2[20]) ^ int(r2[21]) ^ 1) + r2
            t2 = r2[22]
        else:
            t2 = 0
        if z == F:  # Сдвиг r3
            r3 = str(int(r3[7]) ^ int(r3[20]) ^ int(r3[21]) ^ int(r3[22]) ^ 1) + r3
            t3 = r3[23]
        else:
            t3 = 0
        r1 = r1[0:19]
        r2 = r2[0:22]
        r3 = r3[0:23]
        tout = ((int(t1) ^ int(t2) ^ int(t3)))  # Выходной бит

        strarr = audio_data[strCount]
        strout += str(int(strarr[len(strout)]) ^ tout)
        if len(strout) == 8:
            key_stream.append(strout)
            strout = ''
            strCount += 1
    return key_stream

InName = input("Enter the input file: ")

print("Reading audio file:", end=' ')
FrameInput = read_audio_file(InName)
print("Done.")

print("Getting audio info:", end=' ')
info = audio_info(InName)
print("Done.")

print("Converting frames to binary:", end=' ')
BinIn = frame_to_bin(FrameInput)
print("Done.")

print("Entering seed:", end=' ')
seed = randseed()
#seed = ''
print(seed)

print("Encoding:", end=' ')
BinOut = encode(seed, BinIn)
print("Done.")

print("Converting binary to frames:", end=' ')
FrameOut = bin_to_frame(BinOut)
print("Done.")

print("Writing new audio file:", end=' ')
write_audio_file(FrameOut, "coded.wav", info)
print("Done.")
