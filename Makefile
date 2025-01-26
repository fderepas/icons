
default:
	@echo "Type 'make update'"
	@echo "to extract logos from" 
	@echo "    https://github.com/canonical/vanilla-framework.git"

update:
	rm -rf vanilla-framework
	git clone https://github.com/canonical/vanilla-framework.git
	python3 parse.py

clean:
	rm -rf *~ vanilla-framework
