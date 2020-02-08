from time import sleep
import cv2
import serial

# 内蔵カメラのID
BUILT_IN_CAMERA_ID = 0

# 縮小したときのサイズ
RESIZED_WIDTH = 160
RESIZED_HEIGHT = 90

# 白黒2値化するときの閾値
BINARY_THRESHOLD = 100

# 画面が光ったとみなす閾値 (許容するパーセンテージ)
WHITEOUT_THRESHOLD = 0.03

# Arduinoとの通信設定
SERIAL_DEVICE = '/dev/tty.usbmodem141101'
SERIAL_BAUDRATE = 9600


def dodge_lightning(ser):
    ser.write(b'd')
    print('dodge!!')


def is_whiteout(frame, width, height):
    pixels = height * width
    count = 0
    for y in range(height):
        for x in range(width):
            value = frame[y, x]
            # 黒のドットを数える
            if value != 255:
                count += 1

    # 黒のドットが一定の割合以下ならばTrue    
    return (count / pixels <= WHITEOUT_THRESHOLD)


def detect_lightning(frame):

    # 高速化のためにリサイズ
    frame = cv2.resize(frame, (RESIZED_WIDTH, RESIZED_HEIGHT))

    # グレースケールに変換
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 白黒2値化する
    ret, frame = cv2.threshold(frame, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)

    # 現在の画像を表示 (デバッグ用)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise Exception('quit')

    # フレームが完全に白くなれば避ける
    if is_whiteout(frame, RESIZED_WIDTH, RESIZED_HEIGHT):
        return True

    return False


def main():

    # カメラを起動
    capture = cv2.VideoCapture(BUILT_IN_CAMERA_ID)

    if not capture.isOpened():
        raise Exception('Video is not open.')

    # シリアルポートをオープン
    ser = serial.Serial()
    ser.port = SERIAL_DEVICE
    ser.baudrate = SERIAL_BAUDRATE
    ser.setDTR(False)
    ser.open()

    sleep(2)

    while(True):
        # フレームをキャプチャ
        ret, frame = capture.read()

        # 雷を検知したら避ける
        if detect_lightning(frame):
            dodge_lightning(ser)
            sleep(0.5)

    ser.close()

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
