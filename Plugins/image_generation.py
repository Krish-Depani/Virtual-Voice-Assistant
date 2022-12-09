import io
import warnings
from dotenv import load_dotenv
import os
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

load_dotenv(dotenv_path='..\\Data\\.env')

DREAMSTUDIO = os.getenv('DREAMSTUDIO_API')

text = 'a biker on a path to heaven stars in background, hyper-realistic'


stability_api = client.StabilityInference(
    key=DREAMSTUDIO,
    verbose=True,
)

# the object returned is a python generator
answers = stability_api.generate(
    prompt=text,
    seed=34567, # if provided, specifying a random seed makes results deterministic
    steps=20, # defaults to 30 if not specified
)

# iterating over the generator produces the api response
for resp in answers:
    for artifact in resp.artifacts:
        if artifact.finish_reason == generation.FILTER:
            warnings.warn(
                "Your request activated the API's safety filters and could not be processed."
                "Please modify the prompt and try again.")
        if artifact.type == generation.ARTIFACT_IMAGE:
            img = Image.open(io.BytesIO(artifact.binary))
            img.show()

'''
stability_api = client.StabilityInference(
    key=DREAMSTUDIO,
    verbose=True,
)

# the object returned is a python generator
answers = stability_api.generate(
    prompt=text,
    seed=95456, # if provided, specifying a random seed makes results deterministic
)

# iterating over the generator produces the api response
for resp in answers:
    for artifact in resp.artifacts:
        if artifact.finish_reason == generation.FILTER:
            warnings.warn(
                "Your request activated the API's safety filters and could not be processed."
                "Please modify the prompt and try again.")
        if artifact.type == generation.ARTIFACT_IMAGE:
            img = Image.open(io.BytesIO(artifact.binary))
            img.show()
'''''