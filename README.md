# TestVenko_Trainee

## Passo a passo para testar a implementação

### Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.9 instalado
- Pip instalado

### Passo 1: Clonar o repositório

Clone o repositório para sua máquina local:

```sh
git clone <URL_DO_REPOSITORIO>
cd TestVenko_Trainee
```

### Passo 2: Construir e iniciar os containers

Execute o Docker Compose para construir e iniciar os containers:

```sh
docker-compose up --build -d
```

### Passo 3: Verificar os logs

Verifique os logs para garantir que todos os serviços foram iniciados corretamente:

```sh
docker-compose logs -f
```

### Passo 4: Acessar a aplicação

Abra seu navegador e acesse a aplicação web no endereço [link](http://localhost:80).
