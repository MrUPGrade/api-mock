import click

from apimock.bootstrap import run_app

LOG_LEVELS = ['CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG']


@click.command(name='apimock')
@click.option('--log-level', '-l',
              default='INFO',
              type=click.Choice(LOG_LEVELS))
@click.option('--debug', '-d',
              default=False,
              is_flag=True,
              help='Enables debugging logger')
@click.argument('mock_dir',
                default='mock',
                type=click.Path(exists=True))
def cli(**kwargs):
    run_app(kwargs)
