# 🎯 Quick Start - Dashboard ICQA v2.0

## ⚡ Começar em 30 segundos

### 1. Abrir o App
```powershell
cd C:\Users\eoolvei\Desktop
python -m streamlit run dashboard_icqa_pro.py
```

### 2. Acessar no Navegador
```
http://localhost:8501
```

### 3. Carregar Dados
- Clique em cada caixa (SBC, CC, SRC)
- Selecione arquivo CSV

### 4. Explorar!
- **Dashboard**: Visualização geral
- **Análise**: Detalhes por processo
- **Histórico**: Download de dados
- **Configurações**: Editar metas

---

## 📊 Atalhos Principais

### Sidebar
| Opção | Função |
|-------|--------|
| 🔴 Dashboard | Visão geral com KPIs |
| 📈 Análise | Gráficos detalhados |
| 📁 Histórico | Download e exportação |
| ⚙️ Configurações | Editar metas |

### Dashboard
- Métricas em cards com status
- Gráficos comparativos automáticos
- Atualização em tempo real

### Análise
- 1️⃣ Selecione processo (dropdown)
- 2️⃣ Veja gráficos detalhados
- 3️⃣ Analise tabela de dados

---

## 💾 Salvar & Exportar

### Exportar para CSV
1. Vá para **📁 Histórico**
2. Clique em **📥 Baixar CSV**
3. Arquivo baixa automaticamente

### Dados Salvos Automaticamente
- Localização: `C:\Users\eoolvei\.icqa\data.db`
- Histórico de uploads
- Snapshots de performance

---

## ⚙️ Configurações Importantes

### Editar Metas
1. Vá para **⚙️ Configurações**
2. Abra o processo desejado
3. Ajuste valores:
   - **Meta BPH**: (ex: 100)
   - **Meta Qualidade**: (ex: 99.5%)
4. Clique **💾 Salvar**

### Padrões
- **SBC**: BPH ≥ 100 | Qualidade ≥ 99.5%
- **CC**: BPH ≥ 30 | Qualidade ≥ 99.8%
- **SRC**: BPH ≥ 100 | Qualidade ≥ 99.8%

---

## 🔄 Auto-Refresh

1. Abra **Sidebar**
2. Marque **🔄 Auto-refresh**
3. Dashboard atualiza a cada 30s
4. Ideal para monitoramento em tempo real

---

## 📊 Entender os Gráficos

### Comparativo BPH
- **Eixo X**: Semanas (S23, S24, etc)
- **Eixo Y**: BPH (valores)
- **Linhas**: Um processo por cor
- **Hover**: Ver valores exatos

### Distribuição
- **Caixas**: Min, Q1, Mediana, Q3, Max
- **Linha dentro**: Mediana
- **Ponto**: Média
- **Barras**: Desvio padrão

---

## ✅ Entender Status

### Cores de Status

**Verde (✅ OK)**
- BPH dentro da meta
- Qualidade dentro da meta

**Amarelo (🟡 Aviso)**
- BPH próximo da meta (90-100%)
- Qualidade próximo da meta

**Vermelho (❌ Crítico)**
- BPH abaixo da meta
- Qualidade abaixo da meta

---

## 🎯 Exemplo Prático

### Cenário 1: Revisar Performance Semanal
```
1. Abrir app → Dashboard
2. Ver métricas de SBC, CC, SRC
3. Verificar se % de OK está ≥ 90%
4. Se baixo → ir para Análise
5. Analisar qual semana caiu
6. Tomar ação
```

### Cenário 2: Comparar Processos
```
1. Ir para Análise
2. Ver gráfico comparativo
3. Qual processo está melhor?
4. Qual tem maior variação?
5. Exportar dados para relatório
```

### Cenário 3: Acompanhamento Diário
```
1. Ativar 🔄 Auto-refresh
2. Dashboard fica na tela
3. Valores atualizam automaticamente
4. Monitorar KPIs em tempo real
5. Reagir se valor crítico
```

---

## 🚨 Troubleshooting

### App não inicia?
```powershell
# Verificar se Streamlit está instalado
python -m pip list | findstr streamlit

# Reinstalar se necessário
python -m pip install streamlit --upgrade
```

### Erro ao carregar CSV?
- ✅ Verifique separador (`,` ou `;`)
- ✅ Verifique decimal (`.` ou `,`)
- ✅ Nomes de coluna: Semana, BPH, Qualidade

### Dados não aparecem?
- ✅ Recarregue a página (F5)
- ✅ Ative Auto-refresh
- ✅ Confirme carregamento do CSV

---

## 📞 Comandos Úteis

### Iniciar App
```powershell
python -m streamlit run dashboard_icqa_pro.py
```

### Com opções
```powershell
# Porta customizada
python -m streamlit run dashboard_icqa_pro.py --server.port 8080

# Logger nível debug
python -m streamlit run dashboard_icqa_pro.py --logger.level=debug
```

### Parar App
```
Ctrl + C
```

---

## 💡 Dicas Pro

1. **Exportar regularmente** para ter backup
2. **Configurar metas corretas** no início
3. **Ativar Auto-refresh** para acompanhamento live
4. **Analisar tendências** antes de tomar decisões
5. **Manter histórico** de uploads importante

---

## 🎓 Próximos Passos

1. ✅ Dominar Dashboard básico
2. ✅ Explorar Análise detalhada
3. ✅ Configurar metas personalizadas
4. ✅ Automatizar com Auto-refresh
5. ✅ Integrar com seu workflow

---

**Pronto para começar? Abra http://localhost:8501 agora! 🚀**
