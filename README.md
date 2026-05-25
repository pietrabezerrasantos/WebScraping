# Twitter Web Scraping with Selenium 🕷️

Projeto desenvolvido em Python para coleta automatizada de tweets utilizando Selenium.

O sistema acessa perfis do Twitter/X, realiza rolagem automática da página, coleta informações dos tweets e exporta os dados para um arquivo CSV.

---

## Funcionalidades

- Coleta automática de tweets
- Scroll infinito da página
- Extração de:
  - texto do tweet
  - curtidas
  - retweets
  - respostas
  - visualizações
  - data da publicação
  - presença de mídia
- Exportação para CSV
- Tratamento de exceções
- Limitação da quantidade de tweets coletados

---

## Tecnologias utilizadas

- Python
- Selenium
- CSV
- WebDriver
- Automação Web

---

## Estrutura do projeto

```bash
📁 projeto
│
├── scraper.py
├── tweets.csv
└── chromedriver
```

---

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/SEUUSUARIO/twitter-web-scraping.git
```

### 2. Acesse a pasta

```bash
cd twitter-web-scraping
```

### 3. Instale as dependências

```bash
pip install selenium
```

### 4. Execute o projeto

```bash
python scraper.py
```

---

## Objetivo do projeto

O projeto foi desenvolvido com foco em automação web, manipulação de dados e prática de scraping utilizando Selenium.

Além da coleta automatizada de informações, o sistema também realiza tratamento de elementos dinâmicos e armazenamento estruturado dos dados extraídos.

---

## Autor

Pietra Santos
