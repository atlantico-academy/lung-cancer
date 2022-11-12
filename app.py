import streamlit as st
from joblib import load
from pathlib import Path
import pandas as pd
import math
import plotly.graph_objects as go

model = load(Path('models/model.joblib'))
convert = lambda x: 'Sim' if x == 2 else 'Não'
#st.set_page_config(layout="wide")


st.markdown('# LungHealth')
st.markdown('### Cálculo de probabilidade de câncer pulmonar')
st.markdown('Responda esse breve formulário para que possa ser realizado um cálculo da sua probabilidade de câncer pulmonar, **seja sincero** para obter o melhor resultado possível.')
st.markdown('---')

entrada = {}
col1,col2 = st.columns(2)

entrada['GENDER'] = col1.selectbox(
    'Qual seu genero?',
    ('M', 'F'))

entrada['AGE'] = col2.number_input('Idade',min_value=1, max_value=100, value=18, step=1, help='Insira sua idade')

col1,col2,col3 = st.columns(3)

col1.markdown('##### Estilo de vida')
col2.markdown('##### Sintomas')
col3.markdown('##### Enfermidades/Disturbios')

entrada['SMOKING'] = 2 if col1.checkbox('Fumante?', value=False, disabled=False, help='O fumante ativo é quem inala a fumaça do cigarro de maneira direta') else 1

entrada['YELLOW_FINGERS'] = 2 if col2.checkbox('Dedo/mão amarelada?', value=False, disabled=False, help='Se você possui dedos da mão, do pé, ou outras extremidades do corpo amareladas') else 1

entrada['ANXIETY'] = 2 if col3.checkbox('Ansiedade?', value=False, disabled=False, help='Emoção caracterizada por um estado desagradável de agitação interior, muitas vezes acompanhada de comportamento nervoso, como o de se embalar de trás para a frente') else 1

entrada['PEER_PRESSURE'] = 2 if col1.checkbox('Pressão grupal?', value=False, disabled=False, help='Você foi e/ou é influenciado por amigos para fumar, beber, etc...') else 1

entrada['CHRONIC DISEASE'] = 2 if col3.checkbox('Doença Crônica?', value=False, disabled=False, help='Você possui alguma comorbidade cronica?') else 1

entrada['FATIGUE'] = 2 if col2.checkbox('Fadiga?', value=False, disabled=False, help='A sensação de exaustão durante ou após as atividades cotidianas, com sensação de falta de energia') else 1

entrada['ALLERGY'] = 2 if col3.checkbox('Alergia?', value=False, disabled=False, help='Você possui alguma alergia?') else 1

entrada['WHEEZING'] = 2 if col2.checkbox('Pieira?', value=False, disabled=False, help='Som característico, rouco e abafado, provocado pela respiração difícil dos asmáticos e outros doentes do aparelho respiratório.') else 1

entrada['ALCOHOL CONSUMING'] = 2 if col1.checkbox('Consumo alcoólico?', value=False, disabled=False, help='Você consome alcool frequentemente?') else 1

entrada['COUGHING'] = 2 if col2.checkbox('Tosse?', value=False, disabled=False, help='Costuma tossir com frequência?') else 1

entrada['SHORTNESS OF BREATH'] = 2 if col3.checkbox('Falta de ar?', value=False, disabled=False, help='A falta de ar é caracterizada pelo desconforto ou dificuldade para respirar') else 1

entrada['SWALLOWING DIFFICULTY'] = 2 if col3.checkbox('Disfagia?', value=False, disabled=False, help='Dificuldade de engolir alimentos e líquidos, a percepção de “arranhar”, ou ficar “presa” a comida ou bebida na passagem da garganta') else 1

entrada['CHEST PAIN'] = 2 if col2.checkbox('Dor torácica?', value=False, disabled=False, help='Sensação de dor ou desconforto , localizada na região anterior do tórax (peito)') else 1

st.markdown('---')
st.markdown('OBS: Essa aplicação usa aprendizado de máquina para prover um resultado, mas se você acredita que realmente possui câncer pulmonar, independente do resultado desse teste, **CONSULTE UM MÉDICO.**')

def generate_gradient():
    gradient = ["#fffd80","#fff87e", "#fef47d", "#feef7b", "#fdea7a", "#fde578", "#fde177","#fcdc75", "#fcd774", "#fbd272", "#fbce71", "#fac96f", "#fac46e", "#fabf6c","#f9bb6a","#f9b669","#f8b167","#f8ac66","#f8a864","#f7a363", "#f79e61", "#f69960", "#f6955e", "#f6905d", "#f58b5b", "#f5865a", "#f48258","#f47d56","#f47855","#f37353","#f36f52","#f26a50","#f2654f","#f1604d","#f15c4c","#f1574a","#f05249","#f04d47", "#ef4946","#ef4444"]
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

if st.button("CALCULAR RESULTADOS", type="secondary"):

    x = pd.DataFrame({key: [value] for key, value in entrada.items()})

    resultado = model.predict_proba(x)
    probability = resultado[0][1] * 100


    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = probability,
        number = {"suffix": "%"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Probabilidade de câncer pulmonar", 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#171717"},
            'bar': {'color': "#171717", 'thickness': 0.6},
            'bgcolor': "#e5e5e5",
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
        st.info('Você provavelmente não precisa se preocupar, mas caso possua algum sitoma grave e continue suspeitando da possibiidade, busque um médico.')
        
        
        
#st.write(entrada)

#st.write(type(entrada))