import os
import string

import termcolor


def get_template_dir_path():
    """テンプレートファイルのディレクトリを返します

    Returns:
        str: テンプレートファイルのディレクトリを返します
    """
    template_dir_path = None
    try:
        import settings
        if settings.TEMPLATE_PATH:
            template_dir_path = settings.TEMPLATE_PATH
    except ImportError:
        pass

    if not template_dir_path:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_dir_path = os.path.join(base_dir, 'templates')

    return template_dir_path


class NoTemplateError(Exception):
    """テンプレートが存在しないエラー"""


def find_template(temp_file):
    """テンプレートファイルのパスを作成

    Args:
        temp_file (str): テンプレートファイルのファイル名

    Returns:
        temp_file_path: テンプレートファイルのパス

    Raises:
        NoTemplateError: temp_fileが存在しない場合のエラー
    """
    template_dir_path = get_template_dir_path()
    temp_file_path = os.path.join(template_dir_path, temp_file)
    if not os.path.exists(temp_file_path):
        raise NoTemplateError('Could not find {}'.format(temp_file))
    return temp_file_path


def get_template(temp_file_path, color=None):
    """テンプレートファイルを返します

    Args:
        temp_file_path (str): テンプレートファイルのパス
        color ([type], optional): ターミナルで出力する色を制御します
            詳しい情報はこちらをご覧ください.
                https://pypi.python.org/pypi/termcolor

    Returns:
        string.Template: テンプレートの文字列を返します.
    """
    template = find_template(temp_file_path)
    with open(template, 'r', encoding='utf-8') as template_file:
        contents = template_file.read()
        contents = contents.rstrip(os.linesep)
        contents = '{splitter}{sep}{contents}{sep}{splitter}{sep}'.format(
            contents=contents, splitter='=' * 60, sep=os.linesep
        )
        contents = termcolor.colored(contents, color)
        return string.Template(contents)
