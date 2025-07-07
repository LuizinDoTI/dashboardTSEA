"""
Dashboard Principal - TSEA Energia
Aplicação Streamlit para análise de resultados de testes de transformadores

Autor: Protótipo de Luiz
Data: 29 de Junho de 2025
Versão: 2.0 - Integração com Agente de IA
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import warnings

# Importa módulos personalizados
from config import TEXTOS_INTERFACE, APP_CONFIG
from data_generator import obter_dados
from filters import DashboardFilters, criar_filtros_rapidos, aplicar_filtros_rapidos
from metrics import DashboardMetrics
from visualizations import DashboardVisualizations, criar_visualizacao
from utils import (
    DataExporter, DataValidator, SessionManager, 
    configurar_pagina, criar_sidebar_info, criar_alerta_qualidade, log_acao
)
# Importação do novo agente de IA
from ai_agent import AIAgent

# Suprime warnings desnecessários
warnings.filterwarnings('ignore')


def main():
    """Função principal do dashboard"""
    
    # Configuração inicial da página
    configurar_pagina()
    
    # Inicializa sessão
    SessionManager.inicializar_sessao()
    
    # Título principal
    st.title(TEXTOS_INTERFACE['titulo_principal'])
    st.markdown(TEXTOS_INTERFACE['subtitulo'])
    
    log_acao("Acesso ao dashboard", "Usuário acessou a página principal")
    
    # Carregamento dos dados
    with st.spinner("Carregando dados..."):
        df = carregar_dados_dashboard()
    
    if df.empty:
        st.error("❌ Não foi possível carregar os dados. Verifique a configuração.")
        st.stop()
    
    # Validação dos dados
    validador = DataValidator()
    resultado_validacao = validador.validar_dataframe(df)
    
    # Exibe alertas de qualidade se necessário
    alerta = criar_alerta_qualidade(df)
    if alerta:
        st.warning(alerta)
    
    # Criação dos filtros
    filtros_manager = DashboardFilters(df)
    
    # Filtros rápidos na área principal
    filtros_rapidos = criar_filtros_rapidos(df)
    if filtros_rapidos.get('tipo'):
        df = aplicar_filtros_rapidos(df, filtros_rapidos)
        log_acao("Filtro rápido aplicado", f"Tipo: {filtros_rapidos['tipo']}")
    
    # Filtros detalhados na sidebar
    filtros = filtros_manager.criar_filtros_sidebar()
    
    # Validação dos filtros
    filtros_validos, erro_filtros = filtros_manager.validar_filtros(filtros)
    if not filtros_validos:
        st.error(f"❌ {erro_filtros}")
        st.stop()
    
    # Aplicação dos filtros
    df_filtrado = filtros_manager.aplicar_filtros(filtros)
    
    # Salva filtros na sessão
    SessionManager.salvar_filtros(filtros)
    
    log_acao("Filtros aplicados", f"Registros resultantes: {len(df_filtrado)}")
    
    # Verifica se há dados após filtros
    if df_filtrado.empty:
        st.warning(TEXTOS_INTERFACE['sem_dados'])
        st.info("💡 Dica: Tente ajustar os filtros para incluir mais dados.")
        return
    
    # Exibe resumo dos filtros aplicados
    resumo_filtros = filtros_manager.obter_resumo_filtros(filtros)
    st.info(f"📊 {resumo_filtros}")

    # Seção de Resumo da IA
    exibir_secao_ia_resumo(df_filtrado)
    
    # Seção de métricas
    exibir_secao_metricas(df_filtrado)
    
    # Seção de visualizações
    exibir_secao_visualizacoes(df_filtrado)
    
    # Seção de dados detalhados e diagnóstico por IA
    exibir_secao_dados_e_diagnostico(df_filtrado)
    
    # Sidebar com informações adicionais
    criar_sidebar_info()
    
    # Histórico de filtros
    SessionManager.exibir_historico_filtros()


def carregar_dados_dashboard() -> pd.DataFrame:
    """
    Carrega os dados para o dashboard
    
    Returns:
        DataFrame com os dados carregados
    """
    try:
        # Por padrão, usa dados fictícios
        df = obter_dados(fonte='ficticios')
        
        if not df.empty:
            st.session_state.dados_carregados = True
            log_acao("Dados carregados", f"Total de registros: {len(df)}")
        
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()


def exibir_secao_ia_resumo(df: pd.DataFrame):
    """
    Exibe o resumo executivo gerado pela IA.
    """
    with st.expander("🤖 Resumo Executivo por IA (Gemini)", expanded=True):
        with st.spinner("Analisando dados e gerando insights..."):
            agent = AIAgent(df)
            resumo = agent.gerar_resumo_executivo()
            if resumo:
                st.markdown(resumo)
            else:
                st.info("Não foi possível gerar o resumo. Verifique a configuração da API.")


def exibir_secao_metricas(df: pd.DataFrame):
    """
    Exibe a seção de métricas do dashboard
    
    Args:
        df: DataFrame com os dados filtrados
    """
    metrics_manager = DashboardMetrics(df)
    
    metrics_manager.exibir_metricas_principais()
    metrics_manager.exibir_metricas_detalhadas()


def exibir_secao_visualizacoes(df: pd.DataFrame):
    """
    Exibe a seção de visualizações do dashboard
    
    Args:
        df: DataFrame com os dados filtrados
    """
    st.markdown("---")
    st.header(TEXTOS_INTERFACE['graficos_titulo'])
    
    visualizacoes_disponiveis = {
        'eficiencia_tempo': '📈 Eficiência vs Tempo',
        'perdas_temperatura': '🌡️ Perdas vs Temperatura',
        'distribuicao_modelos': '🥧 Distribuição por Modelo',
        'aprovacao_modelo': '✅ Taxa de Aprovação',
        'histograma_eficiencia': '📊 Histograma Eficiência',
        'boxplot_temperatura': '📦 BoxPlot Temperatura',
        'tendencia_mensal': '📅 Tendência Mensal',
        'correlacao_potencia': '⚡ Potência vs Perdas'
    }
    
    graficos_selecionados = st.multiselect(
        "Selecione os gráficos para exibir:",
        options=list(visualizacoes_disponiveis.keys()),
        default=['eficiencia_tempo', 'distribuicao_modelos', 'aprovacao_modelo', 'perdas_temperatura'],
        format_func=lambda x: visualizacoes_disponiveis[x]
    )
    
    if graficos_selecionados:
        num_cols = 2
        cols = st.columns(num_cols)
        for i, grafico_key in enumerate(graficos_selecionados):
            with cols[i % num_cols]:
                fig = criar_visualizacao(grafico_key, df)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Selecione pelo menos um gráfico para visualizar.")


def exibir_secao_dados_e_diagnostico(df: pd.DataFrame):
    """
    Exibe a seção de dados detalhados e o diagnóstico por IA.
    """
    st.markdown("---")
    st.header("🔬 Análise Detalhada e Diagnóstico por IA")

    tab1, tab2 = st.tabs(["Dados Detalhados", "🤖 Diagnóstico de Ativo por IA"])

    with tab1:
        st.subheader(TEXTOS_INTERFACE['dados_titulo'])
        col1, col2 = st.columns(2)
        with col1:
            num_registros = st.selectbox(
                "Registros por página:",
                options=[10, 25, 50, 100, len(df)],
                index=0, key="paginacao"
            )
        with col2:
            ordenar_por = st.selectbox(
                "Ordenar por:",
                options=df.columns.tolist(),
                index=df.columns.tolist().index('Data_Teste')
            )
        
        df_ordenado = df.sort_values(by=ordenar_por, ascending=False)
        st.dataframe(df_ordenado.head(num_registros), use_container_width=True)
        DataExporter.criar_botoes_download(df)

    with tab2:
        st.subheader("Análise de Causa Raiz para um Transformador Específico")
        
        ids_reprovados = df[df['Status_Aprovacao'] == 'Reprovado']['ID_Transformador'].unique()
        ids_outros = df[~df['ID_Transformador'].isin(ids_reprovados)]['ID_Transformador'].unique()
        
        id_selecionado = st.selectbox(
            "Selecione o ID do Transformador para análise:",
            options=np.concatenate([ids_reprovados, ids_outros]),
            help="Transformadores com status 'Reprovado' aparecem primeiro na lista."
        )

        if st.button(f"Gerar Diagnóstico para {id_selecionado}", type="primary"):
            with st.spinner(f"A IA está realizando uma análise completa do transformador {id_selecionado}..."):
                agent = AIAgent(df)
                diagnostico = agent.gerar_diagnostico_transformador(id_selecionado)
                if diagnostico:
                    st.markdown(diagnostico)
                else:
                    st.error("Não foi possível gerar o diagnóstico.")
                log_acao("Diagnóstico IA gerado", f"Ativo: {id_selecionado}")


if __name__ == "__main__":
    main()