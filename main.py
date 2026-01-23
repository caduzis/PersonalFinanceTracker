import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['date', 'amount', 'category', 'description']
    DATE__FORMAT = "%d-%m-%Y"
    
    @classmethod # <- Recebe a propria classe (CSV) como o 1st arg 
    def initialize_csv(cls):
        try: 
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS) 
            # <- dataframe é uma classe e 'columns' é um parametro dela
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod # <- Recebe a propria classe (CSV) como o 1st arg 
    def add_entry(cls,date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            'category': category,
            'description': description
        }

        # Abrindo arquivo CSV e adicionando nova linha
        # boa sintaxe para abrir o arquivo e fechar automaticamente
        with open(cls.CSV_FILE, "a", newline="") as csvfile: 
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully.")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.DATE__FORMAT)
        start_date = datetime.strptime(start_date, CSV.DATE__FORMAT)
        end_date = datetime.strptime(end_date, CSV.DATE__FORMAT)
        # compara as datas já convertidas para 'datatime', caso fosse string não era possível
        mask = (df["date"] >= start_date) & (df["date"] <= end_date) 
        filtered_df = df.loc[mask] # cria um dataframe somente com linhas que passaram no mask

        if filtered_df.empty:
            print("Nenhuma transação encontrada nesse intervalo de datas.")
        else:
            print(f"\nTransações de {start_date.strftime(CSV.DATE__FORMAT)} até {end_date.strftime(CSV.DATE__FORMAT)}:"
                  )
        
            print(filtered_df.to_string(
                index=False, formatters={'date': lambda x: x.strftime(CSV.DATE__FORMAT)}
                )
                )
            
            total_income = filtered_df[filtered_df["category"] == "Renda"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Despesa"]["amount"].sum()
            print("\nResumo:")
            print(f"\nTotal de Renda: R${total_income:.2f}")
            print(f"Total de Despesa: R${total_expense:.2f}")
            print(f"Saldo Líquido: R${(total_income - total_expense):.2f}")

            return filtered_df

def add():
    CSV.initialize_csv()
    date = get_date(
        "Digite a data (DD-MM-AAAA) ou pressione Enter para a data atual: ", 
        allow_default=True
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index('date', inplace=True)

    # 'D' = daily frequency
    income_df = (df[df['category'] == 'Renda']
                 .resample('D')
                 .sum()
                 .reindex(df.index, fill_value=0)
    )
    
    
    expense_df = (df[df['category'] == 'Despesa']
                  .resample('D')
                 .sum()
                 .reindex(df.index, fill_value=0)
    )

    #setting up the canvas where the plot will be drawn
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df['amount'], label='Renda', color='green')
    plt.plot(expense_df.index, expense_df['amount'], label='Despesa', color='red')
    plt.xlabel('Data')
    plt.ylabel('Valor (R$)')
    plt.title('Renda e Despesa ao Longo do Tempo')
    plt.legend() # Ativa a legenda 
    plt.grid()
    plt.show()



def main():
    while True:
        print("\nMenu Principal:")
        print("1. Adicionar nova transação")
        print("2. Visualizar transações por período")
        print("3. Sair")
        choice = input("Escolha uma opção (1-3): ")

        if choice == '1':
            add()
        elif choice == '2':
            start_date = get_date("Digite a data inicial (DD-MM-AAAA): ")
            end_date = get_date("Digite a data final (DD-MM-AAAA): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Deseja visualizar o gráfico das transações? (s/n): ").lower() == 's':
                plot_transactions(df)
        elif choice == '3':
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Por favor, escolha entre 1 e 3.")
        
if __name__ == "__main__":
    main()


            