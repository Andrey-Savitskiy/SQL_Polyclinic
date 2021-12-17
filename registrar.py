from mysql.connector import connect, Error


def registrar(user: str, password: str) -> None:
    while True:
        try:
            command = int(input("""\nВведите:
                1 - для того, чтобы узнать диагноз больного
                2 - для того, чтобы узнать ФИО лечащего врача больного
                3 - для того, чтобы узнать номер кабинета, дни и часы приема врача
                4 - список пациентов у данного врача
                5 - симптомы и лекарство для данного заболевания
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
                    print()
                    select_query = f"""SELECT patient.name, ill.diagnosis from patient
                                        join ill on patient.diagnosis_id = ill.id
                                        where patient.name = '{name}' 
                                        and patient.address = '{address}'
                                    """
                elif command == 2:
                    name = input('\nВведите имя пациента: ')
                    address = input('Введите адрес пациента: ')
                    print()
                    select_query = f"""SELECT doctor.name from patient
                                        join address on patient.address = address.patient_address
                                        join doctor on address.doctor_region = doctor.region
                                        where patient.name = '{name}' 
                                        and patient.address = '{address}'
                                    """
                elif command == 3:
                    name = input('\nВведите имя врача: ')
                    print()
                    select_query = f"""SELECT doctor.name, doctor.office, 
                                        doctor.schedule from doctor
                                        where doctor.name = '{name}'
                                    """
                elif command == 4:
                    name = input('\nВведите имя врача: ')
                    print()
                    select_query = f"""SELECT patient.name from patient
                                        join address on patient.address = address.patient_address
                                        join doctor on address.doctor_region = doctor.region
                                        where doctor.name = '{name}'
                                    """
                elif command == 5:
                    name = input('\nВведите заболевание: ')
                    print()
                    select_query = f"""SELECT ill.id, ill.symptoms, ill.medicine from ill
                                        where ill.diagnosis = '{name}'
                                    """
                elif command == 0:
                    break
                else:
                    print('\nВведена несуществующая команда. Попробуйте еще раз\n')
                    continue

                with connection.cursor(buffered=True) as cursor:
                    cursor.execute(select_query)
                    result = cursor.fetchall()
                    if not len(result):
                        print('\nСовпадений не найдено.\n')
                    else:
                        for row in result:
                            print(row)

        except Error as error:
            print(error)
