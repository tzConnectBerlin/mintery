# Mintery

A repo with some useful scripts for deploying contracts onto Tezos.

## Prerequisites

Dependencies required before proceeding to Installation and Run:

- [docker](https://docs.docker.com)
- [jq](https://stedolan.github.io/jq/download/)
- [envsubst](https://man7.org/linux/man-pages/man1/envsubst.1.html)

## Setup

The `env` file serves as both input as well as output. The following variables can be set for input:

```
NETWORK=.. (optional, defaults to ghostnet)
NODE_URL=.. (optional, defaults to https://ghostnet-archive.tzconnect.berlin

CONTRACT=.. (required, has to be the name (without extension) of a contract that is present in contracts/)
BURN_CAP=.. (optional, defaults to 0.1, it definesthe deployment cost in tez)

ORIGINATOR_ADDRESS=.. (optional if not mainnet, otherwise required, the tz address used to deploy the contract)
ORIGINATOR_PRIV_KEY=.. (same as above)

DOCKER_ARGS=.. (optional, defaults to nothing, can be used to specify custom docker arguments to be specified in docker run executions)
```

## Usage

Once input variables are correctly setup in `env`, call `/script/setup` if targeting a testnet, otherwise call `/script/deploy-contract`. The setup script does the same as `deploy-contract`, but before doing that it also generates a fresh tz address with loaded tez (from a testnet faucet) to use as the originator address (more convenient, but wont work on mainnet).

The contract address of the resulting contract deployment will be present in the `env` file under variable `CONTRACT_ADDRESS`.
