from mysql.connector import connect, Error


def admin(user: str, password: str) -> None:
    while True:
        try:
            command = int(input("""\nВведите:
                1 - для добавления нового больного
                2 - для удаления врача
                3 - для изменения диагноза
                0 - для выхода из аккаунта работника регистратуры
            Ваш номер команды: """))

            with connect(
                host="localhost",
                user=user,
                password=password,
                database='polyclinic',
            ) as connection:

                if command == 1:
                    name = input('\nВведите имя пациента: ')
                    address = input('Введите адрес пациента: ')
                    diagnosis_id = input('Введите заболевание пациента: ')
                    date = input('Введите дату начала болезни пациента без пробелов в формате ГМЧ: ')
                    print()
                    admin_query = f"""
                        INSERT INTO patient(name, address, diagnosis_id, date)
                        VALUES
                            ('{name}', '{address}', {diagnosis_id}, {date})
                    """
                    massage = 'Новый пациент добавлен успешно.\n'
                elif command == 2:
                    id = input('\nВведите id врача: ')
                    print()
                    admin_query = f"""DELETE FROM doctor WHERE doctor.id = {id}
                                    """
                    massage = 'Врач уволен успешно.\n'
                elif command == 3:
                    id = input('\nВведите id диагноза: ')
                    diagnosis = input('Введите новое название диагноза: ')
                    symptoms = input('Введите новые симптомы диагноза: ')
                    medicine = input('Введите новое лечение диагноза: ')
                    print()
                    admin_query = f"""UPDATE
                                            ill
                                        SET
                                            ill.diagnosis = '{diagnosis}',
                                            ill.symptoms = '{symptoms}',
                                            ill.medicine = '{medicine}'
                                        WHERE
                                            ill.id = {id};
                                    """
                    massage = 'Диагноз изменен успешно.\n'
                elif command == 0:
                    break
                else:
                    print('\nВведена несуществующая команда. Попробуйте еще раз\n')
                    continue

                with connection.cursor(buffered=True) as cursor:
                    cursor.execute(admin_query)
                    connection.commit()
                    print(massage)

        except Error as error:
            print(error)
