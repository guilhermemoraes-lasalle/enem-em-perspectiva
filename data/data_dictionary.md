# Dicionário de dados do projeto

Fonte: `RESULTADOS_2025.csv`, microdados do Enem 2025 (Inep). O arquivo original é delimitado por ponto e vírgula e codificado em Latin-1. A unidade de observação é um registro de participante na base de resultados. O projeto não publica identificadores nem dados individuais.

| Campo | Tipo | Significado neste estudo | Tratamento |
|---|---|---|---|
| `TP_DEPENDENCIA_ADM_ESC` | inteiro categórico | Dependência administrativa da escola vinculada ao registro: 1 Federal, 2 Estadual, 3 Municipal, 4 Privada | Mantido apenas quando preenchido e igual a uma categoria prevista |
| `TP_LOCALIZACAO_ESC` | inteiro categórico | Localização da escola: 1 Urbana, 2 Rural | Mantido apenas quando preenchido e igual a uma categoria prevista |
| `TP_PRESENCA_CN` | inteiro categórico | Situação de presença na prova de Ciências da Natureza | Denominador: valores não nulos; presente: código 1 |
| `TP_PRESENCA_CH` | inteiro categórico | Situação de presença na prova de Ciências Humanas | Denominador: valores não nulos; presente: código 1 |
| `TP_PRESENCA_LC` | inteiro categórico | Situação de presença na prova de Linguagens e Códigos | Denominador: valores não nulos; presente: código 1 |
| `TP_PRESENCA_MT` | inteiro categórico | Situação de presença na prova de Matemática | Denominador: valores não nulos; presente: código 1 |
| `NU_NOTA_CN` | decimal | Nota de Ciências da Natureza | Média calculada entre registros presentes, com nota válida |
| `NU_NOTA_CH` | decimal | Nota de Ciências Humanas | Média calculada entre registros presentes, com nota válida |
| `NU_NOTA_LC` | decimal | Nota de Linguagens e Códigos | Média calculada entre registros presentes, com nota válida |
| `NU_NOTA_MT` | decimal | Nota de Matemática | Média calculada entre registros presentes, com nota válida |
| `NU_NOTA_REDACAO` | decimal | Nota da redação | Média calculada entre notas válidas; sem filtro de presença objetiva |
| `dependencia_administrativa` | texto categórico | Rótulo legível da dependência escolar | Derivado no pipeline |
| `localizacao` | texto categórico | Rótulo legível da localização escolar | Derivado no pipeline |
| `taxa_presenca_pct` | decimal | Percentual de registros presentes entre os que têm situação de presença válida para a prova | Calculado por área; não representa toda inscrição sem escola classificada |
| `media` | decimal | Média aritmética da nota válida no grupo e área | Calculada somente entre presentes nas provas objetivas |
| `desvio_padrao` | decimal | Desvio-padrão populacional das notas válidas do grupo e área | Derivado de soma e soma dos quadrados em blocos |
| `n_registros_com_escola_classificada` | inteiro | Quantidade de registros associados ao par dependência-localização | Contagem após excluir categorias escolares ausentes ou inválidas |
| `n_presenca_valida` | inteiro | Registros com valor não nulo de presença para a área | Disponível para as quatro provas objetivas |
| `n_presentes` | inteiro | Registros com código 1 de presença | Disponível para as quatro provas objetivas |
| `n_notas_validas` | inteiro | Quantidade de notas incluídas no cálculo da média | Nota numérica não nula; para provas objetivas, também presença igual a 1 |

**Limite de escopo:** registros sem escola classificada ficam fora da comparação por rede/localização. A análise descreve associações observadas e não controla diferenças socioeconômicas, seletividade ou outros fatores.

