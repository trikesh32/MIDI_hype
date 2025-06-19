TR_DEFAULT_MIDI_CHANNEL = 7
TR_midi_ch = TR_DEFAULT_MIDI_CHANNEL - 1
TR_mode_g = 0
TR_header = [0xf0, 0x42]
TR_result = []


def print_res(result):
    for res in result:
        for _ in res:
            print("0" * (2 - (len(hex(_)) - 2)) + hex(_)[2:], end=' ')
        print()


def create_first_message():
    global mode_g, midi_ch
    try:
        midi_no = int(input("Введите номер миди канала (по умолчанию 7): ")) - 1
    except Exception:
        midi_no = TR_DEFAULT_MIDI_CHANNEL - 1
    midi_ch = midi_no
    mode = int(input("1. combi\n2. prog\nВведите режим: "))
    while mode not in range(1, 3):
        mode = int(input("Фигня: "))
    if mode == 1:
        mode_g = 0
    else:
        mode_g = 2
    message = [0xf0, 0x42, 0x30 + midi_no, 0x63, 0x4e, mode_g, 0xf7]
    TR_result.append(message)
    return message


def create_second_message():
    if mode_g == 0:
        bank = int(input("0.A\n1.B\n2.C\nВведите банк: "))
        if bank not in range(3):
            bank = int(input("Фигня: "))
        patch_no = int(input("Введите номер патча(0...127): "))
        message = [0xF0, 0x42, 0x63, 0xB0 + midi_ch, 0, 0, 0xB0 + midi_ch, 32, bank, 0xC0 + midi_ch, patch_no, 0xf7]
        TR_result.append(message)
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
            first_byte = 0x79
            second_byte = 0
        elif mode == 5:
            first_byte = 0x78
            second_byte = 0
        patch_no = int(input("Введите номер патча(0...128):"))
        if mode == 4 or mode == 5:
            patch_no -= 1
        message = [0xF0, 0x42, 0x63, 0xB0 + midi_ch, 0, first_byte, 0xB0 + midi_ch, 32, second_byte, 0xC0 + midi_ch, patch_no, 0xf7]
        TR_result.append(message)


def create_third_message():
    mode = int(input("0.ARP-OFF\n1.ARP-ON\nВведите: "))
    message = [0xf0, 0x42, 0x63, 0xB0 + midi_ch, 0x63, 0, 0xB0 + midi_ch, 0x62, 0x2, 0xB0 + midi_ch, 6, 0 if mode == 0 else 0x7f, 0xf7]
    TR_result.append(message)
    if mode == 1:
        create_other_messages()


def create_other_messages():
    TR_result.append(
        [0xf0, 0x42, 0x63, 0xB0 + midi_ch, 0x63, 0, 0xB0 + midi_ch, 0x62, 0xA, 0xB0 + midi_ch, 6, int(input("Введите ARG-GATE(0...127): ")), 0xF7]
    )
    TR_result.append(
        [0xf0, 0x42, 0x63, 0xB0 + midi_ch, 0x63, 0, 0xB0 + midi_ch, 0x62, 0xB, 0xB0 + midi_ch, 6,
         int(input("Введите ARP-VELOCITY(0...127): ")), 0xF7]
    )


def TR_main():
    print("ИДЕТ НАСТРОЙКА TR")
    create_first_message()
    create_second_message()
    create_third_message()
    return TR_result


if __name__=="__main__":
    print_res(TR_main())



