/* Return total capacity of all hospitals */
SELECT SUM(capacity) FROM hospital

/* Return hospital occupancy, capacity and name */
SELECT COUNT(patient_id) AS occupancy, capacity, name FROM patient 
JOIN hospital ON patient.hospital_id=hospital.hospital_id
GROUP BY patient.hospital_id

/* Return covid rates for family */

/* Return count of hospitals and sum of capacities for every hospital in a zip code */
SELECT COUNT(zip_code), SUM(capacity) AS capacity, zip_code FROM hospital GROUP BY zip_code 