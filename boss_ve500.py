DEFAULT_MIDI_CHANNEL = 12
def create_dump(midi_channel, mode, prog_num):
    return [0xB0 + midi_channel, 0, mode, 0xB0 + midi_channel, 0x20, 0, 0xC0 + midi_channel, prog_num]




def factory_patches():
    while True:
        try:
            prog_num = int(input("Введите номер программы (1...50): ")) - 1
            if not (0 <= prog_num <= 0x31):
                raise ValueError
            break
        except Exception:
            print("Плохой ввод")
    return prog_num

def user_patches():
    while True:
        try:
            prog_num = int(input("Введите номер программы (1...99): ")) - 1
            if not (0 <= prog_num <= 98):
                raise ValueError
            break
        except Exception:
            print("Плохой ввод")
    return prog_num

def boss_ve500_main():
    print("ИДЕТ НАСТРОЙКА BOSS VE-500")
    try:
        midi_channel = int(input("Введите номер MIDI канала (по умолчанию 12): "))
    except Exception:
        midi_channel = DEFAULT_MIDI_CHANNEL
    print("ВЫБРАН MIDI КАНАЛ: ", midi_channel)
    while True:
        try:
            mode = int(input("1. Factory patches\n2. User patches\nВаш выбор: "))
            if mode != 1 and mode != 2:
                raise ValueError
            mode = 0 if mode == 2 else 1
            break
        except Exception:
            print("Плохой ввод, попробуйте еще")
    if mode == 1:
        print("Выбран режим: Factory patches")
        last_byte = factory_patches()
    else:
        print("Выбран режим: User patches")
        last_byte = user_patches()
    return [create_dump(midi_channel, mode, last_byte)]

def print_res(result):
    for res in result:
        for _ in res:
            print("0" * (2 - (len(hex(_)) - 2)) + hex(_)[2:], end=' ')
        print()

if __name__ == "__main__":
    print_res(boss_ve500_main())