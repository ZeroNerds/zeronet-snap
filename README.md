# zeronet-snap
A snap for ZeroNet

> Open, free and uncensorable websites, using Bitcoin cryptography and BitTorrent network

[» ZeroNet](https://zeronet.io)

[» ZeroNet Repository](https://github.com/HelloZeroNet/ZeroNet)

# Installing

`sudo snap install zeronet`

# Usage

Options only in snap version:

`--enable-tor      Start both tor and zeronet`

All options:

```
usage: zeronet     [-h] [--verbose] [--debug] [--debug_socket]
                   [--debug_gevent] [--batch] [--config_file path]
                   [--data_dir path] [--log_dir path] [--language language]
                   [--ui_ip ip] [--ui_port port] [--ui_restrict [ip [ip ...]]]
                   [--open_browser [browser_name]] [--homepage address]
                   [--updatesite address] [--size_limit size]
                   [--connected_limit connected_limit] [--fileserver_ip ip]
                   [--fileserver_port port] [--disable_udp] [--proxy ip:port]
                   [--ip_external ip]
                   [--trackers [protocol://address [protocol://address ...]]]
                   [--trackers_file path] [--use_openssl {True,False}]
                   [--disable_db] [--disable_encryption]
                   [--disable_sslcompression {True,False}] [--keep_ssl_cert]
                   [--max_files_opened limit] [--use_tempfiles {True,False}]
                   [--stream_downloads {True,False}]
                   [--msgpack_purepython {True,False}]
                   [--fix_float_decimals {True,False}]
                   [--coffeescript_compiler executable_path]
                   [--tor {disable,enable,always}] [--tor_controller ip:port]
                   [--tor_proxy ip:port] [--tor_password password] [--version]
                   [--bit_resolver address]
                   [--optional_limit GB or free space %]
                   {main,siteCreate,siteNeedFile,siteDownload,siteSign,sitePublish,siteVerify,dbRebuild,dbQuery,peerPing,peerGetFile,peerCmd,cryptSign}
                   ...
```

# Compile
Clone the repository and run `snapcraft`

(To install the self-compiled version use `snap install --force-dangerous zeronet*.snap`)

# ToDos
 - [x] Rewrite launch scripts
 - [x] Allow enabling/disabling/adding plugins
 - [x] Compile python scripts
