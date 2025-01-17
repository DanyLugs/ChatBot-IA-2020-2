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

from J48 import *

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
        self.J48 = J48()

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
        caso = self.encontrar_intent_regex(user_input)
        intent = caso.get('intent')
        #Para estos casos al ser muy especificos consideramos que era mejor seguir rastreandolos con REGEX
        if(not intent in ['reservar_hotel_personas','hotel_fecha_inicio','hotel_fecha_fin','estado']):
            caso = self.encontrar_intent_j48(user_input)
            intent = caso.get('intent')
        
        self.identifica_destino(intent)
        self.identifica_contexto(intent) # Asignar contexto, es auxiliar para identificar ciertos casos particulares

        #print('Intent: ' + intent)
        #print('Contexto: ' + self.ctx)
        #print('Destino: ' + str(self.destino))

        respuesta_final = self.get_respuesta(caso)
        dic_des = destinos.get(self.destino)
        if dic_des:
            nombre_des = dic_des.get('nombre')
            if nombre_des:
                respuesta_final = respuesta_final.replace('%1', nombre_des)
        return respuesta_final

    def encontrar_intent_regex(self, user_input):
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

    def encontrar_intent_j48(self, user_input):
        '''
        Encuentra el caso o intent asociado en la base de conocimiento

        :param str user_input: El texto escrito por el usuario
        :return El diccionario que representa el caso o intent deseado
        :rtype: str
        '''
        intent = self.J48.getIntent(user_input)
        for caso in self.conocimiento:
            if caso['intent'] == intent:
                return caso
        return {}

    def get_respuesta(self,caso):
        respuesta = ""
        intent = caso.get('intent')
        if intent == 'desconocido' and self.ctx == 'reservar_hotel':
            return self.get_extra_contexto(intent)
        if intent in ['bienvenida','desconocido','dar_destinos'] or destinos.get(intent):
            respuesta = random.choice(caso['respuesta'])
            if intent == 'dar_destinos':
                dest = ""
                for desti in destinos.values():
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
        if not (intent in ['confirmar','estado','reservar_hotel_personas','hotel_fecha_inicio','hotel_fecha_fin','desconocido']):
            self.ctx = intent



    def get_extra_contexto(self, intent):
        ctx = self.ctx
        if ctx == 'costo_vuelo' and intent == 'estado':
            self.ctx = 'default'
            return 'El costo de vuelo redondo desde ese estado es de $'+ self.generar_cantidad() + ' (moneda nacional) \n ¿Te puedo ayudar con otra cosa?'
        if ctx in ['hoteles','clima'] :
            self.ctx = 'default'
            return self.get_extra_destino(ctx)
        if ctx in ['restaurantes','comidas','atractivos','actividades'] and intent == 'confirmar':
            if self.user_input.lower() in ['si','sí']:
                self.ctx = 'default'
                return self.get_extra_destino(ctx)
            else:
                self.ctx = 'default'
                return "Ok, regresando al principio..."
        if ctx == 'reservar_hotel':
            if intent == 'confirmar':
                if self.user_input.lower() in ['si','sí']:
                    return 'Favor de seleccionar un hotel de la lista de hoteles en %1 (No escriba la palabra %1)' + '\n' + self.get_extra_destino('hoteles')
                else:
                    self.ctx = 'default'
                    return "Ok, regresando al principio..."
            if intent == 'desconocido':
                for hotel in destinos.get(self.destino).get("hoteles"):
                    if simple_text(hotel.get('nombre')).find(self.user_input)>=0:
                        print(hotel.get('nombre'))
                        return "Genial! Por favor dime para cuantas personas es la reservacion"
                return 'Lo siento ese hotel no fue detectado, asugurese de escribir de forma correcta el nombre del hotel (No escriba la palabra %1)\n' +  self.get_extra_destino('hoteles')
            if intent == 'hotel_fecha_fin':
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
                respuesta =' -' + '\n -'.join(lista_resp)
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
            r'hola (.*)',
            r'.*hola.*',
            r'hola',
            r'.*buen(a|o)s (dias|tardes|noches).*'
        ],
        'respuesta': [
            'bienvenido, ¿en que te puedo ayudar?',
            'hola, ¿como te puedo apoyar?'
        ]
    },
    {
        'intent': 'dar_destinos',
        'regex': [
            r'(que|cual|dime|dame|cuales|cuales|que|cual|quiero|a que| a que).*(destinos|lugares).*',
            r'dime a donde puedo viajar.*',
            r'(.*)destinos(.*)'
        ],
        'respuesta': [
            'te dare la lista de destinos con los que contamos:',
            'estos son los lugares en los que te puedo ayudar a realizar una reservacion completa:',
            'nuestros destinos son las playas mas atractivas de mexico:'
        ]
    },
    {
        'intent': 'hoteles',
        'regex': [
            r'(que|que|cuales|cuales|quiero|quisiera|dime)(.*)hoteles(.*)',
            r'.*hoteles.*',
            r'.*hoteles*'
        ],
        'respuesta': [
            'la lista de hoteles diponibles te la muestro a continuacion:'
        ]
    },
    {
        'intent': 'restaurantes',
        'regex': [
            r'.*(restaurante|restaurantes).*',
            r'.*(restaurantes|restaurante).*',
            r'(donde|en que lugar|algun lugar) .* comer.*'
        ],
        'respuesta': [
            'si quieres comer en un bonito lugar en %1, ¿puedo mostrarte los mejores restaurantes de la zona?',
            '¿quieres que te muestre una lista con variedad de lugares para comer delicioso en %1?'
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
            '¿quieres que te muestre una lista con variedad de comida tipica de %1?'
        ]
    },
    {
        'intent': 'atractivos',
        'regex': [
            r'(que|que|cual|cuales|cuales|donde|donde) .* lugares (historicos|historicos|importantes) .*',
            r'(que|que|cual|cuales|cuales|donde|donde) .* lugares (historicos|historicos|importantes) .*',
            r'(que|que|cual|cuales|cuales|donde|donde) .* (atractivo|atractivo) (turistico|turisticos) .*'
        ],
        'respuesta': [
            '¿quieres que te muestre una lista de lugares increibles para visitar en %1'
        ]
    },
    {
        'intent': 'actividades',
        'regex': [
            r'(que|que|cuales|cuales|quiero|quisiera|dime)(.*)actividades(.*)',
            r'.*actividades.*',
            r'.*actividades*'
        ],
        'respuesta': [
            '¿quieres que te muestre una lista de actividades increibles por hacer en %1'
        ]
    },
    {
        'intent': 'clima',
        'regex': [
            r'(que|cual|dime|dame|cuales|cuales|que|cual|quiero|a que| a que).*(clima|tiempo).*',
            r'.*clima.*'
        ],
        'respuesta': [
            'a continuacion una breve descripcion del clima de %1'
        ]
    },
    {
        'intent': 'hotel_fecha_inicio',
        'regex': [
            r'[\d]{1,2} [adfjmnos]\w* [\d]{4}'
        ],
        'respuesta': [
            'muy bien, ahora indicame cuantos dias quieres quedarte en tu destino de la forma: "# dias"'
        ]
    },
    {
        'intent': 'hotel_fecha_fin',
        'regex': [
            r'.*dias'
        ],
        'respuesta': [
            'perfecto tu reservacion se ha hecho satisfacotiramente \n ¿puedo ayudarte con algo mas?',
            'muy bien, genero la reservacion de hotel para esas fechas en ese destino. ¿te puedo ayudar en algo mas?'
        ]
    },
    {
        'intent': 'reservar_hotel',
        'regex': [
            r'quiero(.*)hotel(.*)',
            r'quisiera(.*)hotel(.*)'
        ],
        'respuesta': [
            '¿quieres realizar una reservacion para un hotel en %1?',
            '¿deseas que haga una reservacion para un hotel en %1?'
        ]
    },
    {
        'intent': 'reservar_hotel_personas',
        'regex': [
            r'para (1|2|3|4|5|6|7|8|9|10)(.*)',
            r'(1|2|3|4|5|6|7|8|9|10)(.*)',
            r'(1|2|3|4|5|6|7|8|9|10)'
        ],
        'respuesta': [
            'excelente, ahora indicame la fecha de salida en formato dd mes aaaa'
        ]
    },
    {
        'intent': 'costo_vuelo',
        'regex': [
            r'(precio|costo) .*vuelo.*',
            r'(cuanto|cuanto) .* vuelo.*',
            r'(cuanto|cuanto) .* vuelo .*',
            r'(precio|costo) .* vuelo .*'
        ],
        'respuesta': [
            'para decirte el costo, dime ¿desde que estado de la republica quieres viajar?',
            'para indicarte el precio podrias decirme por favor ¿de que estado de la republica quiere viajar?'
        ]
    },
    {
        'intent': 'estado',
        'regex': [
            r'(aguascalientes|baja california|bajacalifornia sur|campeche|chiapas|chihuahua|ciudad de mexico|ciudad de mexico|df|cdmx|coahuila|colima|durango|guanajuato|guerrero|hidalgo|jalisco)',
            r'(michoacan|estado de mexico|estado de mexico|morelos|nayarit|nuevo leon|monterrey|oaxaca|puebla|queretaro|queretaro|quintana roo|san luis potosi|san luis potosi|sinaloa|sonora|tabasco|tamapulipas|tlaxcala|veracruz|yucatan|zacatecas)'
        ],
        'respuesta': [
            '' # a priori no se puede dar una respuesta, se debe considerar el contexto (ver la funcion self.da_respuesta_apropiada())
        ]
    },
    {
        'intent': 'confirmar',
        'regex': [
            r'si',
            r'claro',
            r'no',
            r'no se'
        ],
        'respuesta': [
            '' # a priori no se puede dar una respuesta, se debe considerar el contexto (ver la funcion self.da_respuesta_apropiada())
        ]
    },
    {
        'intent': 'huatulco',
        'regex': [
            r'quiero (.*) huatulco',
            r'quisiera (.*) huatulco',
            r'.*huatulco.*'
        ],
        'respuesta': respuesta_elegir_destino
    },
    {
        'intent': 'cancun',
        'regex': [
            r'quiero (.*) cancun',
            r'quisiera (.*) cancun',
            r'.*cancun.*'
        ],
        'respuesta': respuesta_elegir_destino
    },
    {
        'intent': 'acapulco',
        'regex': [
            r'quiero (.*) acapulco',
            r'quisiera (.*) acapulco',
            r'.*acapulco.*'
        ],
        'respuesta': respuesta_elegir_destino
    },
    {
        'intent': 'desconocido',
        'regex': [
            r'.*'
        ],
        'respuesta': [
            'disculpa, no comprendi lo que dices',
            'podrias reformular tu pregunta por favor'
            '¿puedes decir lo mismo con otras palabras?'
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
        'nombre': 'Las Brisas Huatulco: $950 la noche por persona, todo incluido',
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
        'nombre': 'Rocoto: Te recomendamos el carpaccio de res como entrada, filete mignon a la mostaza con tocino de plato fuerte, disfruta con vino tinto de la mejor claidad.'
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

actividadesHuatulco = [
    {
        'nombre': 'Crusero turístico: Descubra las maravillosas bahías y el esplendor costero del Parque Nacional Bahías de Hualtico en un crucero de día completo. Maravíllate ante la asombrosa vida marina, las escarpadas costas y las hermosas playas mientras navegas por los brillantes mares del Pacífico.'
    },
    {
        'nombre': 'Historia Oaxaqueña: México es el hogar de numerosos yacimientos arqueológicos, pero solo dos están en el agua. Uno es Tulum, con su fortaleza en el mar Caribe; el otro en el océano Pacífico aquí en Huatulco. Explore las ruinas con un guía local que le contará la historia y la información sobre el lugar y la región. '
    },
    {
        'nombre': 'Excursión 5 bahías: Viva la experiencia del esplendor coster de Huatulco en una excursión de 7 horas de excursión en barco de vela de la región de las bahías y playas vírgenes. En un pequeño grupo limitado a diez, navegará a la Bahía de Santa Cruz y Chahué, y se tumbará en la arena blanca de las playas vírgenes de Yerbabuena y La Entrega. '
    },
    {
        'nombre': 'Recorrido montañoso: Experimente la belleza natural de Huatulco con esta aventura ecológica en las montañas de la Sierra Madre. Después de una recogida conveniente en el hotel, observe aves tropicales y reptiles, aprenda sobre la región con un guía local informativo y disfrute de las maravillosas aguas de Emerald Falls.'
    }
]


huatulco = {
        'nombre' : 'Huatulco',
        'hoteles' : hotelesHuatulco,
        'comidas' : comidaTipicaHuatulco,
        'restaurantes' : restaurantesHuatulco,
        'atractivos' : atractivosHuatulco,
        'actividades' : actividadesHuatulco,
        'clima' : [{ 'nombre' : 'El clima en Huatulco es tropical, cálido y húmedo, temperatura promedio de 27°'}]
    }

#CANCUN

hotelesCancun = [
    {
        'nombre': 'Secrets The Vine Cancún: $6,588 la noche por persona, todo incluido',
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
        'nombre': 'Bandoneon: La decoración del lugar es preciosa y el lugar es muy limpio.'
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

actividadesCancun = [
    {
        'nombre': 'Excursión: Sumérgete en el patrimonio cultural de Yucatán en este tour de un día completo desde Cancún o la Riviera Maya, visitando Chichén Itzá (entrada no incluida), el cenote Ik Kil y Valladolid. Benefíciese del conocimiento histórico de su guía mientras explora las ruinas mayas y la ciudad colonial, luego refrésquese nadando en las frescas aguas del cenote. '
    },
    {
        'nombre': 'Todoterreno: Viaje por la jungla maya en esta visita guiada de día completo llena de acción. Súbase a su propio ATV (o con un conductor) y se diríjase a un cenote, una piscina submarina, donde podrá tomar un refrescante chapuzón. Después vuele por arriba de las copas de los árboles en una tirolina.'
    },
    {
        'nombre': 'Fiesta en Cancun: Obtén un tour VIP de los clubes nocturnos de Cancún sin preocuparte por dónde ir o cómo llegar allí. Esta excursión a un club nocturno en Cancún maneja todos los detalles de su salida nocturna mientras lo mantiene seguro, para que pueda concentrarse en divertirse. Además, esta visita guiada le brinda entrada VIP en tres de los mejores clubes de Cancún, bebidas ilimitadas y servicio ilimitado de botellas en lugares seleccionados. '
    },
    {
        'nombre': 'Recorrido turístico: Navegue desde Cancún a Isla Mujeres a bordo de un catamarán de tres pisos para un día de snorkel, baile de salsa y compras que incluye un desayuno continental, un bufé de fajitas frescas y barra libre por la tarde. Con una combinación de actividades divertidas y tiempo independiente, este emocionante crucero es una excelente manera de ver la hermosa costa caribeña desde el agua mientras se juega y se divierte con estilo.'
    }
]

cancun = {
        'nombre' : 'Cancun',
        'hoteles' : hotelesCancun,
        'comidas' : comidaTipicaCancun,
        'restaurantes' : restaurantesCancun,
        'atractivos' : atractivosCancun,
        'actividades' : actividadesCancun,
        'clima' : [{ 'nombre' : 'El clima en Cancun es tropical, cálido y húmedo, temperatura promedio de 26°'}]
    }

#ACAPULCO

hotelesAcapulco = [
    {
        'nombre': 'Krystal Beach Acapulco: $950 la noche por persona, todo incluido',
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
        'nombre': 'Carlos and Charlies Acapulco: Muy buena música y un gran ambiente. El mojito es la mejor bebida del lugar!'
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

actividadesAcapulco = [
    {
        'nombre': 'Buceo: sumergete en el majestuoso oceano en la isla de la Roqueta, usa equipo de snorkel para ver las maravillas de la naturaleza'
    },
    {
        'nombre': 'XTASEA: Vuele sobre el agua a 60 millas por hora (96 kilómetros por hora) en este tour de actividades múltiples que incluye una visita a la Capilla de la Paz y la liberación de tortugas bebés. Esta excursión privada de un día completo comienza con un emocionante viaje mientras recorre la línea de tirolesa de Xtasea.'
    },
    {
        'nombre': 'Paseo en yate: No hay mejor manera de disfrutar de la belleza de la bahía de Acapulco que navegando en un yate por el océano Pacífico y un cóctel frutal en la mano. En este recorrido de 2,5 horas al atardecer o bajo la luna, podrá disfrutar del lujo de una barra libre y escuchar música en vivo mientras navega bajo el cielo colorido o repleto de estrellas. '
    },
    {
        'nombre': 'Paseo todo incluido: Vea más de Acapulco en menos tiempo, en una visita turística para grupos pequeños, ideal para visitantes primerizos. En un pequeño grupo limitado a 15 personas, podrá marcar las principales atracciones de Acapulco, como Las Brisas, el acantilado con la Capilla de la Paz, la Bahía de Acapulco y los clavadistas de La Quebrada.'
    }
]

acapulco = {
        'nombre' : 'Acapulco',
        'hoteles' : hotelesAcapulco,
        'comidas' : comidaTipicaAcapulco,
        'restaurantes' : restaurantesAcapulco,
        'atractivos' : atractivosAcapulco,
        'actividades' : actividadesAcapulco,
        'clima' : [{ 'nombre' : 'En Acapulco, la temporada de lluvia es nublada, la temporada seca es parcialmente nublada y es muy caliente y opresivo durante todo el año. Durante el transcurso del año, la temperatura generalmente varía de 21 °C a 32 °C y rara vez baja a menos de 18 °C o sube a más de 33 °C.'}]
    }


destinos = {
    1 : huatulco,
    2 : cancun,
    3 : acapulco,
    }


def simple_text(entrada):
    '''
    Devuelve la cadena de entrada sin signos, sin acentos y en minusculas

    :param str entrada: Texto al cual se modificará
    :return text sin signos ni acentos y en minusculas
    :rtype str
    '''
    text = entrada.lower()
    text = text.replace(',', '')
    text = text.replace('?', '')
    text = text.replace('!', '')
    text = text.replace('á', 'a')
    text = text.replace('é', 'e')
    text = text.replace('í', 'i')
    text = text.replace('ó', 'o')
    text = text.replace('ú', 'u')
    text = text.replace('ñ', 'ni')

    return text

#----------------------------------------------------------------------
#  Interfaz de texto
#----------------------------------------------------------------------
def command_interface():

    asistente = chatbot()

    print('')
    print('Hola soy Rod, tu asistente personal de viajes.')
    print('-'*72)
    print('Nos especializamos en las principales playas de México:')
    print('-Huatulco')
    print('-Cancun')
    print('-Acapulco')
    print('='*72)
    print('¿En que te puedo apoyar?')

    input_usuario = ''

    while input_usuario != 'salir':
        try:
            input_usuario = input('> ')
        except EOFError:
            print('Saliendo...')
            jvm.stop()
        else:
            print(asistente.responder(simple_text(input_usuario)))
    print('Saliendo...')
    jvm.stop()
if __name__ == "__main__":
    command_interface()
