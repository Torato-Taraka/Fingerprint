import donna25519 as curve25519
import binascii
import hashlib

print()
print('指纹字符串为：010011011011011000011100000100')
x = hashlib.sha256('010011011011011000011100000100'.encode('utf-8')).hexdigest()
print('sha256加密后的32字节私钥为：', x)
x = binascii.unhexlify(x)

private = curve25519.PrivateKey(x)
public = private.get_public()
#print('Curve25519加密后的私钥为：', int(binascii.hexlify(private.private), 16))
print('Curve25519加密后的公钥为：', str(hex(int(binascii.hexlify(public.public), 16))).replace('0x',''))
