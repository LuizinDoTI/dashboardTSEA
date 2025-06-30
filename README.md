# Dashboard de Análise de Testes - TSEA Energia (Versão 2.0)

**Autor:** Luiz  
**Data da Versão:** 29 de Junho de 2025  
**Status:** Versão Modular e Educativa  

## 📋 Descrição

Este é um dashboard web interativo desenvolvido em Python com Streamlit, projetado especificamente para analisar resultados de testes de transformadores de potência da TSEA Energia. A versão 2.0 foi completamente refatorada para ser mais modular, educativa e fácil de modificar.

### 🎯 Objetivos

- **Centralizar** a análise de dados de ensaios de produção
- **Facilitar** a identificação de tendências e anomalias
- **Substituir** análises manuais demoradas de planilhas
- **Fornecer** visualizações interativas e intuitivas
- **Permitir** fácil modificação e extensão do código

## 🚀 Funcionalidades Principais

### 📊 Visualização de KPIs
- Métricas chave atualizadas dinamicamente
- Comparação com valores de referência
- Alertas automáticos para valores fora de especificação

### 🔍 Filtros Interativos
- **Filtros Básicos:** Modelo, Status, Tipo de Ensaio, Período
- **Filtros Avançados:** Faixas de eficiência, temperatura, perdas, potência
- **Filtros Rápidos:** Botões para seleções comuns
- **Histórico de Filtros:** Rastreamento das seleções anteriores

### 📈 Gráficos Dinâmicos
- **Eficiência vs Tempo:** Tendências por modelo
- **Perdas vs Temperatura:** Correlações e outliers
- **Distribuição por Modelo:** Análise de volume
- **Taxa de Aprovação:** Performance por modelo
- **Histogramas e BoxPlots:** Distribuições estatísticas
- **Tendências Mensais:** Evolução temporal

### 📋 Dados Detalhados
- Tabela interativa com ordenação
- Estatísticas descritivas
- Paginação configurável
- Exportação em CSV e Excel

### 📥 Exportação
- Download em formato CSV
- Download em Excel com formatação
- Dados filtrados conforme seleção

## 🏗️ Arquitetura Modular

O projeto foi estruturado em módulos independentes para facilitar manutenção e modificação:

```
dashboard_tsea_melhorado/
├── dashboard.py          # Aplicação principal
├── config.py            # Configurações centralizadas
├── data_generator.py    # Geração e carregamento de dados
├── filters.py           # Sistema de filtros
├── metrics.py           # Cálculo de métricas e KPIs
├── visualizations.py    # Criação de gráficos
├── utils.py             # Utilitários e funções auxiliares
├── requirements.txt     # Dependências do projeto
└── README.md           # Esta documentação
```

### 📁 Descrição dos Módulos

#### `config.py`
Centraliza todas as configurações do projeto:
- Configurações da aplicação Streamlit
- Parâmetros de dados (modelos, tipos de ensaio)
- Configurações de gráficos e métricas
- Textos da interface (facilita tradução)

#### `data_generator.py`
Responsável pela geração e carregamento de dados:
- Classe `DataGenerator` para dados fictícios
- Funções para carregar dados de Excel/CSV
- Correlações realísticas entre variáveis
- Cache otimizado com Streamlit

#### `filters.py`
Sistema completo de filtros:
- Classe `DashboardFilters` para filtros avançados
- Filtros rápidos para seleções comuns
- Validação de filtros
- Histórico de seleções

#### `metrics.py`
Cálculo e exibição de métricas:
- Classe `DashboardMetrics` para KPIs
- Métricas básicas e avançadas
- Comparação entre períodos
- Relatórios automáticos

#### `visualizations.py`
Criação de gráficos interativos:
- Classe `DashboardVisualizations`
- 8 tipos diferentes de gráficos
- Configurações personalizáveis
- Linhas de referência automáticas

#### `utils.py`
Funções auxiliares e utilitários:
- Exportação de dados (CSV/Excel)
- Validação de dados
- Gerenciamento de sessão
- Formatação e alertas

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**
- **Streamlit** - Framework web/dashboard
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica
- **Plotly Express** - Visualização interativa
- **OpenPyXL** - Manipulação de Excel
- **XlsxWriter** - Formatação de Excel

## 📦 Instalação e Execução

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone ou baixe o projeto:**
   ```bash
   # Se usando git
   git clone <url-do-repositorio>
   cd dashboard_tsea_melhorado
   
   # Ou extraia o arquivo ZIP na pasta desejada
   ```

2. **Crie um ambiente virtual (Recomendado):**
   ```bash
   # Crie o ambiente
   python -m venv venv
   
   # Ative o ambiente
   # Windows:
   venv\\Scripts\\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

### Executando o Dashboard

```bash
streamlit run dashboard.py
```

O dashboard será aberto automaticamente no seu navegador em `http://localhost:8501`

## 🎓 Guia de Modificação

### Como Adicionar Novos Modelos de Transformadores

1. **Edite o arquivo `config.py`:**
   ```python
   MODELOS_TRANSFORMADORES = [
       'TSEA-1000', 
       'TSEA-2500', 
       'TSEA-5000', 
       'TSEA-SPECIAL',
       'TSEA-7500',
       'TSEA-10000',
       'SEU-NOVO-MODELO'  # Adicione aqui
   ]
   ```

### Como Adicionar Novos Tipos de Gráficos

1. **Edite o arquivo `visualizations.py`:**
   ```python
   def seu_novo_grafico(self, df: pd.DataFrame) -> go.Figure:
       """Sua nova visualização"""
       fig = px.bar(df, x='coluna_x', y='coluna_y')
       return fig
   ```

2. **Adicione na função `criar_visualizacao`:**
   ```python
   graficos_disponiveis = {
       'eficiencia_tempo': viz.grafico_eficiencia_tempo,
       'seu_novo_grafico': viz.seu_novo_grafico,  # Adicione aqui
       # ... outros gráficos
   }
   ```

### Como Modificar Métricas de Referência

1. **Edite o arquivo `config.py`:**
   ```python
   METRICAS_CONFIG = {
       'eficiencia_minima': 98.5,  # Modifique este valor
       'temperatura_maxima': 65.0,  # Modifique este valor
       'perdas_maximas': 30.0      # Modifique este valor
   }
   ```

### Como Conectar Dados Reais

1. **Edite o arquivo `dashboard.py`, função `carregar_dados_dashboard`:**
   ```python
   def carregar_dados_dashboard() -> pd.DataFrame:
       try:
           # Para dados de Excel
           df = obter_dados(fonte='excel', caminho_arquivo='caminho/para/seu/arquivo.xlsx')
           
           # Para dados de CSV
           # df = obter_dados(fonte='csv', caminho_arquivo='caminho/para/seu/arquivo.csv')
           
           return df
       except Exception as e:
           st.error(f"Erro ao carregar dados: {str(e)}")
           return pd.DataFrame()
   ```

### Como Adicionar Novos Filtros

1. **Edite o arquivo `filters.py`, método `criar_filtros_sidebar`:**
   ```python
   # Adicione seu novo filtro
   filtros['seu_filtro'] = st.sidebar.selectbox(
       "Seu Novo Filtro:",
       options=['Opção 1', 'Opção 2'],
       help="Descrição do seu filtro"
   )
   ```

2. **Adicione a lógica no método `aplicar_filtros`:**
   ```python
   # Aplique seu filtro
   if filtros.get('seu_filtro'):
       df_filtrado = df_filtrado[df_filtrado['sua_coluna'] == filtros['seu_filtro']]
   ```

## 📊 Estrutura dos Dados

### Colunas Obrigatórias
- `ID_Transformador`: Identificador único
- `Modelo`: Modelo do transformador
- `Data_Teste`: Data do teste (formato datetime)
- `Tipo_Ensaio`: Tipo do ensaio realizado
- `Eficiencia_Percentual`: Eficiência em percentual
- `Elevacao_Temperatura_C`: Elevação de temperatura em °C
- `Perdas_Totais_kW`: Perdas totais em kW
- `Status_Aprovacao`: 'Aprovado' ou 'Reprovado'

### Colunas Opcionais
- `Tensao_Primaria_kV`: Tensão primária
- `Tensao_Secundaria_kV`: Tensão secundária
- `Potencia_Nominal_MVA`: Potência nominal
- `Corrente_Excitacao_A`: Corrente de excitação

### Formato de Arquivo Suportados
- **CSV**: Separado por vírgula, encoding UTF-8
- **Excel**: Formato .xlsx, dados na primeira planilha

## 🔧 Personalização Avançada

### Modificando Cores dos Gráficos

Edite `config.py`:
```python
GRAFICOS_CONFIG = {
    'cores_personalizadas': [
        '#1f77b4',  # Azul
        '#ff7f0e',  # Laranja
        '#2ca02c',  # Verde
        # Adicione suas cores em hexadecimal
    ]
}
```

### Modificando Textos da Interface

Edite `config.py`:
```python
TEXTOS_INTERFACE = {
    'titulo_principal': 'Seu Título Personalizado',
    'subtitulo': 'Sua descrição personalizada',
    # ... outros textos
}
```

### Adicionando Validações Personalizadas

Edite `utils.py`, método `validar_dataframe`:
```python
# Adicione suas validações
if 'sua_coluna' in df.columns:
    valores_invalidos = df[df['sua_coluna'] < 0]
    if len(valores_invalidos) > 0:
        resultado['erros'].append("Valores negativos encontrados em 'sua_coluna'")
```

## 🚀 Próximos Passos e Melhorias

### Funcionalidades Planejadas
- [ ] **Autenticação de usuários** para dados sensíveis
- [ ] **Conexão com banco de dados** SQL
- [ ] **Alertas automáticos** por email
- [ ] **Relatórios agendados** em PDF
- [ ] **API REST** para integração
- [ ] **Dashboard mobile** responsivo
- [ ] **Análise preditiva** com Machine Learning
- [ ] **Comparação entre plantas** diferentes

### Melhorias Técnicas
- [ ] **Testes unitários** automatizados
- [ ] **Documentação** com Sphinx
- [ ] **Deploy automatizado** com Docker
- [ ] **Monitoramento** de performance
- [ ] **Cache distribuído** com Redis
- [ ] **Logs estruturados** com ELK Stack

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
# Certifique-se de que o ambiente virtual está ativado
pip install -r requirements.txt
```

### Erro: "Data inválida"
- Verifique se a coluna `Data_Teste` está no formato correto
- Use `pd.to_datetime()` para converter strings em datas

### Dashboard não carrega
- Verifique se todas as dependências estão instaladas
- Execute `streamlit doctor` para diagnóstico

### Performance lenta
- Reduza o número de registros fictícios em `config.py`
- Use filtros para reduzir o volume de dados

## 📞 Suporte

Para dúvidas ou problemas:

1. **Verifique a documentação** neste README
2. **Consulte os comentários** no código
3. **Execute os exemplos** fornecidos
4. **Teste modificações** em ambiente isolado

## 📄 Licença

Apenas um teste visual e prático para ajudar colaboradores internos.

---

**Desenvolvido com ❤️ usando Python e Streamlit**  
**Versão 2.0 - Modular e Educativa**

