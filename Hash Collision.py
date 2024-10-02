import hashlib

# Function to generate hash using different algorithms
def generate_hash(input_string, algorithm='md5'):
    if algorithm == 'md5':
        return hashlib.md5(input_string.encode()).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(input_string.encode()).hexdigest()

# Example with MD5
input_1 = "hello"
input_2 = "Hello"  # Only difference is the case of 'H'

md5_hash_1 = generate_hash(input_1, 'md5')
md5_hash_2 = generate_hash(input_2, 'md5')

print(f"MD5 Hash of '{input_1}': {md5_hash_1}")
print(f"MD5 Hash of '{input_2}': {md5_hash_2}")

# Example with SHA1
sha1_hash_1 = generate_hash(input_1, 'sha1')
sha1_hash_2 = generate_hash(input_2, 'sha1')

print(f"\nSHA1 Hash of '{input_1}': {sha1_hash_1}")
print(f"SHA1 Hash of '{input_2}': {sha1_hash_2}")

# Hash collision example (MD5 is vulnerable to collisions)
collision_input_1 = "message1"
collision_input_2 = "message2"  # In real life, you'd need special crafted inputs

collision_hash_1 = generate_hash(collision_input_1, 'md5')
collision_hash_2 = generate_hash(collision_input_2, 'md5')

print(f"\nMD5 Hash of '{collision_input_1}': {collision_hash_1}")
print(f"MD5 Hash of '{collision_input_2}': {collision_hash_2}")
print(f"Is collision: {collision_hash_1 == collision_hash_2}")
