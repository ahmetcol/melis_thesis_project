import random

# Hedef noktaların sayısı
num_targets = 10

# Popülasyon boyutu
population_size = 50

# Maksimum nesil sayısı
max_generations = 100

# Çaprazlama olasılığı
crossover_prob = 0.8

# Mutasyon olasılığı
mutation_prob = 0.2

# Maksimum seyahat süresi (zaman penceresi)
max_travel_time = 100

# Her hedef için zaman penceresi aralıkları (başlangıç, bitiş)
time_windows = [(0, 20), (10, 30), (5, 25), (15, 35), (25, 45),
                (30, 50), (40, 60), (50, 70), (60, 80), (70, 90)]

# Hedef noktaları temsil eden rastgele bir başlangıç popülasyonu oluştur
def generate_population(pop_size, num_targets):
    population = []
    for _ in range(pop_size):
        chromosome = random.sample(range(num_targets), num_targets)
        population.append(chromosome)
    return population

# Seyahat süresini hesapla
def calculate_travel_time(chromosome):
    total_time = 0
    for i in range(len(chromosome) - 1):
        start, end = time_windows[chromosome[i]]
        next_start, next_end = time_windows[chromosome[i + 1]]
        travel_time = abs(next_start - end)
        total_time += travel_time
    return total_time

# Toplanan bilgiyi hesapla
def calculate_collected_info(chromosome):
    return sum([chromosome[i] for i in chromosome])

# Diğer fonksiyonlar ve genetik algoritma kodu aynı şekilde devam eder...

# Ana program
best_route = genetic_algorithm()
print("En iyi rotaya sahip birey:", best_route)


#################################################################

import pulp

# Hedef noktaların sayısı
num_targets = 10

# Zaman penceresi sayısı
num_time_windows = 5

# İha kapasitesi
max_capacity = 3

# Hedeflerin toplanan bilgi miktarı
info_collected = [5, 8, 10, 4, 6, 7, 9, 3, 5, 2]

# Seyahat süresi matrisi (örnek veri, kendinize göre güncelleyin)
travel_time_matrix = [
    [0, 12, 18, 8, 10],
    [12, 0, 9, 6, 15],
    [18, 9, 0, 7, 11],
    [8, 6, 7, 0, 5],
    [10, 15, 11, 5, 0],
    [14, 10, 5, 7, 8],
    [6, 7, 8, 4, 3],
    [11, 3, 7, 2, 6],
    [4, 8, 5, 3, 9],
    [9, 4, 7, 2, 5]
]

# PuLP modeli oluşturma
model = pulp.LpProblem("Multi-Objective Drone Routing", pulp.LpMaximize)

# Değişkenler
x = [[pulp.LpVariable(f"x_{i}_{j}", cat=pulp.LpBinary) for j in range(num_time_windows)] for i in range(num_targets)]

# Hedef fonksiyonu (Toplanan bilgiyi maksimize et, seyahat süresini minimize et)
objective = pulp.lpSum(x[i][j] * (info_collected[i] - travel_time_matrix[i][j]) for i in range(num_targets) for j in range(num_time_windows))
model += objective

# Kısıtlar
for i in range(num_targets):
    model += pulp.lpSum(x[i]) <= 1  # Her hedef yalnızca bir kez ziyaret edilebilir
for j in range(num_time_windows):
    model += pulp.lpSum(x[i][j] for i in range(num_targets)) <= 1  # Her zaman penceresinde yalnızca bir iha bulunabilir
model += pulp.lpSum(x[i][j] * max_capacity for i in range(num_targets) for j in range(num_time_windows)) <= max_capacity  # Kapasite kısıtı

# Modeli çözme
model.solve()

# Sonuçları yazdırma
print("Optimal Rota:")
for i in range(num_targets):
    for j in range(num_time_windows):
        if pulp.value(x[i][j]) == 1:
            print(f"Hedef {i+1} - Zaman Penceresi {j+1}")

print(f"Toplanan Bilgi: {pulp.value(objective):.2f}")
