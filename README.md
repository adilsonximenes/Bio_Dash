# 📊 BioTrack - Nutrição & Evolução

Sistema de acompanhamento nutricional e registro de peso para dieta com ovos e frango.

## 🎯 Sobre o Projeto

BioTrack é um aplicativo web para registro diário de refeições e evolução de peso, desenvolvido para quem busca uma alimentação acessível e sustentável.

**Base alimentar:**
- 🥚 Café da manhã: 3 ovos + carboidrato
- 🍗 Almoço: Frango + vegetais + carboidrato
- 💪 Pós-treino: 3 ovos + carboidrato

## ✨ Funcionalidades

- ✅ Registro diário de check-in das refeições
- ⚖️ Histórico de peso com gráfico de evolução
- 📅 Calendário visual de adesão
- 🔐 Modo edição protegido por senha
- 📋 Cardápio semanal integrado
- 📊 Tabela nutricional completa
- 🥤 Sugestões de preparo rápido

## 🍽️ Cardápio Base

| Dia | Café | Almoço | Pós-Treino |
|-----|------|--------|-------------|
| Segunda | Pão Francês | Arroz + Chuchu/Cenoura | Banana + Aveia + Leite |
| Terça | Mamão Papaia | Arroz + Beterraba | Pão Francês |
| Quarta | Banana + Aveia | Batata Doce + Chuchu/Cenoura | Banana + Aveia + Leite |
| Quinta | Pão Francês | Arroz + Abobrinha | Pão Francês |
| Sexta | Mamão Papaia | Batata Doce + Beterraba | Banana + Aveia + Leite |
| Sábado | Banana + Aveia | Arroz + Abóbora | Pão Francês |
| Domingo | Pão Francês | Batata Inglesa + Chuchu/Cenoura | Mamão + Aveia + Leite |

## 🥗 Vegetais (sempre juntos)
- Chuchu + Cenoura (cozidos juntos para otimizar gás)

## 🛠️ Tecnologias

- Python 3.9+
- Streamlit
- Pandas
- Plotly

## 🚀 Como Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/adilsonximenes/Bio_Dash.git

# Entre na pasta
cd Bio_Dash

# Instale as dependências
pip install -r requirements.txt

# Execute o app
streamlit run app.py
```
## 🔐 Senha do Modo Admin
A senha para ativar o modo de edição é configurada via Streamlit Secrets:

No arquivo .streamlit/secrets.toml (local) ou nas configurações do Streamlit Cloud:

[admin]
senha = "sua_senha_aqui"

## 📁 Estrutura do Projeto
```bash
Bio_Dash/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências
├── .gitignore            # Arquivos ignorados
└── .streamlit/
    └── secrets.toml      # Configuração de senha (não versionado)
```
## 📊 Dados Armazenados
peso_diario.csv - Histórico de pesagens

checkin_diario.csv - Registro diário de refeições

(Os CSVs são criados automaticamente na primeira execução)

## 👩‍🍳 Orientações de Preparo
Chuchu + Cenoura: Cozinhar juntos, duram 3-4 dias na geladeira

Frango: Pode fazer quantidade maior, dura 3-4 dias

Ovos cozidos: Duram até 5 dias na geladeira

Shake rápido: Beterraba + banana + aveia + leite (bater no liquidificador)

## 📈 Projeção de Resultados
Taxa de perda ajustada por faixa de peso

Previsão para 30 e 60 dias

Data estimada para atingir a meta

## 🔗 Acesse o App
Clique aqui para acessar o BioTrack

Desenvolvido com ❤️ para uma nutrição acessível e sustentável.

---

### **4. Clique em "Commit new file"**

### **5. Seu README estará visível na página principal do repositório!**

---

## 📋 **RESUMO DOS ARQUIVOS NO SEU REPOSITÓRIO AGORA:**
```bash
Bio_Dash/
├── app.py ✅
├── requirements.txt ✅
├── .gitignore ✅
└── README.md ✅ (acabou de criar)
```
