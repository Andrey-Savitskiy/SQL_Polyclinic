from mysql.connector import connect, Error


def command_execution(sql_command: str, user: str,
                      password: str,
                      database: str = 'polyclinic') -> None:
    """
    Функция, выполняющая SQL запросы
    :param user: имя пользователя
    :param password: пароль
    :param sql_command: команда на создание
    :param database: имя базы данных
    :return:
    """
    with connect(
        host="localhost",
        user=user,
        password=password,
        database=database,
    ) as connection:
        create_table_query = sql_command
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()


def initial(user: str, password: str) -> None:
    """
    Функция с инициализацией: создание БД, создание всех таблиц,
    установка параметров полей таблиц и их межтабличных связей
    :param user: имя пользователя
    :param password: пароль
    :return: None
    """
    with connect(
        host="localhost",
        user=user,
        password=password,
    ) as connection:
        drop_db_query = "DROP DATABASE polyclinic"
        create_db_query = "CREATE DATABASE polyclinic"     # создание БД "polyclinic"
        show_db_query = 'SHOW DATABASES'
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(show_db_query)
            cursor.execute(show_db_query)
            if ('polyclinic',) in cursor:
                cursor.execute(drop_db_query)

            cursor.execute(create_db_query)

    # создание таблицы описание болезней
    create_ill_table_query = """                 
        CREATE TABLE ill(
        id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
        diagnosis VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        symptoms VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        medicine VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        PRIMARY KEY(id) 
        )
        """
    command_execution(sql_command=create_ill_table_query, user=user, password=password)

    # создание таблицы пациентов
    create_patient_table_query = """
        CREATE TABLE patient(
        id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE KEY,
        name VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        address VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        diagnosis_id INT(10) UNSIGNED NOT NULL,
        date DATE NOT NULL,
        CONSTRAINT ill FOREIGN KEY(diagnosis_id) REFERENCES ill(id),
        PRIMARY KEY(address, diagnosis_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
    command_execution(sql_command=create_patient_table_query, user=user, password=password)

    # создание таблицы врачей
    create_doctor_table_query = """
        CREATE TABLE doctor(
        id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE KEY,
        name VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        office INT(10) UNSIGNED NOT NULL,
        region INT(10) UNSIGNED NOT NULL,
        schedule VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        PRIMARY KEY(region)
        ) 
        """
    command_execution(sql_command=create_doctor_table_query, user=user, password=password)

    # создание таблицы адрес-участок
    create_address_table_query = """
        CREATE TABLE address(
        patient_address VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        doctor_region INT(10) UNSIGNED NOT NULL,
        CONSTRAINT patient FOREIGN KEY(patient_address) REFERENCES patient(address),
        CONSTRAINT doctor FOREIGN KEY(doctor_region) REFERENCES doctor(region),
        PRIMARY KEY(patient_address, doctor_region)
        )
        """
    command_execution(sql_command=create_address_table_query, user=user, password=password)

    # Заполняем таблицу болезней
    insert_ill_query = """
        INSERT INTO ill(diagnosis, symptoms, medicine)
        VALUES
            ('ОРЗ', 'Температура 37.5+, красное горло', 'Постельный режим, полоскать горло'),
            ('Коронавирус', 'Температура 38.0+, потеря вкуса', 'Молиться'),
            ('Смерть', 'Температура 25.0-', 'Воскреснуть')
    """
    command_execution(sql_command=insert_ill_query, user=user, password=password)

    # Заполняем таблицу пациентов
    insert_patient_query = """
        INSERT INTO patient(name, address, diagnosis_id, date)
        VALUES
            ('Иванов Иван Иванович', 'ул. Советская 15', 1, 20081023),
            ('Петров Петр Петрович', 'ул. Советская 15', 2, 20101101),
            ('Сидоров Сидор Сидорович', 'ул. Советская 16', 2, 20120427),
            ('Иванов Иван Иванович', 'ул. Ленина 16', 3, 20160229),
            ('Сидоров Сидор Сидорович', 'ул. Ленина 17', 2, 20210428)
    """
    command_execution(sql_command=insert_patient_query, user=user, password=password)

    # Заполняем таблицу врачей
    insert_doctor_query = """
        INSERT INTO doctor(name, office, region, schedule)
        VALUES
            ('Гибнер Христиан Иванович', 301, 1, 'Пн-Пт: 9.00-17.00'),
            ('Костоломова Алена Петровна', 302, 2, 'Сб-Вс: 10.00-18.00')
    """
    command_execution(sql_command=insert_doctor_query, user=user, password=password)

    # Заполняем таблицу соответствия адресов участкам
    insert_address_query = """
        INSERT INTO address(patient_address, doctor_region)
        VALUES
            ('ул. Советская 15', 1),
            ('ул. Советская 16', 1),
            ('ул. Ленина 16', 2),
            ('ул. Ленина 17', 2)
    """
    command_execution(sql_command=insert_address_query, user=user, password=password)
