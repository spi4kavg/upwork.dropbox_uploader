import logging
import os
import os.path
from typing import Optional

import dropbox
from dotenv import dotenv_values
from tqdm import tqdm

logger = logging.getLogger(__name__)

config = dotenv_values("app.env")


def upload_file(dbx: dropbox.Dropbox, file: str) -> Optional[str]:
    # read file
    dropbox_filepath = f"/{file}"
    with open(os.path.join(config['IMAGES_FOLDER'], file), 'rb') as f:
        content = f.read()

    # upload file
    try:
        dbx.files_upload(content, dropbox_filepath)
    except Exception:
        return

    # get shared link of file
    try:
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_filepath)
    except dropbox.exceptions.ApiError as e:
        if e.error.is_shared_link_already_exists():
            shared_link_metadata = dbx.sharing_list_shared_links(dropbox_filepath)
            return shared_link_metadata.links[0].url
        return
    return shared_link_metadata.url


def replace_shared_link_to_download_link(link: str) -> str:
    return link.replace(
        "https://www.dropbox.com/",
        "https://dl.dropboxusercontent.com/"
    )


def main() -> None:
    csv_data = ""

    errors = []

    dbx = dropbox.Dropbox(config['DROPBOX_SECRET'])

    for file in tqdm(os.listdir(config['IMAGES_FOLDER'])[0:5]):
        if not os.path.isfile(os.path.join(config['IMAGES_FOLDER'], file)):
            continue

        # upload file to dropbox
        if (url := upload_file(dbx, file)) is None:
            errors.append(file)
            continue

        # fix link to direct
        url = replace_shared_link_to_download_link(url)

        # add to csv data
        csv_data += f"{url},{file}\n"

    if errors:
        logger.error("Unable to upload files: %s" % "\n".join(errors))

    with open(config['CSV_FILE'], 'w') as f:
        f.write(csv_data)


if __name__ == "__main__":
    main()
