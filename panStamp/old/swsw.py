from struct import *
import hashlib
import socket
import sys
import re
import json
import base64
import numpy
import pylab
import logging

s2b = lambda s: s.encode('latin_1')
ver = None
peer = None

def tostring(data):
    dtype=type(data).__name__
    if dtype=='ndarray':
        if pylab.shape(data)!=(): data=list(data)
        else: data='"'+data.tostring()+'"'
    elif dtype=='dict' or dtype=='tuple':
        try: data=json.dumps(data)#'"'+unicode(data)+'"'
        except: pass
    elif dtype=='NoneType':
        data=''
    elif dtype=='str' or dtype=='unicode':
        data=json.dumps(data)#'"'+unicode(data)+'"'
    
    return str(data)

def part(token):
    digits=""
    for d in re.compile('[0-9]').findall(token):
        digits = digits + str(d)
    count=0
    for s in re.compile(' ').findall(token):
        count = count + 1
    return int(int(digits)/count)

def handshake(data):
    global ver
    
    var = re.compile("Sec-WebSocket-Version: (.*)\r\n").findall(data)
    ver = var[0] if len(var)!=0 else 0
    
    if ver==0: return handshake_hybi00(data)
    return handshake_hybi10(data)

def encode(data):
    global ver
    
    if ver == 0: return encode_hybi00(data)
    return encode_hybi10(data)

def decode(data):
    global ver
    
    if ver == 0: return decode_hybi00(data)
    return decode_hybi10(data)
	
def handshake_hybi00(data):
    bytes = data[len(data)-8:]
    var = re.compile("GET (.*) HTTP").findall(data)
    resource = var[0] if len(var)!=0 else ''
    var = re.compile("Host: (.*)\r\n").findall(data)
    host = var[0] if len(var)!=0 else ''
    var = re.compile("Origin: (.*)\r\n").findall(data)
    origin = var[0] if len(var)!=0 else ''
    var = re.compile("Sec-WebSocket-Key1: (.*)\r\n").findall(data)
    key1 = var[0] if len(var)!=0 else ''
    var = re.compile("Sec-WebSocket-Key2: (.*)\r\n").findall(data)
    key2 = var[0] if len(var)!=0 else ''

    challenge = pack('>II', part(key1), part(key2)) + ''.join([ pack('>B', ord( x )) for x in bytes ])

    hash = hashlib.md5(challenge).digest()

    return "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"+"Upgrade: WebSocket\r\n"+"Connection: Upgrade\r\n"+"Sec-WebSocket-Origin: "+origin+"\r\n"+"Sec-WebSocket-Location: "+" ws://"+host+resource+"\r\n\r\n".encode('latin-1')+hash

def handshake_hybi10(data):
    bytes = data[len(data)-8:]
    var = re.compile("GET (.*) HTTP").findall(data)
    resource = var[0] if len(var)!=0 else ''
    var = re.compile("Host: (.*)\r\n").findall(data)
    host = var[0] if len(var)!=0 else ''
    var = re.compile("Origin: (.*)\r\n").findall(data)
    origin = var[0] if len(var)!=0 else ''
    var = re.compile("Sec-WebSocket-Key: (.*)\r\n").findall(data)
    key = var[0] if len(var)!=0 else ''

    magickey = key+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    hash = base64.b64encode(hashlib.sha1(magickey).digest())

    return "HTTP/1.1 101 Switching Protocols\r\n"+"Upgrade: websocket\r\n"+"Connection: Upgrade\r\n"+"Sec-WebSocket-Accept: "+hash+"\r\n\r\n"
	
def encode_hybi00(data):
    return b"\x00" + data.encode('utf-8') + b"\xff"

def decode_hybi00(data):
    return data.decode('utf-8', 'ignore').replace('\x00','')
	
def encode_hybi10(buf, opcode=0x1, base64=False):
	""" Encode a HyBi style WebSocket frame.
	Optional opcode:
		0x0 - continuation
		0x1 - text frame (base64 encode buf)
		0x2 - binary frame (use raw buf)
		0x8 - connection close
		0x9 - ping
		0xA - pong
	"""
	if base64:
		buf = base64.b64encode(buf)

	b1 = 0x80 | (opcode & 0x0f) # FIN + opcode
	payload_len = len(buf)
	if payload_len <= 125:
		header = pack('>BB', b1, payload_len)
	elif payload_len > 125 and payload_len < 65536:
		header = pack('>BBH', b1, 126, payload_len)
	elif payload_len >= 65536:
		header = pack('>BBQ', b1, 127, payload_len)
    
	return header + buf.encode('utf-8')

def unmask(buf, f):
	pstart = f['hlen'] + 4
	pend = pstart + f['length']
	if numpy:
		b = c = s2b('')
		if f['length'] >= 4:
			mask = numpy.frombuffer(buf, dtype=numpy.dtype('<u4'),
					offset=f['hlen'], count=1)
			data = numpy.frombuffer(buf, dtype=numpy.dtype('<u4'),
					offset=pstart, count=int(f['length'] / 4))
			b = numpy.bitwise_xor(data, mask).tostring()

		if f['length'] % 4:
			mask = numpy.frombuffer(buf, dtype=numpy.dtype('B'),
					offset=f['hlen'], count=(f['length'] % 4))
			data = numpy.frombuffer(buf, dtype=numpy.dtype('B'),
					offset=pend - (f['length'] % 4),
					count=(f['length'] % 4))
			c = numpy.bitwise_xor(data, mask).tostring()
		return b + c
	else:
		data = array.array('B')
		mask = s2a(f['mask'])
		data.fromstring(buf[pstart:pend])
		for i in range(len(data)):
			data[i] ^= mask[i % 4]
		return data.tostring()

def decode_hybi10(buf, base64=False):
	""" Decode HyBi style WebSocket packets.
	Returns:
		{'fin'          : 0_or_1,
		 'opcode'       : number,
		 'mask'         : 32_bit_number,
		 'hlen'         : header_bytes_number,
		 'length'       : payload_bytes_number,
		 'payload'      : decoded_buffer,
		 'left'         : bytes_left_number,
		 'close_code'   : number,
		 'close_reason' : string}
	"""

	f = {'fin'          : 0,
		 'opcode'       : 0,
		 'mask'         : 0,
		 'hlen'         : 2,
		 'length'       : 0,
		 'payload'      : None,
		 'left'         : 0,
		 'close_code'   : None,
		 'close_reason' : None}

	blen = len(buf)
	f['left'] = blen

	if blen < f['hlen']:
		return f 

	b1, b2 = unpack_from(">BB", buf)
	f['opcode'] = b1 & 0x0f
	f['fin'] = (b1 & 0x80) >> 7
	has_mask = (b2 & 0x80) >> 7

	f['length'] = b2 & 0x7f
	
	if f['length'] == 126:
		f['hlen'] = 4
		if blen < f['hlen']:
			return f 
		(f['length'],) = unpack_from('>xxH', buf)
	elif f['length'] == 127:
		f['hlen'] = 10
		if blen < f['hlen']:
			return f 
		(f['length'],) = unpack_from('>xxQ', buf)

	full_len = f['hlen'] + has_mask * 4 + f['length']
	
	if blen < full_len:
		return f 

	f['left'] = blen - full_len
	
	if has_mask:
		f['mask'] = buf[f['hlen']:f['hlen']+4]
		f['payload'] = unmask(buf, f)
	else:
		print("Unmasked frame: %s" % repr(buf))
		f['payload'] = buf[(f['hlen'] + has_mask * 4):full_len]

	if base64 and f['opcode'] in [1, 2]:
		try:
			f['payload'] = base64.b64decode(f['payload'])
		except:
			print("Exception while b64decoding buffer: %s" %
					repr(buf))
			raise
	
	if f['opcode'] == 0x08:
		if f['length'] >= 2:
			f['close_code'] = unpack_from(">H", f['payload'])
		if f['length'] > 3:
			f['close_reason'] = f['payload'][2:]
	
	return unicode(f['payload'],'utf-8')



def connect(addr="127.0.0.1", port=9999):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((addr, port))  
    sock.listen(0)  
    
    print "LISTENING ON PORT " + str(port)
    
    global peer
    
    peer, info = sock.accept()
    
    peer.send(handshake(peer.recv(256)))
    
    print "ACCEPTED CONNECTION FROM " + info[0]
    print "_____________________________"

    return (peer, info)

def send(peer, res):
    print "< " + res
    logging.info("< " + res)
    peer.send(encode(res))

def handle(peer, sigterm="DISCONNECTED", callback=(lambda msg: msg)):
    while True:
        try: 
            req=decode(peer.recv(256))
            
            if req!='':
                if req.find(sigterm)>=0: break
            
                cmds=re.compile('\)[a-z]|\)[A-Z]').findall(req)
                ncmds=len(cmds)+1
                
                for i in range(0,ncmds):
                    if i==(ncmds-1): cmd=req
                    else:
                        end=req.find(cmds[i])+1
                        cmd=req[:end]
                        req=req[end:]
                    
                    print "> " + cmd
                    logging.info("> " + cmd)
                
                    res=callback(cmd)
                    if res != '':
                        send(peer, res)
        except socket.error: break
        except Exception as e: print e
        
    try:
        peer.shutdown(socket.SHUT_RDWR)
    except:
        pass
    finally:
        peer.close()
        print sigterm

if __name__=='__main__':
    handle(connect()[0])