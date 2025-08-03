import dataclasses as dc
import json
import app.decorators.timing as decorator
import requests

from app.helper.utils.logger import Logger


@dc.dataclass
class LLMHandler:
    logger: Logger = Logger(name="LLMHandler", level="DEBUG")
    MODEL_NAME = "mistral"
    MODEL_ENDPOINT = "http://localhost:11434/api/generate"
    SYSTEM_PROMPT = """
    You are a question answering nutrition myth buster system which accepts a query and answers based on the context
    given along with a snippet related to the query. It is not necessary that you stick exactly inside the 
    context & the snippet. However, you should use the snippet for identifying the context of the query.
    
    SNIPPET: <<paragraph>>
    QUERY: <<query>>
    
    [EXAMPLE]
    SNIPPET:
    Caffeine intake below 400mg per day is considered safe by most health authorities.
    QUERY:
    Is it safe to drink 3 cups of coffee a day?
    ANSWER:
    {"result": "Yes, 3 cups of coffee a day are generally considered safe for most healthy adults,
    as it typically amounts to less than 400mg of caffeine."}
    
    CRITICAL : Do not add with the phrases starting with phrases that say if the query exists in the snippet or not. 
    Eg: "The provided snippet doesn't contain the information", "The provided snippet does not explicitly mention",
    While the snippet does not explicitly mention, etc. to the <<answer>> It is not necessary that you stick
    exactly inside the context & the snippet. It is also not necessary that the user need to know that
    the query doesn't exist in the snippet.
    
    Response should be as below -
    {"result": <<answer>>}
    """

    @decorator.timing
    def query_model(self, query, context):
        try:
            prompt_json = self.prepare_prompt(query, context)

            response = requests.post(self.MODEL_ENDPOINT, json=prompt_json)

            if response.status_code != 200:
                response.raise_for_status()

            self.logger.info(f"Query response: {response.text}")

            return json.loads(response.json()["response"].strip())
        except Exception as e:
            self.logger.exception(f"Query failed with error: {e}")
            return {}

    @decorator.timing
    def prepare_prompt(self, query: str, context: list) -> dict:
        """
        Prepare prompt json integrating the query, context & system prompt
        """

        prompt = self.SYSTEM_PROMPT.replace("<<query>>", query)
        prompt = prompt.replace("<<context>>", "\n\n".join(context))

        request_body = {
            "model": self.MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }

        return request_body
