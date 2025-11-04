import * as SQLite from 'expo-sqlite';

const db = SQLite.openDatabase('productos.db');

export const initDB = () => {
  return new Promise((resolve, reject) => {
    db.transaction(tx => {
      tx.executeSql(
        'CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, precio REAL NOT NULL, cantidad INTEGER NOT NULL);',
        [],
        () => resolve(),
        (_, error) => reject(error)
      );
    });
  });
};

export const insertarProducto = (nombre, precio, cantidad) => {
  return new Promise((resolve, reject) => {
    db.transaction(tx => {
      tx.executeSql(
        'INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?);',
        [nombre, precio, cantidad],
        (_, { insertId }) => resolve(insertId),
        (_, error) => reject(error)
      );
    });
  });
};

export const obtenerProductos = () => {
  return new Promise((resolve, reject) => {
    db.transaction(tx => {
      tx.executeSql(
        'SELECT * FROM productos;',
        [],
        (_, { rows: { _array } }) => resolve(_array),
        (_, error) => reject(error)
      );
    });
  });
};

export const actualizarProducto = (id, nombre, precio, cantidad) => {
  return new Promise((resolve, reject) => {
    db.transaction(tx => {
      tx.executeSql(
        'UPDATE productos SET nombre = ?, precio = ?, cantidad = ? WHERE id = ?;',
        [nombre, precio, cantidad, id],
        () => resolve(),
        (_, error) => reject(error)
      );
    });
  });
};

export const eliminarProducto = (id) => {
  return new Promise((resolve, reject) => {
    db.transaction(tx => {
      tx.executeSql(
        'DELETE FROM productos WHERE id = ?;',
        [id],
        () => resolve(),
        (_, error) => reject(error)
      );
    });
  });
};