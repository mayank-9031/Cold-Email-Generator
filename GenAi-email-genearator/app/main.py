from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from streamlit_ui import create_streamlit_app

def main():
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)

if __name__ == "__main__":
    main()