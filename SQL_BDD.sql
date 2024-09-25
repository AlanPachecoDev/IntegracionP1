CREATE DATABASE IF NOT EXISTS BDD_Integracion_1P;

USE BDD_Integracion_1P;

CREATE TABLE IF NOT EXISTS Ventas_Consolidadas (
    IdTransaccion INT,
    IdLocal INT,
    Fecha DATETIME,
    IdCategoria INT,
    IdProducto INT,
    Producto VARCHAR(50),
    Cantidad INT,
    PrecioUnitario DECIMAL(10, 2),
    TotalVenta DECIMAL(10, 2),
    PRIMARY KEY (IdTransaccion, IdLocal) -- Definición de la clave primaria combinada
);

