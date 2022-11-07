import streamlit as st
from joblib import load
import pandas as pd

#model = load('models/model.joblib')
convert = lambda x: 'Sim' if x == 2 else 'Não'
#st.title("Olá")
#if st.button("mundo!"):
    #st.balloons()

    
entrada = {}
col1,col2 = st.columns(2)

entrada['GENDER'] = col1.selectbox(
    'Qual seu genero?',
    ('M', 'F'))

entrada['AGE'] = col2.slider('Insira sua idade',min_value=18, max_value=100)
#st.write('Idade = ', int(idade))

#st.write('You selected:', genero)

# fumante = st.checkbox('Você é fumante', value=True, on_change=(lambda x: 0 if x else 1), disabled=False)
# st.write(fumante)

entrada['SMOKING'] = st.selectbox(
    'Você é fumante?',
    (2, 1),format_func=convert)
#st.write(fumante)
#st.write('You selected:', fumante)

entrada['YELLOW_FINGERS'] = st.selectbox(
    'Você suas extremidades do corpo amareladas?',
    (2, 1),format_func=convert)

#st.write('You selected:', yefing)

entrada['ANXIETY'] = st.selectbox(
    'Você apresenta sinais de transtorno de ansiedade?',
    (2, 1),format_func=convert)

#st.write('You selected:', ansiedade)

entrada['PEER_PRESURE'] = st.selectbox(
    'Por volta da adolescencia, você foi influenciado a fumar?',
    (2, 1),format_func=convert)

#st.write('You selected:', pressao)

entrada['CHRONIC DISEASE'] = st.selectbox(
    'Você possui alguma comorbidade cronica?',
    (2, 1),format_func=convert)

#st.write('You selected:', comorbidade)

entrada['FATIGUE'] = st.selectbox(
    'Você apresenta sinais de cansasso frequentes?',
    (2, 1),format_func=convert)

#st.write('You selected:', fadiga)

entrada['ALLERGY'] = st.selectbox(
    'Você possui alergia a fumaça do cigarro?',
    (2, 1),format_func=convert)

#st.write('You selected:', alergia)

entrada['WHEEZING'] = st.selectbox(
    'Você apresenta um chiado no pulmão?',
    (2, 1),format_func=convert)

#st.write('You selected:', chiado)

entrada['ALCOHOL CONSUMING'] = st.selectbox(
    'Você consome alcool frequente?',
    (2, 1),format_func=convert)

#st.write('You selected:', alcool)

entrada['COUCHING'] = st.selectbox(
    'Você apresenta tosse frequente?',
    (2, 1),format_func=convert)

#st.write('You selected:', tosse)

entrada['SHORTNESS OF BREATH'] = st.selectbox(
    'Você possui respiração curta?',
    (2, 1),format_func=convert)

#st.write('You selected:', respcurta)

entrada['SWALLOWING DIFFICULTY'] = st.selectbox(
    'Você posui alguma dificuldade para ingerir alimentos sólidos ou liquidos?',
    (2, 1),format_func=convert)

#st.write('You selected:', difengolir)

entrada['CHEST PAIN'] = st.selectbox(
    'Você apresenta dor no peito?',
    (2, 1),format_func=convert)

#st.write('You selected:', dorpeito)
st.write(entrada)

# entrada.append(genero)
# entrada.append(idade)
# entrada.append(fumante)
# entrada.append(yefing)
# entrada.append(ansiedade)
# entrada.append(pressao)
# entrada.append(comorbidade)
# entrada.append(fadiga)
# entrada.append(alergia)
# entrada.append(chiado)
# entrada.append(alcool)
# entrada.append(tosse)
# entrada.append(respcurta)
# entrada.append(difengolir)
# entrada.append(dorpeito)

x = pd.DataFrame.from_dict(entrada,orient='index')
st.write(type(x))
x.to_csv('print.csv')
#resultado = model.predict(x)
#st.write(resultado)
#st.write(entrada)

#st.write(type(entrada))