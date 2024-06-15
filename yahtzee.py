import random  # para generar dados aleatorios
import os  # para ayudar a limpiar la pantalla
import time  # para funciones relacionadas con el tiempo


class Player:  # define la clase jugador
    def __init__(self, name):
        self.name = name  # inicializa el nombre del jugador
        self.score = 0  # inicializa el puntaje del jugador
        self.moves = {}  # inicializa un diccionario para registrar los movimientos
        self.bonus_given = False  # indica si se ha otorgado el bono
        self.yahtzee_won = False  # indica si se ha ganado el Yahtzee

    def reset(self):
        self.score = 0  # reinicia el puntaje del jugador
        self.moves = {}  # reinicia el diccionario de movimientos
        self.bonus_given = False  # reinicia el estado del bono otorgado
        self.yahtzee_won = False  # reinicia el estado de Yahtzee ganado


def roll():  # simula el lanzamiento de dados
    global current_dice  # utiliza una variable global current_dice
    current_dice = rolldie(5)  # realiza el primer lanzamiento de los dados
    replacing = []  # lista para almacenar los dados a reemplazar
    replacing_indexes = []  # lista para almacenar los índices de los dados a reemplazar
    rolls = 0  # contador de los lanzamientos realizados
    # Imprime el resultado del primer lanzamiento
    print("Tu primer lanzamiento fue:", current_dice, "\n")

    # Pregunta al usuario si quiere mantener estos dados
    result = input("¿Quieres mantener estos dados? (y o n) ")
    result = (result.lower()).strip()

    # Verifica que la respuesta sea válida (y o n)
    while result not in ("y", "n"):
        result = input(
            "\nProbablemente escribiste algo incorrecto. Intenta de nuevo. ")
        result = (result.lower().strip())

    # Si el usuario decide no mantener los dados, permite dos lanzamientos adicionales
    if result == "n":
        while rolls != 2:  # permitir solo dos lanzamientos adicionales
            if rolls != 0:  # muestra esto solo para el segundo y tercer lanzamiento
                print("Tus dados actuales son:", current_dice, "\n")
                result = input(
                    "¿Quieres mantener estos dados? (y o n) (por defecto es n) ")
                result = (result.lower()).strip()

                # Si el usuario decide mantener los dados, termina el bucle
                if result == "y":
                    break

            # Pide al usuario que ingrese los números ordinales de los dados a reemplazar
            indexes = input(
                "Escribe los números ordinales (el primero sería 1, el segundo 2, etc.)\nde los dados a reemplazar (sin espacios): ")
            try:
                replaced_dice = list(indexes)

                # Itera sobre los dados a reemplazar
                for index in replaced_dice:
                    skip = False
                    # convierte los números ordinales en índices de arreglo
                    array_index = int(index) - 1
                    # Verifica que el índice esté dentro del rango válido (0-4)
                    if array_index < 0:
                        raise IndexError(
                            "¡Ese no era un número ordinal válido!")
                    # Verifica que cada dado se reemplace solo una vez
                    while array_index in replacing_indexes:
                        print("Dado ya reemplazado. Intenta de nuevo. " +
                              str(current_dice[array_index]) + ".\n")
                        skip = True
                        break
                    if skip:
                        continue

                    # Agrega el dado a reemplazar y su índice a las listas correspondientes
                    replacing.append(current_dice[array_index])
                    replacing_indexes.append(array_index)

            except IndexError:
                print("\n¡Sólo tienes 5 dados!\n")
                replacing = []
                replacing_indexes = []
                continue
            except:
                print("\nProbablemente escribiste algo incorrecto. Intenta de nuevo.\n")
                replacing = []
                replacing_indexes = []
                continue
            # Si no se reemplazan dados, termina el bucle
            if len(replacing) == 0:
                print("Manteniendo todos los dados ...")
                break
            # Muestra los dados que se van a reemplazar
            print("Replacing", replacing, "")
            keeping = []

            # Conserva los dados que no se están reemplazando
            for index in (set([0, 1, 2, 3, 4]) - set(replacing_indexes)):
                keeping.append(current_dice[index])

            # Genera nuevos dados para reemplazar los dados seleccionados
            new_dice = rolldie(len(replacing))

            # Agrega los nuevos dados generados a los dados originales conservados
            for new_die in new_dice:
                keeping.append(new_die)

            # Actualiza los dados actuales y reinicia las listas de reemplazo
            current_dice = keeping
            replacing = []
            replacing_indexes = []
            rolls += 1
    # Imprime el resultado del último lanzamiento realizado
    print("\nTu nuevo lanzamiento fue: %s\n" % current_dice)

# Simula un lanzamiento de dados, devolviendo los dados en un arreglo


def rolldie(numToRoll):
    # opciones de los dados del 1 al 6
    diechoices = ['1', '2', '3', '4', '5', '6']
    result = []
    for x in range(numToRoll):
        # elige aleatoriamente un dado y lo agrega al resultado
        result.append(int(random.choice(diechoices)))
    return result

# Cuenta cuántos dados tienen un cierto número


def countDice(number):
    counter = 0
    for n in current_dice:
        if n == number:
            counter += 1
    # score es el número de dados del número multiplicado por el número mismo
    score = counter * number
    return score

# Función para que el jugador elija sus puntos


def choosePoints(player):
    key = allOptions[0]  # lista de opciones disponibles
    value = allOptions[1]  # lista de valores de puntos correspondientes
    # bestOption corresponde a la mejor opción (es la que tiene el máximo valor de puntos)
    bestOption = max(value)
    counter = 1
    for index in range(0, len(key)):
        if value[index] == bestOption:
            print('\033[1m' + str(counter) + ":\t", end='\033[0m')
            print('\033[1m' + str(key[index]) + ":\t" +
                  str(value[index]) + " points" + '\033[0m')
        else:
            print(str(counter) + ":\t", end="")
            print(str(key[index]) + ":\t" + str(value[index]) + " puntos.")
        counter += 1
    option = input(
        "\nAquí están todas tus opciones. Selecciona una opción ingresando su número secuencial.\n")
    while True:
        try:
            # convierte la opción seleccionada en el texto ingresado por el usuario
            option = key[int(option) - 1]
            # convierte la opción a minúsculas y elimina espacios adicionales
            option = (option.strip()).lower()
            for index in range(0, len(key)):
                # copia de la clave en minúsculas sin espacios
                keycopy = (key[index].strip(" ")).lower()
                if keycopy == option:
                    # agrega los puntos al puntaje del jugador
                    player.score += int(value[index])
                    # registra el movimiento del jugador
                    player.moves[key[index]] = int(value[index])
                    return
        except:
            option = input(
                "Probablemente escribiste algo incorrecto. Intenta de nuevo.\n")

# Función para verificar si hay Full House (tres dados de un número y dos dados de otro número)


def checkFullHouse():
    for num in current_dice:
        # verifica si hay tres dados del mismo número
        if current_dice.count(num) == 3:
            for second_num in current_dice:
                # verifica si hay dos dados de otro número
                if current_dice.count(second_num) == 2:
                    return 25  # retorna 25 puntos si hay Full House
    return 0  # retorna 0 puntos si no hay Full House

# Función para verificar si hay Tres de un tipo, Cuatro de un tipo, o Cinco de un tipo


def ofAKind(player, numOfKind):
    for number in current_dice:
        # verifica si hay numOfKind dados del mismo número
        if current_dice.count(number) == numOfKind:
            if numOfKind == 5:  # si es Yahtzee (cinco de un tipo)
                if player.yahtzee_won:  # si ya se ha ganado un Yahtzee antes
                    return 100  # retorna 100 puntos por el segundo Yahtzee
                else:  # si es el primer Yahtzee ganado
                    player.yahtzee_won = True
                    return 50  # retorna 50 puntos por el primer Yahtzee
            else:  # si es Tres de un tipo o Cuatro de un tipo
                return numOfKind * number  # retorna numOfKind veces el número del dado
    return 0  # retorna 0 puntos si no hay Tres de un tipo, Cuatro de un tipo, o Cinco de un tipo

# Función para verificar si hay una Escalera (ya sea pequeña o grande)


def checkStraight(smallOrLarge):
    # elimina duplicados y ordena los dados
    sortedArray = list(set(current_dice))
    if smallOrLarge == 1:  # si es Escalera grande
        if [1, 2, 3, 4, 5] == sortedArray or [2, 3, 4, 5, 6] == sortedArray:
            return 40  # retorna 40 puntos si es Escalera grande
    else:  # si es Escalera pequeña
        if all(x in sortedArray for x in [1, 2, 3, 4]) or all(x in sortedArray for x in [2, 3, 4, 5]) or all(x in sortedArray for x in [3, 4, 5, 6]):
            return 30  # retorna 30 puntos si es Escalera pequeña
    return 0  # retorna 0 puntos si no hay Escalera

# Función para eliminar las opciones tomadas del jugador


def removeTakenOptions(player):
    key = allOptions[0]  # lista de opciones disponibles
    value = allOptions[1]  # lista de valores de puntos correspondientes
    index = len(key) - 1
    # Elimina primero todas las opciones con valor cero
    while index >= 0:
        if "Pass          " not in key[index]:   # no elimina la opción "Pass"
            if value[index] == 0:
                del key[index]
                del value[index]
        index -= 1
    # Reúne las opciones ya tomadas
    for takenKey in player.moves.keys():
        index = len(key) - 1
        while index >= 0:
            if "Pass          " not in takenKey:  # no elimina la opción "Pass"
                if takenKey == key[index]:
                    del key[index]
                    del value[index]
            index -= 1

# Función para verificar si se alcanzó más de 63 puntos en las primeras seis categorías


def over63(player):
    if player.bonus_given:  # si ya se ha dado el bono
        return False
    sumOfFirstSix = 0
    arrayToCheck = ['Ones          ', 'Twos          ', 'Threes        ',
                    'Fours         ', 'Fives         ', 'Sixes         ']
    # categorías para sumar puntos
    if all(x in list(player.moves.keys()) for x in arrayToCheck):
        for index in arrayToCheck:
            # suma los puntos de las primeras seis categorías
            sumOfFirstSix += int(player.moves[index])
    if sumOfFirstSix >= 63:  # si se superan los 63 puntos
        player.bonus_given = True  # se da el bono
        return True
    else:
        return False

# Función para imprimir la tarjeta de puntuación del jugador


def printScoreCard(player, allOptions):
    printedBonus = True
    print("Tarjeta de Puntuación de Yahtzee")
    for key in allOptions:
        if key == "Over 63 = +35 ":  # imprime la línea del bono si está presente
            print(key + "|\t", end="")
        elif key != "Pass          ":  # imprime todas las otras opciones disponibles
            print(key + "|\t", end="")
        for k, v in player.moves.items():
            if k == key and k != "Pass          ":  # si la opción ya está tomada, imprime el valor
                print(str(v), end="")
            if key == "Over 63 = +35 ":  # si se está calculando el bono
                if over63(player):  # verifica si se superaron los 63 puntos
                    player.score += 35  # agrega el bono de 35 puntos
                if player.bonus_given and printedBonus:
                    print("35", end="")
                    printedBonus = False
        print()
    # imprime la puntuación total del jugador
    print("Puntaje acumulado: " + str(player.score))


# Función para limpiar la pantalla
def clear():
    i = 64
    mpt = ""
    while i > 0:
        print(mpt, end="\n")  # imprime líneas en blanco
        i -= 1


# Texto de bienvenida
text1 = '''
Actividad didáctica 2-M1 - Simulación
Comprender y aplicar el método de Montecarlo en una aplicación que permita su ejecución y explotación de los resultados aleatorios obtenidos.

Instrucciones
Se debe realizar un programa que simule el juego de Yatzhee clásico con 2 jugadores (Se adapta para multiples jugadores).

El juego consiste en simular hasta tres lanzamientos de cinco dados convencionales de seis caras en cada turno y sobre cuyos resultados los jugadores puede obtener puntos. La distribución de probabilidad en este caso es uniforme.
'''

print(text1)
print("Bienvenido a Yahtzee!")

# Inicio del programa: solicita al usuario el número de jugadores
num_players = int(input("Ingrese el número de jugadores: "))

# Crea una lista de objetos Player con nombres ingresados por el usuario para cada jugador
players = [Player(input(f"Ingrese el nombre del jugador {
                  i + 1}: ")) for i in range(num_players)]

# Ciclo principal del juego, se repite 3 veces (3 turnos)
for turnNumber in range(3):
    # Itera sobre cada jugador en la lista de jugadores
    for player in players:
        # Imprime un mensaje indicando el inicio del turno del jugador actual
        print(f"Comienza el turno {turnNumber + 1} de {player.name}.\n")
        # Llama a la función roll() para simular el lanzamiento de dados del jugador
        roll()
        # Define todas las opciones de puntuación disponibles para el jugador en este turno
        allOptions = [["Ones          ", "Twos          ", "Threes        ",
                       "Fours         ", "Fives         ", "Sixes         ",
                       "Over 63 = +35 ",
                       "3 of a kind   ", "4 of a kind   ", "Full House    ",
                       "Small Straight", "Large Straight", "Yahtzee       ",
                       "Chance        ", "Pass          "],
                      [countDice(1), countDice(2), countDice(3),
                          countDice(4), countDice(5), countDice(6), 0,
                          ofAKind(player, 3), ofAKind(
                              player, 4), checkFullHouse(),
                          checkStraight(0), checkStraight(
                              1), ofAKind(player, 5),
                          sum(current_dice), 0]]

        # Copia las claves de todas las opciones
        allKeys = allOptions[0].copy()
        # Elimina las opciones de puntuación ya tomadas por el jugador
        removeTakenOptions(player)
        # Permite al jugador elegir dónde aplicar los puntos obtenidos
        choosePoints(player)
        time.sleep(0.5)  # Espera medio segundo antes de continuar

        # Limpia la pantalla para la siguiente iteración del juego
        os.system('cls' if os.name == 'nt' else 'clear')

        # Imprime un mensaje indicando la finalización del turno del jugador actual
        print(f"\nSe completó el turno {turnNumber + 1} para {player.name}.")
        print("Aquí está tu Tarjeta de Puntuación actual:\n\n")
        # Imprime la tarjeta de puntuación del jugador
        printScoreCard(player, allKeys)

# Fin del juego
for player in players:
    # Imprime el puntaje final de cada jugador al finalizar el juego
    print(f"¡Fin del juego! La puntuación de {
          player.name} fue: {player.score}")

# Muestra el puntaje más alto alcanzado por algún jugador
high_score = max(players, key=lambda p: p.score)
print(f"La puntuación más alta fue {
      high_score.score} obtenida por {high_score.name}.")
