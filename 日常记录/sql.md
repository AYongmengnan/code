SELECT COUNT(id) from business_apollo_match; 

create table crunchbase_news1 as select * from crunchbase_news;


DELETE t1
FROM crunchbase_news_etl t1
INNER JOIN crunchbase_news_etl t2 ON t1.url = t2.url AND t1.id > t2.id;


SELECT COUNT(id) from crunchbase_news_etl; 


SELECT COUNT(*)  FROM glassdoor WHERE area != 'Indonesia';

SELECT COUNT(*)  FROM crunchbase WHERE country='Indonesia';

UPDATE crunchbase  set country='Indonesia' where id <=56284 and id>=56183;

DELETE g1
FROM glassdoor g1
JOIN (
    SELECT name, ceo, website, url, MIN(id) AS min_id
    FROM glassdoor
    WHERE area = 'Indonesia'
    GROUP BY name, ceo, website, url
    HAVING COUNT(*) > 1
) g2 ON g1.name = g2.name AND g1.ceo = g2.ceo AND g1.website = g2.website AND g1.url = g2.url AND g1.id > g2.min_id
WHERE g1.area = 'Indonesia';
SELECT crunchbase_id from crunchbase_match cm WHERE b_a_id = 55885;
SELECT COUNT(*) from crunchbase_news cn where company_id  = 50704; 


SELECT COUNT(*) from crunchbase c WHERE country='Indonesia';

SELECT company_id,COUNT(*) as company_count from ph_data_bossjob.jobs j WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) group by company_id ORDER BY company_count DESC limit 30;  



SELECT c.id,c.name,c.legal_name,COUNT(j.id) as company_count
from ph_data_bossjob.companies c 
left join ph_data_bossjob.jobs j 
ON c.id = j.company_id 
WHERE j.published_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY c.id, c.name,c.legal_name
ORDER BY company_count DESC
limit 30;

SELECT j.id,j.job_title,COUNT(ja.job_id) as j_count 
from ph_data_bossjob.job_applications ja 
left join ph_data_bossjob.jobs j 
on ja.job_id = j.id 
WHERE ja.created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY j.id,j.job_title
ORDER BY j_count DESC 
limit 20;