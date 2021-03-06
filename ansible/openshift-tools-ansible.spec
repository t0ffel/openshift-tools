Name:           openshift-tools-ansible
Version:        0.0.22
Release:        1%{?dist}
Summary:        Openshift Tools Ansible
License:        ASL 2.0
URL:            https://github.com/openshift/openshift-tools
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:      ansible
Requires:      python2

%description
Openshift Tools Ansible

This repo contains Ansible code and playbooks
used by Openshift Online Ops.

%prep
%setup -q

%build

%install
# openshift-tools-ansible-zabbix install (standalone lib_zabbix library)
mkdir -p %{buildroot}%{_datadir}/ansible/zabbix
cp -rp roles/lib_zabbix/library/* %{buildroot}%{_datadir}/ansible/zabbix/

# openshift-tools-ansible-inventory install
mkdir -p %{buildroot}/etc/ansible
mkdir -p %{buildroot}%{_datadir}/ansible/inventory
mkdir -p %{buildroot}%{_datadir}/ansible/inventory/aws
mkdir -p %{buildroot}%{_datadir}/ansible/inventory/gce
cp -p inventory/multi_inventory.py %{buildroot}%{_datadir}/ansible/inventory
cp -p inventory/multi_inventory.yaml.example %{buildroot}/etc/ansible/multi_inventory.yaml
cp -p inventory/aws/ec2.py %{buildroot}%{_datadir}/ansible/inventory/aws
cp -p inventory/gce/gce.py %{buildroot}%{_datadir}/ansible/inventory/gce

# openshift-tools-ansible-filter-plugins install
mkdir -p %{buildroot}%{_datadir}/ansible_plugins/filter_plugins
cp -p filter_plugins/ops_filters.py %{buildroot}%{_datadir}/ansible_plugins/filter_plugins/ops_filters.py
cp -p filter_plugins/ops_zabbix_filters.py %{buildroot}%{_datadir}/ansible_plugins/filter_plugins/ops_zabbix_filters.py

# ----------------------------------------------------------------------------------
# openshift-tools-ansible-inventory subpackage
# ----------------------------------------------------------------------------------
%package inventory
Summary:       Openshift Tools Ansible Inventories
BuildArch:     noarch

%description inventory
Ansible inventories used with the openshift-tools scripts and playbooks.

%files inventory
%config(noreplace) /etc/ansible/*
%dir %{_datadir}/ansible/inventory
%{_datadir}/ansible/inventory/multi_inventory.py*


%package inventory-aws
Summary:       OpenShift Tools Ansible Inventories for AWS
Requires:      %{name}-inventory = %{version}
Requires:      python-boto
BuildArch:     noarch

%description inventory-aws
Ansible inventories for AWS used with the openshift-tools scripts and playbooks.

%files inventory-aws
%{_datadir}/ansible/inventory/aws/ec2.py*

%package inventory-gce
Summary:       OpenShift Tools Ansible Inventories for GCE
Requires:      %{name}-inventory = %{version}
Requires:      python-libcloud >= 0.13
BuildArch:     noarch

%description inventory-gce
Ansible inventories for GCE used with the openshift-tools scripts and playbooks.

%files inventory-gce
%{_datadir}/ansible/inventory/gce/gce.py*

# ----------------------------------------------------------------------------------
# openshift-tools-ansible-zabbix subpackage
# ----------------------------------------------------------------------------------
%package zabbix
Summary:       Openshift Tools Ansible Zabbix library
Requires:      python-openshift-tools-zbxapi
BuildArch:     noarch

%description zabbix
Python library for interacting with Zabbix with Ansible.

%files zabbix
%{_datadir}/ansible/zabbix

# ----------------------------------------------------------------------------------
# openshift-tools-ansible-filter-plugins subpackage
# ----------------------------------------------------------------------------------
%package filter-plugins
Summary:       Openshift Tools Ansible Filter Plugins
BuildArch:     noarch

%description filter-plugins
Ansible filter plugins used with the openshift-tools

%files filter-plugins
%dir %{_datadir}/ansible_plugins/filter_plugins
%{_datadir}/ansible_plugins/filter_plugins/ops_filters.py*
%{_datadir}/ansible_plugins/filter_plugins/ops_zabbix_filters.py*

%changelog
* Mon Sep 26 2016 Ivan Horvath <ihorvath@redhat.com> 0.0.22-1
- Adding oadm_manage_node. (kwoodson@redhat.com)
- Adding ability to perform router edits at creation time.
  (kwoodson@redhat.com)

* Thu Sep 22 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.21-1
- wrap inventory refresh in ops-runner (to post result to zabbix)
  (jdiaz@redhat.com)
- fixed a debug msg for ansible 2.2 (mwoodson@redhat.com)
- cleaned up registry cert role (mwoodson@redhat.com)

* Thu Sep 22 2016 Joel Diaz <jdiaz@redhat.com> 0.0.20-1
- shuffle files around to make local development easier (jdiaz@redhat.com)

* Tue Sep 20 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.19-1
- Added gcs monitoring. (kwoodson@redhat.com)
- Adding zabbix objects for gcp snapshotting. (kwoodson@redhat.com)
- fixing aws user role for ansible 2 (mwoodson@redhat.com)

* Fri Sep 16 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.18-1
- Fixes for labeling, snapshotting, and trimming snapshots.
  (kwoodson@redhat.com)

* Thu Sep 15 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.17-1
- fixed monitoring template (mwoodson@redhat.com)

* Thu Sep 15 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.16-1
- Fixing code for snapshots. (kwoodson@redhat.com)
- First attempt at zabbix maintenance. (kwoodson@redhat.com)
- fix a the name typo (zhizhang@zhizhang-laptop-nay.redhat.com)
- fixed debug to use a msg instead of var (mwoodson@redhat.com)
- First attempt at maintenance (kwoodson@redhat.com)
- updated some code docs (mwoodson@redhat.com)
- updated oc_label to handle selectors and multiple labels at a time
  (mwoodson@redhat.com)
- First attempt at zabbix maintenance. (kwoodson@redhat.com)
- fix a the name typo (zhizhang@zhizhang-laptop-nay.redhat.com)
- router doens't support edits yet (mwoodson@redhat.com)
- made edits to router/registry to use registry.ops (mwoodson@redhat.com)
- added config changes to registry deployer (mwoodson@redhat.com)
- fixed debug to use a msg instead of var (mwoodson@redhat.com)
- check for certs in /etc/origin/{master,node} (jdiaz@redhat.com)
- raise severity on config loop trigger to high (jdiaz@redhat.com)
- First attempt at maintenance (kwoodson@redhat.com)

* Mon Sep 12 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.15-1
- Fixing boolean strings for ansible 2.2 (kwoodson@redhat.com)
- ansible 2.2 task naming (jdiaz@redhat.com)
- Fix broken root session logrotate (joesmith@redhat.com)
- Updating from yedit to tools. (kwoodson@redhat.com)
- Adding documentation. (kwoodson@redhat.com)
- Added cgrouputil.py and changed dockerutil to be able to use it if requested.
  (twiest@redhat.com)
- Updating for 2.2. (kwoodson@redhat.com)
- changed kibana -> logs (mwoodson@redhat.com)
- Adding zabbix bits. (kwoodson@redhat.com)
- ansible 2.2 changes. (kwoodson@redhat.com)
- Fixed var name. (kwoodson@redhat.com)
- Adding types to config passed.  This caused an error in 2.2 so I'm explicitly
  setting them. (kwoodson@redhat.com)
- add steps to allow a clean system to ansible_tower role successfully
  (jdiaz@redhat.com)
- add firewalld rpm (jdiaz@redhat.com)
- no bare variables (jdiaz@use-tower2.ops.rhcloud.com)
- add Terminating project check (zhizhang@zhizhang-laptop-nay.redhat.com)
- commented out the fluentd container usage config as it's causing issues on
  some boxes and it's not required. (twiest@redhat.com)
- Added configs for cron-send-docker-containers-usage (twiest@redhat.com)
- change link for existing DNS alerts (sten@redhat.com)

* Wed Aug 31 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.14-1
- add OpenShift Cluster(wide) templates/items/triggers (jdiaz@redhat.com)
- Incorporate changes from arch meeting (rharriso@redhat.com)
- Make sure the checks aleart after the same time now that their interval has
  been increased (rharriso@redhat.com)
- Changes from Ops arch meeting (rharriso@redhat.com)
- don't need dnsmasq checks more than every 15 minutes (rharriso@redhat.com)
- Increase the interval for Zabbix checks to save on both DB load and space
  (rharriso@redhat.com)
- Added specific labels to host types. (kwoodson@redhat.com)
- have primary master heartbeat for synthetic host (jdiaz@redhat.com)
- Added cron-send-docker-containers-usage.py (twiest@redhat.com)
- Adding disk labels to deployment manager (kwoodson@redhat.com)
- changed rc to inherit from dc (mwoodson@redhat.com)
- removed comments (mwoodson@redhat.com)
- more updates to oc scale (mwoodson@redhat.com)
- more fixes for the metrics, included the copy (mwoodson@redhat.com)
- added some options to openshift ansible tools, added mem constraints for
  metrics (mwoodson@redhat.com)
- Add history and trends parameters to the zbx_item and zbx_itemprototype
  modules (rharriso@redhat.com)
- Comments to explain changes in the trigger logic (rharriso@redhat.com)
- Adding in-memory updates. (kwoodson@redhat.com)
- add triggers for iminent certificate expirations (jdiaz@redhat.com)
- add daily cron to report on certificate expirations (jdiaz@redhat.com)
- Minor fix for bool str (kwoodson@redhat.com)
- bind all of /etc/origin into host-monitoring (so we can see certificates)
  (jdiaz@redhat.com)
- fixed spelling error in volume provisioner (mwoodson@redhat.com)
- add items to hold certificate expiration data (jdiaz@redhat.com)
- add trigger and item for saml check (zhizhang@zhizhang-laptop-nay.redhat.com)
- added the openshift_volume_provisioner role (mwoodson@redhat.com)
- added urls for remaining pv check (sten@redhat.com)
- pass in cluster-wide KMS key to generated docker config (jdiaz@redhat.com)
- Fixed boolean passing as strings (kwoodson@redhat.com)
- sleep for a moment before getting newly create KMS data (jdiaz@redhat.com)
- Prune haproxy processes more aggressively (agrimm@redhat.com)
- add saml check (zhizhang@zhizhang-laptop-nay.redhat.com)
- run haproxy script every 15 minutes (jdiaz@redhat.com)
- Changed role openshift_dedicated_admin to explicitly turn off non-primary
  master dedicated-admin-role services. Added oda_config param.
  (twiest@redhat.com)
- add haproxy pruner cron job to infra nodes (jdiaz@redhat.com)
- add item to hold number of haproxy processes found in CLOSE-WAIT state
  (jdiaz@redhat.com)
- Added oda_skip_projects to the openshift_dedicated_admin role.
  (twiest@redhat.com)
- changed zabbix key for build time to match key sent by script
  (sten@redhat.com)
- enable creating encrypted PVs (jdiaz@redhat.com)
- allow tagging resulting AMI (jdiaz@redhat.com)
- add role that can be called during cluster creation (jdiaz@redhat.com)
- added the role openshift_gcp_add_users_to_project (mwoodson@redhat.com)
- role doesn't take osaik_kms_directory parameter (jdiaz@redhat.com)
- add oo_ec2_ami_copy Ansible module (jdiaz@redhat.com)
- Updating the name of the role to be more clear as to what it does
  (mwhittingham@redhat.com)
- GCP support for osohm (kwoodson@redhat.com)
- Forgot an example in the README (mwhittingham@redhat.com)
- Being more explicit about the oadm location (mwhittingham@redhat.com)
- added gcloud config ansible module, created a role with it
  (mwoodson@redhat.com)
- Initial commit (mwhittingham@redhat.com)
- use renamed oo_ec2_ami20 module (jdiaz@redhat.com)
- rename OpenShift Ops roles to prefix with oo_ ...to indicate that this is our
  module (not something pulled/backported) iam_kms cat_fact sysconfig_fact
  (jdiaz@redhat.com)
- added dnsmasq_proxy and dnsmasq_proxy_file (mwoodson@redhat.com)
- Fixes for gcp registry (kwoodson@redhat.com)
- added gcp zone getter (mwoodson@redhat.com)
- Adding gcp_compute_zones (kwoodson@redhat.com)
- added support for generic service account in gcp (mwoodson@redhat.com)
- using common kms names for each cluster (jdiaz@redhat.com)
- deal with rename of ec2_vol20 library (jdiaz@redhat.com)
- Separating registries.  Removing bucket from storage bucket name.
  (kwoodson@redhat.com)
- Fixed a bug in variable name caused by refactor. (kwoodson@redhat.com)
- add role to create and save AWS IAM KMS key data (jdiaz@redhat.com)
- Fix creating the zabbix config template (rharriso@redhat.com)
- Fixed json output format. (kwoodson@redhat.com)
- add AWS IAM KMS ansible library for creating/querying KMS entries
  (jdiaz@redhat.com)
- Have the Zabbix config run in cron and report results to Zabbix
  (rharriso@redhat.com)
- Making openshift_registry work on gcp and aws. Fixed service account keys.
  Added scopes to vminstances. (kwoodson@redhat.com)
- fixed dependency name (mwoodson@redhat.com)
- added ops_os_firewall (mwoodson@redhat.com)
- added ops_os_firewall (mwoodson@redhat.com)
- added dirty_os_firewall (mwoodson@redhat.com)
- Added creating snapshot tag for autoprovisioned PVs to cron.
  (twiest@redhat.com)
- added gcp service account, update haproxy passthrough (mwoodson@redhat.com)
- removed include (mwoodson@redhat.com)
- Normalizing on oo vars (kwoodson@redhat.com)
- Adding storage buckets to dm (kwoodson@redhat.com)
- Adding ability to change from cname to A record. (kwoodson@redhat.com)
- temporary fix for the wrong file extension issue (ihorvath@redhat.com)
- fixing yml extension (ihorvath@redhat.com)
- changing the location of inital config for osohm container
  (ihorvath@redhat.com)
- add synthetic cluster-wide host support to ops-zagg-client (jdiaz@redhat.com)
- added ops-runner timeouts to create-app tests (sten@redhat.com)
- moving everything from dynamic keys to static zabbix items
  (ihorvath@redhat.com)
- Improved nodes_not_schedulable check Check avoids master nodes Reincluded
  zabbix trigger for check (bshpurke@redhat.com)
- added tags support for the dm builder in gcp (mwoodson@redhat.com)
- etcd metrics with dynamic items in zabbix (ihorvath@redhat.com)
- Added graph for openshift.master.cluster.max_mem_pods_schedulable
  (twiest@redhat.com)
- add --timeout to ops-runner and a dynamic item to hold these items
  (jdiaz@redhat.com)
- Added more items and graphs for online preview cluster. (twiest@redhat.com)
- Removed not scheduled check (benpack101@gmail.com)
- delte the cert before upload (zhizhang@zhizhang-laptop-nay.redhat.com)
- more gcp roles and changes (mwoodson@redhat.com)
- Adding pd pv support for gcp dm (kwoodson@redhat.com)
- Adding request path (kwoodson@redhat.com)
- Adding service-account keys and policy (kwoodson@redhat.com)
- Fixed typo with node related zabbix checks(node-not-ready/not-labeled) Added
  zabbix check for non-schedulable nodes Added proper sop links in zabbix
  (bshpurke@redhat.com)
- Added compute node cpu idle and memory available averages items and graphs to
  zabbix (twiest@redhat.com)
- handle one case of not being able to remove the docker vg (sten@redhat.com)
- fixed var name in gcp cluster creation (mwoodson@redhat.com)
- put docker version to 1.9.1 (mwoodson@redhat.com)
- updated gcp cluster creation with reconciler (mwoodson@redhat.com)
- First attempt at the dm reconciler (kwoodson@redhat.com)
- Change config loop failure to a high alert (agrimm@redhat.com)
- removed old role git_rebase_upstream (mwoodson@redhat.com)
- fixed readme files (mwoodson@redhat.com)
- added new roles for gcp (mwoodson@redhat.com)
- First attempt at service account (kwoodson@redhat.com)
- removed warning in temp git dir (mwoodson@redhat.com)
- Fix param swap (kwoodson@redhat.com)
- Updating to take into account colons in ssh key hosts (kwoodson@redhat.com)
- logic fix for ssh key comparison (kwoodson@redhat.com)
- ProjectInfo added for sshkey support (kwoodson@redhat.com)
- Added graphs for scheduled and oversubscribed. (twiest@redhat.com)
- run event watch to catch/report FailedScheduling events (jdiaz@redhat.com)
- have all masters report cluster stats (not just primary master)
  (jdiaz@redhat.com)
- gcloud manifest added (kwoodson@redhat.com)
- add more generous random sleeping for various cron jobs (jdiaz@redhat.com)
- Update the docs for oso_host_monitoring (rharriso@redhat.com)
- Fixed the executable path of gcloud (kwoodson@redhat.com)
- Install the gcloud package which has gcloud cli (kwoodson@redhat.com)
- Added gcloud_compute_image ansible module (kwoodson@redhat.com)
- Added cluster capacity items. (twiest@redhat.com)
- Adding provisioning flag for metadata (kwoodson@redhat.com)
- Updating openshift-tools to use our own pylintrc.  disabling too-many-lines
  (kwoodson@redhat.com)
- Add basic dnsmasq monitoring template and cron configuration
  (rharriso@redhat.com)
- use --node-checks instead of --nodes-checks (jdiaz@redhat.com)
- Added check for nodes without labels (bshpurke@redhat.com)
- First attempt at resource builder for gcp (kwoodson@redhat.com)
- ensuring /var/log/rootlog directories get created (dedgar@redhat.com)
- ironed out ansible style issues and ensured profile directory gets created
  (dedgar@redhat.com)
- cleaning up rootlog portion (dedgar@redhat.com)
- cleaning up formatting (dedgar@redhat.com)
- adding initial rootlog configuration (dedgar@redhat.com)

* Wed Jul 06 2016 Joel Smith <joesmith@redhat.com> 0.0.13-1
- page out when app builds fail >2hr or app creates fail >1hr (sten@redhat.com)
- Add ops_map_format filter to the ops_filters plugin (joesmith@redhat.com)
- Made some tweaks to our users_available calculations per dmcphers feedback.
  (twiest@redhat.com)
- added debug info for nodes not ready check (sten@redhat.com)
- added ops_customizations (mwoodson@redhat.com)
- adding cpu and memory per process monitoring (ihorvath@redhat.com)
- Added ozcs_clusterid to the name in the graphs in os_zabbix_cluster_stats
  (twiest@redhat.com)
- Fixed bug in os_zabbix_cluster_stats (twiest@redhat.com)
- Added graphs for mem.users_available and cpu.users_available.
  (twiest@redhat.com)
- report average cpu and memory allocations for compute nodes across the
  cluster (jdiaz@redhat.com)
- Added features to graph_item (twiest@redhat.com)
- Added check to ops-docker-storage-reinitialize.yml for when the docker_vg is
  being used by another device. (twiest@redhat.com)
- mark zabbix item as a "%%" unit (jdiaz@redhat.com)
- Fixed bug in os_zabbix_cluster_stats (twiest@redhat.com)
- allow passing in auto-logout value for zabbix users (jdiaz@redhat.com)
- deal with new groups being added to a user (jdiaz@redhat.com)
- Added os_zabbix_cluster_stats (twiest@redhat.com)
- Added ability to create items directly on a host to the zbx_item ansible
  module. (twiest@redhat.com)
- add item to hold FailedScheduling event counts (jdiaz@redhat.com)
- Fixed openshift.master.avg_running_pods_per_user (twiest@redhat.com)
- Added metrics for openshift master memory and cpu for the number of users
  using the system. (twiest@redhat.com)
- First attempt at gcloud deployment-manager deployments. (kwoodson@redhat.com)

* Thu Jun 23 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.12-1
- Adding filter plugins from openshift-ansible and moved to ops
  (kwoodson@redhat.com)
- Adding params for calculated items (kwoodson@redhat.com)

* Thu Jun 23 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.11-1
- Setting up filter plugins for ops (kwoodson@redhat.com)
- Install python-gcloud. (kwoodson@redhat.com)
- adding pop functionality (kwoodson@redhat.com)
- Changed the thresholds of the established connections as well as critically
  low memory triggers. (twiest@redhat.com)
- Adding instance_states to gce.py (kwoodson@redhat.com)
- random sleep for 5 minutes and run every 4 hours (jdiaz@redhat.com)
- only need to pass one sleep flag (and not 3600 seconds) (jdiaz@redhat.com)
- Adding a 60 sec wait for possible race condition when restarts of services
  occur (kwoodson@redhat.com)
- fixed pylint errors: (mwoodson@redhat.com)
- removed git status (mwoodson@redhat.com)
- added new git modules (mwoodson@redhat.com)
- changing the cron entries, because they were lacking the names and adding
  defattr to files section in one of the packages in the script spec file
  (ihorvath@redhat.com)
- Fixing spacing (mwhittingham@redhat.com)
- Fixing how far it's indented (mwhittingham@redhat.com)
- Fixing handlers name section (mwhittingham@redhat.com)
- Actually fixing yaml syntax (mwhittingham@redhat.com)
- Fixed bug where ec2_tag would run for each master. (twiest@redhat.com)
- Fixed bug where I wasn't passing creds to ec2_tag. (twiest@redhat.com)
- Fixing yaml syntax (mwhittingham@redhat.com)
- Updated ops-docker-loopback-to-direct-lvm.yml to work with our current setup.
  (twiest@redhat.com)
- removed dump extra .com (mwoodson@redhat.com)
- added the postfix_amazon ses client role; updated from address on gpg send
  role (mwoodson@redhat.com)
- Added volume tags to openshift_aws_persistent_volumes (twiest@redhat.com)
- use nodejs-ex instead of nodejs-example for STI test (sten@redhat.com)
- Adding monitoring for existing connections on etcd and master api server
  (ihorvath@redhat.com)
- twiest asked me to change the wording on zagg queue triggers
  (ihorvath@redhat.com)
- Updating to latest gce.py (kwoodson@redhat.com)
- Changed base OS level checks to run every minute so that Jeremy Eder's team
  can use our zabbix data. (twiest@redhat.com)
- Added purpose tag to EBS PV creator. (twiest@redhat.com)
- stop passing in environment variable to host-monitoring container only one
  script uses one of these environment variables (scripts/monitoring/cron-send-
  create-app.py), and the cron job for it is written in a way where the needed
  environment variable is explicitely passed in before launching it
  (jdiaz@redhat.com)
- Removing handlers section from the task section (mwhittingham@redhat.com)
- Fixing spacing for handlers section (mwhittingham@redhat.com)
- Fixing notify handler (mwhittingham@redhat.com)
- Fixing README spacing (mwhittingham@redhat.com)
- Adding notify to template task for service restarts during config changes
  (mwhittingham@redhat.com)
- Creating openshift_dedicated_admin role (mwhittingham@redhat.com)

* Mon Jun 13 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.10-1
- Fixing a bug if get_entry does not contain a key. (kwoodson@redhat.com)
- Made the snapshot and trim operations more error resistant.
  (twiest@redhat.com)
- allow o+rx on openshift_tools (jdiaz@redhat.com)
- change default(False, True) usage to default(False) (jdiaz@redhat.com)
- allow for per-cluster pruning vars (jdiaz@redhat.com)
- added rhmap to image exceptions (sedgar@redhat.com)
- Backup copy to protect ourselves (kwoodson@redhat.com)
- Added ops-ec2-add-snapshot-tag-to-ebs-volumes.py (twiest@redhat.com)
- cleanup of openshft_aws_user (mwoodson@redhat.com)
- move monitoring container configuration into passed-in/bound file Rather than
  pass numerous environment variable to control how the host-monitoring
  container is started/configured, move environment vars into a yaml file that
  can be bound in. This will configure things like the list of cron jobs to
  instantiate, the clusterid, zagg settings, etc. Logic that determines what
  gets installed is moved into the oso-host-monitoring role when it generates a
  monitoring-config.yml file for each node. Config loop will now install
  /etc/openshift_tools/monitoring-config.yml, and the systemd file for host-
  monitoring will bind it in at the same location. (jdiaz@redhat.com)
- Bug fix for first level entries, added append, and fixed update
  (kwoodson@redhat.com)
- cleaned up some new aws account setup roles : (mwoodson@redhat.com)
- add step to remove /etc/sysconfig/docker-storage file old thin pool settings
  in the file can keep docker-storage-setup from working properly
  (jdiaz@redhat.com)
- Updating for dynamic inventory generation (kwoodson@redhat.com)
- more role cleanup (mwoodson@redhat.com)
- added lib_git (mwoodson@redhat.com)
- added module lib_iam_accountid (mwoodson@redhat.com)
- Adding a test for results coming back as None (kwoodson@redhat.com)
- add no log to ssh add keys (mwoodson@redhat.com)
- more fixes for the aws_user (mwoodson@redhat.com)
- Content is now idempotent. (kwoodson@redhat.com)
- added new roles for setting up aws stuff (mwoodson@redhat.com)
- Fixed return val when updating a list (kwoodson@redhat.com)
- Fixed a bug introduced by the deepcopy. Fixed a bug with create.
  (kwoodson@redhat.com)
- detect/enable cluster capacity reporting in the data hierarchy, set
  g_enable_cluster_capacity_reporting to True for any cluster that should have
  this reporting enabled (jdiaz@redhat.com)

* Tue May 31 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.9-1
- Adding snythetic hosts for bootstrapping (kwoodson@redhat.com)
- TDGC: Update vars in example playbook section (whearn@redhat.com)
- Add temp_dir_git_clone (whearn@redhat.com)

* Tue May 31 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.8-1
- Rename cluster_group to clusterid (kwoodson@redhat.com)

* Tue May 31 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.7-1
- Fixed a bug with partial creates (kwoodson@redhat.com)
- Fixed create state. (kwoodson@redhat.com)
- Changes to prevent flapping (rharriso@redhat.com)
- Add triggers for low available PVs (rharriso@redhat.com)
- Add trigger to alert when failed persistant volumes are present
  (rharriso@redhat.com)
- Adding cluster_var support. (kwoodson@redhat.com)
- add zabbix entries to hold cluster-wide calculated items (jdiaz@redhat.com)

* Wed May 25 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.6-1
- Yedit bug fixes as well as enhancements (kwoodson@redhat.com)
- bind in host's oc and oadm binaries (so we get 3.1/3.2 bins on 3.1/3.2
  clusters) (jdiaz@redhat.com)
- Added osohm_snapshot_aws_access_key_id and
  osohm_snapshot_aws_secret_access_key to the oso_host_monitoring role.
  (twiest@redhat.com)
- fixed some metrics automations (mwoodson@redhat.com)
- Added update to encompass dict and list.  Added list to return only value
  when key is specified (kwoodson@redhat.com)
- Moved account syntax to a hash (kwoodson@redhat.com)
- pass environment OSO_MASTER_PRIMARY to monitoring container
  (jdiaz@redhat.com)
- Openshift metrics role (kwoodson@redhat.com)
- added openshift_* roles (mwoodson@redhat.com)
- Adding selectors on delete (kwoodson@redhat.com)
- Added decode secret option. Added error handling to oadm_router for when it
  fails (kwoodson@redhat.com)
- Fix to oc_secrets delete_after (kwoodson@redhat.com)
- Added statement to catch errors when creation fails (kwoodson@redhat.com)
- Added name and path to secrets file (kwoodson@redhat.com)

* Mon May 16 2016 Thomas Wiest <twiest@redhat.com> 0.0.5-1
- Added ops-ec2-snapshot-ebs-volumes.py and ops-ec2-trim-ebs-snapshots.py
  (twiest@redhat.com)
- Moving lib_openshift_api to lib_openshift_3.2 (kwoodson@redhat.com)
- Added ops-docker-storage-reinitialize.yml and the sysconfig_fact.py module.
  (twiest@redhat.com)
- update logic to avoid delete/create when updating existing node entries
  (jdiaz@redhat.com)
- Adding 3.2 changes (kwoodson@redhat.com)
- add oc_scale to manage replicas on deploymentconfigs (jdiaz@redhat.com)
- Initial oadm_policy_user (kwoodson@redhat.com)
- add extra group tests and update label tests (jdiaz@redhat.com)
- add group module and extend user module to manage group membership
  (jdiaz@redhat.com)
- added fstab_mount_options (mwoodson@redhat.com)
- Adding exist, append, and add_item (kwoodson@redhat.com)
- add user crud to lib_openshift_api (jdiaz@redhat.com)
- Added cat_fact module. (twiest@redhat.com)
- set dm.basesize to 3G EXTRA_DOCKER_STORAGE_OPTIONS is a no-op on 3.1 clusters
  because docker 1.8's /usr/bin/docker-storage-setup doesn't read/use it. On
  3.2 (docker 1.9) it will not allow container images sizes beyond 3G
  (jdiaz@redhat.com)
- Updated router to take cacert (kwoodson@redhat.com)
- added new docker storage setup options (mwoodson@redhat.com)
- Adding ability to force a refresh on the registry (kwoodson@redhat.com)
- add support for labeling and test cases for labeling nodes specifically
  (jdiaz@redhat.com)
- oc_serviceaccount (kwoodson@redhat.com)
- Bug fixes.  Now accept path or content for certs. (kwoodson@redhat.com)
- oadm_project and oc_route (kwoodson@redhat.com)
- Bug fixes to preserve registry service clusterIP (kwoodson@redhat.com)

* Fri Apr 22 2016 Kenny Woodson <kwoodson@redhat.com> 0.0.4-1
- Kubeconfig fix (kwoodson@redhat.com)
- Refactor. Adding registry helpers.  Adding registry (kwoodson@redhat.com)

* Thu Apr 21 2016 Joel Diaz <jdiaz@redhat.com> 0.0.3-1
- depend on ansible1.9 RPM from EPEL (jdiaz@redhat.com)

* Tue Apr 12 2016 Joel Diaz <jdiaz@redhat.com> 0.0.2-1
- copy filters, inventory, docs and test from openshift-ansible
  (jdiaz@redhat.com)

* Mon Apr 11 2016 Joel Diaz <jdiaz@redhat.com> 0.0.1-1
- new package built with tito

