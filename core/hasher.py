import hashlib

def hash_file(filepath, algorithm="sha256"):
    h = hashlib.new(algorithm)

    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(4096):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        return None