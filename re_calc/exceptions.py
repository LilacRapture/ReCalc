class CalcException(Exception):
    """
    Attributes:
        token_position -- position of the token caused the error
        tokens_list
        loc_string -- localization string
        message -- explanation
    """

    def __init__(self, token_position, tokens_list, message, loc_string=None):
        self.token_position = token_position
        self.tokens_list = tokens_list
        self.loc_string = loc_string
        self.message = message
        super().__init__(self.message)


class MathException(Exception):
    """
    Attribute:
        message -- explanation
        loc_string -- localization string

    """

    def __init__(self, message, loc_string=None):
        self.loc_string = loc_string
        self.message = message
        super().__init__(self.message)


def process_float_token(token):
    if isinstance(token, float):
        return "{0:g}".format(token)
    else:
        return token


def get_error_location(token_position, tokens_list):
    string_token_list = [process_float_token(token) for token in tokens_list]
    expression_line = ' '.join(string_token_list)

    processed_tokens = string_token_list[:token_position]
    token_lengths = list(map(lambda token: len(token) + 1, processed_tokens))
    padds_count = sum(token_lengths)
    padds_line = ' ' * padds_count + '^'
    return expression_line + '\n' + padds_line


def catch_calc_errors(f):
    try:
        return {'result': process_float_token(f()),
                'status': 'success'}
    except CalcException as e:
        if hasattr(e, 'message') and hasattr(e, 'token_position') and hasattr(e, 'tokens_list'):
            return {'message': e.message,
                    'token_position': e.token_position,
                    'tokens_list': e.tokens_list,
                    'error_location': get_error_location(e.token_position, e.tokens_list),
                    'loc_string': e.loc_string,
                    'status': 'error'}

    except (MathException, Exception) as e:
        if hasattr(e, 'message'):
            return {'message': e.message,
                    'loc_string': e.loc_string,
                    'status': 'error'}
