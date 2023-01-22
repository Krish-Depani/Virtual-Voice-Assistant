import io
from dotenv import load_dotenv
import os
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

load_dotenv(dotenv_path='..\\Data\\.env')

DREAMSTUDIO = os.getenv('DREAMSTUDIO_API')

def generate_image(text):
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
                print("WARNING: Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
                return
            elif artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.show()