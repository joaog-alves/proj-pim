Clone este repositório : git clone https://github.com/joaog-alves/proj-pim.git  
Crie um ambiente de desenvolvimento : python -m venv venv;  
Vá para o ambiente : venv\Scripts\activate;  
Instale as dependências : pip install -r requirements.txt;  
Vá para o diretório onde está o código fonte: cd projectClinica;  
Crie a base de dados : python manage.py migrate  
Crie um super usuario: python manage.py createsuperuser  
Suba o servidor : python manage.py runserver
Acesse o site em 127.0.0.1:8000/
Utilize o gestor inicial para o primerio acessso: Usuario -> gestor_inicial, Senha -> senha_segura123
Acesse o admin com o superuser criado em: 127.0.0.1:8000/admin
