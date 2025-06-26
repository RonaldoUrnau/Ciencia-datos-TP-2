# Análisis de Datos de Fórmula 1 (1950-2024)

Este proyecto tiene como objetivo analizar datos históricos de la Fórmula 1 desde 1950 hasta 2024 para responder a una serie de preguntas de investigación y visualizar los resultados.

## Estructura del Proyecto

El proyecto se organiza de la siguiente manera:

- `archive/`: Contiene todos los archivos CSV con los datos de la Fórmula 1, así como los scripts de análisis y los gráficos generados.
    - `archive/f1_analysis.py`: Script principal de Python para el análisis de datos y la generación de visualizaciones.
    - `archive/F1_Data_Analysis_Plan.md`: Plan detallado del análisis de datos, incluyendo las preguntas de investigación y la estrategia de implementación.
    - Archivos CSV: `circuits.csv`, `constructor_results.csv`, `constructor_standings.csv`, `constructors.csv`, `driver_standings.csv`, `drivers.csv`, `lap_times.csv`, `pit_stops.csv`, `qualifying.csv`, `races.csv`, `results.csv`, `seasons.csv`, `sprint_results.csv`, `status.csv`.
    - Archivos de gráficos: `q3_argentinian_proportion_pie_chart.png`, `q3_top_nationalities_bar_chart.png`, `q4_top_points_scorers_bar_chart.png`, `q5_top_winners_bar_chart.png`, `q6_argentinian_champions_bar_chart.png`, `q7_argentinian_points_over_years_line_chart.png`, `q7_argentinian_win_proportion_line_chart.png`, `q8_franco_colapinto_points_per_race_bar_chart.png`.

## Preguntas de Investigación

El análisis aborda las siguientes preguntas:

1.  ¿Quién fue el primer piloto en participar en una carrera? ¿Quién fue el último?
2.  ¿Quién fue el primer piloto en ganar una carrera de Fórmula 1? ¿Y el último?
3.  ¿Cuántos pilotos argentinos participaron de la Fórmula 1? ¿Cuántos argentinos hubo en comparación con otras nacionalidades?
4.  ¿Cuántos puntos ganaron en total cada uno de los pilotos?
5.  ¿Cuántas victorias acumularon los pilotos? ¿Cuál fue el piloto más ganador?
6.  ¿Cuántos campeonatos tienen los pilotos argentinos? ¿Quiénes?
7.  ¿Cómo fue el rendimiento de los pilotos argentinos con el paso de los años? ¿Cuál fue el año con mayor proporción de victorias?
8.  ¿Es posible sacar conclusiones sobre el rendimiento de Franco Colapinto? Justificar su respuesta.

## Metodología

El análisis se realiza mediante un script de Python (`f1_analysis.py`) que utiliza las siguientes bibliotecas:

-   **Pandas**: Para la carga, limpieza y manipulación de datos.
-   **Matplotlib** y **Seaborn**: Para la generación de visualizaciones.

El script carga los datos de los archivos CSV, realiza las uniones y transformaciones necesarias, calcula las métricas para responder a cada pregunta y genera gráficos que se guardan como archivos PNG.

## Cómo Ejecutar el Análisis

Para ejecutar el análisis, sigue estos pasos:

1.  **Clona este repositorio:**
    ```bash
    git clone https://github.com/RonaldoUrnau/Ciencia-datos-TP-2.git
    ```
2.  **Navega al directorio del proyecto:**
    ```bash
    cd Ciencia-datos-TP-2
    ```
3.  **Instala las dependencias de Python:**
    Asegúrate de tener Python instalado. Luego, puedes instalar las bibliotecas necesarias usando pip:
    ```bash
    pip install pandas matplotlib seaborn
    ```
4.  **Ejecuta el script de análisis:**
    ```bash
    python archive/f1_analysis.py
    ```

Una vez ejecutado, el script generará los gráficos en el directorio `archive/`.





