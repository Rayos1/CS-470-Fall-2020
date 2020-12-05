import os, random, datetime
import numpy as np
import mysql.connector as sql

# change program directory so that file reading works
os.chdir(__file__[:-11])

# get global seed value
SEED = random.randint(0, 99)

# connect to mysql database and get cursor object
DATAB = sql.connect(option_files='credentials.ini')
CURSOR = DATAB.cursor(buffered=True)

def make_hospital(span=2):
    'Returns values for hospital table row'

    name = get_hospital()

    # get random value with precision to the tenth's place
    capacity = random.randint(350, 750) * 10

    # get random value with precision to the one's place
    staff = random.randint(750, 2500)

    # the first two numbers in zip code are randomly selected, 
    # then the next two are based on a global random seed value
    # defined on startup, and the final value is anothor pair of
    #  random values
    zip_code = f'{random.randint(60, 69)}{SEED:02}{random.randint(0, 9)}'

    return name, capacity, staff, zip_code

def make_patient(ratio):
    'Returns values for patient table row'

    first_name, last_name = get_name()
    age = random.randint(5, 105)
    status = random.randint(0, 7)
    # status = random.choices(
    #     [i for i in range(7)],
    #     []
    #     )

    return first_name, last_name, age, status

def make_test():
    'Returns values for test table row'

    test_date = get_date()
    # result = random.randint(0, 1)
    result, = random.choices([0, 1], [.65, .35])
    brand_id = random.randint(0, 5)

    return test_date, result, brand_id

def make_zip(zip_code):
    'Returns values for zip_code table row'

    median_age = random.randint(25, 60)
    median_income = random.randint(300, 2000) * 100
    population = random.randint(8000, 50000)
    state = get_state(int(zip_code[:2]))

    return zip_code, median_age, median_income, population, state

def get_hospital():
    'Returns variable length hospital name'

    prefix = random.choice(list(hospital))
    main =  random.choice(hospital[prefix])
    direction, = random.choices(
        ['North ', 'South ', 'West ', 'East ', ''],
        [.1, .1, .1, .1, .6]
        )
    prefix = direction + prefix
    direction, = random.choices(
        ['North ', 'South ', 'West ', 'East ', 'City ', ''],
        [.15, .15, .15, .15, .2, .2]
        )
    reg, = random.choices(
        ['Regional ', 'Community ', 'Speciality ', 'Research ', ''],
        [.15, .15, .15, .15, .4]
        )
    type, = random.choices(
        ['Health', 'Hospital', 'Medical Center'],
        [.2, .4, .4]
        )

    return f'{prefix}{main} {direction}{reg}{type}'

def get_name():
    'Returns random first and last name'

    return random.choice(first_names), random.choice(last_names)

def get_date():
    'Returns random date from Feb. to Dec.'

    start_date = datetime.date(2020, 2, 1)
    end_date = datetime.date(2020, 12, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return str(random_date)

def get_state(zip):
    'Returns state abbr. based on zip code'

    if 60 <= zip < 63: return 'IL'
    elif 63 <= zip < 66: return 'MO'
    elif 66 <= zip < 68: return 'KS'
    elif 68 <= zip < 70: return 'NE'

first_names = open('first_names.txt').read().splitlines()
last_names = open('last_names.txt').read().splitlines()
place_names = [
    'Illinois',
    'Missouri',
    'Kansas',
    'Nebraska',
    'Arlington',
    'Bloomington',
    'Bristol',
    'Centerville',
    'Chester',
    'Clayton',
    'Clinton',
    'Dayton',
    'Dover',
    'Fairview',
    'Franklin',
    'Georgetown',
    'Greenville',
    'Jackson',
    'Lebanon',
    'Madison',
    'Manchester',
    'Milton',
    'Newport',
    'Oxford',
    'Riverside',
    'Salem',
    'Springfield',
    'Winchester',
    'San José',
    'San Antonio',
    'Santa Maria',
    'Santa Rosa',
    ]
hospital = {
    'Saint ': first_names,
    '': place_names
    }

# Add new hospitals to database
    # CURSOR.execute('SELECT COUNT(*) FROM hospital')
    # results, = CURSOR.fetchone()

    # while True: 

    #     row = make_hospital()
    #     print(row)

    #     if input('y/n: ') == 'y': 

    #         CURSOR.execute(
    #             'INSERT INTO hospital(name, capacity, staff_num, zip_code) VALUES(%s, %s, %s, %s)', row
    #             )
    #         results += 1
    #         print(results)
    #         DATAB.commit() 

# Add new patients to existing hospitals
SELECT = '''SELECT COUNT(patient_id) AS occupancy, capacity FROM patient JOIN hospital ON patient.hospital_id=hospital.hospital_id WHERE patient.hospital_id=%s GROUP BY patient.hospital_id HAVING (occupancy / capacity) < .8'''
CURSOR.execute(
    'SELECT hospital_id FROM hospital WHERE capacity > 1700'# WHERE zip_code LIKE %s', (f'6_{SEED:02}_',)
    )
hospital_ids = CURSOR.fetchall()

for i in range(100000):

    try: 
        hospital_id = random.choice(hospital_ids)
        CURSOR.execute(SELECT, hospital_id)
        occupancy, capacity = CURSOR.fetchone()
    except: continue
    ratio = occupancy / capacity
    row = hospital_id + make_patient(ratio)
    cuttoff = abs(np.random.normal(.7, .3, 1)) % 1

    if ratio < cuttoff:
        CURSOR.execute(
            '''INSERT IGNORE INTO 
            patient(hospital_id, first_name, last_name, age, status) 
            VALUES(%s, %s, %s, %s, %s)''', row
            )
        DATAB.commit()

# Add new tests to existing patients
    # CURSOR.execute('SELECT patient_id FROM patient WHERE status>0 ORDER BY RAND()')

    # for patient_id in CURSOR.fetchmany(1000):

    #     row = patient_id + make_test()
    #     CURSOR.execute(
    #         'INSERT INTO test(patient_id, test_date, result, brand_id) VALUES(%s, %s, %s, %s)', row
    #         )
    #     DATAB.commit()

# Add new zip codes based on existing hospitals
    # CURSOR.execute('SELECT DISTINCT zip_code FROM hospital')

    # for (zip_code,) in CURSOR.fetchall():

    #     row = make_zip(zip_code)
    #     CURSOR.execute(
    #         'INSERT IGNORE INTO zip_code VALUES(%s, %s, %s, %s, %s)', row
    #         )
    #     DATAB.commit()

# Prune hospital capacities to reduce necessary number of patients
    # UPDATE = 'UPDATE hospital SET capacity=%s WHERE name=%s AND zip_code=%s'
    # SELECT = '''SELECT COUNT(patient_id) AS occupancy, capacity FROM patient JOIN hospital ON patient.hospital_id=hospital.hospital_id WHERE patient.hospital_id=%s GROUP BY patient.hospital_id HAVING (occupancy / capacity) < .9'''
    # CURSOR.execute(SELECT)

    # for capacity, name, zip_code in CURSOR.fetchall():
    #     capacity -= random.randint(8, 18) * 10
    #     CURSOR.execute(UPDATE, (capacity, name, zip_code))
    # DATAB.commit()