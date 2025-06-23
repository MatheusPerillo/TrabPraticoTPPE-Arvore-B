# 🌳 Implementação de Árvore-B com Programação por Contratos (Python 3 + icontract)

Este projeto é a implementação da estrutura de dados **Árvore-B** em **Python 3**, seguindo os princípios de **orientação a objetos** e utilizando **programação por contratos** com a biblioteca [`icontract`](https://icontract.readthedocs.io/en/latest/).

Desenvolvido para a disciplina **FGA0242 - Técnicas de Programação para Plataformas Emergentes**, da **UnB - Universidade de Brasília**.

**Grupo:** Matheus Perillo e Sabrina Berno

---

## 📦 Requisitos

- Python 3
- Recomendado: ambiente virtual (`venv`)

---

## 🔧 Instalação

### 1. Clone o repositório (ou crie os arquivos localmente)

```bash
git clone https://github.com/MatheusPerillo/TrabPraticoTPPE-Arvore-B.git
cd TrabPraticoTPPE-Arvore-B
```

### 2. Crie e ative um ambiente virtual

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## ▶️ Como rodar o projeto

### 1. Rodar o projeto com a árvore apresentada na descrição do projeto

```bash
python main.py
```

### 2. Rodar o projeto com a árvore que testa inserção, busca e remoção de maneira automática

```bash
python main_auto.py
```

## 🧪 Como rodar os testes automatizados com `pytest`

### 1. Rodar todos os testes

```bash
pytest -v tests/
```

### 2. Gerar relatório de cobertura

```bash
pytest --cov=arvore_b tests/
```
