#!/usr/bin/python3

"""
Skript kontroluje / testuje zadání z TGR
"""

import sys, os, zipfile, shutil, json, subprocess
from enum import Enum


class ExitCodes(Enum):
    WRONG_FORMAT = 1
    FILE_NOT_FOUND = 2
    NO_ARGUMENTS = 3
    NOT_A_ZIPFILE = 4


def print_help():
    print("""
            Skript pro ověřování / testování projektů do TGR
            ./test.py soubor.zip [testy]
          """)


def test_directory_format():
    files = os.listdir("./projekt")
    required_files = ['report.pdf', 'src', 'Makefile']
    allowed_files = ['report.pdf', 'src', 'Makefile', 'lib']
    for file in required_files:
        if file not in files:
            shutil.rmtree("./projekt")
            print("Neplatná struktůra! Požadovaný soubor %s nenalezen" % file, file=sys.stderr)
            sys.exit(ExitCodes.WRONG_FORMAT.value)

    for file in files:
        if file not in allowed_files:
            shutil.rmtree("./projekt")
            print("Neplatná struktůra! V kořenovém adresáři jsem nalezl soubor %s, který není ve specifikaci" % file, file=sys.stderr)
            sys.exit(ExitCodes.WRONG_FORMAT.value)


def test_file(name):
    try:
        with zipfile.ZipFile(name, 'r') as file:
            file.extractall("projekt")

    except zipfile.BadZipfile:
        print("Soubor %s není zip!" % name, file=sys.stderr)
        sys.exit(ExitCodes.FILE_NOT_FOUND.value)

    except FileNotFoundError:
        print("Soubor %s nelze najít!" % name, file=sys.stderr)
        sys.exit(ExitCodes.NOT_A_ZIPFILE.value)

    test_directory_format()


def do_test(case, name):
    print("Spouštím test: %s" % case['jmeno'])
    try:
        print("\t%s" % case['popis'])
    except KeyError:
        pass

    try:
        completed_process = subprocess.run([ "./projekt/" + case['spustitelny_soubor']], stdout=subprocess.PIPE)
        if case['selhani'] == "ano":
            if completed_process.returncode == 0:
                print("\tOčekával jsem selhání ale program prošel", file=sys.stderr)
                return
        else:
            if completed_process.stdout.decode('ascii') != case['stdout']:
                print("\tStdout v tomto případě nesedí \n %s \n %s" % (completed_process.stdout, case['stdout']), file=sys.stderr)
                return

        print("\tTest proběhl ok")

    except subprocess.CalledProcessError:
        print("\tNelze zavolat %s! Je spustitelný?" % case['spustitelny_soubor'])

    except FileNotFoundError:
        print("\tNelze zavolat %s! Soubor nebyl nalezen. Je možné, že ho nevytváří Makefile." % case['spustitelny_soubor'])


def test_executable(name):
    with open(name, "r") as file:
        json_data = file.read()
        try:
            json_data = json.loads(json_data)
            do_test(json_data, name)

        except json.JSONDecodeError:
            print("Soubor %s neobsahuje validní json přeskakuji ho!" % name)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Neplatný počet argumentů", file=sys.stderr)
        print_help()
        sys.exit(ExitCodes.NO_ARGUMENTS.value)

    test_file(sys.argv[1])
    test_names = sys.argv[2:]

    subprocess.run(['make', '-C', './projekt'], check = True)
    for test in test_names:
        print("Provádím testy pro %s" % test)
        test_executable("./" + test)

    shutil.rmtree("./projekt")
