import requests

api_url = 'https://slack.com/api/chat.postMessage'

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

    message_dic = {
        'token': token,
        'channel': '#cli_notify',
        'text': message}

    requests.post(api_url, data=message_dic)
