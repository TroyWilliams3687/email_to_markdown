# email_to_markdown

## Introduction

## QuickStart

1. [Install Rye](#installation-and-configuration)
2. [Installation and Configuration](#rye-sync)
3. [Activate](#activate-virtual-environment---traditional-approach)



## Installation and Configuration

To get this project up and running from the repository, it uses [Rye](https://rye-up.com) as the build/dependency manager. There are [instructions](https://rye-up.com/guide/installation/) for installing Rye on many different systems. This set of instructions are for Linux and windows. See the installation guide for other operating systems.

You have to download Rye to your system. Follow the [installation guide](https://rye-up.com/guide/installation/) for your operating system.

Why Rye? That is a good question. Python is a great language but it is tough to create a reproducible environment. You have to have the correct version of Python installed or available. You have to have the correct tools configured. If you are on Linux/BSD you have to make sure that your work doesn't mess up your system Python installation. It is fairly trivial if you are experienced, but annoying enough to have to do it over-and-over again. If you are new, it can be extremely difficult.

Rye takes care of handling the different versions of Python and managing the tools you need for a reproducible environment, particularly if you are doing cross-platform work.

### Linux

For Linux, you can use the following:

```bash
curl -sSf https://rye-up.com/get | bash
```

There are also good guides to configuring Rye for your shell. Here is what I had to do to get it working in ZSH on my system.

Edit **.zshrc**:

```bash
vi ~/.zshrc
```

Add the following:

```bash
source "$HOME/.rye/env"
```

Restart the terminal and type **rye**. To add [shell completion](https://rye-up.com/guide/installation/#shell-completion), you can:

```bash
mkdir $ZSH_CUSTOM/plugins/rye
rye self completion -s zsh > $ZSH_CUSTOM/plugins/rye/_rye
```

### Windows

For windows, download the [installer](https://github.com/mitsuhiko/rye/releases/latest/download/rye-x86_64-windows.exe) listed in the installation guide link.

## Basic Rye Usage

### Rye Update

[Update rye](https://rye-up.com/guide/installation/#updating-rye):

```bash
rye self update
```

### Rye Sync

Once you have rye properly installed, you can run [**rye sync**](https://rye-up.com/guide/commands/sync/), to build (or update) the virtual environment.

Create/Update Virtual Environment

```bash
rye sync
```

> NOTE: This needs to be run from within the repository. If you add new dependencies or modify the **pyproject.toml** you should run **rye sync**.

### Activate Virtual Environment - Traditional Approach

You can add the following alias to your **.zshrc** or **.bashrc**, or you can run the activate script directly:

```bash
# Python Virtual Environment Alias
alias activate="source .venv/bin/activate"
```

>NOTE: On Windows, there is an **activate.ps1**, a PowerShell script that you can execute.

## Usage

```bash
$ emailmd extract

$ emailmd extract ~/email/*.msg ~/email/*.eml ~/email/output

$ emailmd extract ~/"path to email"/*.msg ~/email/output

$ emailmd extract ~/tmp/"email to markdown"/eml/* ~/tmp/"email to markdown"/msg/* ~/email/output

$ emailmd extract ~/tmp/"email to markdown"/eml/* ~/tmp/"email to markdown"/msg/* ~/tmp/"email to markdown"/output

$ emailmd extract -r ~/tmp/'email to markdown'/eml/ ~/tmp/'email to markdown'/output

$ emailmd extract --recursive ~/tmp/'email to markdown'/eml/ ~/tmp/'email to markdown'/output

```


## License

Please refer to [LICENSE.md](LICENSE.md).

