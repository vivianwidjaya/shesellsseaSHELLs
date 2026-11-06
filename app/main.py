import os
import subprocess
import sys
from dataclasses import dataclass


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
            case _:
                self._executable()

    def _executable(self) -> None:
        path = os.getenv("PATH", "")
        path_lst = path.split(os.pathsep)
        for dir in path_lst:
            search_dir = dir + "/" + self._input[0]
            if os.access(search_dir, os.X_OK) == True:
                subprocess.run(self._input, check=False)
                return
        print(f"{self._input[0]}: command not found")

    def _exit(self) -> None:
        sys.exit(0)

    def _clean_input(self) -> list[str]:
        return self._input[1:]

    def _echo(self) -> None:
        print(" ".join(self._clean_input()))

    def _type(self) -> None:
        cleaned_input = self._clean_input()
        if cleaned_input == []:
            return
        for word in cleaned_input:
            if word in ["echo", "exit", "type"]:
                print(f"{word} is a shell builtin")
                return
            else:
                path = os.getenv("PATH", "")
                path_lst = path.split(os.pathsep)
                for dir in path_lst:
                    search_dir = dir + "/" + word
                    if os.access(search_dir, os.X_OK) == True:
                        print(f"{word} is {search_dir}")
                        return
            print(f"{word}: not found")


def main():
    while True:
        sys.stdout.write("$ ")

        input_str = input().split()

        output = Builtins(input_str)
        output.command()


if __name__ == "__main__":
    main()
