---
title: 数据库升级
id: db-upgrade
---

# 数据库升级

本节介绍了 KWDB 数据库在不同部署方式下的升级方法，包括使用部署脚本、编译版本及容器镜像部署的升级流程。升级前请务必仔细阅读相关注意事项，并根据实际部署方式选择合适的升级方案。

## 使用部署脚本升级

由于 3.0 版本进行了重大架构重构，现有的 1.x 和 2.x 版本**无法直接升级**至 3.0 版本。

推荐升级方案：

1. 部署全新的 3.0 版本
2. 通过数据导出导入功能完成版本迁移

具体操作步骤，参见[数据导出](../db-administration/import-export-data/export-data.md)和[数据导入](../db-administration/import-export-data/import-data.md)。

## 编译版本升级

对于从源代码编译安装的 KWDB 实例，可以通过编译新版本源代码的方式进行升级。这种升级方式适用于有特殊定制需求的用户，但需要用户具备一定的编译和部署能力。

### 前提条件

- 已完成数据和配置备份
- 已下载新版本的[源代码](https://gitee.com/kwdb/kwdb)
- [编译环境和相关依赖](https://gitee.com/kwdb/kwdb#%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F%E5%92%8C%E8%BD%AF%E4%BB%B6%E4%BE%9D%E8%B5%96)满足 KWDB 要求

### 步骤

1. 按照 [KWDB 编译文档](https://gitee.com/kwdb/kwdb#%E7%BC%96%E8%AF%91%E5%92%8C%E5%AE%89%E8%A3%85)编译新版本。
2. 使用与原版本相同的[启动命令](../tool-command-reference/client-tool/kwbase-sql-reference.md#kwbase-start)启动服务。
3. 验证服务是否正常运行。

## 容器镜像部署升级

使用 Docker 容器镜像部署的 KWDB 实例，可以通过更新容器镜像的方式进行升级。具体升级方式包括 Docker Compose 升级和 Docker Run 升级。

### Docker Compose 升级

#### 前提条件

- 已完成数据和配置备份
- 已获取新版本容器镜像

#### 步骤

1. 加载新版本容器镜像：

   ```bash
   docker load < KaiwuDB.tar
   ```

2. 停止并移除现有容器：

   ```bash
   docker-compose down
   ```

3. 删除旧版本镜像：

   ```bash
   docker rmi ${image_name}
   ```

4. 修改 `docker-compose.yml` 文件，更新镜像版本。

5. 启动新版本 KWDB。

   ```bash
   docker-compose up
   ```

### Docker Run 升级

#### 前提条件

- 已完成数据和配置备份

#### 步骤

1. 停止 KWDB 容器。容器名称为运行容器时通过 `--name` 参数指定的容器名称。

   ```bash
   docker stop kwdb-container
   ```

2. 删除容器。

   ```bash
   docker rm kwdb-container
   ```

3. 获取新版本镜像。

   - 从镜像仓库拉取：

     ```bash
     docker pull kwdb/kwdb:<新版本号>
     ```

   - 从本地文件导入：

     ```bash
     docker load < KaiwuDB.tar
     ```

4. 启动新版本容器。注意：除镜像名称外，所有参数应与原容器保持一致。

   - 非安全模式:

     ```bash
     docker run -d --privileged --name kwdb \
         --ulimit memlock=-1 \
         --ulimit nofile=$max_files \
         -p $db_port:26257 \
         -p $http_port:8080 \
         -v /var/lib/kaiwudb:/kaiwudb/deploy/kwdb-container \
         --ipc shareable \
         -w /kaiwudb/bin \
         <kwdb_image> \
         ./kwbase start-single-node \
         --insecure \
         --listen-addr=0.0.0.0:26257 \
         --http-addr=0.0.0.0:8080 \
         --store=/kaiwudb/deploy/kwdb-container
     ```

   - 安全模式:

     ```bash
     docker run -d --privileged --name kwdb \
         --ulimit memlock=-1 \
         --ulimit nofile=$max_files \
         -p $db_port:26257 \
         -p $http_port:8080 \
         -v /etc/kaiwudb/certs:<certs_dir> \
         -v /var/lib/kaiwudb:/kaiwudb/deploy/kwdb-container \
         --ipc shareable \
         -w /kaiwudb/bin \<kwdb_image> \
         ./kwbase start-single-node \
         --certs-dir=<certs_dir> \
         --listen-addr=0.0.0.0:26257 \
         --http-addr=0.0.0.0:8080 \
         --store=/kaiwudb/deploy/kwdb-container
     ```