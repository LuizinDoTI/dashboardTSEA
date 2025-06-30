"""
Módulo para criação de visualizações e gráficos
Este módulo contém todas as funções para gerar gráficos do dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st
from config import GRAFICOS_CONFIG, METRICAS_CONFIG


class DashboardVisualizations:
    """Classe responsável pela criação de visualizações do dashboard"""
    
    def __init__(self):
        self.altura_padrao = GRAFICOS_CONFIG['altura_padrao']
        self.cores = GRAFICOS_CONFIG['cores_personalizadas']
        self.template = GRAFICOS_CONFIG['template']
    
    def grafico_eficiencia_tempo(self, df: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de eficiência ao longo do tempo
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Figura do Plotly
        """
        fig = px.line(
            df,
            x='Data_Teste',
            y='Eficiencia_Percentual',
            color='Modelo',
            title='Eficiência por Modelo ao Longo do Tempo',
            labels={
                'Data_Teste': 'Data do Teste',
                'Eficiencia_Percentual': 'Eficiência (%)',
                'Modelo': 'Modelo do Transformador'
            },
            template=self.template,
            height=self.altura_padrao
        )
        
        # Adiciona linha de referência para eficiência mínima
        fig.add_hline(
            y=METRICAS_CONFIG['eficiencia_minima'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Eficiência Mínima ({METRICAS_CONFIG['eficiencia_minima']}%)"
        )
        
        fig.update_layout(
            xaxis_title="Data do Teste",
            yaxis_title="Eficiência (%)",
            legend_title="Modelo"
        )
        
        return fig
    
    def grafico_perdas_temperatura(self, df: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de dispersão entre perdas e temperatura
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Figura do Plotly
        """
        fig = px.scatter(
            df,
            x='Perdas_Totais_kW',
            y='Elevacao_Temperatura_C',
            color='Modelo',
            size='Potencia_Nominal_MVA',
            hover_name='ID_Transformador',
            hover_data=['Status_Aprovacao', 'Tipo_Ensaio'],
            title='Relação entre Perdas Totais e Elevação de Temperatura',
            labels={
                'Perdas_Totais_kW': 'Perdas Totais (kW)',
                'Elevacao_Temperatura_C': 'Elevação de Temperatura (°C)',
                'Modelo': 'Modelo',
                'Potencia_Nominal_MVA': 'Potência (MVA)'
            },
            template=self.template,
            height=self.altura_padrao
        )
        
        # Adiciona linhas de referência
        fig.add_hline(
            y=METRICAS_CONFIG['temperatura_maxima'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Temperatura Máxima ({METRICAS_CONFIG['temperatura_maxima']}°C)"
        )
        
        fig.add_vline(
            x=METRICAS_CONFIG['perdas_maximas'],
            line_dash="dash",
            line_color="orange",
            annotation_text=f"Perdas Máximas ({METRICAS_CONFIG['perdas_maximas']} kW)"
        )
        
        return fig
    
    def grafico_distribuicao_modelos(self, df: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de pizza com distribuição de modelos
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Figura do Plotly
        """
        contagem_modelos = df['Modelo'].value_counts()
        
        fig = px.pie(
            values=contagem_modelos.values,
            names=contagem_modelos.index,
            title='Distribuição de Testes por Modelo',
            template=self.template,
            height=self.altura_padrao
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        return fig
    
    def grafico_aprovacao_por_modelo(self, df: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de barras com taxa de aprovação por modelo
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Figura do Plotly
        """
        # Calcula taxa de aprovação por modelo
        aprovacao_modelo = df.groupby(['Modelo', 'Status_Aprovacao']).size().unstack(fill_value=0)
        aprovacao_modelo['Total'] = aprovacao_modelo.sum(axis=1)
        aprovacao_modelo['Taxa_Aprovacao'] = (aprovacao_modelo.get('Aprovado', 0) / aprovacao_modelo['Total']) * 100
        
        fig = px.bar(
            x=aprovacao_modelo.index,
            y=aprovacao_modelo['Taxa_Aprovacao'],
            title='Taxa de Aprovação por Modelo',
            labels={
                'x': 'Modelo do Transformador',
                'y': 'Taxa de Aprovação (%)'
            },
            template=self.template,
            height=self.altura_padrao
        )
        
        # Adiciona linha de referência
        fig.add_hline(
            y=90,
            line_dash="dash",
            line_color="green",
            annotation_text="Meta: 90%"
        )
        
        fig.update_layout(
            xaxis_title="Modelo do Transformador",
            yaxis_title="Taxa de Aprovação (%)",
            showlegend=False
        )
        
        return fig
    
    def grafico_histograma_eficiencia(self, df: pd.DataFrame) -> go.Figure:
        """
        Cria histograma da distribuição de eficiência
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Figura do Plotly
        """
        fig = px.histogram(
            df,
            x='Eficiencia_Percentual',
            nbins=30,
            title='Distribuição da Eficiência dos Transformadores',
            labels={
                'Eficiencia_Percentual': 'Eficiência (%)',
                'count': 'Frequência'
            },
            template=self.template,
            height=self.altura_padrao
        )
        
        # Adiciona linha de referência para eficiência mínima
        fig.add_vline(
            x=METRICAS_CONFIG['eficiencia_minima'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Eficiência Mínima ({METRICAS_CONFIG['eficiencia_minima']}%)"
        )
        
        fig.update_layout(
            xaxis_title="Eficiência (%)",
            yaxis_title="Frequência",
            showlegend=False
        )
        
        return fig
    
    def grafico_boxplot_temperatura(self, df: pd.DataFrame) -> go.Figure:
        """
        Cria boxplot da temperatura por modelo
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Figura do Plotly
        """
        fig = px.box(
            df,
            x='Modelo',
            y='Elevacao_Temperatura_C',
            title='Distribuição da Elevação de Temperatura por Modelo',
            labels={
                'Modelo': 'Modelo do Transformador',
                'Elevacao_Temperatura_C': 'Elevação de Temperatura (°C)'
            },
            template=self.template,
            height=self.altura_padrao
        )
        
        # Adiciona linha de referência
        fig.add_hline(
            y=METRICAS_CONFIG['temperatura_maxima'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Temperatura Máxima ({METRICAS_CONFIG['temperatura_maxima']}°C)"
        )
        
        fig.update_layout(
            xaxis_title="Modelo do Transformador",
            yaxis_title="Elevação de Temperatura (°C)"
        )
        
        return fig
    
    def grafico_tendencia_mensal(self, df: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de tendência mensal de testes
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Figura do Plotly
        """
        # Agrupa por mês
        df_mensal = df.copy()
        df_mensal['Mes_Ano'] = df_mensal['Data_Teste'].dt.to_period('M')
        
        tendencia = df_mensal.groupby(['Mes_Ano', 'Status_Aprovacao']).size().unstack(fill_value=0)
        tendencia.index = tendencia.index.astype(str)
        
        fig = go.Figure()
        
        # Adiciona barras para aprovados e reprovados
        if 'Aprovado' in tendencia.columns:
            fig.add_trace(go.Bar(
                x=tendencia.index,
                y=tendencia['Aprovado'],
                name='Aprovado',
                marker_color='green'
            ))
        
        if 'Reprovado' in tendencia.columns:
            fig.add_trace(go.Bar(
                x=tendencia.index,
                y=tendencia['Reprovado'],
                name='Reprovado',
                marker_color='red'
            ))
        
        fig.update_layout(
            title='Tendência Mensal de Testes',
            xaxis_title='Mês/Ano',
            yaxis_title='Número de Testes',
            barmode='stack',
            template=self.template,
            height=self.altura_padrao
        )
        
        return fig
    
    def grafico_correlacao_potencia_perdas(self, df: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de correlação entre potência e perdas
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Figura do Plotly
        """
        fig = px.scatter(
            df,
            x='Potencia_Nominal_MVA',
            y='Perdas_Totais_kW',
            color='Status_Aprovacao',
            hover_name='ID_Transformador',
            hover_data=['Modelo', 'Eficiencia_Percentual'],
            title='Correlação entre Potência Nominal e Perdas Totais',
            labels={
                'Potencia_Nominal_MVA': 'Potência Nominal (MVA)',
                'Perdas_Totais_kW': 'Perdas Totais (kW)',
                'Status_Aprovacao': 'Status'
            },
            template=self.template,
            height=self.altura_padrao,
            color_discrete_map={'Aprovado': 'green', 'Reprovado': 'red'}
        )
        
        return fig


def criar_visualizacao(tipo_grafico: str, df: pd.DataFrame) -> go.Figure:
    """
    Função auxiliar para criar visualizações
    
    Args:
        tipo_grafico: Tipo do gráfico a ser criado
        df: DataFrame com os dados
        
    Returns:
        Figura do Plotly
    """
    viz = DashboardVisualizations()
    
    graficos_disponiveis = {
        'eficiencia_tempo': viz.grafico_eficiencia_tempo,
        'perdas_temperatura': viz.grafico_perdas_temperatura,
        'distribuicao_modelos': viz.grafico_distribuicao_modelos,
        'aprovacao_modelo': viz.grafico_aprovacao_por_modelo,
        'histograma_eficiencia': viz.grafico_histograma_eficiencia,
        'boxplot_temperatura': viz.grafico_boxplot_temperatura,
        'tendencia_mensal': viz.grafico_tendencia_mensal,
        'correlacao_potencia': viz.grafico_correlacao_potencia_perdas
    }
    
    if tipo_grafico in graficos_disponiveis:
        return graficos_disponiveis[tipo_grafico](df)
    else:
        st.error(f"Tipo de gráfico '{tipo_grafico}' não encontrado")
        return go.Figure()

