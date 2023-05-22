from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
import re
import logging

logger = logging.getLogger(__name__)

class PasswordValidator:
    """
        Validate that the password contains at least 1 lowercase letter, 1 uppercase letter, 1 
        number, and be at least 6 characters long.
    """
   
    def validate(self, password, user=None):
        if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{6,}$", password):
            raise ValidationError(
                _("Password must contain at least one number, one uppercase letter, one lowercase letter, and at least 6 or more characters."),
                code="password_invalid"
            )
    
    def get_help_text(self):
        return _("Password must contain at least one number, one uppercase letter, one lowercase letter, and at least 6 or more characters.")