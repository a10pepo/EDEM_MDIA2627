import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Renfe Tracking Dashboard", page_icon="🚆", layout="wide")

API_URL = "http://api:8000"

st.title("🚆 Panel de Control - Seguimiento de Trenes Renfe")
st.markdown("Monitorización en tiempo real y mapa interactivo de posiciones y alertas.")

if st.button("🔄 Actualizar Datos"):
    st.rerun()

col1, col2 = st.columns(2)

# --- 1. SECCIÓN DE ALERTAS ---
with col1:
    st.subheader("🚨 Alertas de Proximidad Recientes")
    try:
        response = requests.get(f"{API_URL}/getAlertas?limit=20", timeout=5)
        if response.status_code == 200:
            alertas = response.json()
            if alertas:
                df_alertas = pd.DataFrame(alertas)
                st.dataframe(
                    df_alertas[["id", "vehicle_id_1", "vehicle_id_2", "distance_meters", "lat_1", "lon_1", "lat_2", "lon_2"]],
                    use_container_width=True
                )
            else:
                st.info("No hay alertas de proximidad registradas actualmente.")
        else:
            st.error("Error al consultar las alertas en la API.")
    except requests.exceptions.ConnectionError:
        st.warning("⚠️ El servicio de API no está disponible o la base de datos está arrancando...")
    except Exception as e:
        st.error(f"Error inesperado: {e}")

# --- 2. SECCIÓN DE MAPA Y TREN INDIVIDUAL ---
with col2:
    st.subheader("📍 Mapa y Búsqueda de Tren")
    tren_id_input = st.text_input("Introduce el ID del Tren (ej. 15015):", "")
    
    if tren_id_input:
        try:
            res_tren = requests.get(f"{API_URL}/getTren/{tren_id_input}", timeout=5)
            if res_tren.status_code == 200:
                data_tren = res_tren.json()
                st.success(f"Tren encontrado: **{data_tren['vehicle_id']}** (Ruta: {data_tren.get('route_id', 'N/A')})")
                
                # Mostrar en el mapa obligatorio
                if "latitude" in data_tren and "longitude" in data_tren:
                    df_map = pd.DataFrame([{
                        "lat": data_tren["latitude"],
                        "lon": data_tren["longitude"]
                    }])
                    st.map(df_map, zoom=10)
                else:
                    st.warning("El tren no dispone de coordenadas válidas.")
            elif res_tren.status_code == 404:
                st.warning(f"No se ha encontrado ningún tren con el ID '{tren_id_input}'.")
            else:
                st.error("Error al consultar el tren.")
        except requests.exceptions.ConnectionError:
            st.warning("⚠️ No se puede conectar con la API.")
    else:
        st.info("💡 Introduce un ID de tren arriba para centrar el **mapa interactivo** en su posición actual.")

st.markdown("---")
st.caption(f"Última comprobación de la interfaz: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")