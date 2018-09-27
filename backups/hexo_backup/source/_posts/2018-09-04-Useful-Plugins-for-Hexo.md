---
title: Useful Plugins for Hexo
categories:
  - Tutorial
tags:
  - Hexo
date: 2018-09-04 16:36:10
---

Useful plugins for Hexo

- hexo-deployer-git
- hexo-generator-json-feed
- hexo-generator-seo-friendly-sitemap
- hexo-generator-searchdb


<!-- more -->

## hexo-deployer-git

Git deployer plugin for Hexo.

```bash
npm install hexo-deployer-git --save
```


in `_config.yml`

```yaml
# Deployment
## Docs: https://hexo.io/docs/deployment.html
deploy:
  type: git
  repo: https://github.com/<username>/<username>.github.io.git
  branch: master
```

## hexo-generator-json-feed

[Hexo][hexo] plugin to generate a JSON file similar to RSS feed channel structure with posts contents for generic use or consumption.

```bash
npm i -S hexo-generator-json-feed
```

in `_config.yml`

```yaml
# Json feed
jsonFeed:
  limit: 25
```

## hexo-generator-seo-friendly-sitemap

Generate SEO-friendly sitemap.

Inspired by XML Sitemap in Yoast Wordpress SEO Plugin (https://yoast.com).

It will generate separated sitemap files for pages, posts, categories, tags and a XSL stylesheet.

```bash
npm install hexo-generator-seo-friendly-sitemap --save
```

in `_config.yml`

```yaml
sitemap:
  path: sitemap.xml
  tag: true
  category: true
```


## [hexo-generator-searchdb][searchdb]

Generate search data for Hexo 3.0. This plugin is used for generating a search index file, which contains all the neccessary data of your articles that you can use to write a local search engine for your blog. Supports both XML and JSON format output.

```bash
npm install hexo-generator-searchdb --save
```

in `_config.yml`

```yaml
search:
  path: search.xml
  field: post
  format: html
  limit: 10000
```

See More: [Hexo plugins][hexo-plugins].


[hexo]: https://hexo.io/
[hexo-plugins]: https://hexo.io/plugins/
[searchdb]: https://github.com/theme-next/hexo-generator-searchdb