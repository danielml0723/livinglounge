from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Spacer,
    Paragraph,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

styles = getSampleStyleSheet()

def currency(v):
    return f"₡ {v:,.2f}"


def generate_payroll_pdf(

        empleado,
        fecha_pago,
        salario_mensual,
        salario_hora,
        salario_bruto,
        convenio,
        extra15,
        extra2,
        feriado,
        feriado2,
        comisiones,
        sem,
        ivm,
        banco,
        renta,
        embargos,
        total_devengado,
        total_deducciones,
        salario_neto

):

    BASE_DIR = Path(__file__).resolve().parent.parent

    output_dir = BASE_DIR / "output"
    output_dir.mkdir(exist_ok=True)

    logo_path = BASE_DIR / "assets" / "logo.png"

    filename = f"{fecha_pago}_{empleado['nombre'].replace(' ','_')}.pdf"

    filepath = output_dir / filename

    doc = SimpleDocTemplate(

        str(filepath),

        pagesize=A4,

        leftMargin=18,
        rightMargin=18,
        topMargin=18,
        bottomMargin=18

    )

    elements = []

    # COLORS

    NEGRO = colors.HexColor("#111111")
    ROJO = colors.HexColor("#D5001C")
    LIGHT = colors.HexColor("#F6F7F9")
    BORDER = colors.HexColor("#E6E6E6")
    TEXT = colors.HexColor("#333333")

    # ---------- LOGO ----------

    if logo_path.exists():

        logo = Image(
            str(logo_path),
            width=2.6*cm,
            height=2.6*cm
        )

    else:

        logo = ""

    # ---------- HEADER ----------

    header = Table([

        [

            logo,

            Paragraph(

                """
                <font color="white" size="15">

                <b>LIVING LOUNGE S.A.</b>

                </font>

                <br/>

                <font color="#DDDDDD" size="9">

                Cédula Jurídica: 3-101-663107<br/>
                Teléfono: 2290-8788<br/>
                Sabana Oeste, frente a Cemaco

                </font>
                """,

                styles["Normal"]

            ),

            Paragraph(

                f"""

                <para align=center>

                <font color="white" size="12">

                <b>COMPROBANTE DE PAGO</b>

                </font>

                <br/><br/>

                <font color="#DDDDDD" size="10">

                Fecha Pago<br/>

                <b>{fecha_pago}</b>

                </font>

                </para>

                """,

                styles["Normal"]

            )

        ]

    ],

    colWidths=[80,280,140])

    header.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,-1),NEGRO),

        ('BOX',(0,0),(-1,-1),1,ROJO),

        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),

        ('LEFTPADDING',(0,0),(-1,-1),15),

        ('RIGHTPADDING',(0,0),(-1,-1),15),

        ('TOPPADDING',(0,0),(-1,-1),18),

        ('BOTTOMPADDING',(0,0),(-1,-1),18)

    ]))

    elements.append(header)

    elements.append(Spacer(1,16))

    # ---------- EMPLEADO ----------

    empleado_table = Table([

        [

            Paragraph(
                f"<b>Trabajador</b><br/>{empleado['nombre']}",
                styles["BodyText"]
            ),

            Paragraph(
                f"<b>Puesto</b><br/>{empleado['puesto']}",
                styles["BodyText"]
            )

        ]

    ],

    colWidths=[250,250])

    empleado_table.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,-1),LIGHT),

        ('BOX',(0,0),(-1,-1),0.5,BORDER),

        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),

        ('LEFTPADDING',(0,0),(-1,-1),12),

        ('RIGHTPADDING',(0,0),(-1,-1),12),

        ('TOPPADDING',(0,0),(-1,-1),12),

        ('BOTTOMPADDING',(0,0),(-1,-1),12)

    ]))

    elements.append(empleado_table)

    elements.append(Spacer(1,15))

    # ---------- KPI CARDS ----------

    kpi = Table([

        [

            "SALARIO MENSUAL",
            "COSTO HORA"

        ],

        [

            currency(salario_mensual),
            currency(salario_hora)

        ]

    ],

    colWidths=[255,255])

    kpi.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,0),ROJO),

        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('BACKGROUND',(0,1),(-1,1),LIGHT),

        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),

        ('FONTNAME',(0,1),(-1,1),'Helvetica-Bold'),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),

        ('BOX',(0,0),(-1,-1),0.5,BORDER),

        ('TOPPADDING',(0,0),(-1,-1),10),

        ('BOTTOMPADDING',(0,0),(-1,-1),10)

    ]))

    elements.append(kpi)

    elements.append(Spacer(1,20))

    # ---------- DETALLE ----------

    detalle = [

        ["Código","Descripción","Asignación","Deducción"],

        ["1001","Salario Bruto",currency(salario_bruto),""] ,
        ["1002","Convenio 12 Horas",currency(convenio),""] ,
        ["1003","Horas Extra x1.5",currency(extra15),""] ,
        ["1004","Horas Extra x2",currency(extra2),""] ,
        ["1005","Feriado Obligatorio",currency(feriado),""] ,
        ["1006","Horas x2 Feriado",currency(feriado2),""] ,
        ["1007","Comisiones",currency(comisiones),""] ,

        ["1008","CCSS SEM","","5.5% "+currency(sem)],
        ["1009","CCSS IVM","","4.33% "+currency(ivm)],
        ["1010","Banco Popular","","1% "+currency(banco)],
        ["1011","Renta","",currency(renta)],
        ["1012","Embargos","",currency(embargos)]

    ]

    detalle_table = Table(

        detalle,

        colWidths=[60,240,105,105]

    )

    detalle_table.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,0),NEGRO),

        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),

        ('LINEBELOW',(0,0),(-1,0),2,ROJO),

        ('ROWBACKGROUNDS',

            (0,1),
            (-1,-1),

            [

                colors.white,
                LIGHT

            ]

        ),

        ('BOX',(0,0),(-1,-1),0.5,BORDER),

        ('INNERGRID',(0,1),(-1,-1),0.20,BORDER),

        ('ALIGN',(2,1),(-1,-1),'RIGHT'),

        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),

        ('TEXTCOLOR',(0,1),(-1,-1),TEXT),

        ('TOPPADDING',(0,0),(-1,-1),9),

        ('BOTTOMPADDING',(0,0),(-1,-1),9)

    ]))

    elements.append(detalle_table)

    elements.append(Spacer(1,22))

    # ---------- TOTALS ----------

    total_table = Table([

        ["TOTAL DEVENGADO",currency(total_devengado)],

        ["TOTAL DEDUCCIONES",currency(total_deducciones)],

        ["NETO A PAGAR",currency(salario_neto)]

    ],

    colWidths=[320,190])

    total_table.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,1),LIGHT),

        ('BACKGROUND',(0,2),(-1,2),ROJO),

        ('TEXTCOLOR',(0,2),(-1,2),colors.white),

        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),

        ('FONTSIZE',(0,2),(-1,2),14),

        ('BOX',(0,0),(-1,-1),0.5,BORDER),

        ('INNERGRID',(0,0),(-1,-1),0.25,BORDER),

        ('TOPPADDING',(0,0),(-1,-1),12),

        ('BOTTOMPADDING',(0,0),(-1,-1),12)

    ]))

    elements.append(total_table)

    elements.append(Spacer(1,25))

    # ---------- FOOTER ----------

    footer = Paragraph(

        """

        <para align=center>

        <font color="#777777" size="8">

        Documento generado automáticamente por
        Sistema RRHH Nómina — Living Lounge S.A.

        </font>

        </para>

        """,

        styles["Normal"]

    )

    elements.append(footer)

    doc.build(elements)

    return filepath