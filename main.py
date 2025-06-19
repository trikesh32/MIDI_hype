from TR import TR_main
from JUNOg import JUNOG_main
from X3 import X3_main
from VK7 import VK7_main
from xp60 import XP60_main
from pathlib import Path
from pyperclip import copy

ids = {0: "junog", 1: "xp60", 2: "vk7", 3: "tr", 4: "x3"}
dump = {i: [] for i in range(len(ids))}
que = []
funcs = {0: JUNOG_main, 1: XP60_main, 2: VK7_main, 3: TR_main, 4: X3_main}
def print_res(result):
    res_text = ""
    f = open(f"{Path.home()}/Desktop/dump.txt", "w+")
    for res in result:
        for _ in res:
            res_text += "0" * (2 - (len(hex(_)) - 2)) + hex(_)[2:] + " "
        res_text+="\n"
    f.write(res_text)
    f.close()
    print(res_text, end="")


def print_dump():
    f = open(f"{Path.home()}/Desktop/dump.txt", "w+")
    res_text = ""
    for synt_id in que:
        for res in dump[synt_id]:
            for _ in res:
                res_text += "0" * (2 - (len(hex(_)) - 2)) + hex(_)[2:] + " "
            res_text += "\n"
    f.write(res_text)
    f.close()
    copy(res_text)
    print(res_text, end="")


def add_synt():
    print("0: junog, 1: xp60, 2: vk7, 3: tr, 4: x3")
    synt_id = int(input("Введите номер синтезатора: "))
    print()
    if synt_id not in que:
        que.append(synt_id)
    dump[synt_id] = funcs[synt_id]()
    print()


def change_order():
    global que
    print("Нынеший порядок: ")
    for i in que:
        print(f"{i}: {ids[i]}")
    print()
    que = list(map(int, list(input("Введите новый порядок (цифры без пробелов): "))))


def change_settings():
    for i in que:
        print(f"{i}: {ids[i]}", end=" ")
    print()
    synt_id = int(input("Введите id синтезатора: "))
    dump[synt_id] = funcs[synt_id]()


def main():
    while True:
        print(
            "0. печать существующего дампа\n1. добавить синтезатор\n2. изменить порядок вывода дампа\n3. изменить настройки синтезатора")
        mode = int(input("Ввод: "))

        if mode == 0:
            print_dump()
        elif mode == 1:
            add_synt()
        elif mode == 2:
            change_order()
        elif mode == 3:
            change_settings()
        else:
            print("Ошибка")


if __name__ == "__main__":
    main()