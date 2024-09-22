-- List Glam rock bands and their lifespan until 2022
SELECT 
    DISTINCT band_name,
    CASE
        WHEN split IS NOT NULL AND YEAR(split) >= YEAR(formed) THEN YEAR(split) - YEAR(formed)
        ELSE 2022 - YEAR(formed)
    END AS lifespan
FROM 
    metal_bands
WHERE 
    main_style = 'Glam rock'
    AND formed IS NOT NULL
ORDER BY 
    lifespan DESC;
