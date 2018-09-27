---
title: Github Pages with Hexo
categories:
  - Tutorial
tags:
  - Github
  - Hexo
date: 2018-09-04 20:40:14
---

[Hexo][hexo] 是一个快速、简洁且高效的博客框架. 
Hexo 使用 Markdown(或其他渲染引擎)解析文章, 在几秒内, 即可利用靓丽的主题生成静态网页.


# 简易教程

本章主要介绍在使用 hexo 写文章时最常用的步骤, 如果想查看详细的内容可以查看 [原始文档][hexo] 或 下面的 **补充内容**.


在开始下面内容之前, 默认您已经**安装过Hexo及其相关依赖**, 并且已经设置好 **Github 仓库**. 
如果您还没做过上述操作, 请查看 [原始文档][hexo] 或 下面的 **补充内容**.

- 创建文章(存放至`source/_posts`)

    ```bash
    hexo new [layout] "<title>"
    ```

    上述命令会按照指定的 `layout` (layout 即模板, 存放于 `scaffolds` 文件夹中)生成一个简略的文章.

- 丰富之前创建的简略文章

- 发布(可集中放在 `deploy.sh` 中)

    ```bash
    hexo clean
    hexo generate
    hexo deploy
    ```

> 出现异常时, 可以参考 [异常][hexo-except]

<!-- more -->

# 补充内容

本章包含的是一般在初次使用时才会用到的内容, 或者一些内容的详细介绍.

## 安装

安装只需要几分钟, 遇到问题可以在此[提交][hexo-issue], 原版请查看[这里][hexo-doc].

### 前提

- [Node.js][njs]
- [Git][git]

然后使用下列 [npm][npm](随 Node.js 一同发布的包管理工具) 命令即可安装Hexo.

```bash
npm install -g hexo-cli
```

> 如果上述命令运行失败, 则重新启动命令行窗口再运行上述命令即可


## 建站

执行下列命令, Hexo 将会在指定文件夹中新建所需要的文件

```bash
hexo init {folder}
cd {folder}
npm install
```

新建完成后, 指定文件夹 `{folder}` 目录如下：

```
.
├── _config.yml
├── package.json
├── scaffolds
├── source
|   ├── _drafts
|   └── _posts
└── themes
```

### `_config.yml`

网站的 [配置][hexo-conf] 信息, 您可以在此配置大部分的参数. 

### `package.json`

应用程序的信息. [EJS][ejs], [Stylus][stylus]  和 [Markdown][md] renderer 已默认安装, 您可以自由移除. 

```json
{
  "name": "hexo-site",
  "version": "0.0.0",
  "private": true,
  "hexo": {
    "version": ""
  },
  "dependencies": {
    "hexo": "^3.0.0",
    "hexo-generator-archive": "^0.1.0",
    "hexo-generator-category": "^0.1.0",
    "hexo-generator-index": "^0.1.0",
    "hexo-generator-tag": "^0.1.0",
    "hexo-renderer-ejs": "^0.1.0",
    "hexo-renderer-stylus": "^0.2.0",
    "hexo-renderer-marked": "^0.2.4",
    "hexo-server": "^0.1.2"
  }
}
```

### `scaffolds`

[模版][hexo-wrt] 文件夹. 当您新建文章时, Hexo 会根据 `scaffold` 来建立文件. 

Hexo的模板是指在新建的markdown文件中默认填充的内容. 例如, 如果您修改 `scaffold/post.md` 中的 `Front-matter` 内容, 
那么每次新建一篇文章时都会包含这个修改. 

### `source`

资源文件夹是存放用户资源的地方. 除 `_posts` 文件夹之外, 开头命名为 `_` (下划线)的文件 / 文件夹和隐藏的文件将会被**忽略**. 
Markdown 和 HTML 文件会被解析并放到 `public` 文件夹, 而**其他文件**会被**拷贝**过去. 

### `themes`

[主题][hexo-thm] 文件夹. Hexo 会根据主题来生成静态页面.

比如, 安装一个新主题(首先要进入到**hexo文件夹**)

```bash
git clone https://github.com/theme-next/hexo-theme-next themes/next
```

然后修改`_config.yml`

```yaml
theme: next
```

想要个性化更多时, 可以编辑 `themes/next/_config.yml`. 比如想显示更多菜单, 取消相应的注释, 并在 `source` 文件夹中
添加相应的文件夹及 `index.md`.

```yaml
menu:
  home: / || home
  about: /about/ || user
  tags: /tags/ || tags
  categories: /categories/ || th
  archives: /archives/ || archive
```

想显示头像, 则修改 `avatar` 部分

```yaml
avatar:
  # in theme directory(source/images): /images/avatar.gif
  # in site  directory(source/uploads): /uploads/avatar.gif
  # You can also use other linking images.
  url: /avatar.gif #/images/avatar.gif
```


## 安装server

```bash
npm install hexo-server --save
```

安装完成后, 输入以下命令以启动服务器, 您的网站会在 `http://localhost:4000` 下启动. 在服务器启动期间, Hexo 会监视文件变动并自动更新, 您无须重启服务器. 

```bash
hexo server
```

如果您想要更改端口, 或是在执行时遇到了 `EADDRINUSE` 错误, 可以在执行时使用 `-p` 选项指定其他端口, 如下：

```bash
hexo server -p 5000
```

### 静态模式

在静态模式下, 服务器只处理 `public` 文件夹内的文件, 而不会处理文件变动, 在执行时, 您应该先自行执行 `hexo generate`, 此模式通常用于生产环境（production mode）下. 

```bash
hexo server -s
```

### 自定义 IP

服务器默认运行在 `0.0.0.0`, 您可以覆盖默认的 IP 设置, 如下：

```bash
hexo server -i 192.168.1.1
```

指定这个参数后, 您就只能通过该IP才能访问站点. 例如, 对于一台使用无线网络的笔记本电脑, 除了指向本机的`127.0.0.1`外, 通常还有一个`192.168.*.*`的局域网IP, 如果像上面那样使用`-i`参数, 就不能用`127.0.0.1`来访问站点了. 对于有公网IP的主机, 如果您指定一个局域网IP作为`-i`参数的值, 那么就无法通过公网来访问站点.

## 写作

执行下列命令来创建一篇新文章.

```bash
hexo new [layout] {title}
```

您可以在命令中指定文章的布局（layout）, 默认为 `post`, 可以通过修改 `_config.yml` 中的 `default_layout` 参数来指定默认布局. 

### 布局(Layout)

Hexo 有三种默认布局: `post`, `page` 和 `draft`, 它们分别对应不同的路径, 而您**自定义**的其他布局和 `post` 相同, 都将储存到 `source/_posts` 文件夹. 

|布局 | 路径 |
|-----|------|
|post | source/_posts |
|page  | source |
|draft | source/_drafts |

> 不要处理我的文章
> 
> 如果你不想你的文章被处理(不发布), 你可以将 `Front-Matter` 中的 `layout:` 设为 `false` . 


### 文件名称

Hexo 默认以标题做为文件名称, 但您可编辑 `new_post_name` 参数来改变默认的文件名称, 举例来说, 设为 `:year-:month-:day-:title.md` 可让您更方便的通过日期来管理文章. 

|变量 | 描述 |
|-----|------|
|:title |  标题（小写, 空格将会被替换为短杠） |
|:year  |建立的年份, 比如,  2015 |
|:month |  建立的月份（有前导零）, 比如,  04 |
|:i_month |  建立的月份（无前导零）, 比如,  4 |
|:day   |建立的日期（有前导零）, 比如,  07 |
|:i_day |  建立的日期（无前导零）, 比如,  7 |

### 草稿

刚刚提到了 Hexo 的一种特殊布局: `draft`, 这种布局在建立时会被保存到 `source/_drafts` 文件夹, 您可通过 `publish` 命令将草稿移动到 `source/_posts` 文件夹, 该命令的使用方式与 `new` 十分类似, 您也可在命令中指定 `layout` 来指定布局. 

```bash
hexo publish [layout] {title}
```

草稿默认**不会显示**在页面中, 您可在执行时加上 `--draft` 参数, 或是把 `render_drafts` 参数设为 `true` 来**预览草稿**. 

### 模版(Scaffold)

在新建文章时, Hexo 会根据 `scaffolds` 文件夹内相对应的文件来建立文件, 例如：

```bash
hexo new photo "My Gallery"
```

在执行这行指令时, Hexo 会尝试在 `scaffolds` 文件夹中寻找 `photo.md`, 并根据其内容建立文章, 以下是您可以在模版中使用的变量：


| 变量 | 描述 |
|------|------|
| layout | 布局 |
| title | 标题 |
| date  | 文件建立日期 |


## 发布

Hexo 提供了快速方便的一键部署功能，让您只需一条命令就能将网站部署到服务器上。

```
hexo deploy
```

在开始之前，您必须先在 `_config.yml` 中修改参数，一个正确的部署配置中至少要有 `type` 参数，例如：

```yaml
deploy:
  type: git
```

您可同时使用多个 deployer，Hexo 会依照顺序执行每个 deployer。

```yaml
deploy:
- type: git
  repo:
- type: heroku
  repo:
```

> 缩进
>
> YAML依靠缩进来确定元素间的从属关系。因此，请确保每个deployer的缩进长度相同，并且使用空格缩进。

### Git

#### GH仓库

需要在 [Github][git-new] 中创建一个名为 `<username>.github.io` 的仓库, 
用于存放 Github Pages 用到的静态网站文件.

#### 发布配置

安装 [hexo-deployer-git][hexo-dpler].


```bash
npm install hexo-deployer-git --save
```

修改配置.

```yaml
deploy:
  type: git
  repo: https://github.com/<username>/<username>.github.io.git
  branch: [branch]
  message: [message]
```

| 参数 | 描述|
|------|-----|
| repo  | 库（Repository）地址, 将 `<username>` 替换为您自己的用户名 |
| branch | 分支名称. 如果您使用的是 GitHub 或 GitCafe 的话, 程序会尝试自动检测 |
| message | 自定义提交信息 (默认为 `Site updated: 'YYYY-MM-DD HH:mm:ss's`) |


> 如果访问 `<username>.github.io` 出现404时
> 请到仓库设置`https://github.com/<username>/<username>.github.io/settings` 中修改主题(Choose a Theme).

#### 发布

编写好文章后, 执行下列命令即可发布至GH:

```bash
hexo clean
hexo generate
hexo deploy
```


其他类型的部署可以参照 [原文][hexo-dpl]

[hexo]: https://hexo.io/
[hexo-doc]: https://hexo.io/zh-cn/docs/
[hexo-issue]: https://github.com/hexojs/hexo/issues
[hexo-conf]: https://hexo.io/zh-cn/docs/configuration
[hexo-wrt]: https://hexo.io/zh-cn/docs/writing
[hexo-thm]: https://hexo.io/zh-cn/docs/themes
[hexo-dpler]: https://github.com/hexojs/hexo-deployer-git
[hexo-dpl]: https://hexo.io/zh-cn/docs/deployment.html
[hexo-except]: https://blog.csdn.net/chwshuang/article/details/52350559
[njs]: http://nodejs.org/
[git]: http://git-scm.com/
[npm]: https://www.npmjs.com/
[ejs]: http://embeddedjs.com/
[stylus]: http://learnboost.github.io/stylus/
[md]: http://daringfireball.net/projects/markdown/
[git-new]: https://github.com/new
