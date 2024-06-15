
CREATE DATABASE kiosco;

USE kiosco;

CREATE TABLE Productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    descripcion TEXT,
    precio DECIMAL(10, 2),
    categoria VARCHAR(50)
);

CREATE TABLE Stock (
    id_stock INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT,
    cantidad INT,
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
    
);
-- acá me di cuenta de que sería mejor poner el id de cada categoria en lugar del nombre, así que creé otra tabla en la que puse las categorias.
CREATE TABLE Categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50)
);
-- la tabla en la que van los clientes, esta me va a servir para las transacciones tambien
CREATE TABLE Clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    direccion VARCHAR(255),
    telefono VARCHAR(15)
);
-- transacciones
CREATE TABLE Transacciones (
    id_transaccion INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
);
-- acá puse los detalles especificos de la transacción
CREATE TABLE Detalle_Transaccion (
    id_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_transaccion INT,
    id_producto INT,
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    FOREIGN KEY (id_transaccion) REFERENCES Transacciones(id_transaccion),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);
-- Insertar información de ejemplo en la tabla de Productos
INSERT INTO Productos (nombre, descripcion, precio, categoria) VALUES
('oreos', 'galletitas rellenas', 900.00, 'Snacks'),
('coca-cola', 'botella de 1,5 litros de coca', 2500.00, 'Bebidas'),
('aguila', 'Barra de chocolate', 3600.00, 'Snacks'),
('Agua', 'Botella de agua mineral', 600.00, 'Bebidas');

INSERT INTO Clientes (nombre, direccion, telefono) VALUES
('Jere', 'Calle lalala', '111222333'),
('Fede', 'Avenida lalala', '111222333'),
('Tatiana', 'calle lalala-la', '111222333');

-- Insertar información de ejemplo en la tabla de Stock
INSERT INTO Stock (id_producto, cantidad) VALUES
(1, 20),
(2, 40),
(3, 30),
(4, 40);

INSERT INTO Categorias (nombre) VALUES
('Snack'),
('Bebida'),
('Otros');

ALTER TABLE Productos
ADD COLUMN id_categoria INT,
ADD FOREIGN KEY (id_categoria) REFERENCES Categorias(id_categoria);

UPDATE Productos SET id_categoria = 1 WHERE nombre = 'oreos';
UPDATE Productos SET id_categoria = 2 WHERE nombre = 'coca-cola';
UPDATE Productos SET id_categoria = 1 WHERE nombre = 'aguila';
UPDATE Productos SET id_categoria = 2 WHERE nombre = 'Agua';

INSERT INTO Transacciones (id_cliente) VALUES
(1), -- yo
(2), -- Fede
(3); -- Tatiana


-- detalles de las transacciones
INSERT INTO Detalle_Transaccion (id_transaccion, id_producto, cantidad, precio_unitario) VALUES
(@transaccion_jere, 1, 2, 2.50), -- yo compre 2 oreos
(@transaccion_fede, 2, 1, 1.20), -- fede compro una coca
(@transaccion_fede, 3, 2, 1.00), -- fede compro dos aguilas
(@transaccion_tatiana, 4, 3, 0.80); -- Tatiana compro 3 Aguas


