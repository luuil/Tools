---
title: 'LabelMe-Docker: Online Annotaion Tool Docker Image'
categories:
  - Tool
tags:
  - Docker
  - LabelMe
  - Image Annotation
date: 2018-09-07 10:58:21
---


LabelMe 是一个用 Javascript 编写的图像标注工具, 可以用于 **在线** 图像标注. 也就是说, LabelMe 可以部署在服务器, 然后使用浏览器进行访问.

与传统图像标注工具相比, 优势在于可以从任何地方访问该工具, 而且不需要在自己机器上安装或复制整个大型数据集.

我在空闲时间调研了该工具, 探索了其用法, 创建了此 docker 镜像, 并写成文档进行记录. 在该工具调研之后的 4 个月得到了团队的应用, 现我已将它部署在服务器, 以供外包人员能够远程进行标注. 它有如下优势

- 添加待标图片和获取标注结果方便.
- 降低外包人员招聘成本: 之前需要招聘专职标注人员到公司进行标注, 招聘难度大.
- 降低标注成本: 因为能够远程标注, 自由度高, 可以适当降低标注价格.
- 降低标注数据泄露的风险: 待标图片和标注结果均在服务器上.

截止目前(2018年9月), 已有 `1` 个项目(背景分割) 和 `10` 个标注人员使用该工具共标注了 `~7000` 张图片,
结果显示误标率较低, 约 `3/1000`, 且多数情况为误操作.


<!-- more -->


## 简易教程

这里我们假设在本地已经创建了 `labelme-web` 镜像(如未创建, 请按后两节进行创建),
则运行下列命令即可部署在本地(这里涉及到 Docker, 可以参考本站文章 {% post_link Commonly-Used-Docker-Commands %}):

```bash
sudo docker run -dit -p 1080:80 \
-v /home/luuil/labelme/Images:/var/www/html/Images \
labelme-web:latest
```

> - 其中 `/home/luuil/labelme` 可替换为您自己的目录.
> - 我们将 `Images` 文件夹映射到本地, 是为了更好地 **添加** 待标图片.

### 添加待标注图片

如果要添加新的待标注图片(LabelMe限制 **必须为.jpg格式**), 则进行如下操作:

- 在 `/home/luuil/labelme/Images` 中新建文件夹, 比如 `example`
- 将图片数据放入 `/home/huya/labelme/Images/example`
- 使用浏览器访问 `http://127.0.0.1:1080/tool.html?mode=f&folder=example`

### 获取标注结果

如果想要 **获取** 标注结果 , 需要先进入 Docker, 检查三个结果文件夹

- `/var/www/html/Annotations`
- `/var/www/html/Masks`
- `/var/www/html/Scribbles`

不需要进入容器, 而快速从 Docker 容器内拷贝上述文件夹至本地的 **当前文件夹** 的方式为:

```bash
   sudo docker cp <container_id>:/var/www/html/Annotations . \
&& sudo docker cp <container_id>:/var/www/html/Masks . \
&& sudo docker cp <container_id>:/var/www/html/Scribbles .
```

> `<container_id>` 为部署容器的 ID.

根据不同的标注方法, 可以在 `Annotations`, `Masks` 和 `Scribbles` 等文件夹中找到我们想要的结果, 具体有何区别, 待读者自己探索:).

## Docker

使用第三节中的 Dockerfile, 创建一个 LabelMe Docker image. 随后, 直接运行镜像即可.

### 创建

```bash
sudo docker build -t "labelme-web" .
```

### 运行镜像(即创建容器)

```bash
sudo docker run -dit -p 1080:80 \
-v /home/luuil/labelme/Images:/var/www/html/Images \
labelme-web:latest
```

## Dockerfile

```Dockerfile
# labelme Dockerfile
# base image
FROM ubuntu:14.04.5

# install dependencies
RUN apt-get -y update
RUN apt-get install dialog apt-utils -y
RUN apt-get install -y --no-install-recommends \
    build-essential \
    git \
    apache2 \
    php5 \
    libapache2-mod-perl2 \
    libapache2-mod-php5

# clean up
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm /var/log/dpkg.log

# apache2 configuration
RUN a2enmod include
RUN a2enmod rewrite
RUN a2enmod cgi
RUN update-rc.d apache2 defaults

# confd apache2 configuration
RUN rm /etc/apache2/sites-enabled/000-default.conf
ADD ubuntu.conf /etc/apache2/sites-enabled/000-default.conf

# configure environment
ENV LANG=C
ENV APACHE_LOCK_DIR                     /var/lock/apache2
ENV APACHE_RUN_DIR                      /var/run/apache2
ENV APACHE_PID_FILE                     ${APACHE_RUN_DIR}/apache2.pid
ENV APACHE_LOG_DIR                      /var/log/apache2
ENV APACHE_RUN_USER                     www-data
ENV APACHE_RUN_GROUP                    www-data
ENV APACHE_MAX_REQUEST_WORKERS          32
ENV APACHE_MAX_CONNECTIONS_PER_CHILD    1024
ENV APACHE_ALLOW_OVERRIDE               None
ENV APACHE_ALLOW_ENCODED_SLASHES        Off

# deploy repo
RUN cd /var/www/ \
    && rm -rf html \
    && git clone https://github.com/CSAILVision/LabelMeAnnotationTool.git html \
    && cd html \
    && make \
    && chown -R ${APACHE_RUN_USER}:${APACHE_RUN_GROUP} /var/www

# port binding
EXPOSE 80

# run
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
```

源码: [Github: LabelMeAnnotationTool][labelme]


[docker-doc]: https://docs.docker.com/
[labelme]: https://github.com/CSAILVision/LabelMeAnnotationTool/