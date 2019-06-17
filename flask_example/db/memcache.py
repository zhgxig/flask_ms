import time

from libmc import (
    Client, MC_HASH_MD5, MC_POLL_TIMEOUT, MC_CONNECT_TIMEOUT, MC_RETRY_TIMEOUT
)

mc = Client(
    ['127.0.0.1:11211', '127.0.0.1:11212'], do_split=True,
    comp_threshold=0, noreply=False, prefix=None,
    hash_fn=MC_HASH_MD5, failover=False
)

mc.config(MC_POLL_TIMEOUT, 100)  # 100 ms
mc.config(MC_CONNECT_TIMEOUT, 300)  # 300 ms
mc.config(MC_RETRY_TIMEOUT, 5)  # 5 s


if __name__ == "__main__":
    from pprint import pprint
    # res_data = mc.set("today", "hehe", 100)
    # print(res_data)
    t0 = time.time()
    res = mc.get("today")
    print("res={}".format(res))
    pprint(dir(mc))
    # print(mc.config())
    t1 = time.time()
    print("cost_time={}".format(t1-t0))