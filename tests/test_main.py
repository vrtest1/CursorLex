import sys
from types import SimpleNamespace
from unittest.mock import Mock, patch
import importlib.util
from pathlib import Path

# dummy modules for dependencies not available in the test environment
sys.modules['pyperclip'] = SimpleNamespace(paste=lambda: '')
sys.modules['requests'] = SimpleNamespace(get=Mock())

# load main.py explicitly so we can import without installing deps
spec = importlib.util.spec_from_file_location('main', Path(__file__).resolve().parents[1] / 'main.py')
main = importlib.util.module_from_spec(spec)
sys.modules['main'] = main
spec.loader.exec_module(main)


def test_get_word_meaning_uses_params_and_returns_data():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': [{
            'senses': [
                {
                    'english_definitions': ['sample definition'],
                    'parts_of_speech': ['noun']
                }
            ],
            'japanese': [{
                'reading': 'サンプル'
            }]
        }]
    }
    with patch('main.requests.get', return_value=mock_response) as mock_get:
        result = main.get_word_meaning('sample word')
        mock_get.assert_called_once_with(
            'https://jisho.org/api/v1/search/words',
            params={'keyword': 'sample word'},
            timeout=5
        )
        assert result['english'] == 'sample definition'
        assert result['reading'] == 'サンプル'
