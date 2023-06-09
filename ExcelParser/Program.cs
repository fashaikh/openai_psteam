using System;
using System.IO;
using OfficeOpenXml;
using iTextSharp.text;
using iTextSharp.text.pdf;
using static System.Runtime.InteropServices.JavaScript.JSType;
using System.Drawing;

class Program
{
    static void Main()
    {
        string excelFilePath = @"C:\chatgpt\ExcelParser\datatest.xlsx";
        string outputDirectory = @"C:\chatgpt\ExcelParser\PDFs\Testdata\";

        ExcelPackage.LicenseContext = LicenseContext.NonCommercial;

        // Load the Excel file using EPPlus
        using (var package = new ExcelPackage(new FileInfo(excelFilePath)))
        {
            ExcelWorksheet worksheet = package.Workbook.Worksheets[0]; // Assuming the data is on the first worksheet

            int rowCount = worksheet.Dimension.Rows;
            int colCount = worksheet.Dimension.Columns;

            // Iterate through each row in the Excel sheet
            for (int row = 2; row <= rowCount; row++)
            {
                // Create a new PDF document for each row
                Document document = new Document();

                // Create a unique file name for the PDF document
                string pdfFileName = Path.Combine(outputDirectory, $"Incident-{worksheet.Cells[row, 2].Value?.ToString()}.pdf");

                // Create a new PDF writer
                PdfWriter writer = PdfWriter.GetInstance(document, new FileStream(pdfFileName, FileMode.Create));

                document.Open();

                // Iterate through each column in the current row
                for (int col = 1; col <= colCount; col++)
                {
                    string columnName = "\n" + worksheet.Cells[1, col].Value?.ToString() ?? string.Empty;
                    string cellValue = worksheet.Cells[row, col].Value?.ToString() ?? string.Empty;

                    // Creating Paragraph
                    Paragraph paragraph1 = new Paragraph();


                    iTextSharp.text.Chunk chunk1 = new iTextSharp.text.Chunk(columnName + " :\n\n", FontFactory.GetFont(FontFactory.HELVETICA, 16, iTextSharp.text.Font.UNDERLINE, iTextSharp.text.BaseColor.GRAY));
                    paragraph1.Add(chunk1);
                    iTextSharp.text.Chunk chunk2 = new iTextSharp.text.Chunk(cellValue, FontFactory.GetFont(FontFactory.HELVETICA, 10, iTextSharp.text.BaseColor.BLACK));
                    paragraph1.Add(chunk2);


                    document.Add(paragraph1);
                }

                document.Close();
            }
        }
    }
}
