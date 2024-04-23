import fitz
import csv
def convertor(ip, op):
    writer = csv.writer(open(op, 'w', newline=''))
    doc = fitz.open(ip)
    for i in doc:
        table = i.find_tables()
        if table.tables:
            writer.writerows(table[0].extract())

convertor("DCC1.pdf", "Party.csv")
convertor("DCC2.pdf", "Individual.csv")