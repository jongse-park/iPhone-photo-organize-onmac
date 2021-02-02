#/usr/bin/python

import os
import sys
from osxmetadata import OSXMetaData

def organize(org_path, target_path):

	if os.path.exists(target_path):
		os.system("rm -rf {}".format(target_path))
	os.mkdir(target_path)
	media_files = {}

	for dr in sorted(os.listdir(org_path)):
		if not os.path.isdir(org_path + "/" + dr):
			continue
		for f in os.listdir(org_path + "/" + dr):
			e = f.split(".")[1]
			p = org_path + "/" + dr + "/" + f
			metadata = meta = OSXMetaData(p)
			result = os.popen("mdls -name kMDItemContentCreationDate {}".format(p)).readlines()
			dt, t = result[0].split(" ")[2], result[0].split(" ")[3]
			y, m, d = dt.split("-")
			y_path = target_path + "/" + y
			m_path = y_path + "/" + m
			if not os.path.exists(y_path):
				os.mkdir(y_path)
			if not os.path.exists(m_path):
				os.mkdir(m_path)
			f_pre = "{}_{}".format(dt, t.replace(":", ""))
			if f_pre not in media_files.keys():
				media_files[f_pre] = []
			new_f = "{}_{}.{}".format(f_pre, len(media_files[f_pre]), e)
			media_files[f_pre].append(new_f)
			new_p = m_path + "/" + new_f
			os.popen("mv {} {}".format(p, new_p))

def main():
	if len(sys.argv) != 3:
		print ("Usage: python organize_originals.py [originals_directory_path] [target_directory_path]")
		sys.exit()

	org_path = sys.argv[1]
	target_path = sys.argv[2]

	if not os.path.exists(org_path):
		print ("Error: Path [{}] does not exist.".format(org_path))
		sys.exit()
	if "0" not in os.listdir(org_path):
		print ("Erorr: Path [{}] does not seem to be the proper \"originals\" directory path.".format(org_path))
		sys.exit()
	organize(org_path, target_path)

if __name__ == "__main__":
	main()