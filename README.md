# js-blob-analysis

Partial analysis/deobfuscation of JS malware seen around.

##  Analysis
See [ANALYSIS.MD](./ANALYSIS.md) for (some) details on how this malware works.

## Deobfuscator usage
```
$ uv run python src/cli.py
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  deobfuscate-samples       Deobfuscate dropper samples in...
  download-latest-payloads  Download latest malware payloads from crypto...
```

## Repo Structure
- `/src` - hacky deobfuscator source
- `/test` - tests for the hacky deobfuscator
- `/malware_dropper_samples` - Raw samples of the injected blobs.
- `/malware_dropper_samples_output` - Deobfuscated samples, commited to repo for easy browsing.
- `/malware_payload_samples_output` - Raw/deobfuscated payloads from the BSC chain, commited to repo for easy browsing.
- `/malware_payload_samples_output_manual` - Manually modifed payload samples, commited to repo for easy browsing.


# "Fix"
This is not a solution for actually getting rid of all the infected libraries or binaries on your machine. However, these will atleast prevent the dropper from being able to grab updates/reinstalling, and communication with one/some of the C&C servers.

## DNS blocking
`etc/hosts`:
```
# JS malware dropper uses the latest transactions of some wallets as pointer to smart contracts
# containing the latest version of the malware blob. These are otherwise legitimate hosts, but
# block them entirely to incapacitate the dropper.
127.0.0.1 api.trongrid.io
127.0.0.1 fullnode.mainnet.aptoslabs.com
127.0.0.1 bsc-dataseed.binance.org
127.0.0.1 bsc-rpc.publicnode.com
```

## IP blocking
Ubuntu UFW
```bash
sudo ufw deny out from any to 136.0.9.8
sudo ufw deny out from any to 23.27.20.143
sudo ufw deny out from any to 23.27.202.27
sudo ufw deny out from any to 166.88.4.2
```

Mac pfctl:
1. Edit - `sudo nano /etc/pf.conf`, append:
    ```
    # JS Malware C&C servers
    block drop from any to 136.0.9.8
    block drop from any to 23.27.20.143
    block drop from any to 23.27.202.27
    block drop from any to 166.88.4.2
    ```
2. Load - `sudo pfctl -f /etc/pf.conf`
3. Enable - `sudo pfctl -e`


## IDE persistence
If any of the files contain the senteniel value "C250617A", fully delete and reinstall the infected IDE.

VSCode:
* Windows: `%LOCALAPPDATA%\Programs\Microsoft VS Code\resources\app\node_modules\@vscode\deviceid\dist\index.js`
* Mac: `/Applications/Visual Studio Code.app/Contents/Resources/app/node_modules/@vscode/deviceid/dist/index.js`
* Linux: `/usr/share/code/resources/app/node_modules/@vscode/deviceid/dist/index.js`

Cursor
* Windows: `%LOCALAPPDATA%\Programs\cursor\resources\app\node_modules\@vscode\deviceid\dist\index.js`
* Mac: `/Applications/Cursor.app/Contents/Resources/app/node_modules/@vscode/deviceid/dist/index.js`
* Linux: `/usr/share/cursor/resources/app/node_modules/@vscode/deviceid/dist/index.js `