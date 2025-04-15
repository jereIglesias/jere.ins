-- Crear tabla provincias  
CREATE TABLE IF NOT EXISTS provincias (  
    ID INTEGER PRIMARY KEY AUTOINCREMENT,  
    Nombre TEXT NOT NULL  
);  

-- Crear tabla ciudades  
CREATE TABLE IF NOT EXISTS ciudades (  
    ID INTEGER PRIMARY KEY AUTOINCREMENT,  
    CodPostal TEXT,  
    CPA TEXT,  
    Nombre TEXT NOT NULL,  
    IDProvincia INTEGER,  
    FOREIGN KEY (IDProvincia) REFERENCES provincias(ID) ON DELETE CASCADE  
);  

-- Insertar provincias  
INSERT INTO provincias (Nombre) VALUES ('Buenos Aires');  
INSERT INTO provincias (Nombre) VALUES ('Córdoba');  
INSERT INTO provincias (Nombre) VALUES ('Santa Fe');  
INSERT INTO provincias (Nombre) VALUES ('San Luis');  

-- Insertar ciudades de Buenos Aires  
INSERT INTO ciudades (CodPostal, CPA, Nombre, IDProvincia) VALUES ('1000', 'BAA', 'Buenos Aires', 1);  
INSERT INTO ciudades (CodPostal, CPA, Nombre, IDProvincia) VALUES ('1900', 'BAS', 'La Plata', 1);  
INSERT INTO ciudades (CodPostal, CPA, Nombre, IDProvincia) VALUES ('1600', 'BAM', 'Morón', 1);  
INSERT INTO ciudades (CodPostal, CPA, Nombre, IDProvincia) VALUES ('8000', 'BAS', 'Bahía Blanca', 1);  
INSERT INTO ciudades (CodPostal, CPA, Nombre, IDProvincia) VALUES ('7000', 'BAS', 'Tandil', 1);  

-- Insertar ciudades de Córdoba  
INSERT INTO ciudades (CodPostal, CPA, Nombre, IDProvincia) VALUES ('5000', 'CCO', 'Córdoba', 2);  
INSERT INTO ciudades (CodPostal, CPA, Nombre, IDProvincia) VALUES ('5800', 'CNO', 'Río Cuarto', 2);  
INSERT INTO ciudades (CodPostal, CPA, Nombre, IDProvincia) VALUES ('5900', 'CNO', 'San Francisco', 2);  

-- Insertar ciudades de Santa Fe  
INSERT INTO ciudades (CodPostal, CPA, Nombre, IDProvincia) VALUES ('3000', 'SFE', 'Rosario', 3);  
INSERT INTO ciudades (CodPostal, CPA, Nombre, IDProvincia) VALUES ('2000', 'SFE', 'Santa Fe', 3);  

-- Insertar ciudades de San Luis  
INSERT INTO ciudades (CodPostal, CPA, Nombre, IDProvincia) VALUES ('5700', 'SLU', 'San Luis', 4);  
INSERT INTO ciudades (CodPostal, CPA, Nombre, IDProvincia) VALUES ('5700', 'SLU', 'Villa Mercedes', 4);