from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", size=46)
        width = self.get_string_width("CS50 Shirtificate") + 6
        self.set_x((210 - width) / 2)
        self.cell(
            width, 60, "CS50 Shirtificate", new_x="LMARGIN", new_y="NEXT", align="C"
        )
        self.image("shirtificate.png", x=12, y=70, w=185)


def main():
    shirt(input("Name: "))


def shirt(name):
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Helvetica", style="B", size=20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_x(100)
    pdf.cell(10, 120, f"{name} took CS50", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.output("shirtificate.pdf")


if __name__ == "__main__":
    main()
