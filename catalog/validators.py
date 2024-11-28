from django.core.exceptions import ValidationError
 
def valid_extension(value):
    if (not value.name.endswith('.pdf') and
        not value.name.endswith('.docx') and 
        not value.name.endswith('.doc')):
        raise ValidationError("Archivos permitidos: .pdf, .doc, .docx")
    
    