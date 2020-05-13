#----------------------------------------------------------------------
#  chatbot.py
#
#  Una implementación sencilla de un chatbot
#  basado en intents y expresiones regulares
#  por: 
#  -Arenas Ayala Ramón
#  -Lugo Cano Daniel
#  -Millán Pimentel Óscar Fernando
#----------------------------------------------------------------------

import string
import re
import random

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
        # if intent == 'bienvenida':
        #     return respuesta_cambiada
        if intent == 'ir huatulco':
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
        if intent == 'dar destinos':
            return self.get_destinos()
        elif intent == 'confirmar':
            return self.da_respuesta_apropiada(user_input)    
        return ''

    def identifica_contexto(self, caso):
        intent = caso['intent']
        if intent == 'reservar hotel':
            self.contexto = 'HOTEL'
        elif intent == 'confirmar destino': # TODO
            self.contexto = 'DESTINO'

    def da_respuesta_apropiada(self, user_input):
        if self.contexto == 'HOTEL':
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT' # Devolver el contexto a default para que el siguiente Sí/No ya no tenga que ver con las pizzas
                return 'Claro, confirmando quiere hacer una reservación para un hotel en Huatulco'
            else:
                self.contexto = 'DEFAULT' # Devolver el contexto a default para que el siguiente Sí/No ya no tenga que ver con las pizzas
                return 'Orden de pizza cancelado'
        elif self.contexto == 'DESTINO': # Sería análogo al caso de las pizzas
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

    def get_destinos(self):
        '''
        Devuelve una lista de los destinos disponibles de los cuales el bot tiene 
        información al respecto para dar al usuario.
        Representa un ejemplo de consulta de información o acciones en el flujo
        para construir una respuesta del chatbot
        :return Texto de los destinos turísiticos
        :rtype str
        '''
        lista_lugares = []
        for lugares in destinos:
            lista_lugares.append(lugares['nombre'].title())
        respuesta = ', '.join(lista_lugares)
        if not respuesta:
            return 'Por el momento no tenemos disponible ningún destino'
        return respuesta

#----------------------------------------------------------------------
# Base de conocimiento
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
        'intent': 'bienvenida',
        'regex': [
            r'Hola (.*)',
            r'.*Hola.*',
            r'Hola',
            r'.*Buen(a|o)s (días|tardes|noches).*'
        ],
        'respuesta': [
            'Bienvenido, ¿En que te puedo ayudar?',
            'Hola, ¿Cómo te puedo apoyar?'
        ]
    },
    {
        'intent': 'dar destinos',
        'regex': [
            r'(Qué|Cuál|Dime|Dame|Cuáles|Cuales|Que|Cual).* (destinos|lugares).*'
        ],
        'respuesta': [
            'Te daré la lista de destinos con los que contamos:',
            'Estos son los lugares en los que te puedo ayudar a realizar una reservación completa:',
            'Nuestros destinos son las playas más atractivas de México:'
        ]
    },
    # INFORMACIÓN REFERENTE A HUATULCO
    {
        'intent': 'reservar hotel',
        'regex': [
            r'Quiero (.*) hotel (.*)',
            r'Quisiera (.*) hotel (.*)'
        ],
        'respuesta': [
            '¿Quieres realizar una reservación para un hotel en ese destino?',
            '¿Deseas que haga una reservación para un hotel para ese destino?'
        ]
    },
    {
        'intent': 'ir huatulco',
        'regex': [
            r'Quiero (.*) Huatulco',
            r'Quisiera (.*) Huatulco',
            r'.*Huatulco.*'
        ],
        'respuesta': [
            'Veo que quieres %1 Huatulco, ¿qué necesitas que haga por ti?',
            '¡Huatulco!, gran elección para visitar, ¿cómo puedo ayudarte con tu viaje?'
        ]
    },
    {
        'intent': 'ir cancun',
        'regex': [
            r'Quiero (.*) Cancun',
            r'Quisiera (.*) Cancun',
            r'.*Cancun.*'
        ],
        'respuesta': [
            'Veo que quieres %1 Cancun, ¿qué necesitas que haga por ti?',
            '¡Cancun!, gran elección para visitar, ¿cómo puedo ayudarte con tu viaje?'
        ]
    },
    {
        'intent': 'ir acapulco',
        'regex': [
            r'Quiero (.*) Acapulco',
            r'Quisiera (.*) Acapulco',
            r'.*Acapulco.*'
        ],
        'respuesta': [
            'Veo que quieres %1 Acapulco, ¿qué necesitas que haga por ti?',
            '¡Acapulco!, gran elección para visitar, ¿cómo puedo ayudarte con tu viaje?'
        ]
    },
    {
        'intent': 'ir puerto vallarta',
        'regex': [
            r'Quiero (.*) Puerto Vallarta',
            r'Quisiera (.*) Puerto Vallarta',
            r'.*Puerto Vallarta.*'
        ],
        'respuesta': [
            'Veo que quieres %1 Puerto Vallarta, ¿qué necesitas que haga por ti?',
            'Puerto Vallarta!, gran elección para visitar, ¿cómo puedo ayudarte con tu viaje?'
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
# Diccionario que representa el menú del día
# Ejemplo de información que podría consultarse de manera externa,
# ser generada, o auxiliar en la redacción de una respuesta del chatbot.
#----------------------------------------------------------------------
destinos = [
    {
        'nombre': 'Huatulco',
        'ingredientes': ['jamón', 'piña']
    },
    {
        'nombre': 'Cancun',
        'ingredientes': ['pepperoni', 'queso extra']
    },
    {
        'nombre': 'Acapulco',
        'ingredientes': ['chile', 'chorizo', 'frijoles']
    },
    {
        'nombre': 'Puerto Vallarta',
        'ingredientes': ['chile', 'chorizo', 'frijoles']
    }
]

#----------------------------------------------------------------------
#  Interfaz de texto
#----------------------------------------------------------------------
def command_interface():
    print('Hola soy Rod, tu asistente personal de viajes.')
    print('-'*72)
    print('Nos especializamos en las principales playas de México:')
    print('-Huatulco')
    print('-Cabo San Lucas')
    print('-Cancun')
    print('-Acapulco')
    print('-Puerto Vallarta')
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