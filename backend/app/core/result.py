class Result:
    def __init__(self, success: bool, message: str = "", data=None, code: int = 200):
        self.success = success
        self.message = message
        self.data = data
        self.code = code

    @staticmethod
    def Ok(data=None, message="Success", code=200):
        return Result(True, message, data, code)

    @staticmethod
    def Fail(message="Error", code=400, data=None):
        return Result(False, message, data, code)
