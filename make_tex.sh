#!/bin/bash
cd tex
latexmk main.tex -pdf
mv main.pdf ../tfm.pdf
cd ..
