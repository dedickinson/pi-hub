# Pi Hub orchestration

## Prepare the Pi

1. On you "main PC": Create an ssh key called `ansible`
1. On the Pi: Create a user called `ansible` and put them into the `sudo` group
1. Use `ssh-copy-id` to copy your SSH key from your PC to the Pi
1. Create the `/etc/sudoers.d/020-sudo-nopasswd` file with the line below:

    %sudo ALL=(ALL) NOPASSWD: ALL

Try to SSH into the Pi 

## Get Ansible going

Setup a Python virtual environment and install Ansible:

    make init

Test that you can connect:

    make test

## Orchestrate!

    make run