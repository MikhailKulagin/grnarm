from httpx import Response


class HTTPError(Exception):
    """Общее исключение при любых ошибках http"""
    pass


class HTTPStatusError(HTTPError):
    """HTTP status code в диапазоне ошибок 4XX - 5XX"""

    def __init__(self, response: Response) -> None:
        self.status_code = response.status_code
        self.text = response.text
        message = f'{self.text} {self.status_code}'
        super().__init__(message)


class HTTPContentError(HTTPError):
    """Ошибка типа данных в ответе"""
    pass
