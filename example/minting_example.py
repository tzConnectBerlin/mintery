#!/usr/bin/env python3

import os

import asyncio
import base58
import io
import json
import psycopg2
import requests
import time
import urllib3

PINATA_API_KEY = '...'
PINATA_API_SECRET = '...'
PINATA_JWT = '...'
PINATA_JWT_correct = '...'
PINATA_GATEWAY = 'gateway.pinata.cloud'
PINATA_PORT = 443
PINATA_URI = f"/dns/{PINATA_GATEWAY}/tcp/{PINATA_PORT}/https"

DB_HOST = '...'
DB_USER = '...'
DB_PASSWORD = '...'
DB_NAME = '...'

NFT_OWNER = 'tz1..'

AUTH_NAME = '...'
AUTH_PASS = '...'


class ImageException(Exception):
    """
    Raised when image fetch failed
    """

    def __init__(self, message='Image fetch failed'):
        self.message = message
        super().__init__(self.message)


class IpfsException(Exception):
    """
    Raised when upload to Pinata failed
    """

    def __init__(self, message='Ipfs failed'):
        self.message = message
        super().__init__(self.message)


def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD)


def create_token_id(ipfs):
    b = base58.b58decode(ipfs)
    token_id = int.from_bytes(b[-6:], 'big')
    return token_id


def queue_nft(recipient, content_ipfs_hash):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO peppermint.operations(originator, command) VALUES (%s, %s);",
                (NFT_OWNER,
                 json.dumps({
                     "handler": "nft",
                     "name": "mint",
                     "args": {
                         "token_id": create_token_id(content_ipfs_hash),
                         "to_address": recipient,
                         "metadata_ipfs": f"ipfs://{content_ipfs_hash}",
                     }
                 })))
    conn.commit()
    conn.close()


def nft_metadata(content_ipfs_hash, nft):
    ipfs_uri = f"ipfs://{content_ipfs_hash}"

    metadata = {
        "name": f"{nft['series']} - {nft['number']}",
        "description": "One of a series of unique artworks generated for XYZ by ABC",
        "tags": [],
        "symbol": f"{nft['uuid']}",
        "artifactUri": ipfs_uri,
        "creators": [],
        "formats": [
            {
                "uri": ipfs_uri,
                "mimeType": "image/jpeg"
            }
        ],
        "thumbnailUri": ipfs_uri,
        "decimals": 0,
        "isBooleanAmount": False
    }
    return metadata


def upload_nft_to_pinata(nft):
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}
    r = requests.get(nft['image'])
    if r.status_code != 200:
        raise ImageException
    f = io.BytesIO(r.content)
    response = requests.post("https://api.pinata.cloud/pinning/pinFileToIPFS",
                             headers=headers,
                             files={'file': f},
                             )
    if response.status_code != 200:
        raise IpfsException
    return json.loads(response.content)


def upload_json_to_pinata(obj):
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}
    response = requests.post("https://api.pinata.cloud/pinning/pinJSONToIPFS",
                             headers=headers,
                             json=obj,
                             )
    if response.status_code != 200:
        raise IpfsException
    return json.loads(response.content)


async def persist_nfts(nfts):
    for nft in nfts:
        nft_id = nft['id']
        with open(os.path.join('nfts', f'{nft_id}.json'), 'w') as fp:
            fp.write(json.dumps(nft))


def mark_minted(id):
    r = requests.patch(f"https://human-machine.io/api/artwork/{id}/",
                       auth=(AUTH_NAME, AUTH_PASS),
                       json={
                           "status": "minted"
                       })
    return r.text


def new_mark_minted(id, ipfs, status="minted"):
    r = requests.patch(f"https://human-machine.io/api/artwork/{id}/",
                       auth=(AUTH_NAME, AUTH_PASS),
                       json={
                           "status": status,
                           "ipfs": ipfs
                       })
    return r.text


async def process_nfts(nfts):
    asyncio.create_task(persist_nfts(nfts))
    if len(nfts) == 0:
        print(".", end='')
        return
    nft = nfts[0]

    print(f"processing:\n{json.dumps(nft)}")
    try:
        if nft['title'] == 'image_fetch_failed':
            raise ImageException
        if nft['title'] == 'ipfs_failed':
            raise IpfsException
        if nft['title'] == 'minting_failed':
            raise Exception
        status = "success"
        content_ipfs_hash = upload_nft_to_pinata(nft)['IpfsHash']
        metadata = nft_metadata(content_ipfs_hash, nft)
        metadata_ipfs_hash = upload_json_to_pinata(metadata)['IpfsHash']
        print(metadata_ipfs_hash)
        queue_nft(nft['wallet_address'], metadata_ipfs_hash)

    except ImageException as ie:
        status = "image_fetch_failed"
        print(f"\nException {ie}")
    except IpfsException as ie:
        status = "ipfs_failed"
        print(f"\nException {ie}")
    except Exception as e:
        status = "minting_failed"
        print('\nException minting failed')
    finally:
        print(mark_minted(nft['id']))


async def poll():
    while True:
        try:
            r = requests.get(
                'https://poll.some-uri.io/api/artwork/?status=ready', auth=(AUTH_NAME, AUTH_PASS))
            _json = json.loads(r.text)
            await process_nfts(_json['results'])
        except Exception as e:
            print(f"Exception {e} getting/parsing json")
            time.sleep(2)
            continue
        time.sleep(1)

if __name__ == '__main__':
    if not os.path.exists('nfts'):
        os.mkdir('nfts')

    asyncio.get_event_loop().run_until_complete(poll())
