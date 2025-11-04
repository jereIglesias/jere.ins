# Aplicación CRUD con React Native y SQLite

Esta es una aplicación móvil simple que implementa operaciones CRUD (Crear, Leer, Actualizar, Eliminar) utilizando SQLite como base de datos local.

## Características

- Creación de productos con nombre, precio y cantidad
- Visualización de productos en una lista
- Actualización de productos existentes
- Eliminación de productos con confirmación
- Persistencia de datos usando SQLite
- Navegación entre pantallas
- Interfaz de usuario limpia y sencilla

## Estructura del Proyecto

- `/screens`
  - `ListaProductos.js` - Pantalla principal que muestra la lista de productos
  - `FormularioProducto.js` - Formulario para crear/editar productos
- `/database`
  - `db.js` - Configuración y operaciones de la base de datos SQLite

## Cómo ejecutar el proyecto

1. Asegúrate de tener instalado Node.js y Expo CLI
2. Clona este repositorio
3. Ejecuta `npm install` para instalar las dependencias
4. Ejecuta `npx expo start` para iniciar el proyecto
5. Usa la aplicación Expo Go en tu dispositivo móvil o un emulador para ver la aplicación