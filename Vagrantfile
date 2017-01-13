# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "bento/ubuntu-14.04"
  config.vm.synced_folder "./", "/opt/redash/current"
  config.vm.network "forwarded_port", guest: 8080, host: 9001
  config.vm.provision "shell" do |s|
    s.inline = "/opt/redash/current/setup/vagrant/provision.sh"
    s.privileged = false
  end
end
