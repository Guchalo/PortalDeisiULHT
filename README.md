# cvp
https://cvp.pythonanywhere.com/
admin, admin

## Recuperação da password
[Video demo](https://github.com/DEISI-apps/cvp/blob/main/demo_autenticacao.mp4) 

## Autenticação dual, email || username && password

para permitir autenticação tanto com email como username:
* criar ficheiro backends.py no projeto
* adicionar:

```Python
AUTHENTICATION_BACKENDS = [
    'projeto.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

* no login, testar as duas possibilidades. Deveria ser possivel com 
`authenticate(user, credentials=credentials, password=password)`,
onde credentials pode ser username ou email. Mas não consegui por a fucnionar.
O que está implementado testa as duas possibilidades.
