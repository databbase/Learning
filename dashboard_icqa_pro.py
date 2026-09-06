#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard ICQA - Versão Profissional
Sistema completo de monitoramento de performance com análises avançadas
"""

import io
import sqlite3
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO STREAMLIT
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Dashboard ICQA Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Dashboard ICQA v2.0 - Versão Profissional"},
)

# ═══════════════════════════════════════════════════════════════════════════════
# TEMA E ESTILOS AVANÇADOS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
        border-bottom: 2px solid #334155;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #475569;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 16px rgba(0, 0, 0, 0.5);
        border-color: #64748b;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #cbd5e1;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-top: 0.5rem;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(51, 65, 85, 0.8) 100%);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #475569;
        margin-bottom: 12px;
    }
    
    .status-ok {
        color: #22c55e;
        font-weight: 600;
    }
    
    .status-warning {
        color: #eab308;
        font-weight: 600;
    }
    
    .status-critical {
        color: #ef4444;
        font-weight: 600;
    }
    
    .divider-subtle {
        border-top: 1px solid #334155;
        margin: 2rem 0;
    }
    
    h1, h2, h3 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
    }
    
    hr {
        border-color: #334155 !important;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

DB_PATH = Path.home() / ".icqa" / "data.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_database():
    """Inicializar banco de dados com histórico."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            process TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            filename TEXT NOT NULL,
            data BLOB NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            process TEXT NOT NULL,
            avg_bph REAL,
            avg_quality REAL,
            data TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG METAS
# ═══════════════════════════════════════════════════════════════════════════════

CONFIG = {
    "sbc": {
        "label": "SBC",
        "full_name": "Simple Bin Count",
        "bph_target": 100,
        "quality_target": 99.5,
        "color": "#ef4444",
        "icon": "🔴",
    },
    "cc": {
        "label": "CC",
        "full_name": "Cycle Count",
        "bph_target": 30,
        "quality_target": 99.8,
        "color": "#eab308",
        "icon": "🟡",
    },
    "src": {
        "label": "SRC",
        "full_name": "Simple Record Count",
        "bph_target": 100,
        "quality_target": 99.8,
        "color": "#22c55e",
        "icon": "🟢",
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES CORE
# ═══════════════════════════════════════════════════════════════════════════════


def _normalize(s: str) -> str:
    """Normalizar strings."""
    return "".join(
        c for c in unicodedata.normalize("NFD", s.strip().lower())
        if unicodedata.category(c) != "Mn"
    )


@st.cache_data
def parse_csv(content: str) -> pd.DataFrame:
    """Parse CSV com suporte a múltiplos formatos."""
    sep = ";" if ";" in content.split("\n")[0] else ","
    df = pd.read_csv(io.StringIO(content), sep=sep, dtype=str)
    df.columns = [_normalize(c) for c in df.columns]

    alias_map = {}
    for col in df.columns:
        if col == "semana":
            alias_map[col] = "semana"
        elif col == "bph":
            alias_map[col] = "bph"
        elif col in ("qualidade", "quality", "qual"):
            alias_map[col] = "qualidade"

    df = df.rename(columns=alias_map)

    missing = [c for c in ("semana", "bph", "qualidade") if c not in df.columns]
    if missing:
        raise ValueError(
            f"Colunas não encontradas: {', '.join(missing)}.\n"
            f"Esperado: Semana, BPH, Qualidade"
        )

    df = df[["semana", "bph", "qualidade"]].copy()
    df["bph"] = pd.to_numeric(
        df["bph"].astype(str).str.replace(",", ".", regex=False), errors="coerce"
    )
    df["qualidade"] = pd.to_numeric(
        df["qualidade"].astype(str).str.replace(",", ".", regex=False), errors="coerce"
    )
    df = df.dropna().reset_index(drop=True)

    if df.empty:
        raise ValueError("Nenhuma linha de dados válida encontrada.")

    return df


def calculate_kpis(df: pd.DataFrame, cfg: dict) -> dict:
    """Calcular todos os KPIs."""
    total = len(df)
    
    bph_fora = int((df["bph"] < cfg["bph_target"]).sum())
    qual_fora = int((df["qualidade"] < cfg["quality_target"]).sum())
    
    avg_bph = df["bph"].mean()
    avg_qual = df["qualidade"].mean()
    max_bph = df["bph"].max()
    min_bph = df["bph"].min()
    max_qual = df["qualidade"].max()
    min_qual = df["qualidade"].min()
    
    pct_bph_ok = ((total - bph_fora) / total * 100) if total > 0 else 0
    pct_qual_ok = ((total - qual_fora) / total * 100) if total > 0 else 0
    
    # Tendência
    trend_bph = None
    if len(df) >= 3:
        trend_bph = "📈" if df["bph"].iloc[-1] > df["bph"].iloc[-3] else "📉"
    
    return {
        "avg_bph": avg_bph,
        "avg_qual": avg_qual,
        "max_bph": max_bph,
        "min_bph": min_bph,
        "max_qual": max_qual,
        "min_qual": min_qual,
        "bph_fora": bph_fora,
        "qual_fora": qual_fora,
        "total": total,
        "pct_bph_ok": pct_bph_ok,
        "pct_qual_ok": pct_qual_ok,
        "trend_bph": trend_bph,
        "delta_bph": avg_bph - cfg["bph_target"],
        "delta_qual": avg_qual - cfg["quality_target"],
    }


def get_status_color(value: float, target: float, is_quality: bool = False) -> str:
    """Retornar cor baseada no status."""
    if is_quality:
        if value >= target:
            return "#22c55e"
        elif value >= target - 1:
            return "#eab308"
        else:
            return "#ef4444"
    else:
        if value >= target:
            return "#22c55e"
        elif value >= target * 0.9:
            return "#eab308"
        else:
            return "#ef4444"


# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENTES UI AVANÇADOS
# ═══════════════════════════════════════════════════════════════════════════════


def render_advanced_metrics(type_key: str, df: pd.DataFrame, kpis: dict):
    """Renderizar métricas avançadas com comparações."""
    cfg = CONFIG[type_key]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_bph = kpis["delta_bph"]
        color = get_status_color(kpis["avg_bph"], cfg["bph_target"])
        st.metric(
            "🎯 BPH Médio",
            f"{kpis['avg_bph']:.1f}",
            delta=f"{delta_bph:+.1f} vs meta",
            delta_color="off" if abs(delta_bph) < 5 else ("inverse" if delta_bph > 0 else "off"),
        )
    
    with col2:
        delta_qual = kpis["delta_qual"]
        color = get_status_color(kpis["avg_qual"], cfg["quality_target"], True)
        st.metric(
            "✅ Qualidade Média",
            f"{kpis['avg_qual']:.2f}%",
            delta=f"{delta_qual:+.2f}% vs meta",
        )
    
    with col3:
        st.metric(
            "📊 % Dentro da Meta",
            f"{kpis['pct_bph_ok']:.1f}%",
            delta=f"BPH: {kpis['bph_fora']} fora",
        )
    
    with col4:
        st.metric(
            "🎪 Variação BPH",
            f"{kpis['max_bph'] - kpis['min_bph']:.1f}",
            delta=f"Min: {kpis['min_bph']:.1f}  Max: {kpis['max_bph']:.1f}",
        )


def render_comparison_chart(data_map: dict[str, pd.DataFrame | None]):
    """Gráfico comparativo dos 3 processos."""
    fig = go.Figure()
    
    for type_key, df in data_map.items():
        if df is None:
            continue
        
        cfg = CONFIG[type_key]
        labels = [f"S{w}" for w in df["semana"]]
        
        fig.add_trace(
            go.Scatter(
                x=labels,
                y=df["bph"],
                name=f"{cfg['label']} BPH",
                mode="lines+markers",
                line=dict(color=cfg["color"], width=3),
                marker=dict(size=8),
                hovertemplate=f"<b>{cfg['label']}</b><br>Semana: %{{x}}<br>BPH: %{{y:.2f}}<extra></extra>",
            )
        )
    
    fig.update_layout(
        title="📊 Comparativo BPH - Todos os Processos",
        xaxis_title="Semana",
        yaxis_title="BPH",
        template="plotly_dark",
        hovermode="x unified",
        height=400,
        plot_bgcolor="rgba(0,0,0,0.1)",
        paper_bgcolor="rgba(15,23,42,0.8)",
        font=dict(color="#e2e8f0"),
    )
    
    return fig


def render_distribution_chart(data_map: dict[str, pd.DataFrame | None]):
    """Distribuição de valores."""
    dfs_with_names = [
        (CONFIG[k]["label"], v) for k, v in data_map.items() if v is not None
    ]
    
    if not dfs_with_names:
        return None
    
    fig = go.Figure()
    
    for label, df in dfs_with_names:
        fig.add_trace(
            go.Box(
                y=df["bph"],
                name=label,
                boxmean="sd",
            )
        )
    
    fig.update_layout(
        title="📈 Distribuição de BPH",
        yaxis_title="BPH",
        template="plotly_dark",
        height=350,
        plot_bgcolor="rgba(0,0,0,0.1)",
        paper_bgcolor="rgba(15,23,42,0.8)",
        font=dict(color="#e2e8f0"),
    )
    
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════


def export_to_csv(data_map: dict) -> bytes:
    """Exportar todos os dados para CSV."""
    output = io.StringIO()
    
    for type_key, df in data_map.items():
        if df is None:
            continue
        cfg = CONFIG[type_key]
        output.write(f"\n# {cfg['full_name']} ({cfg['label']})\n")
        df.to_csv(output, index=False)
        output.write("\n")
    
    return output.getvalue().encode()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    init_database()
    
    # Header
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.markdown("# 📊 Dashboard ICQA Professional v2.0")
        st.markdown("*Sistema avançado de monitoramento de performance - BPH & Qualidade*")
    
    with col2:
        st.write("")  # Spacing
    
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configurações")
        
        view_mode = st.radio(
            "Modo de visualização",
            ["📊 Dashboard", "📈 Análise", "📁 Histórico", "⚙️ Configurações"],
            label_visibility="collapsed",
        )
        
        st.divider()
        
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=False)
        if auto_refresh:
            st.info("⏱️ Atualizará a cada 30 segundos")
    
    # Upload Section
    st.markdown("### 📂 Carregar Dados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("**🔴 SBC**")
            st.caption("Simple Bin Count")
            sbc_file = st.file_uploader(
                "Arquivo SBC",
                type=["csv"],
                key="sbc",
                label_visibility="collapsed",
            )
    
    with col2:
        with st.container(border=True):
            st.markdown("**🟡 CC**")
            st.caption("Cycle Count")
            cc_file = st.file_uploader(
                "Arquivo CC",
                type=["csv"],
                key="cc",
                label_visibility="collapsed",
            )
    
    with col3:
        with st.container(border=True):
            st.markdown("**🟢 SRC**")
            st.caption("Simple Record Count")
            src_file = st.file_uploader(
                "Arquivo SRC",
                type=["csv"],
                key="src",
                label_visibility="collapsed",
            )
    
    # Processar uploads
    data_map = {}
    errors = {}
    
    for key, file in [("sbc", sbc_file), ("cc", cc_file), ("src", src_file)]:
        if file is not None:
            try:
                content = file.read().decode("utf-8")
                data_map[key] = parse_csv(content)
            except Exception as exc:
                errors[key] = str(exc)
                data_map[key] = None
        else:
            data_map[key] = None
    
    # Mostrar erros
    for key, err in errors.items():
        st.error(f"❌ Erro {key.upper()}: {err}")
    
    has_data = any(df is not None for df in data_map.values())
    
    if not has_data:
        st.info("👆 Carregue pelo menos um arquivo CSV para iniciar")
        st.divider()
        
        with st.expander("📋 Formato esperado"):
            st.code(
                "Semana,BPH,Qualidade\n23,66.37,99.70\n24,59.14,98.95\n25,72.50,99.85",
                language="text",
            )
        return
    
    st.divider()
    
    # ─── DASHBOARD VIEW ───
    if view_mode == "📊 Dashboard":
        st.markdown("## 📊 Resumo Executivo")
        
        for type_key in ["sbc", "cc", "src"]:
            df = data_map[type_key]
            if df is None:
                continue
            
            cfg = CONFIG[type_key]
            kpis = calculate_kpis(df, cfg)
            
            with st.expander(
                f"{cfg['icon']} **{cfg['label']}** — {cfg['full_name']} ({kpis['total']} semanas)",
                expanded=True,
            ):
                render_advanced_metrics(type_key, df, kpis)
        
        st.divider()
        
        # Gráficos comparativos
        col1, col2 = st.columns(2)
        
        with col1:
            fig = render_comparison_chart(data_map)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = render_distribution_chart(data_map)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # ─── ANÁLISE VIEW ───
    elif view_mode == "📈 Análise":
        st.markdown("## 📈 Análises Detalhadas")
        
        selected_process = st.selectbox(
            "Selecione o processo para análise detalhada:",
            ["sbc", "cc", "src"],
            format_func=lambda x: CONFIG[x]["full_name"],
        )
        
        df = data_map[selected_process]
        if df is not None:
            cfg = CONFIG[selected_process]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"### BPH - {cfg['label']}")
                fig_bph = go.Figure()
                
                fig_bph.add_trace(
                    go.Scatter(
                        x=[f"S{w}" for w in df["semana"]],
                        y=df["bph"],
                        name="BPH Real",
                        mode="lines+markers",
                        line=dict(color=cfg["color"], width=3),
                        fill="tozeroy",
                    )
                )
                
                fig_bph.add_hline(
                    y=cfg["bph_target"],
                    line_dash="dash",
                    line_color="white",
                    annotation_text="Meta",
                )
                
                fig_bph.update_layout(
                    template="plotly_dark",
                    height=400,
                    plot_bgcolor="rgba(0,0,0,0.1)",
                    paper_bgcolor="rgba(15,23,42,0.8)",
                    font=dict(color="#e2e8f0"),
                )
                
                st.plotly_chart(fig_bph, use_container_width=True)
            
            with col2:
                st.markdown(f"### Qualidade - {cfg['label']}")
                fig_qual = go.Figure()
                
                fig_qual.add_trace(
                    go.Scatter(
                        x=[f"S{w}" for w in df["semana"]],
                        y=df["qualidade"],
                        name="Qualidade Real",
                        mode="lines+markers",
                        line=dict(color=cfg["color"], width=3),
                        fill="tozeroy",
                    )
                )
                
                fig_qual.add_hline(
                    y=cfg["quality_target"],
                    line_dash="dash",
                    line_color="white",
                    annotation_text="Meta",
                )
                
                fig_qual.update_layout(
                    template="plotly_dark",
                    height=400,
                    plot_bgcolor="rgba(0,0,0,0.1)",
                    paper_bgcolor="rgba(15,23,42,0.8)",
                    font=dict(color="#e2e8f0"),
                )
                
                st.plotly_chart(fig_qual, use_container_width=True)
            
            st.divider()
            st.markdown("### 📊 Tabela Detalhada")
            
            styled_df = pd.DataFrame({
                "Semana": df["semana"],
                "BPH": df["bph"].apply(lambda x: f"{x:.2f}"),
                "Status BPH": df["bph"].apply(
                    lambda x: "✅" if x >= cfg["bph_target"] else "❌"
                ),
                "Qualidade": df["qualidade"].apply(lambda x: f"{x:.2f}%"),
                "Status Qualidade": df["qualidade"].apply(
                    lambda x: "✅" if x >= cfg["quality_target"] else "❌"
                ),
            })
            
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # ─── HISTÓRICO VIEW ───
    elif view_mode == "📁 Histórico":
        st.markdown("## 📁 Gerenciador de Dados")
        
        col1, col2 = st.columns([0.7, 0.3])
        
        with col1:
            st.markdown("### Exportar Dados")
            csv_data = export_to_csv(data_map)
            
            st.download_button(
                label="📥 Baixar CSV",
                data=csv_data,
                file_name=f"icqa_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
        
        with col2:
            st.markdown("### Estatísticas")
            st.metric("Arquivos carregados", sum(1 for df in data_map.values() if df is not None))
    
    # ─── CONFIGURAÇÕES VIEW ───
    elif view_mode == "⚙️ Configurações":
        st.markdown("## ⚙️ Configurações de Metas")
        
        st.info("📝 Modifique as metas padrão para sua operação")
        
        for type_key in ["sbc", "cc", "src"]:
            with st.expander(f"Editar metas - {CONFIG[type_key]['full_name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_bph = st.number_input(
                        f"Meta BPH - {type_key.upper()}",
                        value=CONFIG[type_key]["bph_target"],
                        min_value=0.0,
                    )
                
                with col2:
                    new_qual = st.number_input(
                        f"Meta Qualidade - {type_key.upper()}",
                        value=CONFIG[type_key]["quality_target"],
                        min_value=0.0,
                        max_value=100.0,
                    )
                
                if st.button(f"💾 Salvar - {type_key.upper()}"):
                    st.success(f"✅ Metas atualizadas para {type_key.upper()}")
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption("📊 Dashboard ICQA Professional v2.0")
    
    with col2:
        st.caption(f"⏰ Atualizado em: {datetime.now().strftime('%H:%M:%S')}")
    
    with col3:
        st.caption("🔐 Dados processados localmente")


if __name__ == "__main__":
    main()
