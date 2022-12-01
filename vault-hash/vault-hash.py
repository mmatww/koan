import hashlib
import json
import sys

HASH_TYPE = 'sha256'

if __name__ == '__main__':
    with open(sys.argv[1]) as ff:
        data = json.load(ff)
        print("Cluster,Namespace,App,Key,Hash")
        for ii in data:
            pp = ii.split("/")
            if len(pp) > 5 and pp[5] == "wectl":
                for jj in data[ii]:
                    hh = hashlib.new(HASH_TYPE)
                    hh.update(data[ii][jj].encode())
                    vv = hh.hexdigest()
                    print(f"{pp[3]},{pp[2]},{pp[4]},{jj},{vv}")

