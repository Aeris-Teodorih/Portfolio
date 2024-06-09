--Найдите количество занятых мест для каждого рейса, процентное отношение 
--количества занятых мест к общему количеству мест в самолете, добавьте 
--накопительный итог вывезенных пассажиров по каждому аэропорту на каждый день
with cc as (select ad.aircraft_code, count(seat_no) as "seats_total"
			from seats s 
			join aircrafts ad on ad.aircraft_code = s.aircraft_code
			group by ad.aircraft_code )
select f.flight_no, count(bp.seat_no) as "seats_used", cc.seats_total,
	   round((cast(count(bp.seat_no) as decimal) / cast(cc.seats_total as decimal))*100,0)  as "percent,%", 
	   f.actual_departure, f.departure_airport,
	   sum(count(bp.seat_no)) over (partition by f.departure_airport, date_trunc('day',f.actual_departure::date)) 	   as "cumulative_day",
	   sum(count(bp.seat_no)) over (partition by f.departure_airport, date_trunc('day',f.actual_departure::date) order by f.actual_departure) as "step_day"
from boarding_passes bp 
join flights f on f.flight_id = bp.flight_id
join cc on cc.aircraft_code = f.aircraft_code
group by f.flight_no, f.departure_airport, f.actual_departure, cc.seats_total
order by 6, 5
limit 600