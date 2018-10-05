# -*- coding:utf-8 -*-
import csv
import math
import random


# 载入数据
def load_csv(fileName):
    lines = csv.reader(open(fileName, 'r'))
    dataSet = list(lines)
    for i in range(1, len(dataSet)):
        dataSet[i] = [float(x) for x in dataSet[i]]
    return dataSet[1:]


# 切分数据
def split_dataSet(dataSet, ratio):
    trainSet = []
    trainSize = int(len(dataSet) * ratio)
    testSet = list(dataSet)
    while len(trainSet) < trainSize:
        index = random.randrange(len(testSet))
        trainSet.append(testSet.pop(index))
    return [trainSet, testSet]


# 分类数据
def separate_by_class(dataset):
    separate = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if vector[-1] not in separate:
            separate[vector[-1]] = []
        separate[vector[-1]].append(vector)
    return separate


# 均值和标准差计算
def mean(numbers):
    return sum(numbers) / float(len(numbers))


def stdev(numbers):
    avg = mean(numbers)
    variance = sum([math.pow(x - avg, 2) for x in numbers]) / float(len(numbers) - 1)
    return math.sqrt(variance)


# 数据特征提取
def summarize(dataSet):
    summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataSet)]
    del summaries[-1]
    return summaries


def summarize_by_class(dataSet):
    separated = separate_by_class(dataSet)
    summaries = {}
    for classValue, instances in separated.items():
        summaries[classValue] = summarize(instances)
    return summaries


# 所属类概率计算
def calculate_probability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
    return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent


def calculate_probability_class(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.items():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probabilities[classValue] *= calculate_probability(x, mean, stdev)
    return probabilities


# 多重预测
def predict(summaries, inputVector):
    probabilities = calculate_probability_class(summaries, inputVector)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.items():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel


def getPredictions(summaries, testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predict(summaries, testSet[i])
        predictions.append(result)
    return predictions


# 评估精度
def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0


def main():
    fileName = 'data.csv'
    ratio = 0.7
    dataSet = load_csv(fileName)
    trainSet, testSet = split_dataSet(dataSet, ratio)
    print('Split {0} rows into train={1} and test={2} rows'.format(len(dataSet), len(trainSet), len(testSet)))
    # 训练模型
    summaries = summarize_by_class(trainSet)
    # 测试模型
    predictions = getPredictions(summaries, testSet)
    #计算精度
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy {0}%'.format(accuracy))
    # 预测数据
    data = input('Please enter height and weight:')
    testSet1 = [[float(data.split(',')[0]), float(data.split(',')[1])]]
    predictions1 = getPredictions(summaries, testSet1)
    if predictions1[0] == 1.0:
        print('Computers predict this is the girl!')
    if predictions1[0] == 0.0:
        print('Computers predict this is the man!')


main()
