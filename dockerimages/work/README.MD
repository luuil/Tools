## Docker image

### Build the image

```bash
docker build -t luuil:work -f ./Dockerfile .
```

### Run the image

```bash
docker run -i -t --rm luuil:work /bin/bash
```

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