from typing import Any, List

from django.db import models
from django.db.models import QuerySet
from rest_framework import serializers


def get_response_serializer(
    model: models.Model, fields: List[str] = [],                          exclude_fields: List[str] = []
):
    if not any([fields, exclude_fields]):
        raise ValueError("Please provide either of fields : fields or exclude fields")

    # if  all(fields and exclude_fields):
    if fields and exclude_fields:
        raise ValueError(
            "Please only provide either of fields : fields or exclude fields"
        )

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            pass

    ResponseSerializer.Meta.model = model
    if fields:
        ResponseSerializer.Meta.fields = fields
    else:
        ResponseSerializer.Meta.exclude = exclude_fields

    return ResponseSerializer


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(BaseModelSerializer, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.error_messages = get_error_messages_code(field_name)


def get_crud_serializer(model: models.Model, fields: list = [], update=True):

    if not fields:
        raise ValueError("Please provide fields to edit.")
    if not model:
        raise ValueError("Please provide model for the serializer")

    class BaseCrudSerializer(BaseModelSerializer):
        def __init__(self, *args, **kwargs):
            if update:
                pk_field = self.Meta.model._meta.pk.name
                self.fields[pk_field] = serializers.PrimaryKeyRelatedField(
                    queryset=self.Meta.model.objects.dfilter(),
                    required=True,
                )
            super(BaseCrudSerializer, self).__init__(*args, **kwargs)

            for field_name, field in self.fields.items():
                field.required = True

        class Meta:
            pass

    BaseCrudSerializer.Meta.model = model

    BaseCrudSerializer.Meta.fields = fields

    return BaseCrudSerializer


class BaseSerializerSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super(BaseSerializerSerializer, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.error_messages = get_error_messages_code(field_name)


def get_error_messages_code(field_name: str = None, extra_kwargs_fields: list = None):
    if field_name:
        return {
            "null": f"{field_name}_null",
            "required": f"{field_name}_required",
            "blank": f"{field_name}_blank",
            "invalid": f"{field_name}_invalid",
            "does_not_exist": f"{field_name}_does_not_exist",
            "incorrect_type": f"{field_name}_invalid",
            "min_value": f"{field_name}_min_value",
            "max_value": f"{field_name}_max_value",
            "max_length": f"{field_name}_max_length",
        }
    elif extra_kwargs_fields:
        return {
            field_name: {
                "error_messages": get_error_messages_code(field_name=field_name)
            }
            for field_name in extra_kwargs_fields
        }


def get_full_error_messages(field_name, field_error,error_messages_dict):
    # print("101 field_name", field_name)
    # print("101 field_error", field_error)
    _base_messages_dict = {
        f"{field_name}_null": f"{field_name} should not be null.",
        f"{field_name}_required": f"Key : {field_name} is missing.",
        f"{field_name}_blank": f"Please enter value for {field_name}.",
        f"{field_name}_invalid": f"Please enter a valid value for Field : {field_name}.",
        f"{field_name}_does_not_exist": "No record found.",
        f"{field_name}_incorrect_type": f"Please enter a valid value for Field : {field_name}.",
        f"{field_name}_min_value": "Please enter a value greater than min value.",
        f"{field_name}_max_value": f"You have exceeded the maximum value for {field_name}",
        f"{field_name}_max_length": f"You have exceeded the maximum length for {field_name}",
    }
    _base_messages_dict = _base_messages_dict | error_messages_dict
    # _base_messages_dict = _base_messages_dict | {
    #     "non_field_errors": "Please check the fields and try again."
    # }
    return _base_messages_dict[field_error]


def get_error_message(serializer_errors, error_messages_dict) -> tuple:
    if not serializer_errors:
        return None, "Validation failed.", None

    # Prefer confirm-password style errors first so users see matching problems first
    priority_keys = ["confirm_password", "confirm_new_password"]
    keys = list(serializer_errors.keys())
    error_field = None
    for pk in priority_keys:
        if pk in serializer_errors:
            error_field = pk
            break

    if not error_field:
        error_field = keys[0]

    # iterate values but we only need the first field's errors
    for field_error in serializer_errors.values():
        # field_error is typically a list of error tokens/strings
        raw = field_error[0]
        if error_field == "non_field_errors":
            friendly = error_messages_dict.get(raw, raw)
            return raw, friendly, error_field

        try:
            friendly = get_full_error_messages(
                field_name=error_field,
                field_error=raw,
                error_messages_dict=error_messages_dict,
            )
        except Exception:
            # If mapping is not available (e.g. custom validation raised a free-text message),
            # fall back to the raw error text so clients still see a helpful message.
            friendly = raw
        return raw, friendly, error_field
