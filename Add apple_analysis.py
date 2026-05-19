import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Descargar datos
datos = yf.download("AAPL", period="2y")
datos.columns = datos.columns.get_level_values(0)

# ==================== ESTADÍSTICAS BÁSICAS ====================
print("="*60)
print("ANÁLISIS APPLE (AAPL) - ÚLTIMOS 2 AÑOS")
print("="*60)

print(f"\nPrecio Actual: ${datos['Close'].iloc[-1]:.2f} USD")
print(f"Precio Más Alto: ${datos['High'].max():.2f} USD")
print(f"Precio Más Bajo: ${datos['Low'].min():.2f} USD")
print(f"Precio Promedio: ${datos['Close'].mean():.2f} USD")
print(f"Volumen Promedio: {int(datos['Volume'].mean()):,} acciones")

# ==================== RETORNOS ====================
datos['Retorno_Diario'] = datos['Close'].pct_change() * 100

print(f"\nRetorno Diario Promedio: {datos['Retorno_Diario'].mean():.3f}%")
print(f"Retorno Máximo: {datos['Retorno_Diario'].max():.2f}%")
print(f"Retorno Mínimo: {datos['Retorno_Diario'].min():.2f}%")
print(f"Volatilidad: {datos['Retorno_Diario'].std():.2f}%")

# ==================== MEDIAS MÓVILES ====================
datos['MA_50']  = datos['Close'].rolling(window=50).mean()
datos['MA_200'] = datos['Close'].rolling(window=200).mean()

print(f"\nMedia Móvil 50 días:  ${datos['MA_50'].iloc[-1]:.2f}")
print(f"Media Móvil 200 días: ${datos['MA_200'].iloc[-1]:.2f}")

# ==================== RENDIMIENTO TOTAL ====================
rendimiento_total = (datos['Close'].iloc[-1] / datos['Close'].iloc[0] - 1) * 100
print(f"\nRendimiento Total 2 años: {rendimiento_total:.2f}%")

# ==================== ÚLTIMOS 30 DÍAS ====================
ultimos_30 = datos.tail(30)
print(f"\n--- ÚLTIMOS 30 DÍAS ---")
print(f"Rendimiento: {(ultimos_30['Close'].iloc[-1] / ultimos_30['Close'].iloc[0] - 1)*100:.2f}%")
print(f"Volatilidad: {ultimos_30['Retorno_Diario'].std():.2f}%")
print(f"Volumen Promedio: {int(ultimos_30['Volume'].mean()):,} acciones")

# ==================== GRÁFICO ====================
plt.figure(figsize=(12, 6))
datos['Close'].plot(label='Precio de Cierre', color='blue')
datos['MA_50'].plot(label='Media Móvil 50 días', color='orange')
datos['MA_200'].plot(label='Media Móvil 200 días', color='red')
plt.title("Precio de Apple (AAPL) - Últimos 2 años")
plt.xlabel("Fecha")
plt.ylabel("Precio USD")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# ==================== CORRELACIÓN VOLUMEN VS PRECIO ====================
correlacion = datos['Volume'].corr(datos['Close'])
print(f"\nCorrelación Volumen vs Precio: {correlacion:.3f}")

if correlacion > 0.3:
    print("→ Cuando sube el volumen tiende a subir el precio")
elif correlacion < -0.3:
    print("→ Cuando sube el volumen tiende a bajar el precio")
else:
    print("→ No hay correlación clara entre volumen y precio")