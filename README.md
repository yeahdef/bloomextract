# bloomextract
A simple http://turntablelab.com category / product page parser

I assume you have virtualenv...

Get up and running by doing this:

	git clone https://github.com/yeahdef/bloomextract.git
	virtualenv env
	source env/bin/activate
	cd bloomextract
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py runserver & sensible-browser http://localhost:8000

Input a product or category page URL into the form from http://turntablelab.com.

I haven't done a large volume of testing, but this appears to work for most physical goods.