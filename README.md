# bloomextract
a simple amazon category / product page parser

I assume you have virtualenv...
Get up and running by doing this:

	git clone https://github.com/yeahdef/bloomextract.git
	virtualenv env
	source env/bin/activate
	cd bloomextract
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py runserver

navigate to localhost in your browser.
input a product or category page URL into the form.