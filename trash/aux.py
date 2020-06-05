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
        self.destino = 0
        self.ctx = 'deafult'
        self.user_input = ""

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
        self.user_input = user_input
        caso = self.encontrar_intent(user_input)
        intent = caso.get('intent')
        self.identifica_destino(intent)
        self.identifica_contexto(intent) # Asignar contexto, es auxiliar para identificar ciertos casos particulares

        print('Intent: ' + intent)
        print('Contexto: ' + self.ctx)
        print('Destino: ' + str(self.destino))
       
        respuesta_final = self.get_respuesta(caso)
        dic_des = destinos.get(self.destino)
        if dic_des:
            nombre_des = dic_des.get('nombre')
            if nombre_des:
                respuesta_final = respuesta_final.replace('%1', nombre_des)
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

    def get_respuesta(self,caso):
        respuesta = ""
        intent = caso.get('intent')
        if intent == 'desconocido' and self.ctx == 'reservar hotel':
            return self.get_extra_contexto(intent)
        if intent in ['bienvenida','desconocido','dar destinos'] or destinos.get(intent):     
            respuesta = random.choice(caso['respuesta'])
            if intent == 'dar destinos':
                dest = ""
                for desti in destinos:
                    dest = dest + desti.get('nombre') + '\n'
                respuesta = respuesta + '\n' + dest
            return respuesta
        if self.destino != 0:
            respuesta = random.choice(caso['respuesta'])
            add = self.get_extra_contexto(intent)
            if add != "":
                respuesta = respuesta + '\n' + add
            if respuesta == "":
                respuesta = "Parece que estas diciendo cosas sin sentido cu cu cu cu o.O"
            return respuesta
        return 'Por favor elige un destino primero por favor'

    def identifica_destino(self, intent):
        new_destino = destinosNi.get(intent)
        if new_destino:
            self.destino = new_destino

    def identifica_contexto(self,intent):
        if not (intent in ['confirmar','estado','reservar hotel personas','hotel fecha inicio','hotel fecha fin','desconocido']):
            self.ctx = intent
            
        

    def get_extra_contexto(self, intent):
        ctx = self.ctx
        if ctx == 'costo vuelo' and intent == 'estado':   
            self.ctx = 'default'
            return 'El costo de vuelo redondo desde ese estado es de $'+ self.generar_cantidad() + ' (moneda nacional) \n ¿Te puedo ayudar con otra cosa?'
        if ctx in ['hoteles','clima'] :
            self.ctx = 'default'
            return self.get_extra_destino(ctx)
        if ctx in ['restaurantes','comidas','atractivos'] and intent == 'confirmar':
            if self.user_input.lower() in ['si','sí']:
                self.ctx = 'default'
                return self.get_extra_destino(ctx)
            else:
                self.ctx = 'default'
                return "Ok, regresando al principio..."
        if ctx == 'reservar hotel':
            if intent == 'confirmar':
                if self.user_input.lower() in ['si','sí']:
                    return 'Favor de seleccionar un hotel de la lista de hoteles en %1 (No escriba la palabra %1)' + '\n' + self.get_extra_destino('hoteles')
                else:
                    self.ctx = 'default'
                    return "Ok, regresando al principio..."
            if intent == 'desconocido':
                for hotel in destinos.get(self.destino).get("hoteles"):
                    if hotel.get('nombre').find(self.user_input)>=0:
                        print(hotel.get('nombre'))
                        return "Genial! Por favor dime para cuantas personas es la reservacion"
                return 'Lo siento ese hotel no fue detectado, asugurese de escribir de forma correcta el nombre del hotel (No escriba la palabra %1)\n' +  self.get_extra_destino('hoteles')
            if intent == 'hotel fecha fin':
                self.ctx = 'default'
                return "..."
        return ""

    def get_extra_destino(self, intent):
        '''
        Devuelve una lista de los en un destino exclusivamente
        :return Texto de los hoteles disponibles en Huatulco
        :rtype str
        '''
        lista_resp = []
        intent_inf = destinos.get(self.destino) 
        if intent_inf:
            lista_inf = intent_inf.get(intent)
            if lista_inf:
                for elem in lista_inf:
                    lista_resp.append(elem['nombre'].title())
                respuesta = '\n -'.join(lista_resp)
                if not respuesta:
                    return 'Por el momento no tenemos información sobre lo que busca disponible en %1'
                return respuesta
        return ''  

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
respuesta_elegir_destino = [
            'Veo que quieres ir %1, ¿qué necesitas que haga por ti?',
            '¡%1!, gran elección para visitar, ¿cómo puedo ayudarte con tu viaje?'
        ]

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
            r'(Qué|Cuál|Dime|Dame|Cuáles|Cuales|Que|Cual|Quiero|A que| A qué).*(destinos|lugares).*',
            r'Dime a donde puedo viajar .*'
        ],
        'respuesta': [
            'Te daré la lista de destinos con los que contamos:',
            'Estos son los lugares en los que te puedo ayudar a realizar una reservación completa:',
            'Nuestros destinos son las playas más atractivas de México:'
        ]
    },
    {
        'intent': 'hoteles',
        'regex': [
            r'(Que|Qué|Cuáles|Cuales|Quiero|Quisiera|Dime)(.*)hoteles(.*)',
            r'.*hoteles.*',
            r'.*Hoteles*'
        ],
        'respuesta': [
            'La lista de hoteles diponibles te la muestro a continuación:'
        ]
    },
    {
        'intent': 'restaurantes',
        'regex': [
            r'.*(restaurante|restaurantes).*',
            r'.*(restaurantes|restaurante).*',
            r'(Donde|En que lugar|Algun lugar) .* comer.*'
        ],
        'respuesta': [
            'Si quieres comer en un bonito lugar en %1, ¿puedo mostrarte los mejores restaurantes de la zona?',
            '¿Quieres que te muestre una lista con variedad de lugares para comer delicioso en %1?'
        ]    
    },
    {
        'intent': 'comidas',
        'regex': [
            r'.*que .* (comer|comida).*',
            r'.*comida tipica.*',
            r'.*comida.*',
            r'.*comer.*'
        ],
        'respuesta': [
            '%1 ofrece gran variedad gastronomica, ¿gustas que te muestre la lista de comida tipica del lugar?',
            '¿Quieres que te muestre una lista con variedad de comida tipica de %1?'
        ]
    },
    {
        'intent': 'atractivos',
        'regex': [
            r'(Que|Qué|Cual|Cuáles|Cuales|Donde|Dónde) .* lugares (historicos|históricos|importantes) .*',
            r'(Que|Qué|Cual|Cuáles|Cuales|Donde|Dónde) .* lugares (historicos|históricos|importantes) .*',
            r'(Que|Qué|Cual|Cuáles|Cuales|Donde|Dónde) .* (atractivo|atractivo) (turistico|turisticos) .*'
        ],
        'respuesta': [
            '¿Quieres que te muestre una lista de lugares increibles para visitar en %1'
        ]
    }, 
  {
        'intent': 'clima',
        'regex': [
            r'(Qué|Cuál|Dime|Dame|Cuáles|Cuales|Que|Cual|Quiero|A que| A qué).*(clima|tiempo).*',
            r'.*clima.*'
        ],
        'respuesta': [
            'A continuación una breve descripción del clima de %1'
        ]
    },
    {
        'intent': 'hotel fecha inicio',
        'regex': [
            r'[\d]{1,2} [ADFJMNOS]\w* [\d]{4}'
        ],
        'respuesta': [
            'Muy bien, ahora indicame cuantos días quieres quedarte en tu destino de la forma: "# dias"'
        ]
    },
    {
        'intent': 'hotel fecha fin',
        'regex': [
            r'.*dias'
        ],
        'respuesta': [
            'Perfecto tu reservación se ha hecho satisfacotiramente \n ¿Puedo ayudarte con algo más?',
            'Muy bien, genero la reservación de hotel para esas fechas en ese destino. ¿Te puedo ayudar en algo más?'
        ]
    },
    {
        'intent': 'reservar hotel',
        'regex': [
            r'Quiero(.*)hotel(.*)',
            r'Quisiera(.*)hotel(.*)'
        ],
        'respuesta': [
            '¿Quieres realizar una reservación para un hotel en %1?',
            '¿Deseas que haga una reservación para un hotel en %1?'
        ]
    },
    {
        'intent': 'reservar hotel personas',
        'regex': [
            r'Para (1|2|3|4|5|6|7|8|9|10)(.*)',
            r'(1|2|3|4|5|6|7|8|9|10)(.*)',
            r'(1|2|3|4|5|6|7|8|9|10)'
        ],
        'respuesta': [
            'Excelente, Ahora indicame la fecha de salida en formato DD MES AAAA'
        ]
    },
    {
        'intent': 'costo vuelo',
        'regex': [
            r'(precio|costo) .*vuelo.*',
            r'(Cuanto|Cuánto) .* vuelo.*',
            r'(Cuanto|Cuánto) .* vuelo .*',
            r'(precio|costo) .* vuelo .*'
        ],
        'respuesta': [
            'Para decirte el costo, dime ¿desde qué estado de la republica quieres viajar?',
            'Para indicarte el precio podrías decirme por favor ¿de qué estado de la republica quiere viajar?'
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
            r'si',
            r'sí',
            r'No',
            r'No sé',
            r'No se'
        ],
        'respuesta': [
            '' # A priori no se puede dar una respuesta, se debe considerar el contexto (ver la función self.da_respuesta_apropiada())
        ]
    },
    {
        'intent': 'huatulco',
        'regex': [
            r'Quiero (.*) Huatulco',
            r'Quisiera (.*) Huatulco',
            r'.*Huatulco.*'
        ],
        'respuesta': respuesta_elegir_destino
    },
    {
        'intent': 'cancun',
        'regex': [
            r'Quiero (.*) Cancun',
            r'Quisiera (.*) Cancun',
            r'.*Cancun.*'
        ],
        'respuesta': respuesta_elegir_destino
    },
    {
        'intent': 'acapulco',
        'regex': [
            r'Quiero (.*) Acapulco',
            r'Quisiera (.*) Acapulco',
            r'.*Acapulco.*'
        ],
        'respuesta': respuesta_elegir_destino
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
    },
       
  
]

#----------------------------------------------------------------------
# Diccionario que representa grupos de información
# Ejemplo de información que podría consultarse de manera externa,
# ser generada, o auxiliar en la redacción de una respuesta del chatbot.
#----------------------------------------------------------------------
destinosNi = {
            "huatulco" : 1,
            "cancun" : 2,
            "acapulco" : 3,
        }

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

huatulco = {
        'nombre' : 'Huatulco',
        'hoteles' : hotelesHuatulco,
        'comidas' : comidaTipicaHuatulco,
        'restaurantes' : restaurantesHuatulco,
        'atractivos' : atractivosHuatulco,
        'clima' : [{ 'nombre' : 'El clima en Huatulco es tropical, cálido y húmedo, temperatura promedio de 27°'}]
    }

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
        'nombre': 'Cochinita Pibil'
    },
    {
        'nombre': 'Sopa de Lima'
    },
    {
        'nombre': 'Panuchos'
    },
    {
        'nombre': 'Ceviche'
    },
    {
        'nombre': 'Tacos de pescado'
    },
    {
        'nombre': 'Salbutes'
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

cancun = {
        'nombre' : 'Cancun',
        'hoteles' : hotelesCancun,
        'comidas' : comidaTipicaCancun,
        'restaurantes' : restaurantesCancun,
        'atractivos' : atractivosCancun,
        'clima' : [{ 'nombre' : 'El clima en Cancun es tropical, cálido y húmedo, temperatura promedio de 26°'}]
    }

#ACAPULCO

hotelesAcapulco = [
    {
        'nombre': '-Krystal Beach Acapulco: $950 la noche por persona, todo incluido',
        'estrellas': '5 estrellas'
    },
    {
        'nombre': 'Romano Palace: $1,200 la noche por persona, todo incluido',
        'estrellas': '5 estrellas'
    },
    {
        'nombre': 'Playa Suites Acapulco: $750 la noche por persona, desayuno incluido',
        'estrellas': '5 estrellas'
    },
    {
        'nombre': 'Las Brisas Acapulco: $1,500 la noche por persona, desayuno incluido',
        'estrellas': '5 estrellas'
    }
]

comidaTipicaAcapulco = [
    {
        'nombre': 'Pulpos en su tinta'
    },
    {
        'nombre': 'Pescado a la Talla'
    },
    {
        'nombre': 'Pozole verde'
    },
    {
        'nombre': 'Camarones al mojo de ajo'
    },
    {
        'nombre': 'Ceviche'
    },
    {
        'nombre': 'Sopa de pescados y mariscos'
    }
]

restaurantesAcapulco= [
    {
        'nombre': '-Carlos and Charlies Acapulco: Muy buena música y un gran ambiente. El mojito es la mejor bebida del lugar!'
    },
    {
        'nombre': 'Lupe de Arena: Un gran lugar para disfrutar de comida mexicanay mariscos.'
    },
    {
        'nombre': 'La Finca Acapulco: Deliciosa paella y como siempre la mejor atención.'
    },
]

atractivosAcapulco = [
    {
        'nombre': 'La Quebrada: un magnífico espacio de arte y vista en el que podrás evidenciar las actividades de clavadistas para los que no le tienen miedo a la adrenalina.'
    },
    {
        'nombre': 'Parque Papagayo: visita los tres lagos artificiales y sus extensas áreas verdes, donde encontrarte con la diversidad de flora y fauna exótica no será novedad.'
    },
    {
        'nombre': 'Tirolesa Xtasea: la tirolesa más grande del mundo sobre el nivel del mar, te ofrece una altura de 100mts sobre la montaña y 700mts sobre el mar con una longitud de 1800mts.'
    },
    {
        'nombre': 'Grutas de Cacahuamilpa: el lugar de los sistemas de cuevas y formaciones calcáreas que presenta 19 salones de forma natural e iluminados con su respectivo nombre, llenos de estalagmitas y estalactitas, toda una aventura'
    }
]

acapulco = {
        'nombre' : 'Acapulco',
        'hoteles' : hotelesAcapulco,
        'comidas' : comidaTipicaAcapulco,
        'restaurantes' : restaurantesAcapulco,
        'atractivos' : atractivosAcapulco,
        'clima' : [{ 'nombre' : 'En Acapulco, la temporada de lluvia es nublada, la temporada seca es parcialmente nublada y es muy caliente y opresivo durante todo el año. Durante el transcurso del año, la temperatura generalmente varía de 21 °C a 32 °C y rara vez baja a menos de 18 °C o sube a más de 33 °C.'}]
    }


destinos = {
    1 : huatulco,
    2 : cancun,
    3 : acapulco,
    }

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
    #print('-Puerto Vallarta')
    print('='*72)
    print('¿En que te puedo apoyar?')

    input_usuario = ''
    asistente = chatbot()
    while input_usuario != 'salir':
        try:
            input_usuario = input('> ')
            #print(destinos.get(1))
        except EOFError:
            print('Saliendo...')
        else:
            print(asistente.responder(input_usuario))

if __name__ == "__main__":
    command_interface()