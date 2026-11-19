# Enem em Perspectiva

**Projeto final · Avaliação G2 · Linguagens de Programação**

|  |  |
|---|---|
| **Autores** | Guilherme Oliveira de Moraes · André Luiz dos Santos Ferreira |
| **Curso** | Sistemas de Informação · 6º período |
| **Instituição** | Centro Universitário LaSalle do Rio de Janeiro |
| **Professor** | Alexandre Neves Louzada |

> G2 identifica a avaliação do projeto; não é o nome do grupo.

---

## Sobre o estudo

O projeto descreve a presença nas provas e as notas do Enem 2025 por dependência administrativa e localização da escola associada ao registro. A base original contém 4.810.772 registros. Destes, 1.739.028 tinham as classificações necessárias para as comparações. A análise é descritiva: diferenças observadas não demonstram que a rede ou a localização causou os resultados.

O artigo em HTML é o produto de comunicação do projeto e está preparado para o GitHub Pages. O repositório também contém o pipeline Python, um notebook de exploração, tabelas agregadas e um dicionário de dados.

## Estrutura

| Arquivo ou pasta | Conteúdo |
|---|---|
| `docs/index.html` | Artigo acadêmico responsivo, com gráficos e tabela interativa |
| `docs/assets/resumo_escola_area.csv` | Agregados carregados pelo artigo publicado |
| `src/etl.py` | Pipeline de leitura em blocos e agregação |
| `notebooks/analise_exploratoria.ipynb` | Exploração complementar das tabelas agregadas |
| `data/processed/` | Resultados agregados sem identificadores individuais |
| `data/data_dictionary.md` | Definição das variáveis e regras de cálculo |
| `requirements.txt` | Dependências Python com versões fixadas |

## Abrir o artigo no computador

Requer Python 3.11. Abra um terminal na pasta do projeto e rode:

```powershell
python -m http.server 8000 --directory docs
```

Acesse `http://localhost:8000` no navegador. Para encerrar o servidor, volte ao terminal e pressione `Ctrl+C`.

## Reproduzir a análise

1. Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

2. Baixe os [Microdados do Enem no portal do Inep](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem) e extraia `microdados_enem_2025/DADOS/RESULTADOS_2025.csv` do ZIP da edição 2025. O 7-Zip consegue extrair somente esse arquivo, que tem mais de 2 GB descompactado.

3. Rode o pipeline:

```powershell
python src/etl.py --input "C:/caminho/RESULTADOS_2025.csv" --output-dir data/processed
```

O script processa o CSV em blocos e atualiza tanto `data/processed/` quanto `docs/assets/`. A base bruta não deve ser enviada ao GitHub. O artigo e as tabelas agregadas já incluídos permitem conferir o estudo sem repetir essa etapa.


## Método em resumo

A unidade de análise é um registro de participante. Para cada prova objetiva, a taxa de presença é a proporção de registros com código de presença igual a 1 entre os que têm uma situação preenchida. As médias e os desvios-padrão usam notas válidas de participantes presentes; para redação, usam-se as notas válidas. Valores ausentes não são imputados. Registros sem dependência administrativa ou localização escolar válida ficam fora das comparações. Consulte `data/data_dictionary.md` para os detalhes.


## Link

https://guilhermemoraes-lasalle.github.io/enem-em-perspectiva/


## Licenças

O código está sob licença MIT. O texto original está sob CC BY 4.0. Os microdados permanecem sujeitos aos termos da fonte oficial do Inep e não são redistribuídos neste repositório.
