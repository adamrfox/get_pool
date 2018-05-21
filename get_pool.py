#!/usr/bin/python

import socket
import sys
import papi
import json
import getpass
import netaddr

def get_pool_from_ip (data, addr):
  pool = ""
  addr_o = netaddr.IPAddress (addr)
  for i , inf in enumerate (data['pools']):
    for j, rng in enumerate (data['pools'][i]['ranges']):
      ip_range = list (netaddr.iter_iprange(data['pools'][i]['ranges'][j]['low'], data['pools'][i]['ranges'][j]['high']))
      if (addr_o in ip_range):
        pool = data['pools'][i]['id']
        return (pool)
  return (pool)

def get_addr_from_int (int_d, pool_d, pool):
  for x, p in enumerate (pool_d['pools']):
    if pool_d['pools'][x]['id'] == pool:
      for y, r in enumerate (pool_d['pools'][x]['ranges']):
        ip_range = list (netaddr.iter_iprange(pool_d['pools'][x]['ranges'][y]['low'],pool_d['pools'][x]['ranges'][y]['high']))
        for z, s in enumerate (int_d['ip_addrs']):
          ip_a = netaddr.IPAddress(int_d['ip_addrs'][z])
          if (ip_a in ip_range):
            return (int_d['ip_addrs'][z])

def get_addr_list_from_pool (ifs_d, pool_d,pool):
  found_addr = ""
  pf = pool.split ('.')
  for i, inf in enumerate (ifs_d['interfaces']):
    for j, own in enumerate (ifs_d['interfaces'][i]['owners']):
      if ifs_d['interfaces'][i]['owners'][j]['groupnet'] == pf[0] and ifs_d['interfaces'][i]['owners'][j]['subnet'] == pf[1] and ifs_d['interfaces'][i]['owners'][j]['pool'] == pf[2]:
        found_addr = get_addr_from_int(ifs_d['interfaces'][i], pool_d, pool)
        addr_list.append (found_addr)
        break
  return (addr_list)


pool = ""
addr_list = []
addr =  socket.gethostbyname(sys.argv[1])
user = raw_input ("User: ")
password = getpass.getpass ("Password: ")
path = "/platform/3/network/interfaces?sort=lnn&dir=ASC"
(status, reason, resp) = papi.call (addr, '8080', 'GET', path, 'any', '', 'application/json', user, password)
if (status != 200):
  print "Bad Status: " + status
  exit (status)
int_data = json.loads(resp)
#print json.dumps (int_data, indent=2, sort_keys=True)
path = "/platform/3/network/pools"
(status, reason, resp) = papi.call (addr, '8080', 'GET', path, 'any', '', 'application/json', user, password)
if status != 200:
  print "Bad Status: " + status
  exit (status)
pool_data = json.loads (resp)
pool = get_pool_from_ip (pool_data, addr)
addr_list = get_addr_list_from_pool (int_data, pool_data, pool)
print addr_list
