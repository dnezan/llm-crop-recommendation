# Hyperspectral Satellite Imagery Viewer and Harvest Planning App 

**Secure, user-friendly and data-driven agriculture-based Streamlit app deployed on Streamlit Community Cloud/Azure App Service**

![](./assets/reth-alpha.png)

**[Installation](./install)**
| [User Book](https://paradigmxyz.github.io/reth)
| [Developer Docs](./docs)
| [Demo](https://agritech-crop-app.streamlit.app/)

*The project is still work in progress, see the [disclaimer below](#status).*

## Installation

Pip install all the package including in *requirements.txt* in a Python>=3.8 environment.
```sh
git clone https://github.com/dnezan/llm-crop-recommendation
pip install requirements.txt
```
To use your Google Earth Engine service account credentials, make sure to authenticate your access by using the code below, and add your credentials as Streamlit Secrets if you are deploying on Streamlit Community Cloud. You can also use Azure Key Vault if you are deploying on Azure.

```python
json_data = st.secrets["json_data"]
# Preparing values
json_object = json.loads(json_data, strict=False)
service_account = st.secrets["service_account"]
json_object = json.dumps(json_object)
# Authorising the app
credentials = ee.ServiceAccountCredentials(service_account, key_data=json_object)
ee.Initialize(credentials)
```

Replace your credentials as a **Secret** in TOML format.
```toml
json_data = { 
    "type": "service_account",
    "project_id": "****",
    "private_key_id": "****",
    "private_key": "****",
    "client_email": "****.iam.gserviceaccount.com",
    "client_id": "****",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "****",
    "universe_domain": "googleapis.com"
     }

service_account = '****.iam.gserviceaccount.com'
```

## How does it work?

some sample text here

## Goals
1. **Accessible**

2. **Integrated**

![gif1](https://github.com/dnezan/llm-crop-recommendation/blob/main/data/gifs/browse.gif?raw=true)

3. **Secure**

4. **Versatile**
![gif1](https://github.com/dnezan/llm-crop-recommendation/blob/main/data/gifs/versatile.gif?raw=true)



1. **Modularity**: Every component of Reth is built to be used as a library: well-tested, heavily documented and benchmarked. We envision that developers will import the node's crates, mix and match, and innovate on top of them. Examples of such usage include but are not limited to spinning up standalone P2P networks, talking directly to a node's database, or "unbundling" the node into the components you need. To achieve that, we are licensing Reth under the Apache/MIT permissive license. You can learn more about the project's components [here](./docs/repo/layout.md).
2. **Performance**: Reth aims to be fast, so we used Rust and the [Erigon staged-sync](https://erigon.substack.com/p/erigon-stage-sync-and-control-flows) node architecture. We also use our Ethereum libraries (including [ethers-rs](https://github.com/gakonst/ethers-rs/) and [revm](https://github.com/bluealloy/revm/)) which we’ve battle-tested and optimized via [Foundry](https://github.com/foundry-rs/foundry/).
3. **Free for anyone to use any way they want**: Reth is free open source software, built for the community, by the community. By licensing the software under the Apache/MIT license, we want developers to use it without being bound by business licenses, or having to think about the implications of GPL-like licenses.
4. **Client Diversity**: The Ethereum protocol becomes more antifragile when no node implementation dominates. This ensures that if there's a software bug, the network does not finalize a bad block. By building a new client, we hope to contribute to Ethereum's antifragility.
5. **Support as many EVM chains as possible**: We aspire that Reth can full-sync not only Ethereum, but also other chains like Optimism, Polygon, BNB Smart Chain, and more. If you're working on any of these projects, please reach out.
6. **Configurability**: We want to solve for node operators that care about fast historical queries, but also for hobbyists who cannot operate on large hardware. We also want to support teams and individuals who want both sync from genesis and via "fast sync". We envision that Reth will be configurable enough and provide configurable "profiles" for the tradeoffs that each team faces.

## Status

The project is **not ready for production use**.

As of June 26, 2023, the app is live on Streamlit community Cloud and the demo can be accessed by clicking on this !link(https://agritech-crop-app.streamlit.app/). It has also been deployed on Azure as an app service.


We recommend using [`cargo nextest`](https://nexte.st/) to speed up testing. With nextest installed, simply substitute `cargo test` with `cargo nextest run`.

> **Note**
> 
> Some tests use random number generators to generate test data. If you want to use a deterministic seed, you can set the `SEED` environment variable.

## Getting Help

If you have any questions, first see if the answer to your question can be found in the [book][book].

If the answer is not there:

- Join the [Telegram][tg-url] to get help, or
- Open a [discussion](https://github.com/paradigmxyz/reth/discussions/new) with your question, or
- Open an issue with [the bug](https://github.com/paradigmxyz/reth/issues/new)

## Security

See [`SECURITY.md`](./SECURITY.md).

## Acknowledgements

Reth is a new implementation of the Ethereum protocol. In the process of developing the node we investigated the design decisions other nodes have made to understand what is done well, what is not, and where we can improve the status quo.

None of this would have been possible without them, so big shoutout to the teams below:
* [Geth](https://github.com/ethereum/go-ethereum/): We would like to express our heartfelt gratitude to the go-ethereum team for their outstanding contributions to Ethereum over the years. Their tireless efforts and dedication have helped to shape the Ethereum ecosystem and make it the vibrant and innovative community it is today. Thank you for your hard work and commitment to the project.
* [Erigon](https://github.com/ledgerwatch/erigon) (fka Turbo-Geth): Erigon pioneered the ["Staged Sync" architecture](https://erigon.substack.com/p/erigon-stage-sync-and-control-flows) that Reth is using, as well as [introduced MDBX](https://github.com/ledgerwatch/erigon/wiki/Choice-of-storage-engine) as the database of choice. We thank Erigon for pushing the state of the art research on the performance limits of Ethereum nodes.
* [Akula](https://github.com/akula-bft/akula/): Reth uses forks of the Apache versions of Akula's [MDBX Bindings](https://github.com/paradigmxyz/reth/pull/132), [FastRLP](https://github.com/paradigmxyz/reth/pull/63) and [ECIES](https://github.com/paradigmxyz/reth/pull/80) . Given that these packages were already released under the Apache License, and they implement standardized solutions, we decided not to reimplement them to iterate faster. We thank the Akula team for their contributions to the Rust Ethereum ecosystem and for publishing these packages.

[book]: https://paradigmxyz.github.io/reth/
[tg-url]: https://t.me/paradigm_reth