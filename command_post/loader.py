model = None

def get_model():
    global model
    if model is None:
        from command_post.model import Model
        model = Model()
    return model