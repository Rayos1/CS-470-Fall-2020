/* Return total capacity of all hospitals */
SELECT SUM(capacity) FROM hospital

/* Return hospital occupancy, capacity and name */
SELECT COUNT(patient_id) AS occupancy, capacity, name FROM patient 
JOIN hospital ON patient.hospital_id=hospital.hospital_id
GROUP BY patient.hospital_id

/* Return first_name, last_name, age, and health status for patients */
SELECT first_name, last_name, age, status_name 
FROM patient JOIN health_category ON health_category.status_id=patient.status

/* Return relevent data for tests on patients */
SELECT first_name, last_name, result, brand_name, test_date 
FROM patient 
JOIN test ON test.test_id=patient.patient_id
JOIN brand_category ON brand_category.brand_id=test.test_id

/* Return count of hospitals and sum of capacities for every hospital in a zip code */
SELECT COUNT(zip_code), SUM(capacity) AS capacity, zip_code FROM hospital GROUP BY zip_code 

/* Return statistics for each state */
SELECT 
	state,
	round(AVG(median_age), 0) AS average_age, 
    round(AVG(median_income), 0) AS average_income, 
    SUM(population) AS popuation
FROM zip_code
GROUP BY state