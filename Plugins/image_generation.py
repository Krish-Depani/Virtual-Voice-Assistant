import io
import warnings

from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

text = 'a biker on a path to heaven stars in background, hyper-realistic'

stability_api = client.StabilityInference(
    key='sk-3QeqTGswltCJpG9wfTAGNSMdb5ut6fqsKf4b1jdzCWxNppW6',
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