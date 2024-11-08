import os
import click
import time
import logging
from subprocess import run
from dataclasses import dataclass


S3_ENDPOINT = "http://localhost:9000"
LOG_MODE = "INFO"

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format":
                '%(asctime)s [%(levelname)s]: [%(processName)s] %(message)s'
            },
        },
        "loggers": {
            "app": {"level": LOG_MODE, "handlers": ["file", "console"]}
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "service.log",
                "formatter": "standard",
                "maxBytes": 1024 ** 2,
                "backupCount": 2,
                "level": LOG_MODE,
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": LOG_MODE
            }
        },
    }
)
log = logging.getLogger(__name__)
log.setLevel(LOG_MODE)


@dataclass
class S3Data():
    """S3 data."""
    s3_location: str
    local_data_location: str
    s3_endpoint: str = S3_ENDPOINT


def get_location(text):
    splited = text.split(',')
    for x in splited:
        if x.startswith("Key"):
            return x.split(":")[1]
        

def get_basename(location):
    return os.path.basename(location)


def get_s3_dir(s3_location):
    return "/".join(s3_location.split("/")[:-1]) + "/"
        

def download_s3_data(s3_data):
    start_time = time.time()
    cmd = (
        f'aws --endpoint-url "{s3_data.s3_endpoint}"'
        f' s3 cp "s3://{s3_data.s3_location}" "{s3_data.local_data_location}"'
    )
    run(cmd, shell=True)
    duration = time.time() - start_time
    log.info("Data %s downloaded in %g s", s3_data.s3_location, duration)


def download_data(location):
    log.info(f"Downloading from {location}")
    data_path = f"./data/{get_s3_dir(location)}"
    if not os.path.exists(data_path):
        os.makedirs(data_path, exist_ok=True)
    s3_data_in = S3Data(
        s3_location=location,
        local_data_location=f"{data_path}{get_basename(location)}"
    )
    download_s3_data(s3_data_in)
    return data_path


def handle_message(message):
    location = get_location(message)
    data_path = download_data(location)
    log.info(f"Data downloaded to {data_path}")


@click.command()
@click.option('--message', default='{EventName:s3:ObjectCreated:Put,Key:bucket/dir1/subdir1/file.extension,',
              help='The message to handle.')
def main(message):
    handle_message(message)


if __name__ == "__main__":
    main()
