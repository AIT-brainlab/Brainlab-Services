This Repository store knowledge, step, guide, and reference of AIT Brainlab Jupyterhub implementation.

Our current implementation (as of this commit) uses `Jupyterhub` with `dockerspawner` to spawner Docker container. The authentication is done with the `openLDAP`. And, user's work is stored via `NAS`.

This document is separate the knowledge for those who want to replicate the work we have done (admin) and for those who want to use the system (user).

- [Topology](#topology)
- [For Jupyterhub User](#for-jupyterhub-user)
  - [Eligibility](#eligibility)
  - [Get a credential](#get-a-credential)
  - [The first thing to do once the credential is received](#the-first-thing-to-do-once-the-credential-is-received)
  - [Accessing Jupyterhub](#accessing-jupyterhub)
  - [SSH to servers](#ssh-to-servers)
    - [Bob's case (intranet)](#bobs-case-intranet)
    - [Alice's case (Internet)](#alices-case-internet)
    - [SSH to containers](#ssh-to-containers)
    - [Passwordless SSH to Servers/Containers](#passwordless-ssh-to-serverscontainers)
- [For Jupyterhub Admin](#for-jupyterhub-admin)

# Topology
  
As mentioned above, the current implementation of `Jupyterhub` uses `dockerspawner` to create a container for each user, uses `NAS` to store the user's `home` where `/.ssh` and `/work` are mapped to the container, and uses `LDAP` for authorization and provisioning.

The topology below is a typical view of `jupyter` users.

![](imgs/topology-jupyterhub.png)

When a user accesses the service, `Jupyterhub` will handle the preliminary procedure, which is authentication and container creation. At authentication, users provide their a credential (username and password) which `Jupyterhub` will validate with the `LDAP`. If the credential is correct, `LDAP` returns the user's information needed for container creation. The list of available docker images is shown. The container creation spawns a container base on the selected image, map `/.ssh`, `/work` from the user's `home` directory which is provided from `NAS` (We choose not to map `~` to prevent conflict from different kernels), and map SSH port (provisioning from `LDAP`). Once the container is spawned, `Jupyterhub` sends users a cookie for accessing the container. Thus, the user is no longer needed to contact `Jupyterhub`

This implementation provides the benefits we are seeking for.
1. It encourages experimenting with libraries.
2. Each user is isolated from the other.
3. We can give them `sudo` privilege under their container.
4. Works are stored in `NAS`. Thus, `Jupyter` service has redundancy. 

# For Jupyterhub User

## Eligibility

If you are a member of AIT Brainlab, you are eligible.

## Get a credential

Please contact the system admin for a credential.

## The first thing to do once the credential is received

You should SSH to `Cairo` (Read [SSH to servers](#ssh-to-servers)). By login to `Cairo`, the system creates your `home` directory. Then, you should create your `/work` and `/.ssh` now.

```sh
mkdir ~/work
mkdir ~/.ssh
chmod 700 ~/.ssh
```

(If you miss this step, these folders will be created by `root` during container creation. Thus, these folders will be owned by `root` not you.)

While you are here, you should reset your password too.

```sh
passwd
```

## Accessing Jupyterhub

`Jupyterhub` is served in both [`LA`](https://la.cs.ait.ac.th) and  [`Tokyo`](https://tokyo.cs.ait.ac.th). 


## SSH to servers

> **Basic Networking**
>
> There are various terms we used for referencing which network we are talking about. *Internet* is the term we use for referencing the outside/global/public network where the services such as `Google`, `Facebook`, `Youtube`, `TikTok` are served. *Intranet* is for referencing inside/local/private network. For example, dorm network, home network, and CSIM network are considered to be private network. Thus, they are intranet. **In general, the service from the intranet can not be accessed from the internet**
>
> Our CSIM network IP is [`192.41.170.0`](https://en.ipshu.com/ip_d_list/192.41.170) which is a public IP range. Then why do we say CSIM network is private. This is because we have a firewall in between CSIM network and the internet. Thus, there is a control who can access what. `Puffer`, `LA`, and `Tokyo` can be accessed from the internet because the firewall allowed any `http` (80) and `https` (443) to go through.

![](imgs/topology-service.png)

There are two scenarios. From the image above, we have `Alice` and `Bob`. `Alice` is outside of the CSIM building, hence `Alice` is accessing the CSIM network through the internet. `Bob` works at the CSIM building, hence `Bob` accessing the services within the intranet.

### Bob's case (intranet)

Since there is no firewall in the intranet, `Bob` can `SSH` to any servers directly. Here is the command.

```sh
ssh <username>@<server_name>
```

You replace `<username>` with the username provided by our lab and replace the `<server_name>` with the server's name.

server's names are
- la.cs.ait.ac.th
- tokyo.cs.ait.ac.th
- cairo.cs.ait.ac.th

> **Fun fact**
>
> When you are in the CSIM network, you can use alias name instead of full server name. For instance, you can use `la` instead of `la.cs.ait.ac.th`.

### Alice's case (Internet)

Unlike `Bob`, `Alice` can not access servers directly. The only way `Alice` can access the server is through the `bazooka` server. Essentially, `Alice` has to SSH to the `bazooka` first, then SSH to other servers.

```sh
ssh <stid>@bazooka.cs.ait.ac.th
# Login with CSIM account
ssh <username>@<serve_rname>
# Login with Brainlab Account
```

If you hate to type the command twice, you can use `Proxy` option. [ref](https://www.cyberciti.biz/faq/linux-unix-ssh-proxycommand-passing-through-one-host-gateway-server/)

```sh
# ProxyJump
ssh -J <stid>@bazooka.cs.ait.ac.th <username>@<serve_rname>
# Login with CSIM account
# Login with Brainlab Account
```

```sh
# ProxyCommand
ssh -o ProxyCommand="ssh -W %h:%p <stid>@bazooka.cs.ait.ac.th"  <username>@<serve_rname>
# Login with CSIM account
# Login with Brainlab Account
```

```sh
# -tt option
ssh -tt <stid>@bazooka.cs.ait.ac.th ssh -tt <username>@<serve_rname>
# Login with CSIM account
# Login with Brainlab Account
```

If you hate to type password, you have to use public/private key authentication.

### SSH to containers

You have to read [SSH to servers](#ssh-to-servers) first.

Let's assume that you have spawned your container in `Tokyo`. At this point, the container SSH port is the last 5 digits of your student id. For instance, if the student id is st123456, the SSH port is `23456`. In addition, other students are also working in `Tokyo` too. Their student is might be st120001 and st120002 so the ports are `20001` and `20002`.

At this point, the `Tokyo` SSH ports are the following
- 22 (default) - SSH to `Tokyo`
- 20001 (student A) - SSH to the container of student A
- 20002 (student B) - SSH to the container of student A
- 23456 (you) - SSH to your container

Therefore, you have to specify a port number when you are SSH to `Tokyo` otherwise the default `22` is used (which you will end up in `Tokyo` server instead).

However, there is no password inside the container (when you use `sudo`, it just runs without asking for a password). Thus, the only way to SSH to containers is you need to do public/private key authentication.

### Passwordless SSH to Servers/Containers



# For Jupyterhub Admin