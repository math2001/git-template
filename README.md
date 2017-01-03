# My git template

<!-- MarkdownTOC -->

- [What is this?](#what-is-this)
- [Installation](#installation)
    - [Requirements](#requirements)
- [Usage](#usage)
- [Template](#template)
    - [CSW - Check Stdout Writers](#csw---check-stdout-writers)

<!-- /MarkdownTOC -->

## What is this?

This repo is a template that I use for my project. Here's what it does:

```commandline
$ git init
Reinitialized existing Git repository in C:/wamp/www/tests/git-tests/testr/.git/
$ git populate
$ ls -R -A
.:
.git/  .gitignore  README.md

./.git:
HEAD  config  description  hooks/  info/  objects/  refs/

./.git/hooks:
applypatch-msg.sample*  commit-msg.sample*   pre-applypatch.sample*  pre-commit.sample*  pre-rebase.sample*   prepare-commit-msg.sample*  update.sample*
commit-msg*             post-update.sample*  pre-commit*             pre-push.sample*    prepare-commit-msg*  py/

./.git/hooks/py:
check-stdout-writers.py*  prepare-commit-msg.py*  validate-commit-message.py*

./.git/info:
exclude

./.git/objects:
info/  pack/

./.git/objects/info:

./.git/objects/pack:

./.git/refs:
heads/  tags/

./.git/refs/heads:

./.git/refs/tags:
```

As you can see, there is a few hooks, and I have the `populate` command, which if you try, is going to yell at you, saying that there is no such command :laughing:


## Installation

Download this packages wherever you want, say in `~/git-template`

```bash
# set your template dir (will only affect the content of the .git)
$ git config --global --set init.templateDir "~/git-template/content"
# set the path to .py who's going to populate your repo content (README, .gitignore)
$ git config --global init.populater "~/git-template/content/populatr.py"

# set the alias 'git populate' to run the populater
$ git config --global alias.populate "!python $(git config --get init.populater) $(git config --get init.templateDir)/../root-content"

```

### Requirements

To use this package, you need to have Python (I'm using python 3.4) on your system, and the `python` command available in your terminal

## Usage

## Template

If you want to change the template of the `.git`, change the content of the `content` folder. This is useful if you want to add some hooks for example. This is used when you run `git init`.

On the opposite side, if you want to edit what's outside of the `.git` folder, edit the content of the `root-content`  folder. This is useful if you want to automatically create a `README.md`, a `.gitignore`. This is used when you run `git populate`.

> !! Watch out! When you run `git populate`, all the content of `root-content` **overwrites** the content of your repository.

### CSW - Check Stdout Writers

This hook (`.git/hooks/py/check-stdout-writers.py`) checks that you haven't left a `print` in your python files, a `console.log` in your js, etc.

#### Escaping

You can escape an SW by making sure there is, in the line just above, this: `CSW: ignore`

```js
if (language == 'js') {
    language = 'javascript'
}
// CSW: ignore
console.log('I dont block your commit')

console[log]('me either!')

console.log('But I do')
```

If you want to escape the entire file, make sure that in the *first* or *second* line, there is this: `CSW: ignore *`

```python
# CSW: ignore *

print('not blocking')

print('me either')

print('great!')
```
