from pylatex import Document, Section, Subsection, Tabular, Figure

class ReportGenerator:
    """Generates a detailed report using PyLaTeX."""
    
    def __init__(self, project_name, results):
        self.project_name = project_name
        self.results = results
    
    def generate_report(self, filename="report.pdf"):
        """Create a PDF report with tables and figures."""
        doc = Document()
        doc.preamble.append(r"\title{" + self.project_name + " Life Cycle Cost Report}")
        doc.append(r"\maketitle")

        with doc.create(Section("LCC Summary")):
            with doc.create(Tabular('|c|c|')) as table:
                table.add_hline()
                table.add_row(["Component", "Cost (in USD)"])
                table.add_hline()
                for key, value in self.results.items():
                    table.add_row([key, f"${value:,.2f}"])
                table.add_hline()
        
        doc.generate_pdf(filename, clean_tex=True)
