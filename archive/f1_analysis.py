import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Establecer estilo de gráfico
sns.set_theme(style="whitegrid")

# --- Carga de Datos ---
try:
    drivers_df = pd.read_csv('drivers.csv')
    races_df = pd.read_csv('races.csv')
    results_df = pd.read_csv('results.csv')
    driver_standings_df = pd.read_csv('driver_standings.csv')
    print("Todos los archivos CSV cargados exitosamente.")
except FileNotFoundError as e:
    print(f"Error al cargar el archivo: {e}. Asegúrese de que los archivos CSV estén en el mismo directorio.")
    exit()

# --- Limpieza Inicial de Datos y Conversión de Tipos ---

# Reemplazar '\N' con NaN en todos los dataframes
drivers_df.replace('\\N', pd.NA, inplace=True)
races_df.replace('\\N', pd.NA, inplace=True)
results_df.replace('\\N', pd.NA, inplace=True)
driver_standings_df.replace('\\N', pd.NA, inplace=True)

# Convertir la columna 'date' en races_df a datetime
races_df['date'] = pd.to_datetime(races_df['date'])

# Convertir 'points' en results_df a numérico, forzando errores a NaN y luego rellenando con 0
results_df['points'] = pd.to_numeric(results_df['points'], errors='coerce').fillna(0)

# Convertir 'positionOrder' en results_df a numérico, forzando errores a NaN
results_df['positionOrder'] = pd.to_numeric(results_df['positionOrder'], errors='coerce')

# Convertir 'wins' en driver_standings_df a numérico
driver_standings_df['wins'] = pd.to_numeric(driver_standings_df['wins'], errors='coerce').fillna(0)

print("Limpieza inicial de datos y conversión de tipos completada.")

# --- Pregunta 1: Primer y Último Piloto en Participar ---
print("\n--- Pregunta 1: Primer y Último Piloto en Participar ---")
# Unir resultados con carreras y pilotos
q1_df = results_df.merge(races_df[['raceId', 'date']], on='raceId')
q1_df = q1_df.merge(drivers_df[['driverId', 'forename', 'surname']], on='driverId')

# Primera participación
first_race_date = q1_df['date'].min()
first_pilots = q1_df[q1_df['date'] == first_race_date]['driverId'].unique()
first_pilots_names = drivers_df[drivers_df['driverId'].isin(first_pilots)]
print(f"Primer(os) piloto(s) en participar (el {first_race_date.strftime('%Y-%m-%d')}):")
for index, row in first_pilots_names.iterrows():
    print(f"- {row['forename']} {row['surname']}")

# Última participación
last_race_date = q1_df['date'].max()
last_pilots = q1_df[q1_df['date'] == last_race_date]['driverId'].unique()
last_pilots_names = drivers_df[drivers_df['driverId'].isin(last_pilots)]
print(f"Último(s) piloto(s) en participar (el {last_race_date.strftime('%Y-%m-%d')}):")
for index, row in last_pilots_names.iterrows():
    print(f"- {row['forename']} {row['surname']}")

# --- Pregunta 2: Primer y Último Piloto en Ganar una Carrera ---
print("\n--- Pregunta 2: Primer y Último Piloto en Ganar una Carrera ---")
# Filtrar por ganadores (positionOrder = 1)
winners_df = q1_df[q1_df['positionOrder'] == 1]

# Primer ganador
first_winner_date = winners_df['date'].min()
first_winner = winners_df[winners_df['date'] == first_winner_date]['driverId'].iloc[0]
first_winner_name = drivers_df[drivers_df['driverId'] == first_winner].iloc[0]
print(f"Primer piloto en ganar una carrera (el {first_winner_date.strftime('%Y-%m-%d')}): {first_winner_name['forename']} {first_winner_name['surname']}")

# Último ganador
last_winner_date = winners_df['date'].max()
last_winner = winners_df[winners_df['date'] == last_winner_date]['driverId'].iloc[0]
last_winner_name = drivers_df[drivers_df['driverId'] == last_winner].iloc[0]
print(f"Último piloto en ganar una carrera (el {last_winner_date.strftime('%Y-%m-%d')}): {last_winner_name['forename']} {last_winner_name['surname']}")

# --- Pregunta 3: Cantidad de Pilotos Argentinos y Comparación ---
print("\n--- Pregunta 3: Cantidad de Pilotos Argentinos y Comparación ---")
argentinian_drivers = drivers_df[drivers_df['nationality'] == 'Argentine'] # Corregido el string de nacionalidad
num_argentinian_drivers = len(argentinian_drivers)
print(f"Número de pilotos argentinos que participaron en la Fórmula 1: {num_argentinian_drivers}")

nationality_counts = drivers_df['nationality'].value_counts()
print("\nComparación con otras nacionalidades (Top 10):")
print(nationality_counts.head(10))

# Visualización para P3: Gráfico de Barras de las Principales Nacionalidades
plt.figure(figsize=(12, 7))
sns.barplot(x=nationality_counts.head(10).index, y=nationality_counts.head(10).values, hue=nationality_counts.head(10).index, palette='viridis', legend=False)
plt.title('Top 10 Nacionalidades por Número de Pilotos de F1')
plt.xlabel('Nacionalidad')
plt.ylabel('Número de Pilotos')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('q3_top_nationalities_bar_chart.png')
plt.close()
print("Gráfico 'q3_top_nationalities_bar_chart.png' guardado.")

# Visualización para P3: Gráfico de Torta para Argentinos vs Otros
other_nationalities_count = nationality_counts.sum() - num_argentinian_drivers
pie_data = pd.Series({'Argentino': num_argentinian_drivers, 'Otros': other_nationalities_count})
plt.figure(figsize=(8, 8))
plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightcoral'])
plt.title('Proporción de Pilotos Argentinos vs. Otras Nacionalidades')
plt.axis('equal') # Asegura que el gráfico de torta sea un círculo.
plt.tight_layout()
plt.savefig('q3_argentinian_proportion_pie_chart.png')
plt.close()
print("Gráfico 'q3_argentinian_proportion_pie_chart.png' guardado.")

# --- Pregunta 4: Puntos Totales por Piloto ---
print("\n--- Pregunta 4: Puntos Totales por Piloto ---")
# Asegurar que 'points' sea numérico y rellenar NaN con 0
results_df['points'] = pd.to_numeric(results_df['points'], errors='coerce').fillna(0)

total_points_per_driver = results_df.groupby('driverId')['points'].sum().reset_index()
total_points_per_driver = total_points_per_driver.merge(drivers_df[['driverId', 'forename', 'surname']], on='driverId')
total_points_per_driver['driverName'] = total_points_per_driver['forename'] + ' ' + total_points_per_driver['surname']
total_points_per_driver = total_points_per_driver.sort_values(by='points', ascending=False)

print("Top 10 pilotos por puntos totales:")
print(total_points_per_driver[['driverName', 'points']].head(10))

# Visualización para P4: Gráfico de Barras Horizontal de los Mayores Anotadores de Puntos
plt.figure(figsize=(12, 8))
sns.barplot(x='points', y='driverName', data=total_points_per_driver.head(20), hue='driverName', palette='coolwarm', legend=False)
plt.title('Top 20 Pilotos de F1 por Puntos Totales en su Carrera')
plt.xlabel('Puntos Totales')
plt.ylabel('Nombre del Piloto')
plt.tight_layout()
plt.savefig('q4_top_points_scorers_bar_chart.png')
plt.close()
print("Gráfico 'q4_top_points_scorers_bar_chart.png' guardado.")

# --- Pregunta 5: Victorias Totales por Piloto y Piloto Más Ganador ---
print("\n--- Pregunta 5: Victorias Totales por Piloto y Piloto Más Ganador ---")
# Filtrar por ganadores (positionOrder = 1)
winners_only_df = results_df[results_df['positionOrder'] == 1]

total_wins_per_driver = winners_only_df.groupby('driverId').size().reset_index(name='wins')
total_wins_per_driver = total_wins_per_driver.merge(drivers_df[['driverId', 'forename', 'surname']], on='driverId')
total_wins_per_driver['driverName'] = total_wins_per_driver['forename'] + ' ' + total_wins_per_driver['surname']
total_wins_per_driver = total_wins_per_driver.sort_values(by='wins', ascending=False)

print("Top 10 pilotos por victorias totales:")
print(total_wins_per_driver[['driverName', 'wins']].head(10))

most_winning_pilot = total_wins_per_driver.iloc[0]
print(f"\nPiloto más ganador: {most_winning_pilot['driverName']} con {most_winning_pilot['wins']} victorias.")

# Visualización para P5: Gráfico de Barras Horizontal de los Mayores Ganadores
plt.figure(figsize=(12, 8))
sns.barplot(x='wins', y='driverName', data=total_wins_per_driver.head(20), hue='driverName', palette='rocket', legend=False)
plt.title('Top 20 Pilotos de F1 por Victorias Totales en su Carrera')
plt.xlabel('Victorias Totales')
plt.ylabel('Nombre del Piloto')
plt.tight_layout()
plt.savefig('q5_top_winners_bar_chart.png')
plt.close()
print("Gráfico 'q5_top_winners_bar_chart.png' guardado.")

# --- Pregunta 6: Campeonatos Argentinos ---
print("\n--- Pregunta 6: Campeonatos Argentinos ---")
# Unir driver_standings con carreras y pilotos
q6_df = driver_standings_df.merge(races_df[['raceId', 'year']], on='raceId')
q6_df = q6_df.merge(drivers_df[['driverId', 'forename', 'surname', 'nationality']], on='driverId')

# Filtrar por pilotos argentinos
argentinian_champions_candidates = q6_df[q6_df['nationality'] == 'Argentine'] # Corregido el string de nacionalidad

# Para encontrar campeones, necesitamos las clasificaciones al final de cada temporada
# Obtener el último raceId para cada año
last_race_of_year = races_df.groupby('year')['raceId'].max().reset_index()
last_race_of_year.rename(columns={'raceId': 'last_raceId'}, inplace=True)

# Unir driver_standings con last_race_of_year para obtener las clasificaciones de fin de temporada
end_of_season_standings = driver_standings_df.merge(last_race_of_year, left_on='raceId', right_on='last_raceId')

# Filtrar por campeones (position = 1)
champions = end_of_season_standings[end_of_season_standings['position'] == 1]

# Unir con pilotos para obtener nacionalidad y nombre
champions = champions.merge(drivers_df[['driverId', 'forename', 'surname', 'nationality']], on='driverId')

# Filtrar por campeones argentinos
argentinian_champions = champions[champions['nationality'] == 'Argentine'] # Corregido el string de nacionalidad

if not argentinian_champions.empty:
    argentinian_championships_count = argentinian_champions.groupby(['driverId', 'forename', 'surname']).size().reset_index(name='championships')
    argentinian_championships_count['driverName'] = argentinian_championships_count['forename'] + ' ' + argentinian_championships_count['surname']
    print("Pilotos argentinos y sus campeonatos:")
    print(argentinian_championships_count[['driverName', 'championships']])

    # Visualización para P6: Gráfico de Barras de Campeones Argentinos
    plt.figure(figsize=(10, 6))
    sns.barplot(x='championships', y='driverName', data=argentinian_championships_count.sort_values(by='championships', ascending=False), hue='driverName', palette='magma', legend=False)
    plt.title('Número de Campeonatos para Pilotos Argentinos de F1')
    plt.xlabel('Número de Campeonatos')
    plt.ylabel('Nombre del Piloto')
    plt.tight_layout()
    plt.savefig('q6_argentinian_champions_bar_chart.png')
    plt.close()
    print("Gráfico 'q6_argentinian_champions_bar_chart.png' guardado.")
else:
    print("No se encontraron campeones argentinos en el conjunto de datos.")

# --- Pregunta 7: Rendimiento Argentino a lo Largo de los Años y Proporción de Victorias ---
print("\n--- Pregunta 7: Rendimiento Argentino a lo Largo de los Años y Proporción de Victorias ---")
# Unir resultados con carreras y pilotos
q7_df = results_df.merge(races_df[['raceId', 'year']], on='raceId')
q7_df = q7_df.merge(drivers_df[['driverId', 'nationality']], on='driverId')

# Filtrar por pilotos argentinos
argentinian_results = q7_df[q7_df['nationality'] == 'Argentine'] # Corregido el string de nacionalidad

# Calcular puntos totales por año para pilotos argentinos
argentinian_points_per_year = argentinian_results.groupby('year')['points'].sum().reset_index()
argentinian_points_per_year.rename(columns={'points': 'total_argentinian_points'}, inplace=True)
print("\nPuntos totales de pilotos argentinos por año:")
print(argentinian_points_per_year.tail()) # Mostrar los últimos años

# Visualización para P7: Gráfico de Líneas de Puntos Argentinos a lo Largo de los Años
plt.figure(figsize=(14, 7))
sns.lineplot(x='year', y='total_argentinian_points', data=argentinian_points_per_year, marker='o')
plt.title('Puntos Totales Anotados por Pilotos Argentinos de F1 por Año')
plt.xlabel('Año')
plt.ylabel('Puntos Totales')
plt.grid(True)
plt.tight_layout()
plt.savefig('q7_argentinian_points_over_years_line_chart.png')
plt.close()
print("Gráfico 'q7_argentinian_points_over_years_line_chart.png' guardado.")

# Calcular el total de carreras por año
total_races_per_year = races_df.groupby('year').size().reset_index(name='total_races')

# Calcular victorias argentinas por año
argentinian_victories_per_year = argentinian_results[argentinian_results['positionOrder'] == 1]
argentinian_victories_per_year = argentinian_victories_per_year.groupby('year').size().reset_index(name='argentinian_wins')

# Unir para calcular la proporción
q7_summary = total_races_per_year.merge(argentinian_victories_per_year, on='year', how='left').fillna(0)
q7_summary['argentinian_wins_proportion'] = q7_summary['argentinian_wins'] / q7_summary['total_races']

# Encontrar el año con la mayor proporción de victorias
year_highest_proportion = q7_summary.sort_values(by='argentinian_wins_proportion', ascending=False).iloc[0]
print(f"\nAño con la mayor proporción de victorias argentinas: {int(year_highest_proportion['year'])} con una proporción de {year_highest_proportion['argentinian_wins_proportion']:.2f} ({int(year_highest_proportion['argentinian_wins'])} victorias de {int(year_highest_proportion['total_races'])} carreras).")

# Visualización para P7: Gráfico de Líneas de la Proporción de Victorias Argentinas a lo Largo de los Años
plt.figure(figsize=(14, 7))
ax1 = sns.lineplot(x='year', y='argentinian_wins_proportion', data=q7_summary, marker='o', color='blue', label='Proporción de Victorias Argentinas')
ax1.set_xlabel('Año')
ax1.set_ylabel('Proporción de Victorias Argentinas', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = plt.twinx()
sns.lineplot(x='year', y='total_races', data=q7_summary, marker='x', color='red', linestyle='--', label='Total de Carreras')
ax2.set_ylabel('Total de Carreras por Año', color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.title('Proporción de Victorias Argentinas en F1 y Total de Carreras a lo Largo de los Años')
plt.grid(True)
plt.tight_layout()
plt.savefig('q7_argentinian_win_proportion_line_chart.png')
plt.close()
print("Gráfico 'q7_argentinian_win_proportion_line_chart.png' guardado.")

# --- Pregunta 8: Análisis de Franco Colapinto ---
print("\n--- Pregunta 8: Análisis de Franco Colapinto ---")
franco_colapinto = drivers_df[drivers_df['forename'] == 'Franco'][drivers_df['surname'] == 'Colapinto']

if not franco_colapinto.empty:
    colapinto_id = franco_colapinto['driverId'].iloc[0]
    colapinto_results = results_df[results_df['driverId'] == colapinto_id]

    if not colapinto_results.empty:
        colapinto_races = colapinto_results.merge(races_df[['raceId', 'year', 'name', 'date']], on='raceId')
        print("Columnas en colapinto_races después de la unión:", colapinto_races.columns) # Impresión de depuración
        total_points_colapinto = colapinto_results['points'].sum()
        total_wins_colapinto = colapinto_results[colapinto_results['positionOrder'] == 1].shape[0]
        num_races_colapinto = colapinto_results.shape[0]

        print(f"Datos de F1 de Franco Colapinto:")
        print(f"  Total de Carreras Participadas: {num_races_colapinto}")
        print(f"  Puntos Totales Anotados: {total_points_colapinto}")
        print(f"  Victorias Totales: {total_wins_colapinto}")
        print("\nResultados Detallados de Carrera para Franco Colapinto:")
        # Ordenar colapinto_races por fecha primero, luego seleccionar columnas para imprimir
        colapinto_races = colapinto_races.sort_values(by='date')
        print(colapinto_races[['year', 'name', 'positionText', 'points']])

        print("\nConclusión sobre el rendimiento de Franco Colapinto:")
        print("Basado en el conjunto de datos proporcionado, podemos analizar el rendimiento de Franco Colapinto observando sus carreras totales participadas, puntos anotados y victorias. Si ha participado en un número significativo de carreras y ha anotado puntos/victorias, se pueden sacar conclusiones. Si sus datos son limitados o inexistentes en este conjunto de datos (que cubre hasta 2020), entonces sería difícil sacar conclusiones completas sobre su carrera en la F1 solo con este conjunto de datos específico.")

        # Visualización para P8: Puntos de Franco Colapinto por Carrera (si existen datos)
        if num_races_colapinto > 0:
            plt.figure(figsize=(10, 6))
            sns.barplot(x='name', y='points', data=colapinto_races.sort_values(by='date'), palette='plasma')
            plt.title(f'Puntos de F1 de Franco Colapinto por Carrera ({colapinto_races["year"].min()}-{colapinto_races["year"].max()})')
            plt.xlabel('Nombre de la Carrera')
            plt.ylabel('Puntos Anotados')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('q8_franco_colapinto_points_per_race_bar_chart.png')
            plt.close()
            print("Gráfico 'q8_franco_colapinto_points_per_race_bar_chart.png' guardado.")

    else:
        print("Franco Colapinto encontrado en drivers.csv, pero no se encontraron resultados de carrera para él en results.csv.")
        print("\nConclusión sobre el rendimiento de Franco Colapinto:")
        print("No es posible sacar conclusiones sobre el rendimiento de Franco Colapinto en la F1 a partir de este conjunto de datos, ya que no hay resultados de carrera registrados para él. Este conjunto de datos cubre hasta 2024, y su participación podría no estar completamente capturada aquí si su carrera en la F1 es más extensa.")
else:
    print("Franco Colapinto no encontrado en el conjunto de datos drivers.csv.")
    print("\nConclusión sobre el rendimiento de Franco Colapinto:")
    print("No es posible sacar conclusiones sobre el rendimiento de Franco Colapinto en la F1 a partir de este conjunto de datos, ya que no está listado en el archivo drivers.csv. Este conjunto de datos cubre hasta 2024, y su carrera en la F1 podría haber comenzado más tarde o podría no estar incluido en este conjunto de datos específico.")

print("\n--- Análisis Completado ---")