# Software Design Document (SDD)
## BRVAL Hub de Treinamentos (HR Tech)

![BRVAL Logo](BRVAL%20logo.png)

**Autor:** Arquiteto de RH e DP (Framework LACE)
**Data:** Outubro de 2026
**Público-Alvo:** Equipe de Departamento Pessoal, Analistas de RH e Engenharia de Dados.

---

## 1. LISTEN (Levantamento de Requisitos e Escopo)

### 1.1. Objetivo do Sistema
Desenvolver uma aplicação web interativa (*SaaS interno*) para o Departamento Pessoal da BRVAL. O sistema automatizará a auditoria de elegibilidade para o Treinamento de Integração, eliminando o controle manual e reduzindo o risco de autuações fiscais por não conformidade com Normas Regulamentadoras (NRs).

### 1.2. Requisitos Funcionais
*   **Upload Dinâmico:** O usuário deve poder fazer upload do arquivo `Controle de Treinamento 03 anos.xlsx`.
*   **Motor de Regras (Filtro):** O sistema deve ignorar colaboradores demitidos e calcular o tempo de casa/último treinamento.
*   **Filtro por Empresa:** Capacidade de selecionar e visualizar os dados segmentados pelas filiais da BRVAL.
*   **Exportação:** Geração de relatórios em formato CSV para acionamento das lideranças.

### 1.3. Requisitos Não Funcionais
*   **Interface:** Web (via navegador), *Dark Theme* corporativo respeitando a paleta da logo (Verde-água e Amarelo).
*   **Privacidade (LGPD):** Processamento em memória volátil (RAM). Sem persistência de dados sensíveis em banco de dados.

---

## 2. ASSESS (Avaliação Técnica, Matemática e de Risco)

### 2.1. Arquitetura de Software
*   **Linguagem:** Python 3.10+
*   **Frontend/Web Framework:** Streamlit (Agilidade na construção de dashboards em Python).
*   **Data Processing:** Pandas (Manipulação de DataFrames e cálculo de datas).

### 2.2. Matemática do DP e Regras de Negócio
A regra de negócio exige que o treinamento seja refeito a cada 3 anos. O sistema não confiará em colunas pré-calculadas no Excel, realizando o processamento no momento do upload para garantir precisão diária.

**Definição da Data Base:**
Se houver data na coluna "1º Treinamento", ela será a Data Base. Caso contrário, assume-se a "Admissão".

**Fórmula Matemática de Tempo:**
$$ Tempo = \frac{\text{Data Atual} - \text{Data Base}}{365.25} $$

**Matriz de Decisão Lógica:**
$$ \text{Status} = \begin{cases} \text{"Precisa"}, & \text{se } Tempo > 3 \\ \text{"Não Precisa"}, & \text{se } Tempo \le 3 \end{cases} $$

#### 2.2.1. Simulação Matemática
| Colaborador | Admissão | 1º Treinamento | Data Base Utilizada | Tempo Decorrido (Anos) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Func. A | 01/01/2020 | 01/01/2023 | 01/01/2023 | 3.7 | **Precisa** |
| Func. B | 15/05/2023 | Nulo | 15/05/2023 | 3.4 | **Precisa** |
| Func. C | 10/10/2024 | Nulo | 10/10/2024 | 2.0 | Não Precisa |

### 2.3. Matriz de Riscos Trabalhistas e Prevenção de Passivo
O sistema atua diretamente na mitigação dos seguintes riscos jurídicos:
*   **Risco eSocial (Evento S-2245):** A não realização da integração (quando atrelada a NRs como NR-1, NR-10) impede o envio de treinamentos ao eSocial. A malha fina cruza a data de admissão com os envios do evento S-2245. Multas são aplicadas por *cabeça*.
*   **Responsabilidade Civil Objetiva:** Em caso de acidente de trabalho, a falta de comprovação de treinamento de integração vigente inverte o ônus da prova e caracteriza culpa *in omittendo* da BRVAL.
*   **Atenção à Jornada (Natureza Salarial):** Os treinamentos detectados pelo sistema **devem** ser realizados dentro da jornada regular. Se realizados fora, configuram Horas Extras, gerando reflexos em DSR, Férias, 13º e FGTS.

---

## 3. CREATE (Especificação de Design e Código)

### 3.1. Design da Interface (UI)
*   **Sidebar (Esquerda):** Exibição da `BRVAL logo.png`. Área de upload contínuo (Drag and Drop). Textos de apoio sobre segurança de dados.
*   **Main Area (Centro):**
    *   Painel de Indicadores (Métricas: Ativos, Conformidade, Vencidos).
    *   Filtro Dropdown ("Selecionar Empresa").
    *   Data Table customizada (apenas os elegíveis).
    *   Botão *Call to Action* "Baixar Relatório (CSV)".

### 3.2. Fluxograma de Dados
1. `User` -> Faz Upload de `Controle de Treinamento 03 anos.xlsx`.
2. `App` -> Lê com `pd.read_excel`.
3. `App` -> Aplica filtro: `df['Demissão'].isna()`.
4. `App` -> Calcula diferença de datas usando `.dt.days / 365.25`.
5. `App` -> Filtra `Status == 'Precisa'`.
6. `User` -> Seleciona Empresa na UI.
7. `App` -> Renderiza tabela e disponibiliza `.csv` para download.

---

## 4. EVALUATE (Testes e Deploy)

### 4.1. Estratégia de Testes
*   **Teste de Estresse de Datas:** Inserir anos bissextos na planilha teste para garantir que o divisor `365.25` mantém a acurácia.
*   **Teste de Formato:** Inserir arquivos corrompidos ou PDFs para garantir que a aplicação retorne um erro amigável ao usuário de DP, e não o código de exceção (*stack trace*).

### 4.2. Estratégia de Deploy
*   **Fase 1 (Local):** Execução via terminal na máquina do analista de RH (`streamlit run app.py`).
*   **Fase 2 (Nuvem):** Hospedagem em provedores como Streamlit Community Cloud ou AWS EC2 (servidor interno BRVAL) para acesso via URL padronizada (ex: `rh.brval.com.br/treinamentos`).