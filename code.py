# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from time import time
from sklearn.metrics import f1_score

student_data = pd.read_csv("student-data.csv")
print "Os dados dos estudantes foram lidos com êxito!"

n_students = len(student_data)
n_features = len(student_data.columns)
n_passed = len(student_data[student_data.passed == 'yes'])
n_failed = len(student_data[student_data.passed == 'no'])
grad_rate = float(n_passed) / n_students * 100

# Imprima os resultados
print "Número total de estudantes: {}".format(n_students)
print "Número de atributos: {}".format(n_features)
print "Número de estudantes aprovados: {}".format(n_passed)
print "Número de estudantes reprovados: {}".format(n_failed)
print "Taxa de graduação: {:.2f}%".format(grad_rate)

# Extraia as colunas dos atributo
feature_cols = list(student_data.columns[:-1])

# Extraia a coluna-alvo 'passed'
target_col = student_data.columns[-1]

# Mostre a lista de colunas
print "Colunas de atributos:\n{}".format(feature_cols)
print "\nColuna-alvo: {}".format(target_col)

# Separe os dados em atributos e variáveis-alvo (X_all e y_all)
X_all = student_data[feature_cols]
y_all = student_data[target_col]

# Mostre os atributos imprimindo as cinco primeiras linhas
print "\nFeature values:"
print X_all.head()


def preprocess_features(X):
    ''' Pré-processa os dados dos estudantes e converte as variáveis binárias
    não numéricas em variáveis binárias (0/1). Converte variáveis categóricas
    em variáveis postiças.'''

    # Inicialize nova saída DataFrame
    output = pd.DataFrame(index=X.index)

    # Observe os dados em cada coluna de atributos
    for col, col_data in X.iteritems():

        # Se o tipo de dado for não numérico, substitua todos os
        # valores yes/no por 1/0
        if col_data.dtype == object:
            col_data = col_data.replace(['yes', 'no'], [1, 0])

        # Se o tipo de dado for categórico, converta-o para uma variável dummy
        if col_data.dtype == object:
            # Example: 'school' => 'school_GP' and 'school_MS'
            col_data = pd.get_dummies(col_data, prefix=col)

        # Reúna as colunas revisadas
        output = output.join(col_data)

    return output

X_all = preprocess_features(X_all)
print "Processed feature columns ({} total features):\n{}".format(
    len(X_all.columns), list(X_all.columns))


# TODO: Importe qualquer funcionalidade adicional de que você possa
# precisar aqui
from sklearn.cross_validation import train_test_split

# TODO: Estabeleça o número de pontos de treinamento
num_train = 300

# Estabeleça o número de pontos de teste
num_test = X_all.shape[0] - num_train

# TODO: Emabaralhe e distribua o conjunto de dados de acordo com o número
# de pontos de treinamento e teste abaixo
X_train, X_test, y_train, y_test = train_test_split(
    X_all, y_all, test_size=num_test, random_state=42, stratify=y_all)

# Mostre o resultado da distribuição
print "O conjunto de treinamento tem {} amostras.".format(X_train.shape[0])
print "O conjunto de teste tem {} amostras.".format(X_test.shape[0])


def train_classifier(clf, X_train, y_train):
    ''' Ajusta um classificador para os dados de treinamento. '''

    # Inicia o relógio, treina o classificador e, então, para o relógio
    start = time()
    clf.fit(X_train, y_train)
    end = time()

    # Imprime os resultados
    print "O modelo foi treinado em {:.4f} segundos".format(end - start)


def predict_labels(clf, features, target):
    ''' Faz uma estimativa utilizando um classificador ajustado baseado
    na pontuação F1. '''

    # Inicia o relógio, faz estimativas e, então, o relógio para
    start = time()
    y_pred = clf.predict(features)
    end = time()

    # Imprime os resultados de retorno
    print "As previsões foram feitas em {:.4f} segundos.".format(end - start)
    return f1_score(target.values, y_pred, pos_label='yes')


def train_predict(clf, X_train, y_train, X_test, y_test):
    ''' Treina e faz estimativas utilizando um classificador baseado na
    pontuação do F1. '''

    # Indica o tamanho do classificador e do conjunto de treinamento
    print "Treinando um {} com {} pontos de treinamento. . .".format(
        clf.__class__.__name__, len(X_train))

    # Treina o classificador
    train_classifier(clf, X_train, y_train)

    # Imprime os resultados das estimativas de ambos treinamento e teste
    print "Pontuação F1 para o conjunto de treino: {:.4f}.".format(
        predict_labels(clf, X_train, y_train))
    print "Pontuação F1 para o conjunto de teste: {:.4f}.".format(
        predict_labels(clf, X_test, y_test))

# TODO: Importe os três modelos de aprendizagem supervisionada do sklearn
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn import tree


# TODO: Inicialize os três modelos
clf_A = SVC(random_state=42)
clf_B = LogisticRegression(random_state=42)
clf_C = tree.DecisionTreeClassifier(random_state=42)


# TODO: Configure os tamanho dos conjuntos de treinamento
print ''
print ''
print 'Modelo SVC:'
for n in [100, 200, 300]:
    train_predict(clf_A, X_train[:n], y_train[:n], X_test, y_test)
    print ''

print ''
print ''
print 'Modelo Regressão logistica:'
for n in [100, 200, 300]:
    train_predict(clf_B, X_train[:n], y_train[:n], X_test, y_test)
    print ''

print ''
print ''
print 'Modelo Arvore de decisão:'
for n in [100, 200, 300]:
    train_predict(clf_C, X_train[:n], y_train[:n], X_test, y_test)
    print ''


# TODO: Importe 'GridSearchCV' e 'make_scorer'
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.metrics import f1_score


# TODO: Crie a lista de parâmetros que você gostaria de calibrar
parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}

# TODO: Inicialize o classificador
clf = SVC(random_state=0)

# TODO: Faça uma função de pontuação f1 utilizando 'make_scorer'
f1_scorer = make_scorer(f1_score, pos_label='yes')

# TODO: Execute uma busca em matriz no classificador utilizando o f1_scorer
# como método de pontuação
grid_obj = GridSearchCV(clf, param_grid=parameters, scoring=f1_scorer)


# TODO: Ajuste o objeto de busca em matriz para o treinamento de dados e
# encontre os parâmetros ótimos
grid_obj = grid_obj.fit(X_train, y_train)

# Get the estimator
clf = grid_obj.best_estimator_

# Reporte a pontuação final F1 para treinamento e teste depois de calibrar os
# parâmetros print "Tuned model has a training F1 score of {:.4f}.".format(
# predict_labels(clf, X_train, y_train))
print "O modelo calibrado tem F1 de {:.4f} no conjunto de treinamento.".format(
    predict_labels(clf, X_train, y_train))
print "O modelo calibrado tem F1 de {:.4f} no conjunto de teste.".format(
    predict_labels(clf, X_test, y_test))