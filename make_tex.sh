#!/bin/bash
cd tex
latexmk --shell-escape main.tex -pdf
mv main.pdf ../tfm.pdf
cd ..
