---
title: KWDB 文档贡献指南
id: CONTRIBUTING
---

# KWDB 文档贡献指南

本仓库包括 KWDB 的用户手册。

## 文档位置

目前，所有用户文档均位于 [`kwdb/docs`](https://gitee.com/kwdb/docs) 仓库。

## 我可以为 KWDB 文档做什么贡献？

你可以在提升 KWDB 文档质量、易用性、维护效率等方面做贡献，比如：

- 提交 Pull Request (PR) 更新过时内容。
- 提交 PR 补充缺失内容。
- 提交 PR 修正文档格式，如标点、空格、缩进、代码块等。
- 提交 PR 改正错别字。
- 回复或解决文档 Issue 并提 PR 更新相关文档。
- 评审其他贡献者的 PR。

## 如何贡献

### 所需工具

- 安装 [Git](https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git)。

### 提交 Issue

欢迎在 [KWDB 文档仓库](https://gitee.com/kwdb/docs/issues)中提交 Issue，我们将不胜感激！提交 Issue 时，请提供以下必要信息：

- 问题摘要
- 文档版本信息（如果有）
- 建议改进的措施（如果有）

如果你愿意，欢迎提交 Pull Request 来修复问题。有关如何提交 Pull Request 的详细信息，参见[提交 Pull Request](#提交-pull-request)。

### 提交 Pull Request

如需为 KWDB 文档提交 PR，遵循以下步骤。

1. 首次在本仓库提 PR 时，请务必签署 [Contributor License Agreement (CLA)](https://gitee.com/organizations/kwdb/cla/kwdb-contributor-protocol)，否则我们将无法合并你的 PR。成功签署 CLA 后，可继续进行后续操作。
2. Fork `kwdb/docs` 文档仓库。
    1. 打开 [`kwdb/docs` 文档仓库](https://gitee.com/kwdb/docs)。
    2. 单击右上角的 [Fork](https://gitee.com/kwdb/docs#) 按钮，等待 Fork 完成即可。
3. 将 Fork 的仓库克隆至本地。

    ```shell
    cd $working_dir # 将 $working_dir 替换为你想要放置 KWDB 文档仓库的目录。
    git clone https://gitee.com/$user/kwdb/docs.git # 将 `$user` 替换为你的 Gitee ID
    ```

4. 新建一个分支。

    1. 确保本地 master 分支与远程分支保持最新。

        ```shell
        cd $working_dir/docs
        git fetch origin
        git checkout master
        git rebase origin/master
        ```

    2. 基于 master 分支创建一个分支。

        ```shell
        git checkout -b new-branch-name
        ```

5. 编辑文档。

    在建好的 `new-branch-name` 分支上编辑文档，可使用 Markdown 编辑器（如 Visual Studio Code）打开 `docs` 仓库，对相应文档进行增、删，或修改，并保存你的修改。

6. 提交文档修改。

    ```shell
    git status # 查看更新的文档
    git add <file> ... # 如果你想提交所有的文档修改，可直接使用 `git add .` 或者 `git add -A`
    git commit -m "commit-message: update the xx"
    ```

7. 保持新建分支与远程 master 分支保持一致。

    ```shell
    # 在新建分支上（new-branch-name）
    git fetch origin
    git rebase origin/master
    ```

8. 将文档修改推至远程分支。

    ```shell
    git push origin new-branch-name # 也可以使用 `git push -u origin new-branch-name`
    ```

9. 创建一个 PR。

    在提交 PR 前，确保已经完成 [PR 检查清单](#pr-检查清单)。

    1. 打开 [Fork 的仓库](https://gitee.com/$user/kwdb/docs)（将其中的 `$user` 替换为你的 Gitee ID），然后单击 **Pull Requests** 页签。
    2. 单击**新建 Pull Request**，在弹出的页面选择源分支（`new-branch-name`）和目标分支、填写 PR 标题和描述信息。
    3. 单击**创建 Pull Request**。

## 参考信息

### PR 检查清单

在提交 (Submit) PR 之前，请务必检查以下内容：

- 文档内容准确、清晰、简洁，遵循写作规范。有关详细信息，参见 [KWDB 文档写作风格与规范](./style-guide.md)。
- PR 的各元素完整、准确，包括：
  - 标题清晰、有意义，包括修改的类型和文档所属的模块，例如 `Fix typos in product-intro.md`。
  - 具有简要描述，例如修改背景等，并添加对应的 Issue ID（如果有）。
- 如果新增、删除文档，需同时更新 `config.ts` 文档。**注意**，请谨慎删除文档，可能会引起不必要的链接失效问题。
- 预览文档，确保文档格式正确、清晰、可读，特别注意表格、图片、列表等特殊样式能够正常显示。
