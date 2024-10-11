"""
Programación 9292
Práctica 2 - Centro de llamadas
autor: Jiménez Malvaez Raúl Emilio
"""
#importamos la clase random, que nos será útil para la simulación
import random

#Creamos una clase cola, donde "almacenaremos" a los elementos (clientes) que esperan ser atendidos
class Cola:
    #Con la función __init__(), inicializamos la cola
    def __init__(self):
        self.elementos = []

    #Con la función cola_vacia(), determinamos si hay elementos (clientes) en espera de ser atendidos
    def cola_vacia(self):
        return len(self.elementos) == 0

    #Con la función agregar(), insertamos elementos (clientes) a la cola
    def agregar(self,elemento):
        self.elementos.append(elemento)

    #Con la función eliminar(), quitamos el elemento (cliente) más antiguo (izquierda) de la cola
    def eliminar(self):
        return self.elementos.pop(0)
    
    #Con la función tamaño(), extraemos la cantidad de elementos (clientes) en la clase Cola
    def tamaño(self):
        return len(self.elementos)


#Definimos la clase Cliente, junto a la cuál definimos sus atributos (características)
class Cliente:
    #Con la función __init__(), inicializamos al cliente
    def __init__(self,tiempo_llegada,premier = False):
        #Definimos el tiempo de llegada del cliente
        self.tiempo_llegada = tiempo_llegada
        #Definimos el tiempo que tiene que esperar, la función random es válida pues cada número entre 1 y 81
        #tiene la misma probabilidad de ser seleccionado, lo que cumple con ser una probabilidad uniforme
        self.tiempo_atencion = random.randint(1,81)
        #Definimos al cliente del segmento premier
        self.premier = premier
        #Definimos en que momento se le comienza a dar atención al cliente
        self.inicio_atencion = None

#Por último, definimos la clase Operador
class Operador:
    #Con la función __init__(): inicializamos al Operador y definimos si puede atender al cliente
    def __init__(self):
        self.disponible = True

#Una vez definidas todas nuestras clases: Cola, CLiente, Operador, debemos simular la atencion al cliente
#Asumimos que la cantidad de clientes esperados es de 1000
def simulacion(lineas_atencion, cantidad_clientes = 1000):
    #Separamos a los clientes en dos colas: principal, y su segmento premier
    cola_principal = Cola()
    cola_premier = Cola()
    #Inicialmente el tiempo debe ser cero, y va aumentando conforme llegan clientes y estos son atendidos
    tiempo = 0
    #Este es el tiempo que un cliente premier debe esperar
    tiempo_espera_premier = []
    #Utilizamos esta variable para definir a los operadores totales que hay, es decir cada línea de atención
    operadores = [Operador() for i in range(lineas_atencion)]

    #Definimos los atributos de cada cliente y los almacenamos en una lista
    clientes = []
    for i in range(cantidad_clientes):
        #Esto nos dice tras cuanto tiempo llegó el cliente, en un lapso entre 1 y 3 minutos
        tiempo_llegada = tiempo + random.randint(1,3)
        #Segmenta a los clientes, siendo que 1 de cada 6 es premier
        premier = random.random()<(1/6)
        #Agrega a los clientes a su respectivo segmento de acuerdo a su llegada y su status
        clientes.append(Cliente(tiempo_llegada,premier))
        #El tiempo se modifica para cada cliente
        tiempo = tiempo_llegada

    #Finalmente, realizamos la simulacion, donde asignaremos a cada cliente a su respectivo segmento
    #Enviamos a la cola a los clientes que no puedan ser atendidos.
    espera_maxima_premier = 0
    #Este ciclo se ejecuta mientras haya clientes que esperen ser atendidos
    while clientes:
        #Mientras haya clientes y el cliente lleve más tiempo en espera, se extrae y se envía a una cola
        while clientes and clientes[0].tiempo_llegada <= tiempo:
            cliente = clientes.pop(0)
            #Si es premier lo enviamos al segmento premier
            if cliente.premier:
                cola_premier.agregar(cliente)
            #De lo contrario, se mantiene en la cola principal
            else:
                cola_principal.agregar(cliente)

        #A cada operador disponible se le asigna un cliente, primero de la cola premier
        for operador in operadores:
            if operador.disponible:
                if not cola_premier.cola_vacia():
                    cliente = cola_premier.eliminar()
                elif not cola_principal.cola_vacia():
                    cliente = cola_principal.eliminar()

                #Modelamos el tiempo que se le atiende al cliente
                #Para esto tomamos en cuenta el momento en que llega y el tiempo que se atiende
                operador.disponible = False
                cliente.inicio_atencion = tiempo
                tiempo_fin_atencion = cliente.inicio_atencion + cliente.tiempo_atencion
                
                #Para los clientes premier calculamos cuanto tiempo tardan en atenderles
                if cliente.premier:
                    tiempo_espera = cliente.inicio_atencion -cliente.tiempo_llegada
                    espera_maxima_premier = max(espera_maxima_premier, tiempo_espera)
        
        #Aumentamos el tiempo transcurrido en 1 minuto para cada iteración
        tiempo_espera += 1
    #Finalmente obtenemos el tiempo de espera maxima del cliente premier
    return espera_maxima_premier, tiempo_espera_premier

#Incorporamos un __main__ de manera que el codigo no se ejecutará como modulo
if __name__ == "__main__":
    #Y modelamos la simulación para distintos números de líneas de atención
    for lineas_atencion in range(19,25):
        espera_maxima_premier, tiempo_espera_premier = simulacion(lineas_atencion)
        #Imprimimos el resultado para cada iteración
        print(f"Número de líneas: {lineas_atencion}")
        print(f"Tiempo de espera máximo premier: {espera_maxima_premier}" " minutos")
        #Y colocamos una linea a modo de separador entre cada escenario
        print("-" * 40)

print("Fin de la simulación")