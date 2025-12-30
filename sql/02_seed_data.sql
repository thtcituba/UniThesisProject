/* ===========================
   02_seed_data.sql
   =========================== */

-- AUTHOR
INSERT INTO dbo.AUTHOR (A_NAME, A_PHONE) VALUES
('Ali DOLANER', '05053331112'),
('Deniz DURUCA', '05072121514'),
('Kerem ONAR', '05096441752'),
('Aynur PINARCI', '05123869907'),
('Celal ILGAZ', '05047861332');
GO

-- UNIVERSITY
INSERT INTO dbo.UNIVERSITY (UNI_NAME, UNI_RECTOR_NAME, UNI_ADDRESS, UNI_PHONE) VALUES
('Bilkent University', 'Mehmet RAUF', NULL, NULL),
('Ankara University', 'Peyami SAFA', NULL, NULL),
('Okan University', 'Arif Nihat ASYA', NULL, NULL),
('Hacettepe University', 'Halide Edib ADIVAR', NULL, NULL),
('Istanbul University', 'Orhan KEMAL', NULL, NULL);
GO

-- INSTITUTE  (UNI_ID'ler identity(100,1) olduğu için: 100,101,102,...)
INSERT INTO dbo.INSTITUTE (INS_NAME, INS_DEANNAME, UNI_ID) VALUES
('Fine Arts Institute', 'Osman CEMAL', 100),
('Health Sciences Institute', 'Ceyhun Atıf KANSU', 101),
('Social Sciences Institute', 'Selin SABA', 102),
('Education Sciences Institute', 'Refik Halit KARAY', 103),
('Engineering and Natural Sciences Institute', 'Nezihe ARAZ', 104);
GO

-- SUPERVISOR
INSERT INTO dbo.SUPERVISOR (S_NAME) VALUES
('Faik Ali OZANSOY'),
('Ceren AKBAL'),
('Turgut UYAR'),
('Sait Faik ABASIYANIK'),
('Yahya Kemal BEYATLI');
GO

-- THESIS
INSERT INTO dbo.THESIS
(T_TITLE, T_ABSTRACT, T_TOPIC, T_KEYWORD, T_YEAR, T_TYPE, T_INSTITUTE, T_PAGE, T_LANGUAGE, T_SUBDATE, A_ID, UNI_ID, S_ID)
VALUES
('Burnout Syndrome',
 'Burnout Syndrome and related factors in medical doctors',
 'Family Medicine',
 NULL, 2016, 'Specialization in Medicine',
 'Medicine Institute', 243, 'English', '2016-03-12',
 1, 100, 1);

INSERT INTO dbo.THESIS
(T_TITLE, T_ABSTRACT, T_TOPIC, T_KEYWORD, T_YEAR, T_TYPE, T_INSTITUTE, T_PAGE, T_LANGUAGE, T_SUBDATE, A_ID, UNI_ID, S_ID)
VALUES
('An Investigation Regarding Obesity Perception',
 'Investigation of the effect of the medical faculty education on obesity perception of medical students',
 'Internal Diseases',
 'obesity', 2022, 'Specialization in Medicine',
 'Medicine Institute', 176, 'English', '2022-12-10',
 2, 101, 2);
GO
