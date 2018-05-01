all: main.pdf

main.pdf: main.tex *.tex *.bib images/*
	pdflatex main
	bibtex main
	pdflatex main
	pdflatex main

# here starts edited content

.PHONY : clean

clean:
	rm main.aux  main.bbl  main.blg  main.lof  main.log  main.lot  main.out  main.pdf main.toc

svoc: svoc.tex *.tex *.bib images/*
	pdflatex svoc
	bibtex svoc
	pdflatex svoc
	pdflatex svoc
