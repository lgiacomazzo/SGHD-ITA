import re
import sys
from pathlib import Path
import subprocess

default_editor = r"C:\Program Files\Notepad++\notepad++.exe"

def editor(filename, editor=None, text=None):
    editor = editor or default_editor

    try:
        path = Path(filename)
        if text is not None:
            path.write_text(text, encoding='utf-8')

        cmd = '{} {}'.format(editor, filename)
        
        subprocess.call(cmd)
        try:
            input("Ok. Modifica il file. Premi un tasto quando salvi il file e finisci")
        except Exception as e:
            print(e)
        return path.read_text(encoding='utf-8')
    except Exception as e:
        print(e)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("Nome script da controllare non presente")
        return
    filename = args[0]
    lines = []
    prefixes = []
    suffixes = []
    with open(filename, 'r+', encoding="utf-8") as file:
        for original_line in file:
            # suffix = [%p] | [%e]
            # line_1 = [line, suffix, '']
            line_with_suffix = re.split("(\[%p\]|\[%e\])$", original_line)
            line_1 = line_with_suffix[0]
        
            if len(line_with_suffix) == 1:
                # file che non sono script di testo, tipo _phone.scx.txt
                prefixes.append("")
                suffixes.append("")
                if "\n" in line_1:
                    lines.append(line_1)
                else:
                    lines.append(line_1+"\n")
                continue
            suffix = line_with_suffix[1]
            # line_2 = [line] or [lin]
            line_2 = re.split("^(\[name\].*\[line\])", line_1)
            if len(line_2) == 1:
                # forse [margin top="38"] o [margin top="76"]
                line_2 = re.split("^(\[margin top=.{4}\])", line_1)
                if len(line_2) == 1:
                    line_2 = ['', '', line_1]
            # line_2 = ['', '[name].*[line]', 'resto stringa'] or ['', '', line_1]
            prefix = line_2[1]
            line = line_2[2]
            prefixes.append(prefix)
            suffixes.append(suffix)
            lines.append(line+"\n")
    # adesso il file è letto (senza la riga vuota alla fine però. Aggiungerla dopo)
    with open("file_temporaneo.txt", "w", encoding="utf-8") as file:
        file.writelines(lines)
    modified_file = editor(filename="file_temporaneo.txt")
    new_lines_from_file = re.split("\n", modified_file)
    new_lines = []
    for prefix, line, suffix in zip(prefixes, new_lines_from_file, suffixes):
        new_line = re.sub("\s+$", "", line)
        new_line = prefix + new_line + suffix
        new_line = re.sub('(\[name\].*)"\.\[%p\]', '\g<1>."[%p]', new_line)
        new_line = new_line.replace('[line]"', '[line]“')
        new_line = new_line.replace('"[%p]', '”[%p]')
        new_line = new_line.replace('"[%e]', '”[%e]')
        new_line = new_line.replace("'", "’")
        new_line = new_line.replace("?.", "?")
        new_line = new_line.replace("!.", "!")
        new_line = new_line + '\n'
        new_lines.append(new_line)
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)
    print("Ricordare di controllare i nomi racchiusi in [name] e [line]")
    print("Ricordare di controllare se alcuni caratteri ’ devono essere cambiati in ‘")
    print("Ricordare di controllare i caratteri \", se cambiarli in “ e ” (solo nel testo, non nei tag tipo [color]) ")

if __name__=="__main__":
    main()