#imports
import streamlit as st

change_gradient = '''
  <style>
    .css-1dp5vir {
      background: linear-gradient(90deg, rgba(6,182,212,1) 0%, rgba(219,39,119,1) 100%) !important;
    }
  </style>
'''

# load docs/index.md

def main():
  # titulo da pagina web
  st.set_page_config(page_title="LungHealth", page_icon='👨‍⚕️', layout="centered")

  # alterar gradiente do streamlit (topo da pagina) para combinar com as cores do dashboard
  st.markdown(change_gradient, unsafe_allow_html=True)

  with open("docs/index.md", "r") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

if __name__ == '__main__':
  main()
