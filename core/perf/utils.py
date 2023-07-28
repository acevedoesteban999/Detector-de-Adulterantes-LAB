import random

def get_cpu():
    return random.randint(0,5)

def get_ram():
    return random.randint(0,4)

def get_eth():
    return random.randint(0,1000)

def get_temp():
    return random.randint(0,100)

def get_storage():
    dict={
        'data1': random.randint(0,1000)/1000,
        'data2': 1,
    }
    dict.update({'porc':dict.get('data1')/dict.get('data2')})
    return dict