import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auditoría ISO 27001", layout="wide")
st.title("🛡️ Evaluación de Auditoría de Sistemas - ISO 27001")

archivo = st.file_uploader("📄 Sube el archivo Excel con el cuestionario", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    respuestas = []

    st.subheader("📝 Cuestionario")

    for _, row in df.iterrows():
        valor = st.slider(
            f"{row['Dominio']} - {row['Pregunta']}",
            min_value=1, max_value=5, value=3, step=1
        )
        respuestas.append({
            "Dominio": row["Dominio"],
            "Pregunta": row["Pregunta"],
            "Respuesta": valor
        })

    if st.button("✅ Generar Informe"):
        df_resp = pd.DataFrame(respuestas)
        resumen = df_resp.groupby("Dominio")["Respuesta"].mean().reset_index()

        st.subheader("📊 Promedios por Dominio")
        st.dataframe(resumen)

        fig = px.bar(resumen, x="Dominio", y="Respuesta", color="Dominio", range_y=[0,5])
        st.plotly_chart(fig)

        st.subheader("🚦 Semáforo de Evaluación")

        for _, row in resumen.iterrows():
            dominio = row["Dominio"]
            promedio = row["Respuesta"]

            if promedio < 2.1:
                st.error(f"🔴 {dominio}: Riesgo Alto ({promedio:.2f}) – Se requiere intervención inmediata.")
            elif promedio < 3.6:
                st.warning(f"🟡 {dominio}: Riesgo Medio ({promedio:.2f}) – Oportunidad de mejora.")
            else:
                st.success(f"🟢 {dominio}: Cumplimiento Bueno ({promedio:.2f}) – Controles adecuados.")

            # Recomendaciones por dominio
            if dominio == "Seguridad Física":
                st.info("🔧 Recomendación: Fortalece los controles físicos en salas técnicas, aplica CCTV, accesos restringidos y registros automatizados.")
            elif dominio == "Gestión de Accesos":
                st.info("🔧 Recomendación: Implementa el principio de mínimo privilegio, autenticación multifactor y revisiones periódicas de usuarios.")
            elif dominio == "Gestión de Incidentes":
                st.info("🔧 Recomendación: Establece un procedimiento formal de respuesta, registro, análisis y mitigación de incidentes informáticos.")
            elif dominio == "Seguridad en BD":
                st.info("🔧 Recomendación: Asegura tus bases de datos con cifrado, respaldos automáticos y control de accesos por roles.")
