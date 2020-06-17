import string
import re

import weka.core.jvm as jvm
import weka.core.converters as converters
from weka.classifiers import Classifier
from weka.core.dataset import Attribute, Instance, Instances

class J48:

    def __init__(self):
        jvm.start()

        data_dir = "./DataSet/"
        self.data = converters.load_any_file(data_dir + "chatbot2.arff")
        self.data.class_is_last()

        self.cls = Classifier(classname="weka.classifiers.trees.J48")
        self.cls.build_classifier(self.data)

        self.intens = self.data.attribute_by_name("intent")


    def transformUserInput(self,user_input):
        '''
        Transforma la entrada del usuario a una representación de 1s y 0s para poder realizar una predicción.

        :param str entrada del usuario
        :return str de 1s y 0s
        :rtype str
        '''
        attributes = self.data.attribute_names()
        data_size = len(attributes)
        vector_input = ['0']*(data_size)

        words = user_input.split()
        attribute_map = { attributes[i] : i for i in range(len(attributes)) }

        for word in words:
            if word in attributes:
                vector_input[attribute_map.get(word)] = '1'

        vector_input[data_size-1] = Instance.missing_value()

        return vector_input



    def getIntent(self,user_input):
        '''
        Identifica el intent por medio de una entrada de usuario y una data haciendo una predicción.

        :param str entrada del usuario
        :param data representación del dataset de GLaDOS
        :return cadena con el intent identificado
        :rtype str
        '''
        vector_input = self.transformUserInput(user_input)

        inst = Instance.create_instance(vector_input)
        #print(inst)
        self.data.add_instance(inst)


        for index, inst in enumerate(self.data):
                pred = int(self.cls.classify_instance(inst))
                dist = self.cls.distribution_for_instance(inst)
                #print("{}: label index={}, class distribution={}".format(index+1, pred, dist))
        
        intent = "desconocido"

        pred = int(self.cls.classify_instance(inst))
        dist = self.cls.distribution_for_instance(inst)
        #print("{}: label index={}, class distribution={}".format(index+1, pred, dist))

        if max(dist) > 0.7:
            intent = self.intens.value(pred)

        return intent
