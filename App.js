import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import ListaProductos from './screens/ListaProductos';
import FormularioProducto from './screens/FormularioProducto';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator 
        initialRouteName="ListaProductos"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#f4511e',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen 
          name="ListaProductos" 
          component={ListaProductos} 
          options={{ title: 'Lista de Productos' }}
        />
        <Stack.Screen 
          name="FormularioProducto" 
          component={FormularioProducto} 
          options={{ title: 'Producto' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}