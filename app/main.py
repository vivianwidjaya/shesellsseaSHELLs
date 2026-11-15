import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Builtins:
    _input: list[str]

    def command(self) -> None:
        match self._input[0]:
            case "echo":
                self._echo()
            case "type":
                self._type()
            case "exit":
                self._exit()
            case "pwd":
                self._pwd()
            case "cd":
                self._cd()
            case _:
                self._executable()

    def _cd(self) -> None:
        if len(self._input) >= 2:
            if self._input[1] == "~":
                os.chdir(Path.home())
            elif len(self._input) == 2:
                path_inp = Path(self._input[1])
                if path_inp.exists() == True:
                    os.chdir(path_inp)
                else:
                    print(
                        f"cd: {' '.join(self._clean_input())}: No such file or directory"
                    )
            else:
                print("cd: too many arguments")
        else:
            os.chdir(Path.home())

    def _getpath(self) -> list[str]:
        path = os.getenv("PATH", "")
        path_lst = path.split(os.pathsep)
        return path_lst

    def _executable(self) -> None:
        path_lst = self._getpath()
        for dir in path_lst:
            search_dir = dir + "/" + self._input[0]
            if os.access(search_dir, os.X_OK) == True:
                subprocess.run(self._input, check=False)
                return
        print(f"{self._input[0]}: command not found")

    def _pwd(self) -> None:
        cur_dir = Path.cwd()
        print(cur_dir)

    def _exit(self) -> None:
        sys.exit(0)

    def _clean_input(self) -> list[str]:
        return self._input[1:]

    def _check_redirect(self) -> bool:
        return bool(">" in self._input[2:] and ">" != self._input[-1])

    def _echo(self) -> None:
        result = " ".join(self._clean_input())
        if not self._check_redirect():
            print(result)
        else:
            Path(self._input[-1]).write_text((result.split(">")[0]) + "\n")

    def _type(self) -> None:
        cleaned_input = self._clean_input()
        if cleaned_input == []:
            return
        for word in cleaned_input:
            if word in ["echo", "exit", "type"]:
                print(f"{word} is a shell builtin")
                return
            else:
                path_lst = self._getpath()
                for dir in path_lst:
                    search_dir = dir + "/" + word
                    if os.access(search_dir, os.X_OK) == True:
                        print(f"{word} is {search_dir}")
                        return
            print(f"{word}: not found")


def main():
    while True:
        sys.stdout.write("$ ")

        input_init = input()
        input_str = shlex.split(input_init)

        output = Builtins(input_str)
        output.command()


if __name__ == "__main__":
    main()
