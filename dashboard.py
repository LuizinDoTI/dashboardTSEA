"""
Dashboard Principal - TSEA Energia
Aplicação Streamlit para análise de resultados de testes de transformadores

Autor: Manus AI (baseado no protótipo de Luiz)
Data: 29 de Junho de 2025
Versão: 2.0 - Versão Modular e Educativa
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
    
    # Log da ação
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
    
    # Log da aplicação de filtros
    log_acao("Filtros aplicados", f"Registros resultantes: {len(df_filtrado)}")
    
    # Verifica se há dados após filtros
    if df_filtrado.empty:
        st.warning(TEXTOS_INTERFACE['sem_dados'])
        st.info("💡 Dica: Tente ajustar os filtros para incluir mais dados.")
        return
    
    # Exibe resumo dos filtros aplicados
    resumo_filtros = filtros_manager.obter_resumo_filtros(filtros)
    st.info(f"📊 {resumo_filtros}")
    
    # Seção de métricas
    exibir_secao_metricas(df_filtrado)
    
    # Seção de visualizações
    exibir_secao_visualizacoes(df_filtrado)
    
    # Seção de dados detalhados
    exibir_secao_dados(df_filtrado)
    
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
        # Para usar dados reais, modifique esta função
        df = obter_dados(fonte='ficticios')
        
        if not df.empty:
            st.session_state.dados_carregados = True
            log_acao("Dados carregados", f"Total de registros: {len(df)}")
        
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()


def exibir_secao_metricas(df: pd.DataFrame):
    """
    Exibe a seção de métricas do dashboard
    
    Args:
        df: DataFrame com os dados filtrados
    """
    metrics_manager = DashboardMetrics(df)
    
    # Métricas principais
    metrics_manager.exibir_metricas_principais()
    
    # Métricas detalhadas
    metrics_manager.exibir_metricas_detalhadas()
    
    # Relatório resumo
    with st.expander("📋 Relatório Resumo", expanded=False):
        relatorio = metrics_manager.gerar_relatorio_resumo()
        st.markdown(relatorio)


def exibir_secao_visualizacoes(df: pd.DataFrame):
    """
    Exibe a seção de visualizações do dashboard
    
    Args:
        df: DataFrame com os dados filtrados
    """
    st.markdown("---")
    st.header(TEXTOS_INTERFACE['graficos_titulo'])
    
    # Seletor de visualizações
    col1, col2 = st.columns([3, 1])
    
    with col2:
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
            "Selecione os gráficos:",
            options=list(visualizacoes_disponiveis.keys()),
            default=['eficiencia_tempo', 'perdas_temperatura', 'distribuicao_modelos', 'aprovacao_modelo'],
            format_func=lambda x: visualizacoes_disponiveis[x]
        )
    
    # Exibe gráficos selecionados
    if graficos_selecionados:
        # Organiza gráficos em grid
        num_graficos = len(graficos_selecionados)
        
        if num_graficos == 1:
            fig = criar_visualizacao(graficos_selecionados[0], df)
            st.plotly_chart(fig, use_container_width=True)
        
        elif num_graficos == 2:
            col1, col2 = st.columns(2)
            with col1:
                fig1 = criar_visualizacao(graficos_selecionados[0], df)
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                fig2 = criar_visualizacao(graficos_selecionados[1], df)
                st.plotly_chart(fig2, use_container_width=True)
        
        elif num_graficos >= 3:
            # Primeira linha
            col1, col2 = st.columns(2)
            with col1:
                fig1 = criar_visualizacao(graficos_selecionados[0], df)
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                fig2 = criar_visualizacao(graficos_selecionados[1], df)
                st.plotly_chart(fig2, use_container_width=True)
            
            # Segunda linha e subsequentes
            for i in range(2, num_graficos, 2):
                col1, col2 = st.columns(2)
                with col1:
                    fig = criar_visualizacao(graficos_selecionados[i], df)
                    st.plotly_chart(fig, use_container_width=True)
                
                if i + 1 < num_graficos:
                    with col2:
                        fig = criar_visualizacao(graficos_selecionados[i + 1], df)
                        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("Selecione pelo menos um gráfico para visualizar.")


def exibir_secao_dados(df: pd.DataFrame):
    """
    Exibe a seção de dados detalhados
    
    Args:
        df: DataFrame com os dados filtrados
    """
    st.markdown("---")
    st.header(TEXTOS_INTERFACE['dados_titulo'])
    
    # Opções de exibição
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mostrar_estatisticas = st.checkbox("📊 Mostrar Estatísticas", value=True)
    
    with col2:
        num_registros = st.selectbox(
            "Registros por página:",
            options=[10, 25, 50, 100, len(df)],
            index=2
        )
    
    with col3:
        ordenar_por = st.selectbox(
            "Ordenar por:",
            options=df.columns.tolist(),
            index=df.columns.tolist().index('Data_Teste') if 'Data_Teste' in df.columns else 0
        )
    
    # Estatísticas descritivas
    if mostrar_estatisticas:
        with st.expander("📈 Estatísticas Descritivas", expanded=False):
            colunas_numericas = df.select_dtypes(include=[np.number]).columns
            if len(colunas_numericas) > 0:
                st.dataframe(df[colunas_numericas].describe())
            else:
                st.info("Nenhuma coluna numérica encontrada para estatísticas.")
    
    # Tabela de dados
    df_ordenado = df.sort_values(by=ordenar_por, ascending=False)
    
    if num_registros < len(df):
        st.dataframe(df_ordenado.head(num_registros), use_container_width=True)
        st.info(f"Exibindo {num_registros} de {len(df)} registros. Use os filtros para refinar a seleção.")
    else:
        st.dataframe(df_ordenado, use_container_width=True)
    
    # Botões de download
    st.markdown("### 📥 Exportar Dados")
    DataExporter.criar_botoes_download(df)
    
    # Log da visualização de dados
    log_acao("Dados visualizados", f"Registros exibidos: {min(num_registros, len(df))}")


def exibir_configuracoes_avancadas():
    """Exibe configurações avançadas na sidebar"""
    with st.sidebar.expander("⚙️ Configurações Avançadas", expanded=False):
        st.markdown("### 🎨 Personalização")
        
        # Tema dos gráficos
        tema_grafico = st.selectbox(
            "Tema dos gráficos:",
            options=['plotly_white', 'plotly_dark', 'ggplot2', 'seaborn'],
            index=0
        )
        
        # Altura dos gráficos
        altura_graficos = st.slider(
            "Altura dos gráficos:",
            min_value=300,
            max_value=800,
            value=400,
            step=50
        )
        
        # Salva configurações na sessão
        st.session_state.tema_grafico = tema_grafico
        st.session_state.altura_graficos = altura_graficos


if __name__ == "__main__":
    main()

