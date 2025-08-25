# Contribuidores
[João Marcos Avancini](https://github.com/J0-M)  
[Letícia Cristina da Silva](https://github.com/leticia-csilva)  
[Raquel Real Haagsma](https://github.com/rhaagsma)  

# AdrenaLife

## Sobre o Projeto

Este projeto simula um site de cadastro de eventos, onde cada evento possui uma atividade e cada atividade pertence a uma categoria.
O sistema possui backend em Django e frontend em React, seguindo boas práticas de arquitetura de software e design patterns.

## Tecnologias Utilizadas
- Backend: Django, Django REST Framework, Pytest
- Frontend: React, Axios
- Banco de Dados: SQLite (padrão Django)

## Estrutura do Projeto
<pre markdown="1">
ProjetoES2024-AdrenaLife/
│── adrenalife/              # Configurações principais do Django
│── app_adrenalife/          # Aplicação Django (models, views, services, tests)
│   ├── migrations/          # Migrações do banco de dados
│   ├── tests.py             # Testes automatizados com Pytest
│   ├── models.py            # Modelos de Categoria, Atividade e Evento
│   ├── views.py             # Views da API
│   ├── services/            # Implementação do padrão Facade
│   └── serializers.py       # Serializadores Django REST Framework
│
│── frontend/                # Aplicação React (interface web)
│   ├── public/
│   └── src/
│       ├── components/      # Componentes React reutilizáveis
│       ├── pages/           # Páginas do sistema
│       ├── services/        # Integração com a API
│       └── App.js           # Componente principal
│
│── manage.py                # Comando principal Django
│── requirements.txt         # Dependências do backend
│── package.json             # Dependências do frontend
</pre>

# Facade

Link da documentação: https://refactoring.guru/pt-br/design-patterns/facade

Este padrão é responsável por simplificar a interaface de um objeto, fragmentando suas responsabilidades em outras classes. No caso deste projeto, funções de rotas de api foram simplificadas em funções separadas para facilitar o entendimento e manter fluidez no código, bem como segmentá-lo para mais fácil manutenção.

``` python
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([AllowAny])
def categoriaManager(request):
    
    if request.method == 'GET':
        return (CategoriaAtividadeService.get_categoria(request))
    
    if request.method == 'POST':
        return(CategoriaAtividadeService.create_categoria(request))
    
    if request.method == 'PUT':
        return(CategoriaAtividadeService.update_categoria(request))
    
    if request.method == 'DELETE':
        return(CategoriaAtividadeService.delete_categoria(request))
        
```

``` python
class CategoriaAtividadeService:
    @staticmethod
    def create_categoria(request):
        newCategoria = request.data
        name = newCategoria.get("nome", None)
        
        categoriaTest = categoria_atividade.objects.filter(nome=name)
        
        if categoriaTest.exists():
            return Response({"Nome já cadastrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = categoriaAtividadeSerializer(data=newCategoria)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def get_categoria(request):
        
        categoriaName = request.GET.get('nome', None)
        categoriaId = request.GET.get('id', None)

        if categoriaName:
            try:
                categoria = categoria_atividade.objects.get(nome=categoriaName)
                serializer = categoriaAtividadeSerializer(categoria)
                return Response(serializer.data)
            except categoria_atividade.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif categoriaId:
            try:
                categoria = categoria_atividade.objects.get(id=categoriaId)
                serializer = categoriaAtividadeSerializer(categoria)
                return Response(serializer.data)
            except categoria_atividade.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:    
            categorias = categoria_atividade.objects.all()
            serializer = categoriaAtividadeSerializer(categorias, many=True)
            return Response(serializer.data)
        
    @staticmethod
    def update_categoria(request):
        data = request.data
        name = request.GET.get('nome', None)
        
        if not name:
            return Response({"Nome não informado"}, status=status.HTTP_400_BAD_REQUEST)
        
        nameTest = data.get("nome", None)
        categoriaTest = categoria_atividade.objects.filter(nome=nameTest)
        
        if categoriaTest.exists():
            return Response({"Nome já cadastrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            updatedcategoria = categoria_atividade.objects.get(nome=name)
        
        except:
            return Response({"Categoria não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = categoriaAtividadeSerializer(updatedcategoria, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def delete_categoria(request):
        name = request.GET.get('nome', None)
        
        if not name:
            return Response({"Nome não informado"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            categoria = categoria_atividade.objects.get(nome=name)
            
            categoria.delete()
            return Response(status=status.HTTP_200_OK)
        
        except:
            return Response({"Categoria não encontrada"}, status=status.HTTP_404_NOT_FOUND)

```

# Testes

Os testes deste projeto foram feitos a partir da ferramente Pytest, uma ferramente de testes automatizados de Python para testar funções e comparar suas sáidas.
O teste possui uma saída esperada, caso essa saída seja a mesma retornada pela função, o teste será um sucesso.
Os testes implementados foram feitos para testar a criação de uma categoria e uma atividade:
``` python
@pytest.mark.django_db
def test_create_and_get_categoria():
    client = APIClient()
    
    categoria_data = {"nome": "Infantil"}
    response = client.post("/apiCategorias/categorias/", categoria_data, format="json")
    assert response.status_code == 201 

    response = client.get("/apiCategorias/categorias/?nome=Infantil")
    assert response.status_code == 200  # Encontrado
    assert response.json()["nome"] == "Infantil"


@pytest.mark.django_db
def test_create_and_get_atividade():
    client = APIClient()

    # Criando categoria
    categoria_data = {"nome": "Infantil"}
    response = client.post("/apiCategorias/categorias/", categoria_data, format="json")
    assert response.status_code == 201
    
    # Criando atividade
    response = client.get("/apiCategorias/categorias/?nome=Infantil")
    assert response.status_code == 200  # Encontrado
    categoria_id = response.json()["id"]
    
    atividade_data = {
        "nome": "Corrida Matinal",
        "descricao": "Treino de corrida de 5km",
        "categoria": categoria_id
    }
    atividade_response = client.post("/apiAtividades/atividades/", atividade_data, format="json")
    assert atividade_response.status_code == 201

    response = client.get("/apiAtividades/atividades/")
    assert response.status_code == 200

    atividade_encontrada = None
    for atividade in response.json():
        if atividade.get("nome") == "Corrida Matinal":
            atividade_encontrada = atividade
            break
    
    assert atividade_encontrada is not None
    assert atividade_encontrada.get("nome") == "Corrida Matinal"
    assert atividade_encontrada.get("descricao") == "Treino de corrida de 5km"
```
Para rodar os testes, é necessário:
# 1 - Instalar o pytest
```
pip install pytest pytest-django
```

# 2 - Acessar a pasta correta de tests.py (Arquivo onde está programado os testes)
```
cd adrenalife
cd app_adrenalife
```

# 3 - Rodar o pytest
```
pytest tests.py
```
