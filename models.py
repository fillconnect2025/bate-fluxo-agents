# models.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date

class Transacao(BaseModel):
    data: date
    valor: float
    descricao: str
    id_transacao: str

class ArquivoUpload(BaseModel):
    caminho: str
    formato: str  # csv, ofx, pdf
    tamanho_bytes: int

class DadosBrutos(BaseModel):
    transacoes: List[Transacao]

class DadosNormalizados(BaseModel):
    transacoes: List[Transacao]

class ConciliacaoResultado(BaseModel):
    conciliated: List[Dict[str, Any]]
    pendencias: List[str]

class Divergencia(BaseModel):
    tipo: str
    descricao: str
    gravidade: str  # alta, média, baixa

class Recomendacao(BaseModel):
    descricao: str
    acao_sugerida: str







class Transaction(BaseModel):
    date: str
    amount: float
    description: str

class ValidationResult(BaseModel):
    filename: str
    file_type: str
    status: str
    error_message: str = ""

class ExtractionResult(BaseModel):
    raw_text: str
    file_type: str
    extraction_status: str

class NormalizationResult(BaseModel):
    normalized_data: List[Dict[str, Any]]
    normalization_rules: List[str]
    errors: List[str] = []


