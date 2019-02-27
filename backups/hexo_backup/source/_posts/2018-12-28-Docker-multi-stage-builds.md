---
title: Docker multi-stage builds
categories:
  - Tutorial
tags:
  - Docker
  - Multi-stage builds
  - Dockerfile
  - 多阶段构建
date: 2018-12-28 10:45:53
---

Docker多阶段构建是17.05以后引入的新特性，旨在解决编译和构建复杂、镜像太大的问题。因此要使用多阶段构建特性必须使用高于或等于17.05的Docker。

<!-- more -->

## 多阶段构建出现之前

构建镜像最具挑战性的一点是使镜像大小尽可能的小。Dockerfile中的每条指令都为图像添加了一个图层，您需要记住在移动到下一层之前清理任何不需要的东西。

为了编写一个真正高效的Dockerfile，传统上需要使用shell技巧和其他逻辑来保持层尽可能小，并确保每个层都具有前一层所需的东西。

实际上，有一个Dockerfile用于开发（包含构建应用程序所需的所有内容），以及用于生产环境的精简版Dockerfile，它只包含您的应用程序以及运行它所需的内容。这被称为**“建造者模式”**。维护两个Dockerfile并不理想。

这是一个Dockerfile.build和Dockerfile的例子，它遵循上面的模式：

Dockerfile.build

```dockerfile
FROM golang:1.7.3
WORKDIR /go/src/github.com/alexellis/href-counter/
COPY app.go .
RUN go get -d -v golang.org/x/net/html \
&& CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .
```

请注意，此示例使用Bash `&&` 运算符压缩两个RUN命令，以避免在image中创建其他层。这很容易出错并且难以维护。

Dockerfile

```dockerfile
FROM alpine:latest  
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY app .
CMD ["./app"]
```

build.sh

```bash
#!/bin/sh
echo Building alexellis2/href-counter:build
docker build --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy \
-t alexellis2/href-counter:build . -f Dockerfile.build
docker container create --name extract alexellis2/href-counter:build  
docker container cp extract:/go/src/github.com/alexellis/href-counter/app ./app  
docker container rm -f extract
echo Building alexellis2/href-counter:latest
docker build --no-cache -t alexellis2/href-counter:latest .
rm ./app
```

当您运行build.sh脚本时，它需要构建第一个image，从中创建容器以复制工件，然后构建第二个image。

多阶段构建可以大大简化这种情况.

## 使用多阶段构建

对于多阶段构建，您可以在Dockerfile中使用多个`FROM`语句。每个FROM指令可以使用不同的基础，并且每个指令都开始一个新的构建。您可以选择性地将工件从一个阶段复制到另一个阶段，从而在最终image中只留下您想要的内容。 

为了说明这是如何工作的，让我们调整上述示例的Dockerfile以使用多阶段构建。

Dockerfile

```dockerfile
FROM golang:1.7.3
WORKDIR /go/src/github.com/alexellis/href-counter/
RUN go get -d -v golang.org/x/net/html  
COPY app.go .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .
FROM alpine:latest  
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=0 /go/src/github.com/alexellis/href-counter/app .
CMD ["./app"]  
```

您只需要单个Dockerfile。您也不需要单独的构建脚本。只需运行docker build

```bash
$ docker build -t app:latest .
```

最终结果是产生与之前相同大小的image，复杂性显著降低。您不需要创建任何中间image，也不需要将任何artifacts提取到本地系统。

### 它是如何工作的？

第二个FROM指令以`alpine:latest`镜像为基础开始一个新的构建阶段。

`COPY –from = 0` 行仅将前一阶段的构建文件复制到此新阶段。Go SDK和任何中间层都被遗忘，而不是保存在最终image中。

### 为多构建阶段命名

默认情况下，阶段未命名，您可以通过**整数**来引用它们，从第0个FROM指令开始。 

但是，您可以通过向FROM指令添加`as NAME`来命名您的阶段。此示例通过命名阶段并使用COPY指令中的名称来改进前一个示例。

这意味着即使稍后重新排序Dockerfile中的指令，COPY也不会中断。

```dockerfile
FROM golang:1.7.3 as builder
WORKDIR /go/src/github.com/alexellis/href-counter/
RUN go get -d -v golang.org/x/net/html  
COPY app.go    .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .
FROM alpine:latest  
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /go/src/github.com/alexellis/href-counter/app .
CMD ["./app"]
```

## 停在特定的构建阶段

构建镜像时，不一定需要构建整个Dockerfile每个阶段。

您可以指定目标构建阶段。以下命令假定您使用的是以前的Dockerfile，但在名为builder的阶段停止：

```bash
$ docker build --target builder -t alexellis2/href-counter:latest .
```

使用此功能可能的一些非常适合的场景是：

- 调试特定的构建阶段
- 在debug阶段，启用所有调试或工具，而在production阶段尽量精简
- 在testing阶段，您的应用程序将填充测试数据，但在production阶段则使用生产数据

## 使用外部镜像作为stage

使用多阶段构建时，您不仅可以从Dockerfile中创建的镜像中进行复制。

您还可以使用`COPY –from`指令从单独的image中复制，使用本地image名称，本地或Docker注册表中可用的标记或标记ID。

如有必要，Docker会提取image并从那里开始复制。

```dockerfile
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

## Ref.

- 官方文档 [multistage-build](https://docs.docker.com/develop/develop-images/multistage-build/)