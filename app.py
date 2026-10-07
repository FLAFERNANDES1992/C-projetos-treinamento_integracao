"""
BRVAL Hub de Treinamentos (HR Tech) - Aplicação Principal
Framework LACE - Arquiteto de RH e DP
Auditoria de elegibilidade para o Treinamento de Integração (Ciclo de 3 Anos)
"""

import os
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd

from audit_engine import (
    process_training_data,
    read_training_file,
    generate_export_csv,
    generate_export_excel,
    check_data_quality,
    generate_convocation_email,
    generate_batch_convocation,
    AuditException,
    InvalidFileFormatError,
    MissingColumnsError
)

# ---------------------------------------------------------
# Configuração da Página
# ---------------------------------------------------------
st.set_page_config(
    page_title="BRVAL Hub de Treinamentos | DP & RH",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Estilização CSS Corporativa (Dark Theme: Verde-água & Amarelo)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Fontes e fundo geral */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Cores de Identidade BRVAL */
    :root {
        --brval-teal: #57A695;
        --brval-teal-light: #73C2B1;
        --brval-teal-dark: #3D786B;
        --brval-yellow: #FFCC29;
        --brval-yellow-light: #FFDC6B;
        --brval-dark-bg: #0B0F17;
        --brval-card-bg: #151C28;
        --brval-card-border: #222C3D;
        --brval-text-muted: #94A3B8;
        --brval-danger: #F87171;
    }

    /* Header e Título */
    .brval-header-container {
        padding: 1.2rem 1.6rem;
        background: linear-gradient(135deg, rgba(87, 166, 149, 0.12) 0%, rgba(255, 204, 41, 0.08) 100%);
        border: 1px solid var(--brval-card-border);
        border-radius: 12px;
        margin-bottom: 1.2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .brval-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .brval-subtitle {
        font-size: 0.95rem;
        color: var(--brval-text-muted);
        margin-top: 4px;
        margin-bottom: 0;
    }

    .brval-badge-saas {
        background-color: rgba(87, 166, 149, 0.2);
        color: var(--brval-teal-light);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid var(--brval-teal);
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* Cards de Métricas */
    .metric-card {
        background: var(--brval-card-bg);
        border: 1px solid var(--brval-card-border);
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
    }
    .metric-card:hover {
        border-color: var(--brval-teal);
        transform: translateY(-2px);
    }
    
    .metric-title {
        font-size: 0.80rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--brval-text-muted);
        font-weight: 600;
        margin-bottom: 0.35rem;
    }
    
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.1;
    }
    
    .metric-footer {
        font-size: 0.78rem;
        margin-top: 0.35rem;
    }
    
    .text-teal { color: var(--brval-teal-light) !important; font-weight: 600; }
    .text-yellow { color: var(--brval-yellow) !important; font-weight: 600; }
    .text-danger { color: var(--brval-danger) !important; font-weight: 600; }
    .text-muted { color: var(--brval-text-muted) !important; }

    /* Projeção Banner */
    .projection-banner {
        background: linear-gradient(90deg, rgba(87, 166, 149, 0.15) 0%, rgba(255, 204, 41, 0.12) 100%);
        border: 1px solid rgba(255, 204, 41, 0.4);
        border-radius: 8px;
        padding: 0.7rem 1.2rem;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        color: #F1F5F9;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Sidebar Customizada */
    .sidebar-security-badge {
        background: rgba(87, 166, 149, 0.08);
        border: 1px solid rgba(87, 166, 149, 0.25);
        border-radius: 8px;
        padding: 0.8rem;
        font-size: 0.8rem;
        color: #CBD5E1;
        margin-top: 1.2rem;
    }

    /* Risk Callouts */
    .risk-card {
        background: #131A26;
        border-left: 4px solid var(--brval-yellow);
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 1rem;
        height: 100%;
    }
    
    .risk-card-teal {
        background: #131A26;
        border-left: 4px solid var(--brval-teal);
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    /* Botão de Download */
    div.stDownloadButton > button {
        background: linear-gradient(90deg, #57A695 0%, #3D786B 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem !important;
        box-shadow: 0 4px 14px rgba(87, 166, 149, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    div.stDownloadButton > button:hover {
        background: linear-gradient(90deg, #6ABAA8 0%, #4D8B7D 100%) !important;
        box-shadow: 0 6px 20px rgba(87, 166, 149, 0.5) !important;
        transform: translateY(-1px) !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Sidebar: Logo, Upload & Simulador de Previsibilidade
# ---------------------------------------------------------
with st.sidebar:
    logo_path = "BRVAL logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("<h2 style='color:#57A695; text-align:center;'>BRVAL</h2>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.85rem; margin-top: -8px;'>Hub de Treinamentos (HR Tech)</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 📂 Upload de Planilha")
    st.markdown(
        "<span style='font-size: 0.85rem; color: #94A3B8;'>"
        "Faça upload do arquivo <code>Controle de Treinamento 03 anos.xlsx</code>:"
        "</span>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Arraste ou selecione a planilha",
        type=["xlsx", "xls", "csv"],
        help="Planilha contendo as colunas: Empresa, Nome do Colaborador, Admissão, Demissão, 1º Treinamento."
    )

    default_excel_file = "Controle de Treinamento 03 anos.xlsx"
    use_default_button = False
    if os.path.exists(default_excel_file):
        st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)
        if st.button("📁 Carregar Arquivo de Demonstração", help="Carrega o arquivo Controle de Treinamento 03 anos.xlsx"):
            use_default_button = True

    st.markdown("---")
    st.markdown("### 🔮 Simulador Preventivo")
    st.markdown(
        "<span style='font-size: 0.82rem; color: #94A3B8;'>"
        "Projete vencimentos futuros para planejar turmas com antecedência:"
        "</span>",
        unsafe_allow_html=True
    )

    projecao_opcao = st.radio(
        "Data de Corte da Auditoria:",
        options=[
            "Data Atual (Hoje)",
            "Próximos 30 dias (+30d)",
            "Próximos 60 dias (+60d)",
            "Próximos 90 dias (+90d)",
            "Data Personalizada"
        ],
        index=0
    )

    data_referencia_calculo = datetime.now()
    if projecao_opcao == "Próximos 30 dias (+30d)":
        data_referencia_calculo = datetime.now() + timedelta(days=30)
    elif projecao_opcao == "Próximos 60 dias (+60d)":
        data_referencia_calculo = datetime.now() + timedelta(days=60)
    elif projecao_opcao == "Próximos 90 dias (+90d)":
        data_referencia_calculo = datetime.now() + timedelta(days=90)
    elif projecao_opcao == "Data Personalizada":
        custom_date = st.date_input("Escolha a data de referência:", value=datetime.now())
        data_referencia_calculo = datetime.combine(custom_date, datetime.min.time())

    # Segurança e LGPD
    st.markdown("""
    <div class="sidebar-security-badge">
        <strong>🔒 Privacidade e LGPD Garantidas</strong><br>
        • Processamento 100% volátil em memória (RAM).<br>
        • Sem banco de dados nem retenção de dados pessoais.<br>
        • Eliminação imediata após o término da sessão.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<div style='font-size: 0.75rem; color: #64748B; text-align: center;'>"
        "Framework LACE • Departamento Pessoal BRVAL<br>"
        "Versão 3.0 Enterprise • Outubro de 2026"
        "</div>",
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# Cabeçalho Principal (Main Area)
# ---------------------------------------------------------
st.markdown("""
<div class="brval-header-container">
    <div>
        <h1 class="brval-title">BRVAL Hub de Treinamentos</h1>
        <p class="brval-subtitle">Auditoria Preventiva de Elegibilidade • Treinamento de Integração (Ciclo de 3 Anos)</p>
    </div>
    <div>
        <span class="brval-badge-saas">SaaS Interno DP</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Obtenção dos Dados
# ---------------------------------------------------------
df_raw = None
source_name = None

if uploaded_file is not None:
    source_name = uploaded_file.name
    try:
        df_raw = read_training_file(uploaded_file)
    except InvalidFileFormatError as iffe:
        st.error(f"⚠️ **Erro no arquivo enviado:** {str(iffe)}")
        st.stop()
    except Exception as ex:
        st.error(f"⚠️ **Ocorreu um erro ao processar o arquivo:** {str(ex)}")
        st.stop()
elif use_default_button or (not uploaded_file and os.path.exists(default_excel_file)):
    source_name = default_excel_file
    try:
        df_raw = read_training_file(default_excel_file)
    except Exception as ex:
        st.error(f"⚠️ Erro ao carregar arquivo de demonstração: {str(ex)}")
        st.stop()

if df_raw is None:
    st.info(
        "👋 **Bem-vindo ao BRVAL Hub de Treinamentos!**\n\n"
        "Para iniciar a auditoria, utilize o painel lateral à esquerda para carregar a planilha "
        "`Controle de Treinamento 03 anos.xlsx`."
    )
    st.stop()


# ---------------------------------------------------------
# Processamento de Dados via Motor de Regras com Data de Corte
# ---------------------------------------------------------
try:
    df_ativos, kpis = process_training_data(df_raw, reference_date=data_referencia_calculo)
except MissingColumnsError as mce:
    st.error(f"⚠️ **Inconsistência no cabeçalho:** {str(mce)}")
    st.stop()
except AuditException as ae:
    st.warning(f"ℹ️ **Aviso da auditoria:** {str(ae)}")
    st.stop()
except Exception as ex:
    st.error(f"⚠️ Erro inesperado durante o cálculo: {str(ex)}")
    st.stop()


# Alerta se houver simulação de data futura ativa
if projecao_opcao != "Data Atual (Hoje)":
    st.markdown(f"""
    <div class="projection-banner">
        <span>🔮</span>
        <div>
            <strong>Modo de Projeção Preventiva Ativo:</strong> 
            Calculando status simulado para a data de corte <strong>{kpis['data_referencia']}</strong> ({projecao_opcao}).
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# Auditoria de Qualidade Cadastral (Data Hygiene)
# ---------------------------------------------------------
issues_cadastrais = check_data_quality(df_raw, reference_date=data_referencia_calculo)
if issues_cadastrais:
    with st.expander(f"🛡️ **Atenção Cadastral: {len(issues_cadastrais)} inconsistência(s) detectada(s) na planilha**", expanded=False):
        st.markdown(
            "Identificamos divergências cadastrais que podem impactar a consistência no **eSocial (Evento S-2245)**. "
            "Recomenda-se correção no sistema de folha de pagamento:"
        )
        df_issues = pd.DataFrame(issues_cadastrais)
        st.dataframe(df_issues, use_container_width=True, hide_index=True)


# ---------------------------------------------------------
# Painel de Indicadores (5 Métricas Corporativas)
# ---------------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Colaboradores Ativos</div>
        <div class="metric-value">{kpis['total_ativos']}</div>
        <div class="metric-footer text-muted">{kpis['total_demitidos']} demissões ignoradas</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Treinamento Vencido</div>
        <div class="metric-value text-yellow">{kpis['total_precisam']}</div>
        <div class="metric-footer text-yellow">Requerem Integração (&gt; 3 anos)</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Risco Crítico (&gt; 5 anos)</div>
        <div class="metric-value text-danger">{kpis.get('total_criticos', 0)}</div>
        <div class="metric-footer text-danger">Gravidade imediata</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Em Conformidade</div>
        <div class="metric-value text-teal">{kpis['total_conforme']}</div>
        <div class="metric-footer text-teal">{kpis['taxa_conformidade']}% da força ativa</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Atenção (Próx. 90d)</div>
        <div class="metric-value text-yellow">{kpis.get('total_atencao_90d', 0)}</div>
        <div class="metric-footer text-muted">Vencimento preventivo</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 1.2rem;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Abas de Navegação (5 Abas Corporativas)
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Auditoria & Elegibilidade",
    "📊 Panorama & Filiais",
    "✉️ Convocação & Notificações",
    "⚖️ Matriz de Riscos Trabalhistas",
    "📐 Simulação & Regras de Cálculo"
])


# ---------------------------------------------------------
# ABA 1: Auditoria & Elegibilidade (Tabela Principal + Exports)
# ---------------------------------------------------------
with tab1:
    col_filter_empresa, col_filter_status, col_filter_urgencia, col_search = st.columns([1.4, 1.1, 1.2, 1.5])

    with col_filter_empresa:
        lista_empresas = ["Todas as Empresas"] + kpis["empresas"]
        empresa_selecionada = st.selectbox(
            "🏢 Selecionar Empresa / Filial:",
            options=lista_empresas,
            index=0
        )

    with col_filter_status:
        status_filter = st.selectbox(
            "🎯 Filtrar Status:",
            options=["Apenas Elegíveis (Precisa)", "Todos os Ativos", "Apenas em Conformidade (Não Precisa)"],
            index=0
        )

    with col_filter_urgencia:
        niveis_disponiveis = ["Todos os Níveis", "Crítico (> 5 anos)", "Alto (4 a 5 anos)", "Moderado (3 a 4 anos)", "Atenção (Vence em 90 dias)", "Conforme Regular"]
        urgencia_filter = st.selectbox(
            "⚠️ Nível de Urgência:",
            options=niveis_disponiveis,
            index=0
        )

    with col_search:
        nome_busca = st.text_input(
            "🔍 Buscar Colaborador:",
            placeholder="Digite o nome..."
        )

    # Aplicação dos Filtros
    df_filtrado = df_ativos.copy()

    if empresa_selecionada != "Todas as Empresas":
        df_filtrado = df_filtrado[df_filtrado["Empresa"] == empresa_selecionada]

    if status_filter == "Apenas Elegíveis (Precisa)":
        df_filtrado = df_filtrado[df_filtrado["Status"] == "Precisa"]
    elif status_filter == "Apenas em Conformidade (Não Precisa)":
        df_filtrado = df_filtrado[df_filtrado["Status"] == "Não Precisa"]

    if urgencia_filter != "Todos os Níveis":
        df_filtrado = df_filtrado[df_filtrado["Nivel_Risco"] == urgencia_filter]

    if nome_busca:
        termo = nome_busca.strip().lower()
        df_filtrado = df_filtrado[df_filtrado["Colaborador"].str.lower().str.contains(termo)]

    # Cabeçalho da Tabela e Botões de Exportação Lado a Lado
    col_tabela_header, col_export_csv, col_export_excel = st.columns([2.5, 1.2, 1.3])
    with col_tabela_header:
        st.markdown(
            f"### Listagem de Colaboradores "
            f"<span style='font-size: 0.95rem; color: #94A3B8; font-weight: normal;'>"
            f"({len(df_filtrado)} resultado(s) exibido(s))</span>",
            unsafe_allow_html=True
        )

    data_str = datetime.now().strftime("%Y%m%d")
    empresa_nome_limpo = empresa_selecionada.replace(" ", "_").replace("/", "_").lower()

    with col_export_csv:
        if not df_filtrado.empty:
            csv_data = generate_export_csv(df_filtrado)
            st.download_button(
                label="📥 Baixar CSV (UTF-8)",
                data=csv_data,
                file_name=f"relatorio_treinamento_{empresa_nome_limpo}_{data_str}.csv",
                mime="text/csv",
                use_container_width=True,
                help="Gera relatório em formato CSV com codificação UTF-8 compatível com Excel."
            )

    with col_export_excel:
        if not df_filtrado.empty:
            excel_data = generate_export_excel(df_ativos, kpis, empresa_filtro=empresa_selecionada)
            st.download_button(
                label="📊 Baixar Excel Oficial (.xlsx)",
                data=excel_data,
                file_name=f"auditoria_treinamento_brval_{empresa_nome_limpo}_{data_str}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                help="Gera planilha oficial estilizada da BRVAL (.xlsx) com abas de Vencidos, Base Completa e Resumo por Filiais."
            )

    # Exibição da Tabela Customizada
    if df_filtrado.empty:
        st.info("Nenhum colaborador encontrado com os critérios de filtro selecionados.")
    else:
        colunas_exibicao = [
            "Empresa",
            "Colaborador",
            "Admissao_Fmt",
            "Primeiro_Treinamento_Fmt",
            "Data_Base_Fmt",
            "Origem_Data_Base",
            "Tempo_Decorrido_Anos",
            "Data_Limite_Fmt",
            "Nivel_Risco",
            "Status"
        ]

        df_display = df_filtrado[colunas_exibicao].copy()
        df_display.columns = [
            "Empresa",
            "Colaborador",
            "Admissão",
            "1º Treinamento",
            "Data Base",
            "Origem",
            "Tempo (Anos)",
            "Limite Renovação",
            "Nível de Urgência",
            "Status"
        ]

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Empresa": st.column_config.TextColumn("Empresa", width="medium"),
                "Colaborador": st.column_config.TextColumn("Colaborador", width="large"),
                "Admissão": st.column_config.TextColumn("Admissão", width="small"),
                "1º Treinamento": st.column_config.TextColumn("1º Treinamento", width="small"),
                "Data Base": st.column_config.TextColumn("Data Base", width="small"),
                "Origem": st.column_config.TextColumn("Origem", width="small"),
                "Tempo (Anos)": st.column_config.NumberColumn(
                    "Tempo (Anos)",
                    format="%.2f",
                    width="small"
                ),
                "Limite Renovação": st.column_config.TextColumn("Limite", width="small"),
                "Nível de Urgência": st.column_config.TextColumn("Urgência", width="medium"),
                "Status": st.column_config.TextColumn("Status", width="small")
            }
        )

    # Resumo Rápido da Seleção
    total_precisam_filtro = (df_filtrado["Status"] == "Precisa").sum()
    if total_precisam_filtro > 0:
        st.warning(
            f"⚠️ **Atenção:** Existem **{total_precisam_filtro}** colaborador(es) nesta seleção "
            f"com prazo de integração superior a 3 anos. Recomenda-se acionamento imediato das lideranças."
        )


# ---------------------------------------------------------
# ABA 2: Panorama Gráfico & Distribuição por Empresa
# ---------------------------------------------------------
with tab2:
    st.markdown("### 📊 Distribuição de Elegibilidade por Empresa")

    grouped = df_ativos.groupby(["Empresa", "Status"]).size().unstack(fill_value=0)
    
    if "Precisa" not in grouped.columns:
        grouped["Precisa"] = 0
    if "Não Precisa" not in grouped.columns:
        grouped["Não Precisa"] = 0

    grouped["Total Ativos"] = grouped["Precisa"] + grouped["Não Precisa"]
    grouped["Taxa Vencidos (%)"] = ((grouped["Precisa"] / grouped["Total Ativos"]) * 100).round(1)
    grouped = grouped.sort_values(by="Precisa", ascending=False)

    col_chart, col_chart_kpi = st.columns([2.5, 1.5])

    with col_chart:
        st.markdown("##### 📌 Pendências de Integração por Filial")
        chart_data = grouped[["Precisa", "Não Precisa"]]
        st.bar_chart(chart_data, color=["#FFCC29", "#57A695"])
        st.caption("🟡 Amarelo: Precisa de Treinamento (> 3 anos) | 🟢 Verde: Em Conformidade (<= 3 anos)")

    with col_chart_kpi:
        st.markdown("##### 🏢 Quadro Resumo de Filiais")
        summary_table = grouped.reset_index()[["Empresa", "Precisa", "Total Ativos", "Taxa Vencidos (%)"]]
        summary_table.columns = ["Empresa", "Vencidos", "Ativos", "Risco (%)"]
        st.dataframe(summary_table, use_container_width=True, hide_index=True)


# ---------------------------------------------------------
# ABA 3: Convocação & Notificações (SESMT / Lideranças)
# ---------------------------------------------------------
with tab3:
    st.markdown("### ✉️ Gerador de Convocação Oficial de Treinamentos")
    st.markdown(
        "Gere notificações formais prontas para envio aos gestores de filial e ao SESMT, "
        "assegurando conformidade com as exigências da NR-1 e do eSocial (Evento S-2245)."
    )

    tipo_convocacao = st.radio(
        "Selecione o formato de convocação:",
        options=["Convocação Coletiva por Filial (Recomendado)", "Convocação Individual por Colaborador"],
        horizontal=True
    )

    if tipo_convocacao == "Convocação Coletiva por Filial (Recomendado)":
        col_filial_conv, _ = st.columns([2, 2])
        with col_filial_conv:
            filial_convocacao = st.selectbox(
                "Selecione a Filial para Convocação:",
                options=kpis["empresas"]
            )

        colabs_vencidos_filial = df_ativos[
            (df_ativos["Empresa"] == filial_convocacao) & 
            (df_ativos["Status"] == "Precisa")
        ].to_dict(orient="records")

        if not colabs_vencidos_filial:
            st.success(f"🎉 Excelente! A filial **{filial_convocacao}** não possui nenhum colaborador com treinamento vencido.")
        else:
            batch_text = generate_batch_convocation(filial_convocacao, colabs_vencidos_filial)
            st.markdown(f"**Total de convocados nesta filial:** `{len(colabs_vencidos_filial)} colaboradores`")
            
            st.text_area(
                "Texto do Memorando / E-mail Oficial:",
                value=batch_text,
                height=320
            )

            st.download_button(
                label="📥 Baixar Comunicado (.txt)",
                data=batch_text.encode("utf-8"),
                file_name=f"convocacao_coletiva_{filial_convocacao.replace(' ', '_').lower()}.txt",
                mime="text/plain"
            )

    else:
        colabs_precisam_df = df_ativos[df_ativos["Status"] == "Precisa"].sort_values(by="Colaborador")
        if colabs_precisam_df.empty:
            st.success("Nenhum colaborador com pendência de integração!")
        else:
            col_selecao_colab, _ = st.columns([2, 2])
            with col_selecao_colab:
                colab_nomes = colabs_precisam_df["Colaborador"].tolist()
                colab_escolhido = st.selectbox("Selecione o Colaborador:", options=colab_nomes)

            row_colab = colabs_precisam_df[colabs_precisam_df["Colaborador"] == colab_escolhido].iloc[0]
            
            email_individual = generate_convocation_email(
                colaborador_nome=row_colab["Colaborador"],
                empresa=row_colab["Empresa"],
                tempo_decorrido=row_colab["Tempo_Decorrido_Anos"],
                data_base_str=row_colab["Data_Base_Fmt"],
                origem_data_base=row_colab["Origem_Data_Base"]
            )

            st.text_area(
                "E-mail de Notificação Formal:",
                value=email_individual,
                height=320
            )

            st.download_button(
                label="📥 Baixar E-mail de Convocação (.txt)",
                data=email_individual.encode("utf-8"),
                file_name=f"convocacao_{row_colab['Colaborador'].replace(' ', '_').lower()}.txt",
                mime="text/plain"
            )


# ---------------------------------------------------------
# ABA 4: Matriz de Riscos Trabalhistas & Passivo
# ---------------------------------------------------------
with tab4:
    st.markdown("### ⚖️ Matriz de Riscos Trabalhistas e Prevenção de Passivo Jurídico")
    st.markdown(
        "A auditoria de integração atua diretamente na blindagem jurídica da BRVAL, "
        "mitigando autuações administrativas e condenações judiciais:"
    )

    col_r1, col_r2, col_r3 = st.columns(3)

    with col_r1:
        st.markdown("""
        <div class="risk-card">
            <h4 style="color:#FFCC29; margin-top:0;">1. Risco eSocial (Evento S-2245)</h4>
            <p style="font-size:0.88rem; color:#CBD5E1; line-height: 1.5;">
                A não realização da integração atrelada a NRs (NR-1, NR-10) impede o envio regular 
                de treinamentos ao <strong>eSocial</strong>. A malha fina digital da Receita Federal e MTE cruza a data de 
                admissão com os envios do evento <strong>S-2245</strong>. As autuações fiscais são aplicadas individualmente por trabalhador irregular.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_r2:
        st.markdown("""
        <div class="risk-card">
            <h4 style="color:#FFCC29; margin-top:0;">2. Responsabilidade Civil Objetiva</h4>
            <p style="font-size:0.88rem; color:#CBD5E1; line-height: 1.5;">
                Em caso de eventual acidente de trabalho, a falta de comprovação documental do 
                treinamento de integração vigente inverte o ônus da prova e caracteriza <strong>culpa in omittendo</strong> 
                da BRVAL perante o Tribunal Superior do Trabalho (TST), ensejando indenizações por danos materiais e morais.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_r3:
        st.markdown("""
        <div class="risk-card">
            <h4 style="color:#FFCC29; margin-top:0;">3. Atenção à Jornada (Horas Extras)</h4>
            <p style="font-size:0.88rem; color:#CBD5E1; line-height: 1.5;">
                Os treinamentos apontados pelo sistema <strong>devem obrigatoriamente</strong> ser realizados dentro 
                da jornada regular de trabalho. Se realizados fora, configuram tempo à disposição do empregador (Art. 4º da CLT), 
                gerando Horas Extras com reflexos diretos em DSR, Férias, 13º e FGTS.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="risk-card-teal">
        <h4 style="color:#73C2B1; margin-top:0;">Recomendação Prática de DP</h4>
        <p style="font-size:0.9rem; color:#CBD5E1; margin-bottom: 0;">
            1. Baixe o relatório consolidado dos elegíveis via Excel (.xlsx) ou CSV.<br>
            2. Utilize a aba <strong>Convocação & Notificações</strong> para emitir os memorandos às filiais.<br>
            3. Colha lista de presença com assinatura e emita o certificado com menção às NRs aplicáveis para lançamento no eSocial (S-2245).
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# ABA 5: Simulação & Regras de Negócio (SDD 2.2)
# ---------------------------------------------------------
with tab5:
    st.markdown("### 📐 Regras de Negócio e Formulação Matemática")
    st.markdown("""
    A auditoria é processada dinamicamente no momento da leitura, ignorando colunas pré-calculadas 
    para garantir acurácia diária sem defasagem temporal.
    """)

    c_math1, c_math2 = st.columns(2)

    with c_math1:
        st.markdown("#### 1. Definição da Data Base")
        st.info("""
        • **Se '1º Treinamento' preenchido:** Data Base = 1º Treinamento  
        • **Se '1º Treinamento' nulo:** Data Base = Admissão
        """)

        st.markdown("#### 2. Fórmula Matemática de Tempo")
        st.latex(r"Tempo = \frac{\text{Data Atual} - \text{Data Base}}{365.25}")
        st.caption("O divisor 365.25 garante a compensação de anos bissextos.")

    with c_math2:
        st.markdown("#### 3. Matriz de Decisão Lógica")
        st.latex(r"""
        Status = \begin{cases} 
        \text{"Precisa"}, & \text{se } Tempo > 3 \\ 
        \text{"Não Precisa"}, & \text{se } Tempo \le 3 
        \end{cases}
        """)

    st.markdown("#### 4. Simulação Matemática Conforme SDD (Seção 2.2.1)")
    simulacao_dados = pd.DataFrame([
        {
            "Colaborador": "Func. A",
            "Admissão": "01/01/2020",
            "1º Treinamento": "01/01/2023",
            "Data Base Utilizada": "01/01/2023",
            "Tempo Decorrido (Anos)": "3.76",
            "Status": "Precisa"
        },
        {
            "Colaborador": "Func. B",
            "Admissão": "15/05/2023",
            "1º Treinamento": "Nulo",
            "Data Base Utilizada": "15/05/2023",
            "Tempo Decorrido (Anos)": "3.39",
            "Status": "Precisa"
        },
        {
            "Colaborador": "Func. C",
            "Admissão": "10/10/2024",
            "1º Treinamento": "Nulo",
            "Data Base Utilizada": "10/10/2024",
            "Tempo Decorrido (Anos)": "1.99",
            "Status": "Não Precisa"
        }
    ])
    st.table(simulacao_dados)
