import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

def criar_tabela(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS balanco_patrimonial (
            categoria TEXT,
            subcategoria TEXT,
            valor REAL
        )
    ''')

def obter_dados_usuario():
    categoria = input("Digite a categoria: ")
    subcategoria = input("Digite a subcategoria: ")
    valor = float(input("Digite o valor: "))
    return categoria, subcategoria, valor

def inserir_dados(cursor, categoria, subcategoria, valor):
    cursor.execute('INSERT INTO balanco_patrimonial (categoria, subcategoria, valor) VALUES (?, ?, ?)',
                   (categoria, subcategoria, valor))

def atualizar_dados(cursor, categoria, subcategoria, valor):
    cursor.execute('UPDATE balanco_patrimonial SET valor = ? WHERE categoria = ? AND subcategoria = ?',
                   (valor, categoria, subcategoria))

def exibir_opcoes():
    print("1. Inserir Dados")
    print("2. Atualizar Dados")
    print("3. Visualizar Balanço Patrimonial")
    print("4. Sair")

def visualizar_balanco(conexao):
    df = pd.read_sql_query('SELECT * FROM balanco_patrimonial', conexao)
    print("Balanço Patrimonial:")
    print(df)

    fig, ax = plt.subplots(figsize=(12, 8))
    df.pivot(index='subcategoria', columns='categoria', values='valor').plot(kind='bar', stacked=True, ax=ax)
    plt.title("Balanço Patrimonial")
    plt.xlabel("Subcategorias")
    plt.ylabel("Valores")
    plt.show()

def main():
    conexao = sqlite3.connect('balanco_patrimonial.db')
    cursor = conexao.cursor()
    criar_tabela(cursor)

    while True:
        exibir_opcoes()
        escolha = input("Escolha uma opção (1-4): ")

        if escolha == "1":
            categoria, subcategoria, valor = obter_dados_usuario()
            inserir_dados(cursor, categoria, subcategoria, valor)
            conexao.commit()
            print("Dados inseridos com sucesso.")
        elif escolha == "2":
            categoria, subcategoria, valor = obter_dados_usuario()
            atualizar_dados(cursor, categoria, subcategoria, valor)
            conexao.commit()
            print("Dados atualizados com sucesso.")
        elif escolha == "3":
            visualizar_balanco(conexao)
        elif escolha == "4":
            print("Até mais!")
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

    conexao.close()

if __name__ == "__main__":
    main()
