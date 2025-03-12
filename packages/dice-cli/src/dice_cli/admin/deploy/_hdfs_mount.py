from dataclasses import dataclass
from typing import List, Tuple

from dice_lib import load_config
from dice_lib.host import HostCommand

FSTAB_PATH: str = "/etc/fstab"


@dataclass
class InstallConfig:
    url: str
    config_url: str
    download_dst: str
    extract_dst: str
    config_dst: str
    mount_point: str
    fstab_entry: str
    symlinks: List[Tuple[str, str]]


def _read_dice_config() -> InstallConfig:
    config = load_config()
    hdfs_info = config.storage.hdfs
    install = hdfs_info.extras.INSTALL_INSTRUCTIONS
    return InstallConfig(
        url=install.HADOOP_TARBALL_URL,
        config_url=install.CONFIG_TARBALL_URL,
        download_dst=install.DOWNLOAD_DESTINATION,
        extract_dst=install.EXTRACT_DESTINATION,
        config_dst=install.CONFIG_DESTINATION,
        mount_point=hdfs_info.extras.HDFS_FUSE_MOUNT,
        fstab_entry=hdfs_info.extras.FSTAB_ENTRY,
        symlinks=[(src, dst) for src, dst in install.SYMLINKS.items()],
    )


def get_setup_commands() -> List[HostCommand]:
    config: InstallConfig = _read_dice_config()
    make_directories = HostCommand(
        "mkdir",
        parameters=[
            "-p",
            config.download_dst,
            config.extract_dst,
            config.config_dst,
        ],
    )
    download_tar = HostCommand(
        "wget", parameters=[config.url, "-O", f"{config.download_dst}/hdfs.tar.gz"]
    )
    extract_tar = HostCommand(
        "tar",
        parameters=[
            "-xzf",
            f"{config.download_dst}/hdfs.tar.gz",
            "-C",
            config.extract_dst,
        ],
    )
    download_config_tar = HostCommand(
        "wget",
        parameters=[
            config.config_url,
            "-O",
            f"{config.download_dst}/hdfs-config.tar.gz",
        ],
    )
    extract_config_tar = HostCommand(
        "tar",
        parameters=[
            "-xzf",
            f"{config.download_dst}/hdfs-config.tar.gz",
            "-C",
            config.config_dst,
        ],
    )

    make_symlinks = [
        HostCommand("ln", parameters=["-s", *link]) for link in config.symlinks
    ]

    fstab_entry = f"{config.fstab_entry!r}"
    make_mount_point = HostCommand("mkdir", parameters=["-p", config.mount_point])
    make_fstab_entry = HostCommand("echo", parameters=[fstab_entry, ">>", FSTAB_PATH])
    mount_hdfs = HostCommand("mount", parameters=[config.mount_point])

    return [
        make_directories,
        download_tar,
        extract_tar,
        download_config_tar,
        extract_config_tar,
        *make_symlinks,
        make_mount_point,
        make_fstab_entry,
        mount_hdfs,
    ]
