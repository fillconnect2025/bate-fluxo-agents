from tools.parse_file import ParseFileTool

tool = ParseFileTool()
resultado = tool._run("data/EXTRATO LOJA - JANEIRO.pdf")

print("\n=== TEXTO EXTRAÍDO COM OCR ===\n")
print(resultado["text"][:2000])  # mostra primeiros 2000 caracteres
