#!/usr/bin/env python
import os
import time
import json
import logging
import threading
import webbrowser

import click
import flask
import sys

from geotagger import settings
from geotagger.gpx import generate_gpx
from geotagger.exif import get_exif_metadata, exiftool_geotag
from geotagger.moves import MovesClient, MovesModel
from geotagger.utils import get_image_file_paths


log = logging.getLogger(__name__)


def load_saved_access_token():
    try:
        with open(token_file_path, 'r') as f:
            return json.load(f)['access_token']
    except Exception as e:
        log.error('Error loading saved Moves API access token: %s', e)


def get_config(path):
    try:
        with open(path, 'r') as f:
            config = json.load(f)
    except Exception:
        log.error('unable to load config file: %s', path)
        raise

    required = [
        'MOVES_ID',
        'MOVES_SECRET',
    ]
    missing = []
    for required_field in required:
        if not config.get(required_field):
            missing.append(required_field)

    if missing:
        log.error('missing configuration: %s', ', '.join(missing))

    return config


def get_image_creation_dates(image_directory):
    image_file_paths = get_image_file_paths(image_directory)
    collection = get_exif_metadata(image_file_paths)
    dates = set()
    for photo in collection:
        dates.add(photo['created'].date())
    dates = sorted(dates)
    return dates


def get_storylines_for_dates(dates):
    access_token = load_saved_access_token()
    if not access_token:
        click.echo(
            'please obtain Moves API access token first: {} auth'
            .format(os.path.basename(sys.argv[0])),
            err=True
        )
        click.get_current_context().exit(1)
    moves_client.access_token = access_token
    moves = MovesModel(moves_client)
    storylines = [moves.get_storyline(date) for date in dates]
    return storylines


def get_gpx_for_dates(dates):
    storylines = get_storylines_for_dates(dates)
    gpx = generate_gpx(storylines)
    return gpx


def get_gpx_for_photo_directory(image_directory):
    dates = get_image_creation_dates(image_directory)
    gpx_data = get_gpx_for_dates(dates)
    return gpx_data


moves_client = None
token_file_path = None


@click.group()
@click.option(
    '--config',
    default=settings.DEFAULT_CONFIG_PATH,
    type=click.Path(dir_okay=False),
    help='Custom config file path (default: {})'
         .format(settings.DEFAULT_CONFIG_PATH),
)
@click.option(
    '--token-file',
    default=settings.DEFAULT_MOVES_TOKEN_PATH,
    help='Use this Moves token file location (default: {}).'
         .format(settings.DEFAULT_MOVES_TOKEN_PATH),
    type=click.Path(dir_okay=False),
)
@click.pass_context
def cli(context, config, token_file):
    """
    Geotagger geotags images based on your Moves app history.

    https://github.com/jakubroztocil/geotagger

    """
    config = get_config(config)
    global moves_client
    global token_file_path
    moves_client = MovesClient(
        client_id=config['MOVES_ID'],
        client_secret=config['MOVES_SECRET'],
    )
    token_file_path = token_file


@cli.command()
@click.argument('image_directory', type=click.Path(
    exists=True, dir_okay=True, file_okay=False))
def gpx(image_directory):
    """
    Generate GPX data for all images in a directory.

    """
    gpx_data = get_gpx_for_photo_directory(image_directory)
    click.echo(gpx_data)


@cli.command()
@click.argument('image_directory', type=click.Path(
    exists=True, dir_okay=True, file_okay=False))
@click.argument('gpx_file', required=False, type=click.Path(
    exists=True, dir_okay=False, file_okay=True))
@click.pass_context
def tag(context, image_directory, gpx_file=None):
    """
    Geotag images in a directory. If you omit the XPX_FILE,
    GeoTagger will fetch location data from Moves and generate
    the log file first.

    """
    if not gpx_file:
        gpx_file = '/tmp/moves.gpx'
        gpx_data = get_gpx_for_photo_directory(image_directory)
        with open(gpx_file, 'w') as f:
            f.write(gpx_data)
    exiftool_geotag(gpx_file, image_directory)


@cli.command()
def auth():
    """
    Authorize geotagger to access your Moves data.

    """

    def serve():
        app = flask.Flask(__name__)

        @app.route('/')
        def authorize():
            log.info('redirecting to Moves for authorization')
            return flask.redirect(moves_client.build_authorize_url())

        @app.route('/redirect')
        def redirect():
            log.info('back from Moves')
            if 'error' in flask.request.args:
                return flask.redirect('/')
            code = flask.request.args.get('code')
            log.info('code is %s', code)
            token_data = moves_client.get_token(code)
            with open(token_file_path, 'w') as f:
                json.dump(token_data, f)
            message = 'Success! You can now kill the process with ^C'
            log.info(message)
            return message

        app.run(port=settings.WEBAPP_PORT)

    server_thread = threading.Thread(target=serve)
    server_thread.start()
    time.sleep(1)
    webbrowser.open_new_tab(settings.WEBAPP_ROOT_URL)
