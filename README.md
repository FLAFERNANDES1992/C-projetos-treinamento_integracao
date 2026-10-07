# BRVAL Hub de Treinamentos (HR Tech)

Aplicação Web interna desenvolvida para o **Departamento Pessoal e Recursos Humanos da BRVAL**. O sistema automatiza a auditoria contínua de elegibilidade para o **Treinamento de Integração**, garantindo conformidade com Normas Regulamentadoras (NR-1, NR-10) e eliminando controles manuais.

![BRVAL Logo](BRVAL%20logo.png)

---

## 🚀 Como Executar o Sistema

### 1. Inicialização Rápida em 1 Clique (Windows)
Basta clicar duas vezes no executável:
- `iniciar_sistema.bat` (ou executar `.\iniciar_sistema.ps1` no PowerShell)

### 2. Execução Manual via Terminal
Com o ambiente Python 3.10+ configurado:
```bash
streamlit run app.py
```
O aplicativo abrirá automaticamente em seu navegador em `http://localhost:8501`.

---

## ⚙️ Funcionalidades e Regras de Negócio (Framework LACE)

1. **Upload e Leitura Dinâmica:**
   - Compatível com a planilha oficial `Controle de Treinamento 03 anos.xlsx` (Excel e CSV).
   - Processamento estritamente em memória volátil (RAM), assegurando total privacidade e conformidade com a **LGPD**.

2. **Motor de Auditoria & Filtro de Desligados:**
   - Colaboradores com data de demissão preenchida (`df['Demissão'].notna()`) são automaticamente desconsiderados.
   - **Data Base:** Utiliza `1º Treinamento` se presente; caso nulo, utiliza `Admissão`.
   - **Cálculo de Tempo:** $(Data Atual - Data Base) / 365.25$.
   - **Matriz de Decisão:** `Precisa` (> 3 anos) e `Não Precisa` ($\le$ 3 anos).

3. **Simulador de Previsibilidade & Projeção Temporal:**
   - Permite projetar o cenário em **Hoje**, **+30 dias**, **+60 dias**, **+90 dias** ou data customizada.
   - Identifica colaboradores em **Atenção Preventiva** antes de estourarem o prazo legal.

4. **Classificação de Níveis de Urgência & Risco:**
   - **Crítico (> 5 anos):** Risco gravíssimo em auditoria fiscal.
   - **Alto (4 a 5 anos):** Prioridade imediata de inclusão em turmas.
   - **Moderado (3 a 4 anos):** Treinamento vencido requerendo agendamento regular.
   - **Atenção (Próx. 90 dias):** Vencimento próximo.
   - **Conforme Regular:** Treinamento em dia.

5. **Exportação Oficial em 2 Formatos:**
   - **Planilha Executiva Excel (.xlsx):** Estilizada com cores da BRVAL contendo 3 abas estruturadas (*Ação Imediata - Vencidos*, *Base Ativos Completa* e *Quadro Resumo Filiais*), filtros automáticos e larguras calculadas.
   - **Relatório CSV (UTF-8 com BOM):** Pronto para sistemas externos e Excel em português.

6. **Gerador de Convocação de Treinamentos (SESMT / Gestão):**
   - Emissão de **Memorando Circular em Lote** por filial.
   - Emissão de **Notificação Individual** por colaborador.
   - Download imediato em arquivo `.txt`.

7. **Auditoria de Qualidade Cadastral (Data Hygiene):**
   - Detecção automática de inconsistências (admissões futuras, treinamentos anteriores à admissão) para sanear o ERP antes do envio ao **eSocial (Evento S-2245)**.

---

## 🛡️ Matriz de Riscos Trabalhistas

- **eSocial (Evento S-2245):** Mitiga autuações na malha fina digital por ausência de envio dos treinamentos obrigatórios por colaborador.
- **Responsabilidade Civil Objetiva:** Previne caracterização de culpa *in omittendo* perante a Justiça do Trabalho em casos de acidentes.
- **Jornada de Trabalho:** Orienta que os treinamentos ocorram dentro da jornada normal para evitar passivos com Horas Extras e reflexos em DSR/FGTS/13º.

---

## 🧪 Testes Automatizados

Para executar a suíte completa de testes:
```bash
python test_audit.py
```
Cobertura:
- Teste de datas bissextas (29/02 com divisor 365.25).
- Simulação matemática da Seção 2.2.1 do SDD.
- Validação e resiliência contra arquivos corrompidos ou PDFs.
- Geração e integridade da planilha Excel oficial (.xlsx com 3 abas).
- Detecção de anomalias cadastrais (Data Hygiene).
- Geração de templates de convocação formal.
- Auditoria da planilha de produção da BRVAL.

---

## 📁 Estrutura do Projeto

```
treinamento_integracao/
├── .streamlit/
│   └── config.toml               # Configuração do Dark Theme corporativo BRVAL
├── app.py                         # Aplicação Web Streamlit (SaaS DP)
├── audit_engine.py                # Motor de regras, cálculo de datas, Excel e LGPD
├── test_audit.py                  # Suíte com 9 testes automatizados
├── iniciar_sistema.bat            # Inicializador em 1 clique (Batch Windows)
├── iniciar_sistema.ps1            # Inicializador em 1 clique (PowerShell)
├── Controle de Treinamento...xlsx # Planilha modelo oficial
├── BRVAL logo.png                 # Logotipo corporativo BRVAL
├── requirements.txt               # Dependências do projeto
├── README.md                      # Documentação de execução e negócio
└── software_design_document_sdd_brval.md # SDD original
```

