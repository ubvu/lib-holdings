from lib_holdings.__main__ import main
from click.testing import CliRunner
from tests import config


def test_holdings():
    runner = CliRunner()
    result = runner.invoke(main, ['--key', config.oclc_key, '--secret', config.oclc_secret, 
                                  'tests/infile_ocns.csv', 'tests/infile_symbols.csv', 'tests/out'])
    print(result.output)
    assert result.exit_code == 0


if __name__ == '__main__':
    test_holdings()
