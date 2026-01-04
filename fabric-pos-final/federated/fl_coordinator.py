from hashlib import sha256

def submit_update(model_weights):
    h = sha256(model_weights.encode()).hexdigest()
    print("Submitting to BFT:", h)
