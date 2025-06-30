"""
Módulo para criação e aplicação de filtros
Este módulo contém todas as funções relacionadas aos filtros do dashboard
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from typing import Tuple, List, Optional
from config import TEXTOS_INTERFACE, DATA_CONFIG


class DashboardFilters:
    """Classe responsável pela criação e aplicação de filtros"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.df_filtrado = df.copy()
    
    def criar_filtros_sidebar(self) -> dict:
        """
        Cria todos os filtros na barra lateral
        
        Returns:
            Dicionário com os valores dos filtros selecionados
        """
        st.sidebar.header(TEXTOS_INTERFACE['filtros_titulo'])
        
        filtros = {}
        
        # Filtro por Modelo do Transformador
        filtros['modelos'] = st.sidebar.multiselect(
            "🔧 Selecione o(s) Modelo(s):",
            options=sorted(self.df['Modelo'].unique()),
            default=sorted(self.df['Modelo'].unique()),
            help="Selecione um ou mais modelos de transformadores para análise"
        )
        
        # Filtro por Status de Aprovação
        filtros['status'] = st.sidebar.multiselect(
            "✅ Status da Aprovação:",
            options=self.df['Status_Aprovacao'].unique(),
            default=self.df['Status_Aprovacao'].unique(),
            help="Filtre por status de aprovação dos testes"
        )
        
        # Filtro por Tipo de Ensaio
        filtros['tipos_ensaio'] = st.sidebar.multiselect(
            "🧪 Tipo de Ensaio:",
            options=sorted(self.df['Tipo_Ensaio'].unique()),
            default=sorted(self.df['Tipo_Ensaio'].unique()),
            help="Selecione os tipos de ensaio para análise"
        )
        
        # Filtro por Intervalo de Datas
        data_min = self.df['Data_Teste'].min().date()
        data_max = self.df['Data_Teste'].max().date()
        
        filtros['periodo'] = st.sidebar.date_input(
            "📅 Selecione o Período:",
            value=(data_min, data_max),
            min_value=data_min,
            max_value=data_max,
            format=DATA_CONFIG['formato_data'],
            help="Defina o período de análise dos testes"
        )
        
        # Filtros avançados (expansível)
        with st.sidebar.expander("🔍 Filtros Avançados", expanded=False):
            # Filtro por faixa de eficiência
            efic_min, efic_max = float(self.df['Eficiencia_Percentual'].min()), float(self.df['Eficiencia_Percentual'].max())
            filtros['eficiencia_range'] = st.slider(
                "Faixa de Eficiência (%):",
                min_value=efic_min,
                max_value=efic_max,
                value=(efic_min, efic_max),
                step=0.1,
                help="Filtre por faixa de eficiência"
            )
            
            # Filtro por faixa de temperatura
            temp_min, temp_max = float(self.df['Elevacao_Temperatura_C'].min()), float(self.df['Elevacao_Temperatura_C'].max())
            filtros['temperatura_range'] = st.slider(
                "Faixa de Temperatura (°C):",
                min_value=temp_min,
                max_value=temp_max,
                value=(temp_min, temp_max),
                step=0.1,
                help="Filtre por faixa de elevação de temperatura"
            )
            
            # Filtro por faixa de perdas
            perdas_min, perdas_max = float(self.df['Perdas_Totais_kW'].min()), float(self.df['Perdas_Totais_kW'].max())
            filtros['perdas_range'] = st.slider(
                "Faixa de Perdas (kW):",
                min_value=perdas_min,
                max_value=perdas_max,
                value=(perdas_min, perdas_max),
                step=0.1,
                help="Filtre por faixa de perdas totais"
            )
            
            # Filtro por potência nominal
            if 'Potencia_Nominal_MVA' in self.df.columns:
                potencias_disponiveis = sorted(self.df['Potencia_Nominal_MVA'].unique())
                filtros['potencias'] = st.multiselect(
                    "Potência Nominal (MVA):",
                    options=potencias_disponiveis,
                    default=potencias_disponiveis,
                    help="Selecione as potências nominais"
                )
        
        # Botão para limpar filtros
        if st.sidebar.button("🔄 Limpar Todos os Filtros"):
            st.rerun()
        
        return filtros
    
    def aplicar_filtros(self, filtros: dict) -> pd.DataFrame:
        """
        Aplica os filtros selecionados ao DataFrame
        
        Args:
            filtros: Dicionário com os filtros selecionados
            
        Returns:
            DataFrame filtrado
        """
        df_filtrado = self.df.copy()
        
        # Verifica se há dados para filtrar
        if df_filtrado.empty:
            return df_filtrado
        
        # Filtro por modelos
        if filtros.get('modelos'):
            df_filtrado = df_filtrado[df_filtrado['Modelo'].isin(filtros['modelos'])]
        
        # Filtro por status
        if filtros.get('status'):
            df_filtrado = df_filtrado[df_filtrado['Status_Aprovacao'].isin(filtros['status'])]
        
        # Filtro por tipos de ensaio
        if filtros.get('tipos_ensaio'):
            df_filtrado = df_filtrado[df_filtrado['Tipo_Ensaio'].isin(filtros['tipos_ensaio'])]
        
        # Filtro por período
        if filtros.get('periodo') and len(filtros['periodo']) == 2:
            data_inicio, data_fim = filtros['periodo']
            df_filtrado = df_filtrado[
                (df_filtrado['Data_Teste'].dt.date >= data_inicio) &
                (df_filtrado['Data_Teste'].dt.date <= data_fim)
            ]
        
        # Filtros avançados
        if filtros.get('eficiencia_range'):
            efic_min, efic_max = filtros['eficiencia_range']
            df_filtrado = df_filtrado[
                (df_filtrado['Eficiencia_Percentual'] >= efic_min) &
                (df_filtrado['Eficiencia_Percentual'] <= efic_max)
            ]
        
        if filtros.get('temperatura_range'):
            temp_min, temp_max = filtros['temperatura_range']
            df_filtrado = df_filtrado[
                (df_filtrado['Elevacao_Temperatura_C'] >= temp_min) &
                (df_filtrado['Elevacao_Temperatura_C'] <= temp_max)
            ]
        
        if filtros.get('perdas_range'):
            perdas_min, perdas_max = filtros['perdas_range']
            df_filtrado = df_filtrado[
                (df_filtrado['Perdas_Totais_kW'] >= perdas_min) &
                (df_filtrado['Perdas_Totais_kW'] <= perdas_max)
            ]
        
        if filtros.get('potencias'):
            df_filtrado = df_filtrado[df_filtrado['Potencia_Nominal_MVA'].isin(filtros['potencias'])]
        
        self.df_filtrado = df_filtrado
        return df_filtrado
    
    def obter_resumo_filtros(self, filtros: dict) -> str:
        """
        Cria um resumo textual dos filtros aplicados
        
        Args:
            filtros: Dicionário com os filtros selecionados
            
        Returns:
            String com o resumo dos filtros
        """
        resumo_partes = []
        
        if filtros.get('modelos') and len(filtros['modelos']) < len(self.df['Modelo'].unique()):
            resumo_partes.append(f"Modelos: {', '.join(filtros['modelos'])}")
        
        if filtros.get('status') and len(filtros['status']) < len(self.df['Status_Aprovacao'].unique()):
            resumo_partes.append(f"Status: {', '.join(filtros['status'])}")
        
        if filtros.get('tipos_ensaio') and len(filtros['tipos_ensaio']) < len(self.df['Tipo_Ensaio'].unique()):
            resumo_partes.append(f"Ensaios: {', '.join(filtros['tipos_ensaio'])}")
        
        if filtros.get('periodo') and len(filtros['periodo']) == 2:
            data_inicio, data_fim = filtros['periodo']
            resumo_partes.append(f"Período: {data_inicio} a {data_fim}")
        
        if not resumo_partes:
            return "Todos os dados estão sendo exibidos (nenhum filtro aplicado)"
        
        return "Filtros aplicados: " + " | ".join(resumo_partes)
    
    def validar_filtros(self, filtros: dict) -> Tuple[bool, str]:
        """
        Valida se os filtros selecionados são válidos
        
        Args:
            filtros: Dicionário com os filtros selecionados
            
        Returns:
            Tupla com (é_válido, mensagem_erro)
        """
        # Verifica se o período está completo
        if filtros.get('periodo') and len(filtros['periodo']) != 2:
            return False, "Por favor, selecione um período completo (data de início e fim)"
        
        # Verifica se pelo menos um modelo está selecionado
        if not filtros.get('modelos'):
            return False, "Selecione pelo menos um modelo de transformador"
        
        # Verifica se pelo menos um status está selecionado
        if not filtros.get('status'):
            return False, "Selecione pelo menos um status de aprovação"
        
        return True, ""


def criar_filtros_rapidos(df: pd.DataFrame) -> dict:
    """
    Cria filtros rápidos na área principal
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        Dicionário com filtros rápidos selecionados
    """
    st.subheader("🚀 Filtros Rápidos")
    
    col1, col2, col3, col4 = st.columns(4)
    
    filtros_rapidos = {}
    
    with col1:
        if st.button("📊 Todos os Dados", help="Exibir todos os dados disponíveis"):
            filtros_rapidos['tipo'] = 'todos'
    
    with col2:
        if st.button("✅ Apenas Aprovados", help="Exibir apenas testes aprovados"):
            filtros_rapidos['tipo'] = 'aprovados'
    
    with col3:
        if st.button("❌ Apenas Reprovados", help="Exibir apenas testes reprovados"):
            filtros_rapidos['tipo'] = 'reprovados'
    
    with col4:
        if st.button("📅 Último Mês", help="Exibir dados do último mês"):
            filtros_rapidos['tipo'] = 'ultimo_mes'
    
    return filtros_rapidos


def aplicar_filtros_rapidos(df: pd.DataFrame, filtros_rapidos: dict) -> pd.DataFrame:
    """
    Aplica filtros rápidos ao DataFrame
    
    Args:
        df: DataFrame original
        filtros_rapidos: Filtros rápidos selecionados
        
    Returns:
        DataFrame filtrado
    """
    if not filtros_rapidos.get('tipo'):
        return df
    
    tipo_filtro = filtros_rapidos['tipo']
    
    if tipo_filtro == 'todos':
        return df
    elif tipo_filtro == 'aprovados':
        return df[df['Status_Aprovacao'] == 'Aprovado']
    elif tipo_filtro == 'reprovados':
        return df[df['Status_Aprovacao'] == 'Reprovado']
    elif tipo_filtro == 'ultimo_mes':
        data_limite = datetime.now() - pd.Timedelta(days=30)
        return df[df['Data_Teste'] >= data_limite]
    
    return df

