.PHONY: requirements requirements-upgrade freeze cloc clean create-pot
.PHONY: update-messages compile-messages tests

requirements:
	-@echo "### Installing requirements"
	-@pip install -r requirements.txt

requirements-upgrade:
	-@echo "### Upgrading requirements"
	-@pip freeze | cut -d = -f 1 | xargs pip install -U

freeze:
	-@echo "### Freezing python packages to requirements.txt"
	-@pip freeze > requirements.txt

cloc:
	-@echo "### Counting lines of code within the project"
	-@echo "# Total:" ; find . -iregex '.*\.py\|.*\.js\|.*\.html\|.*\.css' -type f -exec cat {} + | wc -l
	-@echo "# Python:" ; find . -name '*.py' -type f -exec cat {} + | wc -l
	-@echo "# JavaScript:" ; find . -name '*.js' -type f -exec cat {} + | wc -l
	-@echo "# HTML:" ; find . -name '*.html' -type f -exec cat {} + | wc -l
	-@echo "# CSS:" ; find . -name '*.css' -type f -exec cat {} + | wc -l

clean:
	-@echo "### Cleaning *.pyc and .DS_Store files "
	-@find . -name '*.pyc' -exec rm -f {} \;
	-@find . -name '.DS_Store' -exec rm -f {} \;

create-pot:
	-@echo "Creating pot and translation files."
	-@pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot . \
	--msgid-bugs-address="vladyslav.krylasov@gmail.com" \
	--copyright-holder="Vladyslav Krylasov <vladyslav.krylasov@gmail.com>" \
	--project="Bevbox" --version="1.0.0"
	-@pybabel init -i messages.pot -d translations -l uk
	-@pybabel init -i messages.pot -d translations -l ru

update-messages:
	-@echo "Updating translation files."
	-@pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot . \
	--msgid-bugs-address="vladyslav.krylasov@gmail.com" \
	--copyright-holder="Vladyslav Krylasov <vladyslav.krylasov@gmail.com>" \
	--project="Bevbox" --version="1.0.0"
	-@pybabel update -i messages.pot -d translations

compile-messages:
	-@echo "Compiling messages."
	-@pybabel compile -d translations

tests:
	-@echo "Running tests..."
	-@coverage run --source=app -m pytest app/tests.py -v && coverage report
