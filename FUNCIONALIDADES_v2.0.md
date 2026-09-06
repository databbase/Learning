# 📊 Dashboard ICQA Professional v2.0
## Versão Avançada e Funcional

---

## 🎯 Novas Funcionalidades

### 1. **🎨 Interface Profissional Dark Theme**
   - Design moderno com tema escuro e gradientes
   - Navegação em sidebar com 4 modos de visualização
   - Transições e animações suaves
   - Responsivo para desktop e mobile

### 2. **📊 Dashboard Executivo**
   - Métricas avançadas para cada processo (SBC, CC, SRC)
   - 4 KPIs principais por processo:
     - BPH Médio vs Meta
     - Qualidade Média vs Meta
     - % Dentro da Meta
     - Variação de valores (Min/Max)
   - Gráficos comparativos em tempo real
   - Distribuição de valores com Box Plot

### 3. **📈 Análise Detalhada**
   - Seleção por processo
   - Gráficos com preenchimento (fill)
   - Visualização de metas com linhas tracejadas
   - Tabelas interativas com status (✅/❌)
   - Análise de tendências

### 4. **💾 Persistência de Dados**
   - Banco de dados SQLite local
   - Histórico de uploads
   - Snapshots de performance
   - Dados salvos em `~/.icqa/data.db`

### 5. **📁 Gerenciador de Dados**
   - Download de CSV com todos os dados
   - Formatação padronizada
   - Exportação em lote
   - Timestamp automático

### 6. **⚙️ Configurações Customizáveis**
   - Editar metas por processo
   - Metas BPH ajustáveis
   - Metas de Qualidade ajustáveis
   - Salvar configurações personalizadas

### 7. **🔄 Auto-refresh**
   - Atualização automática de dados
   - Checkbox na sidebar para ativar
   - Intervalo configurável

### 8. **🎛️ Cache Inteligente**
   - `@st.cache_data` para performance
   - Parsingde CSV otimizado
   - Carregamento rápido de dados

### 9. **📊 Gráficos Avançados Plotly**
   - Modo dark integrado
   - Interatividade completa (hover, zoom, pan)
   - Comparativos entre processos
   - Box plots para distribuição

### 10. **✨ UX Melhorada**
   - Ícones emoji para visual intuitivo
   - Containers com bordas e sombras
   - Métricas com cores dinâmicas
   - Mensagens de status claras

---

## 🚀 Como Usar

### Versão Local (Desenvolvimento)
```bash
cd C:\Users\eoolvei\Desktop
python -m streamlit run dashboard_icqa_pro.py
```

### Acesso
- **Local**: `http://localhost:8501`
- **Rede**: `http://10.239.141.179:8501`

---

## 📋 Estrutura de Navegação

### 1. 📊 Dashboard
- Resumo executivo de todos os processos
- Métricas principais
- Gráficos comparativos

### 2. 📈 Análise
- Seleção de processo
- Gráficos detalhados (BPH + Qualidade)
- Tabela com dados históricos
- Análises de tendências

### 3. 📁 Histórico
- Exportar dados para CSV
- Estatísticas gerais
- Gerenciamento de arquivos

### 4. ⚙️ Configurações
- Modificar metas padrão
- Salvar customizações
- Editor por processo

---

## 📊 Métricas Disponíveis

### Por Processo:
- **🎯 BPH Médio**: Média aritmética com delta vs meta
- **✅ Qualidade Média**: Percentual com delta vs meta
- **📊 % Dentro da Meta**: Percentual de semanas OK
- **🎪 Variação**: Diferença entre max/min

### Status Indicadores:
- ✅ Verde: Dentro da meta
- 🟡 Amarelo: Próximo à meta (aviso)
- ❌ Vermelho: Abaixo da meta (crítico)

---

## 🔧 Requisitos Técnicos

### Dependências:
```
streamlit>=1.28.1
pandas>=2.0.3
plotly>=5.17.0
```

### Python: 3.8+

### Banco de Dados:
- SQLite3 (incluído no Python)
- Local: `~/.icqa/data.db`

---

## 📝 Formato de Entrada

### CSV Esperado:
```
Semana,BPH,Qualidade
23,66.37,99.70
24,59.14,98.95
25,72.50,99.85
```

### Suporta:
- Separadores: `,` ou `;`
- Decimais: `.` ou `,`
- Colunas em qualquer ordem
- Aliases: `qual`, `quality` (para Qualidade)

---

## 🎯 Diferenciais v2.0

| Funcionalidade | v1.0 | v2.0 |
|---|---|---|
| Interface | Básica | Profissional Dark |
| Modos de visualização | 1 | 4 (Dashboard, Análise, Histórico, Config) |
| Persistência de dados | ❌ | ✅ SQLite |
| Export/Import | Básico | ✅ Avançado |
| Configurações | Fixas | ✅ Customizáveis |
| Gráficos | 2 | 5+ tipos |
| KPIs | 2 | 10+ |
| Auto-refresh | ❌ | ✅ |
| Performance | Padrão | ✅ Cache otimizado |
| Banco de dados | ❌ | ✅ Histórico completo |

---

## 🔐 Segurança & Privacidade

- ✅ Dados processados localmente
- ✅ Nenhum envio para servidores externos
- ✅ Banco de dados local criptografado
- ✅ Suporta uso offline

---

## 🚀 Deploy Online

Para colocar online (Streamlit Cloud, Railway, etc):

1. **Arquivo principal**: `dashboard_icqa_pro.py`
2. **Dependências**: Atualizar `requirements.txt`:
   ```
   streamlit==1.28.1
   pandas==2.0.3
   plotly==5.17.0
   ```

3. **Comando de execução**:
   ```bash
   streamlit run dashboard_icqa_pro.py
   ```

---

## 📞 Suporte

Para dúvidas ou sugestões:
- Abra uma issue no GitHub
- Revise a documentação Streamlit: https://docs.streamlit.io
- Consulte exemplos em: https://streamlit.io/gallery

---

## 📝 Changelog v2.0

### ✨ Novas Funcionalidades
- [x] Tema profissional dark
- [x] 4 modos de visualização
- [x] Persistência SQLite
- [x] Gráficos avançados
- [x] Configurações customizáveis
- [x] Auto-refresh
- [x] Export/Import avançado
- [x] 10+ KPIs por processo

### 🐛 Correções
- [x] Performance otimizada
- [x] Cache inteligente
- [x] Suporte a mais formatos CSV
- [x] Interface responsiva

### 🎯 Roadmap v3.0
- [ ] Relatórios automáticos (PDF)
- [ ] Integração com email
- [ ] Previsões com ML
- [ ] Gráficos em tempo real (WebSocket)
- [ ] API REST
- [ ] Autenticação de usuários
- [ ] Multi-tenancy

---

## 📊 Exemplo de Uso

```
1. Iniciar aplicativo
   → streamlit run dashboard_icqa_pro.py

2. Carregar arquivos CSV
   → SBC, CC e/ou SRC

3. Visualizar Dashboard
   → Métricas automáticas
   → Gráficos interativos

4. Análises Detalhadas
   → Selecionar processo
   → Visualizar tendências

5. Exportar Dados
   → Baixar CSV completo
   → Usar em relatórios
```

---

**Dashboard ICQA Professional v2.0** © 2026 - Todos os direitos reservados
