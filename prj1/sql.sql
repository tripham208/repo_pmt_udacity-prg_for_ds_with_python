/*Query-1
 we need find top 10 Top 10 country by number customer
*/

select count(country) as number_customer, country
from customer as c
         join address a on c.address_id = a.address_id
         join city cty on a.city_id = cty.city_id
         join country ctry on cty.country_id = ctry.country_id
group by country
order by number_customer desc
limit 10;

/*Query-2
 We need to know what genres are rented the most to expand
*/

WITH table1
         AS (SELECT *
             FROM rental AS r
                      join inventory AS i
                           ON i.inventory_id = r.inventory_id
                      JOIN film AS f
                           ON i.film_id = f.film_id
                      JOIN film_category AS fc
                           ON f.film_id = fc.film_id
                      JOIN category AS c
                           ON fc.category_id = c.category_id)

SELECT DISTINCT(name)                                    as category,
               COUNT(rental_id) OVER (PARTITION BY name) AS num_film_rent
from table1
order by num_film_rent desc
limit 5;

/*Query-3
 We need to compare the sales in 2005 of the two stores
*/

SELECT DATE_PART('month', re.rental_date) AS rent_month,
       DATE_PART('year', re.rental_date)  AS rent_year,
       i.store_id                         AS store_id,
       sum(amount)                        AS amount_rent

FROM rental AS re
         JOIN payment AS pm
              ON re.rental_id = pm.rental_id
         join inventory as i
              ON i.inventory_id = re.inventory_id
where DATE_PART('year', re.rental_date) = 2005
GROUP BY 1,
         2,
         3

ORDER BY 1;

/*Query-4
 we need to know detail time rent in top 3 most category :
 - <=3 days is short
 - <=6 days is medium
 - >6 days is long
*/

with tbl1 as (select DATE_PART('day', re.return_date - re.rental_date) as days,
                     inventory_id
              from rental AS re)
        ,
     tbl2 as (SELECT name,
                     case
                         when days <= 3 then 'short'
                         when days > 3 and days <= 6 then 'medium'
                         else 'long'
                         end as type
              FROM tbl1 AS r
                       join inventory AS i
                            ON i.inventory_id = r.inventory_id
                       JOIN film AS f
                            ON i.film_id = f.film_id
                       JOIN film_category AS fc
                            ON f.film_id = fc.film_id
                       JOIN category AS c
                            ON fc.category_id = c.category_id
              where days is not null),
     tbl3 as (SELECT name, count(name) as num
              from tbl2
              group by name
              order by num desc
              limit 3)

SELECT name,
       type,
       COUNT(type) as time_film_rent

from tbl2
where name in (select name from tbl3)
group by name, type
order by name