from rest_framework.serializers import ValidationError


REQUIRED_FIELDS = {
    "label": str,
    "type": str,
}

def validate_question_options(labels, question_idx):
    if not isinstance(labels, list):
        raise ValidationError(F'The field "questionOptions" in question {question_idx} must be a list.')
    
    selected = 0
    for label_idx, label in enumerate(labels):
        if "label" not in label:
            raise ValidationError(F'The field "label" is missing from question {question_idx}, option {label_idx}.')
        elif not isinstance(label['label'], str):
            raise ValidationError(F'The type of the field "label" in question {question_idx}, option {label_idx} should be str.')
        if "label" not in label:
            raise ValidationError(F'The field "label" is missing from question {question_idx}, option {label_idx}.')
        elif not isinstance(label['label'], str):
            raise ValidationError(F'The type of the field "label" in question {question_idx}, option {label_idx} should be str.')

        if 'selected' in label and label['selected'] == True:
            selected += 1
    return selected

def validate_checkboxes(question: dict, idx: int):
    if "questionOptions" not in question:
        raise ValidationError(F'The field "questionOptions" is missing in question {idx}.')
    validate_question_options(question['questionOptions'], idx)

def validate_dropdown(question: dict, idx: int):
    if "questionOptions" not in question:
        raise ValidationError(F'The field "questionOptions" is missing in question {idx}.')
    selected = validate_question_options(question['questionOptions'], idx)
    if selected > 1:
        raise ValidationError(F'More than one option in question {idx} cannot be selected.')

def validate_multiple_choice(question: dict, idx: int):
    if 'questionOptions' not in question:
        raise ValidationError(F'The field "questionOptions" is missing in question {idx}.')
    selected = validate_question_options(question['questionOptions'], idx)
    if selected > 1:
        raise ValidationError(F'More than one option in question {idx} cannot be selected.')

def validate_auto_complete(question: dict, idx: int):
    if 'questionOptions' not in question:
        raise ValidationError(F'The field "questionOptions" is missing in question {idx}.')
    selected = validate_question_options(question['questionOptions'], idx)
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
    "Checkboxes": validate_checkboxes,
    "Dropdown": validate_dropdown,
    "Multiple Choice": validate_multiple_choice,
    "Auto Complete": validate_auto_complete,
    "Short Text": validate_text,
    "Long Text": validate_text,
    "number": validate_number,
}
