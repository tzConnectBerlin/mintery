# Prerequisites

Dependencies required before proceeding to Installation and Run:

- docker-compose
- yarn
- psql (from postgresql, only needed for using the `script/dbconn` script, not a necessity)


# Installation

Before starting the mintery docker-compose setup, we need to first initialize an
address with some tez, and then deploy an NFT contract that will be owned by you.

First, run the `script/initialize-address.bash` script. This will provide you with
a fresh Tezos address that has some tez loaded on the Hangzhou testnet. Alternatively,
if you already have an address with tez ready, or you want to setup an address with tez
in a different way (see "Address initialization" section), you can skip this step
and instead write your public and private key into a ".env" file in the root directory
of this repo, in the following format:
```
ADMIN_ADDRESS="<your public key here>"
ORIGINATOR_PRIVATE_KEY="<your private key here>"
```

This file also allows a third optional setting, regardless of address initialization
method, called "NODE_URL". By default we are currently using http://art-basel.tzconnect.berlin:18732. This is a Hangzhou2net testnet node. If you wish to deploy on a different net, set this variable to something else in the .env file.

Then, run the `script/deploy-contract.bash` script.

## Address initialization

Deploying a contract requires some tez present in the address associated to the
private key. Since we're deploying on a testnet (Hangzhou2net), we can use one
of the public faucet services that provide us with free tez:

- `@tezos_faucet_bot` on telegram (in our experience the easiest to use)
- https://teztnets.xyz/hangzhounet-faucet (should work as well, but does require the `tezos-client` tool to be installed)

# Run

After installation is done, simply call `docker-compose up`.

When docker-compose is up, you can connect to the database with `script/dbconn`

# Brief intro of each component

The following components are run by docker-compose:

- [Peppermint](https://github.com/tzConnectBerlin/peppermint)
- [Que Pasa](https://github.com/tzConnectBerlin/que-pasa)
- A [PostgreSQL](https://www.postgresql.org/docs/13/index.html) database

Peppermint mints NFTs. Que Pasa reads what happens onchain and delivers a representation of
that in the PostgreSQL database.

Peppermint lives in 1 schema in the database: `peppermint`.

Que Pasa lives in 2 schemas in the database:

- `que_pasa`; for tables that aren't directly related to the contract storage values (such as the `levels` table, which just stores some info about what levels have been processed)
- `onchain_mintery`; for tables that are directly related to the contract storage values
