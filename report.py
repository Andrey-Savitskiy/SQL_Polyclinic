from mysql.connector import connect, Error
from datetime import datetime


def report(user: str, password: str, command: int) -> None:
    try:
        with connect(
            host="localhost",
            user=user,
            password=password,
            database='polyclinic',
        ) as connection:

            if command == 3:
                name = input('\nВведите имя пациента: ')
                address = input('Введите адрес пациента: ')
                print()
                report_query = f"""SELECT patient.name, ill.diagnosis, patient.date FROM patient
                                JOIN ill ON patient.diagnosis_id = ill.id
                                WHERE patient.name = '{name}'
                                AND patient.address = '{address}'
                """
                with connection.cursor(buffered=True) as cursor:
                    cursor.execute(report_query)
                    result = cursor.fetchall()
                    if not len(result):
                        print('\nСовпадений не найдено.\n')
                    else:
                        for row in result:
                            print(f'Данная справка удостоверяет, что {row[0]} болеет {row[1]} с {row[2]}\n')

            elif command == 4:
                report_patients_query = 'SELECT max(patient.id) from patient'
                report_doctor_patients_query = """SELECT doctor.name, count(*), doctor.schedule FROM doctor
                                                    JOIN address ON address.doctor_region = doctor.region
                                                    JOIN patient ON address.patient_address = patient.address
                                                    GROUP BY doctor.name
                                                """
                report_ills_query = """SELECT ill.diagnosis, count(*) FROM ill
                                        JOIN patient ON patient.diagnosis_id = ill.id
                                        GROUP by patient.diagnosis_id
                                    """

                with connection.cursor(buffered=True) as cursor:
                    cursor.execute(report_patients_query)
                    result = cursor.fetchall()
                    print(f'Отчет:\nКоличество пациентов: {result[0][0]}')
                    print()

                    cursor.execute(report_doctor_patients_query)
                    result = cursor.fetchall()
                    print(f'Отчет по врачам(имя, кол-во пациентов, график работы):')
                    for row in result:
                        print(row)
                    print()

                    cursor.execute(report_ills_query)
                    result_1 = cursor.fetchall()
                    print(f'Отчет по заболеваниям(название, кол-во больных):')
                    for row_1 in result_1:
                        print(row_1)
                    print()
            else:
                raise ValueError('\nВведена несуществующая команда. Попробуйте еще раз\n')

    except Error as error:
        print(error)
