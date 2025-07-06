# Guia Completo de Modificação e Aprendizado - Dashboard TSEA

**Autor:** Luiz  
**Data:** 29 de Junho de 2025  
**Versão:** 1.0 - Guia Educativo  

## 📚 Índice

1. [Introdução ao Código](#introdução-ao-código)
2. [Estrutura Modular Explicada](#estrutura-modular-explicada)
3. [Como Modificar Cada Módulo](#como-modificar-cada-módulo)
4. [Exemplos Práticos de Modificação](#exemplos-práticos-de-modificação)
5. [Adicionando Novas Funcionalidades](#adicionando-novas-funcionalidades)
6. [Conectando Dados Reais](#conectando-dados-reais)
7. [Personalizando a Interface](#personalizando-a-interface)
8. [Debugging e Solução de Problemas](#debugging-e-solução-de-problemas)
9. [Boas Práticas de Desenvolvimento](#boas-práticas-de-desenvolvimento)
10. [Exercícios Práticos](#exercícios-práticos)

---

## 1. Introdução ao Código

### 1.1 Filosofia do Design

Este dashboard foi projetado seguindo princípios de **programação modular** e **separação de responsabilidades**. Cada arquivo tem uma função específica, facilitando a manutenção e modificação do código.

### 1.2 Conceitos Fundamentais

**Modularidade:** O código está dividido em módulos independentes que podem ser modificados sem afetar outros componentes.

**Configuração Centralizada:** Todas as configurações estão no arquivo `config.py`, permitindo mudanças rápidas sem editar múltiplos arquivos.

**Reutilização de Código:** Funções e classes são projetadas para serem reutilizadas em diferentes contextos.

**Documentação Inline:** Cada função possui docstrings explicando seu propósito e parâmetros.

### 1.3 Fluxo de Execução

```
dashboard.py (entrada) 
    ↓
config.py (configurações)
    ↓
data_generator.py (carrega dados)
    ↓
filters.py (aplica filtros)
    ↓
metrics.py (calcula KPIs)
    ↓
visualizations.py (cria gráficos)
    ↓
utils.py (funções auxiliares)
```

---

## 2. Estrutura Modular Explicada

### 2.1 config.py - Centro de Controle

Este arquivo é o **coração das configurações**. Aqui você pode modificar praticamente qualquer aspecto do dashboard sem tocar no código principal.

**Principais seções:**
- `APP_CONFIG`: Configurações do Streamlit
- `DATA_CONFIG`: Parâmetros de dados
- `MODELOS_TRANSFORMADORES`: Lista de modelos disponíveis
- `GRAFICOS_CONFIG`: Configurações visuais
- `TEXTOS_INTERFACE`: Todos os textos da interface

**Por que é importante:** Centralizar configurações facilita manutenção e permite mudanças rápidas.

### 2.2 data_generator.py - Fonte dos Dados

Responsável por gerar dados fictícios e carregar dados reais. A classe `DataGenerator` encapsula toda a lógica de criação de dados.

**Funcionalidades principais:**
- Geração de dados fictícios realísticos
- Carregamento de arquivos Excel/CSV
- Aplicação de correlações entre variáveis
- Validação de dados

**Por que é modular:** Permite trocar facilmente entre dados fictícios e reais.

### 2.3 filters.py - Sistema de Filtros

Contém toda a lógica de filtros do dashboard. A classe `DashboardFilters` gerencia filtros básicos e avançados.

**Componentes:**
- Filtros básicos (modelo, status, período)
- Filtros avançados (faixas numéricas)
- Filtros rápidos (botões de ação)
- Validação de filtros

**Por que é separado:** Facilita adicionar novos tipos de filtros sem modificar outras partes.

### 2.4 metrics.py - Cálculos e KPIs

Centraliza todos os cálculos de métricas e indicadores. A classe `DashboardMetrics` organiza diferentes tipos de métricas.

**Tipos de métricas:**
- Básicas (totais, médias, percentuais)
- Avançadas (estatísticas descritivas)
- Comparativas (entre períodos)
- Personalizadas (definidas pelo usuário)

**Por que é importante:** Separar cálculos facilita auditoria e modificação de fórmulas.

### 2.5 visualizations.py - Gráficos Interativos

Contém todas as funções para criar gráficos. A classe `DashboardVisualizations` organiza diferentes tipos de visualizações.

**Tipos de gráficos:**
- Linha (tendências temporais)
- Dispersão (correlações)
- Barras (comparações)
- Pizza (distribuições)
- Histograma (frequências)
- BoxPlot (estatísticas)

**Por que é modular:** Permite adicionar novos gráficos facilmente.

### 2.6 utils.py - Utilitários Gerais

Funções auxiliares que suportam todo o dashboard. Inclui exportação, validação, formatação e gerenciamento de sessão.

**Principais classes:**
- `DataExporter`: Exportação para CSV/Excel
- `DataValidator`: Validação de dados
- `SessionManager`: Gerenciamento de estado

**Por que é necessário:** Evita duplicação de código e centraliza funções comuns.

### 2.7 dashboard.py - Orquestrador Principal

O arquivo principal que coordena todos os módulos. Contém a função `main()` e organiza o fluxo da aplicação.

**Responsabilidades:**
- Configuração inicial
- Carregamento de dados
- Coordenação entre módulos
- Layout da interface
- Tratamento de erros

---

## 3. Como Modificar Cada Módulo

### 3.1 Modificando Configurações (config.py)

#### Adicionando Novos Modelos de Transformadores

```python
# Localização: config.py, linha ~25
MODELOS_TRANSFORMADORES = [
    'TSEA-1000', 
    'TSEA-2500', 
    'TSEA-5000', 
    'TSEA-SPECIAL',
    'TSEA-7500',
    'TSEA-10000',
    'SEU-NOVO-MODELO',  # Adicione aqui
    'OUTRO-MODELO'      # E aqui
]
```

**Impacto:** Novos modelos aparecerão automaticamente nos filtros e gráficos.

#### Modificando Limites de Especificação

```python
# Localização: config.py, linha ~60
METRICAS_CONFIG = {
    'eficiencia_minima': 98.5,  # Mude para 99.0 para ser mais rigoroso
    'temperatura_maxima': 65.0,  # Mude para 60.0 para ser mais restritivo
    'perdas_maximas': 30.0      # Ajuste conforme necessário
}
```

**Impacto:** Afeta alertas, cores dos gráficos e cálculos de conformidade.

#### Personalizando Cores dos Gráficos

```python
# Localização: config.py, linha ~50
GRAFICOS_CONFIG = {
    'cores_personalizadas': [
        '#FF6B6B',  # Vermelho coral
        '#4ECDC4',  # Turquesa
        '#45B7D1',  # Azul céu
        '#96CEB4',  # Verde menta
        '#FFEAA7',  # Amarelo suave
        '#DDA0DD'   # Roxo claro
    ]
}
```

**Impacto:** Todos os gráficos usarão as novas cores automaticamente.

### 3.2 Modificando Geração de Dados (data_generator.py)

#### Ajustando Distribuições de Dados

```python
# Localização: data_generator.py, método _gerar_eficiencia
def _gerar_eficiencia(self, num_registros: int) -> np.ndarray:
    # Mude os parâmetros da distribuição normal
    eficiencia = np.random.normal(99.5, 0.2, num_registros)  # Média mais alta, desvio menor
    eficiencia = np.clip(eficiencia, 98.5, 99.9)  # Ajuste os limites
    return np.round(eficiencia, 2)
```

**Impacto:** Dados gerados terão características diferentes.

#### Adicionando Nova Coluna de Dados

```python
# Localização: data_generator.py, método gerar_dados_ficticios
dados = {
    'ID_Transformador': [f'TR-{1000 + i:04d}' for i in range(num_registros)],
    # ... outras colunas existentes ...
    'Nova_Coluna': self._gerar_nova_coluna(num_registros),  # Adicione aqui
}

# Adicione o método correspondente
def _gerar_nova_coluna(self, num_registros: int) -> np.ndarray:
    """Gera valores para a nova coluna"""
    return np.random.uniform(10, 100, num_registros)
```

**Impacto:** Nova coluna estará disponível para filtros e gráficos.

### 3.3 Modificando Filtros (filters.py)

#### Adicionando Novo Filtro Simples

```python
# Localização: filters.py, método criar_filtros_sidebar
# Adicione após os filtros existentes

filtros['novo_filtro'] = st.sidebar.selectbox(
    "🆕 Seu Novo Filtro:",
    options=['Opção 1', 'Opção 2', 'Opção 3'],
    help="Descrição do que este filtro faz"
)
```

```python
# Localização: filters.py, método aplicar_filtros
# Adicione a lógica de aplicação

if filtros.get('novo_filtro'):
    df_filtrado = df_filtrado[df_filtrado['sua_coluna'] == filtros['novo_filtro']]
```

**Impacto:** Novo filtro aparecerá na sidebar e funcionará automaticamente.

#### Adicionando Filtro de Faixa Numérica

```python
# Localização: filters.py, dentro do expander "Filtros Avançados"

# Filtro por faixa de nova métrica
if 'Nova_Coluna' in self.df.columns:
    nova_min, nova_max = float(self.df['Nova_Coluna'].min()), float(self.df['Nova_Coluna'].max())
    filtros['nova_range'] = st.slider(
        "Faixa da Nova Métrica:",
        min_value=nova_min,
        max_value=nova_max,
        value=(nova_min, nova_max),
        step=0.1,
        help="Filtre por faixa da nova métrica"
    )
```

**Impacto:** Filtro de faixa numérica para a nova coluna.

### 3.4 Modificando Métricas (metrics.py)

#### Adicionando Nova Métrica Básica

```python
# Localização: metrics.py, método calcular_metricas_basicas
metricas = {
    'total_testes': len(self.df),
    # ... métricas existentes ...
    'nova_metrica': self.df['Nova_Coluna'].mean(),  # Adicione aqui
}
```

```python
# Localização: metrics.py, método exibir_metricas_principais
# Adicione nova coluna de métrica

with col_nova:  # Crie uma nova coluna
    st.metric(
        label="🆕 Nova Métrica",
        value=f"{metricas['nova_metrica']:.2f}",
        help="Descrição da nova métrica"
    )
```

**Impacto:** Nova métrica aparecerá no painel principal.

#### Criando Métrica Personalizada

```python
# Localização: metrics.py, adicione novo método na classe DashboardMetrics

def calcular_metrica_personalizada(self) -> float:
    """Calcula uma métrica específica do seu negócio"""
    if self.df.empty:
        return 0
    
    # Exemplo: percentual de testes com alta eficiência E baixa temperatura
    alta_efic = self.df['Eficiencia_Percentual'] > 99.0
    baixa_temp = self.df['Elevacao_Temperatura_C'] < 55.0
    
    testes_otimos = len(self.df[alta_efic & baixa_temp])
    return (testes_otimos / len(self.df)) * 100
```

**Impacto:** Métrica específica para suas necessidades de negócio.

### 3.5 Modificando Visualizações (visualizations.py)

#### Adicionando Novo Tipo de Gráfico

```python
# Localização: visualizations.py, adicione método na classe DashboardVisualizations

def grafico_novo_tipo(self, df: pd.DataFrame) -> go.Figure:
    """
    Cria um novo tipo de gráfico
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        Figura do Plotly
    """
    fig = px.bar(  # ou px.line, px.scatter, etc.
        df,
        x='coluna_x',
        y='coluna_y',
        color='Modelo',
        title='Título do Seu Novo Gráfico',
        labels={
            'coluna_x': 'Rótulo X',
            'coluna_y': 'Rótulo Y'
        },
        template=self.template,
        height=self.altura_padrao
    )
    
    return fig
```

```python
# Localização: visualizations.py, função criar_visualizacao
graficos_disponiveis = {
    'eficiencia_tempo': viz.grafico_eficiencia_tempo,
    # ... outros gráficos ...
    'novo_grafico': viz.grafico_novo_tipo,  # Adicione aqui
}
```

**Impacto:** Novo gráfico estará disponível no seletor de visualizações.

#### Personalizando Gráfico Existente

```python
# Localização: visualizations.py, modifique método existente
def grafico_eficiencia_tempo(self, df: pd.DataFrame) -> go.Figure:
    # ... código existente ...
    
    # Adicione personalização
    fig.update_layout(
        title_font_size=20,  # Título maior
        showlegend=True,     # Sempre mostrar legenda
        plot_bgcolor='lightgray'  # Fundo cinza claro
    )
    
    # Adicione anotação personalizada
    fig.add_annotation(
        text="Dados da TSEA Energia",
        xref="paper", yref="paper",
        x=1, y=1, xanchor='right', yanchor='top',
        showarrow=False
    )
    
    return fig
```

**Impacto:** Gráfico terá aparência personalizada.

---

## 4. Exemplos Práticos de Modificação

### 4.1 Exemplo 1: Adicionando Análise de Vibração

Vamos adicionar uma nova métrica de vibração aos transformadores.

#### Passo 1: Adicionar ao config.py

```python
# Em METRICAS_CONFIG, adicione:
'vibracao_maxima': 5.0,  # mm/s
```

#### Passo 2: Modificar data_generator.py

```python
# No método gerar_dados_ficticios, adicione:
'Vibracao_mm_s': self._gerar_vibracao(num_registros),

# Adicione o método:
def _gerar_vibracao(self, num_registros: int) -> np.ndarray:
    """Gera valores de vibração em mm/s"""
    vibracao = np.random.lognormal(1.0, 0.5, num_registros)
    vibracao = np.clip(vibracao, 0.5, 8.0)
    return np.round(vibracao, 2)
```

#### Passo 3: Adicionar filtro em filters.py

```python
# Em filtros avançados:
if 'Vibracao_mm_s' in self.df.columns:
    vib_min, vib_max = float(self.df['Vibracao_mm_s'].min()), float(self.df['Vibracao_mm_s'].max())
    filtros['vibracao_range'] = st.slider(
        "Faixa de Vibração (mm/s):",
        min_value=vib_min,
        max_value=vib_max,
        value=(vib_min, vib_max),
        step=0.1
    )
```

#### Passo 4: Adicionar métrica em metrics.py

```python
# Em calcular_metricas_basicas:
'vibracao_media': self.df['Vibracao_mm_s'].mean(),

# Em exibir_metricas_principais, adicione nova coluna:
with col_vibracao:
    vibracao = metricas['vibracao_media']
    delta_vib = METRICAS_CONFIG['vibracao_maxima'] - vibracao
    st.metric(
        label="📳 Vibração Média",
        value=f"{vibracao:.2f} mm/s",
        delta=f"{delta_vib:+.2f} mm/s",
        delta_color="normal" if delta_vib > 0 else "inverse"
    )
```

#### Passo 5: Adicionar gráfico em visualizations.py

```python
def grafico_vibracao_eficiencia(self, df: pd.DataFrame) -> go.Figure:
    """Correlação entre vibração e eficiência"""
    fig = px.scatter(
        df,
        x='Vibracao_mm_s',
        y='Eficiencia_Percentual',
        color='Status_Aprovacao',
        title='Correlação entre Vibração e Eficiência',
        labels={
            'Vibracao_mm_s': 'Vibração (mm/s)',
            'Eficiencia_Percentual': 'Eficiência (%)'
        }
    )
    
    fig.add_vline(
        x=METRICAS_CONFIG['vibracao_maxima'],
        line_dash="dash",
        line_color="red",
        annotation_text="Vibração Máxima"
    )
    
    return fig
```

**Resultado:** Sistema completo de análise de vibração integrado ao dashboard.

### 4.2 Exemplo 2: Sistema de Alertas Personalizados

Vamos criar um sistema que destaca transformadores com problemas múltiplos.

#### Passo 1: Criar função de análise em utils.py

```python
def analisar_problemas_multiplos(df: pd.DataFrame) -> pd.DataFrame:
    """Identifica transformadores com múltiplos problemas"""
    df_analise = df.copy()
    
    # Critérios de problema
    df_analise['problema_eficiencia'] = df_analise['Eficiencia_Percentual'] < METRICAS_CONFIG['eficiencia_minima']
    df_analise['problema_temperatura'] = df_analise['Elevacao_Temperatura_C'] > METRICAS_CONFIG['temperatura_maxima']
    df_analise['problema_perdas'] = df_analise['Perdas_Totais_kW'] > METRICAS_CONFIG['perdas_maximas']
    
    # Conta problemas
    df_analise['total_problemas'] = (
        df_analise['problema_eficiencia'].astype(int) +
        df_analise['problema_temperatura'].astype(int) +
        df_analise['problema_perdas'].astype(int)
    )
    
    # Classifica severidade
    df_analise['severidade'] = df_analise['total_problemas'].map({
        0: 'Normal',
        1: 'Atenção',
        2: 'Crítico',
        3: 'Emergência'
    })
    
    return df_analise
```

#### Passo 2: Integrar no dashboard principal

```python
# Em dashboard.py, após aplicar filtros:
df_com_analise = analisar_problemas_multiplos(df_filtrado)

# Exibir alertas
problemas_criticos = len(df_com_analise[df_com_analise['severidade'].isin(['Crítico', 'Emergência'])])
if problemas_criticos > 0:
    st.error(f"🚨 {problemas_criticos} transformadores com problemas críticos detectados!")
```

#### Passo 3: Criar visualização específica

```python
# Em visualizations.py:
def grafico_mapa_problemas(self, df: pd.DataFrame) -> go.Figure:
    """Mapa de calor dos problemas por modelo e período"""
    df_analise = analisar_problemas_multiplos(df)
    
    # Agrupa por modelo e mês
    df_analise['mes'] = df_analise['Data_Teste'].dt.to_period('M').astype(str)
    
    pivot = df_analise.groupby(['Modelo', 'mes'])['total_problemas'].mean().unstack(fill_value=0)
    
    fig = px.imshow(
        pivot.values,
        x=pivot.columns,
        y=pivot.index,
        title='Mapa de Problemas por Modelo e Período',
        labels={'color': 'Problemas Médios'},
        color_continuous_scale='Reds'
    )
    
    return fig
```

**Resultado:** Sistema inteligente de detecção e visualização de problemas.

---

## 5. Adicionando Novas Funcionalidades

### 5.1 Sistema de Relatórios Automáticos

#### Criando gerador de relatórios em utils.py

```python
class RelatorioGenerator:
    """Classe para gerar relatórios automáticos"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.metrics = DashboardMetrics(df)
    
    def gerar_relatorio_completo(self) -> str:
        """Gera relatório completo em Markdown"""
        relatorio = f"""
# Relatório de Análise - TSEA Energia
**Data de Geração:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
**Período Analisado:** {self.df['Data_Teste'].min().strftime('%d/%m/%Y')} a {self.df['Data_Teste'].max().strftime('%d/%m/%Y')}

## Resumo Executivo
{self._gerar_resumo_executivo()}

## Análise Detalhada
{self._gerar_analise_detalhada()}

## Recomendações
{self._gerar_recomendacoes()}
        """
        return relatorio
    
    def _gerar_resumo_executivo(self) -> str:
        metricas = self.metrics.calcular_metricas_basicas()
        return f"""
- **Total de testes realizados:** {metricas['total_testes']:,}
- **Taxa de aprovação:** {metricas['taxa_aprovacao']:.1f}%
- **Eficiência média:** {metricas['eficiencia_media']:.2f}%
- **Temperatura média:** {metricas['temperatura_media']:.1f}°C
        """
    
    def _gerar_analise_detalhada(self) -> str:
        # Implementar análise detalhada
        pass
    
    def _gerar_recomendacoes(self) -> str:
        # Implementar sistema de recomendações
        pass
```

### 5.2 Sistema de Comparação Temporal

#### Adicionando comparação entre períodos

```python
# Em metrics.py, adicione método:
def comparar_com_periodo_anterior(self, df_anterior: pd.DataFrame) -> Dict[str, Any]:
    """Compara métricas com período anterior"""
    metricas_atual = self.calcular_metricas_basicas()
    metricas_anterior = DashboardMetrics(df_anterior).calcular_metricas_basicas()
    
    comparacao = {}
    for metrica in metricas_atual:
        if metrica in metricas_anterior and metricas_anterior[metrica] != 0:
            variacao = ((metricas_atual[metrica] - metricas_anterior[metrica]) / metricas_anterior[metrica]) * 100
            comparacao[f'{metrica}_variacao'] = variacao
            comparacao[f'{metrica}_tendencia'] = 'melhora' if variacao > 0 else 'piora'
    
    return comparacao
```

### 5.3 Sistema de Exportação Avançada

#### Criando exportador com múltiplos formatos

```python
# Em utils.py, expanda DataExporter:
class DataExporterAvancado(DataExporter):
    """Exportador com funcionalidades avançadas"""
    
    @staticmethod
    def to_pdf_report(df: pd.DataFrame, metricas: Dict) -> bytes:
        """Gera relatório em PDF"""
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        # Implementar geração de PDF
        pass
    
    @staticmethod
    def to_powerpoint(df: pd.DataFrame, graficos: List) -> bytes:
        """Gera apresentação PowerPoint"""
        from pptx import Presentation
        
        # Implementar geração de PowerPoint
        pass
```

---

## 6. Conectando Dados Reais

### 6.1 Conectando com Excel/CSV

#### Modificando data_generator.py para dados reais

```python
def carregar_dados_excel_avancado(self, caminho_arquivo: str, planilha: str = None) -> pd.DataFrame:
    """Carrega dados de Excel com validação avançada"""
    try:
        # Carrega dados
        if planilha:
            df = pd.read_excel(caminho_arquivo, sheet_name=planilha)
        else:
            df = pd.read_excel(caminho_arquivo)
        
        # Validação de colunas obrigatórias
        colunas_obrigatorias = [
            'ID_Transformador', 'Modelo', 'Data_Teste', 
            'Eficiencia_Percentual', 'Elevacao_Temperatura_C'
        ]
        
        colunas_faltantes = [col for col in colunas_obrigatorias if col not in df.columns]
        if colunas_faltantes:
            raise ValueError(f"Colunas obrigatórias faltantes: {colunas_faltantes}")
        
        # Conversão de tipos
        df['Data_Teste'] = pd.to_datetime(df['Data_Teste'])
        df['Eficiencia_Percentual'] = pd.to_numeric(df['Eficiencia_Percentual'], errors='coerce')
        
        # Remove linhas com dados críticos faltantes
        df = df.dropna(subset=['ID_Transformador', 'Data_Teste'])
        
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {str(e)}")
        return pd.DataFrame()
```

### 6.2 Conectando com Banco de Dados

#### Adicionando suporte a SQL

```python
# Em data_generator.py, adicione:
import sqlite3
import sqlalchemy

def carregar_dados_sql(self, connection_string: str, query: str) -> pd.DataFrame:
    """Carrega dados de banco SQL"""
    try:
        engine = sqlalchemy.create_engine(connection_string)
        df = pd.read_sql(query, engine)
        
        # Validação e conversão de tipos
        if 'Data_Teste' in df.columns:
            df['Data_Teste'] = pd.to_datetime(df['Data_Teste'])
        
        return df
        
    except Exception as e:
        st.error(f"Erro ao conectar com banco: {str(e)}")
        return pd.DataFrame()

# Exemplo de uso:
# df = generator.carregar_dados_sql(
#     "sqlite:///dados_tsea.db",
#     "SELECT * FROM testes_transformadores WHERE data_teste >= '2024-01-01'"
# )
```

### 6.3 Interface para Upload de Arquivos

#### Adicionando upload na sidebar

```python
# Em dashboard.py, adicione na sidebar:
def criar_interface_upload():
    """Cria interface para upload de dados"""
    st.sidebar.markdown("### 📁 Carregar Dados")
    
    fonte_dados = st.sidebar.radio(
        "Fonte dos dados:",
        ["Dados Fictícios", "Upload de Arquivo", "Banco de Dados"]
    )
    
    if fonte_dados == "Upload de Arquivo":
        arquivo_upload = st.sidebar.file_uploader(
            "Escolha um arquivo:",
            type=['csv', 'xlsx', 'xls'],
            help="Formatos suportados: CSV, Excel"
        )
        
        if arquivo_upload:
            # Salva arquivo temporariamente
            with open(f"/tmp/{arquivo_upload.name}", "wb") as f:
                f.write(arquivo_upload.getbuffer())
            
            # Carrega dados
            if arquivo_upload.name.endswith('.csv'):
                df = obter_dados('csv', f"/tmp/{arquivo_upload.name}")
            else:
                df = obter_dados('excel', f"/tmp/{arquivo_upload.name}")
            
            return df
    
    elif fonte_dados == "Banco de Dados":
        st.sidebar.text_input("String de Conexão:")
        st.sidebar.text_area("Query SQL:")
        # Implementar conexão com banco
    
    return obter_dados('ficticios')
```

---

## 7. Personalizando a Interface

### 7.1 Temas e Estilos Personalizados

#### Criando tema escuro

```python
# Em utils.py, adicione:
def aplicar_tema_escuro():
    """Aplica tema escuro personalizado"""
    st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    .stSidebar {
        background-color: #2d2d2d;
    }
    
    .stMetric {
        background-color: #3d3d3d;
        border: 1px solid #555555;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stSelectbox > div > div {
        background-color: #3d3d3d;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)
```

### 7.2 Layout Responsivo

#### Criando layout adaptativo

```python
# Em dashboard.py, modifique a função de layout:
def criar_layout_responsivo():
    """Cria layout que se adapta ao tamanho da tela"""
    
    # Detecta tamanho da tela via JavaScript
    st.markdown("""
    <script>
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    if (width < 768) {
        // Layout mobile
        document.body.classList.add('mobile-layout');
    } else if (width < 1024) {
        // Layout tablet
        document.body.classList.add('tablet-layout');
    } else {
        // Layout desktop
        document.body.classList.add('desktop-layout');
    }
    </script>
    """, unsafe_allow_html=True)
    
    # CSS responsivo
    st.markdown("""
    <style>
    .mobile-layout .stColumns {
        flex-direction: column !important;
    }
    
    .tablet-layout .stMetric {
        font-size: 0.9em;
    }
    
    .desktop-layout .stMetric {
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)
```

### 7.3 Componentes Personalizados

#### Criando widget de progresso personalizado

```python
# Em utils.py, adicione:
def criar_barra_progresso_personalizada(valor: float, maximo: float, titulo: str):
    """Cria barra de progresso com estilo personalizado"""
    percentual = (valor / maximo) * 100
    
    # Determina cor baseada no valor
    if percentual >= 90:
        cor = "#28a745"  # Verde
    elif percentual >= 70:
        cor = "#ffc107"  # Amarelo
    else:
        cor = "#dc3545"  # Vermelho
    
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <h4>{titulo}</h4>
        <div style="background-color: #e9ecef; border-radius: 10px; height: 20px; overflow: hidden;">
            <div style="
                background-color: {cor}; 
                width: {percentual}%; 
                height: 100%; 
                border-radius: 10px;
                transition: width 0.3s ease;
            "></div>
        </div>
        <small>{valor:.1f} / {maximo:.1f} ({percentual:.1f}%)</small>
    </div>
    """, unsafe_allow_html=True)
```

---

## 8. Debugging e Solução de Problemas

### 8.1 Sistema de Logs

#### Implementando logging detalhado

```python
# Crie arquivo logging_config.py:
import logging
import streamlit as st
from datetime import datetime

def configurar_logging():
    """Configura sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('dashboard.log'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('dashboard_tsea')

# Em cada módulo, adicione:
logger = configurar_logging()

# Exemplo de uso:
def carregar_dados():
    logger.info("Iniciando carregamento de dados")
    try:
        df = obter_dados()
        logger.info(f"Dados carregados com sucesso: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {str(e)}")
        raise
```

### 8.2 Validação de Dados Avançada

#### Sistema de validação robusto

```python
# Em utils.py, expanda DataValidator:
class DataValidatorAvancado(DataValidator):
    """Validador com verificações avançadas"""
    
    @staticmethod
    def validar_consistencia_temporal(df: pd.DataFrame) -> Dict[str, Any]:
        """Valida consistência temporal dos dados"""
        resultado = {'valido': True, 'problemas': []}
        
        if 'Data_Teste' not in df.columns:
            return resultado
        
        # Verifica datas futuras
        datas_futuras = df[df['Data_Teste'] > datetime.now()]
        if len(datas_futuras) > 0:
            resultado['problemas'].append(f"{len(datas_futuras)} registros com datas futuras")
        
        # Verifica gaps temporais grandes
        df_sorted = df.sort_values('Data_Teste')
        gaps = df_sorted['Data_Teste'].diff()
        gaps_grandes = gaps[gaps > pd.Timedelta(days=90)]
        
        if len(gaps_grandes) > 0:
            resultado['problemas'].append(f"{len(gaps_grandes)} gaps temporais > 90 dias")
        
        return resultado
    
    @staticmethod
    def validar_valores_fisicos(df: pd.DataFrame) -> Dict[str, Any]:
        """Valida se valores estão dentro de limites físicos"""
        resultado = {'valido': True, 'problemas': []}
        
        # Eficiência não pode ser > 100%
        if 'Eficiencia_Percentual' in df.columns:
            efic_invalida = df[df['Eficiencia_Percentual'] > 100]
            if len(efic_invalida) > 0:
                resultado['problemas'].append(f"{len(efic_invalida)} registros com eficiência > 100%")
        
        # Temperatura não pode ser negativa
        if 'Elevacao_Temperatura_C' in df.columns:
            temp_invalida = df[df['Elevacao_Temperatura_C'] < 0]
            if len(temp_invalida) > 0:
                resultado['problemas'].append(f"{len(temp_invalida)} registros com temperatura negativa")
        
        return resultado
```

### 8.3 Tratamento de Erros

#### Sistema robusto de tratamento de erros

```python
# Em utils.py, adicione:
class ErrorHandler:
    """Classe para tratamento centralizado de erros"""
    
    @staticmethod
    def handle_data_error(func):
        """Decorator para tratamento de erros de dados"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except pd.errors.EmptyDataError:
                st.error("❌ Arquivo de dados está vazio")
                return pd.DataFrame()
            except pd.errors.ParserError as e:
                st.error(f"❌ Erro ao interpretar dados: {str(e)}")
                return pd.DataFrame()
            except FileNotFoundError:
                st.error("❌ Arquivo não encontrado")
                return pd.DataFrame()
            except Exception as e:
                st.error(f"❌ Erro inesperado: {str(e)}")
                logger.error(f"Erro em {func.__name__}: {str(e)}")
                return pd.DataFrame()
        return wrapper
    
    @staticmethod
    def handle_visualization_error(func):
        """Decorator para tratamento de erros de visualização"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                st.error(f"❌ Erro ao criar visualização: {str(e)}")
                logger.error(f"Erro em visualização {func.__name__}: {str(e)}")
                return go.Figure()  # Retorna gráfico vazio
        return wrapper

# Exemplo de uso:
@ErrorHandler.handle_data_error
def carregar_dados_com_tratamento():
    return pd.read_csv("dados.csv")
```

---

## 9. Boas Práticas de Desenvolvimento

### 9.1 Estrutura de Código

#### Princípios SOLID aplicados

**Single Responsibility Principle (SRP):**
- Cada classe tem uma responsabilidade única
- `DataGenerator` apenas gera dados
- `DashboardFilters` apenas gerencia filtros
- `DashboardMetrics` apenas calcula métricas

**Open/Closed Principle (OCP):**
- Classes abertas para extensão, fechadas para modificação
- Adicione novos gráficos sem modificar código existente
- Adicione novos filtros sem alterar lógica principal

**Dependency Inversion Principle (DIP):**
- Módulos dependem de abstrações, não de implementações
- Use interfaces para trocar fontes de dados facilmente

#### Convenções de nomenclatura

```python
# Classes: PascalCase
class DashboardMetrics:
    pass

# Funções e variáveis: snake_case
def calcular_metricas_basicas():
    total_testes = len(df)

# Constantes: UPPER_SNAKE_CASE
EFICIENCIA_MINIMA = 98.0

# Arquivos: snake_case
# data_generator.py
# dashboard_metrics.py
```

### 9.2 Documentação de Código

#### Docstrings padronizadas

```python
def calcular_metrica_complexa(df: pd.DataFrame, parametro: float) -> Dict[str, float]:
    """
    Calcula métrica complexa baseada em múltiplos fatores.
    
    Esta função implementa um algoritmo proprietário para calcular
    uma métrica que considera eficiência, temperatura e perdas
    de forma ponderada.
    
    Args:
        df (pd.DataFrame): DataFrame com dados dos testes.
            Deve conter colunas: 'Eficiencia_Percentual', 
            'Elevacao_Temperatura_C', 'Perdas_Totais_kW'
        parametro (float): Fator de ponderação entre 0.0 e 1.0.
            Valores maiores dão mais peso à eficiência.
    
    Returns:
        Dict[str, float]: Dicionário com métricas calculadas:
            - 'metrica_principal': Valor principal da métrica
            - 'confiabilidade': Nível de confiança (0-100)
            - 'tendencia': Tendência (-1 a 1)
    
    Raises:
        ValueError: Se o DataFrame estiver vazio ou parametro inválido
        KeyError: Se colunas obrigatórias estiverem ausentes
    
    Example:
        >>> df = pd.DataFrame({
        ...     'Eficiencia_Percentual': [99.1, 98.8, 99.3],
        ...     'Elevacao_Temperatura_C': [55.2, 58.1, 52.9],
        ...     'Perdas_Totais_kW': [12.5, 15.2, 11.8]
        ... })
        >>> resultado = calcular_metrica_complexa(df, 0.7)
        >>> print(resultado['metrica_principal'])
        85.6
    
    Note:
        Esta função usa cache interno para otimizar performance
        em DataFrames grandes (>1000 registros).
    """
    # Implementação da função...
```

### 9.3 Testes e Validação

#### Criando testes unitários

```python
# Crie arquivo test_dashboard.py:
import unittest
import pandas as pd
from data_generator import DataGenerator
from metrics import DashboardMetrics

class TestDataGenerator(unittest.TestCase):
    """Testes para o gerador de dados"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.generator = DataGenerator()
    
    def test_gerar_dados_ficticios(self):
        """Testa geração de dados fictícios"""
        df = self.generator.gerar_dados_ficticios(100)
        
        # Verifica se DataFrame não está vazio
        self.assertFalse(df.empty)
        
        # Verifica número de registros
        self.assertEqual(len(df), 100)
        
        # Verifica colunas obrigatórias
        colunas_esperadas = [
            'ID_Transformador', 'Modelo', 'Data_Teste',
            'Eficiencia_Percentual', 'Elevacao_Temperatura_C'
        ]
        for coluna in colunas_esperadas:
            self.assertIn(coluna, df.columns)
        
        # Verifica tipos de dados
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['Data_Teste']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['Eficiencia_Percentual']))
    
    def test_eficiencia_dentro_limites(self):
        """Testa se eficiência está dentro dos limites"""
        df = self.generator.gerar_dados_ficticios(100)
        
        # Eficiência deve estar entre 98% e 100%
        self.assertTrue((df['Eficiencia_Percentual'] >= 98.0).all())
        self.assertTrue((df['Eficiencia_Percentual'] <= 100.0).all())

class TestDashboardMetrics(unittest.TestCase):
    """Testes para métricas do dashboard"""
    
    def setUp(self):
        """Configuração inicial"""
        # Cria DataFrame de teste
        self.df_teste = pd.DataFrame({
            'Eficiencia_Percentual': [99.1, 98.8, 99.3, 98.5],
            'Status_Aprovacao': ['Aprovado', 'Aprovado', 'Aprovado', 'Reprovado'],
            'Elevacao_Temperatura_C': [55.2, 58.1, 52.9, 67.5],
            'Perdas_Totais_kW': [12.5, 15.2, 11.8, 18.9]
        })
        self.metrics = DashboardMetrics(self.df_teste)
    
    def test_calcular_metricas_basicas(self):
        """Testa cálculo de métricas básicas"""
        metricas = self.metrics.calcular_metricas_basicas()
        
        # Verifica se todas as métricas estão presentes
        self.assertIn('total_testes', metricas)
        self.assertIn('eficiencia_media', metricas)
        self.assertIn('taxa_aprovacao', metricas)
        
        # Verifica valores calculados
        self.assertEqual(metricas['total_testes'], 4)
        self.assertAlmostEqual(metricas['eficiencia_media'], 98.925, places=2)
        self.assertEqual(metricas['taxa_aprovacao'], 75.0)

# Para executar os testes:
if __name__ == '__main__':
    unittest.main()
```

### 9.4 Performance e Otimização

#### Técnicas de otimização

```python
# Em data_generator.py, use cache eficientemente:
@st.cache_data(ttl=3600)  # Cache por 1 hora
def obter_dados_com_cache(fonte: str, **kwargs) -> pd.DataFrame:
    """Versão com cache otimizado"""
    return obter_dados(fonte, **kwargs)

# Em visualizations.py, otimize gráficos grandes:
def otimizar_dados_para_grafico(df: pd.DataFrame, max_pontos: int = 1000) -> pd.DataFrame:
    """Reduz dados para melhorar performance de gráficos"""
    if len(df) <= max_pontos:
        return df
    
    # Amostragem estratificada por modelo
    df_otimizado = pd.DataFrame()
    for modelo in df['Modelo'].unique():
        df_modelo = df[df['Modelo'] == modelo]
        n_amostras = max(1, max_pontos // len(df['Modelo'].unique()))
        df_amostra = df_modelo.sample(min(len(df_modelo), n_amostras))
        df_otimizado = pd.concat([df_otimizado, df_amostra])
    
    return df_otimizado

# Em utils.py, use processamento assíncrono:
import asyncio
import concurrent.futures

async def processar_dados_async(df: pd.DataFrame) -> Dict[str, Any]:
    """Processa dados de forma assíncrona"""
    loop = asyncio.get_event_loop()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Executa cálculos em paralelo
        future_metricas = loop.run_in_executor(executor, calcular_metricas, df)
        future_validacao = loop.run_in_executor(executor, validar_dados, df)
        
        # Aguarda resultados
        metricas = await future_metricas
        validacao = await future_validacao
    
    return {'metricas': metricas, 'validacao': validacao}
```

---

## 10. Exercícios Práticos

### 10.1 Exercício Básico: Novo Modelo

**Objetivo:** Adicionar suporte para um novo modelo de transformador.

**Passos:**
1. Adicione "TSEA-15000" à lista de modelos em `config.py`
2. Modifique a probabilidade de geração em `data_generator.py`
3. Teste o dashboard e verifique se o novo modelo aparece nos filtros
4. Crie um gráfico específico para comparar este modelo com outros

**Solução esperada:**
- Novo modelo visível em todos os filtros
- Dados gerados incluem o novo modelo
- Gráficos mostram o novo modelo corretamente

### 10.2 Exercício Intermediário: Nova Métrica

**Objetivo:** Implementar análise de "Fator de Potência".

**Passos:**
1. Adicione coluna `Fator_Potencia` ao gerador de dados
2. Crie filtro para faixa de fator de potência
3. Adicione métrica de fator de potência médio
4. Crie gráfico correlacionando fator de potência com eficiência
5. Adicione alertas para fator de potência baixo

**Dicas:**
- Fator de potência varia entre 0.8 e 1.0
- Valores abaixo de 0.9 devem gerar alerta
- Use distribuição normal com média 0.95

### 10.3 Exercício Avançado: Sistema de Predição

**Objetivo:** Implementar predição simples de falhas.

**Passos:**
1. Crie função que identifica padrões de degradação
2. Implemente algoritmo simples de predição (regressão linear)
3. Adicione visualização de tendências futuras
4. Crie alertas preditivos
5. Adicione interface para configurar parâmetros de predição

**Conceitos envolvidos:**
- Análise de séries temporais
- Regressão linear
- Extrapolação de tendências
- Intervalos de confiança

### 10.4 Exercício Expert: Dashboard Multi-Planta

**Objetivo:** Expandir para suportar múltiplas plantas industriais.

**Passos:**
1. Modifique estrutura de dados para incluir "Planta"
2. Adicione filtros por planta
3. Crie comparações entre plantas
4. Implemente ranking de performance
5. Adicione mapas geográficos (se aplicável)

**Desafios:**
- Manter performance com mais dados
- Interface intuitiva para múltiplas plantas
- Comparações justas entre plantas diferentes
- Agregações corretas por planta

---

## 📝 Conclusão

Este guia fornece uma base sólida para entender, modificar e expandir o dashboard TSEA. A arquitetura modular permite que você:

1. **Aprenda gradualmente:** Comece com modificações simples e evolua para funcionalidades complexas
2. **Modifique com segurança:** Cada módulo é independente, reduzindo riscos
3. **Expanda facilmente:** Adicione novas funcionalidades sem quebrar o existente
4. **Mantenha qualidade:** Siga as boas práticas documentadas

### Próximos Passos Recomendados

1. **Familiarize-se com o código:** Execute o dashboard e explore cada módulo
2. **Faça modificações simples:** Comece alterando cores e textos
3. **Adicione funcionalidades:** Implemente uma nova métrica ou gráfico
4. **Conecte dados reais:** Substitua dados fictícios pelos seus dados
5. **Otimize performance:** Implemente melhorias conforme necessário

### Recursos Adicionais

- **Documentação Streamlit:** https://docs.streamlit.io/
- **Documentação Plotly:** https://plotly.com/python/
- **Documentação Pandas:** https://pandas.pydata.org/docs/
- **Boas práticas Python:** https://pep8.org/

### Suporte Contínuo

Lembre-se de que este é um projeto vivo. Continue experimentando, aprendendo e melhorando. A modularidade do código facilita a evolução contínua do sistema.


