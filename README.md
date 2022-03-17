# What is lpmadison? 

For anyone who uses Canonical Ubuntu, you may be familiar with the '[rmadison](https://manpages.ubuntu.com/manpages/focal/man1/rmadison.1.html)' or '[cmadison](https://snapcraft.io/cmadison)' tools, which will allow you to query repository packages or cloud packages respectively. Here are some sample outputs: 


### rmadison

```
$ rmadison -a amd64 openssh-server -s bionic,focal,jammy
 openssh-server | 1:7.6p1-4 | bionic | amd64
 openssh-server | 1:8.2p1-4 | focal  | amd64
 openssh-server | 1:8.9p1-3 | jammy  | amd64
```

### cmadison

```
$ cmadison ceph --clear-cache 
 ceph | 15.2.14-0ubuntu0.20.04.2~cloud1  | ussuri           | bionic-updates  | source
 ceph | 15.2.14-0ubuntu0.20.04.2~cloud1  | ussuri-proposed  | bionic-proposed | source
 ceph | 16.2.6-0ubuntu0.21.04.1~cloud0   | wallaby          | focal-updates   | source
 ceph | 16.2.7-0ubuntu0.21.04.1~cloud2   | wallaby-proposed | focal-proposed  | source
 ceph | 16.2.6-0ubuntu1~cloud2           | xena             | focal-updates   | source
 ceph | 16.2.7-0ubuntu0.21.04.1~cloud1   | xena-proposed    | focal-proposed  | source
 ceph | 16.2.7-0ubuntu2~cloud1           | yoga             | focal-updates   | source
 ceph | 17.1.0-0ubuntu1~cloud0           | yoga-proposed    | focal-proposed  | source
```

lpmadison is a tool I wrote to query packages _from the past_ that may no longer be available in the archives, using [Launchpad](https://launchpad.net/). 

There are many features I'll be adding soon, some are stubbed in the code already, but the invocation is very simple: 

```
$ apt -y install python3-venv
$ python3 -mvenv env
$ source env/bin/activate
$ pip install -r requirements.txt

$ ./lpmadison.py --series bionic --package libvirt-bin --arch amd64 
Package: 'libvirt'
        Version: '4.0.0-1ubuntu8.20'
        Published: '2021-12-02 12:38:29.847753+00:00'
        Days ago: 105
        https://launchpad.net/ubuntu/+archive/primary/+files/libvirt-bin_4.0.0-1ubuntu8.20_amd64.deb

Package: 'libvirt'
        Version: '4.0.0-1ubuntu8.20'
        Published: '2021-12-02 06:23:49.804205+00:00'
        Days ago: 105
        https://launchpad.net/ubuntu/+archive/primary/+files/libvirt-bin_4.0.0-1ubuntu8.20_amd64.deb

Package: 'libvirt'
        Version: '4.0.0-1ubuntu8.20'
        Published: '2021-12-02 00:43:52.239973+00:00'
        Days ago: 105
        https://launchpad.net/ubuntu/+archive/primary/+files/libvirt-bin_4.0.0-1ubuntu8.20_amd64.deb
[...]
```

This will go back as far as the search criteria has been met. You can then use this data, dates, times, URLs to reconstruct packages you need that may no longer be available in the public archives. 

I will update this README as more features and capability are added. Suggestions and PRs are always welcome! 
