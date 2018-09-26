## Docker image

Before build, put your own `Identity` and `Identity.pub` file into `.ssh/` directory first.

### Build the image

```bash
docker build -t luuil:work -f ./Dockerfile .
```

### Test the image

```bash
docker run -i -t --rm luuil:work /bin/bash
```

### Run the image

```bash
docker run --name "work" -d -i -t -v "d:/":/d  -v "e:/":/e  -v "f:/":/f luuil:work
```

## Docker container

### Into container

```bash
docker exec -i -t work //bin/bash
```

### Stop container

```bash
docker stop work
```

### Restart container

```bash
docker restart work
```


## Sync alias and scripts with remote

Sync our custom `alias` or `command scripts` with remote machine we used.

We do it in two ways as shown below.

### Command `go`

```bash
go <hostname>
```

will 

- sync `.sh/` dir, exclude `sync.sh`.
- send an copy of `.bashrc` to remote and store at `/tmp/.bashrc_temp`.
- ssh login remote, run `bash` with `/tmp/.bashrc_temp`.

> Excute every time when use `go` command.

Defined in [`.sh/.bash_aliases`](./.sh/.bash_aliases)

### Script `.sh/sync.sh`

```bash
bash .sh/sync.sh
```

will 

- sync `.sh/` dir, exclude `sync.sh`.
- append new line `source ~/.sh/.bashrc_append` to `<remote>:~/.bashrc` file.

> Excute just when run this script.

See details in [`.sh/sync.sh`](./.sh/sync.sh)


## Detail

### SSH Keychain

#### Requirements

- openssh
    ```bash
    apt-get install -y openssh-client
    ```
- keychain
    ```bash
    apt-get install -y keychain
    ```

#### Config

Append to `~/.bashrc`

```bash
eval `keychain --eval ~/.ssh/Identity`
```

Append to `~/.bash_profile` (create it if not exists.)

```bash
ssh-agent bash
```