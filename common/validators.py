from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


#  value is the field's value
def validate_only_letters(value):
    if not value.isalpha():
        raise ValidationError('Value must contain only letters')


# validator with arguments -> ???
# can't give max size in the model - DON'T USE!
def validate_file_max_size_in_mb(max_size):
    def validate(value):
        filesize = value.file.size
        if filesize > max_size * 1024 * 1024:
            raise ValidationError(f'Image file size exceeded {max_size} MB.')

    return validate


# !!!! such class validators can be used in the MODELS !!!!!!!!!
@deconstructible
#  Class decorator that allow the decorated class to be serialized
#     by the migrations subsystem.
class ValidateFileMaxSizeInMb:
    def __init__(self, max_size):
        self.max_size = max_size
        self.max_size_bytes = max_size * 1024 * 1024

    def __call__(self, value):
        if value.file.size > self.max_size_bytes:
            raise ValidationError(f'Image file size exceeded {self.max_size} MB.')


"""
@deconstructible
class ValidateFileMaxSizeInMb:
    def __init__(self, max_size):
        self.max_size = max_size

    #    self.max_size_bytes = max_size * 1024 * 1024

    def __call__(self, value):  # call instance of method as function
        filesize = value.file.size
        if filesize > self.__megabytes_to_bytes():
            raise ValidationError(self.__get_exception_message())

    def __megabytes_to_bytes(self):
        return self.max_size * (2 ** 16)

    def __get_exception_message(self):
        return f"Max file size is {self.max_size:.02f} MB."

"""
"""
def deconstructible(*args, **kwargs):

    Class decorator that allow the decorated class
    to be serialized
    by the migrations subsystem.

    Accepts an optional kwarg `path` to specify the import path.

"""