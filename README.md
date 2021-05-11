About
-----

Package Nexus IQ Server as an RPM and DEB.

(You may also be interested in the [Nexus Repository Manager 3 installer](https://github.com/sonatype-nexus-community/nexus-repository-installer) project.)

[![CircleCI Build Status](https://circleci.com/gh/sonatype-nexus-community/nexus-iq-server-installer.svg?style=shield "CircleCI Build Status")](https://circleci.com/gh/sonatype-nexus-community/nexus-iq-server-installer) 

Usage
--------

Prebuilt binaries of these installers are available from the community 
[Yum](https://repo.sonatype.com/#browse/browse:community-yum-hosted) and 
[Apt](https://repo.sonatype.com/#browse/browse:community-apt-hosted) repositories. 

The [community-hosted](https://repo.sonatype.com/#browse/browse:community-hosted) repository provides example 
Yum configuration (`sonatype-community.repo`) and Apt configuration (`sonatype-community.list`) files, 
and related public keys under the `pki` folder.

#### Yum setup

  1. (One-time setup) Copy the Yum configuration file: [sonatype-community.repo](https://repo.sonatype.com/repository/community-hosted/rpm/sonatype-community.repo)
     to your `/etc/yum.repos.d/` directory.
     
     Or automatically:

         sudo wget -P /etc/yum.repos.d/ https://repo.sonatype.com/repository/community-hosted/rpm/sonatype-community.repo

  2. Install the application via yum. The first time you use our installer, you will be prompted to install the GPG signing key.

         yum install nexus-iq-server
              
#### Apt setup

  1. (One-time setup) Copy the Apt configuration file: [sonatype-community.list](https://repo.sonatype.com/repository/community-hosted/deb/sonatype-community.list)
     to your `/etc/apt/sources.list.d/` directory.
     
     Or automatically:
     
         sudo wget -P /etc/apt/sources.list.d/ https://repo.sonatype.com/repository/community-hosted/deb/sonatype-community.list
         
  2. (One-time setup) Download the [public GPG signing key](https://repo.sonatype.com/repository/community-hosted/pki/deb-gpg/DEB-GPG-KEY-Sonatype.asc)
     and add the key to your apt sources keyring:
     
         wget https://repo.sonatype.com/repository/community-hosted/pki/deb-gpg/DEB-GPG-KEY-Sonatype.asc
         sudo apt-key add DEB-GPG-KEY-Sonatype.asc
  
  3. Install the application via apt-get.

         sudo apt-get update && sudo apt-get install nexus-iq-server         

Overview
--------

Make is used to download the application bundle from Sonatype, populate an RPM build
environment, and invoke `rpmbuild`.
You can specify the bundle version to download by setting the `VERSION` environment variable. 
The RPM will be written to `./build`.

The DEB is generated from the RPM using the [alien](https://wiki.debian.org/Alien) command in another docker container.
This is why you will see a number of `elif` commands in the `%pre`, `%post`, and `%preun` sections of the [.spec](rpm/nexus-iq-server.spec) file,
to ensure the scriptlets work on both distributions. 
The DEB will be written to `./build`. 

Examples:

Build the RPM locally (requires linux tooling).  The RPM will be written to `build/`.

```
$ make build
$ VERSION=1.65.0-01 make rpm
```

Build the RPM in a docker container.  The RPM will be written to `build/`.

```
$ make docker
$ VERSION=1.65.0-01 make docker
```

Build the RPM in a docker container and build the DEB in another container.  The RPM and DEB will be written to `build/`.

```
$ make docker-all
$ VERSION=1.65.0-01 make docker-all
```

Use the `make help` command to see more options.

Tweaks made to the Application
------------------------------

* Software installs to */opt/sonatype/iqserver*.

* The `data directory` is */opt/sonatype/sonatype-work/iqserver*.


Notes/Todo
----------

* Debug yum transaction issue after uninstall.

* Fix upgrading of daemon script (extra/daemon/nexus-iq-server) regarding version number in jar filename (`%config(noreplace)` vs `%config`).

* Use `rpmlint` to validate the generated .rpm installer.

* Use `lintian` to validate the generated .deb installer.

## The Fine Print

It is worth noting that this is **NOT SUPPORTED** by Sonatype, and is a contribution to the open source community (read: you!)

Don't worry, using this community item does not "void your warranty". In a worst case scenario, you may be asked 
by the Sonatype Support team to remove the community item in order to determine the root cause of any issues.

Remember:

* Use this contribution at the risk tolerance that you have
* Do **NOT** file Sonatype support tickets with Sonatype support related to this project
* **DO** file issues here on GitHub, so that the community can pitch in

Phew, that was easier than I thought. Last but not least of all:

Have fun building and using this item, we are glad to have you here!

## Getting help

Looking to contribute, but need some help? There's a few ways to get information:

* Chat with us on [Gitter](https://gitter.im/sonatype/nexus-developers)
* File a GitHub issue in this project.

## Debugging

* It may be helpful to run the .rpm with debug commands like the one below:

      rpm -ivvh nexus-iq-server-1.65.0_01-1.el7.noarch.rpm 
      
  This will provide tons of information about what the installer is doing.

<!--
* There are Docker files for use in testing of .rpm and .deb installers. No Joy here yet. Test in VirtualBox, et al.

      docker build -t test-rpm -f rpm/test-rpm.dockerfile . && docker run --privileged -it -v /sys/fs/cgroup:/sys/fs/cgroup:ro test-rpm /usr/sbin/init
      
      docker build -t test-deb -f deb/test-deb.dockerfile . && docker run --privileged -it test-deb
-->
        
* CI local debug - you can run a local ci build using the following:

      circleci config process .circleci/config.yml > .circleci/local-config.yml  \
          &&  circleci local execute --config .circleci/local-config.yml --job build
  

## Build Installers via CI

  1. Update the version number in [version-to-build.txt](version-to-build.txt) to the new version to be built. e.g.
  
         1.65.0-01
         
     to:
     
         1.66.0-01

     Commit and push the updated [version-to-build.txt](version-to-build.txt) file to the `master` branch.
     
  2. After a new build has completed, click the `manual_deploy` workflow.

   <!-- @todo verify manual_deploy workflow works with manual tag push. -->
