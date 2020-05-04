#----------------------------------------------------------------------
#  chatbot.py
#
#  Una implementación sencilla de un chatbot
#  basado en intents y expresiones regulares
#  por: Arenas Ayala Ramón, Lugo Cano Daniel y Millán Pimentel Óscar Fernando
#----------------------------------------------------------------------

import string
import re
import random
from random import randrange

class chatbot:
    def __init__(self):
        '''
        El chatbot consta de una base de conocimiento representada como una lista de casos o intents

        '''
        self.conocimiento = [] # la base de conocimiento, representan los diferentes casos o intents
        for caso in conocimiento:
            caso['regex'] = list(map(lambda x:re.compile(x, re.IGNORECASE), caso['regex'])) # compilar las expresiones regulares es óptimo cuando se usan varias veces
            self.conocimiento.append(caso)
        # self.regexp_match

    def responder(self, user_input):
        '''
        Flujo básico para identificar coincidencias de intents para responder al usuario.
        Con el texto del usuario como parámetro, los paso a realizarse son:
        1. Encontrar el caso de la base de conocimiento usando expresiones regulares
        2. Si es necesario, realizar acciones asociadas al intent (por ejemplo: consultar información adicional)
        3. Seleccionar una respuesta de la lista de respuestas según el caso del intent
        4. Si es necesario, identificar los parámetros o entidades del texto para dar formato a la respuesta seleccionada
        5. Devolver la respuesta

        :param str user_input: El texto escrito por el usuario
        :return Un texto de respuesta al usuario
        :rtype: str
        '''
        caso = self.encontrar_intent(user_input)
        self.identifica_contexto(caso) # Asignar contexto, es auxiliar para identificar ciertos casos particulares
        informacion_adicional = self.acciones(caso, user_input)
        respuesta = self.convertir_respuesta(random.choice(caso['respuesta']), caso, user_input)
        respuesta_final = (respuesta + '\n' + informacion_adicional).strip() # Strip quita espacios en blanco al inicio y final del texto
        return respuesta_final

    def encontrar_intent(self, user_input):
        '''
        Encuentra el caso o intent asociado en la base de conocimiento

        :param str user_input: El texto escrito por el usuario
        :return El diccionario que representa el caso o intent deseado
        :rtype: str
        '''
        for caso in self.conocimiento:
            for regularexp in caso['regex']:
                match = regularexp.match(user_input)
                if match:
                    self.regexp_selected = regularexp # Asignar esta propiedad es útil para acceder rápidamente a la expresión regular del match
                    return caso
        return {}

    def convertir_respuesta(self, respuesta, caso, user_input):
        '''
        Cambia los textos del tipo %1, %2, %3, etc., por su correspondiente propiedad
        identificada en los grupos parentizados de la expresión regular asociada.

        :param str respuesta: Una respuesta que desea convertirse
        :param dict caso: El caso o intent asociado a la respuesta
        :param str user_input: El texto escrito por el usuario
        :return La respuesta con el cambio de parámetros
        :rtype: str
        '''
        respuesta_cambiada = respuesta
        intent = caso['intent']
        match = self.regexp_selected.match(user_input)
        if intent == 'hacer pedido':
            respuesta_cambiada = respuesta_cambiada.replace('%1', match.group(1))
        return respuesta_cambiada

    def acciones(self, caso, user_input):
        '''
        Obtiene información adicional necesaria para dar una respuesta coherente al usuario.
        El tipo de acciones puede ser una consulta de información, revisar base de datos, generar
        un código, etc. y el resultado final es expresado como una cadena de texto

        :param dict caso: El caso o intent asociado a la respuesta
        :return Texto que representa información adicional para complementar la respuesta al usuario
        :rtype: str
        '''
        intent = caso['intent']
        if intent == 'dar categorias':
            return self.get_categorias()
        # elif intent == 'confirmar pizza':
        #     return self.generar_ticket()
        elif intent == 'confirmar':
            return self.da_respuesta_apropiada(user_input) # TODO
        return ''

    def identifica_contexto(self, caso):
        intent = caso['intent']
        if intent == 'hacer pedido':
            self.contexto = 'PIZZA'
        elif intent == 'confirmar pedido': # TODO
            self.contexto = 'PEDIDO'

    def da_respuesta_apropiada(self, user_input):
        if self.contexto == 'PIZZA':
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT' # Devolver el contexto a default para que el siguiente Sí/No ya no tenga que ver con las pizzas
                return 'Ok, se ha confirmado la pizza que deseas'
            else:
                self.contexto = 'DEFAULT' # Devolver el contexto a default para que el siguiente Sí/No ya no tenga que ver con las pizzas
                return 'Orden de pizza cancelado'
        elif self.contexto == 'PEDIDO': # Sería análogo al caso de las pizzas
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT' # Devolver el contexto a default para que el siguiente Sí/No ya no tenga que ver con las pizzas
                return 'Ok, se ha confirmado tu pedido\n' + generar_ticket()
            else:
                self.contexto = 'DEFAULT' # Devolver el contexto a default para que el siguiente Sí/No ya no tenga que ver con las pizzas
                return 'Bien, tú orden sigue pendiente de ser confirmada'
        elif self.contexto == 'DEFAULT':
            return 'No comprendí lo que dices. ¿Qué necesitas?'
        else:
            return 'No comprendí lo que dices. ¿Qué necesitas?'

    def generar_ticket(self):
        return 'Tu pedido es el número: {}'.format(randrange(0, 15))

    def get_categorias(self):
        '''
        Devuelve la lista de categorias en el mini super, junto con cada producto
        Representa un ejemplo de consulta de información o acciones en el flujo
        para construir una respuesta del chatbot
        :return Texto de las categorias disponibles
        :rtype str
        '''
        lista_productos = []
        for productos in categorias:
            lista_productos.append(productos['nombre'].title())
        respuesta = ', '.join(lista_productos)
        if not respuesta:
            return 'Por el momento no tenemos disponible las categorias'
        return respuesta

#----------------------------------------------------------------------
# Basse de conocimiento
# La base de conocimiento representa una lista de todos los casos o intents
# que el chatbot será capaz de identificar.
#
# Cada caso o intent es un diccionario que incluye los siguientes keys (propiedades):
# - intent: Nombre para identificar el intent
# - regex: Lista de posibles expresiones regulares asociadas al intent, donde los parámetros se obtienen del texto parentizado en la expresión regular
# - respuesta: Lista de posibles respuestas al usuario, indicando los parámetros obtenidos con la notación %1, %2, %3, etc para cada parámetro
#----------------------------------------------------------------------
conocimiento = [
    {
        'intent': 'hacer pedido',
        'regex': [
            r'Quiero hacer un pedido (.*)',
            r'.*pedido.*'
        ],
        'respuesta': [
            '¿Deseas realizar un pedido %1?',
            'Para verificar, ¿Quieres realizar una orden %1?'
        ]
    },
    {
        'intent': 'bienvenida',
        'regex': [
            r'.*Hola.*',
            r'.*Buen(a|o)s (días|tardes|noches).*',
        ],
        'respuesta': [
            'Bienvenido, ¿Qué deseas ordenar?',
            'Hola, ¿Cómo te puedo ayudar?'
        ]
    },
    {
        'intent': 'dar categorias',
        'regex': [
            r'(Qué|Cuál|Dime|Dame).* (categorias).*',
            r'(Qué|Cuáles) .* categorias*.*'
        ],
        'respuesta': [
            'Te daré el las categorias con las que contamos en este momento',
            'Estos son las categorias que tenemos en el mini super',
            'El mini super cuenta con las siguientes categorias'
        ]
    },
    {
        'intent': 'confirmar',
        'regex': [
            r'Sí',
            r'Si',
            r'No',
            r'No sé',
            r'No se'
        ],
        'respuesta': [
            '' # A priori no se puede dar una respuesta, se debe considerar el contexto (ver la función self.da_respuesta_apropiada())
        ]
    },
    # {
    #     'intent': 'confirmar pizza',
    #     'regex': [
    #         r'(Sí|Si)'
    #     ],
    #     'respuesta': [
    #         'Ok'
    #     ]
    # },
    # {
    #     'intent': 'cancelar pizza',
    #     'regex': [
    #         r'NO',
    #         r'(No sé|No se|nose)'
    #     ],
    #     'respuesta': [
    #         'Está bien, entonces qué quieres?',
    #         'Bien, cancelado'
    #     ]
    # },
    {
        'intent': 'desconocido',
        'regex': [
            r'.*'
        ],
        'respuesta': [
            'No te entendí ¿Puedes repetirlo por favor? ',
            'Disculpa, no comprendí lo que dices',
            '¿Puedes decir lo mismo con otras palabras?'
        ]
    }
]

#----------------------------------------------------------------------
# Diccionario que representan las categorias del supermercado en el area de abarrotes
# Ejemplo de información que podría consultarse de manera externa,
# ser generada, o auxiliar en la redacción de una respuesta del chatbot.
#----------------------------------------------------------------------
categorias = [
    {
        'nombre': 'lacteos',
        'productos': ['leche', 'yogurt', 'queso manchego', 'queso oaxaca', 'queso panela', 'crema']
    },
    {
        'nombre': 'enlatados',
        'prodcutos': ['atun', 'frijoles', 'elotes', 'champiñones']
    },
    {
        'nombre': 'botanas',
        'productos': ['cheetos', 'fritos', 'tostitos', 'doritos', 'chips', 'ruffles', 'sabritas', 'paketaxo']
    },
    {
        'nombre': 'galletas',
        'productos': ['chokis', 'emperador', 'principe', 'marias', 'arcoiris', 'canelitas', 'polvorones', 'saladitas']
    },
    {
        'nombre': 'pan',
        'productos': ['pan blanco', 'pan integral', 'pan tostado', 'bimbollos', 'medias noches', 'donas', 'mantecadas', 'panque', 'choco roles']
    },
    {
        'nombre': 'cerelaes',
        'productos': ['avena', 'chocokrispis', 'zucaritas', 'kellogs', 'corn pops', 'trix', 'cheerios', 'all bran', 'froot loops']
    },
    {
        'nombre': 'licores',
        'productos': ['jose cuervo', 'carta blanca', 'bacardi', 'smirnoff', 'torres 10', 'mezacal']
    },
    {
        'nombre': 'frutas',
        'productos': ['fresas', 'platano', 'melon', 'pera', 'manzana', 'durazno', 'mango', 'piña', 'sandia']
    },
    {
        'nombre': 'verduras',
        'productos': ['aguacate', 'calabaza', 'zanahoria', 'cebolla', 'elote', 'papa', 'jitomate', 'pepino', 'tomate']
    },
    {
        'nombre': 'carnes rojas',
        'productos': ['arrachera', 'bisteck', 'molida', 'costilla']
    },
    {
        'nombre': 'pescados',
        'productos': ['filete de pescado', 'mojarra', 'salmon', 'camaron', 'atun fresco']
    },
    {
        'nombre': 'aves',
        'productos': ['milanesa de pollo', 'muslo', 'alitas', 'pierna', 'medallones', 'pechuga']
    }
]

#----------------------------------------------------------------------
#  Interfaz de texto
#----------------------------------------------------------------------
def command_interface():
     print('Hola soy Rod, yo te ayudaré a realizar tus compras sin salir de casa')
     print('-'*72)
     print('Preguntame sobre precios, productos de abarrotes, envíos, dudas generales, lo que quieras-')
     print('siempre y cuando sea en español aunque se un poquito de inglés')
     print('='*72)
     print('¿En que te puedo apoyar?')

     input_usuario = ''
     asistente = chatbot();
     while input_usuario != 'salir':
        try:
            input_usuario = input('> ')
        except EOFError:
            print('Saliendo...')
        else:
            print(asistente.responder(input_usuario))

if __name__ == "__main__":
    command_interface()