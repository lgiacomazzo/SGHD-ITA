import re
from pathlib import Path

hard_coded_path_ita = Path("Temp/ITA")
hard_coded_path_eng = Path("Temp/ENG")

def main():
    all_files = hard_coded_path_ita.glob("*.txt")
    for path_file_ita in all_files:
        print(f"Controllo {path_file_ita}")
        path_file_eng = hard_coded_path_eng.joinpath(path_file_ita.name)
        suffixes_ita = []
        suffixes_eng = []
        with open(path_file_ita, 'r+', encoding="utf-8") as file:
            for original_line in file:
                # suffix = [%p] | [%e]
                # line_1 = [line, suffix, '']
                line_with_suffix = re.split("(\[%p\]$|\[%e\])$", original_line)
                suffix = line_with_suffix[1]
                suffixes_ita.append(suffix)
        with open(path_file_eng, 'r+', encoding="utf-8") as file:
            for original_line in file:
                # suffix = [%p] | [%e]
                # line_1 = [line, suffix, '']
                line_with_suffix = re.split("(\[%p\]$|\[%e\])$", original_line)
                suffix = line_with_suffix[1]
                suffixes_eng.append(suffix)
        for index, couple in enumerate(zip(suffixes_ita, suffixes_eng), 1):
            ita, eng = couple
            if ita != eng:
                print(index, ita, eng)

if __name__=="__main__":
    main()