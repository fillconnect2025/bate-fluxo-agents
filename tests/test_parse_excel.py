# test_parse_excel.py
from tools.parse_file import ParseFileTool

tool = ParseFileTool()
result = tool._run("data/Historico de Vendas - LOJA - SEMESTRAL.xlsx")
print(result)