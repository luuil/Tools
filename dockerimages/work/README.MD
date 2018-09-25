## Docker image

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