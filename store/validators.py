from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_kb = 300
    if file.size > max_size_kb * 1024:
        raise ValidationError(f'The File size can not be greater then {max_size_kb} KB')
