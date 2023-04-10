import requests

api_url = 'https://notify-api.line.me/api/notify'

def line_notify(message: str, token_path: str):
    """messageをlineに送る

    Args:
        message (str): 送りたいメッセージ
        token_path (str): tokenが書かれたファイルのパス

    Example:
        from line_notify import line_notify
        try:
            hogehoge
            line_notify(f'\n{CFG.exp}: ok')
        except Exception as e:
            line_notify(f'\n{CFG.exp}: fail\n{type(e)}: {e}')
            raise e
    """
    with open(token_path, 'r') as f:
        token = f.readline().rstrip('\n')

    token_dic = {'Authorization': 'Bearer' + ' ' + token}
    message_dic = {'message': message}

    requests.post(api_url, headers=token_dic, data=message_dic)
