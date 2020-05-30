from rest_framework.serializers import ValidationError


REQUIRED_FIELDS = {
    "label": str,
    "required": bool,
    "type": str,
}

def validate_values(values, question_idx):
    if not isinstance(values, list):
        raise ValidationError(F'The field "values" in question {question_idx} must be a list.')
    
    selected = 0
    for value_idx, value in enumerate(values):
        if "label" not in value:
            raise ValidationError(F'The field "label" is missing from question {question_idx}, option {value_idx}.')
        elif not isinstance(value['label'], str):
            raise ValidationError(F'The type of the field "label" in question {question_idx}, option {value_idx} should be str.')
        if "value" not in value:
            raise ValidationError(F'The field "value" is missing from question {question_idx}, option {value_idx}.')
        elif not isinstance(value['label'], str):
            raise ValidationError(F'The type of the field "value" in question {question_idx}, option {value_idx} should be str.')

        if 'selected' in value and value['selected'] == True:
            selected += 1
    return selected

def validate_checkbox_group(question: dict, idx: int):
    if "values" not in question:
        raise ValidationError(F'The field "values" is missing in question {idx}.')
    validate_values(question['values'], idx)

def validate_select(question: dict, idx: int):
    if "values" not in question:
        raise ValidationError(F'The field "values" is missing in question {idx}.')
    selected = validate_values(question['values'], idx)
    if selected > 1:
        raise ValidationError(F'More than one option in question {idx} cannot be selected.')

def validate_radio_group(question: dict, idx: int):
    if 'values' not in question:
        raise ValidationError(F'The field "values" is missing in question {idx}.')
    selected = validate_values(question['values'], idx)
    if selected > 1:
        raise ValidationError(F'More than one option in question {idx} cannot be selected.')

def validate_text(question: dict, idx: int):
    pass

def validate_number(question: dict, idx: int):
    pass

def validate_question(question: dict, idx: int):
    for f_name, f_type in REQUIRED_FIELDS.items():
        if f_name not in question:
            raise ValidationError(F'The field "{f_name}" is missing in question {idx}.')
        if not isinstance(question[f_name], f_type):
            raise ValidationError(F'The type of the field "{f_name}" in question {idx} should be {f_type.__name__}.')
        if question['type'] not in VALIDATION_FUNCS:
            raise ValidationError(F'The question type "{question["type"]}" in question {idx} is not a valid type.')

        VALIDATION_FUNCS[question['type']](question, idx)

def validate_form(form: list):
    if not isinstance(form, list):
        raise ValidationError('This field must be an array.')
    
    for i, question in enumerate(form):
        validate_question(question, i)


# Have to place this at the bottom of the module as these functions do not exist until this point
VALIDATION_FUNCS = {
    "checkbox-group": validate_checkbox_group,
    "number": validate_number,
    "radio-group": validate_radio_group,
    "select": validate_select,
    "text": validate_text,
}
