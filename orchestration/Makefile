.DEFAULT_GOAL := deploy

init:
	pipenv install --three

install:
	pipenv install

clean:
	pipenv clean

update: clean
	pipenv update

test:
	pipenv run ansible all -m ping

deploy:
	pipenv run ansible-playbook site.yml