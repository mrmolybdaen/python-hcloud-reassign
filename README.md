# python-hetzner-reassign

The Hetzner API currently does not provide fine-grained access controls for its API. You either have an access token
which can only read information or have an access token which can write (including deletion) an entire project.
This situation makes it necessary that servers using things like `keepalived` for automatic fail-over do not know the API
credentials.
This project aims to provide:
- Scrips for `keepalived` to start CI/CD pipelines
- A Python library and a script for resource reassignment
- CI/CD templates for Gitlab CI/CD, Jenkins, Tekton and Github Workflows.

> **INFO**
> We focus on open platforms such as Gitlab, Jenkins and Tekton.

The library will be provided for different package managers:
- Alpine Package Manager
- Debian Package Manager/APT
- Python via PIP/PyPI
- RedHat Package Manager

See below for further information.

## Installation

The templates provided in this project will install the library on every run. If you like to speed up things, fix a version
or simpy build your own images, or if you prefer to use another environment, you can install yourself.

This project will try to provide the script for at least two (long-term supported) versions of each platform.
We do not aim RHEL or Ubuntu Extended Support which would mean to provide compatibility over a decade.

### PyPI/PIP

The most prominent way would be using PyPI and pip:

```shell
> pip install hcloud_reassign
> hcloud-reassign --version
```

### Debian package

The Debian package is resided in a public repository.

Configure the sources list and repository key as following:
```shell
```

Afterwards install the package:
```shell
> sudo apt update
> sudo apt install hcloud-reassign
```

### Alpine

### RedHat based distributions

## Usage

The script needs an INI formatted configuration file given by `--config`.

A `[client]` section is mandatory to configure the client.
To configure resources you can add as many sections as you want. To specify the function used for reassignment, you need
to define a type. The following types exist:
- `ip_floating`
- `ip_public`
- `routes`

IP addresses in private networks cannot get assigned. Addresses are set either manually or via Hetzner DHCP which cannot
be controlled via API.

Hetzner API tokens are bound to a project. So there is no need to specify a project. However, this also means, one needs
to provide different configuration files for different projects.

Resource names are unique per project. This is why we do not use UIDs. 

```ini
[client]
api_url=<optional|Hetzner API URL>
api_token=<optional|API Token, can be omitted if --token was specified>

; Floating ip addresses - change the assigned VM
[floating.NAME]
type=ip_floating
resource=floating-test-01
source=srv-test-01
destination=srv-test-02

; For primary ip addresses as described by Hetzner
; Warning: Reassigning primary IP addresses will result in reboots!
; One cannot add more than one primary ip. 
; There is no such thing like secondary ip addresses in the Hetzner Cloud.
[public.NAME]
type=ip_public
resource=public-test-01
source=
destination=

; For routes
; Reassigning/changing routes means, changing the specified gateway.
; This is mostly relevant for outbound traffic. Be aware that changing the standard gateway
; means not to reassign the route, but deleting the old one and 
[route.NAME]
type=route
network=0.0.0.0/0
source=10.0.0.1
destination=10.0.0.2
```

## Constrains

This projects aims at smaller projects with a need for higher availability and downtime minimization.
Larger projects might make use of DNS APIs and DNS roundrobin instead.

If a server goes down and keepalived kicks in for reassignment, the downtime will last longer due to pipeline creation.
This usually needs about a minute or two to fully run small scripts.

## Contributing

### Pre-Commit hooks

Please use pre-commit!
The project provides a conifguration file for pre-commit hooks. This way you can only commit changes which fulfill some
standards such as linters oder code styles.
Fully fledged automated testing will run in a CI/CD pipeline.

```shell
> pip install pre-commit
> pre-commit install
```

### Commit messages

Use small commits and human-readable and human understandable commit messages. Cherry-picking from commits needs
explanation and not a messages "Cherrypick <commit hash 1> to <commit hash 2>" or something like that.
A good source is:
- https://py-pkgs.org/07-releasing-versioning.html
and especially:
- https://py-pkgs.org/07-releasing-versioning.html#automatic-version-bumping


### CHANGELOG

The changelog leaves Python territory. We use a Debian format to only write it ones.
The changelog will not reflect every commit but the important changes. (Bug fixes, Features, Version bumps)
