#!/usr/bin/python

from calendar import EPOCH
import math
import random
from turtle import dot
from typing import Callable, Dict, List, Tuple, TypeVar, DefaultDict

from util import *

FeatureVector = Dict[str, int]
WeightVector = Dict[str, float]
Example = Tuple[FeatureVector, int]

############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction


def extractWordFeatures(x: str) -> FeatureVector:
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x:
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    res = dict()
    for palabras in x.split():
        res[palabras] = ( 1 if palabras not in res else res[palabras] +1 )
    return res
    # END_YOUR_CODE


############################################################
# Problem 3b: stochastic gradient descent

T = TypeVar('T')


def learnPredictor(trainExamples: List[Tuple[T, int]],
                   validationExamples: List[Tuple[T, int]],
                   featureExtractor: Callable[[T], FeatureVector],
                   numEpochs: int, eta: float) -> WeightVector:
    '''
    Given |trainExamples| and |validationExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of epochs to
    train |numEpochs|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Notes:
    - Only use the trainExamples for training!
    - You should call evaluatePredictor() on both trainExamples and validationExamples
    to see how you're doing as you learn after each epoch.
    - The predictor should output +1 if the score is precisely 0.
    '''
    w = {}  # feature => weight


    ejemplosDesempacados = [(featureExtractor(ejemplo[0]),ejemplo[1]) for ejemplo in trainExamples]

    #eta = eta **2 
    for t in range(numEpochs):
        for phi,y in ejemplosDesempacados:
            prodPunto = dotProduct(w,phi)*y
            
            if(prodPunto < 1) : 
                #e = eta / t -> x = eta/_/n  :  x^2 = eta^2/n    <- Intentando dividir el eta por la raiz del
                #e = e**2                                               numUpdates me truena por tiempo :(
                increment (w ,eta*y, phi)
    
    return w


############################################################
# Problem 3c: generate test case


def generateDataset(numExamples: int, weights: WeightVector) -> List[Example]:
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)

    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a score for the given weight vector.
    # y should be 1 or -1 as classified by the weight vector.
    # y should be 1 if the score is precisely 0.

    # Note that the weight vector can be arbitrary during testing.
    def generateExample() -> Tuple[Dict[str, int], int]:
        phi={}
        for valores in random.sample(list(weights) , random.randint(1,len(weights))):
            phi[valores]=random.randint(1,756)
        y= (1 if dotProduct(weights,phi)>0 else -1)
        return phi, y

    return [generateExample() for _ in range(numExamples)]


############################################################
# Problem 3d: character features


def extractCharacterFeatures(n: int) -> Callable[[str], FeatureVector]:
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces mapped to their n-gram counts.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    You may assume that n >= 1.
    '''
    def extract(x: str) -> Dict[str, int]:
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        x = x.replace(' ','')
        res = dict()
        for i in range(len(x)-n+1):
            pal = x[i:i+n] 
            res[pal] = (( 1 if pal not in res else res[pal] +1 ))
        return res
        # END_YOUR_CODE

    return extract


############################################################
# Problem 3e:


def testValuesOfN(n: int):
    '''
    Use this code to test different values of n for extractCharacterFeatures
    This code is exclusively for testing.
    Your full written solution for this problem must be in sentiment.pdf.
    '''
    trainExamples = readExamples('polarity.train')
    validationExamples = readExamples('polarity.dev')
    featureExtractor = extractCharacterFeatures(n)
    weights = learnPredictor(trainExamples,
                             validationExamples,
                             featureExtractor,
                             numEpochs=20,
                             eta=0.01)
    outputWeights(weights, 'weights')
    outputErrorAnalysis(validationExamples, featureExtractor, weights,
                        'error-analysis')  # Use this to debug
    trainError = evaluatePredictor(
        trainExamples, lambda x:
        (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
    validationError = evaluatePredictor(
        validationExamples, lambda x:
        (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
    print(("Official: train error = %s, validation error = %s" %
           (trainError, validationError)))
############################################################
# Problem 5: k-means
############################################################




def kmeans(examples: List[Dict[str, float]], K: int,
           maxEpochs: int) -> Tuple[List, List, float]:
    '''
    examples: list of examples, each example is a string-to-float dict representing a sparse vector.
    K: number of desired clusters. Assume that 0 < K <= |examples|.
    maxEpochs: maximum number of epochs to run (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments (i.e. if examples[i] belongs to centers[j], then assignments[i] = j),
            final reconstruction loss)
    '''
    # BEGIN_YOUR_CODE (our solution is 28 lines of code, but don't worry if you deviate from this)

    def ReconstructionRoss():
        suma =0
        for i in range(tamMuestra):
            suma += Distancia(i, pertenencias[i] )
        return suma

    def Distancia(idPunto , idCentro ):
        return( memPuntos[idPunto] -  2*dotProduct(examples[idPunto],pCentroides[idCentro]) + memCentroides[idCentro] )

    def PuntPertCentro(idPunto):
        distMinima = Distancia(idPunto,0)
        iMinima = 0
        for i in range(1,K):
            distAux = Distancia(idPunto,i) 
            if(distAux < distMinima):
                distMinima = distAux
                iMinima = i
        return iMinima

    def PuntoIgual(idCentro): 
        for i in range(tamMuestra):
            if( (pertenencias[i] == idCentro or pertPasadas[i] == idCentro)
                 and pertPasadas[i] != pertenencias[i]):
                return False
        return True

    def RecalcularCentro(idPunto,centro):
        res =  dict()
        numPuntos=0
        for i in range(tamMuestra):
            if(pertenencias[i] == idPunto):
                numPuntos+=1
                for key in examples[i]:
                    res[key] = (examples[i][key] if key not in res else (res[key]+examples[i][key]) )
        
        for key in res :
            res[key] = res[key]/numPuntos
        return res

    def Convergio():
        for i in range(tamMuestra):
            if(pertenencias[i] != pertPasadas[i]):
                return False

        return True

   
    tamMuestra = len(examples)
    pertenencias = [-1]*(tamMuestra+1)
    pCentroides = random.sample( examples , K) 
    
    memCentroides = [-1]*K
    memPuntos = [-1]*tamMuestra
    for i,punto in enumerate(examples):
        memPuntos[i] = dotProduct(punto,punto)
    
    #Sacamos la primera iteracion por ser especial wuuu

    for i,centroide in enumerate(pCentroides):
        memCentroides[i] = dotProduct(centroide,centroide)

    for posPunto in range(tamMuestra):
            pertenencias[posPunto]=PuntPertCentro(posPunto)

    for idCentro,centro in enumerate(pCentroides):
        pCentroides[idCentro] = RecalcularCentro(idCentro,centro)
    pertPasadas = pertenencias.copy()


    #Empieza el ciclo bien bien
    for i in range(1,maxEpochs):
        for i,centroide in enumerate(pCentroides):
            memCentroides[i] = dotProduct(centroide,centroide)

        for posPunto in range(tamMuestra):
            pertenencias[posPunto]=PuntPertCentro(posPunto)

        if(Convergio()):
            break

        for idCentro,centro in enumerate(pCentroides):
            if not PuntoIgual(idCentro):
                pCentroides[idCentro] = RecalcularCentro(idCentro,centro)

        pertPasadas = pertenencias.copy()

    return pCentroides,pertenencias,ReconstructionRoss()
    # END_YOUR_CODE
