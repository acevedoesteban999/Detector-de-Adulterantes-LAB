import random
import psutil

def get_cpu():
    return psutil.cpu_percent()    
    return random.randint(0,5)

def get_ram():
    return psutil.virtual_memory().percent
    return random.randint(0,4)

def get_eth():
    net_io = psutil.net_io_counters()
    ethernet_usage = net_io.bytes_sent + net_io.bytes_recv
    return ethernet_usage
    return random.randint(0,1000)

def get_temp():
    try:
        temperature=psutil.sensors_temperatures()['cpu_thermal'][0].current
    except:
        temperature=random.randint(25,60)
    return temperature
    return random.randint(0,100)

def get_storage():
    disk_usage = psutil.disk_usage('/')

    # Convertir los valores a GB
    total_space = disk_usage.total / (1024**3)
    used_space = disk_usage.used / (1024**3)
    #free_space = disk_usage.free / (1024**3)
    
    return {"total_space":round(total_space,3),"used_space":round(used_space,3),"porc":round(used_space*100/total_space,1)}