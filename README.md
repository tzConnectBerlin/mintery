# Prerequisites

Dependencies required before proceeding to Installation and Run:

- docker-compose
- yarn
- psql (from postgresql, only needed for using the `script/dbconn` script, not a necessity)


# Installation

Before starting the mintery docker-compose setup, we need to first deploy an
NFT contract that will be owned by you.

Run the `script/deploy-contract.bash` script, giving your public tezos key (aka your tz1 address) as first argument, and the corresponding private key as second argument. For example:

```bash
./script/deploy-contract.bash tz1g3coajkc9N77XDy55pVEgBGWspQfYqMiH edsk...
```

# Run

After installation is done, simply call `docker-compose up`.

When docker-compose is up, you can connect to the database with `script/dbconn`
