X3_DEFAULT_MIDI_CHANNEL = 1
X3_midi_ch = X3_DEFAULT_MIDI_CHANNEL - 1
X3_mode_g = 0
X3_header = [0xf0, 0x42]
X3_result = []


def print_res(result):
    for res in result:
        for _ in res:
            print("0" * (2 - (len(hex(_)) - 2)) + hex(_)[2:], end=' ')
        print()


def create_first_message():
    global mode_g, midi_ch
    try:
        midi_no = int(input("Введите номер миди канала (по умолчанию 1): ")) - 1
    except Exception:
        midi_no = X3_DEFAULT_MIDI_CHANNEL - 1
    midi_ch = midi_no
    mode = int(input("1. combi\n2. prog\nВведите режим: "))
    while mode not in range(1, 3):
        mode = int(input("Фигня: "))
    if mode == 1:
        mode_g = 0
    else:
        mode_g = 2
    message = [0xf0, 0x42, 0x30 + midi_ch, 0x35, 0x4e, mode_g, 0, 0xf7]
    X3_result.append(message)
    return message


def create_second_message():
    if mode_g == 0:
        bank = int(input("0.A\n1.B\nВведите банк: "))
        while bank not in range(2):
            bank = int(input("Фигня: "))
        patch_no = int(input("Введите номер патча(0...99): "))
        message = [0xF0, 0x42, 0x30+ midi_ch, 0xB0 + midi_ch, 0, 0, 0xB0 + midi_ch, 32, bank, 0xC0 + midi_ch, patch_no, 0xf7]
        X3_result.append(message)
    else:
        mode =  int(input("0. A\n1. B\n2. C\n3. D\n4. GM\n5. GM drum\nВведите банк:"))
        if mode == 0:
           first_byte = 0
           second_byte = 0
        elif mode == 1:
           first_byte = 0
           second_byte = 1
        elif mode == 2:
           first_byte = 0
           second_byte = 2
        elif mode == 3:
           first_byte = 0
           second_byte = 3
        elif mode == 4:
            first_byte = 0x38
            second_byte = 0
        elif mode == 5:
            first_byte = 0x3e
            second_byte = 0
        patch_no = int(input("Введите номер патча(0...99 если A B C D, 1...128 для GM, 129...136 для GM drums): "))
        if mode == 4:
            patch_no -= 1
        if mode == 5:
            if patch_no == 129:
                patch_no = 0
            elif patch_no == 130:
                patch_no = 16
            elif patch_no == 131:
                patch_no = 25
            elif patch_no == 132:
                patch_no = 32
            elif patch_no == 133:
                patch_no = 40
            elif patch_no == 134:
                patch_no = 64
            elif patch_no == 135:
                patch_no = 24
            elif patch_no == 136:
                patch_no = 48
        message = [0xF0, 0x42, 0x30 + midi_ch, 0xB0 + midi_ch, 0, first_byte, 0xB0 + midi_ch, 32, second_byte, 0xC0 + midi_ch, patch_no, 0xf7]
        X3_result.append(message)


def X3_main():
    print("ИДЕТ НАСТРОЙКА X3")
    create_first_message()
    create_second_message()
    return X3_result

if __name__=="__main__":
    print_res(X3_main())



