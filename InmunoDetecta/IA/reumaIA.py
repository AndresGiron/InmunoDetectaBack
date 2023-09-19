import joblib
from flask import jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.feature_extraction.text import  CountVectorizer
import os

vectorizador = TfidfVectorizer(max_features=5)

def hacerPrediccion(archivo_json):

    #Bloque para el promedio de la longitud de las palabras
    def promedioLongitudPalabras(texto):
        palabras = texto.split()  # Dividir el texto en palabras
        longitudes = [len(palabra) for palabra in palabras]
        return sum(longitudes) / len(longitudes) if longitudes else 0  # Calcular el promedio o devolver 0 si no hay palabras
    
    if archivo_json["ANCAs_titulos_y_patron_"] != "":
        valor = archivo_json["ANCAs_titulos_y_patron_"]
        if isinstance(valor, str):
            archivo_json["ANCAs_titulos_y_patron_"] = promedioLongitudPalabras(valor)
            print(archivo_json["ANCAs_titulos_y_patron_"])
    
    if archivo_json["ANAs_t_tulos_y_patr_n"] != "":
        valor = archivo_json["ANAs_t_tulos_y_patr_n"]
        if isinstance(valor, str):
            archivo_json["ANAs_t_tulos_y_patr_n"] = promedioLongitudPalabras(valor)
            print(archivo_json["ANAs_t_tulos_y_patr_n"])
            
    #Fin bloque promedio longitud de las palabras

    for key, value in archivo_json.items():
        if value == "":
            archivo_json[key] = None

    for key, value in archivo_json.items():
        if isinstance(value, bool):
            archivo_json[key] = 0 if value else 1


    data = []
    processor = joblib.load('InmunoDetecta/IA/processor.pkl')
    model = joblib.load('InmunoDetecta/IA/reuma_forest.pkl')

    data = pd.DataFrame.from_dict([archivo_json])

    #print(data)
    data_transformed = processor.transform(data)

    #print([data_transformed])

    prediccion = model.predict(data_transformed)
    archivo_json['Infeccion asociada a la enfermedad'] = prediccion.tolist()[0]
    print("prediccion ",prediccion.tolist()[0])
    return archivo_json



# ejemploObjeto = {
#     "Edad al momento del evento": 60,
#     "Genero": 0,
#     "Etnia": 0,
#     "Escolaridad": None,
#     "Coomorbilidades previas- HTA": 0,
#     "Coomorbilidades previas - Insuficiencia venosa ": 1,
#     "Coomorbilidades previas - Dislipidemia ": 1,
#     "Coomorbilidades previas - Osteoporosis": 1,
#     "Coomorbilidades previas - Cardiopatia": 1,
#     "Coomorbilidades previas - Obesidad": 1,
#     "Coomorbilidades previas - Diabetes Mellitus": 1,
#     "Coomorbilidades previas - EPOC": 1,
#     "Coomorbilidades previas - Enfermedad cerebrovascular (ECV)": 1,
#     "Coomorbilidades previas Cáncer": 0,
#     "Coomorbilidades previas Enfermedad renal cronica": 1,
#     "Coomorbilidades previas - Trastorno depresivo ": 1,
#     "Coomorbilidades previas - Hipotiroidismo": 1,
#     "Coomorbilidades previas -Tuberculosis": 1,
#     "Coomorbilidades previas  - Infeccion por VIH": 1,
#     "Coomorbilidades previas - Otras": 1,
#     "Seguimiento previo por reumatologia": 1,
#     "Dx reumatologico final agrupado": 3,
#     "Uso_de_tratamiento_antibiotico": 0,
#     "Tenía tratamiento reumatologico previo": 1,
#     "Esteroide": 1,
#     "Antimalarico": 1,
#     "Leflunomida": 1,
#     "Metotrexate": 1,
#     "Sulfasalazina": 1,
#     "Biológico": 1,
#     "Azatioprina": 1,
#     "Ciclofosfamida": 1,
#     "Micofenolato": 1,
#     "Tacrolimus": 1,
#     "Hipouricemiante": 1,
#     "Ciclosporina": 1,
#     "Otro": 1,
#     "Recibió esquema inmunosupresor en la hospitalizacion": 1,
#     "Esteroide_1": 1,
#     "Azatioprina_1": 1,
#     "Ciclofosfamida_1": 1,
#     "Micofenolato_1": 1,
#     "Tracolimus_1": 1,
#     "Ciclosporina_1": 1,
#     "Enfermedad reumatica activa_1": 1,
#     "Requerimiento de Ventilacion mecanica": 1,
#     "Requerimiento de TRR de novo": 1,
#     "Recuento_de_leucocitos_al_ingr": 1350,
#     "Recuento_de_linfocitos_al_ingr": 1060,
#     "Recuento_de_eosinofilos_al_ing": 40,
#     "Hemoglobina_al_ingreso__gr_dl_": 10,
#     "Plaquetas_al_ingreso__celulas_": 62000,
#     "Creatinina_al_ingreso": 1.12,
#     "Segun_los_hallazgos_del_uroan_Proteinas": 1,
#     "Segun_los_hallazgos_del_uroan_Eritrocitos": 0,
#     "Segun_los_hallazgos_del_uroan_Leucocitos ": 1,
#     "Segun_los_hallazgos_del_uroan_Cilindros": 1,
#     "CPK__valor_mas_representativo_": None,
#     "TGO_al_inicio_copy": 50,
#     "TGP_al_inicio__copy": 42,
#     "PCR_al_ingreso_": 145.4,
#     "VSG_al_ingreso_": None,
#     "Resultados_de_anticuerpos_anti peptido citrulinado ": None,
#     "T_tulos_Factor_Reumatoide_al_i": None,
#     "Anticuerpos_anti_DNA_dc": 1,
#     "T_tulos_Anti_DNA_dc_al_ingreso": None,
#     "T_tulos_Anti_Ro_al_ingreso": None,
#     "T_tulos_Anti_La_al_ingreso": None,
#     "T_tulos_anti_RNP_al_ingreso": None,
#     "T_tulos_anti_Sm_al_ingreso": None,
#     "T_tulos_anti_cardiolipinas_IgG": None,
#     "T_tulos_anti_cardiolipinas_IgM": None,
#     "T_tulos_anti_B__glicoproteina_": None,
#     "T_tulos_anti_B__glicopro_copy": None,
#     "Anticiaguante_lupico_por_venen": None,
#     "ANCAs_titulos_y_patron_": None,
#     "ANAs_t_tulos_y_patr_n": None,
#     "ANCAs": 1,
#     "ANAs": 1,
#     "Antigeno_de_superficie_para_hepatitis B": 1,
#     "Anticuerpos_para_Hepatitis_C": 1,
#     "ELISA_para_VIH": 1,
#     }

# ejemploObjeto2 = {
#     "Edad al momento del evento": 60,
#     "Genero": 0,
#     "Etnia": "",
#     "Escolaridad": "",
#     "Coomorbilidades previas- HTA": True,
#     "Coomorbilidades previas - Insuficiencia venosa ": False,
#     "Coomorbilidades previas - Dislipidemia ": False,
#     "Coomorbilidades previas - Osteoporosis": False,
#     "Coomorbilidades previas - Cardiopatia": True,
#     "Coomorbilidades previas - Obesidad": False,
#     "Coomorbilidades previas - Diabetes Mellitus": True,
#     "Coomorbilidades previas - EPOC": False,
#     "Coomorbilidades previas - Enfermedad cerebrovascular (ECV)": False,
#     "Coomorbilidades previas Cáncer": False,
#     "Coomorbilidades previas Enfermedad renal cronica": False,
#     "Coomorbilidades previas - Trastorno depresivo ": False,
#     "Coomorbilidades previas - Hipotiroidismo": False,
#     "Coomorbilidades previas -Tuberculosis": False,
#     "Coomorbilidades previas  - Infeccion por VIH": False,
#     "Coomorbilidades previas - Otras": False,
#     "Dx reumatologico final agrupado": "1",
#     "Seguimiento previo por reumatologia": True,
#     "Uso_de_tratamiento_antibiotico": False,
#     "Tenía tratamiento reumatologico previo": False,
#     "Esteroide": False,
#     "Antimalarico": False,
#     "Leflunomida": False,
#     "Metotrexate": False,
#     "Sulfasalazina": False,
#     "Biológico": False,
#     "Azatioprina": False,
#     "Ciclofosfamida": False,
#     "Micofenolato": False,
#     "Tacrolimus": False,
#     "Hipouricemiante": False,
#     "Ciclosporina": False,
#     "Otro": False,
#     "Recibió esquema inmunosupresor en la hospitalizacion": False,
#     "Esteroide_1": False,
#     "Azatioprina_1": False,
#     "Ciclofosfamida_1": False,
#     "Micofenolato_1": False,
#     "Tracolimus_1": False,
#     "Ciclosporina_1": False,
#     "Enfermedad reumatica activa_1": False,
#     "Requerimiento de Ventilacion mecanica": False,
#     "Requerimiento de TRR de novo": False,
#     "Recuento_de_leucocitos_al_ingr": "10410",
#     "Recuento_de_linfocitos_al_ingr": "810",
#     "Recuento_de_eosinofilos_al_ing": "10",
#     "Hemoglobina_al_ingreso__gr_dl_": "12.8",
#     "Plaquetas_al_ingreso__celulas_": "276000",
#     "Creatinina_al_ingreso": "0.71",
#     "Segun_los_hallazgos_del_uroan_Proteinas": False,
#     "Segun_los_hallazgos_del_uroan_Eritrocitos": False,
#     "Segun_los_hallazgos_del_uroan_Cilindros": False,
#     "ELISA_para_VIH": False,
#     "CPK__valor_mas_representativo_": "",
#     "TGO_al_inicio_copy": "",
#     "TGP_al_inicio__copy": "",
#     "PCR_al_ingreso_": 204.6,
#     "VSG_al_ingreso_": "",
#     "Resultados_de_anticuerpos_anti peptido citrulinado ": 8,
#     "T_tulos_Factor_Reumatoide_al_i": 10,
#     "Anticiaguante_lupico_por_venen": "",
#     "Anticuerpos_anti_DNA_dc": False,
#     "T_tulos_Anti_DNA_dc_al_ingreso": "",
#     "T_tulos_Anti_Ro_al_ingreso": "",
#     "T_tulos_Anti_La_al_ingreso": "",
#     "T_tulos_anti_RNP_al_ingreso": "",
#     "T_tulos_anti_Sm_al_ingreso": "",
#     "T_tulos_anti_cardiolipinas_IgG": "",
#     "T_tulos_anti_cardiolipinas_IgM": "",
#     "T_tulos_anti_B__glicoproteina_": "",
#     "T_tulos_anti_B__glicopro_copy": "",
#     "ANCAs": False,
#     "ANCAs_titulos_y_patron_": "",
#     "ANAs": False,
#     "ANAs_t_tulos_y_patr_n": "",
#     "Antigeno_de_superficie_para_hepatitis B": False,
#     "Anticuerpos_para_Hepatitis_C": False,
#     "Segun_los_hallazgos_del_uroan_Leucocitos ": False
# }

# print(hacerPrediccion(ejemploObjeto2))
