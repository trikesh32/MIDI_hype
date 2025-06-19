XP60_DEFAULT_ID = 18

XP60_header = [0xf0, 0x41, 0x11, 0x6a, 0x12]
XP60_end = [0xf7]


def calculate_cs(message):
    summ = 0
    for i in range(len(message)):
        summ += message[i]
    return (128 - (summ % 128)) % 128


def create_first_message(mode):
    message = [0, 0, 0, 0, mode]
    message.append(calculate_cs(message))
    message += XP60_end
    message = XP60_header + message
    return message


def create_perform_message():
    message = [0, 0, 0, 1]
    bank = int(input("0.user\n1.PR-A\n2.PR-B\n3. card\nВведите банк: "))
    while bank not in range(4):
        bank = int(input("Фигня: "))
    arg = int(input("Введите номер перформанса(1...32): "))
    while arg not in range(1, 33):
        arg = int(input("Фигня: "))
    if bank == 0:
        message.append(arg - 1)
    elif bank == 1:
        message.append(64 - 1 + arg)
    elif bank == 2:
        message.append(96 - 1 + arg)
    elif bank == 3:
        message.append(32 - 1 + arg)
    message.append(calculate_cs(message))
    message += XP60_end
    message = XP60_header + message
    return message


def create_octava_message():
    octava = int(input("Введите октаву (-3...0...3)"))
    while octava not in range(-3, 4):
        octava = int(input("Фигня: "))
    message = [0, 0, 0, 0x2d, octava + 3]
    message.append(calculate_cs(message))
    message+= XP60_end
    message = XP60_header + message
    return message

def create_patch_messages():
    res = []
    message = [0, 0, 0, 2]
    mode = int(input("0.user&preset\n1.PCM\n2.EXP\nВведите тип группы патча: "))
    while mode not in range(3):
        mode = int(input("Фигня"))
    message = [0, 0, 0, 2, mode]
    message.append(calculate_cs(message))
    message += XP60_end
    message = XP60_header + message
    res.append(message)


    patch_group_id = int(input("1.user\n2.card\n3.PR-A\n4.PR-B\n5.PR-C\n6.GM\nВведите patch group id: "))
    while patch_group_id not in range(1, 7):
        patch_group_id = int(input("Фигня: "))
    message = [0, 0, 0, 3, patch_group_id]
    message.append(calculate_cs(message))
    message += XP60_end
    message = XP60_header + message
    res.append(message)

    patch_no = int(input("Введите номер патча(1 - 128): "))
    while patch_no not in range(1, 129):
        patch_no = int(input("Фигня: "))
    patch_no -= 1
    message = [0, 0, 0, 4, patch_no // 16, patch_no % 16]
    message.append(calculate_cs(message))
    message += XP60_end
    message = XP60_header + message
    res.append(message)
    return res
def print_res(result):
    for res in result:
        for _ in res:
            print("0" * (2 - (len(hex(_)) - 2)) + hex(_)[2:], end=' ')
        print()


def XP60_main():
    print("ИДЕТ НАСТРОЙКА XP60")
    try:
        XP60_header[2] = int(input("введите номер ID device для миди канала 3 (enter для ID по умолч. 18): ")) - 1
    except Exception:
        XP60_header[2] = XP60_DEFAULT_ID - 1
    result = []
    mode = int(input("0. perf\n1. patch\n2. gm\nВведите режим: "))
    while mode not in range(0, 3):
        mode = int(input("Фигня: "))
    result.append(create_first_message(mode))
    if mode == 0:
        result.append(create_perform_message())
    if mode == 1:
        result += create_patch_messages()
    result.append(create_octava_message())
    return result


if __name__ == "__main__":
    print_res(XP60_main())


