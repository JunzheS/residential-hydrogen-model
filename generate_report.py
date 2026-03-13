from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from hydrogen_model import run_model


def generate_report():

    results = run_model(
        PV_capacity=5,
        electricity_demand=3500,
        heating_demand=10000,
        electricity_price=0.25,
        gas_price=0.10,
        electrolyser_efficiency=52
    )

    file_name = "hydrogen_analysis_report.pdf"

    c = canvas.Canvas(file_name, pagesize=letter)

    y = 750

    c.setFont("Helvetica",12)

    c.drawString(50,y,"Residential Hydrogen System Analysis")
    y -= 40

    for k,v in results.items():

        line = f"{k} : {round(v,2)}"

        c.drawString(50,y,line)

        y -= 25

    c.save()

    print("Report generated:",file_name)


if __name__ == "__main__":

    generate_report()
