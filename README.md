# 山下隆義 個人ホームページ — GitHub Pages版

公開先（初回公開後）: **https://tktkymym.github.io/**  
リポジトリ名: **tktkymym.github.io**

日本語・英語のプロフィールと研究業績ページです。論文266件（2020〜2026年の国内学会・研究会を含む）、トップページの紹介論文12件、旧業績308件を収録し、薄い青とグレーの配色を採用しています。ICPR 2026 **Best Industry Related Paper Award**を受賞欄と対象論文に掲載しています。

## 初回の公開

1. GitHubの `tktkymym` アカウントに、`tktkymym.github.io` というリポジトリを作成します。GitHub Freeで公開する場合はPublicにします。
2. このフォルダの**中身**をリポジトリの `main` ブランチへアップロードします。`build.py`、`content`、`dist`、`.github` がリポジトリ直下になるようにしてください。`.github/workflows/pages.yml` も必ず含めます。
3. リポジトリの **Settings → Pages → Build and deployment → Source** で **GitHub Actions** を選択します。
4. **Actions → Publish website → Run workflow** から `main` を指定して実行します。
5. 処理が成功すると https://tktkymym.github.io/ で公開されます。Actionsの実行結果にも公開URLが表示されます。

以後は `main` ブランチへの変更を保存・pushするたびに、HTMLの生成とGitHub Pagesへの公開が自動で行われます。サイトの表示にサーバー側のPythonやNode.jsは必要ありません。

## 今後の更新

| 編集内容 | ファイル |
| --- | --- |
| 論文の追加・修正 | `content/publications.json` |
| 詳細略歴・受賞歴 | `content/profile-records.json` |
| 過去の業績 | `content/archive.json` |
| 本文・構成・日英の紹介文 | `build.py` |
| 配色・レイアウト・検索動作 | `dist/assets/` のCSS・JavaScript |
| 情報の出典 | `SOURCES.md` |

論文には `id`、`title`、`authors`、`venue`、`year`、`type`、`category`、`url`、`sources` を指定します。`type` は `journal` / `conference` / `workshop`、`category` は `vision` / `driving` / `learning` / `biology` です。トップページに掲載する論文には、表示順を表す正の整数を `featured` に指定します。概要は `summary_ja` / `summary_en`、受賞名は `award` に記載できます。

受賞欄の見出しなど、トップページに直接表示する文章は `build.py` にあります。受賞歴を追加する場合は、必要に応じてこちらも更新してください。

## ローカルでHTMLを生成する

Python 3.9以降で、追加パッケージを入れずに実行できます。GitHub ActionsではPython 3.13を使用します。

```bash
python3 build.py
```

生成先は `dist/index.html`、`dist/index_e.html`、`dist/publications.html`、`dist/publications_e.html` です。`dist/index.html` をブラウザで開いて内容を確認できます。

`dist/assets` はCSS・JavaScript・画像の元ファイルです。`dist` フォルダ全体を削除したり、Gitの追跡対象から外したりしないでください。生成済みHTMLを直接編集しても、次回のビルドで上書きされるため、更新には上記の生成元を使います。

## 公開URLを変更する場合

通常は設定不要です。ActionsがGitHub Pagesの公開URLを取得し、canonical・日英の代替ページURL・OGP・構造化データに反映します。別名のプロジェクトリポジトリやカスタムドメインにも対応できます。

手元で別の公開先向けに生成する場合は、`SITE_URL` を指定します。

```bash
SITE_URL=https://tktkymym.github.io/profile/ python3 build.py
```

値は `http://` または `https://` で始まる絶対URLとし、検索パラメーター、フラグメント、認証情報を含めないでください。末尾の `/` は自動で補います。未指定の場合は https://tktkymym.github.io/ を使います。

## 公式ドキュメント

- [GitHub Pagesの公開元の設定](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [GitHub Pagesのカスタムワークフロー](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Python環境の設定](https://github.com/actions/setup-python)

この一式にはGitHubへの公開設定と生成済みHTMLが含まれます。GitHubへのアップロードや初回公開は、上記の手順で実行してください。
