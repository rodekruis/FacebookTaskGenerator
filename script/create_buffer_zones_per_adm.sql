--select * from hrsl_poly limit 10;
--select * from admin3mwi limit 10;

--explain select * from hrsl_poly where admin3 = 'AFRMWI30304';


/*
CREATE INDEX hrsl_poly_wkb_geometry_geom_idx
  ON public.hrsl_poly
  USING gist
  (wkb_geometry);

CREATE INDEX hrsl_poly_admin3_idx
  ON public.hrsl_poly
  (admin3);
*/


select * from testbuf;

--CREATE SEQUENCE testbuf_id_seq CYCLE;


DROP TABLE testbuf;
CREATE TABLE testbuf AS
--EXPLAIN
SELECT 
  nextval('testbuf_id_seq'::regclass) AS id,
  (st_dump(
    st_transform(
      st_intersection(
        st_union(
          st_buffer(
            st_intersection(
	      st_transform(hrsl.wkb_geometry, 32736), st_transform(adm.wkb_geometry, 32736)
            )
          , 40, 2)
        )
        , min(st_transform(adm.wkb_geometry, 32736))::geometry
      )
    , 4326) )).geom AS geometry,
  --(st_dump(st_intersection(st_transform(st_union(st_buffer(st_transform(hrsl.wkb_geometry, 32736), 40, 2)), 4326), st_union(adm.wkb_geometry)))).geom AS geometry,
  --st_intersection(st_transform(st_union(st_buffer(st_transform(hrsl.wkb_geometry, 32736), 40)), 4326), st_union(adm.wkb_geometry)).geom as geometry,
  hrsl.admin3 AS admin3,
  min(adm.district) AS district
FROM 
  hrsl_poly hrsl
LEFT JOIN admin3mwi adm ON hrsl.admin3 = adm.p_code /*AND ST_INTERSECTS(hrsl.wkb_geometry, adm.wkb_geometry)*/
/*WHERE
  hrsl.admin3 IN ('AFRMWI31439',
    'AFRMWI31440', 
    'AFRMWI31441', 
    'AFRMWI31442', 
    'AFRMWI31437'--,
    --'AFRMWI30304',
    --'AFRMWI30306'
    )*/
GROUP BY hrsl.admin3
--LIMIT 10;



