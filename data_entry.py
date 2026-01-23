from datetime import datetime

DATE__FORMAT = "%d-%m-%Y"
CATEGORIES = {
    'R': 'Renda',
    'D': 'Despesa'
}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(DATE__FORMAT)
    try: 
        valid_date = datetime.strptime(date_str, DATE__FORMAT)
        return valid_date.strftime(DATE__FORMAT)
    except ValueError:
        print("Data inválida. Por favor, use o formato DD-MM-AAAA.")
        return get_date(prompt, allow_default)

def get_amount():
    try: 
        amount = float(input("Digite o valor: "))
        if amount <= 0:
            raise ValueError("O valor deve ser positivo.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Digite a categoria: ('R' para Renda, 'D' para Despesa):  ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("Categoria inválida. Por favor, escolha 'R' para Renda, 'D' para Despesa.")
    return get_category()
    
def get_description():
    return input("Descrição (opcional): ")
