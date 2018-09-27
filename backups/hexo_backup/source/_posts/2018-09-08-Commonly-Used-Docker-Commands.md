---
title: Commonly Used Docker Commands
categories:
  - Tutorial
tags:
  - Docker
date: 2018-09-08 16:21:35
---

## 常用的 Docker 命令

本文集中了一些常用的 Docker 命令, 详细还请查看 [官方文档][docker-cmds].

- 查看容器: `docker ps`
- 查看镜像: `docker images`
- 运行镜像: `docker run <IMAGE>`
- 进入容器: `docker exec -t -i <CONTAINER> /bin/bash`


<!-- more -->

### 查看本地容器

```
docker ps
```

- [docker ps][docker-cmds-ps]


### 查看本地镜像

```
docker images
```

- [docker images][docker-cmds-images]


### 运行镜像: 物理机映射到容器

```
docker run -v /local/path:/inner/path  -d -i -t <IMAGE>
```

如

```
docker run -v /home/luuil:/luuil  -dit ubuntu:latest
```

- [docker run][docker-cmds-run]


### 进入指定容器

形式

```
docker exec -it <CONTAINER> /bin/bash
```

如

```
docker exec -it 5cb8d5b22575 /bin/bash
```

- [docker exec][docker-cmds-exec]

## 高级命令

更不常用的那些命令.

### 运行 NVIDIA DOCKER, 并指定使用的GPU

```
docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=0,1 --rm nvidia/cuda nvidia-smi
```

- [docker run][docker-cmds-run]
- [nvidia docker run][nv-docker-run]

### 创建及发布镜像(私有仓库)

```
docker build -t <IMAGE> -f <Dockerfile> .
docker tag <SOURCE_IMAGE>[:TAG] <TARGET_IMAGE>[:TAG]
docker push NAME[:TAG]
```

如

```
docker build -t src-image -f Dockerfile ..
docker tag src-image:latest registry-host:5000/myadmin/tgt-image:latest
docker push registry-host:5000/myadmin/tgt-image:latest
```

- [docker build][docker-cmds-build]
- [docker tag][docker-cmds-tag]
- [docker push][docker-cmds-push]


### 将变更后的镜像保存: `docker commit`


```
docker commit -m "commit message" <CONTAINER> [REPOSITORY[:TAG]]
```

- [docker commit][docker-cmds-commit]

### 根据 Dockerfile 创建镜像: `docker build`

```
docker build -t "test_image:latest" .
```

- [docker build][docker-cmds-build]

## 异常状况

下面内容属于容器异常时的一些解决办法.

### 停止 `Restarting` 状态的容器

```
docker update --restart=no <CONTAINER>
```

- [docker update][docker-cmds-update]

[docker-cmds]: https://docs.docker.com/engine/reference/commandline/docker/
[docker-cmds-ps]: https://docs.docker.com/engine/reference/commandline/ps/
[docker-cmds-build]: https://docs.docker.com/engine/reference/commandline/build/
[docker-cmds-commit]: https://docs.docker.com/engine/reference/commandline/commit/
[docker-cmds-update]: https://docs.docker.com/engine/reference/commandline/update/
[docker-cmds-tag]: https://docs.docker.com/engine/reference/commandline/tag/
[docker-cmds-push]: https://docs.docker.com/engine/reference/commandline/push/
[docker-cmds-exec]: https://docs.docker.com/engine/reference/commandline/exec/
[docker-cmds-images]: https://docs.docker.com/engine/reference/commandline/images/
[docker-cmds-run]: https://docs.docker.com/engine/reference/commandline/run/
[nv-docker-run]: https://github.com/NVIDIA/nvidia-docker/wiki/Usage