# Dashboard de Salários na Área de Dados

Este projeto é um dashboard interativo desenvolvido com Python, Streamlit e Plotly para explorar e visualizar dados salariais da área de dados.

## Objetivo

O objetivo deste dashboard é permitir que usuários analisem salários, cargos, senioridade, tipo de contrato e modalidade de trabalho de forma visual e interativa, facilitando a compreensão de tendências e comparações.

## Funcionalidades

- Filtros interativos por:
  - ano
  - senioridade
  - tipo de contrato
  - tamanho da empresa
- Métricas principais, como:
  - salário médio
  - salário máximo
  - total de registros
  - cargo mais frequente
- Gráficos interativos com Plotly para visualizar:
  - top cargos por salário médio
  - distribuição de salários
  - proporção dos tipos de trabalho
  - salário médio por país para Cientistas de Dados
- Tabela detalhada com os dados filtrados

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- Plotly

## Estrutura do projeto

```text
Dashboard-Imersao-Alura/
├── .gitignore
├── app.py
├── dados-imersao-final.csv
├── requirements.txt
├── style.css
└── README.md
```

## Requisitos

Antes de rodar o projeto, certifique-se de ter instalado:

- Python 3.10 ou superior
- pip

## Como instalar

1. Clone o repositório:

```bash
git clone https://github.com/laertegomess/Dashboard-Imersao-Alura.git
cd Dashboard-Imersao-Alura
```

2. Crie um ambiente virtual e ative-o:

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

No diretório do projeto, execute:

```bash
python -m streamlit run app.py
```

A aplicação abrirá no navegador em:

```text
http://localhost:8501
```

Se a porta 8501 já estiver em uso, você pode usar:

```bash
python -m streamlit run app.py --server.port 8502
```

## Arquivos principais

- app.py: contém a lógica do dashboard, filtros, métricas e gráficos
- dados-imersao-final.csv: arquivo com os dados utilizados pela aplicação
- style.css: arquivo com estilos visuais do dashboard, incluindo o tema dark
- requirements.txt: dependências do projeto

## Observações

- O projeto usa um arquivo CSV local para facilitar execução em máquinas diferentes, sem depender de conexões externas.
- O dashboard funciona com um único ambiente virtual, mantido em .venv.
- O diretório `.venv` está listado em `.gitignore` e não deve ser enviado ao GitHub.
- Se quiser contribuir, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto é de uso livre para fins educacionais e de estudo.
