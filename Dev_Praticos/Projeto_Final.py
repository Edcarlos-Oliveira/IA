# Importação dos modulos necessários:
import json
from flask import Flask, jsonify, request
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, ConceptsOptions, RelationsOptions, EmotionOptions, EntitiesOptions, SemanticRolesOptions, SentimentOptions, CategoriesOptions, SyntaxOptions, SyntaxOptionsTokens

# Credenciais watson:
def chave():
    authenticator = IAMAuthenticator("Sua apiKey aqui")
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2023-06-23', authenticator=authenticator)
    natural_language_understanding.set_service_url("Sua url aqui")
    return(natural_language_understanding)
    
# Comentários
def banco_dados():
    dados = {'comentarios':['Péssimo app não atende o esperado', 'Não gostei horrível', 'Adorei atende minhas necessidades', 'Lixo trava toda hora', 'Interessante tem grande potencial', 'Confesso que não uso muito', 'O app tem muita instabilidade', 'Estou tendo problemas com o uso do app', 'Muito bom excelente', 'Gostei muito achei perfeito','Lamentável app não atende o esperado', 'Gostei supera os demais apps', 'Adorei atende minhas necessidades', 'Que coisa ruim trava toda hora', 'Tem grande potencial', 'Não uso muito', 'O app tem muita falha', 'Não tenho problemas com o uso do app', 'Muito bom excelente', 'Odiei nem abre']}
    return dados

# Analisando os Positivos e Negativos
def analisador(positivos, negativos):
    dados = banco_dados()
    nlp = chave()
    for i in range(len(dados['comentarios'])):
        response = nlp.analyze(text=dados['comentarios'][i], language='pt', features=Features(sentiment=SemanticRolesOptions())).get_result(),
    
        for sent in response:
            if (sent['sentiment']['document']['label']) == 'positive':
                positivos.append(dados['comentarios'][i])
            else:
                negativos.append(dados['comentarios'][i])
    return(positivos, negativos)
    
# Analisando os substantivos Positivos
def subst_positivos(subs_positivos, positivos):
    nlp = chave()
    
    for subP in range(len(positivos)):
        response_subP = nlp.analyze(text=positivos[subP],features=Features(syntax=SyntaxOptions(sentences=True,
                                                        tokens=SyntaxOptionsTokens(lemma=True, part_of_speech=True)))).get_result(),
        for subsP in response_subP:
            if (subsP['syntax']['tokens'][2]['part_of_speech']) == 'NOUN':
                subs_positivos.append(subsP['syntax']['tokens'][2]['text'])
    return(f'Total(is): {len(subs_positivos)}, Substantivo(s): {sorted(subs_positivos)}')

# Substantivos Negativos
def subst_negativos(subs_negativos, negativos):
    nlp = chave()

    for subN in range(len(negativos)):
        response_subN = nlp.analyze(text=negativos[subN],language='pt',features=Features(syntax=SyntaxOptions(sentences=True, 
                                                        tokens=SyntaxOptionsTokens(lemma=True, part_of_speech=True)))).get_result(),
        for subsN in response_subN:
            if (subsN['syntax']['tokens'][2]['part_of_speech']) == 'NOUN':
                subs_negativos.append(subsN['syntax']['tokens'][2]['text'])
    return(f'Total(is): {len(subs_negativos)}, Substantivo(s): {sorted(subs_negativos)}')

