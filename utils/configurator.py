import json as _json
from os import PathLike
from typing import Any as _Any
from typing import Dict as _Dict
from typing import Optional, TypeAlias


class InvalidDataException(Exception):
    pass


class Config(object):
    _ConfigDataType: TypeAlias = _Dict[str, _Any]
    _default_cfg_data: _ConfigDataType = {
        "BOT_TOKEN": "",
        "ADMINS": [],
        "ADMINS_CHAT": None,
        "ALLOWED_GROUPS": [],
    }
    _default_cfg_data_types = {
        "BOT_TOKEN": str,
        "ADMINS": list,
        "ADMINS_CHAT": Optional[int],
        "ALLOWED_GROUPS": list,
    }

    def __init__(self, file_path: PathLike) -> None:
        self._file = file_path
        self.data: _Dict[str, _Any] = self._get_data()
        self._verify_data()

    def _verify_data(self) -> None:
        if not isinstance(self.data, _Dict):
            raise InvalidDataException('Invalid config data type')
        for key in Config._default_cfg_data.keys():
            if key not in self.data:
                raise InvalidDataException(f'No {key} in config data')
            elif not isinstance(
                self.data[key], Config._default_cfg_data_types[key]
            ):
                raise InvalidDataException(
                    f'{key} value type is not {Config._default_cfg_data_types[key]}'
                )

    def _get_data(self) -> _Dict[str, _Any]:
        with open(self._file, mode='r') as cfg_file:
            return _json.loads(cfg_file.read())

    @property
    def bot_token(self) -> str:
        return self.data['BOT_TOKEN']

    @bot_token.setter
    def bot_token(self, token: str) -> None:
        self.data['BOT_TOKEN'] = token

    @property
    def admins(self) -> list[int]:
        return self.data['ADMINS']

    @property
    def admins_chat(self) -> Optional[int]:
        return self.data['ADMINS_CHAT']

    @admins_chat.setter
    def admins_chat(self, chat_id: int) -> None:
        self.data['ADMINS_CHAT'] = chat_id

    @property
    def allowed_groups(self) -> list[int]:
        return self.data['ALLOWED_GROUPS']

    def update_data(self) -> None:
        self.data = self._get_data()

    def save(self) -> None:
        with open(self._file, mode='w') as cfg_file:
            data = _json.dumps(self.data, indent=4)
            cfg_file.write(data)


def set_default_config(file_path: PathLike) -> None:
    """Сбрасывает конфигурацию"""
    with open(file_path, mode='w') as cfg_file:
        data = _json.dumps(Config._default_cfg_data)
        cfg_file.write(data)
