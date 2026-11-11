from adiskreader.datasource import DataSource
from adiskreader.disks import Disk


async def url_to_fs(url, partition_idx=None, fstype='NTFS', disk_member=None, parent_paths=None):
	"""Open a filesystem from any datasource URL supported by adiskreader.

	disk_member selects a disk inside an OVA archive, parent_paths supplies
	parent images for VDI/QCOW2 differencing chains.
	"""
	ds = await DataSource.from_url(url)
	disk = await Disk.from_datasource(ds, disk_member=disk_member, parent_paths=parent_paths)
	partitions = await disk.list_partitions()

	if partition_idx is not None:
		return await partitions[partition_idx].mount()

	for partition in partitions:
		if fstype is not None and partition.FileSytemType != fstype:
			continue
		try:
			fs = await partition.mount()
			rootdir = await fs.get_root()
			for name in ('Windows', 'WINDOWS', 'windows'):
				if await rootdir.get_child(name) is not None:
					return fs
		except Exception:
			continue

	await ds.close()
	return None
