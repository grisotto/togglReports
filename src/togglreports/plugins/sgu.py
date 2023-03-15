from typing import Callable
import pandas as pd
import datetime as dt


class SGUReport():
    """
    Sgu report
    """

    _base_data: list[dict]
    _base_config: dict
    _config: dict

    _default_filename: str = 'SGU_report'
    _file_format: str = 'csv'
    _file_encoding: str = 'ansi'
    _separator: str = ';'

    _default_ignore_tag: str = '<IGNORE>'
    _max_num_chars: int = 50

    def __init__(self, data: list[dict], base_config: dict, config: dict):
        self._base_data = data
        self._base_config = base_config
        self._config = config

    def export(self) -> None:
        """ Export data to file """
        data = self._process(self._base_data)

        filename = self._base_config.get('name', self._default_filename)
        prefix = f'{dt.datetime.today().strftime("%Y%m%d")}_' if self._base_config.get('add_date', False) else ''

        pd.DataFrame.from_dict(data).to_csv(
            f'{prefix}{filename}.{self._file_format}',
            index=False,
            encoding=self._file_encoding,
            sep=self._separator
        )

    def _process(self, data: list[dict]) -> list[dict]:
        """ Process data to specific format """
        username = self._config.get('username', '')
        ignored_tag = self._config.get('ignored_tag', self._default_ignore_tag)
        default_tag = self._config.get('default_tag', '')
        processed_data = []

        for entry in data:
            # Check if entry is a valid entry
            if (len(entry['tags']) >= 1):
                if ignored_tag in entry['tags']:
                    continue
                categ = entry['tags'][0]
            else:
                categ = default_tag

            processed_data.append({
                'DATA': dt.datetime.fromisoformat(entry['start']).strftime("%d/%m/%Y"),
                'PROJETO': entry['project'],
                'CATEGORIA': categ,
                'ATIVIDADE': entry['description'][:self._max_num_chars],
                'OPORTUNIDADE': '',
                'HORAS': str(float(entry['dur']) / 3600000).replace('.', ','),
                'USERNAME': username
            })

        return processed_data


def register(register_function: Callable, name: str) -> None:
    """ Register plugin """
    register_function(name, SGUReport)
