from Initial_DB import initial, Error
from registrar import registrar
from admin import admin
from report import report


# -- ввести свои права суперпользователя
USER = 'root'
PASSWORD = 'D2p96oMJ8Yrc1HDhSZDe'


if __name__ == '__main__':
    try:
        initial(user=USER, password=PASSWORD)

        while True:
            try:
                account = int(input('\nНажмите:\n'
                                    '1 - для входа как работник регистратуры\n'
                                    '2 - для входа как администратор\n'
                                    '3 - для выдачи справки пациента\n'
                                    '4 - для выдачи отчета о работе поликлиники\n'
                                    '0 - для выхода из программы\n'
                                    'Ваш выбор: '
                                    ))
                print()

                if account == 1:
                    registrar(user=USER, password=PASSWORD)
                elif account == 2:
                    admin(user=USER, password=PASSWORD)
                elif account == 3:
                    report(user=USER, password=PASSWORD, command=account)
                elif account == 4:
                    report(user=USER, password=PASSWORD, command=account)
                elif account == 0:
                    break
                else:
                    print('\nВведена несуществующая команда. Попробуйте еще раз\n')
                    continue

            except Error as error:
                print(error)
                continue

    except Error as error:
        print(error)
