from django.test import TestCase
import pytest
from rest_framework.test import APIClient
from datetime import datetime, timedelta

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