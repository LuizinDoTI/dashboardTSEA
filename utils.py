"""
Módulo de utilitários e funções auxiliares
Este módulo contém funções auxiliares para o dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime
from typing import Optional, Dict, Any
from config import EXPORT_CONFIG, TEXTOS_INTERFACE


class DataExporter:
    """Classe responsável pela exportação de dados"""
    
    @staticmethod
    def to_csv(df: pd.DataFrame, filename: Optional[str] = None) -> bytes:
        """
        Converte DataFrame para CSV
        
        Args:
            df: DataFrame a ser convertido
            filename: Nome do arquivo (opcional)
            
        Returns:
            Bytes do arquivo CSV
        """
        return df.to_csv(index=False).encode(EXPORT_CONFIG['encoding'])
    
    @staticmethod
    def to_excel(df: pd.DataFrame, filename: Optional[str] = None) -> bytes:
        """
        Converte DataFrame para Excel
        
        Args:
            df: DataFrame a ser convertido
            filename: Nome do arquivo (opcional)
            
        Returns:
            Bytes do arquivo Excel
        """
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Dados_Testes', index=False)
            
            # Adiciona formatação
            workbook = writer.book
            worksheet = writer.sheets['Dados_Testes']
            
            # Formato para cabeçalhos
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # Aplica formato aos cabeçalhos
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Ajusta largura das colunas
            for i, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).map(len).max(),
                    len(str(col))
                ) + 2
                worksheet.set_column(i, i, min(max_length, 50))
        
        return output.getvalue()
    
    @staticmethod
    def criar_botoes_download(df: pd.DataFrame):
        """
        Cria botões de download para CSV e Excel
        
        Args:
            df: DataFrame a ser exportado
        """
        if df.empty:
            st.warning("Nenhum dado disponível para download")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = DataExporter.to_csv(df)
            st.download_button(
                label=TEXTOS_INTERFACE['botao_download_csv'],
                data=csv_data,
                file_name=EXPORT_CONFIG['nome_arquivo_csv'],
                mime='text/csv',
                help="Baixar dados filtrados em formato CSV"
            )
        
        with col2:
            excel_data = DataExporter.to_excel(df)
            st.download_button(
                label=TEXTOS_INTERFACE['botao_download_excel'],
                data=excel_data,
                file_name=EXPORT_CONFIG['nome_arquivo_excel'],
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                help="Baixar dados filtrados em formato Excel com formatação"
            )


class DataValidator:
    """Classe para validação de dados"""
    
    @staticmethod
    def validar_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Valida a estrutura e qualidade dos dados
        
        Args:
            df: DataFrame a ser validado
            
        Returns:
            Dicionário com resultado da validação
        """
        resultado = {
            'valido': True,
            'erros': [],
            'avisos': [],
            'estatisticas': {}
        }
        
        if df.empty:
            resultado['valido'] = False
            resultado['erros'].append("DataFrame está vazio")
            return resultado
        
        # Verifica colunas obrigatórias
        colunas_obrigatorias = [
            'ID_Transformador', 'Modelo', 'Data_Teste', 'Tipo_Ensaio',
            'Eficiencia_Percentual', 'Elevacao_Temperatura_C', 
            'Perdas_Totais_kW', 'Status_Aprovacao'
        ]
        
        colunas_faltantes = [col for col in colunas_obrigatorias if col not in df.columns]
        if colunas_faltantes:
            resultado['valido'] = False
            resultado['erros'].append(f"Colunas obrigatórias faltantes: {', '.join(colunas_faltantes)}")
        
        # Verifica valores nulos
        for col in df.columns:
            nulos = df[col].isnull().sum()
            if nulos > 0:
                percentual = (nulos / len(df)) * 100
                if percentual > 10:
                    resultado['avisos'].append(f"Coluna '{col}' tem {percentual:.1f}% de valores nulos")
        
        # Verifica tipos de dados
        if 'Data_Teste' in df.columns:
            try:
                pd.to_datetime(df['Data_Teste'])
            except:
                resultado['erros'].append("Coluna 'Data_Teste' não está em formato de data válido")
        
        # Verifica valores numéricos
        colunas_numericas = ['Eficiencia_Percentual', 'Elevacao_Temperatura_C', 'Perdas_Totais_kW']
        for col in colunas_numericas:
            if col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    resultado['erros'].append(f"Coluna '{col}' deve ser numérica")
        
        # Estatísticas básicas
        resultado['estatisticas'] = {
            'total_registros': len(df),
            'colunas': len(df.columns),
            'periodo': {
                'inicio': df['Data_Teste'].min() if 'Data_Teste' in df.columns else None,
                'fim': df['Data_Teste'].max() if 'Data_Teste' in df.columns else None
            }
        }
        
        return resultado
    
    @staticmethod
    def exibir_resultado_validacao(resultado: Dict[str, Any]):
        """
        Exibe o resultado da validação na interface
        
        Args:
            resultado: Resultado da validação
        """
        if resultado['valido']:
            st.success("✅ Dados validados com sucesso!")
        else:
            st.error("❌ Problemas encontrados na validação dos dados:")
            for erro in resultado['erros']:
                st.error(f"• {erro}")
        
        if resultado['avisos']:
            st.warning("⚠️ Avisos:")
            for aviso in resultado['avisos']:
                st.warning(f"• {aviso}")
        
        # Exibe estatísticas
        if resultado['estatisticas']:
            with st.expander("📊 Estatísticas dos Dados"):
                stats = resultado['estatisticas']
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total de Registros", f"{stats['total_registros']:,}")
                with col2:
                    st.metric("Número de Colunas", stats['colunas'])
                with col3:
                    if stats['periodo']['inicio'] and stats['periodo']['fim']:
                        periodo_dias = (stats['periodo']['fim'] - stats['periodo']['inicio']).days
                        st.metric("Período (dias)", periodo_dias)


class SessionManager:
    """Classe para gerenciamento de sessão do Streamlit"""
    
    @staticmethod
    def inicializar_sessao():
        """Inicializa variáveis de sessão"""
        if 'dados_carregados' not in st.session_state:
            st.session_state.dados_carregados = False
        
        if 'filtros_aplicados' not in st.session_state:
            st.session_state.filtros_aplicados = {}
        
        if 'historico_filtros' not in st.session_state:
            st.session_state.historico_filtros = []
    
    @staticmethod
    def salvar_filtros(filtros: Dict[str, Any]):
        """
        Salva filtros no histórico da sessão
        
        Args:
            filtros: Filtros a serem salvos
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        entrada_historico = {
            'timestamp': timestamp,
            'filtros': filtros.copy()
        }
        
        if 'historico_filtros' not in st.session_state:
            st.session_state.historico_filtros = []
        
        st.session_state.historico_filtros.append(entrada_historico)
        
        # Mantém apenas os últimos 10 filtros
        if len(st.session_state.historico_filtros) > 10:
            st.session_state.historico_filtros = st.session_state.historico_filtros[-10:]
    
    @staticmethod
    def exibir_historico_filtros():
        """Exibe histórico de filtros aplicados"""
        if 'historico_filtros' in st.session_state and st.session_state.historico_filtros:
            with st.expander("📝 Histórico de Filtros"):
                for i, entrada in enumerate(reversed(st.session_state.historico_filtros)):
                    st.text(f"{entrada['timestamp']} - Filtros aplicados")


def formatar_numero(numero: float, casas_decimais: int = 2, sufixo: str = "") -> str:
    """
    Formata número para exibição
    
    Args:
        numero: Número a ser formatado
        casas_decimais: Número de casas decimais
        sufixo: Sufixo a ser adicionado
        
    Returns:
        String formatada
    """
    if pd.isna(numero):
        return "N/A"
    
    if abs(numero) >= 1000000:
        return f"{numero/1000000:.{casas_decimais}f}M{sufixo}"
    elif abs(numero) >= 1000:
        return f"{numero/1000:.{casas_decimais}f}K{sufixo}"
    else:
        return f"{numero:.{casas_decimais}f}{sufixo}"


def criar_alerta_qualidade(df: pd.DataFrame) -> Optional[str]:
    """
    Cria alertas baseados na qualidade dos dados
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        String com alerta ou None
    """
    if df.empty:
        return None
    
    alertas = []
    
    # Verifica taxa de aprovação baixa
    if 'Status_Aprovacao' in df.columns:
        taxa_aprovacao = (df['Status_Aprovacao'].value_counts(normalize=True).get('Aprovado', 0)) * 100
        if taxa_aprovacao < 85:
            alertas.append(f"⚠️ Taxa de aprovação baixa: {taxa_aprovacao:.1f}%")
    
    # Verifica eficiência baixa
    if 'Eficiencia_Percentual' in df.columns:
        eficiencia_media = df['Eficiencia_Percentual'].mean()
        if eficiencia_media < 98.5:
            alertas.append(f"⚠️ Eficiência média baixa: {eficiencia_media:.2f}%")
    
    # Verifica temperatura alta
    if 'Elevacao_Temperatura_C' in df.columns:
        temp_alta = len(df[df['Elevacao_Temperatura_C'] > 60])
        if temp_alta > 0:
            alertas.append(f"🌡️ {temp_alta} testes com temperatura elevada (>60°C)")
    
    return " | ".join(alertas) if alertas else None


def configurar_pagina():
    """Configura a página do Streamlit"""
    from config import APP_CONFIG
    
    st.set_page_config(
        page_title=APP_CONFIG['page_title'],
        page_icon=APP_CONFIG['page_icon'],
        layout=APP_CONFIG['layout'],
        initial_sidebar_state=APP_CONFIG['initial_sidebar_state']
    )
    
    # CSS personalizado
    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stAlert {
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def criar_sidebar_info():
    """Cria informações na sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Informações")
    st.sidebar.info(
        "Este dashboard permite analisar resultados de testes de transformadores "
        "de forma interativa. Use os filtros para explorar os dados."
    )
    
    st.sidebar.markdown("### 🔧 Configurações")
    if st.sidebar.button("🔄 Recarregar Dados"):
        st.cache_data.clear()
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Desenvolvido com ❤️ usando Streamlit**")
    st.sidebar.markdown("**Versão:** 2.0")


def log_acao(acao: str, detalhes: str = ""):
    """
    Registra ações do usuário (para debugging)
    
    Args:
        acao: Ação realizada
        detalhes: Detalhes adicionais
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if 'log_acoes' not in st.session_state:
        st.session_state.log_acoes = []
    
    st.session_state.log_acoes.append({
        'timestamp': timestamp,
        'acao': acao,
        'detalhes': detalhes
    })
    
    # Mantém apenas os últimos 50 logs
    if len(st.session_state.log_acoes) > 50:
        st.session_state.log_acoes = st.session_state.log_acoes[-50:]

