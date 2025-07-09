# Analysis

## Overview

At a high level, this malware seemingly has three parts to it:

0. Dropper
    * JS libraries and/or repos are infected with the dropper. When executed, downloads and runs payload1/payload2.
1. Payload 1 - RAT
    * Handles persistence on disk / infecting IDE installations.
    * Connects to C&C, waits for commands (file upload/download/execution, etc)
2. Payload 2(/3) - Info Stealer
    * Steals environment vars, browser cookies, dev credentials, password dbs, crypto wallets, etc. 

## Samples

We have two samples of the latest(?) malware dropper in question, found in two different repos over the past few weeks:
* `sample1@7456491591821f8c46a832a43fde4b6be57ab53d`
* `sample2@76b7975b3e87dcb2f8ec935cde8fbd3f8a912f0a`

Each dropper sample has a version identifier (set in the global `_V` variable), which is used to identify itself to the C&C server(s):
* Sample1: `'5-143'`
* Sample2: `'5-3-3'`

Despite the version differences, both of the droppers variants have the same logic once deobfuscated, so the following will treat them as the same.

## Dropper

The dropper is first seen injected into (seemingly) random .js files, at the end of the file (prefixed by hundreds of spaces to mask it's presence in editors without word-wrapping enabled).

Once it decodes itself through multiple layers of obfuscation, it fetches the latest payloads stored as input data to on-chain transactions.

### Payload download logic

1. Get a transaction hash on the BSC chain via either TRON or APTOS chains:
    - `https://api.trongrid.io/v1/accounts/<TRON ACCOUNT>/transactions?only_confirmed=true&only_from=true&limit=1` (raw data decoded as hex and reversed)
    - `https://fullnode.mainnet.aptoslabs.com/v1/accounts/<APTOS ACCOUNT>/transactions?limit=1` (payload arguments[0])

2. Get the encoded payload stored as an input the transacation, via:
    - `eth_getTransactionByHash` on `bsc-dataseed.binance.org` with the transacation hash
    - `eth_getTransactionByHash` on `bsc-rpc.publicnode.com` with the transacation hash

3. Decode payload1 with the key provided key

In specific, it will use the hardcoded TRON/APTOS/KEY values:
```python
{
    'name': 'payload1',
    'key': '2[gWfGj;<:-93Z^C',
    'trongrid_id': 'TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP',
    'aptos_id': '0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e',
},
{
    'name': 'payload2',
    'key': 'm6:tTh^D)cBz?NM]',
    'trongrid_id': 'TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG',
    'aptos_id': '0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3',
}
```

See the `download_latest_payloads` command in `./src/cli.py` for a reimplementation of this logic.


## Payload 1
At the time of writing, Payload 1 just another small script which solely downloads an another payload from the blockchain(s):
```
{
    'name': 'payload1_inner',
    'key': 'cA]2!+37v,-szeU}',
    'trongrid_id': 'TLmj13VL4p6NQ7jpxz8d9uYY6FUKCYatSe',
    'aptos_id': '0x3414a658f13b652f24301e986f9e0079ef506992472c1d5224180340d8105837',
}
```
### Payload 1 (inner)

The inner payload effectively acts as a RAT and has two main roles:
1. Injecting itself into VSCode / Cursor installation for persistance ([See partially deobfuscated source](https://github.com/angu26/js-blob-analysis/blob/main/malware_payload_samples_output_manual/payload1_inner_bsc_0xc8090a40230cfacb82ead30d8d290a22f8e5f508800d725f8ae2dd1d35e03427_synchrony_deobfu.malware_sample#L93C24-L217))

    VSCode:
    * Windows: `%LOCALAPPDATA%\Programs\Microsoft VS Code\resources\app\node_modules\@vscode\deviceid\dist\index.js`
    * Mac: `/Applications/Visual Studio Code.app/Contents/Resources/app/node_modules/@vscode/deviceid/dist/index.js`
    * Linux: `/usr/share/code/resources/app/node_modules/@vscode/deviceid/dist/index.js`

    Cursor
    * Windows: `%LOCALAPPDATA%\Programs\cursor\resources\app\node_modules\@vscode\deviceid\dist\index.js`
    * Mac: `/Applications/Cursor.app/Contents/Resources/app/node_modules/@vscode/deviceid/dist/index.js`
    * Linux: `/usr/share/cursor/resources/app/node_modules/@vscode/deviceid/dist/index.js`

    The sentinel string ["C250617A" is used](https://github.com/angu26/js-blob-analysis/blob/main/malware_payload_samples_output_manual/payload1_inner_bsc_0xc8090a40230cfacb82ead30d8d290a22f8e5f508800d725f8ae2dd1d35e03427_synchrony_deobfu.malware_sample#L71-L79) to detect whether the dropper has already been installed into the IDE files.

2. Start session with a C&C server and wait for commands ([See partially deobfuscated source](https://github.com/angu26/js-blob-analysis/blob/main/malware_payload_samples_output_manual/payload1_inner_bsc_0xc8090a40230cfacb82ead30d8d290a22f8e5f508800d725f8ae2dd1d35e03427_synchrony_deobfu.malware_sample#L494-L603))
    * Commands / Capabilites
        - `ss_info` - get client info
        - `ss_ip` - get client public IP
        - `ss_upf` - upload file to C&C
        - `ss_upd` - upload entire directory to C&C
        - `ss_dir` - change current working directory
        - `ss_fcd` - change current working directory
        - `ss_stop` - stop session
        - `ss_inz` - install dropper into C&C-specified file
        - `ss_eval` - run C&C-provided string as JS `eval`

## Payload 2
Similar to payload 1, payload 2 is just a smaller wrapper to download _another_ inner payload. However, this one retreives the inner payload directly from a C&C server rather than the blockchain(s).

The encoded blob is downloaded with a GET request to `https://23.27.20[.]143:27017/$/boot` with these specific headers (note the global dropper version in `_V`):
```js
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML; like Gecko) Chrome/131.0.0.0 Safari/537.36';
headers['Sec-V'] = _global['_V'] || 0x0;
```

Then, the blob is decoded with a hard-coded key ([See deobfuscated source](https://github.com/angu26/js-blob-analysis/blob/main/malware_payload_samples_output_manual/payload2_bsc_0x13e3ce3aefc019258c618265241ec1c51d858e6e5457a48ea5e38820fc4ba9a1_deobfu_beautified.malware_sample#L6-L14)).


### Payload 2 (inner)
1. Start the malware client code again as a separate node process
2. Steal process environment variables ([See partially deobfuscated source](https://github.com/angu26/js-blob-analysis/blob/main/malware_payload_samples_output_manual/payload2_inner_5-3-3_synchrony_deobfu.malware_sample#L161-L198))
    * The process environment variables are collected and posted to the C&C server at `https://23.27.20[.]143:27017/snv`, along with the local hostname and username.
3. Fetch and run another payload3 (written in Python)
    * This logic seems to have [extensive checks](https://github.com/angu26/js-blob-analysis/blob/main/malware_payload_samples_output_manual/payload2_inner_5-3-3_synchrony_deobfu.malware_sample#L199-L335) to bail out first when running under AWS, Amplify, GCP, Vercel, buildbot, Github Runners, and other test cases.

## Payload 3
[See partially deobfuscated source](https://github.com/angu26/js-blob-analysis/blob/main/malware_payload_samples_output_manual/payload3_inner_load_decoded.malware_sample)

This payload is a fairly extensive stealer, targeting:
1. Browsers (perfs, profiles, extensions lists, cookies/sessions)
2. Password managers (1password, bitwarden, dashlane, etc)
3. Dev credentials (`.npm`, `.git-credentials`, `~/.config/git/credentials`, etc)
4. Crypto wallets/keypairs (exodus, bitcoin, dogecoin, monero, solana, etc)

The files are uploaded either:
1. Directly to these C&C server(s) via HTTP
    * `http://136.0.9[.]8:27017`
    * `http://23.27.202[.]27:27017`
    * `http://166.88.4[.]2:27017`
2. To these Telegram chat ID's (with `https://api.telegram.org/bot7870147428:AAGbYG_eYkiAziCKRmkiQF-GnsGTic_3TTU/sendDocument`):
    - `7699029999`
    - `7609033774`
    - `-4697384025`

# Resources
* `rand-user-agent` supply chain attack in May 2025 w/ same malware family
    - https://www.aikido.dev/blog/catching-a-rat-remote-access-trojian-rand-user-agent-supply-chain-compromise
* Newer infections/supply chain attacks w/ same malware family
    - https://www.aikido.dev/blog/react-native-aria-attack