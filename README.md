# Prerequisites

Dependencies required before proceeding to Installation and Run:

- [docker](https://docs.docker.com)
- [jq](https://stedolan.github.io/jq/download/)
- envsubst


# Installation

Before starting the mintery docker setup, we need to first initialize an
address with some tez, and then deploy an NFT contract that will be owned by you.

If you prefer not to be bothered with the details, simply execute `./script/setup`.
Otherwise, continue reading for more detailed information on what steps this `setup`
sequentially applies.

First, run the `script/initialize-address` script. This will provide you with
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

Then, run the `script/deploy-contract` script.

## Address initialization

Deploying a contract requires some tez present in the address associated to the
private key. Since we're deploying on a testnet, we can use one
of the public faucet services that provide us with free tez:

- `@tezos_faucet_bot` on telegram
- https://teztnets.xyz/
