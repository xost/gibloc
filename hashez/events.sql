select E.eventType,
       E.result,
       E.registred,
       E.badFiles_id,
       count(F.id)
from hashez_event E left join hashez_file F on E.fileSet_id=F.fileSet_id
where E.client_id=3;

select E.eventType,
       E.result,
       E.registred,
       E.badFiles_id,


SELECT E.eventType,
       E.result,
       E.registred,
       E.badFiles_id,
       (
         SELECT count(*)
         FROM hashez_file F
         WHERE F.fileSet_id=E.fileSet_id
       ) as files_count
FROM hashez_event E
WHERE E.client_id=3;
