# Virtual Machine Manager News

## Release 5.0.0 (November 26, 2024)
- virt-clone: colne serial files (Oleg Vasilev)
- virt-clone: Copy disk permissions as well (Martin Kletzander)
- virt-install: Add properties for AMD SEV-SNP (Daniel P. Berrangé)
- virt-install: Add passt backend for user network interface
- virt-install: Add support for --sound multichannel,stream (Lin Ma)
- virt-install: Add support for --tpm backend.debug,backend.source (Lin Ma)
- virt-xml: add --edit --convert-to-q35
- virt-xml: add --edit --convert-to-vnc
- virt-xml: Add --edit --boot uefi
- virt-manager: Fix opening graphical console with egl-headless (Feng Jiang)
- virt-manager: Add support to create external snapshots
- virt-manager: Default to scaling=Always for consoles
- virt-manager: switch to not forking by default
- cli: Add more --disk options (Lin Ma)
- cli: Add --memdev target.address_base for virtio-mem and virtio-pmem (Lin Ma)
- cli: Add --features kvm.pv-ipi.state=on|off (Lin Ma)
- cli: Add --video model.blob=on|off (Lin Ma)
- Add missing Hyper-V features and enable most of them by default
- Add loongarch support (Xianglai Li)
- Add support for hvf domain type (Mohamed Akram)
- Support creating sparse volumes on ZFS pools (Iain Buclaw)
- UEFI improvements for riscv64 and loongarch64 VMs (Andrea Bolognani)
- Add graphics to riscv64 and aarch64
- build: switch from setuptools to meson
- diskbackend: Drop support for sheepdog (Lin Ma)
- cli: Deprecate --cpu host in favor of --cpu host-model (Andrea Bolognani)

## Release 4.1.0 (August 04, 2022)
- Fix build with setuptools-61 (Peter Alfredsen, Miro Hrončok)
- add UI and cli support for qemu-vdagent channel (Jonathon Jongsma)
- cli: More --iothreads suboptions (Lin Ma)
- launch_security: Use SEV-ES policy=0x07 if host supports it (Charles
  Arnold)
- cli: Add support for URL query with disks (Martin Kletzander)

## Release 4.0.0 (March 02, 2022)
- virt-install --os-variant/--osinfo is now a hard requirement for most
  cases
- Add 'Enable shared memory' UI checkbox (Lin Ma)
- add UI preference to default to UEFI for new VMs (Charles Arnold)
- Add virtiofs filesystem driver UI option
- Fill in all --cputune, --cpu, --shmem, --input, and --boot suboptions
  (Hugues Fafard)
- virt-* mdev improvements (Shalini Chellathurai Saroja)
- bhyve improvements (Roman Bogorodskiy)
- Revive network portgroup UI
- enable a TPM by default when UEFI is used (Daniel P. Berrangé)
- Use cpu host-passthrough by default on qemu x86
- use virtio-gpu video for most modern distros
- Default to extra pcie root ports for q35
- set discard=unmap by default for sparse disks and block devices
- We now require xorissofs for --location ISO
- We now use setuptools rather than just plain distutils

## Release 3.2.0 (November 14, 2020)
- Slim down filesystem device editor UI
- Fix TOCTTOU virt-install bugs (Martin Pitt)
- Several other bug fixes

## Release 3.1.0 (September 30, 2020)
- Return to using qcow2 sparse by default with libvirt 5.0.0+
- Make VM window shortcuts less likely to conflict with guest usage
- Fix 3.0.0 regression with spice audio
- createvol: Add explicit option for qcow2 non-sparse
- Unconditionally add USB redirdev to new VMs when using SPICE
- Unconditionally add sound devices to new VMs
- Translation string improvements (Pino Toscano)

## Release 3.0.0 (September 15, 2020)
- virt-install --cloud-init support (Athina Plaskasoviti, Cole Robinson)
- The virt-convert tool has been removed. Please use virt-v2v instead
- A handful of UI XML configuration options have been removed. The XML
  editor can be used instead. For a larger discussion see this thread:
  https://www.redhat.com/archives/virt-tools-list/2019-June/msg00117.html
- The 'New VM' UI now has a 'Manual Install' option which creates a VM
  without any required install media
- In the 'New VM' UI, the network/pxe install option has been removed. If
  you need network boot, choose 'Manual Install' and set the boot device after
  initial VM creation
- 'Clone VM' UI has been reworked and simplified
- 'Migrate VM' UI now has an XML editor for the destination VM
- Global and per-vm option to disable graphical console autoconnect. This
  makes it easier to use virt-manager alongside another client like virt-
  viewer
- virt-manager: set guest time after VM restore (Michael Weiser)
- virt-manager: option to delete storage when removing disk device (Lily
  Nie)
- virt-manager: show warnings if snapshot operation is unsafe (Michael
  Weiser)
- Unattended install improvements (Fabiano Fidêncio)
- cli: new --xml XPATH=VAL option for making direct XML changes
- virt-install: new --reinstall=DOMAIN option
- virt-install: new --autoconsole text|graphical|none option
- virt-install: new --os-variant detect=on,require=on suboptions
- cli: --clock, --keywrap, --blkiotune, --cputune additions (Athina
  Plaskasoviti)
- cli: add --features kvm.hint-dedicated.state= (Menno Lageman)
- cli:--iommu option (Menno Lageman)
- cli: Add --graphics websocket= support (Petr Benes)
- cli: Add --disk type=nvme source.* suboptions
- cli: Fill in all --filesystem suboptions
- Translation string improvements (Pino Toscano)
- Convert from .pod to .rst for man pages
- Switch to pytest as our test runner
- Massively improved unittest and uitest code coverage
- Now using github issues as our bug tracker

## Release 2.2.1 (July 03, 2019)
- CVE-2019-10183: Replace --unattended user-password and admin-password with
  user-password-file and admin-password-file (Fabiano Fidêncio)
- Consistent --memballoon default across non-x86 (Andrea Bolognani)
- virt-install: add --numatune memnode.* (Athina Plaskasoviti)
- Drop hard dep on gtksourceview4, gtksourceview3 is fine as well

## Release 2.2.0 (June 17, 2019)
- libvirt XML viewing and editing UI for new and existing domain, pools,
  volumes, networks
- virt-install: libosinfo --unattended support (Fabiano Fidêncio, Cole
  Robinson)
- Improve CPU model security defaults (Pavel Hrdina)
- virt-install: new --install  option. Ex: virt-install --install fedora29
- virt-install: new --install kernel=,initrd=
- virt-install: --disk, --memory, --name defaults from libosinfo (Fabiano
  Fidêncio, Cole Robinson)
- virt-install: add device suboption aliases which consistently match
  libvirt XML naming
- virt-xml: new --start, --no-define options (Marc Hartmayer)
- virt-install: Add driver_queues argument to --controller (Vasudeva Kamath)
- RISC-V support (Andrea Bolognani)
- Device default improvements for non-x86 KVM (Andrea Bolognani)
- Redesigned 'New Network' wizard
- libguestfs inspection improvements (Pino Toscano)
- virt-install: Add support for xenbus controller (Jim Fehlig)
- cli: Add --disk wwn=,rawio= (Athina Plaskasoviti)
- cli: Add --memballoon autodeflate=,stats.period= (Athina Plaskasoviti)
- cli: Add --iothreads (Athina Plaskasoviti)
- cli: Add --numatune memory.placement (Athina Plaskasoviti)
- cli: Add --launchSecurity option (Erik Skultety)
- cli: Fill in --memorybacking options
- cli: --smartcard: support database= and certificate[0-9]*=
- cli: --sysinfo: Add chasis suboptions
- cli: --metadata: add genid= and genid_enable=
- cli: --vcpus: add vcpus.vcpu[0-9]* config
- cli: fill in all common char source options for --serial, --parellel,
  --console, --channel, --smartcard, --rng, --redirdev

## Release 2.1.0 (February 03, 2019)
- Bash autocompletion support (Lin Ma, Cole Robinson)
- UI and command line --vsock support (Slavomir Kaslev)
- virt-xml: Add --os-variant option (Andrea Bolognani)
- virt-install: use libosinfo cpu, mem, disk size defaults (Fabiano
  Fidencio)
- virt-install: Better usage of libosinfo -unknown distro IDs (Fabiano
  Fidencio)
- virt-install: More usage of libosinfo for ISO --location detection
- virt-install: Add --location LOCATION,kernel=X,initrd=Y for pointing to
  kernel/initrd in media that virt-install/libosinfo fails to detect

## Release 2.0.0 (October 15, 2018)
- Finish port to Python 3 (Radostin Stoyanov, Cole Robinson)
- Improved VM defaults for supported OS: q35 PCIe, usb3, CPU host-model
- Search based OS selection UI for new VMs (Daniel P. Berrangé, Cole
  Robinson)
- Track OS name for lifetime of domain in <metadata> XML
- Host interface management UI has been completely removed
- Show domain IP on interface details page (Lin Ma, Cole Robinson)
- More efficient stats polling with AllDomainStats (Simon Kobyda, Cole
  Robinson)
- TPM device model and backend UI (Marc-André Lureau, Stefan Berger)
- Show <channel> connection state in UI (Lin Ma)
- Show attached devices in <controller> UI (Lin Ma)
- UI option to plug/unplug VM nic link (Simon Kobyda)
- UI support for disk discard and detect_zeroes (Povilas Kanapickas, Lin Ma)
- Improved SUSE --location URL/ISO detection (Charles Arnold)
- cli and UI support for SCSI persistent reservations (Lin Ma)
- cli: Add --network mtu.size= option (Anya Harter)
- cli: Add --disk driver.copy_on_read (Anya Harter)
- cli: Add --disk geometry support (Anya Harter)
- cli: Add --sound codec support (Anya Harter)
- cli: Add --hostdev net/char/block for LXC (Lubomir Rintel)
- cli: Add --memorybacking access_mode and source_type (Marc-André Lureau)
- cli: Add --boot rebootTimout (Yossi Ovadia)
- cli: Add --boot bootloader=
- cli: Add --destroy-on-exit

## Release 1.5.0 (February 06, 2018)
- python3 prep work (Radostin Stoyanov, Cole Robinson, Cédric Bosdonnat)
- Switch --location ISO to use isoinfo (Andrew Wong)
- virt-install: add --cpu numa distance handling (Menno Lageman)
- virt-install: fix --disk for rbd volumes with auth (Rauno Väli)
- virt-install: add --cputune vcpupin handling (Wim ten Have)
- details ui: Showing attached scsi devices per controller (Lin Ma)
- network ui: Show details about SR-IOV VF pool (Lin Ma)
- Greatly expand UI test suite coverage

## Release 1.4.3 (September 19, 2017)
- Improve install of debian/ubuntu non-x86 media (Viktor Mihajlovski, Andrew
  Wong)
- New virt-install --graphics listen.* (Pavel Hrdina)
- New virt-install --disk snapshot_policy= (Pavel Hrdina)
- New virt-install --cpu cache.* (Lin Ma)
- Several bug fixes

## Release 1.4.2 (August 08, 2017)

- New VM wizard virt-bootstrap integration (Radostin Stoyanov)
- New VM wizard support for virtuozzo containers (Mikhail Feoktistov)
- network UI: add support to create SR-IOV VF pool (Lin Ma)
- Nicer OS list in New VM wizard (Pino Toscano)
- Better defaults for UEFI secureboot builds (Pavel Hrdina)
- Fix defaults for aarch64 VMs if graphics are requested
- virt-install: new `--memdev` option (Pavel Hrdina)
- virt-install: add `--disk logical/physical_block_size` (Yuri Arabadji)
- virt-install: add `--features hyperv_reset=, hyperv_synic=` (Venkat Datta N
  H)

## Release 1.4.1 (March 08, 2017)

- storage/nodedev event API support (Jovanka Gulicoska)
- UI options for enabling spice GL (Marc-André Lureau)
- Add default virtio-rng /dev/urandom for supported guest OS
- Cloning and rename support for UEFI VMs (Pavel Hrdina)
- libguestfs inspection UI improvements (Pino Toscano)
- virt-install: Add `--qemu-commandline`
- virt-install: Add `--network vhostuser` (Chen Hanxiao)
- virt-install: Add `--sysinfo` (Charles Arnold)

## Release 1.4.0 (June 18, 2016)

- virt-manager: spice GL console support (Marc-André Lureau, Cole Robinson)
- Bump gtk and pygobject deps to 3.14
- virt-manager: add checkbox to forget keyring password (Pavel Hrdina)
- cli: add `--graphics gl=` (Marc-André Lureau)
- cli: add `--video accel3d=` (Marc-André Lureau)
- cli: add `--graphics listen=none` (Marc-André Lureau)
- cli: add `--transient` flag (Richard W.M. Jones)
- cli: `--features gic=` support, and set a default for it (Pavel Hrdina)
- cli: Expose `--video heads, ram, vram, vgamem`
- cli: add `--graphics listen=socket`
- cli: add device address.type/address.bus/...
- cli: add `--disk seclabelX.model` (and .label, .relabel)
- cli: add `-cpu cellX.id` (and .cpus, and .memory)
- cli: add `--network rom_bar=` and `rom_file=`
- cli: add `--disk backing_format=`
- Many bug fixes and improvements

## Release 1.3.2 (December 24, 2015)

- Fix dependency issues with vte

## Release 1.3.1 (December 06, 2015)

- Fix command line API on RHEL7 pygobject

## Release 1.3.0 (November 24, 2015)

- Git hosting moved to http://github.com/virt-manager/virt-manager
- Switch translation infrastructure from transifex to fedora.zanata.org
- Add dogtail UI tests and infrastructure
- Improved support for s390x kvm (Kevin Zhao)
- virt-install and virt-manager now remove created disk images if VM
  install startup fails
- Replace urlgrabber usage with requests and urllib2
- virt-install: add `--network` virtualport support for openvswitch
  (Daniel P. Berrange)
- virt-install: support multiple `--security` labels
- virt-install: support `--features kvm_hidden=on|off` (Pavel Hrdina)
- virt-install: add `--features pmu=on|off`
- virt-install: add `--features pvspinlock=on|off` (Abhijeet Kasurde)
- virt-install: add `--events on_lockfailure=on|off` (Abhijeet Kasurde)
- virt-install: add `--network link_state=up|down`
- virt-install: add `--vcpu placement=static|auto`

## Release 1.2.1 (June 06, 2015)

- Bugfix release
- Fix connecting to older libvirt versions (Michał Kępień)
- Fix connecting to VM console with non-IP hostname (Giuseppe Scrivano)
- Fix addhardware/create wizard errors when a nodedev disappears
- Fix adding a second cdrom via customize dialog

## Release 1.2.0 (May 04, 2015)

- OVMF/AAVMF Support (Laszlo Ersek, Giuseppe Scrivano, Cole Robinson)
- Improved support for AArch64 qemu/kvm
- virt-install: Support `--disk type=network` parameters
- virt-install: Make `--disk` just work
- virt-install: Add `--disk sgio=` option (Giuseppe Scrivano)
- addhardware: default to an existing bus when adding a new disk
  (Giuseppe Scrivano)
- virt-install: Add `--input` device option
- virt-manager: Unify storagebrowser and storage details functionality
- virt-manager: allow setting a custom connection row name
- virt-install: Support `--hostdev scsi` passthrough
- virt-install: Fill in a bunch of `--graphics` spice options
- Disable spice image compression for new local VMs
- virt-manager: big reworking of the migration dialog

## Release 1.1.0 (September 07, 2014)

- Switch to libosinfo as OS metadata database (Giuseppe Scrivano)
- Use libosinfo for OS detection from CDROM media labels (Giuseppe
  Scrivano)
- Use libosinfo for improved OS defaults, like recommended disk size
  (Giuseppe Scrivano)
- virt-image tool has been removed, as previously announced
- Enable Hyper-V enlightenments for Windows VMs
- Revert virtio-console default, back to plain serial console
- Experimental q35 option in new VM 'customize' dialog
- UI for virtual network QoS settings (Giuseppe Scrivano)
- virt-install: `--disk discard=` support (Jim Minter)
- addhardware: Add spiceport UI (Marc-André Lureau)
- virt-install: `--events on_poweroff` etc. support (Chen Hanxiao)
- cli:`--network portgroup=` support and UI support
- cli:`--boot initargs=` and UI support
- addhardware: allow setting controller model (Chen Hanxiao)
- virt-install: support setting hugepage options (Chen Hanxiao)

## Release 1.0.1 (March 22, 2014)

- virt-install/virt-xml: New `--memorybacking` option (Chen Hanxiao)
- virt-install/virt-xml: New `--memtune option` (Chen Hanxiao)
- virt-manager: UI for LXC `<idmap>` (Chen Hanxiao)
- virt-manager: gsettings key to disable keygrab (Kjö Hansi Glaz)
- virt-manager: Show domain state reason in the UI (Giuseppe Scrivano)
- Fix a number of bugs found since the 1.0.0 release

## Release 1.0.0 (February 14, 2014)

- virt-manager: Snapshot support
- New tool virt-xml: Edit libvirt XML in one shot from the command line
- Improved defaults: qcow2, USB2, host CPU model, guest agent channel,...
- Introspect command line options like `--disk=?` or `--network=help`
- The virt-image tool will be removed before the next release, speak up
  if you have a good reason not to remove it.
- virt-manager: Support arm vexpress VM creation
- virt-manager: Add guest memory usage graphs (Thorsten Behrens)
- virt-manager: UI for editing `<filesystem>` devices (Cédric Bosdonnat)
- Spice USB redirection support (Guannan Ren)
- `<tpm>` UI and command line support (Stefan Berger)
- `<rng>` UI and command line support (Giuseppe Scrivano)
- `<panic>` UI and command line support (Chen Hanxiao)
- `<blkiotune>` command line support (Chen Hanxiao)
- virt-manager: support for glusterfs storage pools (Giuseppe Scrivano)
- cli: New options `--memory`, `--features`, `--clock`, `--metadata`, `--pm`
- Greatly improve app responsiveness when connecting to remote hosts
- Lots of UI cleanup and improvements

## Release 0.10.0 (June 19, 2013)

- Merged code with python-virtinst. virtinst is no longer public
- Port from GTK2 to GTK3 (Daniel Berrange, Cole Robinson)
- Port from gconf to gsettings
- Port from autotools to python distutils
- Remove virt-manager-tui
- Remove HAL support
- IPv6 and static route virtual network support (Gene Czarcinski)
- virt-install: Add `--cpu host-passthrough` (Ken ICHIKAWA, Hu Tao)

## Release 0.9.5 (April 01, 2013)

- Enable adding virtio-scsi disks (Chen Hanxiao)
- Support security auto-relabel setting (Martin Kletzander)
- Support disk iotune settings (David Shane Holden)
- Support 'reset' as a reboot option (John Doyle)
- Bug fixes and minor improvements

## Release 0.9.4 (July 29, 2012)

- Fix VNC keygrab issues

## Release 0.9.3 (July 09, 2012)

- Fix broken release tar.gz of version 0.9.2

## Release 0.9.2 (July 09, 2012)

- Convert to gtkbuilder: UI can now be edited with modern glade tool
- virt-manager no longer runs on RHEL5, but can manage a remote RHEL5
  host
- Option to configure spapr net and disk devices for pseries (Li Zhang)
- Many bug fixes and improvements

## Release 0.9.1 (January 31, 2012)

- Support for adding usb redirection devices (Marc-André Lureau)
- Option to switch usb controller to support usb2.0 (Marc-André Lureau)
- Option to specify machine type for non-x86 guests (Li Zhang)
- Support for filesystem device type and write policy (Deepak C Shetty)
- Many bug fixes!

## Release 0.9.0 (July 26, 2011)

- Use a hiding toolbar for fullscreen mode
- Use libguestfs to show guest packagelist and more (Richard W.M. Jones)
- Basic 'New VM' wizard support for LXC guests
- Remote serial console access (with latest libvirt)
- Remote URL guest installs (with latest libvirt)
- Add Hardware: Support `<filesystem>` devices
- Add Hardware: Support `<smartcard>` devices (Marc-André Lureau)
- Enable direct interface selection for qemu/kvm (Gerhard Stenzel)
- Allow viewing and changing disk serial number

## Release 0.8.7 (March 24, 2011)

- Allow renaming an offline VM
- Spice password support (Marc-André Lureau)
- Allow editing NIC `<virtualport>` settings (Gerhard Stenzel)
- Allow enabling/disabling individual CPU features
- Allow easily changing graphics type between VNC and SPICE for existing
  VM
- Allow easily changing network source device for existing VM

## Release 0.8.6 (Jan 14, 2011)

- SPICE support (requires spice-gtk) (Marc-André Lureau)
- Option to configure CPU model
- Option to configure CPU topology
- Save and migration cancellation (Wen Congyang)
- Save and migration progress reporting
- Option to enable bios boot menu
- Option to configure direct kernel/initrd boot

## Release 0.8.5 (August 24, 2010)

- Improved save/restore support
- Option to view and change disk cache mode
- Configurable VNC keygrab sequence (Michal Novotny)

## Release 0.8.4 (March 24, 2010)

- 'Import' install option, to create a VM around an existing OS image
- Support multiple boot devices and boot order
- Watchdog device support
- Enable setting a human readable VM description.
- Option to manually specifying a bridge name, if bridge isn't detected

## Release 0.8.3 (February 8th, 2010)

- New ability to manage network interfaces: start, stop, and view existing
  interfaces. Provision new bridge, bond, and vlan devices.
- New option to 'customize VM before install', which allows adjusting most
  VM options from the install wizard.

## Release 0.8.2 (December 14th, 2009)

This is largely a bug fix release. The following important bugs were fixed:

- Right click in the manager window operates on the clicked row, NOT
  the last selected row. This could cause an admin to accidentally shut down
  the wrong machine.
- Running virt-manager on a new machine / user account no longer produces
  a traceback.

Additionally, there is one new feature:

- Allow ejecting and connecting floppy media

## Release 0.8.1 (December 3rd, 2009)

 - VM Migration wizard, exposing various migration options
 - Enumerate CDROM and bridge devices on remote connections
 - Can once again list multiple graphs in main manager window (Jon Nordby)
 - Support disabling dhcp (Michal Novotny), and specifying 'routed' type for
   new virtual networks
 - Support storage pool source enumeration for LVM, NFS, and SCSI
 - Allow changing VM ACPI, APIC, clock offset, individual vcpu pinning,
   and video model (vga, cirrus, etc.)
 - Many improvements and bugfixes

## Release 0.8.0 (July 28th, 2009)

This release includes:

 - New 'Clone VM' Wizard
 - Improved UI, including an overhaul of the main 'manager' view
 - System tray icon for easy VM access (start, stop, view console/details)
 - Wizard for adding serial, parallel, and video devices to existing VMs.
 - CPU pinning support (Michal Novotny)
 - Ability to view and change VM security (sVirt) settings (Dan Walsh)
 - Many bug fixes and improvements

## Release 0.7.0 (March 9th, 2009)

This release includes:

  - Redesigned 'New Virtual Machine' wizard (Jeremy Perry, Tim Allen,
    Cole Robinson)
  - Option to remove storage when deleting a virtual machine.
  - File browser for libvirt storage pools and volumes, for use when
    attaching storage to a new or existing guest.
  - Physical device assignment (PCI, USB) for existing virtual machines.
  - Bug fixes and minor improvements.

## Release 0.6.1 (January 26th, 2009)

This release includes:

  - VM disk and network stats reporting (Guido Gunther)
  - VM Migration support (Shigeki Sakamoto)
  - Support for adding sound devices to an existing VM
  - Enumerate host devices attached to an existing VM
  - Allow specifying a device model when adding a network device to an
      existing VM
  - Combine the serial console view with the VM Details window
  - Allow connection to multiple VM serial consoles
  - Bug fixes and many minor improvements.

## Release 0.6.0 (September 10th, 2008)

This release includes:

  - Remote storage management and provisioning: View, add, remove, and
      provision libvirt managed storage. Attach managed storage to a
      remote VM.
  - Remote VM installation support: Install from managed media (cdrom)
      or PXE. Simple install time storage provisioning.
  - VM details and console windows merged: each VM is now represented by a
      single tabbed window.
  - Use Avahi to list libvirtd instances on network
  - Hypervisor Autoconnect: Option to connect to hypervisor at virt-manager
      start up.
  - Option to add sound device emulation when creating new guests.
  - Virtio and USB options when adding a disk device.
  - Allow viewing and removing VM sound, serial, parallel, and console devices.
  - Specifying a specific keymap when adding display device.
  - Keep app running if manager window is closed by VM window is still open.
  - Allow limiting amount of stored stats history
  - Numerous bug fixes and minor improvements.

## Release 0.5.4

This release focuses on minor feature enhancement and bug fixes. Using
the new GTK-VNC accelerated scaling support, the guest console window
can be smoothly resized to fill the screen. The SSH username is passed
through to the VNC console when tunnelling. Adding bridged network
devices is fixed. Support for all libvirt authentication methods is
enabled including Kerberos and PolicyKit. Solaris portability fix for
the text console. Support for detecting bonding and VLAN devices for
attaching guest NICs. Allow fullvirt guests to install off kernel and
initrd as well as existing CDROM methods. Fix invocation of DBus methods
to use an interface. Allow setting of autostart flag, and changing boot
device ordering. Control the new VM wizard based on declared hypervisor
capabilities.

## Release 0.5.3

This is a bug fix release. The sizing of the VNC window is fixed for
screens where the physical size is less than the guest screen size.
The 'new vm' button is switched back to its old (more obvious style/
placement). Restore of VMs is working again for local connections. A
menu for sending special key sequences to the guest is added. Lots of
other misc bug fixes

## Release 0.5.2

This is a bug fix release. Some broken menu items are hooked up again.
The rounding of memory values is fixed. Re-connecting to the VNC display
is fixed. Blocking of GTK accelerators is re-introduced when VNC is
active. Scrollbars on the VNC widget are re-introduced if the console
is close to the maximum local screensize. One new VM wizard is enabled
per connection. Hardware device details are immediately refreshed after
changes. Ability to add/remove display and input devices is enabled.

## Release 0.5.1

This release improves upon the remote management capabilities. It can
now tunnel connections to the VNC server over SSH. It avoids prompting
for SSH passwords on the console. Handling of VNC connections & retries
is made more robust. There is support for changing CDROM media on the
fly (requires suitably updated libvirt). There is ability to PXE boot
install fullyvirtualized guests. Connections to hypervisors are opened
in the background to avoid blocking the whole UI.

## Release 0.5.0

This release introduces the ability to manage multiple remote machines,
using either SSH+public keys, or TLS+x509 certificates to connect and
authenticate. The main user interface is re-worked to show multiple
hosts in a tree view, remembering connections across restarts. It is
not currently possible to create new guests with a remote host connection.
This capability will be added in a future release. The guest VNC console
implementation has been replaced with the GTK-VNC widget for greatly
improved performance and increased feature set. Other miscellaneous bug
fixes and feature enhancements are also included.

## Release 0.4.0

This release introduces major new functionality. There is new UI for the
creation & management of virtual networks using the new libvirt networking
APIs. The guest creation wizard can now attach VMs to a virtual network or
shared physical devices. The initial connection dialog is no longer shown,
either a QEMU or Xen connection is automatically opened based on host kernel
capabilities. For existing guests there is support for the addition and
removal of both disk & network devices (hot-add/remove too if supported by
the virtualization platform being used - eg Xen paravirt). The keymap for
guest VNC server is automatically set based on the local keymap to assist
people using non-English keyboard layouts. There is improved error reporting
for a number of critical operations such as starting guests / connecting
to the hypervisor.

## Release 0.3.2

The release introduces online help for all windows / dialogs in the
application, to explain usage & operation of key functions. Auto-popup
of consoles was fixed for existing inactive domains. Additional control
operations are available on the right-click menu in the VM list. A
handful of other minor bug fixes are also applied.

## Release 0.3.1

This release introduces support for managing QEMU / KVM virtual machines
using the new libvirt QEMU driver backend. This requires a new libvirt
(at least 0.2.0) to enable the QEMU driver. It also requires an install
of the virtinst package of at least version 0.101.0 to support QEMU. The
dual cursor problem is worked around by grabbing the mouse pointer upon
first button press (release with Ctrl+Alt). The progress bar display
when creating new VMs has had its appearance tweaked. The new VM creation
wizard also allows the user to specify the type of guest OS being installed.
This will allow the setup of virtual hardware to be optimized for the needs
of specific guest OS.

## Release 0.3.0

This release brings a major functionality update, enabling management
of inactive domains. This requires a new libvirt (at least 0.1.11)
to provide implementations of inactive domain management for Xen 3.0.3
and Xen 3.0.4. With this new functionality the display will list all
guests which are in the 'shutoff' state. The guest can be started with
the 'Run' button in the virtual console window. The vistinst package
must also be updated to at least version 0.100.0 to ensure that during
provisioning of guests it uses the new inactive domain management APIs.
Finally there have been a variety of minor UI fixes & enhancements
such as progress bars during guest creation, reliability fixes to the
virtual console and even greater coverage for translations.

## Release 0.2.6

The release focus has been on major bug fixing. This is also the
first release in which (partial) translations are available for
the UI in approximately 20 languages - thanks to the Fedora i18n
team for excellent progress on this. It is now possible to control
the virt-manager UI with command line arguments as well as the DBus
API & it DBus activation is no longer used by default which fixes
interaction with GNOME keyring & AT-SPI accessibility. Numerous
UI issues were fixed / clarified, particularly in the graphical
console and new VM creation wizard.


## Release 0.1.4

 * Integration with GNOME keyring for the VNC console to avoid
   need to remember passwords when accessing the guest domain's
   console
 * Use cairo to rendered a '50% alpha gray wash' over the screenshot
   to give appearance of a 'dimmed' display when paused. Also render
   the word 'paused' in big letters.
 * Initial cut of code for saving domain snapshots to disk
 * Added icons for buttons which were missing graphics
 * Miscellaneous RPM spec file fixes to comply with rpmlint
 * Update status icons to match those in the gnome-applet-vm
 * Added domain ID and # VCPUs to summary view
 * Misc bug fixes

## Release 0.1.3

 * Fixed DBus service activation & general brokenness
 * Added a display of virtual CPU count in summary page
 * Fixed alignment of status label in details page
 * Make hardware config panel resizeable
 * Switch detailed graph rendering to use sparkline code
 * Switch to use filled sparkline graphs

## Release 0.1.2

 * First public release
