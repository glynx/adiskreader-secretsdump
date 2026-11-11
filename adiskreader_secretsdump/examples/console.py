import asyncio
import argparse
import sys
from adiskreader_secretsdump.utils import url_to_fs
from adiskreader_secretsdump.modules.registry import REGSecrets
from adiskreader_secretsdump.modules.ntds import NTDSSecrets, NTDSNotFoundError

async def amain():
	parser = argparse.ArgumentParser(description='Secretsdump for adiskreader')
	parser.add_argument('-v', '--verbose', action='count', default=0)
	#parser.add_argument('-o', '--out-file', help='Output file path.')
	parser.add_argument('--pid', type=int, help='Partition index to use. This should not be needed in most cases.')
	parser.add_argument('--disk', help='Disk member inside an OVA archive (name or index).')
	parser.add_argument('--parent', action='append', default=[], help='Parent image for a VDI/QCOW2 differencing chain. Can be repeated.')
	parser.add_argument('--no-history', action='store_true', help='Do not parse history')
	parser.add_argument('url', help='Adiskreader connection URL')

	args = parser.parse_args()

	fs = await url_to_fs(
		args.url,
		args.pid,
		disk_member=args.disk,
		parent_paths=args.parent or None,
	)
	if fs is None:
		raise Exception('No suitable partition found!')
	
	rs = REGSecrets(fs)
	async for line in rs.run():
		print(line)

	ns = NTDSSecrets(fs, rs.result)
	ns.with_history = not args.no_history
	try:
		async for line in ns.run():
			print(line)
	except NTDSNotFoundError as e:
		print('[!] %s' % e, file=sys.stderr)
	
	



def main():
	asyncio.run(amain())

if __name__ == '__main__':
	main()
