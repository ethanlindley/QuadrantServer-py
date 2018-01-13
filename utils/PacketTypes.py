"""
PacketTypes module will contain all of the packets that are used for
server and client communication. More packets will be added as the server continues
to develop.
"""

policy_file_req = "<policy-file-request/>\0"
policy_file_res = "<cross-domain-policy><allow-access-from domain='*' to-ports='*' /></cross-domain-policy>\0"

api_ver_chk_req = "<body action='verChk' r='0'>"
api_OK = "<msg t='sys'><body action='apiOK' r='0'></body></msg>\0"
api_KO = "<msg t='sys'><body action='apiKO' r='0'></body></msg>\0"
