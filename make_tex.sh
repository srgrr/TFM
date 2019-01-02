#!/bin/bash
cd tex
pdflatex main.tex
rm *.log
rm *.aux
rm *.toc
mv main.pdf ../tfm.pdf
cd ..
