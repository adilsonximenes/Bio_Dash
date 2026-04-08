import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
import calendar

# ============================================
# CONFIGURAÇÕES DE SEGURANÇA
# ============================================

if 'modo_edicao' not in st.session_state:
    st.session_state.modo_edicao = False

def verificar_senha():
    """Verifica senha usando Streamlit Secrets"""
    with st.sidebar.expander("🔐 Acesso Admin"):
        senha = st.text_input("Senha:", type="password", key="senha_admin")
        
        # Tenta pegar a senha dos secrets
        try:
            SENHA_CORRETA = st.secrets["admin"]["senha"]
        except:
            # Fallback para teste local (NÃO use em produção!)
            SENHA_CORRETA = "bio2024"
            st.warning("⚠️ Usando senha padrão (modo local)")
        
        if st.button("Ativar Edição"):
            if senha == SENHA_CORRETA:
                st.session_state.modo_edicao = True
                st.success("Modo edição ativado")
                st.rerun()
            else:
                st.error("Senha incorreta")
        
        if st.session_state.modo_edicao:
            if st.button("Desativar Edição"):
                st.session_state.modo_edicao = False
                st.rerun()
            st.info("🔧 Modo EDIÇÃO ativo")

# ============================================
# DADOS DO USUÁRIO
# ============================================
ALTURA = 1.64
IDADE = 47
PESO_INICIAL = 85.8
PESO_META = 65.8

HOJE = datetime.now().strftime('%Y-%m-%d')

# ============================================
# CARDÁPIO
# ============================================
def get_cardapio_semanal():
    return pd.DataFrame({
        "Dia": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
        
        "🌅 Café (3 ovos)": [
            "+ Pão Francês", "+ Mamão Papaia", "+ Banana + Aveia",
            "+ Pão Francês", "+ Mamão Papaia", "+ Banana + Aveia", "+ Pão Francês"
        ],
        
        "🍽️ Almoço (Frango)": [
            "+ Arroz + Chuchu/Cenoura",
            "+ Arroz + Chuchu/Cenoura + Beterraba",
            "+ Batata Doce + Chuchu/Cenoura",
            "+ Arroz + Chuchu/Cenoura + Abobrinha",
            "+ Batata Doce + Chuchu/Cenoura + Beterraba",
            "+ Arroz + Chuchu/Cenoura + Abóbora",
            "+ Batata Inglesa + Chuchu/Cenoura"
        ],
        
        "💪 Pós-Treino (3 ovos)": [
            "+ Banana + Aveia + Leite", "+ Pão Francês", "+ Banana + Aveia + Leite",
            "+ Pão Francês", "+ Banana + Aveia + Leite", "+ Pão Francês", "+ Mamão Papaia + Aveia + Leite"
        ],
        
        "🥗 Vegetais fixos": ["Chuchu+Cenoura"] * 7,
        "🥕 Legume extra": ["-", "Beterraba", "-", "Abobrinha", "Beterraba", "Abóbora", "Batata Inglesa"]
    })

def get_tabela_nutricional():
    return pd.DataFrame({
        "Alimento / Porção": [
            "🥚 Ovos (3 unid)", "🍗 Frango grelhado (150g)", "🍚 Arroz branco (100g)",
            "🥔 Batata Doce (100g)", "🥔 Batata Inglesa (100g)", "🥒 Chuchu (100g)",
            "🥕 Cenoura (100g)", "🍠 Beterraba (unidade pequena)", "🥒 Abobrinha (100g)",
            "🎃 Abóbora (100g)", "🥖 Pão Francês (50g)", "🍌 Banana (1 unid)",
            "🥣 Aveia (2 colheres)", "🥛 Leite semidesnatado (200ml)", "🍈 Mamão Papaia (1 unid)"
        ],
        "Kcal": [210, 240, 130, 85, 80, 22, 35, 35, 18, 35, 150, 90, 100, 80, 120],
        "Proteína(g)": [18, 45, 2.5, 1.5, 2.0, 1.5, 1.0, 1.5, 1.5, 1.2, 4.5, 1.1, 4.0, 6.0, 1.5],
        "Carboidrato(g)": [1.5, 0, 28, 20, 18, 4.5, 8.0, 7.0, 3.5, 8.0, 28.5, 23, 17, 10, 30],
        "Gordura(g)": [15, 6, 0.2, 0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.2, 1.5, 0.3, 2.0, 2.0, 0.3]
    })

def get_orientacoes_preparo():
    return """
    ### 📋 Orientações de Preparo e Consumo
    
    **🥗 Vegetais (Chuchu + Cenoura):** Cozinhe juntos. Dura 3-4 dias na geladeira.
    
    **🥕 Legumes extras:** Beterraba (pequena), Abobrinha, Abóbora, Batata Inglesa.
    
    **🥤 Preparo rápido:** Beterraba + banana + aveia + leite (bater no liquidificador)
    
    **⏰ Validade:** Cozidos: 3-4 dias | Ovos cozidos: 5 dias | Frango: 3-4 dias
    """

# ============================================
# FUNÇÕES DE PERSISTÊNCIA
# ============================================
def carregar_dados():
    """Carrega dados de peso e check-in"""
    
    # Arquivo de peso
    if not os.path.exists('peso_diario.csv'):
        df_peso = pd.DataFrame({'Data': [HOJE], 'Peso': [PESO_INICIAL]})
        df_peso.to_csv('peso_diario.csv', index=False)
    else:
        df_peso = pd.read_csv('peso_diario.csv')
        df_peso['Data'] = pd.to_datetime(df_peso['Data'])
        df_peso = df_peso.sort_values('Data')
    
    # Arquivo de check-in
    colunas_checkin = ['Data', 'Refeicao', 'Status', 'Acucar', 'Timestamp']
    if not os.path.exists('checkin_diario.csv'):
        pd.DataFrame(columns=colunas_checkin).to_csv('checkin_diario.csv', index=False)
    
    df_checkin = pd.read_csv('checkin_diario.csv')
    for col in colunas_checkin:
        if col not in df_checkin.columns:
            df_checkin[col] = ''
    
    return df_peso, df_checkin

def salvar_peso(data_str, peso):
    """Salva ou atualiza peso em uma data específica"""
    df_peso, _ = carregar_dados()
    df_peso = df_peso[df_peso['Data'].dt.strftime('%Y-%m-%d') != data_str]
    novo = pd.DataFrame({'Data': [data_str], 'Peso': [peso]})
    novo['Data'] = pd.to_datetime(novo['Data'])
    df_peso = pd.concat([df_peso, novo], ignore_index=True)
    df_peso = df_peso.sort_values('Data')
    df_peso.to_csv('peso_diario.csv', index=False)

def excluir_peso(data_str):
    """Exclui um registro de peso específico"""
    df_peso, _ = carregar_dados()
    df_peso = df_peso[df_peso['Data'].dt.strftime('%Y-%m-%d') != data_str]
    df_peso.to_csv('peso_diario.csv', index=False)
    return len(df_peso)

def salvar_checkin(data_str, cafe, almoco, pos, acucar):
    """Salva check-in para uma data específica"""
    _, df_checkin = carregar_dados()
    df_checkin = df_checkin[df_checkin['Data'] != data_str]
    
    novos = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if cafe:
        novos.append({'Data': data_str, 'Refeicao': 'Café', 'Status': 'OK', 'Acucar': acucar, 'Timestamp': timestamp})
    if almoco:
        novos.append({'Data': data_str, 'Refeicao': 'Almoço', 'Status': 'OK', 'Acucar': acucar, 'Timestamp': timestamp})
    if pos:
        novos.append({'Data': data_str, 'Refeicao': 'Pós-Treino', 'Status': 'OK', 'Acucar': acucar, 'Timestamp': timestamp})
    
    if novos:
        df_checkin = pd.concat([df_checkin, pd.DataFrame(novos)], ignore_index=True)
    
    df_checkin.to_csv('checkin_diario.csv', index=False)
    return len(novos)

def listar_todos_pesos():
    """Retorna DataFrame com todos os pesos registrados"""
    df_peso, _ = carregar_dados()
    if not df_peso.empty:
        return df_peso.copy()
    return pd.DataFrame()

# ============================================
# FUNÇÕES DE CÁLCULO
# ============================================
def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def calcular_taxa_perda(peso_atual):
    if peso_atual > 80:
        return 0.080
    elif peso_atual > 75:
        return 0.070
    elif peso_atual > 70:
        return 0.060
    else:
        return 0.050

def calcular_proteina_diaria():
    return 81

# ============================================
# INTERFACE PRINCIPAL
# ============================================
def main():
    st.set_page_config(
        page_title="BioTrack - Nutrição & Evolução",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.title("📊 BioTrack - Nutrição & Evolução")
    st.caption("Registro alimentar e acompanhamento de peso")
    
    with st.sidebar:
        st.header("⚙️ Controle")
        verificar_senha()
        st.markdown("---")
        st.caption(f"📅 Hoje: {HOJE}")
        
        df_peso_side, df_checkin_side = carregar_dados()
        if not df_checkin_side.empty:
            st.caption(f"📝 Check-ins: {df_checkin_side['Data'].nunique()} dias")
        if not df_peso_side.empty:
            st.caption(f"⚖️ Pesagens: {len(df_peso_side)}")
    
    df_peso, df_checkin = carregar_dados()
    peso_atual = float(df_peso['Peso'].iloc[-1]) if not df_peso.empty else PESO_INICIAL
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        faltam = PESO_META - peso_atual
        delta = f"{faltam:+.1f} kg" if faltam != 0 else "Meta atingida"
        st.metric("Peso Atual", f"{peso_atual:.1f} kg", delta=delta)
    
    with col2:
        imc = calcular_imc(peso_atual, ALTURA)
        st.metric("IMC", f"{imc:.1f}")
    
    with col3:
        st.metric("Proteína Diária", f"{calcular_proteina_diaria()} g")
    
    with col4:
        if not df_checkin.empty:
            st.metric("Dias Registrados", f"{df_checkin['Data'].nunique()}")
        else:
            st.metric("Dias Registrados", "0")
    
    # Projeção
    st.markdown("---")
    st.subheader("📈 Projeção")
    
    taxa = calcular_taxa_perda(peso_atual)
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Em 30 dias", f"{peso_atual - (taxa * 30):.1f} kg")
    col_b.metric("Em 60 dias", f"{peso_atual - (taxa * 60):.1f} kg")
    
    if peso_atual > PESO_META:
        dias_meta = int((peso_atual - PESO_META) / taxa)
        data_meta = datetime.now() + timedelta(days=dias_meta)
        col_c.metric("Previsão da Meta", data_meta.strftime('%d/%m/%Y'))
    else:
        col_c.success("🎯 Meta alcançada!")
    
    # Check-in do dia
    st.markdown("---")
    st.subheader(f"📝 Check-in de Hoje - {HOJE}")
    
    with st.container(border=True):
        checks_hoje = df_checkin[df_checkin['Data'] == HOJE]['Refeicao'].tolist() if not df_checkin.empty else []
        
        col_q1, col_q2, col_q3, col_q4 = st.columns(4)
        
        cafe = col_q1.checkbox("🌅 Café da Manhã (3 ovos)", value="Café" in checks_hoje)
        almoco = col_q2.checkbox("🍽️ Almoço (Frango + vegetais)", value="Almoço" in checks_hoje)
        pos = col_q3.checkbox("💪 Pós-Treino (3 ovos)", value="Pós-Treino" in checks_hoje)
        
        acucar_hoje = False
        if not df_checkin.empty and HOJE in df_checkin['Data'].values:
            acucar_hoje = df_checkin[df_checkin['Data'] == HOJE]['Acucar'].iloc[0]
        
        acucar = col_q4.toggle("🍬 Consumiu açúcar?", value=acucar_hoje)
        
        if st.button("✅ Salvar Registro de Hoje", type="primary", use_container_width=True):
            salvar_checkin(HOJE, cafe, almoco, pos, acucar)
            st.success(f"Registro de {HOJE} salvo!")
            st.rerun()
    
    # Modo Edição
    if st.session_state.modo_edicao:
        st.markdown("---")
        st.warning("🔧 MODO EDIÇÃO ATIVO")
        
        # Gerenciar Pesos
        st.subheader("⚖️ Gerenciar Pesos Registrados")
        
        df_pesos_completos = listar_todos_pesos()
        
        if not df_pesos_completos.empty:
            for idx, row in df_pesos_completos.iterrows():
                data_reg = row['Data'].strftime('%Y-%m-%d')
                peso_reg = row['Peso']
                
                col_a, col_b, col_c, col_d = st.columns([3, 2, 1, 1])
                
                with col_a:
                    st.write(f"📅 **{data_reg}**")
                with col_b:
                    peso_edit = st.number_input(f"Peso", value=float(peso_reg), step=0.1, key=f"peso_edit_{idx}", label_visibility="collapsed")
                with col_c:
                    if st.button("✏️ Salvar", key=f"save_{idx}"):
                        salvar_peso(data_reg, peso_edit)
                        st.success(f"Peso de {data_reg} alterado")
                        st.rerun()
                with col_d:
                    if st.button("🗑️ Excluir", key=f"del_{idx}"):
                        excluir_peso(data_reg)
                        st.warning(f"Peso de {data_reg} removido")
                        st.rerun()
                st.divider()
        else:
            st.info("Nenhum peso registrado ainda")
        
        # Adicionar novo peso
        st.subheader("➕ Adicionar Novo Peso")
        
        with st.container(border=True):
            col_p1, col_p2, col_p3 = st.columns(3)
            
            with col_p1:
                nova_data = st.date_input("Data:", value=datetime.now(), key="nova_data_peso")
            with col_p2:
                novo_peso_valor = st.number_input("Peso (kg):", step=0.1, value=float(peso_atual), key="novo_peso_valor")
            with col_p3:
                if st.button("💾 Adicionar Peso", type="primary"):
                    data_str = nova_data.strftime('%Y-%m-%d')
                    salvar_peso(data_str, novo_peso_valor)
                    st.success(f"Peso registrado para {data_str}")
                    st.rerun()
        
        # Corrigir check-in
        st.markdown("---")
        st.subheader("📝 Corrigir Check-in de Dias Anteriores")
        
        with st.container(border=True):
            data_corrigir = st.date_input(
                "Selecione a data:", 
                value=datetime.now() - timedelta(days=1),
                max_value=datetime.now(),
                key="data_corrigir_checkin"
            )
            
            data_str = data_corrigir.strftime('%Y-%m-%d')
            
            checkins_exist = []
            acucar_exist = False
            
            if not df_checkin.empty:
                checkins_exist = df_checkin[df_checkin['Data'] == data_str]['Refeicao'].tolist()
                if data_str in df_checkin['Data'].values:
                    registros = df_checkin[df_checkin['Data'] == data_str]
                    if len(registros) > 0:
                        acucar_exist = registros['Acucar'].iloc[0]
            
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            
            cafe_retro = col_c1.checkbox("🌅 Café", value="Café" in checkins_exist)
            almoco_retro = col_c2.checkbox("🍽️ Almoço", value="Almoço" in checkins_exist)
            pos_retro = col_c3.checkbox("💪 Pós-Treino", value="Pós-Treino" in checkins_exist)
            acucar_retro = col_c4.checkbox("🍬 Açúcar", value=acucar_exist)
            
            if st.button("✅ Salvar Correção", use_container_width=True):
                salvar_checkin(data_str, cafe_retro, almoco_retro, pos_retro, acucar_retro)
                st.success(f"Check-in de {data_str} salvo!")
                st.rerun()
    
    # Gráfico
    st.markdown("---")
    st.subheader("📊 Histórico de Peso")
    
    if len(df_peso) > 0:
        fig = px.line(df_peso, x='Data', y='Peso', markers=True, 
                      title="Evolução do Peso",
                      labels={'Peso': 'Peso (kg)', 'Data': 'Data'})
        fig.add_hline(y=PESO_META, line_dash="dash", line_color="green", 
                      annotation_text=f"Meta: {PESO_META}kg")
        fig.update_layout(hovermode='x unified', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Cardápio
    st.markdown("---")
    st.subheader("📋 Cardápio Semanal")
    st.dataframe(get_cardapio_semanal(), use_container_width=True, hide_index=True)
    
    with st.expander("⚡ Preparo Rápido"):
        st.markdown("""
        - **3 ovos mexidos + banana** - Refeição rápida
        - **Leite + aveia + banana batido** - Lanche
        - **Beterraba + banana + aveia + leite** - Shake nutritivo
        """)
    
    with st.expander("📋 Orientações de Preparo"):
        st.markdown(get_orientacoes_preparo())
    
    with st.expander("📊 Tabela Nutricional"):
        st.dataframe(get_tabela_nutricional(), use_container_width=True, hide_index=True)
    
    # Rodapé
    st.markdown("---")
    
    if not df_checkin.empty:
        total_dias = df_checkin['Data'].nunique()
        total_refeicoes = len(df_checkin)
        st.caption(f"📊 Resumo: {total_dias} dias | {total_refeicoes} refeições")
    
    if len(df_peso) > 1:
        peso_ini = df_peso['Peso'].iloc[0]
        peso_fim = df_peso['Peso'].iloc[-1]
        st.caption(f"⚖️ Evolução: {peso_ini:.1f}kg → {peso_fim:.1f}kg")
    
    st.caption(f"🔄 Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

if __name__ == "__main__":
    main()