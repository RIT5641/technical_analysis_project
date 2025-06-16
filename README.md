# Proyecto de Análisis Técnico con backtesting

## Contexto

El análisis técnico estudia datos históricos de precios y volumen para identificar patrones, tendencias y señales estadísticas que puedan anticipar el comportamiento futuro del mercado. Debido a que los mercados son dinámicos y los parámetros afectan el rendimiento, optimizar estrategias ayuda a encontrar configuraciones más robustas que equilibren riesgo y retorno.

---

## Proyecto

Este proyecto implementa tres estrategias técnicas sobre un activo financiero (por default, AAPL) usando la librería `backtesting`. El objetivo es comparar sus desempeños, optimizar sus parámetros y evaluar su rendimiento contra una estrategia pasiva o la tasa libre de riesgo estadounidense.

### Estrategias implementadas:
- **Cruce de Medias Móviles (SMA Cross)**: Compra cuando la media móvil de corto plazo cruza hacia arriba la de largo plazo.
- **Bandas de Bollinger (BB)**: Compra si el precio rompe la banda inferior y vende si rompe la banda superior.
- **Índice de Fuerza Relativa (RSI)**: Compra si RSI < 30 (sobreventa), vende si RSI > 70 (sobrecompra).
- **Estrategia Pasiva (Buy & Hold)**: Compra una vez y mantiene la posición durante todo el periodo.

### Flujo del proyecto:
1. Descarga de precios históricos vía `yfinance`.
2. Separación cronológica en 70% para entrenamiento y 30% para prueba.
3. Optimización de parámetros clave con base en Return [%] en el set de entrenamiento.
4. Evaluación de cada estrategia en el set de prueba.
5. Comparación de resultados en términos de retorno, ratio de Sharpe y operaciones realizadas.

Todo el código está modularizado usando clases y estructuras orientadas a objetos (OOP).

---

## Cómo ejecutar

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar librerías y dependencias
```bash
pip install -r requirements.txt
```
3. Ejecutar main.py:
```bash
python main.py
```
Esto descargará los datos, entrenará las estrategias, optimizará los parámetros, ejecutará las simulaciones y mostrará los resultados en consola.
4. Abrir el archivo report.ipynb para visualizar comparaciones, tablas resumen y conclusiones finales.