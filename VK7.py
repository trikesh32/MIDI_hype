VK7_DEFAULT_MIDI_CHANNEL = 6
VK7_header = [0xC0]


def print_res(result):
    for res in result:
        print("0" * (2 - (len(hex(res)) - 2)) + hex(res)[2:], end=' ')


def VK7_main():
    print("ИДЕТ НАСТРОЙКА VK7")
    try:
        VK7_header[0] += int(input("введите номер MIDI channel для id device 19 (по умолчанию 6): ")) - 1
    except Exception:
        VK7_header[0] += VK7_DEFAULT_MIDI_CHANNEL - 1
    result = []
    bank_no = int(input("Введите номер банка(1...8): "))
    while bank_no not in range(1, 9):
        bank_no = int(input("Фигня: "))
    patch_no = int(input("Введите номер патча(1...8): "))
    while patch_no not in range(1, 9):
        patch_no = int(input("Фигня: "))
    result.append(VK7_header[0])
    result.append((bank_no - 1) * 8 + patch_no - 1)
    result = [result]
    return result


if __name__ == "__main__":
    print_res(VK7_main())


