#imports
import streamlit as st
from joblib import load
from pathlib import Path
import pandas as pd
import math
import plotly.graph_objects as go

model = load(Path('models/model.joblib')) # carrega o modelo

# função auxiliar para criar uma checkbox
def custom_checkbox(label, info, column):
    return 2 if column.checkbox(label, value=False, disabled=False, help=info) else 1

# função auxiliar para criar um gradiente que combina com as cores do streamlit (dark)
def generate_gradient():
    #gradient = ["#fffd80","#fff87e", "#fef47d", "#feef7b", "#fdea7a", "#fde578", "#fde177","#fcdc75", "#fcd774", "#fbd272", "#fbce71", "#fac96f", "#fac46e", "#fabf6c","#f9bb6a","#f9b669","#f8b167","#f8ac66","#f8a864","#f7a363", "#f79e61", "#f69960", "#f6955e", "#f6905d", "#f58b5b", "#f5865a", "#f48258","#f47d56","#f47855","#f37353","#f36f52","#f26a50","#f2654f","#f1604d","#f15c4c","#f1574a","#f05249","#f04d47", "#ef4946","#ef4444"]
    gradient = ["#06b6d4", "#00b4d7", "#00b3d9", "#00b1dc", "#00afde", "#00ade1", "#00abe3", "#00a9e5", "#00a7e7", "#00a5e8", "#11a2ea", "#22a0eb", "#2f9deb", "#3b9bec", "#4598ec", "#4f95ec", "#5992eb", "#628fea", "#6b8be9", "#7388e7", "#7c84e5", "#8481e2", "#8c7de0", "#9379dc", "#9a74d8", "#a170d4", "#a86cd0", "#ae67cb", "#b462c5", "#ba5dc0", "#bf58ba", "#c453b3", "#c84ead", "#cc49a6", "#d0439e", "#d33e97", "#d6388f", "#d83287", "#da2d7f", "#db2777"]
    step = 100/len(gradient)
    res = []
    i = 0
    for i in range(len(gradient)):
        start = i*step
        end = start + step
        res.append({
            'range': [start, end],
            'color': gradient[i]
        })
    #st.write(res)
    return res

change_gradient = '''
  <style>
    .css-1dp5vir {
      background: linear-gradient(90deg, rgba(6,182,212,1) 0%, rgba(219,39,119,1) 100%) !important;
    }
  </style>
'''

def main():
    
    # titulo da pagina web
    st.set_page_config(page_title="LungHealth", page_icon='👨‍⚕️', layout="centered")

    # alterar gradiente do streamlit (topo da pagina) para combinar com as cores do dashboard
    st.markdown(change_gradient, unsafe_allow_html=True)

    # descrição do app
    st.markdown('## LungHealth')
    st.markdown('### Cálculo de probabilidade de câncer pulmonar')
    st.markdown('Responda esse breve formulário para que possa ser realizado um cálculo da sua probabilidade de câncer pulmonar, **seja sincero** para obter o melhor resultado possível.')

    # dados do paciente
    entrada = {}

    # cria colunas para os inputs generalistas (idade, sexo, etc)
    col1,col2 = st.columns(2)
    entrada['GENDER'] = col1.selectbox(
        'Qual seu genero?',
        ('M', 'F'))

    entrada['AGE'] = col2.number_input('Idade',min_value=1, max_value=100, value=18, step=1, help='Insira sua idade')

    # cria colunas para os checkboxes
    col1,col2,col3 = st.columns(3)

    #col1
    col1.markdown('##### Estilo de vida')
    entrada['SMOKING'] = custom_checkbox('Fumante?', 'O fumante ativo é quem inala a fumaça do cigarro de maneira direta', col1)
    entrada['PEER_PRESSURE'] = custom_checkbox('Pressão grupal?', 'Você foi e/ou é influenciado por amigos para fumar, beber, etc...', col1)
    entrada['ALCOHOL CONSUMING'] = custom_checkbox('Consumo alcoólico?','Você consome alcool frequentemente?', col1) 

    #col2
    col2.markdown('##### Sintomas')
    entrada['YELLOW_FINGERS'] = custom_checkbox('Dedo/mão amarelada?', 'Se você possui dedos da mão, do pé, ou outras extremidades do corpo amareladas', col2) 
    entrada['FATIGUE'] = custom_checkbox('Fadiga?','A sensação de exaustão durante ou após as atividades cotidianas, com sensação de falta de energia', col2) 
    entrada['COUGHING'] = custom_checkbox('Tosse?','Costuma tossir com frequência?', col2) 
    entrada['SHORTNESS OF BREATH'] = custom_checkbox('Falta de ar?','A falta de ar é caracterizada pelo desconforto ou dificuldade para respirar', col2) 
    entrada['CHEST PAIN'] = custom_checkbox('Dor torácica?','Sensação de dor ou desconforto , localizada na região anterior do tórax (peito)', col2) 

    #col3
    col3.markdown('##### Enfermidades/Disturbios')
    entrada['ANXIETY'] = custom_checkbox('Ansiedade?', 'Emoção caracterizada por um estado desagradável de agitação interior, muitas vezes acompanhada de comportamento nervoso, como o de se embalar de trás para a frente', col3) 
    entrada['CHRONIC DISEASE'] = custom_checkbox('Doença Crônica?','Você possui alguma comorbidade cronica?', col3) 
    entrada['ALLERGY'] = custom_checkbox('Alergia?','Você possui alguma alergia?', col3) 
    entrada['WHEEZING'] = custom_checkbox('Pieira?','Som característico, rouco e abafado, provocado pela respiração difícil dos asmáticos e outros doentes do aparelho respiratório.',col3) 
    entrada['SWALLOWING DIFFICULTY'] = custom_checkbox('Disfagia?','Dificuldade de engolir alimentos e líquidos, a percepção de “arranhar”, ou ficar “presa” a comida ou bebida na passagem da garganta', col3) 

    # observações
    st.markdown('###### OBS: Essa aplicação usa aprendizado de máquina para prover um resultado, mas se você acredita que realmente possui câncer pulmonar, independente do resultado desse teste, **CONSULTE UM MÉDICO.**')

    # botão de submit
    if st.button("CALCULAR RESULTADOS", type="secondary"):

        x = pd.DataFrame({key: [value] for key, value in entrada.items()})

        resultado = model.predict_proba(x)
        probability = resultado[0][1] * 100


        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = probability,
            number = {"suffix": "%"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Seu resultado:", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#171717"},
                'bar': {'color': "#171717", 'thickness': 0.6},
                'bgcolor': "#8c7de0",
                'borderwidth': 4,
                'bordercolor': "#f5f5f5",
                'steps': 
                    generate_gradient()
            }))

        fig.update_layout(font = {'color': "#f5f5f5", 'family': "Arial"})

        st.write(fig)

        if probability <= 20:
            st.success('Suas chances de contrair câncer pulmonar são mínimas, não precisa se preocupar!')
        elif probability >= 80:
            st.error('Você possui chance alta de contrair câncer de pulmão. Se possível busque um médico')
        else:
            st.info('Você provavelmente não precisa se preocupar, mas caso possua algum sitoma grave e continue suspeitando da possibilidade, busque um médico.')

if __name__ == '__main__':
    main()