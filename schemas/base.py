from pydantic import model_validator

class AtLeastOneFieldRequiredMixin:
    @model_validator(mode="after")
    def _check_at_least_one_field(self):
        if not any(
            getattr(self, field) not in (None, "")
            for field in self.model_fields
        ):
            raise ValueError("At least one field must be provided")
        return self