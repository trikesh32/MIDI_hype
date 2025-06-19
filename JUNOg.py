JUNO_G_DEFAULT_ID = 20

JUNO_G_header = [0xf0, 0x41, 0x13, 0x00, 0x00, 0x15,0x12]
JUNO_G_end = [0xf7]
JUNO_G_message1 = [
    [1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0],
    [1, 0, 0, 2, 0],
    [1, 0, 0, 3, 0],
    [1, 0, 0, 0x13, 0]
]
JUNO_G_message0= [
    [1, 0, 0, 0, 0],
    [1, 0, 0, 4, 0],
    [1, 0, 0, 5, 0],
    [1, 0, 0, 6, 0],
    [1, 0, 0, 0x13, 0]
]

def calculate_cs(message):
    summ = 0
    for i in range(5):
        summ += message[i]
    return (128 - (summ % 128)) % 128


def create_message(source_message, value):
    actual = []
    actual += source_message
    actual[-1] = value
    actual.append(calculate_cs(actual))
    actual += JUNO_G_end
    actual = JUNO_G_header + actual
    return actual

def print_res(result):
    for res in result:
        for _ in res:
            print("0" * (2 - (len(hex(_)) - 2)) + hex(_)[2:], end=' ')
        print()
def create_full(type):
    result = []
    result.append(create_message(JUNO_G_message0[0], type))

    if type == 0:
        choice = int(input("""
            0. user
            1. pr-a
            2. pr-b
            3. pr-c
            4. pr-d
            5. pr-e
            6. pr-f
            7. gm
            8. card
            9. exp
            \rВыберите банк патча: """))
        while (choice not in range(0, 10)):
            choice = int(input("неправильно: "))
        if choice == 0:
            bank = int(input("введите номер патча: "))
            while (bank not in range(1, 257)):
                bank = int(input("неправильно: "))
            result.append(create_message(JUNO_G_message0[1], 0x57))
            if bank in range(0, 129):
                result.append(create_message(JUNO_G_message0[2], 0))
            else:
                result.append(create_message(JUNO_G_message0[2], 1))
            result.append(create_message(JUNO_G_message0[3], (bank- 1) % 128))

        elif choice == 1:
            bank = int(input("введите номер патча: "))
            while (bank not in range(1, 129)):
                bank = int(input("неправильно: "))
            result.append(create_message(JUNO_G_message0[1], 0x57))
            result.append(create_message(JUNO_G_message0[2], 0x40))
            result.append(create_message(JUNO_G_message0[3], bank - 1))

        elif choice == 2:
            bank = int(input("введите номер патча: "))
            while (bank not in range(1, 129)):
                bank = int(input("неправильно: "))
            result.append(create_message(JUNO_G_message0[1], 0x57))
            result.append(create_message(JUNO_G_message0[2], 0x41))
            result.append(create_message(JUNO_G_message0[3], bank - 1))

        elif choice == 3:
            bank = int(input("введите номер патча: "))
            while (bank not in range(1, 129)):
                bank = int(input("неправильно: "))
            result.append(create_message(JUNO_G_message0[1], 0x57))
            result.append(create_message(JUNO_G_message0[2], 0x42))
            result.append(create_message(JUNO_G_message0[3], bank - 1))

        elif choice == 4:
            bank = int(input("введите номер патча: "))
            while (bank not in range(1, 129)):
                bank = int(input("неправильно: "))
            result.append(create_message(JUNO_G_message0[1], 0x57))
            result.append(create_message(JUNO_G_message0[2], 0x43))
            result.append(create_message(JUNO_G_message0[3], bank - 1))

        elif choice == 5:
            bank = int(input("введите номер патча: "))
            while (bank not in range(1, 129)):
                bank = int(input("неправильно: "))
            result.append(create_message(JUNO_G_message0[1], 0x57))
            result.append(create_message(JUNO_G_message0[2], 0x44))
            result.append(create_message(JUNO_G_message0[3], bank - 1))

        elif choice == 6:
            bank = int(input("введите номер патча: "))
            while (bank not in range(1, 129)):
                bank = int(input("неправильно: "))
            result.append(create_message(JUNO_G_message0[1], 0x57))
            result.append(create_message(JUNO_G_message0[2], 0x45))
            result.append(create_message(JUNO_G_message0[3], bank - 1))

        elif choice == 7:
            bank = int(input("введите номер патча: "))
            while (bank not in range(1, 257)):
                bank = int(input("неправильно: "))
            result.append(create_message(JUNO_G_message0[1], 0x79))
            result.append(create_message(JUNO_G_message0[2], 0x0))
            result.append(create_message(JUNO_G_message0[3], bank - 1))

        elif choice == 8:
            bank = int(input("введите номер патча: "))
            while (bank not in range(1, 257)):
                bank = int(input("неправильно: "))
            result.append(create_message(JUNO_G_message0[1], 0x57))
            if bank in range(0, 129):
                result.append(create_message(JUNO_G_message0[2], 0x20))
            else:
                result.append(create_message(JUNO_G_message0[2], 0x21))
            result.append(create_message(JUNO_G_message0[3], (bank - 1) % 128))

        elif choice == 9:
            srx = int(input("Введите номер платы SRX: "))
            bank = int(input("введите номер патча: "))
            result.append(create_message(JUNO_G_message0[1], 93))
            result.append(create_message(JUNO_G_message0[2], srx - 1))
            result.append(create_message(JUNO_G_message0[3], bank - 1))

    elif type == 1:
        choice = int(input("""
                    0. user
                    1. card
                    2. prst
                    \rВыберите банк патча: """))
        while (choice not in range(0, 3)):
            choice = int(input("неправильно: "))
        if choice == 0:
            bank = int(input("введите номер патча: "))
            while (bank not in range(1, 65)):
                bank = int(input("неправильно: "))
            result.append(create_message(JUNO_G_message1[1], 85))
            result.append(create_message(JUNO_G_message1[2], 0))
            result.append(create_message(JUNO_G_message1[3], bank-1))
        elif choice == 1:
            bank = int(input("введите номер патча: "))
            while (bank not in range(1, 65)):
                bank = int(input("неправильно: "))
            result.append(create_message(JUNO_G_message1[1], 85))
            result.append(create_message(JUNO_G_message1[2], 32))
            result.append(create_message(JUNO_G_message1[3], bank - 1))
        elif choice == 2:
            bank = int(input("введите номер патча: "))
            while (bank not in range(1, 65)):
                bank = int(input("неправильно: "))
            result.append(create_message(JUNO_G_message1[1], 85))
            result.append(create_message(JUNO_G_message1[2], 64))
            result.append(create_message(JUNO_G_message1[3], bank - 1))

    n = int(input("Введите окатавы (-3...0...3): "))
    while n not in range(-3, 4):
        n = int(input("Не правильно вводи еще: "))
    result.append(create_message(JUNO_G_message0[4], 64 + n))

    return result


def JUNOG_main():
    print("ИДЕТ НАСТРОЙКА JUNO_G")
    try:
        JUNO_G_header[2] = int(input("введите номер ID device для миди канала 5 (enter для ID по умолч. 20): ")) - 1
    except Exception:
        JUNO_G_header[2] = JUNO_G_DEFAULT_ID - 1
    type = int(input("Введите 0 - патч, 1 - перформанс: "))

    result_dump = create_full(type)
    return result_dump


if __name__ == "__main__":
    print_res(JUNOG_main())