import datetime
import requests

def inpput_date():
    """
    Введення дати. Перевірка її формату та щоб вона була не раніше 2022 року
    """
    while True:
        date = input('Дата у форматі YYYY-MM-DD (починаючи з 2022-01-01): ')
        try:
            datetime.date.fromisoformat(date)
        except ValueError:
            print('*** неправильний формат дати: необхідно YYYY-MM-DD\n')
        else:
            if int(date[:4]) < 2022:
                print('*** дата має бути не раніше 2022 року\n')
            else:
                return date

def input_currency(currencies_list, which_currency):
    """
    Введення валюти. Перевірка, чи є така валюта в API.
    currencies_list - список всіх валют з API
    which_currency - вид валюти (початкова чи кінцева)
    """
    while True:
        currency = input(f'Код {which_currency} валюти: ').lower()
        if currency in currencies_list:
            return currency
        else:
            print('*** немає інформації про таку валюту')


if __name__ == '__main__':
    # опис програми
    print("Тут Ви можете дивитися історію конвертації валют")
    print("Потрібно ввести лише дату, початкову валюту та кінцеву\n\n")

    # отримання інформації про всі валюти, що є в API
    l = requests.get(f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies.min.json')
    l = tuple(l.json().keys())
    print("Всі валюти, про які є інформація: ")
    print(l)

    stop = False
    while not stop:
        # Введення даних
        date = inpput_date()
        from_currency = input_currency(l, 'початкової')
        to_currency = input_currency(l, 'кінцевої')

        try:
            # отримання значення кінцевої валюти з API
            req = requests.get(f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/{date}/currencies/{from_currency}/{to_currency}.json')
            # Збереження в змінну
            amount = req.json()[to_currency]

            # Виведення результату
            print(f'\nДата: {date}')
            print(f'1 {from_currency} = {amount} {to_currency}')
        except Exception:
            print('*** ніякої інформації не знайдено за таким запитом')

        # можливість зупинки
        stop = input('\n\tнапишіть q, щоб закінчити\n\taбо будь-що інше, щоб продовжити: ').lower()== 'q'
