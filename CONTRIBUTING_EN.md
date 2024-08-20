---
title: KWDB Documentation Contributing Guide
id: CONTRIBUTING_EN
---

# KWDB Documentation Contributing Guide

Welcome to KWDB documentation! This repository contains all user docs about KWDB.

## Where the KWDB Docs

All KWDB user guides are located in the [`kwdb/docs`](https://gitee.com/kwdb/docs) repository.

## What You Can Contribute

You can start from any one of the following items to help improve KWDB documentation at the [KWDB documentation website](https://kaiwudb.com/kaiwudb_docs/#/):

- Fix typos or format (punctuation, space, indentation, code block, etc.).
- Fix or update inappropriate or outdated descriptions.
- Add missing content (sentence, paragraph, or a new document).
- Submit, reply to, and resolve docs issues.
- Review Pull Requests (PRs) created by others.

## How to Contribute

### Required Tools

- Install [Git](https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git).

### Submit Issues

We appreciate that you submit a doc issue and provide the following required information when submitting an issue:

- Issue description
- Doc version (if any)
- Improvement proposals (if any)

If you like, welcome to submit PRs to resolve issues. For details about how to submit a PR, see [Submit Pull Requests](#submit-pull-requests)

### Submit Pull Requests

To submit a PR for KWDB docs, follow these steps.

1. Your PRs can only be merged after you sign the [Contributor License Agreement (CLA)](https://gitee.com/organizations/kwdb/cla/kwdb-contributor-protocol). Please make sure you sign the CLA before continuing.
2. Fork the `kwdb/docs` repository.
    1. Visit the [`kwdb/docs`](https://gitee.com/kwdb/docs) repository.
    2. Click the **Fork** button on the top right and wait for it to finish.
3. Clone the forked repository to local storage.

    ```shell
    cd $working_dir # Switch to the directory that you want put the fork in, for example, "cd ~/Documents/Gitee".
    git clone https://gitee.com/$user/kwdb/docs.git # Replace "$user" with your Gitee ID.
    ```

4. Create a new branch.
    1. Ensure your local master is up-to-date with the remote master branch.

        ```shell
        cd $working_dir/docs
        git fetch origin
        git checkout master
        git rebase origin/master
        ```

    2. Create a new branch based on the master branch.

        ```shell
        git checkout -b new-branch-name
        ```

5. Edit your docs.

    Edit some file(s) on the `new-branch-name` branch and save your changes. You can use editors like Visual Studio Code to open and edit `.md` files.

6. Commit your changes.

    ```shell
    git status # Check your updated docs. 
    git add <file> ... # Adds the file(s) you want to commit. If you want to commit all changes, you can directly use `git add .` or `git add -A`.
    git commit -m "commit-message: update the xx"
    ```

7. Keep your branch in sync with the remote master branch.

    ```shell
    # on "new-branch-name" branch
    git fetch origin
    git rebase origin/master
    ```

8. Push your changes to the remote.

    ```shell
    git push origin new-branch-name # You can also use the "git push -u origin new-branch-name".
    ```

9. Create a PR。

    Before submitting your PR, ensure you have gone through the [PR checklist](#pr-checklist).

    1. Visit the forked [`kwdb/docs`](https://gitee.com/$user/kwdb/docs) repository (Replace `$user` with your Gitee ID.) and then select the **Pull Requests** tab.
    2. Click the **New Pull Request** button.
    3. At the **Create Pull Request** page, choose the source branch (`new-branch-name`) and the target branch, and add the PR title and descriptions.
    4. Click the **Create Pull Request** button.

## References

### PR Checklist

Ensure to check the following before submitting your PR:

- The content of the document is accurate, clear, concise, and follows the writing standards. For more information, see [Style Guide](./style-guide.md). 
- Elements of the PR are complete and accurate, including:
  - A clear and meaningful title, including the type of modification and the module to which the document belongs, e.g. `Fix typos in product-intro.md`.
  - A brief description, for example, the context of the change etc., with the corresponding Issue ID (if any).
- If a document is added or deleted, the `config.ts` document needs to be updated at the same time. **NOTE**: Please take care when deleting documents, as this may cause unexpected broken links.
- Preview the document to make sure it is correctly formatted, clear and readable. Pay special attention to tables, images and lists.
