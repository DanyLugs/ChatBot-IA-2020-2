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
import decimal
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
        # if intent == 'bienvenida':
        #     return respuesta_cambiada
        if intent == 'ir huatulco':
            respuesta_cambiada = respuesta_cambiada.replace('%1', match.group(1))
        if intent == 'ir cancun':
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
        elif intent == 'hoteles huatulco':
            return self.get_hotelesHuatulco()  
        elif intent == 'hoteles cancun':
            return self.get_hotelesCancun()        
        elif intent == 'confirmar' or intent == 'estado':
            return self.da_respuesta_apropiada(user_input)     
        return ''

    def identifica_contexto(self, caso):
        intent = caso['intent']
        
        #HUATULCO
        if intent == 'reservar hotel':
            self.contexto = 'HOTEL'
        elif intent == 'confirmar destino':
            self.contexto = 'DESTINO'
        elif intent == 'reservar hotel personas':
            self.contexto = 'CUANTAS_PERSONAS'
        
        #CANCUN
        if intent == 'reservar hotel cancun':
            self.contexto = 'HOTEL_CANCUN'
        elif intent == 'confirmar destino':
            self.contexto = 'DESTINO'
        elif intent == 'reservar hotel personas cancun':
            self.contexto = 'CUANTAS_PERSONAS_CANCUN'
        
        #HUATULCO
        elif intent == 'recomendaciones huatulco comida':
            self.contexto = 'COMIDA_HUATULCO'
        elif intent == 'recomendaciones huatulco restaurante':
            self.contexto = 'RESTAURANTE_HUATULCO'   
        elif intent == 'recomendaciones huatulco lugares':
            self.contexto = 'LUGARES_HUATULCO'
        elif intent == 'costo vuelo huatulco':
            self.contexto = 'VUELO_HUATULCO'
        
        #CANCUN
        elif intent == 'recomendaciones cancun comida':
            self.contexto = 'COMIDA_CANCUN'
        elif intent == 'recomendaciones cancun restaurante':
            self.contexto = 'RESTAURANTE_CANCUN'   
        elif intent == 'recomendaciones cancun lugares':
            self.contexto = 'LUGARES_CANCUN'
        elif intent == 'costo vuelo cancun':
            self.contexto = 'VUELO_CANCUN'    

    def da_respuesta_apropiada(self, user_input):
        #HUATULCO
        if self.contexto == 'HOTEL':
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT' # Devolver el contexto a default para que el siguiente Sí/No ya no tenga que ver con las pizzas
                return 'Claro, ¿Para cuantas personas necesita su reservación de hotel en Huatulco?' #
            else:
                self.contexto = 'DEFAULT' # Devolver el contexto a default para que el siguiente Sí/No ya no tenga que ver con las pizzas
                return 'Reservacion cancelada, ¿qué puedo hacer por ti?'
        elif self.contexto == 'CUANTAS_PERSONAS':
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT'
                return 'De acuerdo, te muestro la lista de hoteles disponibles en ese destino: \n' + self.get_hotelesHuatulco()
            else:
                self.contexto = 'DEFAULT'
                return 'He cancelado la reservación, ¿Necesitas que haga algo más?'
        
        #CANCUN
        if self.contexto == 'HOTEL_CANCUN':
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT' # Devolver el contexto a default para que el siguiente Sí/No ya no tenga que ver con las pizzas
                return 'Claro, ¿Para cuantas personas necesita su reservación de hotel en Cancun?' #
            else:
                self.contexto = 'DEFAULT' # Devolver el contexto a default para que el siguiente Sí/No ya no tenga que ver con las pizzas
                return 'Reservacion cancelada, ¿qué puedo hacer por ti?'
        elif self.contexto == 'CUANTAS_PERSONAS_CANCUN':
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT'
                return 'De acuerdo, te muestro la lista de hoteles disponibles en ese destino: \n' + self.get_hotelesCancun()
            else:
                self.contexto = 'DEFAULT'
                return 'He cancelado la reservación, ¿Necesitas que haga algo más?'
            
        #HUATULCO    
        elif self.contexto == 'COMIDA_HUATULCO':
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT'
                return 'Aqui tienes la lista de comida tipica del lugar: \n' + self.get_comidaTipicaHuatulco()
            else:
                self.contexto = 'DEFAULT'
                return '¿En qué más puedo ayduarte?'    
        elif self.contexto == 'RESTAURANTE_HUATULCO':
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT'
                return 'Estos son los mejores restaurantes de Huatulco: \n' + self.get_restaurantesHuatulco() + '\n¿Puedo ayudarte con otra cosa?'
            else:
                self.contexto = 'DEFAULT'
                return '¿En qué más puedo ayduarte?'   
        elif self.contexto == 'LUGARES_HUATULCO':
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT'
                return 'Te recomiendo visitar las playas muy tranquilas de Huatulco, el centro donde puedes encontrar artesanias locales y comida típica, además aquí tienes una lista de algunos lugares que debes visitar si vas a Huatulco: \n' + self.get_atractivosHuatulco() + '\n\n¿Puedo ayudarte con otra cosa?'             
            else:
                self.contexto = 'DEFAULT'
                return 'En qué más puedo ayudarte?'  
        elif self.contexto == 'VUELO_HUATULCO':
            if user_input.lower() == 'CDMX':
                self.contexto = 'DEFAULT'
                return 'El costo de vuelo redondo desde ese estado es de $'+ self.generar_cantidad() + ' (moneda nacional) \n ¿Te puedo ayudar con otra cosa?'
            else: 
                self.contexto = 'DEFAULT'
                return 'El precio del vuelo desde ese estado es de $'+ self.generar_cantidad() + ' (moneda nacional) \n ¿Te puedo ayudar con otra cosa?'   
        
        #Cancun    
        elif self.contexto == 'COMIDA_CANCUN':
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT'
                return 'Aqui tienes la lista de comida tipica del lugar: \n' + self.get_comidaTipicaCancun()
            else:
                self.contexto = 'DEFAULT'
                return '¿En qué más puedo ayduarte?'    
        elif self.contexto == 'RESTAURANTE_CANCUN':
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT'
                return 'Estos son los mejores restaurantes de Cancun: \n' + self.get_restaurantesCancun() + '\n¿Puedo ayudarte con otra cosa?'
            else:
                self.contexto = 'DEFAULT'
                return '¿En qué más puedo ayduarte?'   
        elif self.contexto == 'LUGARES_CANCUN':
            if user_input.lower() == 'si' or user_input.lower() == 'sí':
                self.contexto = 'DEFAULT'
                return 'Te recomiendo visitar las playas muy tranquilas de Cancun, el centro donde puedes encontrar artesanias locales y comida típica, además aquí tienes una lista de algunos lugares que debes visitar si vas a Cancun: \n' + self.get_atractivosCancun() + '\n\n¿Puedo ayudarte con otra cosa?'             
            else:
                self.contexto = 'DEFAULT'
                return 'En qué más puedo ayudarte?'  
        elif self.contexto == 'VUELO_CANCUN':
            if user_input.lower() == 'CDMX':
                self.contexto = 'DEFAULT'
                return 'El costo de vuelo redondo desde ese estado es de $'+ self.generar_cantidad() + ' (moneda nacional) \n ¿Te puedo ayudar con otra cosa?'
            else: 
                self.contexto = 'DEFAULT'
                return 'El precio del vuelo desde ese estado es de $'+ self.generar_cantidad() + ' (moneda nacional) \n ¿Te puedo ayudar con otra cosa?'   
          
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

    #Funciones Huatulco
    
    def get_hotelesHuatulco(self):
        '''
        Devuelve una lista de los hoteles en Huatulco exclusivamente
        :return Texto de los hoteles disponibles en Huatulco
        :rtype str
        '''
        lista_hoteles = []
        for hoteles in hotelesHuatulco:
            lista_hoteles.append(hoteles['nombre'].title())
        respuesta = '\n\n -'.join(lista_hoteles)
        if not respuesta:
            return 'Por el momento no tenemos hoteles disponibles en Huatulco'
        return respuesta

    def get_comidaTipicaHuatulco(self):
        '''
        Devuelve una lista con la comida tipica de Huatulco
        Responde al intent = 'recomendaciones huatulco comida'
        Cuando el usuario pregunta por comida en ese destino
        :return Texto de las comidas tipicas del lugar según mexicodestinos.com
        :rtype str
        ''' 
        lista_comida = []
        for comida in comidaTipicaHuatulco:
            lista_comida.append(comida['nombre'].title())
        respuesta = ', '.join(lista_comida)
        if not respuesta:
            return 'No se encuentra disponible la lista de comida tipica de Huatulco en este momento'
        return respuesta 

    def get_restaurantesHuatulco(self):
        '''
        Devuelve una lista con los mejores restaurantes de Huatulco
        Responde al intent = 'recomendaciones huatulco restaurante'
        Cuando el usuario pregunte sobre lugares para comer en ese destino
        :return Texto de las comidas tipicas del lugar de acuerdo con opiniones en tripadvisor.com.mx
        :rtype str
        '''
        lista_restaurantes = []
        for restaurantes in restaurantesHuatulco:
            lista_restaurantes.append(restaurantes['nombre'].title())
        respuesta = '\n\n -'.join(lista_restaurantes).upper()
        if not respuesta:
            return 'No se encuentran disponibles los restaurantes de la zona'
        return respuesta  

    def get_atractivosHuatulco(self):
        '''
        Devuelve una lista con los atractivos turísticos de Huatulco
        Responde al intent = 'recomendaciones lugares huatulco'
        Cuando el usuario pregunta sobre atractivos turísiticos o lugares históricos
        :return Texto de los atractivos turísticos de Huatulco
        :rtype str
        '''
        lista_lugares = []
        for lugares in atractivosHuatulco:
            lista_lugares.append(lugares['nombre'].title())
        respuesta = '\n\n -'.join(lista_lugares).upper()
        if not respuesta:
            return 'No se encuentra disponible la lista de lugares turísiticos'
        return respuesta  
    
    #Funciones Cancun
    
    def get_hotelesCancun(self):
        '''
        Devuelve una lista de los hoteles en Cancun exclusivamente
        :return Texto de los hoteles disponibles en Cancun
        :rtype str
        '''
        lista_hoteles = []
        for hoteles in hotelesCancun:
            lista_hoteles.append(hoteles['nombre'].title())
        respuesta = '\n\n -'.join(lista_hoteles)
        if not respuesta:
            return 'Por el momento no tenemos hoteles disponibles en Cancun'
        return respuesta

    def get_comidaTipicaCancun(self):
        '''
        Devuelve una lista con la comida tipica de Cancun
        Responde al intent = 'recomendaciones Cancun comida'
        Cuando el usuario pregunta por comida en ese destino
        :return Texto de las comidas tipicas del lugar según mexicodestinos.com
        :rtype str
        ''' 
        lista_comida = []
        for comida in comidaTipicaCancun:
            lista_comida.append(comida['nombre'].title())
        respuesta = ', '.join(lista_comida)
        if not respuesta:
            return 'No se encuentra disponible la lista de comida tipica de Cancun en este momento'
        return respuesta 

    def get_restaurantesCancun(self):
        '''
        Devuelve una lista con los mejores restaurantes de Cancun
        Responde al intent = 'recomendaciones Cancun restaurante'
        Cuando el usuario pregunte sobre lugares para comer en ese destino
        :return Texto de las comidas tipicas del lugar de acuerdo con opiniones en tripadvisor.com.mx
        :rtype str
        '''
        lista_restaurantes = []
        for restaurantes in restaurantesCancun:
            lista_restaurantes.append(restaurantes['nombre'].title())
        respuesta = '\n\n -'.join(lista_restaurantes).upper()
        if not respuesta:
            return 'No se encuentran disponibles los restaurantes de la zona'
        return respuesta  

    def get_atractivosCancun(self):
        '''
        Devuelve una lista con los atractivos turísticos de Cancun
        Responde al intent = 'recomendaciones lugares Cancun'
        Cuando el usuario pregunta sobre atractivos turísiticos o lugares históricos
        :return Texto de los atractivos turísticos de Cancun
        :rtype str
        '''
        lista_lugares = []
        for lugares in atractivosCancun:
            lista_lugares.append(lugares['nombre'].title())
        respuesta = '\n\n -'.join(lista_lugares).upper()
        if not respuesta:
            return 'No se encuentra disponible la lista de lugares turísiticos'
        return respuesta  

    def generar_cantidad(self):
        return '{}'.format(decimal.Decimal(random.randrange(150000, 450000))/100)          
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

    # INFORMACIÓN REFERENTE A HUATULCO INICIO
    {
        'intent': 'hoteles huatulco',
        'regex': [
            r'(Que|Qué|Cuáles|Cuales|Quiero|Quisiera|Dime) (.*) hoteles (.*) Huatulco'
        ],
        'respuesta': [
            'La lista de hoteles diponibles te la muestro a continuación:'
        ]
    },
    {
        'intent': 'que hotel huatulco',
        'regex': [
            r'.*Las Brisas Huatulco.*',
            r'.*El Barcelo.*',
            r'.*Camino Real Zaashila.*'
            r'.*Secrets Huatulco Resort & Spa.*'
        ],
        'respuesta': [
            'Excelente, ¿Me puedes indicar la fecha de llegada al destino? Por favor utiliza el formato: "DD MES YYYY".'
        ]
    },
    {
        'intent': 'hotel huatulco fecha inicio',
        'regex': [
            r'[\d]{1,2} [ADFJMNOS]\w* [\d]{4}'
        ],
        'respuesta': [
            'Muy bien, ahora indicame cuantos días quieres quedarte en tu destino de la forma: "# dias"'
        ]
    },
    {
        'intent': 'hotel huatulco fecha fin',
        'regex': [
            r'.* dias'
        ],
        'respuesta': [
            'Perfecto tu reservación se ha hecho satisfacotiramente \n ¿Puedo ayudarte con algo más?',
            'Muy bien, genero la reservación de hotel para esas fechas en ese destino. ¿Te puedo ayudar en algo más?'
        ]
    },
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
        'intent': 'reservar hotel personas',
        'regex': [
            r'Para (1|2|3|4|5|6|7|8|9|10) (.*)',
            r'(1|2|3|4|5|6|7|8|9|10) (.*)',
            r'(1|2|3|4|5|6|7|8|9|10)'
        ],
        'respuesta': [
            'Excelente, ¿Tenemos disponible la lista de hoteles, deseas verla?'
        ]
    },
    
    {
        'intent': 'reservar hotel cancun',
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
        'intent': 'reservar hotel personas cancun',
        'regex': [
            r'Para (1|2|3|4|5|6|7|8|9|10) (.*)',
            r'(1|2|3|4|5|6|7|8|9|10) (.*)',
            r'(1|2|3|4|5|6|7|8|9|10)'
        ],
        'respuesta': [
            'Excelente, ¿Tenemos disponible la lista de hoteles, deseas verla?'
        ]
    },
    
    {
        'intent': 'recomendaciones huatulco restaurante',
        'regex': [
            r'.* (restaurante|restaurantes) .* huatulco',
            r'.* (restaurantes|restaurante) .* huatulco .*',
            r'(Donde|En que lugar|Algun lugar) .* comer .* huatulco .*'
        ],
        'respuesta': [
            'Si quieres comer en un bonito lugar en Huatulco, ¿puedo mostrarte los mejores restaurantes de la zona?',
            '¿Quieres que te muestre una lista con variedad de lugares para comer delicioso en Huatulco?'
        ]    
    },
    {
        'intent': 'recomendaciones huatulco comida',
        'regex': [
            r'.* que .* (comer|comida) .* huatulco.*',
            r'.* comida tipica .* huatulco .*',
            r'.* comida .* huatulco .*',
            r'.* comida .* huatulco',
            r'.* comer .* huatulco'
        ],
        'respuesta': [
            'Huatulco ofrece gran variedad gastronomica del estado de Oaxaca, ¿gustas que te muestre la lista de comida tipica del lugar?',
            '¿Quieres que te muestre una lista con variedad de comida tipica de Huatulco?'
        ]
    },
    {
        'intent': 'recomendaciones huatulco lugares',
        'regex': [
            r'(Que|Qué|Cual|Cuáles|Cuales|Donde|Dónde) .* lugares (historicos|históricos|importantes) .* huatulco',
            r'(Que|Qué|Cual|Cuáles|Cuales|Donde|Dónde) .* lugares (historicos|históricos|importantes) .* huatulco .*',
            r'(Que|Qué|Cual|Cuáles|Cuales|Donde|Dónde) .* (atractivo|atractivo) (turistico|turisticos) .* huatulco'
        ],
        'respuesta': [
            'La riqueza histórica y cultural del estado de Oaxaca es extensa, de este repertorio, una partre se encuentra en Huatulco, ¿Quieres que te muestre una lista sitios para visitar?'
        ]
    },    
    {
        'intent': 'costo vuelo huatulco',
        'regex': [
            r'(precio|costo) .* vuelo .* huatulco .*',
            r'(Cuanto|Cuánto) .* vuelo .* huatulco .*',
            r'(Cuanto|Cuánto) .* vuelo .* huatulco',
            r'(precio|costo) .* vuelo .* huatulco'
        ],
        'respuesta': [
            'Para decirte el costo, dime ¿desde qué estado de la republica quieres viajar?',
            'Para indicarte el precio podrías decirme por favor ¿de qué estado de la republica quiere viajar?'
        ]    
    },
    {
        'intent': 'actividades huatulco',
        'regex': [
            r'(Que|Qué) puedo hacer en Huatulco .*',
            r'(Que|Que) actividades .* Huatulco .*',
            r'(Que|Qué) puedo hacer en Huatulco',
            r'(Que|Que) actividades .* Huatulco',
            r'(Que|Qué) .* hacer .* huatulco',
            r'(Que|Qué) .* hacer .* huatulco.*'
        ],
        'respuesta': [
            'Yo te recomiendo dar el tour por las Bahías de Huatulco, aquí podrás encontrar las playas más bonitas y solitarias de todo Huatulco \n¿Puedo ayudarte con otra cosa?',
            'Si te encanta nadar y la naturaleza lo tuyo será el recorrido con snorkel en las playas de Huatulco, podrás ver cientos de peces de diferentes espcies así como fauna marina \n¿Puedo ayudarte con otra cosa?',
            'Si lo que buscas es algo más cultural e histórico, puedes recorrer los yacimientos arqueológicos así como el centro de Huatulco en busca de artesanias locales \n¿Puedo ayudarte con otra cosa?'
        ]    
    },
    {
        'intent': 'dar clima huatulco',
        'regex': [
            r'(Qué|Cuál|Dime|Dame|Cuáles|Cuales|Que|Cual|Quiero|A que| A qué).* (clima|tiempo).* Huatulco.*',
            r'.* clima .* Huatulco .*'
        ],
        'respuesta': [
            'El clima en Huatulco es tropical, cálido y húmedo, temperatura promedio de 27°',
            '27° promedio durante todo el año, nueblado en verano con algunas precepitaciones pero no deja de ser un clima perfecto para disfrutar la playa'
        ]
    },
    {
        'intent': 'dar destinos',
        'regex': [
            r'(Qué|Cuál|Dime|Dame|Cuáles|Cuales|Que|Cual|Quiero|A que| A qué).* (destinos|lugares).*',
            r'Dime a donde puedo viajar .*'
        ],
        'respuesta': [
            'Te daré la lista de destinos con los que contamos:',
            'Estos son los lugares en los que te puedo ayudar a realizar una reservación completa:',
            'Nuestros destinos son las playas más atractivas de México:'
        ]
    },
    {
        'intent': 'huatulco',
        'regex': [
            r'Huatulco'
        ],
        'respuesta': [
            'Excelente lugar para descansar, disfrutar la playa y una bebida referscante'
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
    
    # INFORMACION REFERENTE A HUATULCO FIN
    
    # INFORMACIÓN REFERENTE A CANCUN INICIO
    {
        'intent': 'hoteles cancun',
        'regex': [
            r'(Que|Qué|Cuáles|Cuales|Quiero|Quisiera|Dime) (.*) hoteles (.*) Cancun'
        ],
        'respuesta': [
            'La lista de hoteles diponibles te la muestro a continuación:'
        ]
    },
    {
        'intent': 'que hotel cancun',
        'regex': [
            r'.*Secrets The Vine Cancún.*',
            r'.*Hyatt Ziva Cancún.*',
            r'.*Crown Paradise Club Cancun.*'
            r'.*Live Aqua Beach Resort Cancún.*'
        ],
        'respuesta': [
            'Excelente, ¿Me puedes indicar la fecha de llegada al destino? Por favor utiliza el formato: "DD MES YYYY".'
        ]
    },
    {
        'intent': 'hotel cancun fecha inicio',
        'regex': [
            r'[\d]{1,2} [ADFJMNOS]\w* [\d]{4}'
        ],
        'respuesta': [
            'Muy bien, ahora indicame cuantos días quieres quedarte en tu destino de la forma: "# dias"'
        ]
    },
    {
        'intent': 'hotel cancun fecha fin',
        'regex': [
            r'.* dias'
        ],
        'respuesta': [
            'Perfecto tu reservación se ha hecho satisfacotiramente \n ¿Puedo ayudarte con algo más?',
            'Muy bien, genero la reservación de hotel para esas fechas en ese destino. ¿Te puedo ayudar en algo más?'
        ]
    },
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
        'intent': 'reservar hotel personas',
        'regex': [
            r'Para (1|2|3|4|5|6|7|8|9|10) (.*)',
            r'(1|2|3|4|5|6|7|8|9|10) (.*)',
            r'(1|2|3|4|5|6|7|8|9|10)'
        ],
        'respuesta': [
            'Excelente, ¿Tenemos disponible la lista de hoteles, deseas verla?'
        ]
    },
    
    {
        'intent': 'reservar hotel cancun',
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
        'intent': 'reservar hotel personas cancun',
        'regex': [
            r'Para (1|2|3|4|5|6|7|8|9|10) (.*)',
            r'(1|2|3|4|5|6|7|8|9|10) (.*)',
            r'(1|2|3|4|5|6|7|8|9|10)'
        ],
        'respuesta': [
            'Excelente, ¿Tenemos disponible la lista de hoteles, deseas verla?'
        ]
    },
    
    {
        'intent': 'recomendaciones cancun restaurante',
        'regex': [
            r'.* (restaurante|restaurantes) .* cancun',
            r'.* (restaurantes|restaurante) .* cancun .*',
            r'(Donde|En que lugar|Algun lugar) .* comer .* cancun .*'
        ],
        'respuesta': [
            'Si quieres comer en un bonito lugar en Cancun, ¿puedo mostrarte los mejores restaurantes de la zona?',
            '¿Quieres que te muestre una lista con variedad de lugares para comer delicioso en Cancun?'
        ]    
    },
    {
        'intent': 'recomendaciones cancun comida',
        'regex': [
            r'.* que .* (comer|comida) .* cancun.*',
            r'.* comida tipica .* cancun .*',
            r'.* comida .* cancun .*',
            r'.* comida .* cancun',
            r'.* comer .* cancun'
        ],
        'respuesta': [
            'Cancun ofrece gran variedad gastronomica del estado de Oaxaca, ¿gustas que te muestre la lista de comida tipica del lugar?',
            '¿Quieres que te muestre una lista con variedad de comida tipica de Cancun?'
        ]
    },
    {
        'intent': 'recomendaciones cancun lugares',
        'regex': [
            r'(Que|Qué|Cual|Cuáles|Cuales|Donde|Dónde) .* lugares (historicos|históricos|importantes) .* cancun',
            r'(Que|Qué|Cual|Cuáles|Cuales|Donde|Dónde) .* lugares (historicos|históricos|importantes) .* cancun .*',
            r'(Que|Qué|Cual|Cuáles|Cuales|Donde|Dónde) .* (atractivo|atractivo) (turistico|turisticos) .* cancun'
        ],
        'respuesta': [
            'La riqueza histórica y cultural del estado de Quintana Roo es extensa, de este repertorio, una partre se encuentra en Cancun, ¿Quieres que te muestre una lista sitios para visitar?'
        ]
    },    
    {
        'intent': 'costo vuelo cancun',
        'regex': [
            r'(precio|costo) .* vuelo .* cancun .*',
            r'(Cuanto|Cuánto) .* vuelo .* cancun .*',
            r'(Cuanto|Cuánto) .* vuelo .* cancun',
            r'(precio|costo) .* vuelo .* cancun'
        ],
        'respuesta': [
            'Para decirte el costo, dime ¿desde qué estado de la republica quieres viajar?',
            'Para indicarte el precio podrías decirme por favor ¿de qué estado de la republica quiere viajar?'
        ]    
    },
    {
        'intent': 'actividades cancun',
        'regex': [
            r'(Que|Qué) puedo hacer en Cancun .*',
            r'(Que|Que) actividades .* Cancun .*',
            r'(Que|Qué) puedo hacer en Cancun',
            r'(Que|Que) actividades .* Cancun',
            r'(Que|Qué) .* hacer .* cancun',
            r'(Que|Qué) .* hacer .* cancun.*'
        ],
        'respuesta': [
            'Le recomiendo que se adelante a largas colas y al abrasador calor del mediodía en un recorrido con acceso a primera hora a Chichén Itzá desde Cancún, una gran elección para las familias\n¿Puedo ayudarte con otra cosa?.',
            'Si te encanta nadar y la naturaleza lo tuyo será el recorrido con snorkel en las playas de Cancun, podrás ver cientos de peces de diferentes espcies así como fauna marina \n¿Puedo ayudarte con otra cosa?',
            'Si lo que buscas es algo más cultural e histórico, puedes recorrer los yacimientos arqueológicos así como el centro de Cancun en busca de artesanias locales \n¿Puedo ayudarte con otra cosa?'
        ]    
    },
    {
        'intent': 'dar clima cancun',
        'regex': [
            r'(Qué|Cuál|Dime|Dame|Cuáles|Cuales|Que|Cual|Quiero|A que| A qué).* (clima|tiempo).* Cancun.*',
            r'.* clima .* Cancun .*'
        ],
        'respuesta': [
            'El clima en Cancun es tropical, cálido y húmedo, temperatura promedio de 26°',
            '26° promedio durante todo el año, nueblado en verano con algunas precepitaciones pero no deja de ser un clima perfecto para disfrutar la playa'
        ]
    },
    {
        'intent': 'dar destinos',
        'regex': [
            r'(Qué|Cuál|Dime|Dame|Cuáles|Cuales|Que|Cual|Quiero|A que| A qué).* (destinos|lugares).*',
            r'Dime a donde puedo viajar .*'
        ],
        'respuesta': [
            'Te daré la lista de destinos con los que contamos:',
            'Estos son los lugares en los que te puedo ayudar a realizar una reservación completa:',
            'Nuestros destinos son las playas más atractivas de México:'
        ]
    },
    {
        'intent': 'cancun',
        'regex': [
            r'Cancun'
        ],
        'respuesta': [
            'Excelente lugar para descansar, disfrutar la playa y una bebida referscante'
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
    
    # INFORMACION REFERENTE A CANCUN FIN
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
        'intent': 'estado',
        'regex': [
            r'(Aguascalientes|AGS|Baja California|BajaCAlifornia SUr|Campeche|Chiapas|Chihuahua|Ciudad de México|Ciudad de Mexico|DF|CDMX|Coahuila|Colima|Durango|Guanajuato|Guerrero|Hidalgo|Jalisco)',
            r'(Michoacán|Estado de Mexico|Estado de México|Morelos|Nayarit|Nuevo León|Monterrey|Oaxaca|Puebla|Querétaro|Queretaro|Quintana Roo|San Luis Potosí|San Luis Potosi|Sinaloa|Sonora|Tabasco|Tamapulipas|Tlaxcala|Veracruz|Yucatán|Zacatecas)'
        ],
        'respuesta': [
            '' # A priori no se puede dar una respuesta, se debe considerar el contexto (ver la función self.da_respuesta_apropiada())
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
            'Disculpa, no comprendí lo que dices',
            'Podrías reformular tu pregunta por favor'
            '¿Puedes decir lo mismo con otras palabras?'
        ]
    }
]

#----------------------------------------------------------------------
# Diccionario que representa grupos de información
# Ejemplo de información que podría consultarse de manera externa,
# ser generada, o auxiliar en la redacción de una respuesta del chatbot.
#----------------------------------------------------------------------
destinos = [
    {
        'nombre': 'Huatulco'
    },
    {
        'nombre': 'Cancun'
    },
    {
        'nombre': 'Acapulco'
    },
    {
        'nombre': 'Puerto Vallarta'
    }
]

#HUATULCO
hotelesHuatulco = [
    {
        'nombre': '-Las Brisas Huatulco: $950 la noche por persona, todo incluido',
        'estrellas': '5 estrellas'
    },
    {
        'nombre': 'El Barcelo: $1,200 la noche por persona, todo incluido',
        'estrellas': '5 estrellas'
    },
    {
        'nombre': 'Camino Real Zaashila: $750 la noche por persona, desayuno incluido',
        'estrellas': '5 estrellas'
    },
    {
        'nombre': 'Secrets Huatulco Resort & Spa: $1,500 la noche por persona, desayuno incluido',
        'estrellas': '5 estrellas'
    }
]

comidaTipicaHuatulco = [
    {
        'nombre': 'Quesillo'
    },
    {
        'nombre': 'Chapulines'
    },
    {
        'nombre': 'Cecina enchilada'
    },
    {
        'nombre': 'Chilaquiles'
    },
    {
        'nombre': 'Pescados y mariscos'
    },
    {
        'nombre': 'Pan de nata'
    }
]

restaurantesHuatulco = [
    {
        'nombre': '-Rocoto: Te recomendamos el carpaccio de res como entrada, filete mignon a la mostaza con tocino de plato fuerte, disfruta con vino tinto de la mejor claidad.'
    },
    {
        'nombre': 'Mare: Si disfrutas de la comida italiana esta es la opcion para ti, precios accesibles, alimentos de la mejor calidad y atención excepcional.'
    },
    {
        'nombre': 'Viena Huatulco: Si lo que buscas es algo más exotico Viena Huatulco es tu opción, gran variedad de platillos austriacos y postres que te harán pedir doble porción.'
    },
    {
        'nombre': 'Mercader: Lugar acogedor, menú completo, sabores exquisitos con su comida internacional, si eres hogareño esta es tu opción.'
    }
]

atractivosHuatulco = [
    {
        'nombre': 'La bufadora: un lugar creado por la naturaleza ubicado en Bahias de Huatulco, su sonido al expulsar agua acumulada en su pequeña cueva te dejará atónito'
    },
    {
        'nombre': 'Cara en la piedra: Ubicado en Bahias de Huatulco, una belleza natural que en sus acantilados formó, a lo largo de muchos años, un rostro, ver para creer.'
    },
    {
        'nombre': 'Bahia de Maguey: Una de las playas virgenes más visitadas de Huatulco, cuenta con exquisitos restaurantes que te deleitaran con sus marsicadas y parrilladas de mariscos'
    },
    {
        'nombre': 'Puerto de cruceros: Un gran muelle para que encayen los cruceros que viajan por el Oceano Pacífico, una vista impresionante si tienes la suerte de que llegue uno cuando visites Huatulco'
    }
]

#CANCUN

hotelesCancun = [
    {
        'nombre': '-Secrets The Vine Cancún: $6,588 la noche por persona, todo incluido',
        'estrellas': '5 estrellas'
    },
    {
        'nombre': 'Hyatt Ziva Cancún: $5,837 la noche por persona, todo incluido',
        'estrellas': '5 estrellas'
    },
    {
        'nombre': 'Crown Paradise Club Cancun: $3,313 la noche por persona, todo incluido',
        'estrellas': '5 estrellas'
    },
    {
        'nombre': 'Live Aqua Beach Resort Cancún: $6,961 la noche por persona',
        'estrellas': '5 estrellas'
    }
]

comidaTipicaCancun = [
    {
        'nombre': 'Quesillo'
    },
    {
        'nombre': 'Chapulines'
    },
    {
        'nombre': 'Cecina enchilada'
    },
    {
        'nombre': 'Chilaquiles'
    },
    {
        'nombre': 'Pescados y mariscos'
    },
    {
        'nombre': 'Pan de nata'
    }
]

restaurantesCancun = [
    {
        'nombre': '-Bandoneon: La decoración del lugar es preciosa y el lugar es muy limpio.'
    },
    {
        'nombre': 'Taquería Los Chachalacos: Excelente servicio, la comida deliciosa, el chicharrón de queso delicioso, pide la salsa especial.'
    },
    {
        'nombre': 'Rino~s Pizza Time: Excelente lugar para cenar con amigos/familia. La comida es exquisita y sin demoras.'
    },
    {
        'nombre': 'MercaderPeter~s Restaurante: Atención personalizada por el chef y manteniendo un ambiente muy agradable. La comida excelente y terminando con un postre delicioso. No dejar de acudir en su viaje a Cancún.'
    }
]

atractivosCancun = [
    {
        'nombre': 'Playa Delfines: Una playa con belleza escenica, es una parada obligatoria en tu viaje a la Riviera Maya.'
    },
    {
        'nombre': 'Xoximilco Cancun: Es una experiencia única para conocer y disfrutar de una auténtica fiesta mexicana, con música típica de varios rincones de Mexico, comida y bebida variada y buena y que todo en conjunto.'
    },
    {
        'nombre': 'Dolphin Discovery: Sin duda, el momento más espectacular, es el llamado "Foot Push" donde dos delfines te empujarán por la planta de tus pies a gran velocidad hasta ir "volando" fuera del agua, esta es una experiencia inolvidable.'
    },
    {
        'nombre': 'Chichen Itza: Una de las nuevas 7 maravillas del mundo que no te puedes perder.'
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