

cards = $(shell python3 -c "for n in range(1,48): print(f'cards/{n:02d}.svg')")
guideicons = $(wildcard guideicons/*.svg)
storyicons = $(wildcard storyicons/*/*.svg)


story-cards.pdf: story-cards.sla $(cards) $(guideicons) $(storyicons)
	scribus -ns -g -py scripts/to-pdf.py story-cards.sla


$(cards): template.svg
	mkdir -p cards
	scripts/cardgen.py


.PHONY: clean
clean:
	rm -f *.pdf
