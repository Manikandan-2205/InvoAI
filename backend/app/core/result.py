from fastapi import status

class Result:
    def __init__(self, success: bool, data=None, message: str = "", code: int = status.HTTP_200_OK):
        self.success = success
        self.data = data
        self.message = message
        self.code = code

    @classmethod
    def Ok(cls, data=None, message="Success", code=status.HTTP_200_OK):
        return cls(True, data, message, code)

    @classmethod
    def Fail(cls, message="Error", code=status.HTTP_400_BAD_REQUEST):
        return cls(False, None, message, code)
