#!/usr/bin/python
"""
MIT License

Copyright (c) 2020 Marek Gaik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import os
import argparse


def makePro(target_dir):
    HEADER = "TEMPLATE = app\n" \
             "CONFIG += console\n" \
             "CONFIG -= app_bundle\n" \
             "CONFIG -= qt\n" \
             "CONFIG += c++11\n" \
             "CONFIG += stl\n"

    INC = "INCLUDEPATH += \\ \n"
    SRC = "SOURCES += \\ \n"
    HEADERS = "HEADERS += \\ \n"

    for root, dirs, files in os.walk(target_dir):
        def add_esc(text):
            return text + " \\ \n"

        rel_dir = os.path.relpath(root, target_dir)
        INC += add_esc(rel_dir)
        for file in files:
            if file.endswith((".h", ".hpp", ".hxx")):
                HEADERS += add_esc(os.path.join(rel_dir, file))
            elif file.endswith((".c", ".cpp", ".cxx")):
                SRC += add_esc(os.path.join(rel_dir, file))

    return HEADER + "\n" + INC + "\n" + SRC + "\n" + HEADERS + "\n"


def main():
    parser = argparse.ArgumentParser(description="The very simple Qt .pro file generator")
    parser.add_argument("--dir",
                        help="the root dir for where the project will be scanned and created",
                        required=True)
    parser.add_argument("--name",
                        help="the target file name e.g. project.pro",
                        required=True)
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        sys.exit("--dir must point to the existing directory")

    pro = makePro(args.dir)
    print(pro)

    with (open(os.path.join(args.dir, args.name), "w")) as f:
        f.write(pro)


if __name__ == "__main__":
    main()
