import streamlit as st
from modules.storage import load_employees
from modules.pdf_generator import generate_payroll_pdf

# CONFIG

st.set_page_config(
    page_title="Sistema RRHH Nómina",
    layout="wide"
)

# HEADER

st.title("🏢 Sistema RRHH — Nómina")

st.markdown("""
### Living Lounge S.A.

**Cédula Jurídica:** 3-101-663107  
**Teléfono:** 2290-8788  
**Dirección:** Sabana Oeste, 400 mts oeste, frente a Cemaco
""")

# PERIODO

c1,c2,c3 = st.columns(3)

with c1:
    fecha_desde = st.date_input("Fecha Desde")

with c2:
    fecha_hasta = st.date_input("Fecha Hasta")

with c3:
    tipo_planilla = st.selectbox(
        "Tipo Planilla",
        ["Semanal","Quincenal","Mensual"]
    )

st.divider()

# LOAD EMPLOYEES

df = load_employees()

# KPIs

k1,k2,k3 = st.columns(3)

with k1:
    st.metric("Colaboradores",len(df))

with k2:
    st.metric(
        "Salario Base Total",
        f"₡{df['salario_mensual'].sum():,.0f}"
    )

with k3:
    st.metric("Periodo",tipo_planilla)

st.divider()

st.subheader("Colaboradores")

# STORAGE RESULTADOS PDF

payroll_results = []

# LOOP EMPLEADOS

for idx,row in df.iterrows():

    salario_mensual = float(row["salario_mensual"])

    salario_diario = salario_mensual / 30

    salario_hora = salario_diario / 8

    with st.expander(
        f"{row['nombre']} | {row['puesto']} | ₡{salario_mensual:,.0f}"
    ):

        st.info(f"""

Salario Mensual: ₡{salario_mensual:,.0f}

Salario Diario: ₡{salario_diario:,.2f}

Salario Hora: ₡{salario_hora:,.2f}

""")

        st.markdown("### Devengados")

        d1,d2,d3 = st.columns(3)

        with d1:

            horas_bruto = st.number_input(
                "1001 Salario Bruto (Horas)",
                value=48.0,
                key=f"1001_{idx}"
            )

            convenio_horas = st.number_input(
                "1002 Convenio 12 Horas",
                value=0.0,
                key=f"1002_{idx}"
            )

            extra15_horas = st.number_input(
                "1003 Horas Extra x1.5",
                value=0.0,
                key=f"1003_{idx}"
            )

        with d2:

            extra2_horas = st.number_input(
                "1004 Horas Extra x2",
                value=0.0,
                key=f"1004_{idx}"
            )

            feriado_horas = st.number_input(
                "1005 Feriado Pago Obligatorio",
                value=0.0,
                key=f"1005_{idx}"
            )

            feriado2_horas = st.number_input(
                "1006 Horas x2 Feriado",
                value=0.0,
                key=f"1006_{idx}"
            )

        with d3:

            comisiones = st.number_input(
                "1007 Comisiones",
                value=0.0,
                key=f"1007_{idx}"
            )

        # CALCULOS

        salario_bruto = horas_bruto * salario_hora

        convenio = convenio_horas * salario_hora

        extra15 = extra15_horas * salario_hora * 1.5

        extra2 = extra2_horas * salario_hora * 2

        feriado = feriado_horas * salario_hora

        feriado2 = feriado2_horas * salario_hora * 2

        total_devengado = (

            salario_bruto +
            convenio +
            extra15 +
            extra2 +
            feriado +
            feriado2 +
            comisiones

        )

        # DEDUCCIONES

        sem = total_devengado * 0.055

        ivm = total_devengado * 0.0433

        banco = total_devengado * 0.01

        st.divider()

        st.markdown("### Deducciones Automáticas")

        x1,x2,x3 = st.columns(3)

        with x1:

            st.metric(
                "1008 SEM 5.5%",
                f"₡{sem:,.0f}"
            )

            st.metric(
                "1009 IVM 4.33%",
                f"₡{ivm:,.0f}"
            )

        with x2:

            st.metric(
                "1010 Banco Popular 1%",
                f"₡{banco:,.0f}"
            )

        with x3:

            embargos = st.number_input(
                "1012 Embargos",
                value=0.0,
                key=f"embargos_{idx}"
            )

            renta = st.number_input(
                "1011 Renta",
                value=0.0,
                key=f"renta_{idx}"
            )

        total_deducciones = (

            sem +
            ivm +
            banco +
            renta +
            embargos

        )

        salario_neto = (

            total_devengado -
            total_deducciones

        )

        st.divider()

        r1,r2,r3 = st.columns(3)

        with r1:
            st.metric(
                "Total Devengado",
                f"₡{total_devengado:,.0f}"
            )

        with r2:
            st.metric(
                "Total Deducciones",
                f"₡{total_deducciones:,.0f}"
            )

        with r3:
            st.metric(
                "Salario Neto",
                f"₡{salario_neto:,.0f}"
            )

        # GUARDAR RESULTADOS

        payroll_results.append({

            "empleado":row,

            "salario_mensual":salario_mensual,
            "salario_hora":salario_hora,

            "salario_bruto":salario_bruto,
            "convenio":convenio,
            "extra15":extra15,
            "extra2":extra2,
            "feriado":feriado,
            "feriado2":feriado2,
            "comisiones":comisiones,

            "sem":sem,
            "ivm":ivm,
            "banco":banco,
            "renta":renta,
            "embargos":embargos,

            "total_devengado":total_devengado,
            "total_deducciones":total_deducciones,
            "salario_neto":salario_neto

        })

st.divider()

# GENERADOR PDF

if st.button("📄 Generar PDFs"):

    fecha_pago = fecha_hasta.strftime("%Y-%m-%d")

    for p in payroll_results:

        generate_payroll_pdf(

            empleado=p["empleado"],

            fecha_pago=fecha_pago,

            salario_mensual=p["salario_mensual"],
            salario_hora=p["salario_hora"],

            salario_bruto=p["salario_bruto"],
            convenio=p["convenio"],
            extra15=p["extra15"],
            extra2=p["extra2"],
            feriado=p["feriado"],
            feriado2=p["feriado2"],
            comisiones=p["comisiones"],

            sem=p["sem"],
            ivm=p["ivm"],
            banco=p["banco"],
            renta=p["renta"],
            embargos=p["embargos"],

            total_devengado=p["total_devengado"],
            total_deducciones=p["total_deducciones"],
            salario_neto=p["salario_neto"]

        )

    st.success("PDFs generados correctamente en carpeta OUTPUT.")