import React, { useState, useEffect } from 'react';
import { 
  View, 
  TextInput, 
  StyleSheet, 
  TouchableOpacity, 
  Text, 
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView
} from 'react-native';
import { insertarProducto, actualizarProducto } from '../database/db';

export default function FormularioProducto({ route, navigation }) {
  const productoExistente = route.params?.producto;
  const [nombre, setNombre] = useState('');
  const [precio, setPrecio] = useState('');
  const [cantidad, setCantidad] = useState('');

  useEffect(() => {
    if (productoExistente) {
      setNombre(productoExistente.nombre);
      setPrecio(productoExistente.precio.toString());
      setCantidad(productoExistente.cantidad.toString());
    }
  }, [productoExistente]);

  const validarCampos = () => {
    if (!nombre.trim()) {
      Alert.alert('Error', 'El nombre es requerido');
      return false;
    }
    if (!precio.trim() || isNaN(precio) || parseFloat(precio) <= 0) {
      Alert.alert('Error', 'El precio debe ser un número válido mayor a 0');
      return false;
    }
    if (!cantidad.trim() || isNaN(cantidad) || parseInt(cantidad) < 0) {
      Alert.alert('Error', 'La cantidad debe ser un número válido mayor o igual a 0');
      return false;
    }
    return true;
  };

  const guardarProducto = async () => {
    if (!validarCampos()) return;

    try {
      if (productoExistente) {
        await actualizarProducto(
          productoExistente.id,
          nombre,
          parseFloat(precio),
          parseInt(cantidad)
        );
      } else {
        await insertarProducto(
          nombre,
          parseFloat(precio),
          parseInt(cantidad)
        );
      }
      navigation.goBack();
    } catch (error) {
      console.error(error);
      Alert.alert('Error', 'No se pudo guardar el producto');
    }
  };

  return (
    <KeyboardAvoidingView 
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      style={styles.container}
    >
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <View style={styles.inputContainer}>
          <Text style={styles.label}>Nombre:</Text>
          <TextInput
            style={styles.input}
            value={nombre}
            onChangeText={setNombre}
            placeholder="Ingrese el nombre del producto"
          />
        </View>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>Precio:</Text>
          <TextInput
            style={styles.input}
            value={precio}
            onChangeText={setPrecio}
            placeholder="Ingrese el precio"
            keyboardType="decimal-pad"
          />
        </View>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>Cantidad:</Text>
          <TextInput
            style={styles.input}
            value={cantidad}
            onChangeText={setCantidad}
            placeholder="Ingrese la cantidad"
            keyboardType="number-pad"
          />
        </View>

        <TouchableOpacity 
          style={styles.button}
          onPress={guardarProducto}
        >
          <Text style={styles.buttonText}>
            {productoExistente ? 'Actualizar' : 'Guardar'}
          </Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollContainer: {
    padding: 20,
  },
  inputContainer: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    marginBottom: 5,
    color: '#333',
  },
  input: {
    backgroundColor: '#fff',
    padding: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#ddd',
    fontSize: 16,
  },
  button: {
    backgroundColor: '#f4511e',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 20,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});