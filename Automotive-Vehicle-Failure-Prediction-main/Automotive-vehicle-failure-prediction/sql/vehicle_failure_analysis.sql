use telemetry_data;
RENAME TABLE synthetic_telemetry_data TO syn
-- PHASE 1 — Understand the fleet
-- Q1
-- How many total telemetry records are in the dataset?
SELECT COUNT(vehicle_id) AS total_records FROM syn;
-- '1970'

-- Q2
-- How many unique vehicles are present?
SELECT COUNT(DISTINCT(vehicle_id)) AS  count_of_brands FROM syn;
# 50
-- Q3
-- How many unique vehicle brands are present?
SELECT COUNT(DISTINCT(brand)) AS  count_of_brands FROM syn;
#10

-- Q4
-- How many records does each vehicle brand have?
SELECT brand,COUNT(*) AS count_of_records FROM syn GROUP BY brand;
-- BMW	192
-- Honda	168
-- Mercedes-Benz	150
-- Audi	325
-- Ford	205
-- Kia	233
-- Nissan	112
-- Toyota	315
-- Hyundai	117
-- Chevrolet	153

-- Business question:
-- Is the dataset evenly distributed across brands?
-- no
-- Q5
-- How many records does each vehicle have?
SELECT vehicle_id,COUNT(*) AS count_of_records FROM syn GROUP BY vehicle_id ORDER BY count_of_records DESC ;
-- VEH0001	44
-- VEH0038	44
-- VEH0049	44
-- VEH0036	44
-- VEH0020	44
-- VEH0034	44
-- VEH0033	44
-- VEH0017	44
-- VEH0023	44
-- VEH0019	44
-- VEH0037	43
-- VEH0039	43
-- VEH0042	43
-- VEH0006	42
-- VEH0046	42
-- VEH0043	42
-- VEH0008	41
-- VEH0048	41
-- VEH0028	40
-- VEH0032	40
-- VEH0016	40
-- VEH0040	40
-- VEH0005	39
-- VEH0010	39
-- VEH0027	39
-- VEH0035	39
-- VEH0041	39
-- VEH0007	38
-- VEH0009	38
-- VEH0011	38
-- VEH0018	38
-- VEH0031	38
-- VEH0022	38
-- VEH0000	38
-- VEH0026	38
-- VEH0003	37
-- VEH0024	37
-- VEH0002	36
-- VEH0029	36
-- VEH0030	36
-- VEH0025	36
-- VEH0045	36
-- VEH0012	35
-- VEH0004	35
-- VEH0021	35
-- VEH0044	35
-- VEH0015	35
-- VEH0047	35
-- VEH0014	35
-- VEH0013	35

--------------------------------------------------------------------------------
-- PHASE 2 — Failure overview
-- Q6
-- How many records are classified as:
-- No Failure
-- Actual failure
SELECT failure_type,COUNT(failure_type) AS count_of_records FROM syn GROUP BY failure_type;

-- Q7

-- What is the overall failure rate?

SELECT 
    100.0 * sum(CASE WHEN failure_type <> 'No Failure' THEN 1 END) / COUNT(*) AS failure_percentage
FROM syn;
-- '1.77665'

-- Q8
-- What are the counts of each failure_type?
SELECT failure_type ,COUNT(failure_type) AS failure_count FROM  syn GROUP BY  failure_type;
-- No Failure	1935
-- Low Brake Fluid	5
-- Battery Dead	4
-- Brake Pad Worn	9
-- Engine Overheat	4
-- Excessive Vibration	2
-- Battery Drain	4
-- Low Oil Pressure	1
-- Low Battery Voltage	4
-- Brake Overheat	2 

-- Q9
-- Which 5 failure types occur most frequently?
SELECT failure_type ,COUNT(failure_type) AS failure_count FROM  syn  WHERE failure_type<> "No Failure" 
GROUP BY   failure_type  ORDER BY failure_count DESC LIMIT 5;
-- Brake Pad Worn	9
-- Low Brake Fluid	5
-- Battery Dead	4
-- Engine Overheat	4
-- Battery Drain	4

-- Q10
-- Which failure type occurs least frequently, excluding No Failure?
SELECT failure_type ,COUNT(failure_type) AS failure_count FROM  syn  WHERE failure_type<> "No Failure" 
GROUP BY   failure_type  ORDER BY failure_count  LIMIT 1;
-- Low Oil Pressure	1
----------------------------------------------------------
-- PHASE 3 — System-level failure analysis

-- Q12
-- What percentage of all actual failures belongs to each system?
-- I DONT UNDERSTAND THIS QUESTION

-- Q13
-- Which vehicle system has the highest failure burden?
SELECT vehicle_id,COUNT(*) AS counts FROM  syn WHERE failure_type <> "No Failure"  GROUP BY 
vehicle_id ORDER BY counts DESC LIMIT 1;
-- VEH0026	4


-- Q14
-- Which specific failure contributes most to the dominant system?
SELECT  failure_type,COUNT(vehicle_id) AS counts FROM  syn WHERE failure_type <>"No Failure"  GROUP BY 
failure_type ORDER BY counts DESC LIMIT 1;
-- Brake Pad Worn	9
------------------------------------------------------
-- PHASE 4 — Vehicle analysis


-- Q15
-- How many failures does each vehicle have?
SELECT vehicle_id,COUNT(failure_type) AS counts FROM  syn WHERE failure_type <> "No Failure"  GROUP BY 
vehicle_id ORDER BY counts DESC LIMIT 5;
-- VEH0026	4
-- VEH0049	3
-- VEH0011	2


-- Q16

-- Which 10 vehicles have the highest number of failures?
SELECT vehicle_id,COUNT(failure_type) AS counts FROM  syn WHERE failure_type <> "No Failure"  GROUP BY 
vehicle_id ORDER BY counts DESC LIMIT 10;
-- VEH0026	4
-- VEH0049	3
-- VEH0011	2
-- VEH0016	2
-- VEH0028	2
-- VEH0031	2
-- VEH0035	2
-- VEH0004	1
-- VEH0005	1
-- VEH0006	1

-- Q17
-- Which vehicles have experienced more than one failure?
SELECT vehicle_id,COUNT(failure_type) AS counts FROM  syn WHERE failure_type <> "No Failure"  GROUP BY 
vehicle_id  HAVING counts>1 ORDER BY counts DESC ;
-- Q18

-- Which vehicle has the highest failure rate?
SELECT 
    vehicle_id,
    COUNT(CASE WHEN TRIM(failure_type) <> 'No Failure' THEN 1 END) AS total_failures,
    COUNT(*) AS total_records,
    ROUND(
        100.0 * COUNT(CASE WHEN TRIM(failure_type) <> 'No Failure' THEN 1 END) / COUNT(*), 
        2
    ) AS failure_rate_pct
FROM syn
GROUP BY vehicle_id
ORDER BY failure_rate_pct DESC, total_failures DESC
LIMIT 1;
------------------------------------------------------------
-- PHASE 5 — Brand analysis

-- "Are some vehicle brands experiencing more failures than others?"

-- Q19
-- How many failures does each brand have?
SELECT brand,COUNT(failure_type) AS counts FROM  syn WHERE failure_type <> "No Failure"  GROUP BY 
brand ORDER BY counts DESC;
-- Audi	8
-- Toyota	8
-- Chevrolet	5
-- BMW	4
-- Kia	3
-- Hyundai	3
-- Ford	2
-- Nissan	1
-- Mercedes-Benz	1

-- Q20
-- What is the failure rate for each brand?
SELECT 
brand,
SUM(CASE WHEN failure_type <> 'No Failure' THEN 1 ELSE 0 END) AS no_of_failures,
COUNT(*) AS total,
ROUND(SUM(CASE WHEN failure_type <> 'No Failure' THEN 1 ELSE 0 END)*100/COUNT(*),2) AS failure_rate
FROM syn 
GROUP BY brand ORDER BY failure_rate DESC ;

-- Chevrolet	5	153	3.27
-- Hyundai	3	117	2.56
-- Toyota	8	315	2.54
-- Audi	8	325	2.46
-- BMW	4	192	2.08
-- Kia	3	233	1.29
-- Ford	2	205	0.98
-- Nissan	1	112	0.89
-- Mercedes-Benz	1	150	0.67
-- Honda	0	168	0.00

-- Q21
-- Which brand has the highest failure rate?
SELECT 
brand,
SUM(CASE WHEN failure_type <> 'No Failure' THEN 1 ELSE 0 END) AS no_of_failures,
COUNT(*) AS total,
ROUND(SUM(CASE WHEN failure_type <> 'No Failure' THEN 1 ELSE 0 END)*100/COUNT(*),2) AS failure_rate
FROM syn 
GROUP BY brand ORDER BY failure_rate DESC LIMIT 1;
-- Chevrolet	5	153	3.27

-- Q22
-- Which brand has the lowest failure rate?
SELECT 
brand,
SUM(CASE WHEN failure_type <> 'No Failure' THEN 1 ELSE 0 END) AS no_of_failures,
COUNT(*) AS total,
ROUND(SUM(CASE WHEN failure_type <> 'No Failure' THEN 1 ELSE 0 END)*100/COUNT(*),2) AS failure_rate
FROM syn 
GROUP BY brand ORDER BY failure_rate ASC LIMIT 1;
-- Honda	0	168	0.00

-- Q23
-- For each brand, what is its most common failure type?
WITH RankedFailures AS (
    SELECT 
        brand,
        failure_type,
        COUNT(*) AS failure_count,
        ROW_NUMBER() OVER (
            PARTITION BY brand 
            ORDER BY COUNT(*) DESC
        ) AS rnk
    FROM syn
    WHERE TRIM(failure_type) <> 'No Failure'
    GROUP BY brand, failure_type
)
SELECT 
    brand,
    failure_type AS most_common_failure,
    failure_count
FROM RankedFailures
WHERE rnk = 1
ORDER BY failure_count DESC;
-- Audi	Brake Pad Worn	3
-- Toyota	Brake Pad Worn	3
-- Chevrolet	Low Battery Voltage	2
-- Hyundai	Battery Drain	2
-- BMW	Low Brake Fluid	1
-- Ford	Battery Dead	1
-- Kia	Brake Pad Worn	1
-- Mercedes-Benz	Battery Dead	1
-- Nissan	Brake Pad Worn	1

-- PHASE 6 — Vehicle operating conditions



-- Under what conditions did it happen?

-- Q24

-- What is the average:engine temperature,coolant temperature,engine RPM,engine load,engine hours,
-- fuel consumption,battery health
-- battery temperature
-- brake temperature
-- for No Failure vs Failure?
SELECT failure_type,AVG(engine_temp_c),AVG(coolant_temp_c),AVG(engine_rpm),AVG(engine_load_percent),
AVG(engine_hours),AVG(engine_hours),AVG(fuel_consumption_lph),AVG(fuel_consumption_lph)
,AVG(battery_health_percent),AVG(battery_temp_c),AVG(brake_temp_c) FROM syn GROUP BY failure_type;
-- failure_type, AVG(engine_temp_c), AVG(coolant_temp_c), AVG(engine_rpm), AVG(engine_load_percent), AVG(engine_hours), AVG(engine_hours), AVG(fuel_consumption_lph), AVG(fuel_consumption_lph), AVG(battery_health_percent), AVG(battery_temp_c), AVG(brake_temp_c)
-- No Failure	95.04298843454752	89.86638807425345	2013.5836327887698	40.00599517851945	2612.519566512273	2612.519566512273	5.124912866520035	5.124912866520035	94.33644706692374	25.00288353279219	79.5737577484814
-- Low Brake Fluid	95.21144018855624	88.32713309750233	1698.4234867533373	45.737035168673934	2728.7463543413496	2728.7463543413496	1.9078622877013316	1.9078622877013316	94.93944667500726	23.025031656253574	293.2687527208333
-- Battery Dead	99.9599772685329	90.14911241122867	2446.1564363605285	57.994777257916844	2025.919565351818	2025.919565351818	4.837697259534959	4.837697259534959	95.20693311572307	25.089409300380147	60.633739335993724
-- Brake Pad Worn	96.09403127853369	90.86005233596997	2194.528846400384	37.70415766256034	2434.0406013954043	2434.0406013954043	5.1968289919518735	5.1968289919518735	93.43436897851072	23.79859559587017	328.502064118683
-- Engine Overheat	112.40860114868326	90.66801840966625	1624.5242891721039	25.699385980451346	3127.55204949646	3127.55204949646	3.6095204213281216	3.6095204213281216	92.65019771380227	27.48563266614142	80.99155636003992
-- Excessive Vibration	108.59365536840235	91.00840406854489	1017.126204253656	38.68294136570066	4223.356043276349	4223.356043276349	4.315470510026826	4.315470510026826	92.51985038564338	30.986318802083712	119.76133089653305
-- Battery Drain	91.88424331700526	90.61655144575488	2014.7919890246606	37.191951604072976	3909.080402143933	3909.080402143933	4.308140821436266	4.308140821436266	94.4999628082004	25.062657312649744	120.76659330364245
-- Low Oil Pressure	108.64518875087661	93.92400388336272	1707.592781233533	37.01380132920734	834.911542990802	834.911542990802	2.90362846683872	2.90362846683872	98.45131565481427	30.289317268929423	39.150518583994874
-- Low Battery Voltage	93.6998479138551	90.54834142227762	1456.0877704001507	42.6551499499047	2040.5886706038984	2040.5886706038984	9.997973441048025	9.997973441048025	92.44076721593461	24.976581210286938	79.24692783739688
-- Brake Overheat	88.34752697173938	89.08247211817422	2071.679367044707	25.423418021637918	3081.2945752961587	3081.2945752961587	8.550258730339852	8.550258730339852	94.41644171942409	22.564661312852245	362.72333675609315
----------------------------------------------------------------
-- PHASE 7 — Engineering/root-cause questions

-- Q30 — Engine
-- For Engine Overheat vs No Failure:
-- What are the average engine temperature, coolant temperature, RPM, engine load and engine hours?
SELECT failure_type,AVG(engine_temp_c),AVG(coolant_temp_c),AVG(engine_rpm),AVG(engine_load_percent),
AVG(engine_hours) FROM syn WHERE failure_type IN ("No Failure","Engine Overheat") GROUP BY failure_type;

-- failure_type, AVG(engine_temp_c), AVG(coolant_temp_c), AVG(engine_rpm), AVG(engine_load_percent), AVG(engine_hours)
-- No Failure	95.04298843454752	89.86638807425345	2013.5836327887698	40.00599517851945	2612.519566512273
-- Engine Overheat	112.40860114868326	90.66801840966625	1624.5242891721039	25.699385980451346	3127.55204949646

-- Q31 — Battery
-- For battery-related failures vs No Failure:
-- What are the average battery health, battery voltage, battery temperature and battery charge percentage?
SELECT  failure_type,AVG(battery_health_percent),AVG(battery_voltage_v),AVG(battery_temp_c) FROM syn WHERE failure_type
IN('Battery Dead','Battery Drain','Low Battery Voltage','No Failure') GROUP BY failure_type;

-- failure_type, AVG(battery_health_percent), AVG(battery_voltage_v), AVG(battery_temp_c)
-- No Failure	94.33644706692374	12.593331764228374	25.00288353279219
-- Battery Dead	95.20693311572307	10.294905922544464	25.089409300380147
-- Battery Drain	94.4999628082004	10.103669259790696	25.062657312649744
-- Low Battery Voltage	92.44076721593461	9.680600917452315	24.976581210286938



-- Q32 — Brake
-- For brake-related failures vs No Failure:
-- What are the average brake temperature, brake pad wear, brake fluid level and brake pedal position?
SELECT DISTINCT(failure_type) FROM syn;
SELECT  failure_type,AVG(brake_temp_c),AVG(brake_pad_wear_mm),AVG(brake_fluid_level_psi),AVG(brake_pedal_pos_percent)
 FROM syn WHERE failure_type
IN('Low Brake Fluid','Brake Pad Worn','Brake Overheat','No Failure') GROUP BY failure_type;

-- failure_type, AVG(brake_temp_c), AVG(brake_pad_wear_mm), AVG(brake_fluid_level_psi), AVG(brake_pedal_pos_percent)
-- No Failure	79.5737577484814	8.066911527956623	1001.4463034258717	50.04519356359883
-- Low Brake Fluid	293.2687527208333	8.849929877088696	512.9456571126705	51.0899005206217
-- Brake Pad Worn	328.502064118683	8.46829719102302	565.7554498077674	44.721354592183566
-- Brake Overheat	362.72333675609315	7.290403025067281	618.9707752950084	22.28962662319192

-- Q33
-- For each failure type, what is the maximum engine temperature observed?
SELECT failure_type,MAX(engine_temp_c) FROM syn WHERE failure_type <> "No Failure" GROUP BY failure_type ;

-- failure_type, MAX(engine_temp_c)
-- Low Brake Fluid	98.70300780606836
-- Battery Dead	111.7185636524671
-- Brake Pad Worn	106.01716836002362
-- Engine Overheat	119.3224707208603
-- Excessive Vibration	109.04485651945728
-- Battery Drain	96.0093140159594
-- Low Oil Pressure	108.64518875087661
-- Low Battery Voltage	98.77171828803394
-- Brake Overheat	90.1152014180764

-- Q34
-- For each failure type, what is the maximum brake temperature observed?
SELECT failure_type,MAX(brake_temp_c) FROM syn WHERE failure_type <> "No Failure" GROUP BY failure_type ;

-- failure_type, MAX(brake_temp_c)
-- Low Brake Fluid	359.27781303428037
-- Battery Dead	142.66971115909615
-- Brake Pad Worn	399.3553595147635
-- Engine Overheat	136.80682706778728
-- Excessive Vibration	144.19873302991346
-- Battery Drain	154.82453633203977
-- Low Oil Pressure	39.150518583994874
-- Low Battery Voltage	99.16282580407247
-- Brake Overheat	387.6485348441271

-- Q35
-- For each failure type, what is the minimum battery health observed?
SELECT failure_type,MIN(battery_health_percent) FROM syn WHERE failure_type <> "No Failure" GROUP BY failure_type ;

-- failure_type, MIN(battery_health_percent)
-- Low Brake Fluid	91.0167771868084
-- Battery Dead	90.29097604124891
-- Brake Pad Worn	91.26559890804464
-- Engine Overheat	90.99003046225448
-- Excessive Vibration	91.41174784737576
-- Battery Drain	93.3836837729028
-- Low Oil Pressure	98.45131565481427
-- Low Battery Voltage	91.07692080257021
-- Brake Overheat	93.94590604302863
-----------------------------------------------------------------
-- PHASE 8 — Advanced SQL
-- Q36

-- Rank vehicles within each brand by their number of failures.
SELECT 
brand,
COUNT(failure_type),
row_number() over(ORDER BY  COUNT(failure_type) DESC ) AS rank_of_failures
FROM syn
WHERE failure_type <> "No Failure"
GROUP BY brand;

-- brand, COUNT(failure_type), rank_of_failures
-- Audi	8	1
-- Toyota	8	2
-- Chevrolet	5	3
-- BMW	4	4
-- Kia	3	5
-- Hyundai	3	6
-- Ford	2	7
-- Nissan	1	8
-- Mercedes-Benz	1	9

-- Q37
-- For each brand, calculate:
-- brand
-- total_records
-- failure_records
-- failure_rate
-- brand_rank
SELECT 
    brand,
    COUNT(*) AS total_records,
    COUNT(CASE WHEN TRIM(failure_type) <> 'No Failure' THEN 1 END) AS failure_records,
    ROUND(
        100.0 * COUNT(CASE WHEN TRIM(failure_type) <> 'No Failure' THEN 1 END) / COUNT(*), 
        2
    ) AS failure_rate,
    DENSE_RANK() OVER (
        ORDER BY 100.0 * COUNT(CASE WHEN TRIM(failure_type) <> 'No Failure' THEN 1 END) / COUNT(*) DESC
    ) AS brand_rank
FROM syn
GROUP BY brand
ORDER BY brand_rank ASC;

-- brand, total_records, failure_records, failure_rate, brand_rank
-- Chevrolet	153	5	3.27	1
-- Hyundai	117	3	2.56	2
-- Toyota	315	8	2.54	3
-- Audi	325	8	2.46	4
-- BMW	192	4	2.08	5
-- Kia	233	3	1.29	6
-- Ford	205	2	0.98	7
-- Nissan	112	1	0.89	8
-- Mercedes-Benz	150	1	0.67	9
-- Honda	168	0	0.00	10

-- Q38
-- For each vehicle, calculate:

-- vehicle_id
-- total_observations
-- failures
-- failure_rate
SELECT 
    vehicle_id,
    COUNT(*) AS total_observations,
    COUNT(CASE WHEN TRIM(failure_type) <> 'No Failure' THEN 1 END) AS failures,
    ROUND(
        100.0 * COUNT(CASE WHEN TRIM(failure_type) <> 'No Failure' THEN 1 END) / COUNT(*), 
        2
    ) AS failure_rate
FROM syn
GROUP BY vehicle_id
ORDER BY failure_rate DESC, total_observations DESC;

-- vehicle_id, total_observations, failures, failure_rate
-- VEH0026	38	4	10.53
-- VEH0049	44	3	6.82
-- VEH0031	38	2	5.26
-- VEH0011	38	2	5.26
-- VEH0035	39	2	5.13
-- VEH0028	40	2	5.00
-- VEH0016	40	2	5.00
-- VEH0004	35	1	2.86
-- VEH0015	35	1	2.86
-- VEH0047	35	1	2.86
-- VEH0029	36	1	2.78
-- VEH0025	36	1	2.78
-- VEH0024	37	1	2.70
-- VEH0009	38	1	2.63
-- VEH0005	39	1	2.56
-- VEH0010	39	1	2.56
-- VEH0008	41	1	2.44
-- VEH0048	41	1	2.44
-- VEH0006	42	1	2.38
-- VEH0043	42	1	2.38
-- VEH0046	42	1	2.38
-- VEH0020	44	1	2.27
-- VEH0036	44	1	2.27
-- VEH0023	44	1	2.27
-- VEH0017	44	1	2.27
-- VEH0001	44	0	0.00
-- VEH0019	44	0	0.00
-- VEH0033	44	0	0.00
-- VEH0034	44	0	0.00
-- VEH0038	44	0	0.00
-- VEH0039	43	0	0.00
-- VEH0042	43	0	0.00
-- VEH0037	43	0	0.00
-- VEH0032	40	0	0.00
-- VEH0040	40	0	0.00
-- VEH0027	39	0	0.00
-- VEH0041	39	0	0.00
-- VEH0007	38	0	0.00
-- VEH0022	38	0	0.00
-- VEH0018	38	0	0.00
-- VEH0000	38	0	0.00
-- VEH0003	37	0	0.00
-- VEH0002	36	0	0.00
-- VEH0030	36	0	0.00
-- VEH0045	36	0	0.00
-- VEH0012	35	0	0.00
-- VEH0013	35	0	0.00
-- VEH0021	35	0	0.00
-- VEH0044	35	0	0.00
-- VEH0014	35	0	0.00

-- Q39
-- Find vehicles whose failure rate is higher than their brand's average failure rate.
WITH BrandStats AS (
    -- Calculate overall failure rate for each brand
    SELECT 
        brand,
        100.0 * COUNT(CASE WHEN TRIM(failure_type) <> 'No Failure' THEN 1 END) / COUNT(*) AS brand_avg_failure_rate
    FROM syn
    GROUP BY brand
),
VehicleStats AS (
    -- Calculate failure rate for each vehicle
    SELECT 
        vehicle_id,
        brand,
        COUNT(*) AS total_observations,
        COUNT(CASE WHEN TRIM(failure_type) <> 'No Failure' THEN 1 END) AS vehicle_failures,
        100.0 * COUNT(CASE WHEN TRIM(failure_type) <> 'No Failure' THEN 1 END) / COUNT(*) AS vehicle_failure_rate
    FROM syn
    GROUP BY vehicle_id, brand
)
SELECT 
    v.vehicle_id,
    v.brand,
    v.total_observations,
    v.vehicle_failures,
    ROUND(v.vehicle_failure_rate, 2) AS vehicle_failure_rate,
    ROUND(b.brand_avg_failure_rate, 2) AS brand_avg_failure_rate
FROM VehicleStats v
JOIN BrandStats b ON v.brand = b.brand
WHERE v.vehicle_failure_rate > b.brand_avg_failure_rate
ORDER BY (v.vehicle_failure_rate - b.brand_avg_failure_rate) DESC;

-- vehicle_id, brand, total_observations, vehicle_failures, vehicle_failure_rate, brand_avg_failure_rate
-- VEH0026	Toyota	38	4	10.53	2.54
-- VEH0049	Audi	44	3	6.82	2.46
-- VEH0016	BMW	40	2	5.00	2.08
-- VEH0011	Toyota	38	2	5.26	2.54
-- VEH0028	Hyundai	40	2	5.00	2.56
-- VEH0031	Chevrolet	38	2	5.26	3.27
-- VEH0010	Mercedes-Benz	39	1	2.56	0.67
-- VEH0035	Chevrolet	39	2	5.13	3.27
-- VEH0015	Kia	35	1	2.86	1.29
-- VEH0008	Nissan	41	1	2.44	0.89
-- VEH0006	Ford	42	1	2.38	0.98
-- VEH0046	Ford	42	1	2.38	0.98
-- VEH0009	Kia	38	1	2.63	1.29
-- VEH0036	Kia	44	1	2.27	1.29
-- VEH0004	BMW	35	1	2.86	2.08
-- VEH0047	BMW	35	1	2.86	2.08
-- VEH0025	Audi	36	1	2.78	2.46
-- VEH0024	Toyota	37	1	2.70	2.54
-- VEH0005	Audi	39	1	2.56	2.46

-- Q40

-- For each failure type, rank the vehicle brands by failure count.
WITH FailureCounts AS (
    SELECT 
        failure_type,
        brand,
        COUNT(*) AS failure_count,
        DENSE_RANK() OVER (
            PARTITION BY failure_type 
            ORDER BY COUNT(*) DESC
        ) AS brand_rank
    FROM syn
    WHERE TRIM(failure_type) <> 'No Failure'
    GROUP BY failure_type, brand
)
SELECT 
    failure_type,
    brand,
    failure_count,
    brand_rank
FROM FailureCounts
ORDER BY failure_type, brand_rank;
-- failure_type, brand, failure_count, brand_rank
-- Battery Dead	Ford	1	1
-- Battery Dead	Mercedes-Benz	1	1
-- Battery Dead	Toyota	1	1
-- Battery Dead	Audi	1	1
-- Battery Drain	Hyundai	2	1
-- Battery Drain	Kia	1	2
-- Battery Drain	BMW	1	2
-- Brake Overheat	Kia	1	1
-- Brake Overheat	Ford	1	1
-- Brake Pad Worn	Toyota	3	1
-- Brake Pad Worn	Audi	3	1
-- Brake Pad Worn	Nissan	1	2
-- Brake Pad Worn	Kia	1	2
-- Brake Pad Worn	BMW	1	2
-- Engine Overheat	Audi	2	1
-- Engine Overheat	Toyota	1	2
-- Engine Overheat	Chevrolet	1	2
-- Excessive Vibration	Toyota	1	1
-- Excessive Vibration	Chevrolet	1	1
-- Low Battery Voltage	Chevrolet	2	1
-- Low Battery Voltage	Toyota	1	2
-- Low Battery Voltage	BMW	1	2
-- Low Brake Fluid	BMW	1	1
-- Low Brake Fluid	Audi	1	1
-- Low Brake Fluid	Toyota	1	1
-- Low Brake Fluid	Hyundai	1	1
-- Low Brake Fluid	Chevrolet	1	1
-- Low Oil Pressure	Audi	1	1

-- Q41

-- Identify the top 3 failure types within each brand.
WITH RankedFailures AS (
    SELECT 
        brand,
        failure_type,
        COUNT(*) AS failure_count,
        DENSE_RANK() OVER (
            PARTITION BY brand 
            ORDER BY COUNT(*) DESC
        ) AS failure_rank
    FROM syn
    WHERE TRIM(failure_type) <> 'No Failure'
    GROUP BY brand, failure_type
)
SELECT 
    brand,
    failure_rank,
    failure_type,
    failure_count
FROM RankedFailures
WHERE failure_rank <= 3
ORDER BY brand, failure_rank;

-- brand, failure_rank, failure_type, failure_count
-- Audi	1	Brake Pad Worn	3
-- Audi	2	Engine Overheat	2
-- Audi	3	Low Brake Fluid	1
-- Audi	3	Low Oil Pressure	1
-- Audi	3	Battery Dead	1
-- BMW	1	Low Brake Fluid	1
-- BMW	1	Brake Pad Worn	1
-- BMW	1	Battery Drain	1
-- BMW	1	Low Battery Voltage	1
-- Chevrolet	1	Low Battery Voltage	2
-- Chevrolet	2	Excessive Vibration	1
-- Chevrolet	2	Engine Overheat	1
-- Chevrolet	2	Low Brake Fluid	1
-- Ford	1	Battery Dead	1
-- Ford	1	Brake Overheat	1
-- Hyundai	1	Battery Drain	2
-- Hyundai	2	Low Brake Fluid	1
-- Kia	1	Brake Pad Worn	1
-- Kia	1	Battery Drain	1
-- Kia	1	Brake Overheat	1
-- Mercedes-Benz	1	Battery Dead	1
-- Nissan	1	Brake Pad Worn	1
-- Toyota	1	Brake Pad Worn	3
-- Toyota	2	Engine Overheat	1
-- Toyota	2	Excessive Vibration	1
-- Toyota	2	Battery Dead	1
-- Toyota	2	Low Battery Voltage	1
-- Toyota	2	Low Brake Fluid	1
---------------------------------------------------
