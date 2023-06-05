from django.contrib.postgres.utils import prefix_validation_error
from django.core import exceptions, checks
from django.db import models
from django.db.models import JSONField


class CustomArrayField(JSONField):

    def __init__(
        self,
        **kwargs,
    ):
        # self.name = name
        self.base_field = models.TextField(max_length=100, null=False, blank=False, name='value')
        super().__init__(**kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)

        base_checks = self.base_field.check()
        if base_checks:
            error_messages = "\n    ".join("%s (%s)" % (base_check.msg, base_check.id) for base_check in base_checks
                                           if isinstance(base_check, checks.Error))
            if error_messages:
                errors.append(checks.Error("Base field for array has errors:\n    %s" % error_messages, obj=self))
            warning_messages = "\n    ".join("%s (%s)" % (base_check.msg, base_check.id) for base_check in base_checks
                                             if isinstance(base_check, checks.Warning))
            if warning_messages:
                errors.append(checks.Warning("Base field for array has warnings:\n    %s" % warning_messages, obj=self))

        return errors

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if type(value) != list:
            raise exceptions.ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )

        for index, part in enumerate(value):
            try:
                self.base_field.validate(part, model_instance)
            except exceptions.ValidationError as error:
                raise prefix_validation_error(
                    error,
                    prefix=self.error_messages["item_invalid"],
                    code="item_invalid",
                    params={"nth": index + 1},
                )
